#!/usr/bin/env python3
"""Generator for lab-c round-2 requests, 2026-11-25 (validated against protocol/request.schema.json).
Research (sub-3 A-A pre-registered round, see prereg_subthree_2026-11-25.json): 001-006.
Review (P-0030 A-C edge runs, 2 of the remaining 2.78 review credits): 007-008.
Writes to out/requests/2026-11-25/r2/lab-c/NNN.json.
"""
import json, math
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[4]   # .../alien-physics-lab
DATE, RND, LAB = "2026-11-25", "r2", "lab-c"
OUT = ROOT / "out" / "requests" / DATE / RND / LAB
SCHEMA = json.loads((ROOT / "protocol" / "request.schema.json").read_text())

def pair(p1, p2, T, dt, sp=("A", "A")):
    return {"particles": [
        {"species": sp[0], "pos": list(p1), "vel": [0.0, 0.0]},
        {"species": sp[1], "pos": list(p2), "vel": [0.0, 0.0]}],
        "duration": T, "sample_dt": dt}

h = 2.0 / math.sqrt(2) / 2   # half-offset for diagonal r0 = 2.0
REQS = [
    ("001", "research", None,
     "Research (not citable): A-A pair at rest, r0 = 2.0, vertical. Orientation replicate of 012 (horizontal). "
     "Pre-registered: clamped table (TAB) predicts closest approach 0.071 near T 0.6; P-0026 law (P26) predicts 0.690 at T 0.6.",
     pair((5.0, 4.0), (5.0, 6.0), 0.6, 0.001)),
    ("002", "research", None,
     "Research (not citable): A-A pair at rest, r0 = 2.0, diagonal (45 degrees). Second orientation for 012. "
     "Pre-registered: TAB 0.071, P26 0.690 closest approach at T 0.6.",
     pair((5.0 - h, 5.0 - h), (5.0 + h, 5.0 + h), 0.6, 0.001)),
    ("003", "research", None,
     "Research (not citable): A-A pair at rest, r0 = 1.75, horizontal, T = 0.5. Pre-registered: TAB 0.073 at t 0.47; P26 0.511 at t 0.50.",
     pair((4.125, 5.0), (5.875, 5.0), 0.5, 0.001)),
    ("004", "research", None,
     "Research (not citable): A-A pair at rest, r0 = 1.75, vertical, T = 0.5. Orientation replicate of 003. Same pre-registered predictions.",
     pair((5.0, 4.125), (5.0, 5.875), 0.5, 0.001)),
    ("005", "research", None,
     "Research (not citable): A-A pair at rest, r0 = 2.75, horizontal, T = 1.0. Pre-registered: TAB closest approach 0.632, P26 0.848 at t 1.0.",
     pair((3.625, 5.0), (6.375, 5.0), 1.0, 0.001)),
    ("006", "research", None,
     "Research (not citable): exact repeat of 012 (A-A pair at rest, r0 = 2.0, horizontal, T = 0.6). Tests run-to-run reproducibility of the close-approach observable.",
     pair((4.0, 5.0), (6.0, 5.0), 0.6, 0.001)),
    ("007", "review", "P-0030",
     "Review of P-0030 at the low edge of its domain: one A and one C at rest, separation 2.5 exactly, diagonal, T = 2.0 (the claim's window limit). "
     "Pre-registered: P-0030 predicts repulsion with the tabulated K_AC, K_CA at r 2.5.",
     {"particles": [{"species": "A", "pos": [4.25, 4.0], "vel": [0.0, 0.0]},
                    {"species": "C", "pos": [5.75, 6.0], "vel": [0.0, 0.0]}],
      "duration": 2.0, "sample_dt": 0.001}),
    ("008", "review", "P-0030",
     "Review of P-0030 at the high edge of its domain: one A and one C at rest, separation 3.5 exactly, vertical, T = 2.0. "
     "Orientation and edge check against 007.",
     {"particles": [{"species": "A", "pos": [5.0, 3.25], "vel": [0.0, 0.0]},
                    {"species": "C", "pos": [5.0, 6.75], "vel": [0.0, 0.0]}],
      "duration": 2.0, "sample_dt": 0.001}),
]

OUT.mkdir(parents=True, exist_ok=True)
for nnn, acct, cites, purpose, setup in REQS:
    obj = {"request_id": f"{DATE}/{RND}/{LAB}/{nnn}", "lab": LAB, "account": acct,
           "purpose": purpose, "setup": setup, "instruments": ["tracker"]}
    if cites:
        obj["cites_paper"] = cites
    jsonschema.validate(obj, SCHEMA)
    cost_k = 0.02
    cost = 1 + cost_k * len(setup["particles"]) * setup["duration"]
    assert setup["duration"] / setup["sample_dt"] <= 2000 + 1e-9
    (OUT / f"{nnn}.json").write_text(json.dumps(obj, indent=2) + "\n")
    print(nnn, acct, cites or "-", f"cost={cost:.3f}")
