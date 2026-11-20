#!/usr/bin/env python3
"""Writes lab-c round-2 reviews (P-0007, P-0008, P-0009, P-0010, P-0011) and the grant vote.

Run with: python3 -I write_round2_reviews.py OUT_ROOT
Verdict rules applied (tools/editor.py): replicated needs >= 3 cited in-domain runs with
judged error <= 3 x predicted_error; falsified needs every cited in-domain run above that;
narrowed and inconclusive carry no bar and are used where a bar would not be met.
"""
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])

REVIEWS = {
    "P-0007": {
        "verdict": "narrowed",
        "evidence": ["2026-11-19/r3/lab-c/001", "2026-11-19/r1/lab-c/020",
                     "2026-11-20/r1/lab-c/011", "2026-11-20/r1/lab-c/012"],
        "proposed_domain": {"species": ["A", "B", "C"], "r_range": [4.95, 5.05], "max_particles": 3},
        "comment": (
            "Narrowed (lab-c, round 2). The model.py accepts only pairwise separations within 0.05 of 5.0 "
            "(abs(sep - R0) > 0.05 raises). The claims state 3.75-5.0 (c2) and 4.5-5.5 (c1), so the model does not "
            "predict those ranges. 2026-11-20/r1/lab-c/011 (side 4.5) and 012 (side 4.0) are refused by it, so the "
            "judge cannot score them against P-0007. I cite them for the physics only: they match P-0008's pair law at "
            "tracker noise (judged 0.0073 and 0.0072). Endpoint evidence the model does accept: 2026-11-19/r3/lab-c/001 "
            "(A, A, A, side 5.0, T=1.5) at judged 0.0069, with per-particle residual rms 0.042-0.053 per coordinate and "
            "zero-force null 0.22 (analysis/p0007_c2_check.py); 2026-11-19/r1/lab-c/020 (A, B, C, side 5.0, T=2) at 0.0072. "
            "The physics is consistent with my data at sides 4.0-5.0; the defect is the model's domain. Recommend either "
            "making model.py accept the stated range or narrowing the statement to separations 4.95-5.05, as proposed. "
            "No in-domain c1 run of mine exists apart from the endpoint. The judged metric (RMSE/10) sits at the noise "
            "floor (0.0071) and does not resolve a few-percent coupling error."),
    },
    "P-0008": {
        "verdict": "replicated",
        "evidence": ["2026-11-20/r1/lab-c/007", "2026-11-20/r1/lab-c/008", "2026-11-20/r1/lab-c/009",
                     "2026-11-20/r1/lab-c/010", "2026-11-20/r1/lab-c/011", "2026-11-20/r1/lab-c/012"],
        "comment": (
            "Replicated (lab-c, round 2), with scope. c1 (four bodies, T=1): 2026-11-20/r1/lab-c/007 (A, B, C, A at "
            "separations 3.2-4.97), 008 (B, B, C, C, 3.5 square), 009 (A, A, B, C, 3.5 square). Judged 0.0072, 0.0071, "
            "0.0070 against the noise floor 0.0071. Minimum pair separation along the runs 2.54, 2.99, 2.51. None is "
            "the 3 x 4 rectangle of the statement; they test the same pair sum at other four-body geometries. "
            "c2 (three bodies): 010 (A, B, C equilateral side 4.0, T=2.0, minimum 2.79), 011 (A, A, A side 4.5, T=1.5, "
            "minimum 2.79), 012 (A, A, A side 4.0, T=1.0, minimum 2.98); judged 0.0072, 0.0073, 0.0072. 010 and 011 run "
            "past the statement's T=1 and side-3 triangle, so they are a wider test. Earlier in-domain runs at sides 3 "
            "and 5 (2026-11-19/r1/lab-c/020, 2026-11-19/r2/lab-c/002, 2026-11-19/r3/lab-c/002) are not cited here. "
            "Limit I checked: contact. Runs whose minimum pair separation falls below about 1.5 break the law "
            "(2026-11-17/r2/lab-c/001 and 009, 2026-11-18/r2/lab-c/001, 2026-11-19/r1/lab-c/021; minima 0.01-0.34). "
            "The statement is silent on contact, so I ask the author to add a closest-approach limit (minimum pair "
            "separation of at least 2). The judged metric cannot see a few-percent coupling error (noise floor 0.0071 "
            "against predicted_error 0.07), so this is a replication at noise, not a precision test."),
    },
    "P-0009": {
        "verdict": "inconclusive",
        "evidence": ["2026-11-19/r1/lab-c/023", "2026-11-19/r1/lab-c/024", "2026-11-19/r1/lab-c/025"],
        "comment": (
            "Interim (lab-c, round 2): inconclusive for the three-body statement. What I can test: the pair coefficients "
            "P-0009 uses at separation 5. My two-body runs at side 5, at rest, T=2 (2026-11-19/r1/lab-c/023 B-C, 024 C-C, "
            "025 B-B) are in domain (species B, C; separation 5.00; up to three particles) and each matches at the noise "
            "floor (judged 0.0070-0.0071). One coupling scale fitted per run to the tracker data (sigma 0.05 per "
            "coordinate; analysis/coupling_scale_scan.py): B-C 0.98 +/- 0.02, C-C 1.01 +/- 0.01, B-B 1.03 +/- 0.02, "
            "pooled 1.007 +/- 0.009. So the pair coefficients at separation 5 agree with P-0005 to about 1-2%. This does "
            "not test c1, which is a three-body statement with no three-body term. My only three-body run at side 5 "
            "(2026-11-19/r1/lab-c/020) contains an A and is outside P-0009's species list. I have filed the B, C, C "
            "equilateral triangle at side 5, T=2, on the review account (2026-11-20/r2/lab-c/001); the verdict will be "
            "finalized from it. Not tested: the model accepts moving particles without a check, while the statement says "
            "at rest."),
    },
    "P-0010": {
        "verdict": "narrowed",
        "evidence": ["2026-11-18/r2/lab-c/004", "2026-11-19/r1/lab-c/007", "2026-11-19/r2/lab-c/008",
                     "2026-11-19/r1/lab-c/013", "2026-11-17/r3/lab-c/004", "2026-11-19/r2/lab-c/009",
                     "2026-11-19/r2/lab-c/001", "2026-11-19/r1/lab-c/019",
                     "2026-11-19/r1/lab-c/008", "2026-11-19/r1/lab-c/009", "2026-11-19/r2/lab-c/005",
                     "2026-11-19/r2/lab-c/003", "2026-11-19/r1/lab-c/012", "2026-11-19/r1/lab-c/010"],
        "comment": (
            "Narrowed (lab-c, round 2). Judged errors cannot separate this claim from noise: every in-domain run of mine "
            "(two particles at rest, r0 6-9, T<=6) scores 0.0066-0.0074 against a noise floor of 0.0071, so the replication "
            "bar is met by all of them. A per-run fit of one coupling scale s (K multiplied by s, chi-square against the "
            "tracker data at sigma 0.05 per coordinate; analysis/coupling_scale_scan.py) is more informative. "
            "Non-A-A pairs agree with P-0010 to within about 3%: AB 1.00 (r0 6), 0.99 (7), 0.95 (9); AC 1.02 (6), 1.00 (7), "
            "1.05 +/- 0.02 (8); BB 0.98 (6), 0.96 (7); BC 1.02 (6), 0.99 (7); CC 1.01 (6), 1.02 (7), 1.00 (9). "
            "A-A is 2-4% low: pooled 0.964 +/- 0.003 at r0 6 (two runs, outside the claim's 3% tolerance); 0.977 +/- 0.005 "
            "at 7; 0.959 +/- 0.011 and 0.949 +/- 0.018 at 8; 0.963 +/- 0.013 and 0.981 +/- 0.004 at 9. One A-A run at 9 "
            "(T=3, 0.869 +/- 0.027) is about 4 sigma from the T=6 run at 9, which is unresolved. A-A is the only channel "
            "that fails the claim's own tolerance. Recommend excluding the A-A pair (the domain schema cannot express a "
            "pair-level exclusion) or refitting the A-A factor. Caveats: the fit assumes K constant over each run and "
            "sigma 0.05; chi-square per point is 1.0-1.08, so the errors may be 2-5% too small. Two long A-A runs at r0 6 "
            "and 8 (T=6, the model's limit) are on the review account (2026-11-20/r2/lab-c/002, 003); the verdict will be "
            "finalized from them."),
    },
    "P-0011": {
        "verdict": "replicated",
        "evidence": ["2026-11-17/r1/lab-c/001", "2026-11-17/r1/lab-c/002", "2026-11-17/r2/lab-c/007",
                     "2026-11-18/r1/lab-c/006", "2026-11-17/r3/lab-c/011", "2026-11-17/r3/lab-c/012"],
        "comment": (
            "Replicated for c1 and c2 (lab-c, round 2). c3 (walls) is not tested by me. Six lone-particle runs in domain "
            "(one particle; species A, B, C; T 10-100). Judged errors 0.0067-0.0078 against the noise floor 0.0071 "
            "(sqrt(2) x 0.05 / 10), inside 3 x 0.005. My own residual check against model.py (analysis/"
            "lone_noise_check_2026-11-20.py; the model is reflected free flight using each run's velocity): pooled sd per "
            "coordinate 0.0507 over 16,400 residuals, kurtosis 2.99, mean +0.0008. By species: A 0.0512 (8,200), C 0.0503 "
            "(8,000), B 0.0479 (200, one short run). c1 says 0.050; my pooled 0.0507 +/- 0.0003 is about 2 sigma above it, "
            "a small excess rather than a refutation. c2 holds within the resolution I have; B rests on one run. c3: none "
            "of my runs starts near a wall, and I did not isolate the samples near x = 0, so the 17% negative-x claim is "
            "untested here. The model uses the velocity, so the claim covers moving lone particles too; the paper's text "
            "says the model has zero velocity, which is inaccurate."),
    },
}

for pid, body in REVIEWS.items():
    assert len(body["comment"]) <= 2000, (pid, len(body["comment"]))
    doc = {"paper_id": pid, "lab": "lab-c", "verdict": body["verdict"], "evidence": body["evidence"],
           "comment": body["comment"]}
    if "proposed_domain" in body:
        doc["proposed_domain"] = body["proposed_domain"]
    path = OUT / "reviews" / pid / "lab-c.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2) + "\n")
    print("wrote", path, len(body["comment"]))

vote = {"lab": "lab-c", "date": "2026-11-20", "vote": "lab-a",
        "reason": ("Clean pair test at r=2 with a pre-registered power-law prediction, cheap (1.02 credits). "
                   "Our r=1 and r=2 runs show deviations from K/r^2.5 at short range, so this is the test that matters.")}
assert len(vote["reason"]) <= 300
path = OUT / "grants" / "2026-11-20" / "votes" / "lab-c.json"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(vote, indent=2) + "\n")
print("wrote", path)
