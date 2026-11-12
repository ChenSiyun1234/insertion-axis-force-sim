# Simulation architecture

I model a compact linear end-effector axis and a heavier insertion fixture. The
case identifier `arm` denotes the compact linear axis; `rack` denotes the
heavier fixture. Both use prismatic joints. I build both scenes from boxes and a plane in `sim3d/scene.py`.
All physical and interface choices are catalogued in [ASSUMPTIONS.md](ASSUMPTIONS.md).

The Python host sends framed commands through a bandwidth-limited UART model.
The C controller implements CRC checking, parameter validation, stationary tare,
a velocity PI loop, seating detection, force envelopes, fault latching, homing,
and unloading backoff. `docs/INTERFACE.md` documents the wire protocol and native
ABI. `firmware/include/pin_plan.h` lists the simulated logical pin assignments.
The portable C sources have no device-register dependency.

The force node evaluates an assumed resistive force curve, divider, and filter.
`sim/fsr.py` advances the exact held-force RC response at each integration step,
then quantizes a noisy voltage to an unsigned code. The controller inverts the
same calibration. `hw/fsr/run.py` independently constructs plain-device netlists
and uses ngspice for DC and excitation-step comparisons. ADC acquisition loading,
hysteresis and temperature are outside this model.

`sim/can_bus.py` computes classic CAN framing, CRC, bit stuffing, arbitration,
finite transmit queues, receive FIFOs, retries and bus-off behavior. Synthetic
traffic in `sim/can_traffic.py` places the force node and controller on a shared
bus. Encoders remain local. The controller consumes the latest delivered sample.
The periodic traffic sweep records held-reading age separately from delivery age.
Synthetic error injection and finite buffers are selected experiment conditions.

`sim3d/mj_plant.py` integrates the mechanisms. The compact fixture uses native
box contacts with a calibrated compliant patch; the heavy fixture applies an
explicit contact law matching the reference integrator. Motor current commands
use a first-order lag. The alternate PWM model solves the held-speed electrical
step and includes back-EMF. A sign error detector can identify an individual motor
or encoder reversal; coordinated reversal can preserve the loop's apparent sign.

`experiments/run_all.py` generates the heavier reference fixture's ADC, speed,
compliance, envelope and filter sweeps. `sim3d/cases.py` writes traces, replay
positions, closed-loop metrics, delay tables and CAN statistics. Rendered media
replay those saved positions. Generated results belong in `results/` and the
independent electrical results in `hw/`. The electrical input and brake models
are separate circuit studies and have no coupling to axis motion.

I compile the controller for the selected embedded target and evaluate the
circuit models across their stated tolerance corners.
