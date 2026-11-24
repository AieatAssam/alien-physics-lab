"""Check the P-0027 table model (A-A K(r), piecewise linear) against all lab-a A-A runs.

1. Judge-style RMSE/L of predict() against each run: H30 (2026-11-23/r3/lab-a/001-016) and
   round 1 A-A runs (2026-11-24/r1/lab-a/011-018), plus the P-0003 edge runs 009-010 (own paper, not a review).
2. Minimum predicted separation over each run's duration (to set T_MAX).
3. Predicted separation gap between table and constant-K 17.7 for candidate designs (to set design T).

Usage: python3 -I check_P0027_2026-11-24.py <repo_root> <model_path>
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

ROOT, MODEL = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("p0027", MODEL)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
L = 10.0


def runs():
    out = []
    for n in range(1, 17):
        out.append(("2026-11-23/r3/lab-a", n))
    for n in range(9, 19):
        out.append(("2026-11-24/r1/lab-a", n))
    return out


def judge(run_dir, n):
    with open(os.path.join(ROOT, "results", run_dir, f"{n:03d}.json")) as f:
        res = json.load(f)
    with open(os.path.join(ROOT, "requests", run_dir, f"{n:03d}.json")) as f:
        req = json.load(f)
    X = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in res["samples"]], float)
    t = np.array([s["t"] for s in res["samples"]])
    pred = m.predict(req["setup"])
    PX = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in pred], float)
    k = min(len(X), len(PX))
    e = math.sqrt(np.mean((PX[:k] - X[:k]) ** 2)) / L
    p0 = np.array([p["pos"] for p in req["setup"]["particles"]], float)
    sep0 = math.dist(p0[0], p0[1])
    minsep = min(math.dist(a[0], a[1]) for a in PX)
    return dict(run=f"{run_dir}/{n:03d}", sep=round(sep0, 3), T=req["setup"]["duration"],
                rmse_over_L=round(e, 5), min_pred_sep=round(minsep, 3), n=[len(X), len(PX)])


print("== P-0027 table vs measured A-A runs ==")
rows = []
for rd, n in runs():
    try:
        r = judge(rd, n)
        rows.append(r)
        print(r)
    except ValueError as ex:
        print(rd, n, 'outside claim window:', ex)

# Minimum predicted separation vs duration for each separation (for T_MAX choice)
print("\n== minimum predicted separation over T (K table) ==")
for r0 in (3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0):
    p0 = [{"species": "A", "pos": [5 - r0 / 2, 5.0], "vel": [0.0, 0.0]},
          {"species": "A", "pos": [5 + r0 / 2, 5.0], "vel": [0.0, 0.0]}]
    for T in (1.0, 2.0, 3.0):
        try:
            s = m.predict({"particles": p0, "duration": T, "sample_dt": T / 1990.0})
        except ValueError as ex:
            print(f"r0 {r0:4.1f} T {T:3.1f}: outside window ({ex})")
            continue
        ms = min(math.dist(a["particles"][0]["pos"], a["particles"][1]["pos"]) for a in s)
        print(f"r0 {r0:4.1f} T {T:3.1f}: min predicted sep {ms:.3f}")
