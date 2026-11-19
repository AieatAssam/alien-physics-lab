"""Fit A-A coefficient at separation 4 (2026-11-18/r2/lab-b/018) and 6 (r2/021). Run from repo root: python3 -I <this>."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lab_b_tools import load, fit_single_K, fmt

for rid, tmax in [("2026-11-18/r2/lab-b/018", 2.0), ("2026-11-18/r2/lab-b/021", 2.0)]:
    req = load(f"requests/{rid}.json")
    res = load(f"results/{rid}.json")
    coarse = fit_single_K(req, res, tmax, 0.002, 12.0, 22.0, 0.1)
    fine = fit_single_K(req, res, tmax, 0.002, coarse[1] - 0.1, coarse[1] + 0.1, 0.01)
    print(f"{rid} (A-A, r0={math.dist(req['setup']['particles'][0]['pos'], req['setup']['particles'][1]['pos']) if False else ''}K={fine[1]:.2f}")
    print(fmt(fine[2], fine[3]))
