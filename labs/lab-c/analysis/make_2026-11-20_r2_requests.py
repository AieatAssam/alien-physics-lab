#!/usr/bin/env python3
"""Writes lab-c round-2 requests (2026-11-20/r2) under out/requests/.

Run with: python3 -I make_2026-11-20_r2_requests.py OUT_ROOT
Review account (cites papers under review): 001 P-0009 BCC triangle side 5; 002 and 003 P-0010 A-A pairs at r0 6 and 8, T=6.
Research account: 004-007 short-range pairs, predictions in pred_2026-11-20_r2_shortrange.json.
Budget (cost = 1 + 0.02 * particles * duration): review 1.12 + 1.24 + 1.24 = 3.60 of 15 allowance
(8.49 left after round 1); research 1.016 * 3 + 1.04 = 4.09 of 40 (33.94 left).
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) / "requests" / "2026-11-20" / "r2" / "lab-c"
ROOT.mkdir(parents=True, exist_ok=True)
SIDE = 5.0 * math.sqrt(3) / 2  # height of equilateral triangle, side 5
TRI = [(2.5, 4.0), (7.5, 4.0), (5.0, 4.0 + SIDE)]


def part(species, pos):
    return {"species": species, "pos": [round(pos[0], 6), round(pos[1], 6)], "vel": [0.0, 0.0]}


def write(nnn, body):
    (ROOT / f"{nnn}.json").write_text(json.dumps(body, indent=2) + "\n")


REQS = {
    "001": {
        "request_id": "2026-11-20/r2/lab-c/001", "lab": "lab-c", "account": "review", "cites_paper": "P-0009",
        "purpose": ("P-0009 c1 three-body replicate: B, C, C equilateral triangle, side 5, at rest, T=2. "
                    "lab-c's own side-5 runs are two-body only and cannot test the three-body statement. "
                    "Applies P-0009's rule (rms <= 0.07 per coordinate supports, > 0.12 refutes) and its "
                    "coefficients (B-B 6.12, B-C -6.10, C-C 12.36)."),
        "setup": {"particles": [part("B", TRI[0]), part("C", TRI[1]), part("C", TRI[2])],
                  "duration": 2.0, "sample_dt": 0.02},
        "instruments": ["tracker", "census"],
    },
    "002": {
        "request_id": "2026-11-20/r2/lab-c/002", "lab": "lab-c", "account": "review", "cites_paper": "P-0010",
        "purpose": ("P-0010 c1 long-run test of the A-A factor at r0=6, two A particles at rest, T=6 (the model's "
                    "limit). lab-c's A-A fits at r0 6 give 0.96-0.97 of P-0010's coefficient (2 runs), outside its "
                    "3% tolerance. Rule: fitted A-A scale within 0.97-1.03 supports P-0010; outside it refutes."),
        "setup": {"particles": [part("A", (2.0, 5.0)), part("A", (8.0, 5.0))], "duration": 6.0, "sample_dt": 0.02},
        "instruments": ["tracker", "census"],
    },
    "003": {
        "request_id": "2026-11-20/r2/lab-c/003", "lab": "lab-c", "account": "review", "cites_paper": "P-0010",
        "purpose": ("P-0010 c1 long-run test of the A-A factor at r0=8, two A particles at rest, T=6. lab-c's A-A fits at "
                    "r0 8 give 0.95-0.96 of P-0010's coefficient (2 runs). Same rule as 002: fitted scale within "
                    "0.97-1.03 supports, outside refutes."),
        "setup": {"particles": [part("A", (1.0, 5.0)), part("A", (9.0, 5.0))], "duration": 6.0, "sample_dt": 0.02},
        "instruments": ["tracker", "census"],
    },
    "004": {
        "request_id": "2026-11-20/r2/lab-c/004", "lab": "lab-c", "account": "research",
        "purpose": ("Short-range AA law (H16). Two A at rest, r0=1.5, T=0.4. Pre-registered P-0008 power-law prediction in "
                    "analysis/pred_2026-11-20_r2_shortrange.json. Use only samples where the prediction is >= 0.5. "
                    "Falsifier: late-window mean residual (measured - predicted) beyond 0.1 with the sign measured > predicted."),
        "setup": {"particles": [part("A", (4.25, 5.0)), part("A", (5.75, 5.0))], "duration": 0.4, "sample_dt": 0.0002},
        "instruments": ["tracker", "census"],
    },
    "005": {
        "request_id": "2026-11-20/r2/lab-c/005", "lab": "lab-c", "account": "research",
        "purpose": ("Short-range AC law (H16), repulsive pair. Two particles A and C at rest, r0=1.5, T=0.4. Prediction in "
                    "pred_2026-11-20_r2_shortrange.json. Falsifier: late-window mean residual beyond 0.1 with sign measured < predicted "
                    "(weaker repulsion at short range)."),
        "setup": {"particles": [part("A", (4.25, 5.0)), part("C", (5.75, 5.0))], "duration": 0.4, "sample_dt": 0.0002},
        "instruments": ["tracker", "census"],
    },
    "006": {
        "request_id": "2026-11-20/r2/lab-c/006", "lab": "lab-c", "account": "research",
        "purpose": ("Short-range CC law (H16). Two C at rest, r0=1.5, T=0.4. Round-1 CC at r0=1.0 (2026-11-20/r1/lab-c/006) "
                    "ran 0.1-0.3 past the power-law prediction. Prediction in pred_2026-11-20_r2_shortrange.json. Falsifier: "
                    "late-window mean residual beyond 0.1 with sign measured > predicted."),
        "setup": {"particles": [part("C", (4.25, 5.0)), part("C", (5.75, 5.0))], "duration": 0.4, "sample_dt": 0.0002},
        "instruments": ["tracker", "census"],
    },
    "007": {
        "request_id": "2026-11-20/r2/lab-c/007", "lab": "lab-c", "account": "research",
        "purpose": ("Where the deviation starts: two A at rest, r0=2.5, T=1.0, below P-0008's 2.95 lower bound. Prediction in "
                    "pred_2026-11-20_r2_shortrange.json. Falsifier: late-window mean residual beyond 0.1 with sign measured > predicted "
                    "while predicted separation is above 1.7."),
        "setup": {"particles": [part("A", (3.75, 5.0)), part("A", (6.25, 5.0))], "duration": 1.0, "sample_dt": 0.0005},
        "instruments": ["tracker", "census"],
    },
}
for nnn, body in REQS.items():
    if body["account"] != "review":
        body.pop("cites_paper", None)
    write(nnn, body)
    print(nnn, body["account"], "cost", round(1 + 0.02 * len(body["setup"]["particles"]) * body["setup"]["duration"], 4))
