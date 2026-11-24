"""Round 2, 2026-11-24 requests for lab-a (Plumbline). Written before any result exists.

Research account (own K(r) table, off-node interpolation test and crowd-8 ring):
  001  A-A sep 3.5, horizontal, T 1.0          prediction K(3.5) = 17.692 (linear between nodes 3 and 4)
  002  A-A sep 4.5, diagonal, T 1.5            prediction K(4.5) = 17.768
  003  A-A sep 5.5, diagonal, T 2.0            prediction K(5.5) = 17.226
  004  A-A sep 6.5, horizontal, T 2.0          prediction K(6.5) = 15.869
  005  A-A sep 6.5, diagonal, T 2.0 (replicate) prediction K(6.5) = 15.869
  006  A-A sep 7.5, diagonal, T 3.0            prediction K(7.5) = 14.277
  007  A-A sep 8.5, horizontal, T 3.0          prediction K(8.5) = 12.528
  008  Crowd-8 ring (3x3 grid minus centre, spacing 3.1), at rest, T 1.0
  009  Crowd-8 ring replicate, T 1.0
Review account (cites P-0026, lab-keystone, A crowd of 16 at rest, T <= 0.3). Edge-oriented:
  010  16 A, 4x4 grid spacing 1.52 (minimum pair 1.52, just above the 1.5 lower edge), T 0.3
  011  16 A, ring of radius 4.9 about (5,5) (adjacent chord 1.92, largest pair 9.8), T 0.3
  012  16 A, irregular layout, seeded, minimum pair >= 1.6, largest pair <= 10.2, T 0.3

Usage: python3 -I make_2026-11-24_r2_requests.py <out_dir>
"""
import json
import math
import os
import random
import sys

DATE = "2026-11-24"
ROUND = "r2"
LAB = "lab-a"
CX, CY = 5.0, 5.0


def pair(sep, orient):
    if orient == "horizontal":
        d = (sep / 2.0, 0.0)
    elif orient == "vertical":
        d = (0.0, sep / 2.0)
    else:
        s = sep / 2.0 / math.sqrt(2.0)
        d = (s, s)
    return (CX - d[0], CY - d[1]), (CX + d[0], CY + d[1])


def dt_for(T):
    return round(T / 1990.0, 10)


def req(idx, account, purpose, parts, T, cites=None):
    r = {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{idx:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {
            "particles": [
                {"species": sp, "pos": [round(p[0], 6), round(p[1], 6)], "vel": [0.0, 0.0]}
                for sp, p in parts
            ],
            "duration": T,
            "sample_dt": dt_for(T),
        },
        "instruments": ["tracker"],
    }
    if cites:
        r["cites_paper"] = cites
    return r


def aa(sep, orient):
    a, b = pair(sep, orient)
    return [("A", a), ("A", b)]


def ring8():
    s = 3.1
    return [("A", (CX + i * s, CY + j * s)) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)]


def grid16():
    s = 1.52
    return [("A", (CX + (i - 1.5) * s, CY + (j - 1.5) * s)) for i in range(4) for j in range(4)]


def ring16():
    R = 4.9
    return [("A", (CX + R * math.cos(2 * math.pi * k / 16), CY + R * math.sin(2 * math.pi * k / 16)))
            for k in range(16)]


def irregular16():
    rng = random.Random(20261124)
    pts = []
    while len(pts) < 16:
        c = (rng.uniform(1.5, 8.5), rng.uniform(1.5, 8.5))
        if all(math.dist(c, p) >= 1.6 for p in pts):
            cand = pts + [c]
            if all(math.dist(a, b) <= 10.2 for i, a in enumerate(cand) for b in cand[i + 1:]):
                pts = cand
    return [("A", p) for p in pts]


def main():
    out = sys.argv[1]
    d = os.path.join(out, "requests", DATE, ROUND, LAB)
    os.makedirs(d, exist_ok=True)
    reqs = [
        req(1, "research", "A-A K(r) off-node interpolation: sep 3.5 horizontal, T 1.0", aa(3.5, "horizontal"), 1.0),
        req(2, "research", "A-A K(r) off-node interpolation: sep 4.5 diagonal, T 1.5", aa(4.5, "diagonal"), 1.5),
        req(3, "research", "A-A K(r) off-node interpolation: sep 5.5 diagonal, T 2.0", aa(5.5, "diagonal"), 2.0),
        req(4, "research", "A-A K(r) off-node interpolation: sep 6.5 horizontal, T 2.0", aa(6.5, "horizontal"), 2.0),
        req(5, "research", "A-A K(r) off-node interpolation: sep 6.5 diagonal, T 2.0 (replicate)", aa(6.5, "diagonal"), 2.0),
        req(6, "research", "A-A K(r) off-node interpolation: sep 7.5 diagonal, T 3.0", aa(7.5, "diagonal"), 3.0),
        req(7, "research", "A-A K(r) off-node interpolation: sep 8.5 horizontal, T 3.0", aa(8.5, "horizontal"), 3.0),
        req(8, "research", "Crowd-8 ring at T 1.0 (table-K vs constant-K discriminating; min pair ~2.3)", ring8(), 1.0),
        req(9, "research", "Crowd-8 ring at T 1.0, replicate", ring8(), 1.0),
        req(10, "review", "P-0026 edge: 16 A on a 4x4 grid, spacing 1.52 (minimum pair at the 1.5 lower edge), T 0.3",
            grid16(), 0.3, "P-0026"),
        req(11, "review", "P-0026 edge: 16 A on a ring of radius 4.9 (adjacent chord 1.92, largest pair 9.8), T 0.3",
            ring16(), 0.3, "P-0026"),
        req(12, "review", "P-0026: 16 A irregular seeded layout, minimum pair >= 1.6, largest pair <= 10.2, T 0.3",
            irregular16(), 0.3, "P-0026"),
    ]
    totals = {"review": 0.0, "research": 0.0}
    for r in reqs:
        n = len(r["setup"]["particles"])
        T = r["setup"]["duration"]
        cost = 1 + 0.02 * n * T
        totals[r["account"]] += cost
        with open(os.path.join(d, r["request_id"].split("/")[-1] + ".json"), "w") as f:
            json.dump(r, f, indent=2)
            f.write("\n")
        print(r["request_id"], r["account"], "N", n, "T", T, "cost", round(cost, 3), "|", r["purpose"][:60])
    print("totals", {k: round(v, 3) for k, v in totals.items()})


if __name__ == "__main__":
    main()
