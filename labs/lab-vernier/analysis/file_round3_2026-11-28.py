"""Write round-3 requests for the sample-timing replicate (2026-11-28/r3/lab-vernier/001-012).

Geometry: two A at rest, x 4.5 and 5.5, y 5.0 (r0 1.0), T 0.6, tracker only (same as the r1 and r2 runs).
  001-006: sample_dt 0.0003 (2000 samples), fine arm
  007-012: sample_dt 0.001  (601 samples),  coarse arm
Cost 1.024 each (research account), 12.29 credits in total.

Pre-registered in NOTEBOOK.md (round 3, written before any result):
  P2: at dt 0.0003, 0 or 1 of 6 runs below 1.0 at t = 0.60 (primary metric);
      at dt 0.001, at least 4 of 6 runs below 1.0.
  F3: dt 0.001 shows 2 or fewer of 6 below 1.0, OR dt 0.0003 shows 3 or more of 6 below 1.0.
      Either one closes the dt effect for this geometry.

Usage: python3 -I file_round3_2026-11-28.py <repo_root>
Writes only under <repo_root>/out/requests/2026-11-28/r3/lab-vernier/.
"""
import json
import os
import sys

ROOT = sys.argv[1]
OUT = os.path.join(ROOT, "out", "requests", "2026-11-28", "r3", "lab-vernier")
os.makedirs(OUT, exist_ok=True)

ARMS = [
    (0.0003, range(1, 7)),
    (0.001, range(7, 13)),
]

for dt, nums in ARMS:
    for n in nums:
        rid = f"2026-11-28/r3/lab-vernier/{n:03d}"
        req = {
            "request_id": rid,
            "lab": "lab-vernier",
            "account": "research",
            "purpose": (
                f"Sample-timing replicate (round 3). A-A at rest, r0 1.0 horizontal (x 4.5, 5.5; y 5.0), "
                f"T 0.6, sample_dt {dt}. Pre-registered P2/F3 in NOTEBOOK.md. Tests whether sample_dt sets the "
                f"fraction of runs below separation 1.0 at t = 0.60."
            ),
            "setup": {
                "particles": [
                    {"species": "A", "pos": [4.5, 5.0], "vel": [0.0, 0.0]},
                    {"species": "A", "pos": [5.5, 5.0], "vel": [0.0, 0.0]},
                ],
                "duration": 0.6,
                "sample_dt": dt,
            },
            "instruments": ["tracker"],
        }
        path = os.path.join(OUT, f"{n:03d}.json")
        with open(path, "w") as f:
            json.dump(req, f, indent=2)
            f.write("\n")
        print("wrote", path)
