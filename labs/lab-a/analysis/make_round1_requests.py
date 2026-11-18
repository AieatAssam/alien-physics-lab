"""Round 1 (2026-11-18) requests for lab-a. Writes out/requests/2026-11-18/r1/lab-a/NNN.json.
Research (001-013, expected 14.54 credits):
  001-002  A-B at rest, separation 5, T=2          (species dependence of pair force)
  003      B-B at rest, separation 5, T=2
  004      C-C at rest, separation 5, T=2
  005      A-C at rest, separation 5, T=2
  006-007  A-A at rest, separation 8, T=4           (far field; power law vs screened form)
  008-009  A-A at rest, separation 9, T=4           (far field, repeat)
  010      A-A at rest, separation 4 along 45 deg, T=2  (isotropy)
  011      A-A at rest, separation 4 along y, T=2       (isotropy)
  012      A-A at rest, separation 2, T=0.5             (near-field low end of domain)
  013      16 particles species A, T=1                  (cost constant at N=16)
Review (014-016, expected 6.20 credits, cites P-0002): lone species-C edge tests.
"""
import json, os, math

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "requests", "2026-11-18", "r1", "lab-a")
OUT = os.path.normpath(OUT)
os.makedirs(OUT, exist_ok=True)

def P(sp, x, y, vx=0.0, vy=0.0):
    return {"species": sp, "pos": [x, y], "vel": [vx, vy]}

def req(n, purpose, particles, duration, dt, account="research", cites=None, instruments=("tracker", "census")):
    d = {
        "request_id": f"2026-11-18/r1/lab-a/{n:03d}",
        "lab": "lab-a",
        "account": account,
        "purpose": purpose,
        "setup": {"particles": particles, "duration": duration, "sample_dt": dt},
        "instruments": list(instruments),
    }
    if cites:
        d["cites_paper"] = cites
    return n, d

off = 4.0 / math.sqrt(2)  # each coordinate offset for separation 4.0 along the diagonal
grid = [1.5, 3.5, 5.5, 7.5]

reqs = [
    req(1, "A-B pair at rest, separation 5 along x (y=5), T=2. Species dependence of the pair force; repeat 002 to check reproducibility. Census watches for species change under interaction.",
        [P("A", 2.0, 5.0), P("B", 7.0, 5.0)], 2.0, 0.02),
    req(2, "Repeat of 001 (A-B, separation 5, T=2).",
        [P("A", 2.0, 5.0), P("B", 7.0, 5.0)], 2.0, 0.02),
    req(3, "B-B pair at rest, separation 5, T=2. Same geometry as r3/005-006 (A-A). Tests whether B-B attraction matches A-A.",
        [P("B", 2.0, 5.0), P("B", 7.0, 5.0)], 2.0, 0.02),
    req(4, "C-C pair at rest, separation 5, T=2. Same geometry as r3/005-006 (A-A).",
        [P("C", 2.0, 5.0), P("C", 7.0, 5.0)], 2.0, 0.02),
    req(5, "A-C pair at rest, separation 5, T=2. Mixed-species pair; compares the A-C force with the A-A force at the same separation.",
        [P("A", 2.0, 5.0), P("C", 7.0, 5.0)], 2.0, 0.02),
    req(6, "A-A pair at rest, separation 8 along x (y=5), T=4. Far-field test: power law K/r^2.5 predicts about 0.084 per particle at r=8.5; screened inverse-square (lambda 8) predicts about 15% less.",
        [P("A", 1.0, 5.0), P("A", 9.0, 5.0)], 4.0, 0.04),
    req(7, "Repeat of 006 (A-A, separation 8, T=4).",
        [P("A", 1.0, 5.0), P("A", 9.0, 5.0)], 4.0, 0.04),
    req(8, "A-A pair at rest, separation 9 along x (y=5), T=4. Edge of the chamber span; far-field discriminator as in 006.",
        [P("A", 0.5, 5.0), P("A", 9.5, 5.0)], 4.0, 0.04),
    req(9, "Repeat of 008 (A-A, separation 9, T=4).",
        [P("A", 0.5, 5.0), P("A", 9.5, 5.0)], 4.0, 0.04),
    req(10, "A-A pair at rest, separation 4 along the 45-degree diagonal, T=2. Isotropy: compare with horizontal separation 4 (r3/003-004).",
        [P("A", 2.0, 2.0), P("A", 2.0 + off, 2.0 + off)], 2.0, 0.02),
    req(11, "A-A pair at rest, separation 4 along y (x=5), T=2. Isotropy: compare with horizontal separation 4 (r3/003-004).",
        [P("A", 5.0, 2.0), P("A", 5.0, 6.0)], 2.0, 0.02),
    req(12, "A-A pair at rest, separation 2 along x (y=5), T=0.5. Near-field low end of the proposed domain; the attraction should be strong (about 3 per particle) but contact is far.",
        [P("A", 4.0, 5.0), P("A", 6.0, 5.0)], 0.5, 0.01),
    req(13, "Cost constant check at the particle limit: 16 species-A particles at rest on a 4x4 grid (spacing 2), T=1. Predicted cost 1 + 0.02*16*1 = 1.32.",
        [P("A", x, y) for x in grid for y in grid], 1.0, 0.1, instruments=("tracker",)),
    req(14, "Review of P-0002 (lab-b): lone species-C at speed about 8.6 over 40 time units, many wall bounces. Tests the claim at high speed (claim tested only at speed 3.6).",
        [P("C", 3.0, 6.0, 7.0, -5.0)], 40.0, 0.1, account="review", cites="P-0002", instruments=("tracker", "census")),
    req(15, "Review of P-0002: lone species-C exact corner hit, from (8,8) with velocity (3,3), reaching (10,10) at t=2/3. Tests corner reflection for species C; claim does not state corners.",
        [P("C", 8.0, 8.0, 3.0, 3.0)], 20.0, 0.05, account="review", cites="P-0002", instruments=("tracker", "census")),
    req(16, "Review of P-0002: lone species-C at very low speed (0.22) over 100 time units, from (5,5) with velocity (0.2,0.1). Tests the claim's no-drift statement well beyond its 40-unit run.",
        [P("C", 5.0, 5.0, 0.2, 0.1)], 100.0, 0.1, account="review", cites="P-0002", instruments=("tracker", "census")),
]

total_research = 0.0
total_review = 0.0
for n, d in reqs:
    cost = 1 + 0.02 * len(d["setup"]["particles"]) * d["setup"]["duration"]
    if d["account"] == "review":
        total_review += cost
    else:
        total_research += cost
    with open(os.path.join(OUT, f"{n:03d}.json"), "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
print(f"wrote {len(reqs)} requests to {OUT}")
print(f"expected research cost {total_research:.2f}, review cost {total_review:.2f}")
