#!/usr/bin/env python3
"""Round 3 (2026-11-20) research requests for lab-c (Nullius). Account: research. Writes into OUT.

Run with: python3 -I make_2026-11-20_r3_requests.py OUT_ROOT

Question: the short-range pair law. The P-0008 law (K / r^2.5, P-0005 coefficients) overstates the pair
coupling at r0 = 1.5 to 2.5 by 8-25% (round 2: scale s = 0.75 AA, 0.81 AC, 0.87 CC at r0 1.5; AA 0.92 at 2.5).
The open questions:
  (a) does s fall further as r0 drops to 1.0 (AA), and rise back to 1 at 3 to 4 (P-0008 domain edge)?
  (b) is the deviation the same for every species pair (round 1 suggested BB shows none)?
Each request is pre-registered by the expected range of s, given in its purpose. s is the coupling scale
that best fits the pre-collision samples (scale_fit_short_range.py method). Falsifiers are listed per run.
"""
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
DATE = "2026-11-20"
ROUND = "r3"
LAB = "lab-c"


def pair(sp1, sp2, r0, cx=5.0, cy=5.0):
    return [
        {"species": sp1, "pos": [round(cx - r0 / 2, 6), cy], "vel": [0.0, 0.0]},
        {"species": sp2, "pos": [round(cx + r0 / 2, 6), cy], "vel": [0.0, 0.0]},
    ]


REQS = [
    # key, pair, r0, T, dt, purpose
    ("AA", "A", "A", 1.0, 0.3, 0.0002,
     "Short-range AA at r0=1.0 at rest, T=0.3 (pre-collision window). Expected s in [0.55, 0.80] if the "
     "AA deficit keeps growing as r falls; falsifier: s >= 0.90 (deficit not monotone in r)."),
    ("AA", "A", "A", 2.0, 0.6, 0.0004,
     "Short-range AA at r0=2.0 at rest, T=0.6. Expected s in [0.80, 0.90] (between 0.75 at r0 1.5 and 0.92 at 2.5); "
     "falsifier: s outside [0.72, 0.97]."),
    ("AA", "A", "A", 3.0, 2.0, 0.001,
     "AA at r0=3.0 at rest, T=2.0: P-0008's domain edge (2.95 to 5.05). Expected s in [0.97, 1.03]; "
     "falsifier: s < 0.95 (P-0008 coefficient wrong at its own domain edge)."),
    ("AA", "A", "A", 3.5, 1.5, 0.00075,
     "AA at r0=3.5 at rest, T=1.5, inside P-0008's domain. Expected s in [0.97, 1.03]; "
     "falsifier: s < 0.95 or > 1.05."),
    ("AA", "A", "A", 4.0, 2.0, 0.001,
     "AA at r0=4.0 at rest, T=2.0, inside P-0008's domain. Expected s in [0.98, 1.03]; "
     "falsifier: s < 0.95 or > 1.05."),
    ("AA", "A", "A", 1.5, 0.4, 0.0002,
     "Replicate of 2026-11-20/r2/lab-c/004 (AA at r0=1.5, at rest, T=0.4) to test the reproducibility of "
     "its scale s=0.75. Expected s in [0.70, 0.80]; falsifier: s > 0.85 or < 0.65."),
    ("AB", "A", "B", 1.5, 0.4, 0.0002,
     "AB at r0=1.5 at rest, T=0.4. Round-1 AB at r0=1 showed weaker attraction. Expected s in [0.75, 0.95]; "
     "falsifier: s in [0.97, 1.03] (AB shows no short-range deficit)."),
    ("AC", "A", "C", 1.5, 0.4, 0.0002,
     "Replicate of 2026-11-20/r2/lab-c/005 (AC at r0=1.5, repulsive, at rest, T=0.4). Expected s in [0.76, 0.86]; "
     "falsifier: s > 0.90 or < 0.72."),
    ("AC", "A", "C", 2.5, 1.0, 0.0005,
     "AC at r0=2.5, repulsive, at rest, T=1.0. Expected s in [0.85, 0.97]; falsifier: s in [0.98, 1.02]."),
    ("BB", "B", "B", 1.5, 0.4, 0.0002,
     "BB at r0=1.5 at rest, T=0.4. Round-1 BB at r0=1 showed no deviation. Expected s in [0.97, 1.03]; "
     "falsifier: s < 0.92 (the deficit is not species-specific to AA, AC, CC)."),
    ("BC", "B", "C", 1.5, 0.4, 0.0002,
     "BC at r0=1.5, repulsive, at rest, T=0.4. Round-1 BC showed weaker repulsion. Expected s in [0.75, 0.95]; "
     "falsifier: s in [0.97, 1.03]."),
    ("CC", "C", "C", 2.5, 1.0, 0.0005,
     "CC at r0=2.5 at rest, T=1.0. Expected s in [0.90, 1.00] (CC at 1.5 gave 0.87); falsifier: s > 1.02 or s < 0.85."),
    ("BB", "B", "B", 2.5, 1.0, 0.0005,
     "BB at r0=2.5 at rest, T=1.0. Expected s in [0.97, 1.03]; falsifier: s < 0.94."),
    ("CC", "C", "C", 1.5, 0.4, 0.0002,
     "Replicate of 2026-11-20/r2/lab-c/006 (CC at r0=1.5, at rest, T=0.4). Expected s in [0.82, 0.92]; "
     "falsifier: s > 0.95 or < 0.78."),
    ("AC", "A", "C", 3.0, 2.0, 0.001,
     "AC (repulsive) at r0=3.0, at rest, T=2.0: P-0008 domain edge for this pair. Expected s in [0.97, 1.03]; "
     "falsifier: s < 0.94."),
    ("CC", "C", "C", 3.0, 2.0, 0.001,
     "CC at r0=3.0, at rest, T=2.0: P-0008 domain edge for this pair. Expected s in [0.97, 1.03]; "
     "falsifier: s < 0.94."),
    ("AA", "A", "A", 7.0, 3.0, 0.0015,
     "AA at r0=7.0 at rest, T=3.0 (before closest approach; P-0010 approach at r0 6 is near t=4). Scale s relative to "
     "P-0010 (G0, G1 times s). Expected s in [0.96, 1.02]; falsifier: s outside [0.93, 1.05]."),
]


def main():
    base = OUT / "requests" / DATE / ROUND / LAB
    base.mkdir(parents=True, exist_ok=True)
    meta = []
    for i, (key, sp1, sp2, r0, T, dt, purpose) in enumerate(REQS, start=1):
        rid = f"{DATE}/{ROUND}/{LAB}/{i:03d}"
        req = {
            "request_id": rid,
            "lab": LAB,
            "account": "research",
            "purpose": purpose,
            "setup": {
                "particles": pair(sp1, sp2, r0),
                "duration": T,
                "sample_dt": dt,
            },
            "instruments": ["tracker", "census"],
        }
        path = base / f"{i:03d}.json"
        path.write_text(json.dumps(req, indent=2) + "\n", encoding="utf-8")
        cost = 1 + 0.02 * 2 * T
        meta.append((i, key, sp1 + sp2, r0, T, dt, round(cost, 3), round(T / dt)))
    for row in meta:
        print(row)
    print("total est cost", round(sum(m[6] for m in meta), 3))


if __name__ == "__main__":
    main()
