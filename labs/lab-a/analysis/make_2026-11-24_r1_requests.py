"""Round 1, 2026-11-24 requests for lab-a (Plumbline). Written before any result exists.

Review account (cites paper):
  001-008  P-0025 (lab-b, A-B at rest, r0 4-8, T<=2): domain-edge and interpolation-node runs.
Research account:
  009-010  P-0003 (own paper, A-A r0 3-6, T<=2): upper-edge run at r0 5.99 (not a review; never review own paper).
  011-012  A-A sep 4, T 2 (horizontal, diagonal)           K(r) table point.
  013-016  A-A sep 8, T 3 (2 horizontal, 2 diagonal)        K(r) table point, replicated.
  017-018  A-A sep 6, T 2 (horizontal, diagonal)            K(r) table point.
  019-020  A-only ring of 8 (3x3 grid minus centre, spacing 3.1), at rest, T 0.5. Crowd-8 test.

Usage: python3 -I make_2026-11-24_r1_requests.py <out_dir>
"""
import json
import math
import os
import sys

DATE = "2026-11-24"
ROUND = "r1"
LAB = "lab-a"
CX, CY = 5.0, 5.0


def pair(sep, orient, a_first=True):
    """Two particles at rest centred on (5,5). Returns (pos_a, pos_b)."""
    if orient == "horizontal":
        d = (sep / 2.0, 0.0)
    elif orient == "vertical":
        d = (0.0, sep / 2.0)
    else:
        s = sep / 2.0 / math.sqrt(2.0)
        d = (s, s)
    left = (CX - d[0], CY - d[1])
    right = (CX + d[0], CY + d[1])
    return (left, right) if a_first else (right, left)


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


def ring8():
    s = 3.1
    pts = []
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            pts.append(("A", (CX + i * s, CY + j * s)))
    return pts


def main():
    out = sys.argv[1]
    d = os.path.join(out, "requests", DATE, ROUND, LAB)
    os.makedirs(d, exist_ok=True)
    reqs = []
    # Review account: P-0025 edges and interpolation nodes (A-B, A first unless noted).
    p25 = "P-0025"
    reqs.append(req(1, "review", "P-0025 edge: A-B at rest, r0 4.01 (inside lower edge), horizontal, T 2",
                    [("A", pair(4.01, "horizontal")[0]), ("B", pair(4.01, "horizontal")[1])], 2.0, p25))
    reqs.append(req(2, "review", "P-0025 edge: A-B at rest, r0 4.01, diagonal, T 2 (close approach to r ~2.2)",
                    [("A", pair(4.01, "diagonal")[0]), ("B", pair(4.01, "diagonal")[1])], 2.0, p25))
    reqs.append(req(3, "review", "P-0025 edge: A-B at rest, r0 7.99 (inside upper edge), horizontal, T 2",
                    [("A", pair(7.99, "horizontal")[0]), ("B", pair(7.99, "horizontal")[1])], 2.0, p25))
    reqs.append(req(4, "review", "P-0025 edge: A-B at rest, r0 7.99, diagonal, T 2",
                    [("A", pair(7.99, "diagonal")[0]), ("B", pair(7.99, "diagonal")[1])], 2.0, p25))
    reqs.append(req(5, "review", "P-0025 interpolation node check: A-B r0 4.5, vertical, T 2",
                    [("A", pair(4.5, "vertical")[0]), ("B", pair(4.5, "vertical")[1])], 2.0, p25))
    reqs.append(req(6, "review", "P-0025 interpolation check: A-B r0 5.5, diagonal, T 2",
                    [("A", pair(5.5, "diagonal")[0]), ("B", pair(5.5, "diagonal")[1])], 2.0, p25))
    reqs.append(req(7, "review", "P-0025 orientation swap: B on left, A on right, r0 6.5, horizontal, T 2",
                    [("A", pair(6.5, "horizontal", a_first=False)[0]), ("B", pair(6.5, "horizontal", a_first=False)[1])],
                    2.0, p25))
    reqs.append(req(8, "review", "P-0025 interpolation check: A-B r0 7.5, vertical, T 2",
                    [("A", pair(7.5, "vertical")[0]), ("B", pair(7.5, "vertical")[1])], 2.0, p25))
    # Review account: P-0003 upper edge (A-A, r0 3-6, T<=2). 5.99 sits 0.01 inside the edge.
    # P-0003 is my own paper: no review account, no cites_paper (never review own paper).
    reqs.append(req(9, "research", "P-0003 upper edge (own paper, not a review): A-A r0 5.99, horizontal, T 2",
                    [("A", pair(5.99, "horizontal")[0]), ("A", pair(5.99, "horizontal")[1])], 2.0))
    reqs.append(req(10, "research", "P-0003 upper edge (own paper, not a review): A-A r0 5.99, diagonal, T 2",
                    [("A", pair(5.99, "diagonal")[0]), ("A", pair(5.99, "diagonal")[1])], 2.0))
    # Research account: A-A K(r) table at 4, 6, 8 and the crowd test.
    reqs.append(req(11, "research", "A-A K(r) table: sep 4, horizontal, T 2",
                    [("A", pair(4.0, "horizontal")[0]), ("A", pair(4.0, "horizontal")[1])], 2.0))
    reqs.append(req(12, "research", "A-A K(r) table: sep 4, diagonal, T 2",
                    [("A", pair(4.0, "diagonal")[0]), ("A", pair(4.0, "diagonal")[1])], 2.0))
    reqs.append(req(13, "research", "A-A K(r) table: sep 8, horizontal, T 3",
                    [("A", pair(8.0, "horizontal")[0]), ("A", pair(8.0, "horizontal")[1])], 3.0))
    reqs.append(req(14, "research", "A-A K(r) table: sep 8, diagonal, T 3",
                    [("A", pair(8.0, "diagonal")[0]), ("A", pair(8.0, "diagonal")[1])], 3.0))
    reqs.append(req(15, "research", "A-A K(r) table: sep 8, horizontal, replicate, T 3",
                    [("A", pair(8.0, "horizontal")[0]), ("A", pair(8.0, "horizontal")[1])], 3.0))
    reqs.append(req(16, "research", "A-A K(r) table: sep 8, diagonal, replicate, T 3",
                    [("A", pair(8.0, "diagonal")[0]), ("A", pair(8.0, "diagonal")[1])], 3.0))
    reqs.append(req(17, "research", "A-A K(r) table: sep 6, horizontal, T 2",
                    [("A", pair(6.0, "horizontal")[0]), ("A", pair(6.0, "horizontal")[1])], 2.0))
    reqs.append(req(18, "research", "A-A K(r) table: sep 6, diagonal, T 2",
                    [("A", pair(6.0, "diagonal")[0]), ("A", pair(6.0, "diagonal")[1])], 2.0))
    ring = ring8()
    for k in (19, 20):
        reqs.append(req(k, "research",
                        "Crowd-8 test: 8 A at rest on 3x3 grid minus centre, spacing 3.1 (pair r 3.1 to 8.78), T 0.5",
                        ring, 0.5))

    total = {"review": 0.0, "research": 0.0}
    for r in reqs:
        n = len(r["setup"]["particles"])
        T = r["setup"]["duration"]
        cost = 1 + 0.02 * n * T
        total[r["account"]] += cost
        with open(os.path.join(d, r["request_id"].split("/")[-1] + ".json"), "w") as f:
            json.dump(r, f, indent=2)
            f.write("\n")
        print(r["request_id"], r["account"], "N", n, "T", T, "cost", round(cost, 3), "|", r["purpose"][:60])
    print("totals", {k: round(v, 3) for k, v in total.items()})


if __name__ == "__main__":
    main()
