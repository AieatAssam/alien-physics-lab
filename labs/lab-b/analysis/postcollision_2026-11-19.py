"""Reproducibility of A-B sep-1 runs (2026-11-19/r1/lab-b/003, 004, 005). Pure Python.

Compares run pairs at common sample times and reports the first time the
tracker separation falls below 0.5 (the post-collision region).
"""
import json
import math
import os

REPO = os.getcwd()


def load(rid):
    return json.load(open(os.path.join(REPO, f"results/2026-11-19/r1/lab-b/{rid}.json")))


def by_t(res):
    return {round(float(s["t"]), 6): [p["pos"] for p in s["particles"]] for s in res["samples"]}


def sep(xs):
    return math.dist(xs[0], xs[1])


r3, r4, r5 = (by_t(load(x)) for x in ["003", "004", "005"])
print("first t with tracker sep < 0.5 (003, 004, 005):",
      [min((t for t in d if sep(d[t]) < 0.5), default=None) for d in (r3, r4, r5)])
print("first t with tracker sep < 0.3:",
      [min((t for t in d if sep(d[t]) < 0.3), default=None) for d in (r3, r4, r5)])


def compare(a, b, label):
    rows = []
    for t in sorted(set(a) & set(b)):
        if t <= 0:
            continue
        d = max(math.dist(a[t][i], b[t][i]) for i in range(2))
        rows.append((t, d))
    for lo, hi in [(0, 0.3), (0.3, 0.6), (0.6, 1.0), (1.0, 1.5), (1.5, 2.0)]:
        sel = [d for t, d in rows if lo < t <= hi]
        if sel:
            print(f"  {label} t in ({lo},{hi}]: max per-particle diff {max(sel):.3f}, mean {sum(sel)/len(sel):.3f}")


print("003 vs 004 (identical requests):")
compare(r3, r4, "003-004")
print("003 vs 005 (sample_dt 0.01 vs 0.001), common times:")
compare(r3, r5, "003-005")
