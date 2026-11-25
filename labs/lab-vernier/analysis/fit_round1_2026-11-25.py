"""Round-1 (2026-11-25) research runs 001-019 and 006-017 pair fits, lab-vernier, round 2.

Per run: fit P = 2.5 coefficient(s) by pure-python RK4 (fit_tools.fit_couplings) over a pre-contact
window: t <= first time the measured separation drops below 1.5 (A-A and C-C attract and can close).
A-C runs (repulsive) use the full window, cut at the same rule for safety.
Pre-registered A-C predictions (from notebook round 1): K_AC(2.75)=-8.94, K_CA(2.75)=-21.08;
K_AC(3.25)=-9.08, K_CA(3.25)=-21.54; K_AC(3.0)=-9.06, K_CA(3.0)=-21.32.
Run: python3 -I fit_round1_2026-11-25.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit_tools as ft  # noqa: E402

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
DATE = "2026-11-25/r1/lab-vernier"

RUNS = {
    "AC": [("001", 2.75, "H"), ("002", 2.75, "V"), ("003", 3.25, "H"), ("004", 3.25, "V"),
           ("005", 3.0, "D"), ("018", 2.5, "D"), ("019", 3.5, "D")],
    "AA": [("006", 2.5, "H"), ("007", 2.5, "V"), ("008", 3.0, "H"), ("009", 3.0, "V"),
           ("010", 3.5, "H"), ("011", 3.5, "V")],
    "CC": [("012", 2.5, "H"), ("013", 2.5, "V"), ("014", 3.0, "H"), ("015", 3.0, "V"),
           ("016", 3.5, "H"), ("017", 3.5, "V")],
}
PRED_AC = {2.75: (-8.94, -21.08), 3.25: (-9.08, -21.54), 3.0: (-9.06, -21.32)}


def cut_time(setup, res, rmin=1.5):
    """First sample time where the measured separation is below rmin (fit window ends before it)."""
    for s in res["samples"]:
        p = s["particles"]
        if math.dist(p[0]["pos"], p[1]["pos"]) < rmin:
            return s["t"]
    return None


def fit(pair, rid):
    req = ft.load_json(f"{REPO}/requests/{rid}.json")
    res = ft.load_json(f"{REPO}/results/{rid}.json")
    setup = req["setup"]
    sp = [p["species"] for p in setup["particles"]]
    cut = cut_time(setup, res)
    tmax = (cut - 1e-9) if cut is not None else None
    if pair == "AC":
        keys = [("A", "C"), ("C", "A")]
        coup0 = {("A", "C"): -8.5, ("C", "A"): -21.0}
        bounds = {k: (-40.0, 0.0) for k in keys}
    elif pair == "AA":
        keys = [("A", "A")]
        coup0 = {("A", "A"): 17.0}
        bounds = {("A", "A"): (0.0, 40.0)}
    else:
        keys = [("C", "C")]
        coup0 = {("C", "C"): 12.0}
        bounds = {("C", "C"): (0.0, 40.0)}
    coup, mse = ft.fit_couplings(setup, res, coup0, keys, bounds, P=2.5, tmax=tmax, tmin=0.0, sweeps=3)
    return coup, math.sqrt(mse), tmax, cut, sp


def main():
    for pair, items in RUNS.items():
        for num, r0, orient in items:
            rid = f"{DATE}/{num}"
            coup, rms, tmax, cut, sp = fit(pair, rid)
            tag = " ".join(f"K{k[0]}({k[1]})={v:.3f}" for k, v in coup.items())
            extra = ""
            if pair == "AC":
                pa, pc = PRED_AC.get(r0, (None, None))
                if pa is not None:
                    extra = f" pred K_AC={pa} K_CA={pc}"
            print(f"{num} {pair} r0={r0} {orient} cut={cut} tmax={tmax} {tag} rms/coord={rms:.4f}{extra}",
                  flush=True)


if __name__ == "__main__":
    main()
