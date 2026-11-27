"""Round-3 requests for lab-c: sample-step test of the post-contact outcome (2026-11-27).

Writes out/requests/2026-11-27/r3/lab-c/001-008.json (research account, tracker only).
Pre-registered (see NOTEBOOK.md, round 3): see the rule text there.
Usage: python3 -I make_2026-11-27_r3_requests.py <repo_root>
"""
import json
import os
import sys

ROOT = sys.argv[1]
OUT = os.path.join(ROOT, "out", "requests", "2026-11-27", "r3", "lab-c")
os.makedirs(OUT, exist_ok=True)

GEOM_013 = [{"species": "A", "pos": [3.875, 5.0], "vel": [0.0, 0.0]},
            {"species": "A", "pos": [6.125, 5.0], "vel": [0.0, 0.0]}]
GEOM_012 = [{"species": "A", "pos": [4.0, 5.0], "vel": [0.0, 0.0]},
            {"species": "A", "pos": [6.0, 5.0], "vel": [0.0, 0.0]}]

PLAN = [
    ("001", GEOM_013, 0.001, "r1-013 geometry at dt 0.001 (replicate 1 of 4)"),
    ("002", GEOM_013, 0.001, "r1-013 geometry at dt 0.001 (replicate 2 of 4)"),
    ("003", GEOM_013, 0.001, "r1-013 geometry at dt 0.001 (replicate 3 of 4)"),
    ("004", GEOM_013, 0.001, "r1-013 geometry at dt 0.001 (replicate 4 of 4)"),
    ("005", GEOM_013, 0.01, "r1-013 geometry at dt 0.01 (coarse step 1 of 2)"),
    ("006", GEOM_013, 0.01, "r1-013 geometry at dt 0.01 (coarse step 2 of 2)"),
    ("007", GEOM_012, 0.001, "r1-012 geometry at dt 0.001 (replicate 1 of 2)"),
    ("008", GEOM_012, 0.001, "r1-012 geometry at dt 0.001 (replicate 2 of 2)"),
]

for n, geom, dt, label in PLAN:
    req = {
        "request_id": f"2026-11-27/r3/lab-c/{n}",
        "lab": "lab-c",
        "account": "research",
        "purpose": "Sample-step test of the post-contact A-A outcome: " + label + ". "
                   "Tests whether ejection depends on sample_dt (see NOTEBOOK round 3).",
        "setup": {"particles": geom, "duration": 1.5, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    assert 1.5 / dt <= 2000 and len(geom) <= 16
    with open(os.path.join(OUT, f"{n}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    print("wrote", n, label, "cost", round(1 + 0.02 * len(geom) * 1.5, 2))
