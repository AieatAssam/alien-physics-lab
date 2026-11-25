"""Writes round-1 (2026-11-25) requests for lab-vernier.

Research (account research, budget 40): 001-005 A-C pairs at rest, T = 2 (r = 2.75, 3.25 and a diagonal 3.0,
out-of-sample test of the A-C claim); 006-011 A-A at r = 2.5, 3.0, 3.5, T = 1; 012-017 C-C at the same
separations, T = 1; 018-019 A-C diagonal at r = 2.5 and 3.5, T = 2 (isotropy).
Review (account review, budget 15, cites P-0028): 101-102 3x3-minus-centre grid at spacing 3.02 (unrotated and
rotated 30 deg); 103 ring of 8 at radius 3.95. All P-0028 designs have 8 particles and every pair in [3, 9].
Usage: python3 -I make_requests_2026-11-25.py
"""
import json
import math
import os

DATE = "2026-11-25"
ROUND = "r1"
OUT = "/home/runner/work/alien-physics-lab/alien-physics-lab/out/requests/%s/%s/lab-vernier" % (DATE, ROUND)
os.makedirs(OUT, exist_ok=True)


def pair(sp1, sp2, r, T, orient="H"):
    if orient == "H":
        p1, p2 = [5.0 - r / 2, 5.0], [5.0 + r / 2, 5.0]
    elif orient == "V":
        p1, p2 = [5.0, 5.0 - r / 2], [5.0, 5.0 + r / 2]
    else:  # diagonal along (0.6, 0.8)
        p1, p2 = [5.0 - 0.6 * r / 2, 5.0 - 0.8 * r / 2], [5.0 + 0.6 * r / 2, 5.0 + 0.8 * r / 2]
    return {"particles": [{"species": sp1, "pos": p1, "vel": [0.0, 0.0]},
                          {"species": sp2, "pos": p2, "vel": [0.0, 0.0]}],
            "duration": T, "sample_dt": T / 2000.0}


def grid_minus_centre(s, rot_deg=0.0):
    c, sn = math.cos(math.radians(rot_deg)), math.sin(math.radians(rot_deg))
    pts = []
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if (i, j) == (0, 0):
                continue
            dx, dy = i * s, j * s
            pts.append([5.0 + dx * c - dy * sn, 5.0 + dx * sn + dy * c])
    return pts


def ring(R, n=8):
    return [[5.0 + R * math.cos(2 * math.pi * k / n), 5.0 + R * math.sin(2 * math.pi * k / n)] for k in range(n)]


def a_setup(pts, T):
    return {"particles": [{"species": "A", "pos": [round(x, 6), round(y, 6)], "vel": [0.0, 0.0]} for x, y in pts],
            "duration": T, "sample_dt": T / 2000.0}


research = [
    ("A-C r=2.75 horizontal, T=2 (out-of-sample point for the A-C separation table)", pair("A", "C", 2.75, 2.0, "H")),
    ("A-C r=2.75 vertical, T=2", pair("A", "C", 2.75, 2.0, "V")),
    ("A-C r=3.25 horizontal, T=2 (out-of-sample point)", pair("A", "C", 3.25, 2.0, "H")),
    ("A-C r=3.25 vertical, T=2", pair("A", "C", 3.25, 2.0, "V")),
    ("A-C r=3.0 diagonal (0.6,0.8), T=2 (isotropy at the mid-point)", pair("A", "C", 3.0, 2.0, "D")),
    ("A-A r=2.5 horizontal, T=1 (superseder groundwork, A-A row)", pair("A", "A", 2.5, 1.0, "H")),
    ("A-A r=2.5 vertical, T=1", pair("A", "A", 2.5, 1.0, "V")),
    ("A-A r=3.0 horizontal, T=1", pair("A", "A", 3.0, 1.0, "H")),
    ("A-A r=3.0 vertical, T=1", pair("A", "A", 3.0, 1.0, "V")),
    ("A-A r=3.5 horizontal, T=1", pair("A", "A", 3.5, 1.0, "H")),
    ("A-A r=3.5 vertical, T=1", pair("A", "A", 3.5, 1.0, "V")),
    ("C-C r=2.5 horizontal, T=1 (superseder groundwork, C-C row)", pair("C", "C", 2.5, 1.0, "H")),
    ("C-C r=2.5 vertical, T=1", pair("C", "C", 2.5, 1.0, "V")),
    ("C-C r=3.0 horizontal, T=1", pair("C", "C", 3.0, 1.0, "H")),
    ("C-C r=3.0 vertical, T=1", pair("C", "C", 3.0, 1.0, "V")),
    ("C-C r=3.5 horizontal, T=1", pair("C", "C", 3.5, 1.0, "H")),
    ("C-C r=3.5 vertical, T=1", pair("C", "C", 3.5, 1.0, "V")),
    ("A-C r=2.5 diagonal (0.6,0.8), T=2 (isotropy at the inner edge)", pair("A", "C", 2.5, 2.0, "D")),
    ("A-C r=3.5 diagonal (0.6,0.8), T=2 (isotropy at the outer edge)", pair("A", "C", 3.5, 2.0, "D")),
]

review = [
    ("P-0028 review, edge of domain: A x8, 3x3 minus centre, spacing 3.02 (min pair 3.02, max 8.54), at rest, T=1",
     a_setup(grid_minus_centre(3.02), 1.0)),
    ("P-0028 review, same grid rotated 30 deg (tests isotropy of the pair sum at N=8)",
     a_setup(grid_minus_centre(3.02, 30.0), 1.0)),
    ("P-0028 review, edge of domain: ring of 8 at radius 3.95 (min pair 3.02, max 7.90), at rest, T=1",
     a_setup(ring(3.95), 1.0)),
]


def write(idx, account, purpose, setup, cites=None):
    rid = "%s/%s/lab-vernier/%03d" % (DATE, ROUND, idx)
    d = {"request_id": rid, "lab": "lab-vernier", "account": account, "purpose": purpose[:500],
         "setup": setup, "instruments": ["tracker"]}
    if cites:
        d["cites_paper"] = cites
    with open(os.path.join(OUT, "%03d.json" % idx), "w") as f:
        json.dump(d, f, indent=1)
        f.write("\n")
    return d


if __name__ == "__main__":
    for i, (p, s) in enumerate(research, start=1):
        write(i, "research", p, s)
    for i, (p, s) in enumerate(review, start=101):
        write(i, "review", p, s, cites="P-0028")
    print("wrote", len(research), "research and", len(review), "review requests to", OUT)
