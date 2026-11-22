#!/usr/bin/env python3
"""Round-1 2026-11-22 requests (lab-c) and the grant proposal. Run: python3 -I make_2026-11-22_requests.py REPO_ROOT"""
import json, math, sys
from pathlib import Path
REPO = Path(sys.argv[1])
OUT = REPO / "out"
DATE, RND, LAB = "2026-11-22", "r1", "lab-c"

def parts(spec):
    return [{"species": s, "pos": list(p), "vel": [0.0, 0.0]} for s, p in spec]

def write(num, req):
    d = OUT / "requests" / DATE / RND / LAB
    d.mkdir(parents=True, exist_ok=True)
    req = {"request_id": f"{DATE}/{RND}/{LAB}/{num:03d}", "lab": LAB, **req}
    (d / f"{num:03d}.json").write_text(json.dumps(req, indent=2) + "\n")

# Review runs for P-0018 (C-C at r0 = 1.0, T = 0.15, the claim's stated duration).
cc_pairs = {
    "horizontal": [(("C", (4.5, 5.0)), ("C", (5.5, 5.0)))],
    "vertical":   [(("C", (5.0, 4.5)), ("C", (5.0, 5.5)))],
    "diagonal":   [(("C", (4.6464, 4.6464)), ("C", (5.3536, 5.3536)))],
}
for i, (name, pair) in enumerate(cc_pairs.items(), start=1):
    write(i, {
        "account": "review", "cites_paper": "P-0018",
        "purpose": f"Review of P-0018 claim c1 (C-C pair at r0 = 1.0, T <= 0.15, the claim's stated duration). {name} orientation; the earlier T = 0.3 runs collide near t = 0.26, so this run stays inside the claimed window.",
        "setup": {"particles": parts(pair[0]), "duration": 0.15, "sample_dt": 0.0005},
        "instruments": ["tracker", "census"],
    })

# Research runs: A-B pair at r0 = 1.0 at full T = 0.6 (open problem close-AB).
ab = {
    "horizontal": [("A", (4.5, 5.0)), ("B", (5.5, 5.0))],
    "vertical":   [("A", (5.0, 4.5)), ("B", (5.0, 5.5))],
}
for j, (name, pair) in enumerate(ab.items(), start=4):
    write(j, {
        "account": "research",
        "purpose": f"Close A-B pair at r0 = 1.0, at rest, {name}, full T = 0.6 (open problem close-AB). Previous A-B r0 = 1.0 runs were T = 0.3 only, where the scale cannot be resolved; this tests the law over a full claim-length window and records contact timing.",
        "setup": {"particles": parts(pair), "duration": 0.6, "sample_dt": 0.0005},
        "instruments": ["tracker", "census"],
    })

# Grant proposal: 8-body additivity test (crowd-8).
cx, cy, R = 5.0, 5.0, 3.5
species_cycle = ["A", "B", "C", "A", "B", "C", "A", "B"]
ring = [(species_cycle[k], (round(cx + R * math.cos(2 * math.pi * k / 8), 4),
                             round(cy + R * math.sin(2 * math.pi * k / 8), 4))) for k in range(8)]
grant = {
    "lab": LAB, "date": DATE,
    "title": "Crowd of eight: does the pairwise law add up at N = 8? Octagon of A, B, C at rest, T = 5",
    "pitch": "Our pairwise law (P-0005 and P-0008 couplings, scaled per species) is tested only up to three bodies (triangle at side 5 and 3, supported at tracker noise). Question: does the pairwise sum still hold for eight bodies? Eight particles at rest on a radius-3.5 octagon (adjacent separation 2.68, all species A, B, C in a cycle), T = 5, dt = 0.01. Prediction: judged error of the pairwise sum at or below 0.01 (noise floor 0.007). Falsifier: error above 0.03, or a residual that grows with N beyond tracker noise, which would mean many-body terms.",
    "setup": {"particles": parts(ring), "duration": 5.0, "sample_dt": 0.01},
}
(OUT / "grants" / DATE / "proposals").mkdir(parents=True, exist_ok=True)
(OUT / "grants" / DATE / "proposals" / f"{LAB}.json").write_text(json.dumps(grant, indent=2) + "\n")
print("wrote requests 001-005 and grant proposal")
