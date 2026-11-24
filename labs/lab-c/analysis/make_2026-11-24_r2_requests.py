#!/usr/bin/env python3
"""Generate lab-c round-2 requests for 2026-11-24 (run from the repo root; writes under out/requests).

001 (review, cites P-0026): 16 A particles at rest, random non-overlapping layout inside the chamber,
    every initial pairwise distance in [1.7, 9.0] (inside P-0026's [1.5, 10.5] with margin), T = 0.3,
    sample_dt 0.003, tracker. Cost 1 + 0.02 * 16 * 0.3 = 1.096 of the 2.04 review credits left.
    It is the only crowd test available to lab-c under the review account today (one run; see notebook).
002-004 (research, not cited): A-A pair at rest, horizontal, centre (5,5), r0 = 4, 6, 8, T = 6,
    sample_dt 0.01, tracker. Tests whether the A-B exponent (about 2.9 to 3.0, from runs 013-022)
    is shared by an A-A pair under the same geometry (a species test).
"""
import json, math
from pathlib import Path
import numpy as np

ROOT = Path.cwd()
OUT = ROOT / "out" / "requests" / "2026-11-24" / "r2" / "lab-c"
OUT.mkdir(parents=True, exist_ok=True)


def crowd(n=16, seed=20261124):
    rng = np.random.default_rng(seed)
    while True:
        pts = [rng.uniform(1.0, 9.0, size=2)]
        ok = True
        tries = 0
        while len(pts) < n and tries < 200000:
            tries += 1
            c = rng.uniform(1.0, 9.0, size=2)
            d = [np.hypot(*(c - p)) for p in pts]
            if min(d) >= 1.7 and max(d) <= 9.0:
                pts.append(c)
        if len(pts) == n:
            return [[round(float(x), 4), round(float(y), 4)] for x, y in pts]


def particles(pos, species="A"):
    return [{"species": species, "pos": p, "vel": [0.0, 0.0]} for p in pos]


def pair(r0):
    return [[5.0 - r0 / 2, 5.0], [5.0 + r0 / 2, 5.0]]


pos16 = crowd()
d = [math.dist(a, b) for i, a in enumerate(pos16) for b in pos16[i + 1:]]
assert 1.7 <= min(d) and max(d) <= 9.0, (min(d), max(d))

reqs = [
    dict(request_id="2026-11-24/r2/lab-c/001", lab="lab-c", account="review", cites_paper="P-0026",
         purpose=("Review of P-0026 (A crowd at rest, up to 16 particles, T <= 0.3). One 16-particle "
                  "random layout, all initial pairwise distances in [1.7, 9.0], tracker only. Tests the "
                  "summed pair law at N = 16 on a layout different from the paper's eight-pair run."),
         setup=dict(particles=particles(pos16), duration=0.3, sample_dt=0.003),
         instruments=["tracker"]),
]
for k, r0 in enumerate([4.0, 6.0, 8.0], start=2):
    reqs.append(dict(
        request_id=f"2026-11-24/r2/lab-c/{k:03d}", lab="lab-c", account="research",
        purpose=(f"Species test (not cited): A-A pair at rest, horizontal, r0 = {r0}, centre (5,5), T = 6.0. "
                 "Same geometry as the A-B long-window runs 2026-11-24/r1/lab-c/013-022, to compare the "
                 "fitted exponent and K for an A-A pair."),
        setup=dict(particles=particles(pair(r0)), duration=6.0, sample_dt=0.01),
        instruments=["tracker"]))

for r in reqs:
    (OUT / f"{r['request_id'].split('/')[-1]}.json").write_text(json.dumps(r, indent=2) + "\n")
    print("wrote", r["request_id"], r["account"])
