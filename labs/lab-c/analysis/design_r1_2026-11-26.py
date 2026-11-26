#!/usr/bin/env python3
"""Design for round 1 2026-11-26 (lab-c, Nullius). Pure python (no numpy in this environment).

(a) P-0034 (vernier) edge check: how far does its predict() (K held flat below 2.5) sit from the P-0026 law
    (lab-c's ungated copy, law_ungated.py) for A-A pairs at r0 in {3.0, 3.25, 3.5}, T = 1?
(b) P-0031 / P-0033 edge layouts: asymmetric 3- and 4-body arrangements at rest with every initial pairwise
    distance inside [5.0, 7.08] (inside both domains) and the spread pushed to the edges.

Run: python3 -I design_r1_2026-11-26.py REPO_ROOT
"""
import importlib.util
import itertools
import math
import random
import sys
from pathlib import Path

REPO = Path(sys.argv[1])


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


HERE = Path(__file__).resolve().parent
v34 = load("p34", REPO / "papers" / "P-0034" / "model.py")
law = load("law", HERE / "law_ungated.py")


def sep_min(samples):
    best = (float("inf"), None)
    for s in samples:
        d = math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"])
        if d < best[0]:
            best = (d, s["t"])
    return best


print("(a) P-0034 A-A pair vs P-0026 law, T = 1, dt = 0.001")
for r0 in (3.0, 3.25, 3.5):
    setup = {"particles": [{"species": "A", "pos": [5 - r0 / 2, 5.0], "vel": [0, 0]},
                           {"species": "A", "pos": [5 + r0 / 2, 5.0], "vel": [0, 0]}],
             "duration": 1.0, "sample_dt": 0.001}
    a = v34.predict(setup)
    b = law.predict(setup)
    se, n = 0.0, 0
    for p, q in zip(a, b):
        for i in range(2):
            for c in range(2):
                e = p["particles"][i]["pos"][c] - q["particles"][i]["pos"][c]
                se += e * e
                n += 1
    rmse_L = math.sqrt(se / n) / 10.0
    print(f"  r0={r0}: RMSE/L(P-0034 vs P26 law)={rmse_L:.5f}  "
          f"P-0034 min sep {sep_min(a)[0]:.3f} at t={sep_min(a)[1]:.3f}; P26 min sep {sep_min(b)[0]:.3f} at t={sep_min(b)[1]:.3f}")

print("(b) edge layouts: asymmetric, all pairwise distances in [5.0, 7.08]")
random.seed(7)


def pair_dists(pts):
    return [math.dist(a, b) for a, b in itertools.combinations(pts, 2)]


def ok(pts, lo=5.0, hi=7.08, margin=1.5):
    ds = pair_dists(pts)
    inside = all(lo + 0.02 <= d <= hi - 0.02 for d in ds)
    walls = all(margin <= x <= 10 - margin and margin <= y <= 10 - margin for x, y in pts)
    return inside and walls, ds


# triangles: pick an asymmetric triangle with sides spread over [5, 7.08]
best3 = None
for _ in range(200000):
    a = (random.uniform(2, 8), random.uniform(2, 8))
    b = (a[0] + random.uniform(-7, 7), a[1] + random.uniform(-7, 7))
    c = (random.uniform(2, 8), random.uniform(2, 8))
    good, ds = ok([a, b, c])
    if not good:
        continue
    spread = max(ds) - min(ds)
    asym = max(ds) - min(ds)
    if best3 is None or spread > best3[0]:
        best3 = (spread, [a, b, c], ds)
print("  triangle widest-spread:", round(best3[0], 3), [tuple(round(x, 3) for x in p) for p in best3[1]],
      [round(d, 3) for d in best3[2]])

# 4-body: all six pairwise distances in [5.0, 7.08] leave almost no room. A rhombus of side 5.0 is forced to be a
# square (diagonals 10 cos(t/2), 10 sin(t/2) both within [5, 7.08] only at t/2 = 44.9 deg); a Gaussian perturbation
# of sigma 0.004 on the side-5.0 square stays in the domain in only about 3 percent of draws (55/2000 when run).
# Result: N = 4 claims in this domain test squares only (checked by perturbation, not by a proof).
sq = [(0.0, 0.0), (5.0, 0.0), (5.0, 5.0), (0.0, 5.0)]
feas = 0
for _ in range(2000):
    q = [(x + random.gauss(0, 0.004), y + random.gauss(0, 0.004)) for x, y in sq]
    ds4 = pair_dists(q)
    if min(ds4) >= 5.0 and max(ds4) <= 7.08:
        feas += 1
print(f"  4-body: side-5.0 square perturbed by sigma 0.004 stays in domain in {feas}/2000 draws")
