"""Inspect grant run 2026-11-19/r3/lab-a/001: wall excursions and the closest approach.
Usage: python3 -I inspect_grant_2026-11-20.py <repo_root>
"""
import json
import math
import sys

g = json.load(open(f"{sys.argv[1]}/results/2026-11-19/r3/lab-a/001.json"))
S = g["samples"]
worst = 0.0
n_out_by_more_than_015 = 0
for s in S:
    for p in s["particles"]:
        for c in p["pos"]:
            d = max(0.0 - c, c - 10.0, 0.0)
            worst = max(worst, d)
            if d > 0.15:
                n_out_by_more_than_015 += 1
print("max excursion outside [0,10] (tracker): %.4f" % worst)
print("coordinates more than 0.15 outside the chamber:", n_out_by_more_than_015)

best = (float("inf"), None, None)
for s in S:
    ps = s["particles"]
    for a in range(len(ps)):
        for b in range(a + 1, len(ps)):
            d = math.dist(ps[a]["pos"], ps[b]["pos"])
            if d < best[0]:
                best = (d, s["t"], (a, b, ps[a]["species"], ps[b]["species"]))
print("closest tracker approach: sep %.3f at t=%.2f pair %s" % best)
close = []
for s in S:
    ps = s["particles"]
    for a in range(len(ps)):
        for b in range(a + 1, len(ps)):
            if math.dist(ps[a]["pos"], ps[b]["pos"]) < 0.5:
                close.append((round(s["t"], 2), a, b))
print("pair-sample hits with tracker sep < 0.5:", len(close), "first few:", close[:6])
