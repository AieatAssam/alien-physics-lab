"""Per-run two-coupling fit for A-C pairs at rest (lab-vernier, 2026-11-25).

Fits K_A(C) (A accelerated toward C, negative = away) and K_C(A) with P = 2.5 fixed, on the
full window of each run, using fit_tools.fit_couplings (pure python, RK4 with walls).
Compares with P-0005's separation-5 values K_A(C) = -8.77, K_C(A) = -21.25.

Run: python3 -I fit_AC_sep_2026-11-25.py
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit_tools as ft  # noqa: E402

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
RUNS = [
    "2026-11-24/r3/lab-vernier/%03d" % i for i in range(1, 11)
]
P0005 = {("A", "C"): -8.77, ("C", "A"): -21.25}

rows = []
for rid in RUNS:
    req = ft.load_json(f"{REPO}/requests/{rid}.json")
    res = ft.load_json(f"{REPO}/results/{rid}.json")
    setup = req["setup"]
    sep = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])
    coup0 = {("A", "C"): -8.0, ("C", "A"): -20.0}
    bounds = {("A", "C"): (-40.0, 0.0), ("C", "A"): (-40.0, 0.0)}
    coup, mse = ft.fit_couplings(setup, res, coup0, list(coup0), bounds, P=2.5,
                                 tmax=None, tmin=0.0, sweeps=3)
    rms = math.sqrt(mse)
    rows.append((rid, sep, setup["duration"], coup[("A", "C")], coup[("C", "A")], rms))
    print(f"{rid} sep={sep:.2f} T={setup['duration']} K_A(C)={coup[('A','C')]:.3f} "
          f"K_C(A)={coup[('C','A')]:.3f} rms/coord={rms:.4f} "
          f"ratio A={coup[('A','C')]/P0005[('A','C')]:.3f} C={coup[('C','A')]/P0005[('C','A')]:.3f}",
          flush=True)
