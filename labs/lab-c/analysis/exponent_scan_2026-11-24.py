#!/usr/bin/env python3
"""Joint (K, P) scan: constant coupling K and exponent P (force = K / r^P) on lab-c's round-3 map runs.

Uses P-0025's predictor (read-only) with K_TAB replaced by a constant K and the exponent module
variable P replaced; RATIO fixed at 1.41 (species K_B/K_A), so only K_A and P are scanned.
Runs are cut at the pre-approach window (separation >= 3.0, t <= 2). Reports the SSE surface
minimum and the SSE at P = 2.5 (the value the paper and our notebook assumed).
Usage: python3 -I exponent_scan_2026-11-24.py REPO_ROOT
"""
import importlib.util, json, math, sys
from pathlib import Path
import numpy as np

REPO = Path(sys.argv[1])
CUT = 3.0
RUNS = [f"2026-11-23/r3/lab-c/{n:03d}" for n in range(3, 13)]


def load_model():
    spec = importlib.util.spec_from_file_location("m", REPO / "papers" / "P-0025" / "model.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_data(rid):
    d, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / d / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / d / rnd / lab / f"{nnn}.json").read_text())
    return req["setup"], res["samples"]


def window(samples):
    seps = [math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in samples]
    for i in range(2, len(samples) - 2):
        if samples[i]["t"] >= 0.5 and sum(seps[i - 2:i + 3]) / 5 < CUT:
            return min(samples[i]["t"], 2.0)
    return min(samples[-1]["t"], 2.0)


mod = load_model()
DATA = {}
for rid in RUNS:
    setup, samples = run_data(rid)
    DATA[rid] = (setup, samples, window(samples))


def sse_for(K, P):
    mod.K_TAB = np.full(5, K)
    mod.P = P
    total, n_tot = 0.0, 0
    for rid, (setup, samples, tmax) in DATA.items():
        pred = mod.predict(setup)
        pm = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
        for s in samples:
            t = round(s["t"], 9)
            if t <= 0 or t > tmax + 1e-9 or t not in pm:
                continue
            for p in s["particles"]:
                for k in range(2):
                    total += (p["pos"][k] - pm[t][p["id"]][k]) ** 2
                    n_tot += 1
    return total, n_tot


Ks = np.linspace(5.0, 12.0, 15)
Ps = np.array([2.0, 2.25, 2.5, 2.75, 3.0, 3.25])
grid = np.zeros((len(Ks), len(Ps)))
n_pts = 0
for i, K in enumerate(Ks):
    for j, P in enumerate(Ps):
        v, n_pts = sse_for(K, P)
        grid[i, j] = v
i_min, j_min = np.unravel_index(np.argmin(grid), grid.shape)
sig2 = grid[i_min, j_min] / n_pts
print(f"points={n_pts} runs={len(DATA)}")
print(f"best: K={Ks[i_min]:.2f} P={Ps[j_min]:.2f} rms_per_coord={math.sqrt(grid[i_min, j_min] / n_pts):.5f}")
j25 = int(np.argmin(np.abs(Ps - 2.5)))
print(f"best K at P=2.5: K={Ks[np.argmin(grid[:, j25])]:.2f} rms={math.sqrt(grid[:, j25].min() / n_pts):.5f}")
print("P      min_SSE/n (over K)  K_at_min")
for j, P in enumerate(Ps):
    print(f"{P:4.2f}   {math.sqrt(grid[:, j].min() / n_pts):.5f}   {Ks[np.argmin(grid[:, j])]:.2f}")
