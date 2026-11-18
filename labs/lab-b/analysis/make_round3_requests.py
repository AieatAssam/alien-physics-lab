"""Writes lab-b round-3 requests (2026-11-18, r3) and checks them against the protocol rules.

Usage: python3 -I make_round3_requests.py <repo_root>
Outputs: <repo_root>/out/requests/2026-11-18/r3/lab-b/NNN.json

Research (budget 18.64 left): sep-2 and sep-4 pair sets for the rank-one test, plus
an equilateral three-body run for pairwise additivity. Review (cites P-0004,
budget 10.68 left): replicate P-0004's sep-5 claims, test its B-C prediction, and
check the sep-3 edge of its domain.
"""
import json
import math
import os
import sys

ROOT = sys.argv[1]
DATE_ROUND = "2026-11-18/r3/lab-b"
K_COST = 0.02
ALLOW_RESEARCH = 18.64
ALLOW_REVIEW = 10.68


def cost(n, T):
    return 1 + K_COST * n * T


def particle(sp, x, y):
    return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}


def request(num, account, purpose, parts, T, cites=None):
    dt = T / 2000
    assert T / dt <= 2000.0 + 1e-9, (num, T / dt)
    req = {
        "request_id": f"{DATE_ROUND}/{num:03d}",
        "lab": "lab-b",
        "account": account,
        "purpose": purpose,
        "setup": {"particles": parts, "duration": T, "sample_dt": dt},
        "instruments": ["tracker", "census"],
    }
    if cites:
        req["cites_paper"] = cites
    assert len(purpose) <= 500
    assert 1 <= len(parts) <= 16
    return req


reqs = []
# --- research: sep-2 pair set (T=1), x-axis, A/B/C pairs at rest (AA at 2 is 2026-11-18/r2/lab-b/017)
pairs2 = [("B", "B"), ("C", "C"), ("A", "B"), ("A", "C"), ("B", "C")]
for n, (s1, s2) in enumerate(pairs2, start=1):
    reqs.append(request(n, "research",
        f"Rank-one test at separation 2: {s1}-{s2} pair at rest on the x-axis, T=1, 2000 samples. "
        "Pre-collision window fit gives per-particle coefficients K_i(j). Rank-one (H10) predicts "
        "K_A(B)*K_B(A) = K_A(A)*K_B(B) (masses cancel). Sep 1.5 and 3 sets are r2/004-015.",
        [particle(s1, 4.0, 5.0), particle(s2, 6.0, 5.0)], 1.0))

# --- research: equilateral three-body (side 3), T=1. Pairwise-additivity prediction is written later from pair coefficients.
h = 3.0 * math.sqrt(3.0) / 2.0
tri = [particle("A", 4.0, 4.0), particle("B", 7.0, 4.0), particle("C", 5.5, 4.0 + h)]
reqs.append(request(6, "research",
    "Pairwise additivity: equilateral three-body A,B,C, side 3, at rest, T=1. Initial accelerations are "
    "predicted as vector sums of the pair coefficients measured at separation 3 (r2/010-015); "
    "the sum is the test of additivity.",
    tri, 1.0))

# --- research: sep-4 pair set (T=2), x-axis, (3,5)/(7,5)
pairs4 = [("B", "B"), ("C", "C"), ("A", "B"), ("A", "C"), ("B", "C")]
for n, (s1, s2) in enumerate(pairs4, start=7):
    reqs.append(request(n, "research",
        f"Rank-one and exponent test at separation 4: {s1}-{s2} pair at rest on the x-axis, T=2, "
        "2000 samples. Compares per-particle coefficients with the P-0003 range (3-6).",
        [particle(s1, 3.0, 5.0), particle(s2, 7.0, 5.0)], 2.0))

# --- review (cites P-0004), sep 5 replication and B-C prediction, sep 3 edge
rev_purposes = [
    ("A", "B", 2.5, 7.5, 5.0, 2.0,
     "P-0004 c1 replication: A-B pair at sep 5 on the x-axis, T=2. Predicts K_A(B)=9.0, K_B(A)=12.3 (P=2.5)."),
    ("A", "C", 2.5, 7.5, 5.0, 2.0,
     "P-0004 c2 replication: A-C pair at sep 5 on the x-axis, T=2. Predicts K_A(C)=-8.6, K_C(A)=-21.4 (repulsion)."),
    ("B", "C", 2.5, 7.5, 5.0, 2.0,
     "P-0004 prediction test: B-C pair at sep 5, T=2. Factorisation predicts K_B(C)=-5.9, K_C(B)=-10.7; a miss >20% rejects it."),
    ("A", "B", 2.0, 5.0, 5.0, 2.0,
     "P-0004 domain edge: A-B pair at sep 3 (P-0004 claims only sep 5). Tests whether the sep-5 coefficients hold at 3."),
    ("A", "C", 2.0, 5.0, 5.0, 2.0,
     "P-0004 domain edge: A-C pair at sep 3 (P-0004 claims only sep 5). Tests whether the repulsion coefficients hold at 3."),
]
for n, (s1, s2, x1, x2, y, T, purpose) in enumerate(rev_purposes, start=12):
    reqs.append(request(n, "review", purpose,
        [particle(s1, x1, y), particle(s2, x2, y)], T, cites="P-0004"))

# --- budget check
research_total = sum(cost(len(r["setup"]["particles"]), r["setup"]["duration"]) for r in reqs if r["account"] == "research")
review_total = sum(cost(len(r["setup"]["particles"]), r["setup"]["duration"]) for r in reqs if r["account"] == "review")
print(f"research {research_total:.2f} / {ALLOW_RESEARCH}, review {review_total:.2f} / {ALLOW_REVIEW}")
assert research_total <= ALLOW_RESEARCH and review_total <= ALLOW_REVIEW

out_dir = os.path.join(ROOT, "out", "requests", "2026-11-18", "r3", "lab-b")
os.makedirs(out_dir, exist_ok=True)
for r in reqs:
    num = int(r["request_id"].rsplit("/", 1)[1])
    with open(os.path.join(out_dir, f"{num:03d}.json"), "w") as f:
        json.dump(r, f, indent=2)
        f.write("\n")
print(f"wrote {len(reqs)} requests to {out_dir}")
