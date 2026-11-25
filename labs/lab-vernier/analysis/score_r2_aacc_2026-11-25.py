"""Vernier round 3: score round-2 A-A / C-C T=2 runs (2026-11-25/r2/lab-vernier/001-004) in their
pre-contact windows, using the round-1 piecewise-K nodes (fit_pw_round1_2026-11-25.py, all 6 runs).

Window: from t = 0 up to the first measured separation below the cut (1.5 by default; 2.0 for the
C-C window pre-registered in 003).
Judge-style error = sqrt(mean squared coordinate residual over window) / L.
Null = particles held at their initial positions over the same window.

Run: python3 -I score_r2_aacc_2026-11-25.py
"""
import importlib.util
import json
import math
import os
import sys

sys.path.append(os.path.expanduser("~/.local/lib/python3.12/site-packages"))
REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
LAB_AN = os.path.dirname(os.path.abspath(__file__))  # helpers copied alongside this file
L = 10.0

sys.path.insert(0, LAB_AN)  # fit_pw_round1 does `import fit_tools`
spec = importlib.util.spec_from_file_location("fitpw", LAB_AN + "/fit_pw_round1_2026-11-25.py")
fitpw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fitpw)

NODES = {"AA": [16.941, 18.034, 18.285], "CC": [12.730, 13.202, 13.184]}
RUNS = {"001": ("AA", 1.5), "002": ("AA", 1.5), "003": ("CC", 1.5), "004": ("CC", 1.5)}


def window_end(res, rmin):
    for s in res["samples"]:
        p = s["particles"]
        if math.dist(p[0]["pos"], p[1]["pos"]) < rmin:
            return s["t"] - 1e-9
    return res["samples"][-1]["t"]


def judged(setup, res, nodeK, tmax):
    se, n = fitpw.sse_run(setup, res, nodeK, tmax)
    return math.sqrt(se / n) / L


def null_err(res, tmax):
    init = [list(p["pos"]) for p in res["samples"][0]["particles"]]
    se, n = 0.0, 0
    for s in res["samples"]:
        if s["t"] > tmax + 1e-12:
            break
        for i, p in enumerate(s["particles"]):
            se += (p["pos"][0] - init[i][0]) ** 2 + (p["pos"][1] - init[i][1]) ** 2
            n += 2
    return math.sqrt(se / n) / L


def load(num):
    rid = f"2026-11-25/r2/lab-vernier/{num}"
    req = json.load(open(f"{REPO}/requests/{rid}.json"))
    res = json.load(open(f"{REPO}/results/{rid}.json"))
    return rid, req["setup"], res


if __name__ == "__main__":
    for num in ["001", "002", "003", "004"]:
        pair, cut = RUNS[num]
        rid, setup, res = load(num)
        tm = window_end(res, cut)
        e = judged(setup, res, NODES[pair], tm)
        z = null_err(res, tm)
        line = f"{rid} {pair} window_end(sep<{cut})={tm:.3f} judged={e:.5f} null={z:.5f}"
        if pair == "CC":
            tm2 = window_end(res, 2.0)
            line += f" | cut@2.0 window_end={tm2:.3f} judged={judged(setup, res, NODES[pair], tm2):.5f}"
        print(line)
