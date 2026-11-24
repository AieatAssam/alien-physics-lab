"""Round-3 (2026-11-23) H24 and H25 free fits, run 2026-11-24.

Free fit of the pair coefficient(s) with exponent P fixed at 2.5, over the full run window
(duration of each run). Uses labs/lab-vernier/analysis/fit_tools.py (fit_couplings).
Pre-registered predictions are in NOTEBOOK.md (round 3 section) and are compared below.
Run from the repo root: python3 -I <this file>.
"""
import importlib.util
import json
import math
import os

ROOT = os.getcwd()
HERE = os.path.join(ROOT, "labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)

P = 2.5
ALL_KEYS = [("A", "A"), ("B", "B"), ("A", "B"), ("B", "A"), ("A", "C"), ("C", "A"), ("B", "C"), ("C", "B"), ("C", "C")]


def load(day, rnd, i):
    rid = f"{day}/r{rnd}/lab-vernier/{i:03d}"
    req = ft.load_json(os.path.join(ROOT, "requests", rid + ".json"))
    res = ft.load_json(os.path.join(ROOT, "results", rid + ".json"))
    return req, res


# (run index, label, keys to fit, prediction text)
PLAN = [
    (11, "A-B r0 1.5 T0.5", [("A", "B")], "H24: 6.5 +/- 0.4; constant K: 7.6"),
    (12, "A-B r0 1.5 T0.5", [("A", "B")], ""),
    (13, "A-B r0 1.5 T0.5", [("A", "B")], ""),
    (14, "A-B r0 1.5 T0.5", [("A", "B")], ""),
    (15, "A-B r0 3.0 T2", [("A", "B")], "H24: 8.8; constant K: 7.6"),
    (16, "A-B r0 3.0 T2", [("A", "B")], ""),
    (17, "A-B r0 2.5 T1.2", [("A", "B")], "H24: 8.2"),
    (18, "A-B r0 2.5 T1.2", [("A", "B")], ""),
    (19, "A-A r0 2.0 T0.8", [("A", "A")], "15.6 (P-0024) / 13.55 (P-0013) / 11.3 (P-0012)"),
    (20, "A-A r0 2.0 T0.8", [("A", "A")], ""),
    (21, "A-A r0 3.0 T2", [("A", "A")], "19.3 (P-0024) / 13.55 (constant)"),
    (22, "A-A r0 3.0 T2", [("A", "A")], ""),
]

coup0 = {k: 0.0 for k in ALL_KEYS}
coup0[("A", "B")] = 7.5
coup0[("B", "A")] = 11.0
coup0[("A", "A")] = 13.0

for i, label, keys, pred in PLAN:
    req, res = load("2026-11-23", 3, i)
    dur = req["setup"]["duration"]
    bounds = {k: (-40.0, 40.0) for k in keys}
    coup, mse = ft.fit_couplings(req["setup"], res, coup0, keys, bounds, P=P, tmax=dur, sweeps=2)
    row = dict(run=f"r3/{i:03d}", label=label, duration=dur,
               fit={f"{a}({b})": round(coup[(a, b)], 3) for a, b in keys},
               fit_rmse_L=round(math.sqrt(mse) / ft.L, 5), prediction=pred)
    print(json.dumps(row), flush=True)
