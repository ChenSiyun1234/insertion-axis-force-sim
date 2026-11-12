"""Linear insertion fixtures built from primitive geometry."""

from dataclasses import dataclass
import math
import mujoco as mj
from sim.params import Params


@dataclass(frozen=True)
class ArmParams:
    carriage_mass: float = 2.0  # kg
    module_mass: float = 2.0  # kg
    lead: float = .010  # m/rev
    gap: float = .010  # m
    friction: float = 4.0  # N
    latch_peak: float = 20.0  # N
    latch_hold: float = 8.0  # N
    latch_length: float = .008  # m
    end: float = .040  # m
    end_k: float = 500000.0  # N/m
    jam_at: float = .020  # m
    jam_k: float = 20000.0  # N/m
    contact_k: float = 20000.0  # N/m
    damping_ratio: float = .05
    kt: float = .060  # Nm/A
    gear: float = 1.0  # direct screw drive
    efficiency: float = .80
    rotor_j: float = 1.2e-5  # kg m^2
    current_tau: float = .0005  # s
    max_current: float = 4.0  # A
    joint_friction: float = 1.0  # N
    encoder_counts: int = 4096  # counts/rev

    @property
    def radius(self):
        # Equivalent transmission radius converts motor angle to linear travel.
        return self.lead/(2*math.pi)

    @property
    def max_tip_force(self):
        return self.kt*self.gear*self.efficiency*self.max_current/self.radius

    @property
    def counts_per_m(self):
        return self.encoder_counts*self.gear/self.lead


ARM = ArmParams()


def box(body, name, pos, size, mass=0, color=(.5, .6, .7, 1)):
    return body.add_geom(name=name, type=mj.mjtGeom.mjGEOM_BOX, pos=pos,
                         size=size, mass=mass, rgba=color, contype=0, conaffinity=0)


def build(case, jam=False, parameters=None):
    if case not in ("arm", "rack"):
        raise ValueError(case)
    p = parameters or Params()
    a = ARM
    spec = mj.MjSpec()
    spec.modelname = "generic_linear_insertion"
    spec.option.timestep = p.dt
    spec.option.gravity = [0, 0, 0]
    spec.worldbody.add_light(pos=[0, -1, 2], dir=[0, 0, -1])
    spec.worldbody.add_geom(type=mj.mjtGeom.mjGEOM_PLANE, size=[2, 2, .1],
                            rgba=[.12, .15, .19, 1], contype=0, conaffinity=0)
    base = spec.worldbody.add_body(name="fixture", pos=[0, 0, .50])
    box(base, "base_plate", [.20, 0, -.07], [.40, .15, .02], color=[.3, .34, .4, 1])
    for y in (-.09, .09):
        box(base, "", [.20, y, -.035], [.35, .01, .015], color=[.7, .74, .8, 1])
    controller = base.add_body(name="controller", pos=[-.13, .11, .02])
    box(controller, "controller_box", [0, 0, 0], [.06, .03, .025], color=[.15, .6, .45, 1])
    for name, pos, axes in [
        ("overview", [1.1, -1.3, 1.3], [1, .5, 0, -.25, .5, 1]),
        ("rack_view", [.7, -1.2, 1.1], [1, 0, 0, 0, .5, 1])]:
        spec.worldbody.add_camera(name=name, pos=pos, xyaxes=axes)
    carriage = base.add_body(name="arm_tool" if case == "arm" else "axis_carriage")
    drive_name = "axis_slide"
    radius = a.radius if case == "arm" else p.lead/(2*math.pi)
    rotor = a.rotor_j if case == "arm" else p.rotor_j
    carriage.add_joint(name=drive_name, type=mj.mjtJoint.mjJNT_SLIDE,
                       axis=[1, 0, 0], armature=rotor/radius**2,
                       frictionloss=a.joint_friction if case == "arm" else 0)
    box(carriage, "carriage", [-.06, 0, 0], [.05, .06, .025],
        a.carriage_mass if case == "arm" else p.carriage_mass, [.2, .5, .85, 1])
    if case == "rack":
        load = base.add_body(name="server")
        load.add_joint(name="server_slide", type=mj.mjtJoint.mjJNT_SLIDE, axis=[1, 0, 0])
        box(load, "load", [.10, 0, 0], [.10, .08, .04], p.server_mass, [.8, .75, .5, 1])
        box(base, "end_stop", [p.end_stop/1000+.22, 0, 0], [.02, .12, .06])
        names = dict(drive_joint=drive_name, load_joint="server_slide")
    else:
        box(carriage, "tool_pad", [-.004, 0, 0], [.004, .025, .025], color=[.9, .5, .12, 1])
        load = base.add_body(name="module", pos=[a.gap+.020, 0, 0])
        load.add_joint(name="module_slide", type=mj.mjtJoint.mjJNT_SLIDE,
                       axis=[1, 0, 0], frictionloss=a.friction)
        box(load, "module_case", [0, 0, 0], [.020, .040, .040], a.module_mass, [.8, .75, .5, 1])
        box(base, "end_stop", [a.gap+.040+a.end+.015, 0, 0], [.015, .10, .06])
        preliminary = spec.compile()
        effective_mass = a.carriage_mass+a.rotor_j/a.radius**2
        reduced = effective_mass*a.module_mass/(effective_mass+a.module_mass)
        damping = 2*a.damping_ratio*math.sqrt(a.contact_k*reduced)
        inverse_weight = sum(preliminary.body_invweight0[preliminary.body(n).id, 0]
                             for n in ("arm_tool", "module"))
        impedance = .001  # contact regularization
        # Parallel box faces have four native contact points; share patch stiffness.
        scale = (1-impedance)*inverse_weight/4
        spec.add_pair(name="pad_module", geomname1="tool_pad", geomname2="module_case",
                      condim=1, solimp=[impedance, impedance, .001, .5, 2],
                      solref=[-a.contact_k*scale, -damping*scale])
        names = dict(drive_joint=drive_name, load_joint="module_slide",
                     contact_geoms=("tool_pad", "module_case"), damping=damping)
    if jam:
        x = a.gap+.04+a.jam_at if case == "arm" else p.x_jam/1000+.20
        box(base, "jam_marker", [x, .06, 0], [.008, .025, .04], color=[.95, .22, .12, 1])
    return spec.compile(), names
