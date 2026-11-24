#!/usr/bin/env python3
"""Round-3 research requests (lab-c): A-A exponent test at r0 = 7 and 9 (H and V), plus a flat-to-5 check,
a replicate, and an exploratory A-B run at r0 = 9.

Pre-registration: out/labs/lab-c/analysis/prereg_AA_2026-11-24_r3.py (M1 = P 3.10, K 47.00; M2 = P-0027 table).
Decision rule (set before results; corrected from an earlier 1.2 / 1.5 threshold once the expected values were
computed, see prereg output: E[chi2/n of M2 | M1 true] ~ 1.17 to 1.19): on the horizontal r0 = 7 and 9 runs
(001, 002, 006, 008), pool chi2 over the four runs for M1 and M2 (sigma 0.05, window r >= 3).
  Delta = (pooled chi2/n of M2) - (pooled chi2/n of M1).  Delta >= +0.10 -> M1 (power law P 3.1) preferred.
  Delta <= -0.10 -> M2 (Plumbline table) preferred.  Otherwise undecided.
Rows 003-004 are orientation controls; 005 tests the flat-K claim on [3, 5]; 007 and 009 are exploratory; 008 is a pre-registered replicate of 001.
Writes out/requests/2026-11-24/r3/lab-c/NNN.json. Usage: python3 -I make_2026-11-24_r3_requests.py REPO_ROOT
"""
import json, sys
from pathlib import Path

REPO = Path(sys.argv[1])
OUT = REPO / "out/requests/2026-11-24/r3/lab-c"
OUT.mkdir(parents=True, exist_ok=True)
C = 5.0


def pair(r0, orient, species):
    h = r0 / 2
    a, b = ([C - h, C], [C + h, C]) if orient == "H" else ([C, C - h], [C, C + h])
    return [
        {"species": species[0], "pos": a, "vel": [0.0, 0.0]},
        {"species": species[1], "pos": b, "vel": [0.0, 0.0]},
    ]


# n, orient, r0, T, species, purpose
ROWS = [
    (1, "H", 7.0, 8.0, ("A", "A"),
     "Horizontal A-A pair at rest, r0 = 7, centre (5,5), T = 8. Exponent test (lab-c round 3): pre-registered "
     "power law P 3.10 vs P-0027 K(r) table; rule in analysis/prereg_AA_2026-11-24_r3.py."),
    (2, "H", 9.0, 8.0, ("A", "A"),
     "Horizontal A-A pair at rest, r0 = 9 (edge of P-0027 domain), centre (5,5), T = 8. Exponent test, pre-registered."),
    (3, "V", 7.0, 8.0, ("A", "A"),
     "Vertical A-A pair at rest, r0 = 7, centre (5,5), T = 8. Orientation control for 001."),
    (4, "V", 9.0, 8.0, ("A", "A"),
     "Vertical A-A pair at rest, r0 = 9, centre (5,5), T = 8. Orientation control for 002."),
    (5, "H", 5.0, 3.0, ("A", "A"),
     "Horizontal A-A pair at rest, r0 = 5, T = 3 (window closes near t = 2.2). Tests P-0027's flat-K claim on [3, 5]."),
    (6, "H", 9.0, 8.0, ("A", "A"),
     "Horizontal A-A pair at rest, r0 = 9, T = 8. Replicate of 002 (same geometry), pre-registered with 002."),
    (7, "H", 9.0, 8.0, ("A", "B"),
     "Horizontal A-B pair at rest, r0 = 9, centre (5,5), T = 8. Species check: is the A-B exponent from the "
     "notebook map (r 3 to 8) the same at r = 9? Exploratory, not pre-registered."),
    (8, "H", 7.0, 8.0, ("A", "A"),
     "Horizontal A-A pair at rest, r0 = 7, T = 8. Replicate of 001 (same geometry), pre-registered with 001."),
    (9, "H", 8.0, 10.0, ("A", "A"),
     "Horizontal A-A pair at rest, r0 = 8, centre (5,5), T = 10. Longer window than 004 (T = 6 did not reach separation 3). "
     "Exploratory; extends the r0 = 8 run past the T = 6 window."),
]

for n, orient, r0, dur, species, purpose in ROWS:
    req = {
        "request_id": f"2026-11-24/r3/lab-c/{n:03d}",
        "lab": "lab-c",
        "account": "research",
        "purpose": purpose,
        "setup": {"particles": pair(r0, orient, species), "duration": dur, "sample_dt": 0.01},
        "instruments": ["tracker"],
    }
    (OUT / f"{n:03d}.json").write_text(json.dumps(req, indent=2) + "\n")
    print("wrote", OUT / f"{n:03d}.json")
