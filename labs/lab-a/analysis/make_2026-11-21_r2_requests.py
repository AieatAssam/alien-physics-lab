"""lab-a round 2 (2026-11-21): writes research requests 001-004 and review-account requests 005-013.

Research: orientation/position control for the A-A r0 = 1.0 close result (r1/009 diagonal at (3,3) gave K 10.35,
about 3 sigma below the horizontal runs at (5,5), K 11.05 and 11.52), plus a third replicate at r0 = 1.25.
Review (cites P-0013, P-0014, P-0015): edge-of-domain runs for each paper, in domain and pre-registered.
Usage: python3 -I make_2026-11-21_r2_requests.py <repo_root>
"""
import json
import math
import os
import sys

root = sys.argv[1]
DATE, RND, LAB = "2026-11-21", "r2", "lab-a"
OUT = os.path.join(root, "out", "requests", DATE, RND, LAB)
os.makedirs(OUT, exist_ok=True)


def P(sp, x, y):
    return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}


def pair_centred(cx, cy, r, ux, uy, sp1, sp2):
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    return [P(sp1, cx - ux * r / 2, cy - uy * r / 2), P(sp2, cx + ux * r / 2, cy + uy * r / 2)]


R = [
    # n, account, cites, purpose, particles, T, dt
    (1, "research", None,
     "Orientation/position control, A-A r0 = 1.0, horizontal, centred (3,3), at rest, T=0.15. Compares with r1/009 (diagonal, centred (3,3), K 10.35) and the horizontal runs at (5,5) (K 11.05, 11.52). Rule: K within 1 sigma (~0.3) of 11.3 supports orientation independence at (3,3).",
     pair_centred(3.0, 3.0, 1.0, 1.0, 0.0, "A", "A"), 0.15, 0.0005),
    (2, "research", None,
     "Orientation/position control, A-A r0 = 1.0, diagonal, centred (5,5), at rest, T=0.15. Second control for r1/009. Rule: K within 1 sigma of 11.3 supports orientation independence; K near 10.35 with a horizontal near 11.3 points to an orientation effect.",
     pair_centred(5.0, 5.0, 1.0, 1.0, 1.0, "A", "A"), 0.15, 0.0005),
    (3, "research", None,
     "Repeat of r1/009 (A-A r0 = 1.0, diagonal, centred (3,3), T=0.15, identical setup), to test whether K 10.35 reproduces. Two runs pinned to the same setup separate noise from a geometry effect.",
     pair_centred(3.0, 3.0, 1.0, 1.0, 1.0, "A", "A"), 0.15, 0.0005),
    (4, "research", None,
     "Third replicate of A-A r0 = 1.25, horizontal, centred (5,5), at rest, T=0.15. r1/005 and r1/006 gave K 11.55 and 13.25 (about 2 sigma apart); the pre-registered mean 12.5 needs a third run before the r0 = 1.25 point is used.",
     pair_centred(5.0, 5.0, 1.25, 1.0, 0.0, "A", "A"), 0.15, 0.0005),
    (5, "review", "P-0013",
     "Edge test of P-0013 (A-A, r0 = 1.5, at rest, T=0.4, both particles 2+ from walls): horizontal centred (5,5). In domain; tests the A-A scale S_AA = 0.753 on a fresh pair. Compare with 2026-11-20/r1/lab-a/003 (A-A r0 = 1.5, T=0.3).",
     pair_centred(5.0, 5.0, 1.5, 1.0, 0.0, "A", "A"), 0.4, 0.0005),
    (6, "review", "P-0013",
     "Mixed-species test of P-0013 (A-C, r0 = 1.5, at rest, T=0.4): A on the lower side, C above, vertical, centred (5,5). Tests S_AC = 0.811 on the cross pair, with unscaled P-0008 coefficients as the alternative (P-0013 itself says the judged metric does not separate them).",
     [P("A", 5.0, 4.25), P("C", 5.0, 5.75)], 0.4, 0.0005),
    (7, "review", "P-0013",
     "C-C test of P-0013 (r0 = 1.5, at rest, T=0.4), diagonal along (0.6,0.8), centred (5,5). Tests S_CC = 0.874 at r0 = 1.5 on an orientation not used by the paper's own fits.",
     pair_centred(5.0, 5.0, 1.5, 0.6, 0.8, "C", "C"), 0.4, 0.0005),
    (8, "review", "P-0014",
     "Edge test of P-0014 at its T limit: A-A at r0 = 2.5 (lower edge of 2.5 to 3.5), at rest, T=2.0, horizontal centred (5,5). The claim's T up to 2 is untested at r0 below 4; the paper's model predicts a close approach here, so the run probes both the coefficient and the collision regime.",
     pair_centred(5.0, 5.0, 2.5, 1.0, 0.0, "A", "A"), 2.0, 0.005),
    (9, "review", "P-0014",
     "Mixed edge test of P-0014 (A-C, r0 = 2.5, at rest, T=2.0), horizontal centred (5,5). Tests the cross-pair table at the lower edge of the range and the long T.",
     pair_centred(5.0, 5.0, 2.5, 1.0, 0.0, "A", "C"), 2.0, 0.005),
    (10, "review", "P-0014",
     "Edge test of P-0014 (C-C, r0 = 3.5, upper edge of 2.5 to 3.5, at rest, T=2.0), horizontal centred (5,5). The paper's model predicts a close approach at this pair within T=2; tests whether the claim holds at the upper edge at the T limit.",
     pair_centred(5.0, 5.0, 3.5, 1.0, 0.0, "C", "C"), 2.0, 0.005),
    (11, "review", "P-0015",
     "Edge test of P-0015 (B-C, r0 = 1.0 exact, at rest, T=0.6, the claim's T limit), horizontal centred (5,5), B on the left. Tests K_BC = -4.32 and K_CB = -7.31 at the duration limit.",
     pair_centred(5.0, 5.0, 1.0, 1.0, 0.0, "B", "C"), 0.6, 0.0005),
    (12, "review", "P-0015",
     "Orientation test of P-0015 (B-C, r0 = 1.0, at rest, T=0.6), diagonal along (0.6,0.8), centred (5,5), B at lower left. Second orientation for the close B-C constants.",
     pair_centred(5.0, 5.0, 1.0, 0.6, 0.8, "B", "C"), 0.6, 0.0005),
    (13, "review", "P-0015",
     "Order test of P-0015 (C-B, r0 = 1.0, at rest, T=0.6), vertical, centred (5,5), C below and B above. Checks the C-first ordering, since the claim's K_BC and K_CB enter by species not slot.",
     [P("C", 5.0, 4.5), P("B", 5.0, 5.5)], 0.6, 0.0005),
]

for n, account, cites, purpose, parts, T, dt in R:
    rid = "%s/%s/%s/%03d" % (DATE, RND, LAB, n)
    doc = {
        "request_id": rid,
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": parts, "duration": T, "sample_dt": dt},
        "instruments": ["tracker", "census"],
    }
    if cites:
        doc["cites_paper"] = cites
    with open(os.path.join(OUT, "%03d.json" % n), "w") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")
    d = math.dist(parts[0]["pos"], parts[1]["pos"])
    print(rid, account, cites or "-", "".join(p["species"] for p in parts), "r0=%.3f" % d, "T=%s" % T,
          "cost=%.3f" % (1 + 0.02 * len(parts) * T), len(purpose))
