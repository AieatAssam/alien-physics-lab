"""Grid check of the close-range probes r2/008-010 (lab-vernier, round 3).

Grid over the signed pair coefficients (P = 2.5 fixed), rms per coordinate on tracker data.
Run with: python3 -I close_grid_2026-11-20.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fit_tools import load_json, sse_window
from review_check import R

RQ = R + "/requests/2026-11-20/r2/lab-vernier/{}.json"
RS = R + "/results/2026-11-20/r2/lab-vernier/{}.json"


def load(n):
    return load_json(RQ.format(n)), load_json(RS.format(n))


def grid2(n, keys, ranges, tmax, steps=21):
    req, res = load(n)
    base = {(a, b): 0.0 for a in "ABC" for b in "ABC"}
    (k1, k2), ((lo1, hi1), (lo2, hi2)) = keys, ranges
    best = None
    for i in range(steps):
        for j in range(steps):
            c = dict(base)
            c[k1] = lo1 + (hi1 - lo1) * i / (steps - 1)
            c[k2] = lo2 + (hi2 - lo2) * j / (steps - 1)
            e = sse_window(req["setup"], res, c, 2.5, tmax)
            if best is None or e < best[0]:
                best = (e, c[k1], c[k2])
    return math.sqrt(best[0]), best[1], best[2]


def grid1(n, key, rng, tmax, steps=61):
    req, res = load(n)
    base = {(a, b): 0.0 for a in "ABC" for b in "ABC"}
    lo, hi = rng
    best = None
    for i in range(steps):
        c = dict(base)
        c[key] = lo + (hi - lo) * i / (steps - 1)
        e = sse_window(req["setup"], res, c, 2.5, tmax)
        if best is None or e < best[0]:
            best = (e, c[key])
    return math.sqrt(best[0]), best[1]


for tmax in (0.2, 0.3):
    rms, k1, k2 = grid2("009", [("A", "B"), ("B", "A")], [(-5, 25), (-10, 25)], tmax)
    print("A-B r2/009 window t<=%.1f: best K_AB %.2f K_BA %.2f rms %.4f" % (tmax, k1, k2, rms))
for tmax in (0.2, 0.3):
    rms, k = grid1("008", ("B", "B"), (0, 12), tmax)
    print("B-B r2/008 window t<=%.1f: best K_BB %.2f rms %.4f" % (tmax, k, rms))
rms, k1, k2 = grid2("010", [("B", "C"), ("C", "B")], [(-10, 0), (-15, 0)], None)
print("B-C r2/010 full window: best K_BC %.2f K_CB %.2f rms %.4f" % (k1, k2, rms))
