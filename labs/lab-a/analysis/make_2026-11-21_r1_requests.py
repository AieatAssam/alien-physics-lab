"""lab-a 2026-11-21 round 1: writes the research requests out/requests/2026-11-21/r1/lab-a/001-009.json.
Close-range pre-registrations (values written before any result; see NOTEBOOK.md):
  001/002 B-B at r0 = 1.0, T = 0.3: K_pred 4.0 (0.35 x K_AA(1.0)), rule +-10%
  003/004 C-C at r0 = 1.0, T = 0.15: K_pred in [8.0, 9.6], outside = surprise
  005/006 A-A at r0 = 1.25, T = 0.15: K_pred 12.5 (interpolation of K(1.0)=11.3 and K(1.5)=14.0), rule +-5%
  007/008 A-A at r0 = 0.85, T = 0.12: K_pred in [9.5, 11.5] (extrapolation), flat 18 refuted if K_fit < 13.3
  009     A-A at r0 = 1.0, diagonal, centred (3,3), T = 0.15: K_pred 11.3 +-5% (isotropy at close range)
Usage: python3 -I make_2026-11-21_r1_requests.py <repo_root>
"""
import json
import math
import os
import sys

root = sys.argv[1]
out_dir = os.path.join(root, "out", "requests", "2026-11-21", "r1", "lab-a")
os.makedirs(out_dir, exist_ok=True)
DT = 0.0005


def pair(sp_a, sp_b, cx, cy, r0, dirx=1.0, diry=0.0):
    ux, uy = dirx * r0 / 2, diry * r0 / 2
    return [
        {"species": sp_a, "pos": [cx - ux, cy - uy], "vel": [0.0, 0.0]},
        {"species": sp_b, "pos": [cx + ux, cy + uy], "vel": [0.0, 0.0]},
    ]


c = 1.0 / math.sqrt(2.0)
specs = [
    ("B pair r0=1.0, T=0.3 (replicate 1)", "B", "B", 5.0, 5.0, 1.0, 1.0, 0.0, 0.3),
    ("B pair r0=1.0, T=0.3 (replicate 2)", "B", "B", 5.0, 5.0, 1.0, 1.0, 0.0, 0.3),
    ("C pair r0=1.0, T=0.15 (replicate 1)", "C", "C", 5.0, 5.0, 1.0, 1.0, 0.0, 0.15),
    ("C pair r0=1.0, T=0.15 (replicate 2)", "C", "C", 5.0, 5.0, 1.0, 1.0, 0.0, 0.15),
    ("A pair r0=1.25, T=0.15 (replicate 1)", "A", "A", 5.0, 5.0, 1.25, 1.0, 0.0, 0.15),
    ("A pair r0=1.25, T=0.15 (replicate 2)", "A", "A", 5.0, 5.0, 1.25, 1.0, 0.0, 0.15),
    ("A pair r0=0.85, T=0.12 (replicate 1)", "A", "A", 5.0, 5.0, 0.85, 1.0, 0.0, 0.12),
    ("A pair r0=0.85, T=0.12 (replicate 2)", "A", "A", 5.0, 5.0, 0.85, 1.0, 0.0, 0.12),
    ("A pair r0=1.0, diagonal, centred (3,3), T=0.15", "A", "A", 3.0, 3.0, 1.0, c, c, 0.15),
]
for i, (label, sa, sb, cx, cy, r0, dx, dy, T) in enumerate(specs, start=1):
    parts = pair(sa, sb, cx, cy, r0, dx, dy)
    doc = {
        "request_id": "2026-11-21/r1/lab-a/%03d" % i,
        "lab": "lab-a",
        "account": "research",
        "purpose": ("Close-range two-particle run: %s, at rest. Pre-registered in analysis/"
                    "make_2026-11-21_r1_requests.py (K prediction and rule written before any result). "
                    "Fit K on the separation profile, P = 2.5 fixed, true r0 from the setup." % label),
        "setup": {"particles": parts, "duration": T, "sample_dt": DT},
        "instruments": ["tracker", "census"],
    }
    path = os.path.join(out_dir, "%03d.json" % i)
    with open(path, "w") as fh:
        json.dump(doc, fh, indent=1)
    print(path, "r0=%.4f T=%.2f n=%d" % (math.dist(parts[0]["pos"], parts[1]["pos"]), T, round(T / DT)))
