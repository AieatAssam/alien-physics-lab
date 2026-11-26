"""Generate lab-b requests for round 3, 2026-11-26.

Review account (cites P-0035, edge runs of the A-A pair window [2.0, 2.75], T <= 0.6):
  001: r0 2.01 horizontal (lower window edge, margin 0.01 inside the boundary), T 0.6
  002: r0 2.74 vertical (upper window edge, margin 0.01 inside the boundary), T 0.6

Research account (H21, scalene A-triangle, pre-registered in the round-1 grant proposal;
the grant was won by lab-a, so this runs on research credits):
  003: three A particles at rest, pairwise distances 5.6, 5.9, 6.2 (all in P-0031 domain [5.0, 7.1]), T 2.0

Every request is checked against its stated domain before it is written.
"""
import json, math, os, sys

ROOT = sys.argv[1]
DATE, ROUND, LAB = "2026-11-26", "r3", "lab-b"
OUT = os.path.join(ROOT, "out", "requests", DATE, ROUND, LAB)
os.makedirs(OUT, exist_ok=True)


def pair(sp, x0, y0, x1, y1):
    return [{"species": sp, "pos": [x0, y0], "vel": [0.0, 0.0]},
            {"species": sp, "pos": [x1, y1], "vel": [0.0, 0.0]}]


def dist_range(parts):
    d = [math.dist(parts[i]["pos"], parts[j]["pos"]) for i in range(len(parts)) for j in range(i + 1, len(parts))]
    return min(d), max(d)


# P-0035 window [2.0, 2.75]: both particles at least 2.0 from every wall.
e_lo = pair("A", 5 - 1.005, 5.0, 5 + 1.005, 5.0)           # r0 2.01
e_hi = pair("A", 5.0, 5 - 1.37, 5.0, 5 + 1.37)             # r0 2.74

# H21 scalene triangle: A = (2.0, 2.5), B = A + (5.6, 0), C with |AC| = 5.9, |BC| = 6.2.
ax, ay = 2.0, 2.5
bx, by = ax + 5.6, ay
cx = ax + (5.6 ** 2 + 5.9 ** 2 - 6.2 ** 2) / (2 * 5.6)
cy = ay + math.sqrt(5.9 ** 2 - (cx - ax) ** 2)
scalene = [{"species": "A", "pos": [ax, ay], "vel": [0.0, 0.0]},
           {"species": "A", "pos": [bx, by], "vel": [0.0, 0.0]},
           {"species": "A", "pos": [round(cx, 6), round(cy, 6)], "vel": [0.0, 0.0]}]

reqs = [
    ("review", "P-0035", "A-A pair, r0 2.01 horizontal, T 0.6 (P-0035 window edge, lower end; no-clamp law at 2.01).",
     e_lo, 0.6, 0.005, (2.0, 2.75), 2),
    ("review", "P-0035", "A-A pair, r0 2.74 vertical, T 0.6 (P-0035 window edge, upper end; tests 2.75 end from below).",
     e_hi, 0.6, 0.005, (2.0, 2.75), 2),
    ("research", None, "H21: scalene A-triangle at rest, sides 5.6, 5.9, 6.2 (P-0031 domain), T 2.0; pre-registered falsifier judged RMSE/L > 0.021.",
     scalene, 2.0, 0.01, (5.0, 7.1), 3),
]

for n, (account, paper, purpose, parts, T, dt, rr, nmax) in enumerate(reqs, start=1):
    lo, hi = dist_range(parts)
    assert len(parts) <= nmax and rr[0] <= lo and hi <= rr[1], (n, lo, hi)
    assert all(p["species"] == "A" for p in parts), n
    assert all(0 < p["pos"][k] < 10 for p in parts for k in range(2)), n
    if account == "review":
        assert all(2.0 <= p["pos"][k] <= 8.0 for p in parts for k in range(2)), n
    req = {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{n:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": parts, "duration": T, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    if paper:
        req["cites_paper"] = paper
    with open(os.path.join(OUT, f"{n:03d}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    cost = 1 + 0.02 * len(parts) * T
    print(account, paper, f"{n:03d}", f"r0 {lo:.4f}..{hi:.4f}", f"T={T}", f"N={len(parts)}", f"cost~{cost:.3f}")
