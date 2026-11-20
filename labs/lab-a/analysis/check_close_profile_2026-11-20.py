"""lab-a, 2026-11-20 round 2: separation vs time (quarters of each run) for close-range runs 001-004
against their pre-registered predictions. Usage: python3 -I check_close_profile_2026-11-20.py <repo_root>
"""
import json
import math
import os
import sys

root = sys.argv[1]
RUNS = [("001", "AA_r2"), ("002", "AA_r2_rep"), ("003", "AA_r1p5"), ("004", "BB_r2")]
for i, tag in RUNS:
    r = json.load(open(os.path.join(root, "results", "2026-11-20", "r1", "lab-a", i + ".json")))
    pred = json.load(open(os.path.join(root, "labs", "lab-a", "analysis", "pred_2026-11-20_%s.json" % tag)))
    n = len(r["samples"])
    q = n // 5
    print("== %s %s (bins of %d samples)" % (i, tag, q))
    for b in range(5):
        a0, a1 = b * q, min((b + 1) * q, n)
        ms, ps = [], []
        dm = []  # mean (meas - pred) position residual per coord
        for s in range(a0, a1):
            mb = {p["id"]: p["pos"] for p in r["samples"][s]["particles"]}
            P = pred["samples_pos"][s]
            ms.append(math.hypot(mb[0][0] - mb[1][0], mb[0][1] - mb[1][1]))
            ps.append(math.hypot(P[0][0] - P[1][0], P[0][1] - P[1][1]))
        t = r["samples"][a0]["t"]
        print("  t=%.3f-%.3f  meas_sep=%.3f  pred_sep=%.3f  diff=%+.3f" %
              (t, r["samples"][a1 - 1]["t"], sum(ms) / len(ms), sum(ps) / len(ps), sum(ms) / len(ms) - sum(ps) / len(ps)))
