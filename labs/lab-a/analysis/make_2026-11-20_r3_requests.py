"""lab-a, 2026-11-20 round 3: write the round-3 request files (validated against protocol/request.schema.json).

Order in file names matters for budget (requests over budget are rejected in file order).
Usage: python3 -I make_2026-11-20_r3_requests.py <repo_root>
"""
import json
import os
import sys

root = sys.argv[1]
DATE, ROUND, LAB = "2026-11-20", 3, "lab-a"
outdir = os.path.join(root, "out", "requests", DATE, "r%d" % ROUND, LAB)
os.makedirs(outdir, exist_ok=True)


def P(species, x, y, vx=0.0, vy=0.0):
    return {"species": species, "pos": [x, y], "vel": [vx, vy]}


def req(n, account, purpose, particles, duration, sample_dt, cites=None):
    d = {
        "request_id": "%s/r%d/%s/%03d" % (DATE, ROUND, LAB, n),
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": particles, "duration": duration, "sample_dt": sample_dt},
        "instruments": ["tracker", "census"],
    }
    if cites:
        d["cites_paper"] = cites
    assert len(purpose) <= 500, n
    assert duration / sample_dt <= 2000 + 1e-9, n
    return d


reqs = [
    # 001 grant main event: exactly the filed proposal (grants/2026-11-20/proposals/lab-a.json), cost 1.02
    req(1, "grant",
        "Grant main event, as proposed: close-range C-C pair at rest, separation 2.0, T = 0.5, centred at (5,5). "
        "Pre-registered flat-K test (analysis/pred_2026-11-20_CC_r2_grant.json: K = 12.36, predicted separation "
        "1.370 at T = 0.5). Rule: fit K (P = 2.5 fixed) to the separation profile; the round-2 run at separation 3 "
        "gave K_fit = 13.05 (+5.6%, inconclusive).",
        [P("C", 4.0, 5.0), P("C", 6.0, 5.0)], 0.5, 0.0005),
    # 002 research: replicate of 2026-11-20/r2/lab-a/001 (C-C at separation 3, T = 1). Pre-registered rule
    # (analysis/pred_close_CC3_2026-11-20.py) said repeat if inconclusive.
    req(2, "research",
        "Replicate of 2026-11-20/r2/lab-a/001 (C-C pair at rest, separation 3.0, T = 1.0, centred at (5,5)). "
        "That run gave K_fit = 13.05 (P = 2.5 fixed), +5.6% from 12.36: inconclusive under the pre-registered rule. "
        "Same design, same rule (analysis/pred_close_CC3_2026-11-20.py).",
        [P("C", 3.5, 5.0), P("C", 6.5, 5.0)], 1.0, 0.002),
    # 003, 004 research: A-A at separation 1.0, T = 0.15, two runs. Pre-registered in
    # analysis/pred_AA_r1p0_2026-11-20.py (flat K = 18 vs trend K in [14, 15.6]).
    req(3, "research",
        "Close-range A-A pair at rest, separation 1.0, T = 0.15, centred at (5,5). First data at r < 1.5 for A-A. "
        "Pre-registered in analysis/pred_AA_r1p0_2026-11-20.py: flat K = 18 (sep(T) 0.480) vs trend K in [14,15.6] "
        "(sep(T) 0.571-0.626). Rule: fit K (P = 2.5) on the separation profile. Repeat run 004 follows.",
        [P("A", 4.5, 5.0), P("A", 5.5, 5.0)], 0.15, 0.0005),
    req(4, "research",
        "Repeat of 2026-11-20/r3/lab-a/003 (A-A pair at rest, separation 1.0, T = 0.15, centred at (5,5)), same "
        "pre-registration in analysis/pred_AA_r1p0_2026-11-20.py. Repeated before trust.",
        [P("A", 4.5, 5.0), P("A", 5.5, 5.0)], 0.15, 0.0005),
    # 005 research: replicate of 2026-11-20/r1/lab-a/004 (B-B at separation 2, T = 0.5; K_fit 5.7 vs 6.12 flat).
    req(5, "research",
        "Replicate of 2026-11-20/r1/lab-a/004 (B-B pair at rest, separation 2.0, T = 0.5, centred at (5,5)). "
        "The first run gave K_fit = 5.7 (P = 2.5), 7% below the separation-5 value 6.12 (P-0005). Pre-registered in "
        "analysis/pred_2026-11-20_BB_r2.json. Rule: fit K on the separation profile, flat if within 5% of 6.12.",
        [P("B", 4.0, 5.0), P("B", 6.0, 5.0)], 0.5, 0.0005),
    # 006-009 review of P-0010 (keystone, two particles at rest, r0 in [6, 9], T <= 6). Review account, cites P-0010.
    req(6, "review",
        "Review of P-0010, bulk edge: C-C pair at rest, r0 = 9.0 (domain upper edge), T = 6 (domain limit). "
        "Tests the S_C = 0.9475 factor at r0 = 9 (keystone G(9) = 0.682, K_CC = 8.0). Non-colliding (predicted min "
        "separation 7.7).",
        [P("C", 0.5, 5.0), P("C", 9.5, 5.0)], 6.0, 0.01, cites="P-0010"),
    req(7, "review",
        "Review of P-0010, bulk: A-A pair at rest on the diagonal, r0 = 7.5, T = 6. Isotropy check at the claim's "
        "radial factor G(7.5) = 0.820 (K_AA = 14.8). Non-colliding (predicted min separation 2.8).",
        [P("A", 1.5, 1.5), P("A", 6.8033, 6.8033)], 6.0, 0.01, cites="P-0010"),
    req(8, "review",
        "Review of P-0010, bulk lower edge: B-B pair at rest, r0 = 6.0 (domain lower edge), T = 6. Tests the "
        "radial factor G(6) = 0.958 for an own-species pair with no C factor (K_BB = 5.86). Non-colliding "
        "(predicted min separation 2.9).",
        [P("B", 2.0, 6.0), P("B", 8.0, 6.0)], 6.0, 0.01, cites="P-0010"),
    req(9, "review",
        "Review of P-0010, domain edge where the predictor has no collision handling: A-A pair at rest, r0 = 6.0, "
        "T = 6. Predicted collision near t = 4.1 (min separation 0.02, K_AA = 17.2 fixed). The claim's domain "
        "includes T <= 6, so this run tests the claim where it is undefined. Companion to the bulk runs 006-008.",
        [P("A", 2.0, 5.0), P("A", 8.0, 5.0)], 6.0, 0.01, cites="P-0010"),
    # 010-012 review of P-0011 (lab-vernier, lone particle, tracker noise sd 0.05, no wall clipping).
    req(10, "review",
        "Review of P-0011 (c3, no wall clipping): lone A particle at rest at (0.05, 5.0), T = 10. Tests whether "
        "the tracker reports x < 0 with zero-mean residual and sd near 0.05 per coordinate.",
        [P("A", 0.05, 5.0)], 10.0, 0.01, cites="P-0011"),
    req(11, "review",
        "Review of P-0011 (c2, species independence): lone B particle, speed about 0.94, from (5,5) with velocity "
        "(0.8, -0.5), T = 10 (wall reflections). Residual sd per coordinate against the reflected-line model.",
        [P("B", 5.0, 5.0, 0.8, -0.5)], 10.0, 0.01, cites="P-0011"),
    req(12, "review",
        "Review of P-0011 (c2, species independence): lone C particle from (9.0, 2.0) with velocity (-1.2, 0.7), "
        "T = 10 (wall reflections). Residual sd per coordinate against the reflected-line model.",
        [P("C", 9.0, 2.0, -1.2, 0.7)], 10.0, 0.01, cites="P-0011"),
]

for r in reqs:
    path = os.path.join(outdir, "%s.json" % r["request_id"].split("/")[-1])
    with open(path, "w") as fh:
        json.dump(r, fh, indent=2)
        fh.write("\n")
    print(path, r["account"], "cost~%.3f" % (1 + 0.02 * len(r["setup"]["particles"]) * r["setup"]["duration"]))
