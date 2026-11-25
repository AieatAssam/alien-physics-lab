#!/usr/bin/env python3
"""Writes lab-c round-2 review verdicts (2026-11-25) to out/reviews/P-XXXX/lab-c.json, validated against
protocol/review.schema.json. Evidence = lab-c review-account round-1 ids scored in scores_reviews_2026-11-25.txt.
"""
import json
from pathlib import Path
import jsonschema
ROOT = Path(__file__).resolve().parents[4]
SCHEMA = json.loads((ROOT / "protocol" / "review.schema.json").read_text())
D = "2026-11-25/r1/lab-c/"
REVIEWS = {
 "P-0026": {
  "paper_id": "P-0026", "lab": "lab-c", "verdict": "replicated",
  "evidence": [D + "001", D + "002", D + "003"],
  "comment": ("Three in-domain review runs (001-003): 16 A at rest, random layouts, all pairs in [1.5, 10.5], T = 0.3, dt 0.003. "
              "Judge-style RMSE/L with the paper's predict(): 0.00508, 0.00510, 0.00501 against bar 3 x 0.007 = 0.021. "
              "Replicated at the claim's stated scope (N <= 16, T <= 0.3, species A). Limit: the judge cannot separate exponent 2.099 "
              "from 2.5 at these durations, so this supports the sum at T <= 0.3, not the exponent. "
              "Non-citable context: a research run at r0 = 2.0 (2026-11-25/r1/lab-c/012, not cited here) is matched at noise level by this pair law, "
              "while the P-0027 clamp below 3 gives RMSE/L 0.013 on the same run (one run; replication pending)."),
 },
 "P-0027": {
  "paper_id": "P-0027", "lab": "lab-c", "verdict": "narrowed",
  "evidence": [D + "004", D + "006", D + "007", D + "008"],
  "proposed_domain": {"species": ["A"], "r_range": [5.0, 9.0], "max_particles": 2},
  "comment": ("Narrowed to r0 in [5, 9]. Runs 006 (r0 5, T 2), 007 (r0 7, T 3), 008 (r0 9, T 3) pass: RMSE/L 0.00502, 0.00497, 0.00507, bar 0.021. "
              "Run 004 (r0 = 3.0, T = 1.5, in domain) fails: predict() returns RMSE/L 373, because its integrator diverges after t about 1.21 "
              "when the pair passes through near-contact (model separations reach 10^3-10^4). Before t = 1.2 the table matches the run at "
              "RMSE/L 0.00525. The observed pair reaches a raw minimum separation of 0.018 and then separates on the far side, so the claim's "
              "window at r0 < 5 includes passes through near-contact, where the claim gives no law (K is clamped at K(3) below 3) and the model output diverges. "
              "Run 005 (diagonal, r0 = 2.9999995) is 5e-7 below the strict domain and is not cited. "
              "The judge cannot separate the table from a power-law continuation at r0 5 to 9 (difference below 0.001), so the narrowed domain is "
              "supported by 006-008 and not by a discriminating test."),
 },
 "P-0028": {
  "paper_id": "P-0028", "lab": "lab-c", "verdict": "replicated",
  "evidence": [D + "009", D + "010", D + "011"],
  "comment": ("Three in-domain 8-particle review runs at the floor (009: 3x3 grid minus centre, spacing 3.02; 010: 8-circle, neighbour chord 3.02; "
              "011: 8-circle, chord 3.10), T = 1.0. Judge RMSE/L 0.00495, 0.00507, 0.00505, bar 0.021. Replicated at the claim's stated scope. "
              "Limits: the judge cannot test the sub-3 clamp here. The paper's model puts the closest pair approach at 2.18 to 2.54 over each run, where the "
              "table and a power-law continuation differ by less than the bar (0.006-0.009 RMSE/L). "
              "Non-citable context: research run 2026-11-25/r1/lab-c/012 (r0 = 2.0) does separate the clamp from the P-0026 law, so the table's "
              "K below 3 may be wrong (one run, not replicated; I am not citing it here). The judged runs reach only 2.18 to 2.54, a shallow part of that region, so they do not test it."),
 },
 "P-0029": {
  "paper_id": "P-0029", "lab": "lab-c", "verdict": "replicated",
  "evidence": [D + "006", D + "007", D + "008"],
  "comment": ("Three in-domain review runs within P-0029's domain and windows: 006 (r0 5, T 2.0), 007 (r0 7, T 3.0), 008 (r0 9, T 3.0). "
              "Judge RMSE/L 0.00502, 0.00497, 0.00507, bar 0.021. Replicated. Same runs back the narrowed P-0027 verdict. "
              "Limit: at these layouts the judge cannot separate the table from a power-law continuation (difference below 0.001 RMSE/L), so "
              "this does not test the K(r) shape. Out of scope: r0 below 5, which P-0029 withdraws."),
 },
}
for pid, obj in REVIEWS.items():
    jsonschema.validate(obj, SCHEMA)
    p = ROOT / "out" / "reviews" / pid
    p.mkdir(parents=True, exist_ok=True)
    (p / "lab-c.json").write_text(json.dumps(obj, indent=2) + "\n")
    print(pid, obj["verdict"], "ok")
