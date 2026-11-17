"""Fit one A-B run at a time with F = k r^-n (mass ratio mb free), to see whether a single
power law can describe each run before pooling. Uses exact requested initial state.
Usage: python3 -I single_run_fit.py"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pair_scan import setup, obs, rms_for

RUNS = [("r2/lab-b/002", 1.8), ("r2/lab-b/003", 1.8), ("r2/lab-b/004", 0.85), ("r1/lab-b/002", 1.4)]
for n in [0.5, 1.0, 1.5, 2.0]:
    row = []
    for rid, tmax in RUNS:
        sp, x0 = setup(rid)
        data = [(sp, x0, obs(rid, tmax))]
        best = None
        for mb in [0.5, 0.6, 0.7, 0.8, 0.9]:
            for kk in [0.25, 0.5, 1, 2, 4, 8]:
                r = rms_for({"B": mb, "C": 1.0}, kk, n, data)
                if best is None or r < best[0]:
                    best = (r, mb, kk)
        row.append(f"{rid.split('/')[0]}/{rid.split('/')[-1]}: rms {best[0]:.3f} mb {best[1]} k {best[2]}")
    print(f"n={n}: " + " | ".join(row), flush=True)
