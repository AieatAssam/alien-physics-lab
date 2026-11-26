"""Generate lab-b review-account requests for round 1, 2026-11-26 (reviews of P-0032, P-0033, P-0034).

Every request is checked against its paper's stated domain before it is written.
"""
import json, math, os, sys

ROOT = sys.argv[1]
DATE, ROUND, LAB = "2026-11-26", "r1", "lab-b"
OUT = os.path.join(ROOT, "out", "requests", DATE, ROUND, LAB)
os.makedirs(OUT, exist_ok=True)


def pair(sp, x0, y0, x1, y1):
    return [{"species": sp, "pos": [x0, y0], "vel": [0.0, 0.0]},
            {"species": sp, "pos": [x1, y1], "vel": [0.0, 0.0]}]


def square(side, cx, cy, deg):
    h = side / 2.0
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    pts = []
    for dx, dy in [(-h, -h), (h, -h), (h, h), (-h, h)]:
        pts.append([cx + c * dx - s * dy, cy + s * dx + c * dy])
    return [{"species": "A", "pos": p, "vel": [0.0, 0.0]} for p in pts]


def dist_range(parts):
    d = [math.dist(parts[i]["pos"], parts[j]["pos"]) for i in range(len(parts)) for j in range(i + 1, len(parts))]
    return min(d), max(d)


s2_diag = 2.25 / 2 / math.sqrt(2)
reqs = [
    # P-0032: A-A pair at rest, r0 in [2.0, 2.5], T <= 0.6, max 2 particles, both >= 2 from walls.
    ("P-0032", "A-A pair, r0 2.05 horizontal, T 0.6 (in P-0032 domain; tests the no-clamp pair law at the window edge).",
     pair("A", 5 - 1.025, 5.0, 5 + 1.025, 5.0), 0.6, 0.005, (2.0, 2.5), 2),
    ("P-0032", "A-A pair, r0 2.25 diagonal, T 0.6 (in P-0032 domain; mid-window, full T of the claim).",
     pair("A", 5 - s2_diag, 5 - s2_diag, 5 + s2_diag, 5 + s2_diag), 0.6, 0.005, (2.0, 2.5), 2),
    ("P-0032", "A-A pair, r0 2.45 vertical, T 0.6 (in P-0032 domain; upper window edge, full T).",
     pair("A", 5.0, 5 - 1.225, 5.0, 5 + 1.225), 0.6, 0.005, (2.0, 2.5), 2),
    # P-0033: A-A square at rest, pairs in [5.0, 7.08], T <= 2, 4 particles.
    ("P-0033", "A-A square side 5.002, axis-aligned, centre (4.5, 5.5), T 2.0 (in P-0033 domain at its full duration).",
     square(5.002, 4.5, 5.5, 0), 2.0, 0.01, (5.0, 7.08), 4),
    ("P-0033", "A-A square side 5.002, rotated 20 degrees, centre (5.5, 4.5), T 2.0 (in P-0033 domain at its full duration).",
     square(5.002, 5.5, 4.5, 20), 2.0, 0.01, (5.0, 7.08), 4),
    # P-0034: A-A and C-C pairs at rest, r0 in [3.0, 3.5], T <= 1, max 2 particles.
    ("P-0034", "A-A pair, r0 3.25 horizontal, T 1.0 (in P-0034 domain; mid-range node check).",
     pair("A", 5 - 1.625, 5.0, 5 + 1.625, 5.0), 1.0, 0.01, (3.0, 3.5), 2),
    ("P-0034", "A-A pair, r0 3.5 horizontal, T 1.0 (in P-0034 domain; upper edge).",
     pair("A", 5 - 1.75, 5.0, 5 + 1.75, 5.0), 1.0, 0.01, (3.0, 3.5), 2),
    ("P-0034", "C-C pair, r0 3.0 horizontal, T 1.0 (in P-0034 domain; lower edge, C claim).",
     pair("C", 5 - 1.5, 5.0, 5 + 1.5, 5.0), 1.0, 0.01, (3.0, 3.5), 2),
    ("P-0034", "C-C pair, r0 3.5 horizontal, T 1.0 (in P-0034 domain; upper edge, C claim).",
     pair("C", 5 - 1.75, 5.0, 5 + 1.75, 5.0), 1.0, 0.01, (3.0, 3.5), 2),
]

for n, (paper, purpose, parts, T, dt, rr, nmax) in enumerate(reqs, start=1):
    lo, hi = dist_range(parts)
    assert len(parts) <= nmax and lo >= rr[0] and hi <= rr[1] and all(p["species"] in "ABC" for p in parts), (n, lo, hi)
    assert all(0 < p["pos"][k] < 10 for p in parts for k in range(2)), n
    req = {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{n:03d}",
        "lab": LAB,
        "account": "review",
        "purpose": purpose,
        "cites_paper": paper,
        "setup": {
            "particles": parts,
            "duration": T,
            "sample_dt": dt,
        },
        "instruments": ["tracker"],
    }
    with open(os.path.join(OUT, f"{n:03d}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    print(paper, f"{n:03d}", f"r0 {lo:.4f}..{hi:.4f}", f"T={T}", f"N={len(parts)}")
