"""Generic resistive force sensor, divider, filter and unsigned ADC."""

from dataclasses import dataclass
import math

import numpy as np

from .sensors import Sensors

# Interlink FSR 400 Series datasheet, pp. 2-3: typical curve (N, ohm).
# Digitized with g = 9.81 m/s^2; source link in docs/ASSUMPTIONS.md.
CURVE_POINTS = ((0.3, 62000), (0.5, 29000), (1, 15000), (2, 8500),
                (5, 4300), (10, 2550), (20, 1500))
_slope, _intercept = np.polyfit(np.log(np.array(CURVE_POINTS)[:, 0]),
                             np.log(np.array(CURVE_POINTS)[:, 1]), 1)
FSR_A, FSR_B = float(np.exp(_intercept)), float(-_slope)
ACTUATION_N = 0.2  # Datasheet typical minimum actuation force.
OFF_OHM = 10e6  # Assumed finite open approximation; datasheet specifies >10 MOhm.
VREF = 3.3  # Assumed VDDA = VREF+ = sensor excitation, V.
FULL_SCALE = 4095  # Unsigned 12-bit ADC.


@dataclass(frozen=True)
class FrontEnd:
    pulldown_ohm: float
    series_ohm: float
    capacitance_F: float


FRONT_ENDS = {"standard": FrontEnd(3300, 1000, 47e-9),
              "slow": FrontEnd(6800, 4700, 220e-9),
              "sensitive": FrontEnd(1500, 680, 22e-9)}


def resistance(force_N):
    # Power-law extrapolation above the 20 N datasheet curve.
    return OFF_OHM if force_N < ACTUATION_N else FSR_A * force_N ** -FSR_B


def static_channel(force_N, revision="standard"):
    """Return DC transfer and local differential N/LSB (before quantisation)."""
    circuit = FRONT_ENDS[revision]
    r = resistance(force_N)
    pd = circuit.pulldown_ohm
    volts = VREF * pd / (pd + r)
    code = FULL_SCALE * volts / VREF
    sensitivity = (force_N * (pd+r)**2 / (FULL_SCALE*pd*FSR_B*r)
                   if force_N >= ACTUATION_N else math.inf)
    return dict(fsr_ohm=r, node_volts=volts, ideal_code=code,
                N_per_LSB=sensitivity,
                tau_ms=(circuit.series_ohm + pd*r/(pd+r))*circuit.capacitance_F*1000)


class FSRSensors:
    """Exact held-force RC update at plant rate, then one ADC sample per tick."""

    rate = 1000  # One conversion per firmware tick.
    window = 0
    counts_per_N = 1  # Unused bridge calibration, retained for the SIL interface.

    def __init__(self, parameters, revision="standard"):
        self.parameters, self.revision = parameters, revision
        self.voltage = 0.0  # Assumed initially discharged capacitor at power-on.
        self.next_ready = 1 / self.rate
        self.code = 0
        self.codes = []
        self.rng = np.random.default_rng(parameters.seed)

    encoder = Sensors.encoder

    def advance_voltage(self, force_N, dt):
        channel = static_channel(force_N, self.revision)
        decay = math.exp(-dt / (channel["tau_ms"] / 1000))
        self.voltage = channel["node_volts"] + (self.voltage-channel["node_volts"])*decay
        return self.voltage

    def step(self, plant, time_s, stop=False, full=False):
        self.advance_voltage(plant.force, self.parameters.dt)
        if time_s + 1e-9 < self.next_ready:
            return False
        self.next_ready += 1 / self.rate
        if stop:
            return False
        # 1.5 LSB RMS ADC noise; RC state persists between conversions.
        self.code = FULL_SCALE if full else max(0, min(FULL_SCALE, round(
            FULL_SCALE*self.voltage/VREF + self.rng.normal(0, 1.5))))
        self.codes.append(self.code)
        return True
