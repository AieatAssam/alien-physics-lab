"""lab-a (Plumbline) round 2 of 2026-11-27: request generator (B-C transitivity test).

Usage: python3 -I make_2026-11-27_r2_requests.py <repo_root>

Writes out/requests/2026-11-27/r2/lab-a/001-003.json and validates each against protocol/request.schema.json.

Design: if each species has one response factor f_i (displacement ratio R_ij = |d_i|/|d_j| = f_i/f_j),
then R_BC = R_AC / R_AB. From the late-window ratios already measured:
  R_AC = 0.4234 (2026-11-26/r2/lab-a/001,002 at 3.0; 2026-11-27/r1/lab-a/009,010 at 5.0)
  R_AB = 0.7222 (2026-11-26/r2/lab-a/003 at 3.0; 2026-11-27/r1/lab-a/011,012 at 5.0)
  Prediction R_BC = |dB|/|dC| = 0.586. Falsifier: a replicate outside 0.586 +- 0.03 (about 5%).
Particle 0 = B, particle 1 = C. Pair centred on (5, 5). Tracker only, dt 0.005, T 2.0, research account.
"""
import json
import math
import os
import sys

ROOT = sys.argv[1]
DATE, ROUND, LAB = "2026-11-27", "r2", "lab-a"
C = 5.0


def pair(r, orient):
    if orient == "h":
        dx, dy = r / 2.0, 0.0
    else:
        dx = dy = r / 2.0 / math.sqrt(2.0)
    return [[C - dx, C - dy], [C + dx, C + dy]]


specs = [
    ("001", 5.0, "h", "B-C horizontal, separation 5.0, at rest, T 2. Transitivity test: pre-registered prediction |dB|/|dC| = R_AC/R_AB = 0.586 (late window 1.8 to 2.0). Falsifier: a replicate outside 0.586 +- 0.03."),
    ("002", 5.0, "d", "B-C diagonal, separation 5.0, replicate of 001 (same prediction and falsifier)."),
    ("003", 3.0, "h", "B-C horizontal, separation 3.0, at rest, T 2. Same transitivity prediction at a second separation (R_AC and R_AB at 3.0 are measured in 2026-11-26/r2)."),
]

schema_path = os.path.join(ROOT, "protocol", "request.schema.json")
try:
    import jsonschema
    schema = json.load(open(schema_path))
except Exception as e:  # validation is required; report if unavailable
    jsonschema = None
    print("WARNING: jsonschema not available:", e)

outdir = os.path.join(ROOT, "out", "requests", DATE, ROUND, LAB)
os.makedirs(outdir, exist_ok=True)
for num, r, orient, purpose in specs:
    pos = pair(r, orient)
    req = {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{num}",
        "lab": LAB,
        "account": "research",
        "purpose": purpose,
        "setup": {
            "particles": [
                {"species": "B", "pos": pos[0], "vel": [0.0, 0.0]},
                {"species": "C", "pos": pos[1], "vel": [0.0, 0.0]},
            ],
            "duration": 2.0,
            "sample_dt": 0.005,
        },
        "instruments": ["tracker"],
    }
    if jsonschema is not None:
        jsonschema.validate(req, schema)
    cost = 1 + 0.02 * 2 * 2.0
    with open(os.path.join(outdir, num + ".json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    print(req["request_id"], "validated" if jsonschema else "unvalidated", "r0=%.3f" % math.dist(pos[0], pos[1]), "cost=%.2f" % cost)
