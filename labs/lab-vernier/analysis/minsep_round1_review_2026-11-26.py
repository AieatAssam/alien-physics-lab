"""Closest approach and wall clearance for the round-1 review runs (2026-11-26/r1/lab-vernier/001-011).
Usage: python3 -I minsep_round1_review_2026-11-26.py <repo>/results
"""
import json, math, sys, os
RES = sys.argv[1]
for i in range(1, 12):
    rid = f"2026-11-26/r1/lab-vernier/{i:03d}"
    d = json.load(open(os.path.join(RES, "2026-11-26/r1/lab-vernier", f"{i:03d}.json")))
    S = d["samples"]
    mins, walls = [], []
    for s in S:
        P = [p["pos"] for p in s["particles"]]
        for a in range(len(P)):
            for b in range(a + 1, len(P)):
                mins.append(math.dist(P[a], P[b]))
        for p in P:
            walls.append(min(p[0], p[1], 10 - p[0], 10 - p[1]))
    t_end = S[-1]["t"]
    print(f"{rid} T={t_end:.3f} n={len(S)} min_sep_measured={min(mins):.3f} "
          f"min_wall_clearance_measured={min(walls):.3f}")
