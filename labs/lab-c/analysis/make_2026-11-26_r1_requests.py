#!/usr/bin/env python3
"""Round 1, 2026-11-26 requests for lab-c (Nullius). Writes out/requests/2026-11-26/r1/lab-c/NNN.json.

Review account (15 credits, each cites the paper it reviews):
  001-003  P-0031 (lab-b, A 3-4 bodies, pairwise [5.0, 7.1], T <= 2):
           asymmetric triangles (sides 7.05/5.89/5.08 and 7.09/5.0/6.0) and an A square of side 5.
  004-006  P-0033 (lab-keystone, A square-type 4 bodies, pairwise [5.0, 7.08], T <= 2): three squares of side 5
           (translated, rotated, corner-placed).
  007-011, 017  P-0034 (lab-vernier, A-A and C-C pairs, r0 in [3.0, 3.5], T <= 1): r0 3.0, 3.25, 3.5 for A; 3.0, 3.25, 3.5 for C.
Research account (40 credits, round-1 own science):
  012-016  pair near-contact and mixed-species checks, see analysis notes.

Run: python3 -I make_2026-11-26_r1_requests.py REPO_ROOT
"""
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
DATE, ROUND, LAB = "2026-11-26", "r1", "lab-c"
OUT = REPO / "out" / "requests" / DATE / ROUND / LAB
OUT.mkdir(parents=True, exist_ok=True)


def part(sp, x, y):
    return {"species": sp, "pos": [float(x), float(y)], "vel": [0.0, 0.0]}


def dist(a, b):
    return math.dist(a, b)


def tri_asym_1():
    # sides AB 7.048, AC 5.891, BC 5.079 (search result, all within [5.0, 7.1])
    return [(2.186, 6.236), (7.984, 2.23), (7.978, 7.309)]


def tri_asym_2():
    # sides AB 7.09, AC 5.0, BC 6.0: A=(2,2), B=(9.09,2), C on the upper side with |AC|=5, |BC|=6
    A, B = (2.0, 2.0), (9.09, 2.0)
    d = B[0] - A[0]  # 7.09
    x = A[0] + (5.0 ** 2 - 6.0 ** 2 + d ** 2) / (2 * d)  # foot along AB from |AC|=5, |BC|=6
    y = A[1] + math.sqrt(5.0 ** 2 - (x - A[0]) ** 2)
    return [A, B, (x, y)]


def square(cx, cy, side, rot_deg=0.0):
    h = side / 2.0
    th = math.radians(rot_deg)
    corners = [(-h, -h), (h, -h), (h, h), (-h, h)]
    return [(cx + x * math.cos(th) - y * math.sin(th), cy + x * math.sin(th) + y * math.cos(th))
            for x, y in corners]


def pair_axis(r0, cx=5.0, cy=5.0, orient="h"):
    h = r0 / 2.0
    if orient == "h":
        return [(cx - h, cy), (cx + h, cy)]
    if orient == "v":
        return [(cx, cy - h), (cx, cy + h)]
    d = h / math.sqrt(2.0)
    return [(cx - d, cy - d), (cx + d, cy + d)]


REQS = []


def add(idx, account, purpose, species_pos, duration, sample_dt, cites=None):
    REQS.append((idx, account, purpose, species_pos, duration, sample_dt, cites))


# --- review runs for P-0031 (Icarus, lab-b)
t1 = tri_asym_1()
t2 = tri_asym_2()
sq1 = square(3.5, 3.5, 5.0)
add(1, "review", "Review of P-0031 (lab-b): asymmetric A triangle, sides 7.05/5.89/5.08 (all pairs in [5.0, 7.1]), at rest, T = 2.",
    [("A", *t1[0]), ("A", *t1[1]), ("A", *t1[2])], 2.0, 0.01, "P-0031")
add(2, "review", "Review of P-0031 (lab-b): second asymmetric A triangle, sides 7.09/5.00/6.00 (pairs at both range edges), at rest, T = 2.",
    [("A", *t2[0]), ("A", *t2[1]), ("A", *t2[2])], 2.0, 0.01, "P-0031")
add(3, "review", "Review of P-0031 (lab-b): A square of side 5.0 at the lower-left (corners 1 to 6), at rest, T = 2 (N = 4 case).",
    [("A", *sq1[0]), ("A", *sq1[1]), ("A", *sq1[2]), ("A", *sq1[3])], 2.0, 0.01, "P-0031")

# --- review runs for P-0033 (Keystone): squares of side 5 (the only N = 4 shape the domain allows)
add(4, "review", "Review of P-0033 (lab-keystone): A square of side 5.0 translated to corners 2.5 to 7.5, at rest, T = 2.",
    [("A", *p) for p in square(5.0, 5.0, 5.0)], 2.0, 0.01, "P-0033")
add(5, "review", "Review of P-0033 (lab-keystone): A square of side 5.0 rotated 30 degrees about (5, 5), at rest, T = 2.",
    [("A", *p) for p in square(5.0, 5.0, 5.0, rot_deg=30.0)], 2.0, 0.01, "P-0033")
add(6, "review", "Review of P-0033 (lab-keystone): A square of side 5.0 placed near the lower-left wall (corners 0.5 to 5.5), at rest, T = 2.",
    [("A", *p) for p in square(3.0, 3.0, 5.0)], 2.0, 0.01, "P-0033")

# --- review runs for P-0034 (Vernier): A-A and C-C pairs, r0 in [3.0, 3.5]
add(7, "review", "Review of P-0034 (lab-vernier): A-A pair at rest, r0 = 3.0 horizontal, T = 1.",
    [("A", *p) for p in pair_axis(3.0, orient="h")], 1.0, 0.01, "P-0034")
add(8, "review", "Review of P-0034 (lab-vernier): A-A pair at rest, r0 = 3.5 diagonal, T = 1.",
    [("A", *p) for p in pair_axis(3.5, orient="d")], 1.0, 0.01, "P-0034")
add(9, "review", "Review of P-0034 (lab-vernier): C-C pair at rest, r0 = 3.0 vertical, T = 1.",
    [("C", *p) for p in pair_axis(3.0, orient="v")], 1.0, 0.01, "P-0034")
add(10, "review", "Review of P-0034 (lab-vernier): C-C pair at rest, r0 = 3.5 horizontal, T = 1.",
    [("C", *p) for p in pair_axis(3.5, orient="h")], 1.0, 0.01, "P-0034")
add(11, "review", "Review of P-0034 (lab-vernier): A-A pair at rest, r0 = 3.25 horizontal (interior of [3.0, 3.5]), T = 1.",
    [("A", *p) for p in pair_axis(3.25, orient="h")], 1.0, 0.01, "P-0034")

add(17, "review", "Review of P-0034 (lab-vernier): C-C pair at rest, r0 = 3.25 vertical (interior of [3.0, 3.5]), T = 1. Third C-C pass for claim c2.",
    [("C", *p) for p in pair_axis(3.25, orient="v")], 1.0, 0.01, "P-0034")

# --- research runs (own science, round 1): near-contact behaviour and mixed species
add(12, "research", "Research (round 1): A-A pair at rest, r0 = 2.0 horizontal, T = 1.5, through the near-contact region. Tests whether the P-0026 pair law's contact behaviour (pairs rebound) is the same at r0 2.0 as at 1.75 (2026-11-25/r3 001, 005).",
    [("A", *p) for p in pair_axis(2.0, orient="h")], 1.5, 0.005)
add(13, "research", "Research (round 1): A-A pair at rest, r0 = 2.25 horizontal, T = 1.5. Places the contact-time boundary between 2.0 and 2.5.",
    [("A", *p) for p in pair_axis(2.25, orient="h")], 1.5, 0.005)
add(14, "research", "Research (round 1): A-A pair at rest, r0 = 2.75 diagonal, T = 0.6. Replicates the 2.75 edge of the P-0026 pair law with a second orientation (2026-11-25/r3 004 was horizontal).",
    [("A", *p) for p in pair_axis(2.75, orient="d")], 0.6, 0.001)
add(15, "research", "Research (round 1): mixed A-C pair at rest, r0 = 3.0 horizontal, T = 1. First mixed-species pair in lab-c's own data, to test whether the A-A and C-C pair laws (P-0034) say anything about A-C.",
    [("A", 3.5, 5.0), ("C", 6.5, 5.0)], 1.0, 0.01)
add(16, "research", "Research (round 1): C-C pair at rest, r0 = 2.5 horizontal, T = 1.5, near-contact check for species C (P-0034 stops at r0 3.0).",
    [("C", *p) for p in pair_axis(2.5, orient="h")], 1.5, 0.005)

total = {"review": 0.0, "research": 0.0}
for idx, account, purpose, sp_pos, duration, sample_dt, cites in REQS:
    parts = [part(sp, x, y) for sp, x, y in sp_pos]
    doc = {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{idx:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": parts, "duration": duration, "sample_dt": sample_dt},
        "instruments": ["tracker"],
    }
    if cites:
        doc["cites_paper"] = cites
    assert len(purpose) <= 500, idx
    n = len(parts)
    if cites in ("P-0031", "P-0033", "P-0034") and account == "review":
        # domain check against the claim's stated r_range (every initial pairwise distance)
        rng = {"P-0031": (5.0, 7.1), "P-0033": (5.0, 7.08), "P-0034": (3.0, 3.5)}[cites]
        ds = [math.dist(a["pos"], b["pos"]) for i, a in enumerate(parts) for b in parts[i + 1:]]
        print("   pairwise", [round(d, 4) for d in ds], "range", rng)
        assert all(rng[0] - 1e-9 <= d <= rng[1] + 1e-9 for d in ds), idx
        assert all(0.0 <= c <= 10.0 for p in parts for c in p["pos"]), idx
    assert int(round(duration / sample_dt)) <= 2000
    cost = 1 + 0.02 * n * duration
    total[account] += cost
    (OUT / f"{idx:03d}.json").write_text(json.dumps(doc, indent=2) + "\n")
    print(f"{idx:03d} {account:8s} N={n} T={duration} dt={sample_dt} cost={cost:.2f} cites={cites}")

print({k: round(v, 2) for k, v in total.items()})
