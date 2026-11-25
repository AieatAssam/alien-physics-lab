"""Round 1, 2026-11-25 requests for lab-a (account research). Writes out/requests/2026-11-25/r1/lab-a/NNN.json.

Purpose: measure the A-A pair force at separations 1.5 to 3, where the P-0027 table is clamped (r < 3)
and where a steeper power law (P about 3.2) predicts 30 to 150% more force. Short runs (T 0.15 to 0.3)
keep the pair far from contact, so the local acceleration is measured directly, not a trajectory average.
Also: B-B, C-C and A-B at separation 2.5 (species factorisation test), and two A-A falls from r0 = 5.
Usage: python3 -I make_2026-11-25_r1_requests.py <out_dir>
"""
import json, math, os, sys

OUT = sys.argv[1]
DAY, RND, LAB = "2026-11-25", 1, "lab-a"
D = os.path.join(OUT, "requests", DAY, f"r{RND}", LAB)
os.makedirs(D, exist_ok=True)


def pair(sp1, sp2, r0, orient, cx=5.0, cy=5.0):
    if orient == "h":
        p1, p2 = (cx - r0 / 2, cy), (cx + r0 / 2, cy)
    else:
        o = r0 / 2 / math.sqrt(2)
        p1, p2 = (cx - o, cy - o), (cx + o, cy + o)
    return [{"species": sp1, "pos": [p1[0], p1[1]], "vel": [0.0, 0.0]},
            {"species": sp2, "pos": [p2[0], p2[1]], "vel": [0.0, 0.0]}]


runs = [
    ("A-A pair at rest, separation 2.0 horizontal, T 0.3: local A-A force at r = 2 (table clamped below 3).",
     pair("A", "A", 2.0, "h"), 0.3, 0.005),
    ("A-A separation 2.0 diagonal, replicate of 001 in the other orientation.",
     pair("A", "A", 2.0, "d"), 0.3, 0.005),
    ("A-A separation 2.5 horizontal, T 0.3: local force at r = 2.5 (table clamped below 3).",
     pair("A", "A", 2.5, "h"), 0.3, 0.005),
    ("A-A separation 2.5 diagonal, replicate of 003.",
     pair("A", "A", 2.5, "d"), 0.3, 0.005),
    ("A-A separation 3.0 horizontal, T 0.3: boundary check against the table value 17.68 at r = 3.",
     pair("A", "A", 3.0, "h"), 0.3, 0.005),
    ("A-A separation 3.0 diagonal, replicate of 005.",
     pair("A", "A", 3.0, "d"), 0.3, 0.005),
    ("A-A separation 1.5 horizontal, T 0.15: closest local point for the close-range law.",
     pair("A", "A", 1.5, "h"), 0.15, 0.0025),
    ("A-A separation 1.5 diagonal, replicate of 007.",
     pair("A", "A", 1.5, "d"), 0.15, 0.0025),
    ("B-B separation 2.5 horizontal, T 0.3: species factorisation (B-B against A-A at the same separation).",
     pair("B", "B", 2.5, "h"), 0.3, 0.005),
    ("C-C separation 2.5 horizontal, T 0.3: species factorisation (C-C against A-A at the same separation).",
     pair("C", "C", 2.5, "h"), 0.3, 0.005),
    ("A-B separation 2.5 horizontal, T 0.3: A-B against A-A at the same separation.",
     pair("A", "B", 2.5, "h"), 0.3, 0.005),
    ("A-A radial fall from r0 = 5 horizontal at rest, T 4: pre-contact K(r) over 5 to about 2 (trajectory).",
     pair("A", "A", 5.0, "h"), 4.0, 0.02),
    ("A-A radial fall from r0 = 5 diagonal, replicate of 012.",
     pair("A", "A", 5.0, "d"), 4.0, 0.02),
]

written = []
for i, (purpose, particles, T, dt) in enumerate(runs, start=1):
    n = int(round(T / dt))
    assert n <= 2000, n
    req = {
        "request_id": f"{DAY}/r{RND}/{LAB}/{i:03d}",
        "lab": LAB,
        "account": "research",
        "purpose": purpose,
        "setup": {"particles": particles, "duration": T, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    with open(os.path.join(D, f"{i:03d}.json"), "w") as f:
        json.dump(req, f, indent=2)
    cost = 1 + 0.02 * len(particles) * T
    written.append((i, round(cost, 3)))
print("wrote", len(written), "requests; total cost", round(sum(c for _, c in written), 3))
print(written)
