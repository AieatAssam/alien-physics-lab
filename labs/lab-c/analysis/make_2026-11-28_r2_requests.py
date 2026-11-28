"""Generate lab-c 2026-11-28/r2 research requests 001-008 (pre-registered in NOTEBOOK, round 2).

Geometry R13 = r1-013 (A-A, x 3.875 and 6.125, y 5, r0 2.25). Geometry R30 = r0 3.0 (x 3.5 and 6.5, y 5).
Replicate pairs at dt 0.0025, 0.0035, 0.0045 (R13) and dt 0.004 (R30). T 1.5, tracker only.
Usage: python3 make_2026-11-28_r2_requests.py <repo_root>
"""
import json
import os
import sys

REPO = sys.argv[1]
OUT = os.path.join(REPO, "out", "requests", "2026-11-28", "r2", "lab-c")
os.makedirs(OUT, exist_ok=True)

GEOM = {
    "R13": [(3.875, 5.0), (6.125, 5.0)],
    "R30": [(3.5, 5.0), (6.5, 5.0)],
}
PLAN = [
    ("R13", 0.0025, 1), ("R13", 0.0025, 2),
    ("R13", 0.0035, 1), ("R13", 0.0035, 2),
    ("R13", 0.0045, 1), ("R13", 0.0045, 2),
    ("R30", 0.004, 1), ("R30", 0.004, 2),
]
for i, (g, dt, rep) in enumerate(PLAN, start=1):
    rid = f"{i:03d}"
    (x0, y0), (x1, y1) = GEOM[g]
    req = {
        "request_id": f"2026-11-28/r2/lab-c/{rid}",
        "lab": "lab-c",
        "account": "research",
        "purpose": (f"dt map, geometry {g}, A-A at rest, sample_dt {dt}, replicate {rep} of 2. "
                    "Pre-registered in NOTEBOOK (round 2): contact below 0.2, ejected if post-contact max >= 5, "
                    "bound if < 3."),
        "setup": {
            "particles": [
                {"species": "A", "pos": [x0, y0], "vel": [0.0, 0.0]},
                {"species": "A", "pos": [x1, y1], "vel": [0.0, 0.0]},
            ],
            "duration": 1.5,
            "sample_dt": dt,
        },
        "instruments": ["tracker"],
    }
    with open(os.path.join(OUT, rid + ".json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    print(rid, g, dt, rep)
