"""Check independent netlists against voltage division and the RC step law."""
import numpy as np
import pytest
from hw.fsr.run import netlist
from hw.spice import simulate_released
from sim.fsr import FRONT_ENDS, static_channel


@pytest.mark.parametrize("channel", FRONT_ENDS)
def test_solver_dc_and_step(channel):
    expected = static_channel(10, channel)
    dc = simulate_released(netlist(channel))["adc"][-1]
    assert dc == pytest.approx(expected["node_volts"], abs=1e-6)
    d = simulate_released(netlist(channel, transient=True))
    elapsed = d["time"]-.001
    selected = elapsed > 1e-6
    exact = expected["node_volts"]*(1-np.exp(-elapsed[selected]/(expected["tau_ms"]/1000)))
    assert np.max(np.abs(d["adc"][selected]-exact)) < .002
