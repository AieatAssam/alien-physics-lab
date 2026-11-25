"""Write round-2 (2026-11-25) requests for lab-b. Run: python3 -I make_2026-11-25_r2_requests.py <out_root>

Review account (cites P-0028, P-0030): N=8 rings (P-0028, T <= 1) and A-C pairs (P-0030, T = 1).
Research account: N=3 and N=4 at-rest additivity checks (T <= 2, all pairs inside 3..9).
"""
import json, math, os, sys

root = sys.argv[1]
DATE, RND, LAB = "2026-11-25", "r2", "lab-b"
C = (5.0, 5.0)


def ring(R, offset_deg, centre=C, n=8):
    out = []
    for k in range(n):
        a = math.radians(offset_deg + 360.0 * k / n)
        out.append([round(centre[0] + R * math.cos(a), 6), round(centre[1] + R * math.sin(a), 6)])
    return out


def part(sp, p):
    return {"species": sp, "pos": p, "vel": [0.0, 0.0]}


def req(nnn, account, purpose, parts, T, dt, cites=None):
    d = {
        "request_id": f"{DATE}/{RND}/{LAB}/{nnn:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": parts, "duration": T, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    if cites:
        d["cites_paper"] = cites
    return d


reqs = []
# --- review account, P-0028: N = 8 at rest, all pairwise distances in [3, 9], T = 1 ---
reqs.append(req(1, "review", "Review of P-0028: 8 A at rest on a ring R = 4.2 (angles 0,45,...), centre (5,5), T = 1. Pair range 3.2 to 8.4.",
                [part("A", p) for p in ring(4.2, 0.0)], 1.0, 0.01, "P-0028"))
reqs.append(req(2, "review", "Review of P-0028: 8 A at rest on a ring R = 4.45, rotated 22.5 deg, centre (5,5), T = 1. Pair range 3.4 to 8.9 (near the 9 edge).",
                [part("A", p) for p in ring(4.45, 22.5)], 1.0, 0.01, "P-0028"))
reqs.append(req(3, "review", "Review of P-0028: 8 A at rest on a ring R = 4.3, rotated 22.5 deg, centre (5.2,4.8) off-centre, T = 1. Pair range 3.3 to 8.6.",
                [part("A", p) for p in ring(4.3, 22.5, centre=(5.2, 4.8))], 1.0, 0.01, "P-0028"))
# --- review account, P-0030: A-C pair at rest, separation 2.55 / 3.0 / 3.45, T = 1 ---
reqs.append(req(4, "review", "Review of P-0030: A-C pair at rest, separation 2.55, horizontal, centre (5,5), T = 1.",
                [part("A", [3.725, 5.0]), part("C", [6.275, 5.0])], 1.0, 0.001, "P-0030"))
reqs.append(req(5, "review", "Review of P-0030: A-C pair at rest, separation 3.0, vertical, centre (5,5), T = 1 (orientation check).",
                [part("A", [5.0, 3.5]), part("C", [5.0, 6.5])], 1.0, 0.001, "P-0030"))
reqs.append(req(6, "review", "Review of P-0030: A-C pair at rest, separation 3.45, horizontal, centre (5,5), T = 1 (edge of 2.5 to 3.5).",
                [part("A", [3.275, 5.0]), part("C", [6.725, 5.0])], 1.0, 0.001, "P-0030"))
# --- research account: additivity at N = 3 and N = 4 (symmetric, no collapse into the r < 3 region) ---
s3 = 6.0
R3 = s3 / math.sqrt(3)
tri = [[5.0, 5.0 + R3], [5.0 - s3 / 2, 5.0 - R3 / 2], [5.0 + s3 / 2, 5.0 - R3 / 2]]
reqs.append(req(7, "research", "Three A at rest, equilateral triangle side 6.0, centre (5,5), T = 2. Symmetric additivity check at N = 3 with all pairs at 6 (inside the P-0027 table range).",
                [part("A", p) for p in tri], 2.0, 0.01))
sq = 2.5
sqr = [[5 - sq, 5 - sq], [5 + sq, 5 - sq], [5 + sq, 5 + sq], [5 - sq, 5 + sq]]
reqs.append(req(8, "research", "Four A at rest, square side 5.0 (diagonal 7.07), centre (5,5), T = 1.5. Symmetric additivity check at N = 4.",
                [part("A", p) for p in sqr], 1.5, 0.01))

os.makedirs(os.path.join(root, "out", "requests", DATE, RND, LAB), exist_ok=True)
for r in reqs:
    p = os.path.join(root, "out", "requests", DATE, RND, LAB, r["request_id"].split("/")[-1] + ".json")
    with open(p, "w") as f:
        json.dump(r, f, indent=2)
        f.write("\n")
    print(p)
