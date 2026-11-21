#!/usr/bin/env python3
"""Round 2 (2026-11-21) requests for lab-c. Writes out/requests/2026-11-21/r2/lab-c/001..013.json.
Research 001-008: close-range r0 = 1.0 pairs at a new centre (3, 6) plus vertical BB/CC replicates, T = 0.3, dt = 0.0005.
Review 009-011: P-0012 (lab-a) AA at r = 1.0, T = 0.15 (the claim's duration limit), three placements.
Review 012-013: P-0015 (lab-vernier) BC at r = 1.0, T = 0.6 (the claim's stated domain), two orientations.
Run: python3 -I make_2026-11-21_r2_requests.py REPO_ROOT
"""
import json, sys
from pathlib import Path
ROOT = Path(sys.argv[1]) / "out" / "requests" / "2026-11-21" / "r2" / "lab-c"
ROOT.mkdir(parents=True, exist_ok=True)
RID = "2026-11-21/r2/lab-c/{:03d}"

def P(sp, x, y):
    return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}

def write(n, account, purpose, parts, T, dt, cites=None):
    req = {"request_id": RID.format(n), "lab": "lab-c", "account": account, "purpose": purpose,
           "setup": {"particles": parts, "duration": T, "sample_dt": dt},
           "instruments": ["tracker", "census"]}
    if cites:
        req["cites_paper"] = cites
    (ROOT / f"{n:03d}.json").write_text(json.dumps(req, indent=2) + "\n", encoding="utf-8")

close = [("AA", "AA"), ("AB", "AB"), ("AC", "AC"), ("BB", "BB"), ("BC", "BC"), ("CC", "CC")]
for i, (pair, _) in enumerate(close, start=1):
    write(i, "research", f"Close-range {pair} at r0 = 1.0, centre (3,6): location replicate of 2026-11-21/r1 {i:03d} (centre (5,5)). Tests whether the per-pair short-range scale is location-independent.",
          [P(pair[0], 2.5, 6.0), P(pair[1], 3.5, 6.0)], 0.3, 0.0005)
write(7, "research", "Close-range BB, vertical orientation at (7,3)-(7,4): isotropy and replicate of BB at r0 = 1.0 (BB scale disagreed between windows).",
      [P("B", 7.0, 3.0), P("B", 7.0, 4.0)], 0.3, 0.0005)
write(8, "research", "Close-range CC, vertical orientation at (7,3)-(7,4): isotropy and replicate of CC at r0 = 1.0 (CC scale disagreed between windows).",
      [P("C", 7.0, 3.0), P("C", 7.0, 4.0)], 0.3, 0.0005)
for n, (a, b, c) in zip((9, 10, 11), [((2.0, 2.0), (3.0, 2.0), "horizontal near the lower-left corner"),
                                      ((5.0, 4.5), (5.0, 5.5), "vertical at the centre"),
                                      ((7.0, 8.0), (8.0, 8.0), "horizontal at upper right")]):
    write(n, "review", f"Review of P-0012 claim c1 (A-A pair at rest, r0 = 1.0, duration 0.15): run {c}. Judged-domain check: species A, two particles, separation exactly 1.0.",
          [P("A", *a), P("A", *b)], 0.15, 0.0001, cites="P-0012")
write(12, "review", "Review of P-0015 claim c1 (B-C pair at r0 = 1.0, T <= 0.6): horizontal, B at (4.5,5) and C at (5.5,5), T = 0.6.",
      [P("B", 4.5, 5.0), P("C", 5.5, 5.0)], 0.6, 0.0005, cites="P-0015")
write(13, "review", "Review of P-0015 claim c1 (B-C pair at r0 = 1.0, T <= 0.6): vertical, B at (5,4.5) and C at (5,5.5), T = 0.6.",
      [P("B", 5.0, 4.5), P("C", 5.0, 5.5)], 0.6, 0.0005, cites="P-0015")
print("wrote", len(list(ROOT.glob("*.json"))), "requests to", ROOT)
