"""Writes lab-c round-1 (2026-11-18) requests under out/requests/2026-11-18/r1/lab-c/.

Research (A-A pair, relative velocity test):
  001 approach   (4,5) v=(+1,0); (6,5) v=(-1,0)
  002 recede     (4,5) v=(-1,0); (6,5) v=(+1,0)
  003 co-moving  (4,5) v=(0,+1); (6,5) v=(0,+1)   [absolute-velocity control]
  004 approach at r=4  (3,5) v=(+1,0); (7,5) v=(-1,0), T=0.8
  005 recede   at r=4  (3,5) v=(-1,0); (7,5) v=(+1,0), T=0.8
Review (cites P-0002, lone species C, speed 4.95, duration 60, exact corner hits):
  006 (3,?) -> start (1,1) v=(3.5,3.5)
"""
import json, os

OUT = "out/requests/2026-11-18/r1/lab-c"
os.makedirs(OUT, exist_ok=True)
DATE_ROUND = "2026-11-18/r1/lab-c"
TRACKER_CENSUS = ["tracker", "census"]


def part(sp, pos, vel):
    return {"species": sp, "pos": list(pos), "vel": list(vel)}


REQS = [
    ("001", "research", None,
     "Relative-velocity test, A-A at separation 2.0 along x, approaching (each speed 1 toward the other). "
     "Initial acceleration from a fit with known v0 and x0, compare with at-rest value from 2026-11-17/r3/lab-c/001 (F about 2.6). "
     "A velocity-dependent pair force would show a difference from 002.",
     {"particles": [part("A", (4.0, 5.0), (1.0, 0.0)), part("A", (6.0, 5.0), (-1.0, 0.0))], "duration": 0.4, "sample_dt": 0.0002}),
    ("002", "research", None,
     "Relative-velocity test, A-A at separation 2.0 along x, receding (each speed 1 away from the other). "
     "Compare with 001 (approaching). A conservative, velocity-independent force gives equal initial acceleration.",
     {"particles": [part("A", (4.0, 5.0), (-1.0, 0.0)), part("A", (6.0, 5.0), (1.0, 0.0))], "duration": 0.4, "sample_dt": 0.0002}),
    ("003", "research", None,
     "Absolute-velocity control, A-A at separation 2.0 along x, both particles moving together at (0,+1). "
     "Zero relative velocity. Should reproduce the at-rest force if the pair force depends only on relative state.",
     {"particles": [part("A", (4.0, 5.0), (0.0, 1.0)), part("A", (6.0, 5.0), (0.0, 1.0))], "duration": 0.4, "sample_dt": 0.0002}),
    ("004", "research", None,
     "Relative-velocity test at r=4.0 (static force about 0.57), A-A approaching at speed 1 each. "
     "Velocity effects may be relatively larger where the static force is small.",
     {"particles": [part("A", (3.0, 5.0), (1.0, 0.0)), part("A", (7.0, 5.0), (-1.0, 0.0))], "duration": 0.8, "sample_dt": 0.0004}),
    ("005", "research", None,
     "Relative-velocity test at r=4.0, A-A receding at speed 1 each. Pair with 004.",
     {"particles": [part("A", (3.0, 5.0), (-1.0, 0.0)), part("A", (7.0, 5.0), (1.0, 0.0))], "duration": 0.8, "sample_dt": 0.0004}),
    ("007", "research", None,
     "Species ratio across separation: A-B at rest, r=4.0 along x (T=0.8). Round 3 gave A-B at r=2 = 1.8 and A-A at r=2 = 2.6. "
     "A product-form pair law F_ij = kappa q_i q_j / r^2 predicts F_AB(4) about 0.39 (A-A at r=4 is 0.57, from 2026-11-17/r3/lab-c/003).",
     {"particles": [part("A", (3.0, 5.0), (0.0, 0.0)), part("B", (7.0, 5.0), (0.0, 0.0))], "duration": 0.8, "sample_dt": 0.0004}),
    ("008", "research", None,
     "Species ratio across separation: A-C at rest, r=4.0 along x (T=0.8). Round 3 gave A-C at r=2 = -2.5 (repulsive). "
     "Product-form prediction at r=4 about -0.55.",
     {"particles": [part("A", (3.0, 5.0), (0.0, 0.0)), part("C", (7.0, 5.0), (0.0, 0.0))], "duration": 0.8, "sample_dt": 0.0004}),
    ("009", "research", None,
     "Isotropy check, corrected. A-A at rest along y at r=2.0: (5,4) and (5,6). Replaces 2026-11-17/r3/lab-c/005, which placed both "
     "particles at (5,4) by mistake (a generator bug; r=0 is not a valid isotropy test). Compare with 2026-11-17/r3/lab-c/001 (along x).",
     {"particles": [part("A", (5.0, 4.0), (0.0, 0.0)), part("A", (5.0, 6.0), (0.0, 0.0))], "duration": 0.4, "sample_dt": 0.0002}),
    ("006", "review", "P-0002",
     "Review of P-0002 (lone species-C free flight, speed 3.6, duration 40). Edge test: speed 4.95 (paper tested 3.6), "
     "duration 60 (paper tested 40), exact diagonal with corner hits at t=2.57 (10,10) and t=5.43 (0,0). "
     "Speed decay would indicate drag; drift would indicate a bias.",
     {"particles": [part("C", (1.0, 1.0), (3.5, 3.5))], "duration": 60.0, "sample_dt": 0.03}),
]

for num, account, cites, purpose, setup in REQS:
    doc = {
        "request_id": f"{DATE_ROUND}/{num}",
        "lab": "lab-c",
        "account": account,
        "purpose": purpose,
        "setup": setup,
        "instruments": TRACKER_CENSUS,
    }
    if cites:
        doc["cites_paper"] = cites
    with open(os.path.join(OUT, f"{num}.json"), "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    print("wrote", num)
