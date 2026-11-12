"""Mechanical defaults in SI units; controller positions use mm."""

from dataclasses import dataclass

HX_URL = "https://cdn.sparkfun.com/assets/0/2/7/d/1/HX711_datasheet.pdf"
ADS_URL = "https://www.ti.com/lit/ds/symlink/ads1220.pdf"
# rate, settling periods, input-referred RMS noise V, input full scale V
# IDEAL_1000 is the synthetic baseline.
ADC_MODELS = {
    # Synthetic reference: no averaging, bridge vibration or electrical noise.
    "IDEAL_1000": (1000, 0, 0.0, 2.048 / 128),
    # datasheet: HX_URL, p. 3, gain 128 and settling footnote.
    "HX711_10": (10, 4, 50e-9, 5 / 256),
    "HX711_80": (80, 4, 90e-9, 5 / 256),
    # datasheet: ADS_URL, Table 7-1, gain 128; settling in 8.3.6.
    "ADS1220_330": (330, 1, 0.34e-6, 2.048 / 128),
    "ADS1220_1000": (1000, 1, 0.70e-6, 2.048 / 128),
    # datasheet: ADS_URL, Table 7-5, gain 128, turbo; settling in 8.3.6.
    "ADS1220_2000": (2000, 1, 0.82e-6, 2.048 / 128),
}


@dataclass
class Params:
    """Physical assumptions in SI units unless a field comment specifies otherwise."""

    lead: float = 0.010  # mm/rev
    efficiency: float = 0.9
    kt: float = 0.1  # N m/A
    rotor_j: float = 1.2e-5  # kg m^2
    max_current: float = 8  # A
    current_tau: float = 0.0005  # s
    carriage_mass: float = 6  # kg
    coulomb: float = 10  # N
    friction_smoothing: float = 0.001  # m/s
    viscous: float = 50  # N/(m/s)
    server_mass: float = 25  # kg
    rail_mu: float = 0.1
    gravity: float = 9.81  # m/s^2
    pusher_k: float = 200  # N/mm
    damping_ratio: float = 0.05
    mate_start: float = 280  # mm
    mate_rise_end: float = 290  # mm
    connector_peak: float = 90  # N
    connector_hold: float = 60  # N
    end_stop: float = 295  # mm
    end_k: float = 500  # N/mm
    x_jam: float = 150  # mm
    k_jam: float = 100  # N/mm
    encoder_lines: int = 2048  # lines/rev
    quadrature: int = 4
    cell_rating: float = 500  # N
    cell_mv_v: float = 2  # mV/V
    excitation: float = 5  # V
    vibration_rms: float = (
        2  # N RMS per plant sample
    )
    vibration_amp: float = 5  # N
    vibration_hz: float = 150  # Hz
    dt: float = 0.0001  # s
    control_dt: float = 0.001  # s
    baud: int = 115200
    seed: int = 42
