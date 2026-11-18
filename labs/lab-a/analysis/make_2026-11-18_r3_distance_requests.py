"""lab-a round 3 (2026-11-18): distance-law test of the sep-5 pair coefficients.

Writes out/requests/2026-11-18/r3/lab-a/001-007.json (research account).
Predictions are pre-registered in each purpose string. They assume the sep-5 pair
coefficients measured in round 1-2 (run means) and the A-A far-field ratio
K_AA(7)/K_AA(5) = 15.48/18.0 = 0.86 (r2/006-007 vs P-0003).
Usage: python3 -I make_2026-11-18_r3_distance_requests.py <repo_root>
"""
import json, os, sys

ROOT = sys.argv[1]
DAY, RND = "2026-11-18", "r3"
OUT = os.path.join(ROOT, "out/requests", DAY, RND, "lab-a")
os.makedirs(OUT, exist_ok=True)


def pair(sp1, sp2, sep, y=5.0):
    x1 = 5.0 - sep / 2.0
    x2 = 5.0 + sep / 2.0
    return [
        {"species": sp1, "pos": [x1, y], "vel": [0.0, 0.0]},
        {"species": sp2, "pos": [x2, y], "vel": [0.0, 0.0]},
    ]


REQS = [
    ("C", "C", 7.0, 4.0, 0.04,
     "Distance-law test, C-C at rest, separation 7 along x (y=5), T=4. If C-C follows the A-A ratio "
     "K(7)/K(5)=0.86 (P-0003, r2/006-007), predicts K_C(C) about 10.6 (sep-5 mean 12.36). Repeat is 002."),
    ("C", "C", 7.0, 4.0, 0.04,
     "Repeat of 001: C-C at rest, separation 7 along x (y=5), T=4. Predicts K_C(C) about 10.6 if the A-A distance law holds for C-C."),
    ("C", "C", 9.0, 4.0, 0.04,
     "Distance-law test, C-C at rest, separation 9 along x (y=5), T=4. A-A ratio K(9)/K(5)=0.65 (r1/008-009) predicts K_C(C) about 8.0."),
    ("B", "C", 7.0, 4.0, 0.04,
     "Distance-law test, B-C at rest, separation 7 along x (y=5), T=4. Same-law prediction from sep-5 means: K_B(C) about -5.2, K_C(B) about -9.1. Repeat is 007."),
    ("A", "C", 7.0, 4.0, 0.04,
     "Distance-law test, A-C at rest, separation 7 along x (y=5), T=4. Same-law prediction from sep-5 means: K_A(C) about -7.5, K_C(A) about -18.3."),
    ("B", "B", 7.0, 4.0, 0.04,
     "Distance-law test, B-B at rest, separation 7 along x (y=5), T=4. Same-law prediction: K_B(B) about 5.3 (sep-5 mean 6.12)."),
    ("B", "C", 7.0, 4.0, 0.04,
     "Repeat of 004: B-C at rest, separation 7 along x (y=5), T=4. Predicts K_B(C) about -5.2 and K_C(B) about -9.1 if the same distance law holds."),
]

for i, (s1, s2, sep, T, dt, purpose) in enumerate(REQS, start=1):
    rid = f"{DAY}/{RND}/lab-a/{i:03d}"
    req = {
        "request_id": rid,
        "lab": "lab-a",
        "account": "research",
        "purpose": purpose,
        "setup": {
            "particles": pair(s1, s2, sep),
            "duration": T,
            "sample_dt": dt,
        },
        "instruments": ["tracker", "census"],
    }
    with open(os.path.join(OUT, f"{i:03d}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    cost = 1 + 0.02 * 2 * T
    print(f"{rid} {s1}-{s2} sep={sep} T={T} cost={cost:.2f}")
print("total cost", round(len(REQS) * (1 + 0.02 * 2 * 4.0), 2))
