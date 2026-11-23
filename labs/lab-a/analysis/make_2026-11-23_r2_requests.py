"""Plumbline 2026-11-23 round 2: A-A exponent test of P-0024 (review account, cites P-0024).
Design check (exponent_design_2026-11-23.py): P=2.10 vs best-fit P=2.5 differ by ~0.0002 RMSE/L per run at
r0 2.9, T 0.6 (about 2 sigma per run at tracker sigma 0.05, ~4 sigma for four runs). Not informative at T <= 0.3.
Writes out/requests/2026-11-23/r2/lab-a/001-004.json.
"""
import json, math, os, sys
out = sys.argv[1]
half = 2.9 / (2 * math.sqrt(2))  # diagonal half-offset for separation 2.9
layouts = {
    "001": ("horizontal, centre (5,5)", [[3.55, 5.0], [6.45, 5.0]]),
    "002": ("vertical, centre (5,5)", [[5.0, 3.55], [5.0, 6.45]]),
    "003": ("diagonal, centre (5,5)", [[5 - half, 5 - half], [5 + half, 5 + half]]),
    "004": ("horizontal, centre (4,4) (repeat of 001 at a different site)", [[2.55, 4.0], [5.45, 4.0]]),
}
d = os.path.join(out, "requests", "2026-11-23", "r2", "lab-a")
os.makedirs(d, exist_ok=True)
for nnn, (label, pos) in layouts.items():
    req = {
        "request_id": f"2026-11-23/r2/lab-a/{nnn}",
        "lab": "lab-a",
        "account": "review",
        "cites_paper": "P-0024",
        "purpose": ("Exponent test of P-0024 (A-A, P=2.10 vs 2.5). Two A at rest, separation 2.9 (in P-0024 domain, "
                    f"duration 0.6 window for r0 in [2.5,3.0]), {label}. Dense sampling (dt 0.001) to fit the "
                    "exponent by trajectory; the judged RMSE alone cannot discriminate."),
        "setup": {
            "particles": [{"species": "A", "pos": p, "vel": [0.0, 0.0]} for p in pos],
            "duration": 0.6,
            "sample_dt": 0.001,
        },
        "instruments": ["tracker"],
    }
    with open(os.path.join(d, nnn + ".json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    print(nnn, "written", "sep", round(math.dist(pos[0], pos[1]), 4))
