"""Design of H30 (A-A distance law, round 3, 2026-11-23). Written before any H30 result exists.

Question: is the A-A pair force K / r^P with one (K, P) over separations 3 to 9?
Method: two A particles at rest, separations 3, 5, 7, 9, horizontal and diagonal, centre (5,5).
Short T chosen per separation so the pair moves a few percent of r0 (local acceleration regime).
Each run gives a local acceleration, read from the trajectory with the P = 2.5 model
(fit K only). Replicated 2 horizontal + 2 diagonal per separation.

Pre-registered prediction (P = 2.5, K = 17.7, from P-0003): K_fit = 17.7 at every separation.
Local acceleration a(r0) = 17.7 / r0^2.5: 1.14, 0.317, 0.137, 0.0728.

This script (a) computes the predicted trajectories with K = 17.7 and checks minimum separation
(no run may approach within 1.0, where the integrator is not trustworthy), and (b) writes the
round-3 request files and the pre-registration JSON. It does not read any H30 results.

Usage: python3 -I design_H30_2026-11-23.py <repo_root_out_dir>
  <repo_root_out_dir> = out/ directory of the lab's output tree (requests written beneath it).
"""
import json
import math
import os
import sys

DATE = "2026-11-23"
ROUND = "r3"
LAB = "lab-a"
K_REF = 17.7
P_REF = 2.5
CENTRE = (5.0, 5.0)
MIN_SEP_LIMIT = 1.0

# (separation, T, orientation)
DESIGN = []
for sep, T in ((3.0, 1.0), (5.0, 2.0), (7.0, 3.0), (9.0, 3.0)):
    for orient in ("horizontal", "horizontal", "diagonal", "diagonal"):
        DESIGN.append((sep, T, orient))


def positions(sep, orient):
    cx, cy = CENTRE
    if orient == "horizontal":
        d = (sep / 2.0, 0.0)
    elif orient == "vertical":
        d = (0.0, sep / 2.0)
    else:
        s = sep / 2.0 / math.sqrt(2.0)
        d = (s, s)
    return [(cx - d[0], cy - d[1]), (cx + d[0], cy + d[1])]


def simulate_min_sep(p0, K, P, T, h=2e-4):
    """RK4 two-body. Returns minimum separation over [0, T]."""
    x = [list(p) for p in p0]
    v = [[0.0, 0.0], [0.0, 0.0]]

    def acc(xx):
        dx = xx[1][0] - xx[0][0]
        dy = xx[1][1] - xx[0][1]
        r = math.hypot(dx, dy)
        f = K / r ** (P + 1)
        return [[f * dx, f * dy], [-f * dx, -f * dy]]

    n = int(round(T / h))
    rmin = math.dist(x[0], x[1])
    for _ in range(n):
        a1 = acc(x)
        x2 = [[x[i][c] + 0.5 * h * v[i][c] for c in range(2)] for i in range(2)]
        v2 = [[v[i][c] + 0.5 * h * a1[i][c] for c in range(2)] for i in range(2)]
        a2 = acc(x2)
        x3 = [[x[i][c] + 0.5 * h * v2[i][c] for c in range(2)] for i in range(2)]
        v3 = [[v[i][c] + 0.5 * h * a2[i][c] for c in range(2)] for i in range(2)]
        a3 = acc(x3)
        x4 = [[x[i][c] + h * v3[i][c] for c in range(2)] for i in range(2)]
        v4 = [[v[i][c] + h * a3[i][c] for c in range(2)] for i in range(2)]
        a4 = acc(x4)
        for i in range(2):
            for c in range(2):
                x[i][c] += h / 6 * (v[i][c] + 2 * v2[i][c] + 2 * v3[i][c] + v4[i][c])
                v[i][c] += h / 6 * (a1[i][c] + 2 * a2[i][c] + 2 * a3[i][c] + a4[i][c])
        rmin = min(rmin, math.dist(x[0], x[1]))
    return rmin


def sample_dt_for(T):
    # 1990 samples: safely below the 2000 limit, avoids float issues at the boundary.
    return T / 1990.0


def make_request(idx, sep, T, orient):
    rid = f"{DATE}/{ROUND}/{LAB}/{idx:03d}"
    pos = positions(sep, orient)
    return {
        "request_id": rid,
        "lab": LAB,
        "account": "research",
        "purpose": (f"H30 A-A distance law. Two A at rest, separation {sep} ({orient}), centre (5,5), "
                    f"T={T}. Local acceleration at r0 = {sep}; prediction K=17.7, P=2.5."),
        "setup": {
            "particles": [
                {"species": "A", "pos": [round(pos[0][0], 6), round(pos[0][1], 6)], "vel": [0.0, 0.0]},
                {"species": "A", "pos": [round(pos[1][0], 6), round(pos[1][1], 6)], "vel": [0.0, 0.0]},
            ],
            "duration": T,
            "sample_dt": round(sample_dt_for(T), 10),
        },
        "instruments": ["tracker"],
    }


def main():
    out_root = sys.argv[1]
    req_dir = os.path.join(out_root, "requests", DATE, ROUND, LAB)
    os.makedirs(req_dir, exist_ok=True)
    prereg = {"id": "H30-A-A-distance-law", "date": DATE, "lab": LAB,
              "status": "pre-registered before H30 results exist",
              "prediction": {"K": K_REF, "P": P_REF,
                             "local_accel": {str(s): round(K_REF / s ** P_REF, 5) for s in (3.0, 5.0, 7.0, 9.0)}},
              "runs": [], "decision_rule": {
                  "supported": "every separation: mean K_fit within 4% of 17.7, and both orientations agree within 3%",
                  "refuted": "any separation mean K_fit off 17.7 by more than 8%, with replicates agreeing within 3%",
                  "inconclusive": "otherwise. Record and do not claim either way.",
                  "secondary": "free-P slope from local accelerations, P = ln(a3/a9)/ln(3). Reported, not decisive."}}
    min_sep_ok = True
    for i, (sep, T, orient) in enumerate(DESIGN, start=1):
        req = make_request(i, sep, T, orient)
        pos = [tuple(p["pos"]) for p in req["setup"]["particles"]]
        rmin = simulate_min_sep(pos, K_REF, P_REF, T)
        if rmin < MIN_SEP_LIMIT:
            min_sep_ok = False
        cost = 1 + 0.02 * 2 * T
        prereg["runs"].append({"request_id": req["request_id"], "sep": sep, "T": T, "orient": orient,
                               "predicted_min_sep": round(rmin, 4), "cost_est": round(cost, 4)})
        path = os.path.join(req_dir, f"{i:03d}.json")
        with open(path, "w") as f:
            json.dump(req, f, indent=2)
            f.write("\n")
        print(i, req["request_id"], sep, T, orient, "min_sep", round(rmin, 3), "cost", round(cost, 3))
    total = sum(r["cost_est"] for r in prereg["runs"])
    prereg["total_cost_est"] = round(total, 3)
    print("total cost est", round(total, 3), "min_sep_ok", min_sep_ok)
    with open(os.path.join(out_root, "labs", LAB, "analysis", f"prereg_H30_{DATE}.json"), "w") as f:
        json.dump(prereg, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
