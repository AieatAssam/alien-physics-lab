#!/usr/bin/env python3
"""Generic scorer (lab-c, round 1 2026-11-26).

For each request id, loads requests/<id>.json and results/<id>.json from the repo, runs the paper model's
predict(setup) and reports:
  - judged error: RMSE over all x/y components of (predicted - measured), divided by L = 10
  - in-domain check via the model's own ValueError (if it raises, the run is marked out-of-model-domain)
  - raw tracker minimum pair separation d_obs and its time (two-particle runs)

Run:  python3 -I score_generic.py REPO_ROOT MODEL_PY ID [ID ...]
      ID like 2026-11-25/r3/lab-c/001
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

L = 10.0
REPO = Path(sys.argv[1])
MODEL_PY = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("paper_model", MODEL_PY)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def rmse_over(pred, meas):
    se, n = 0.0, 0
    for p, m in zip(pred, meas):
        for i in range(len(p["particles"])):
            for c in range(2):
                e = p["particles"][i]["pos"][c] - m["particles"][i]["pos"][c]
                se += e * e
                n += 1
    return math.sqrt(se / n) / L


def dmin_obs(meas):
    best = (float("inf"), None)
    for m in meas:
        ps = m["particles"]
        if len(ps) != 2:
            return None
        d = math.dist(ps[0]["pos"], ps[1]["pos"])
        if d < best[0]:
            best = (d, m["t"])
    return best


for rid in sys.argv[3:]:
    req = json.loads((REPO / "requests" / f"{rid}.json").read_text())
    res = json.loads((REPO / "results" / f"{rid}.json").read_text())
    setup = req["setup"]
    meas = res["samples"]
    r0 = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"]) if len(setup["particles"]) == 2 else None
    head = f"{rid} N={len(setup['particles'])} T={setup['duration']} dt={setup['sample_dt']} r0={r0}"
    try:
        pred = mod.predict(setup)
    except ValueError as e:
        print(head, "| MODEL REFUSES (out of model domain):", e)
        continue
    if len(pred) != len(meas):
        print(head, f"| LENGTH MISMATCH pred={len(pred)} meas={len(meas)}")
        continue
    ok = all(abs(p["t"] - m["t"]) < 1e-9 for p, m in zip(pred, meas))
    e_full = rmse_over(pred, meas)
    # windowed: up to half the run and up to t = 0.6
    half = [i for i, m in enumerate(meas) if m["t"] <= setup["duration"] / 2 + 1e-9]
    e_half = rmse_over([pred[i] for i in half], [meas[i] for i in half])
    dm = dmin_obs(meas)
    dmtxt = f"d_obs={dm[0]:.4f} at t={dm[1]:.3f}" if dm else "d_obs=n/a"
    print(head, f"| RMSE/L={e_full:.5f} first_half={e_half:.5f} times_match={ok} {dmtxt} budget_rem={res.get('budget_remaining')}")
