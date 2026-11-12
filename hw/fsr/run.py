"""Independent divider/filter netlists and fresh DC/transient verification."""
from pathlib import Path
import csv
import json
import numpy as np
from hw.spice import simulate_released
from sim.fsr import FRONT_ENDS, VREF, resistance, static_channel

ROOT = Path(__file__).resolve().parent


def netlist(name, force=10, transient=False):
    c = FRONT_ENDS[name]
    source = "PULSE(0 3.3 1m 1n 1n 10m 20m)" if transient else str(VREF)
    analysis = ".tran 1u 5m 0 1u" if transient else ".op"
    return f"""Independent resistive force divider: {name}; all components assumed
Vexc supply 0 {source}
Rforce supply divider {resistance(force):.17g}
Rdown divider 0 {c.pulldown_ohm}
Rfilter divider adc {c.series_ohm}
Cfilter adc 0 {c.capacitance_F}
.options reltol=1e-7 abstol=1e-12
{analysis}
.end
"""


def run():
    ROOT.mkdir(exist_ok=True)
    rows = []
    for name in FRONT_ENDS:
        (ROOT/f"{name}.cir").write_text(netlist(name), encoding="ascii")
        for force in (.2, .5, 1, 2, 5, 10, 15, 20, 35, 50):
            actual = float(simulate_released(netlist(name, force))["adc"][-1])
            expected = static_channel(force, name)
            rows.append(dict(channel=name, force_N=force, spice_V=actual,
                             analytic_V=expected["node_volts"],
                             error_V=actual-expected["node_volts"],
                             adc_code=round(4095*actual/VREF),
                             tau_ms=expected["tau_ms"]))
        circuit = netlist(name, transient=True)
        (ROOT/f"{name}_step.cir").write_text(circuit, encoding="ascii")
        d = simulate_released(circuit)
        with (ROOT/f"{name}_step.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["time_s", "adc_V"])
            w.writerows(zip(d["time"], d["adc"]))
    with (ROOT/"dc.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    result = dict(dc_points=len(rows), max_dc_error_V=max(abs(r["error_V"]) for r in rows))
    (ROOT/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result))


if __name__ == "__main__":
    run()
