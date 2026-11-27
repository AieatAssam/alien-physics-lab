"""Score 2026-11-27/r1/lab-c/001-004 (r1-012 and r1-013 setups, sample-step and replicate test).

Pre-registered rule: post-contact maximum separation >= 5 is ejected, < 3 is bound, 3 to 5 is no verdict.
Contact = first sample with separation < 0.1. Usage: python3 -I score_r1_2026-11-27.py <repo_root>
"""
import json
import math
import sys

ROOT = sys.argv[1]
RUNS = [
    ("001", "r1-012 setup, dt 0.001"),
    ("002", "r1-012 exact replicate, dt 0.005"),
    ("003", "r1-012 with y offset 0.01, dt 0.001"),
    ("004", "r1-013 setup, dt 0.001"),
]
for n, label in RUNS:
    d = json.load(open(f"{ROOT}/results/2026-11-27/r1/lab-c/{n}.json"))
    seps = [(s["t"], math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"])) for s in d["samples"]]
    contact = next((t for t, x in seps if x < 0.1), None)
    post = [x for t, x in seps if contact is not None and t >= contact]
    pmax = max(post)
    if pmax >= 5:
        verdict = "ejected"
    elif pmax < 3:
        verdict = "bound"
    else:
        verdict = "no verdict"
    print(f"{n} {label}: contact t={contact} post-contact max={pmax:.2f} -> {verdict} (samples {len(seps)}, cost {d['cost']})")
