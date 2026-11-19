#!/usr/bin/env python3
"""lab-keystone, round 1 (2026-11-19).

Writes the experiment requests and the grant proposal, and pre-registers
predictions for each request from the P-0005 pair table (lab-a), before any
results exist.

Run from the repository root:
    python3 out/labs/lab-keystone/analysis/plan_round1.py

Two force-law hypotheses are integrated, with no walls and no collisions
handled (the script reports the minimum pair separation so that a predicted
collision is visible):
  H1: accel on i = K_i(j) * r^-2.5 * unit(x_j - x_i)          (power law, P-0005)
  H2: same K, but radial factor 5^-2.5 (5/r)^2 exp(-(r-5)/8)  (screened form, P-0003)
K_i(j) is the acceleration coefficient on a particle of species i from species j
at r = 5, positive = attraction. Values are P-0005 run means.
"""
import json
import math
import os

import numpy as np

DATE = "2026-11-19"
ROUND = "r1"
LAB = "lab-keystone"
REPO_REQ_DIR = os.path.join("out", "requests", DATE, ROUND, LAB)
REPO_GRANT_DIR = os.path.join("out", "grants", DATE, "proposals")
ANALYSIS_DIR = os.path.join("out", "labs", LAB, "analysis")

# K_i(j), from P-0005 table (run means, separation 5, P = 2.5)
K = {
    ("A", "A"): 18.0,
    ("A", "B"): 8.99, ("B", "A"): 12.34,
    ("A", "C"): -8.77, ("C", "A"): -21.25,
    ("B", "B"): 6.12,
    ("C", "C"): 12.36,
    ("B", "C"): -6.10, ("C", "B"): -10.59,
}


def f_power(r):
    return r ** -2.5


def f_screen(r):
    return 5.0 ** -2.5 * (5.0 / r) ** 2 * math.exp(-(r - 5.0) / 8.0)


def accel(x, species, f):
    n = len(species)
    a = np.zeros_like(x)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = x[j] - x[i]
            r = float(np.linalg.norm(d))
            a[i] += K[(species[i], species[j])] * f(r) * d / r
    return a


def simulate(x0, species, T, f, dt=1e-3):
    """RK4 integration from rest. Returns final positions and min pair separation."""
    x = np.array(x0, dtype=float)
    v = np.zeros_like(x)
    n = int(round(T / dt))
    min_sep = np.inf
    for _ in range(n):
        def deriv(xx, vv):
            return vv, accel(xx, species, f)
        k1x, k1v = deriv(x, v)
        k2x, k2v = deriv(x + 0.5 * dt * k1x, v + 0.5 * dt * k1v)
        k3x, k3v = deriv(x + 0.5 * dt * k2x, v + 0.5 * dt * k2v)
        k4x, k4v = deriv(x + dt * k3x, v + dt * k3v)
        x = x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        v = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        for i in range(len(species)):
            for j in range(i + 1, len(species)):
                min_sep = min(min_sep, float(np.linalg.norm(x[i] - x[j])))
    return x, min_sep


def pair(s1, s2, r, y=5.0):
    """Two particles at rest, centred at x = 5, separation r along x."""
    return [
        {"species": s1, "pos": [5.0 - r / 2, y], "vel": [0.0, 0.0]},
        {"species": s2, "pos": [5.0 + r / 2, y], "vel": [0.0, 0.0]},
    ]


def particles_from(spec):
    return [{"species": s, "pos": p, "vel": v} for s, p, v in spec]


def request(n, account, purpose, particles, T, dt, cites=None):
    req = {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{n:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
    }
    if cites:
        req["cites_paper"] = cites
    req["setup"] = {"particles": particles, "duration": T, "sample_dt": dt}
    req["instruments"] = ["tracker", "census"]
    return req


def cost(particles, T, k=0.02):
    # Season k is not yet observed by this lab; 0.02 is the value lab-a reports.
    return 1 + k * len(particles) * T


REQUESTS = []

# ---- review account (11.2 of 15 credits), each cites the paper it tests ----
REQUESTS.append(request(1, "review",
    "Edge of P-0001 domain: lone A at speed 4.2 (tested only at 1.1), passes through the corner (1,1)->(10,10) at t = 3.",
    particles_from([("A", [1.0, 1.0], [3.0, 3.0])]), 10.0, 0.1, cites="P-0001"))
REQUESTS.append(request(2, "review",
    "Edge of P-0002 domain: lone C at speed 6.0 (tested at 3.6), 20 time units, many wall bounces.",
    particles_from([("C", [1.0, 5.0], [6.0, 0.5])]), 20.0, 0.1, cites="P-0002"))
REQUESTS.append(request(3, "review",
    "Far field for P-0003 (separation 8, beyond its 3-6 domain): power law r^-2.5 vs screened exp(-r/8)/r^2 differ by about 13% at r = 8.",
    pair("A", "A", 8.0), 6.0, 0.1, cites="P-0003"))
REQUESTS.append(request(4, "review",
    "Far field for P-0003 (separation 9): power law and screened form differ by about 19%.",
    pair("A", "A", 9.0), 6.0, 0.1, cites="P-0003"))
for n, (s1, s2) in zip(range(5, 11), [("A", "A"), ("A", "B"), ("A", "C"), ("B", "B"), ("C", "C"), ("B", "C")]):
    REQUESTS.append(request(n, "review",
        f"Edge of P-0005 domain (separation 5 only): {s1}-{s2} pair at rest at separation 3, tests whether the P-0005 coefficient scales as r^-2.5.",
        pair(s1, s2, 3.0), 1.0, 0.05, cites="P-0005"))

# ---- research account (about 7 of 40 credits) ----
REQUESTS.append(request(11, "research",
    "Three-body additivity: A, A, C at rest, triangle sides about 4-4.5. Tests whether the pairwise sum holds for N = 3 (untested in any paper).",
    particles_from([("A", [3.0, 3.0], [0.0, 0.0]), ("A", [7.0, 3.0], [0.0, 0.0]), ("C", [5.0, 7.0], [0.0, 0.0])]),
    2.0, 0.05))
REQUESTS.append(request(12, "research",
    "Four-body additivity: A, B, C, A at rest on a square of side 4. Mixed species, N = 4.",
    particles_from([("A", [3.0, 3.0], [0.0, 0.0]), ("B", [7.0, 3.0], [0.0, 0.0]),
                    ("C", [3.0, 7.0], [0.0, 0.0]), ("A", [7.0, 7.0], [0.0, 0.0])]),
    2.0, 0.05))
REQUESTS.append(request(13, "research",
    "Far field, A-B pair at separation 8, T = 6: the A-B coefficient at a second separation.",
    pair("A", "B", 8.0), 6.0, 0.1))
REQUESTS.append(request(14, "research",
    "Far field, A-C pair at separation 8, T = 3 (C is repelled, so a longer run would push it into the wall).",
    pair("A", "C", 8.0), 3.0, 0.1))
REQUESTS.append(request(15, "research",
    "Far field, B-C pair at separation 8, T = 4 (same wall margin reason as 014).",
    pair("B", "C", 8.0), 4.0, 0.1))
REQUESTS.append(request(16, "research",
    "Lone species-B free flight, 20 time units, many wall bounces. The lone-particle baseline has only been measured for A and C.",
    particles_from([("B", [2.0, 2.0], [1.5, -1.0])]), 20.0, 0.1))


def predict_all():
    out = []
    for req in REQUESTS:
        parts = req["setup"]["particles"]
        species = [p["species"] for p in parts]
        x0 = [p["pos"] for p in parts]
        T = req["setup"]["duration"]
        if req["setup"]["particles"][0]["vel"] != [0.0, 0.0] or len(parts) == 1:
            # free-flight and moving-particle requests: not predicted by the pair table
            out.append({"request_id": req["request_id"], "note": "free flight, prediction = straight-line with specular walls (see P-0001/P-0002)",
                        "cost": cost(parts, T)})
            continue
        xh1, msep1 = simulate(x0, species, T, f_power)
        xh2, msep2 = simulate(x0, species, T, f_screen)
        out.append({
            "request_id": req["request_id"],
            "cost": cost(parts, T),
            "H1_final_pos": xh1.round(3).tolist(),
            "H2_final_pos": xh2.round(3).tolist(),
            "H1_min_pair_sep": round(msep1, 3),
            "H2_min_pair_sep": round(msep2, 3),
            "H1_minus_H2_max_displacement": round(float(np.max(np.abs(xh1 - xh2))), 3),
        })
    return out


GRANT = {
    "lab": LAB,
    "date": DATE,
    "title": "Superposition test: 16 particles at rest on a 4x4 lattice, mixed species",
    "pitch": (
        "Sixteen particles at rest on a 4x4 lattice (spacing 2.7), species A/B/C mixed. "
        "The pair table (P-0005, r^-2.5 at separation 5) predicts each particle's acceleration as a sum over partners. "
        "Pre-registered: each particle's displacement at T = 1.0 is within 15% of the additive prediction. "
        "A larger deviation counts against additivity at N > 2. "
        "No paper here tests N > 2 additivity. Nearest-neighbour spacing 2.7 lies below the fitted range (3 to 6), so this also probes the short-range form."
    ),
    "setup": {
        "particles": [],
        "duration": 1.0,
        "sample_dt": 0.02,
    },
}

LATTICE_SPECIES = [
    ["A", "B", "C", "A"],
    ["B", "C", "A", "B"],
    ["C", "A", "B", "C"],
    ["A", "B", "C", "A"],
]
for iy, row in enumerate(LATTICE_SPECIES):
    for ix, s in enumerate(row):
        GRANT["setup"]["particles"].append({
            "species": s,
            "pos": [round(1.0 + 2.7 * ix, 2), round(1.0 + 2.7 * iy, 2)],
            "vel": [0.0, 0.0],
        })


def main():
    os.makedirs(REPO_REQ_DIR, exist_ok=True)
    os.makedirs(REPO_GRANT_DIR, exist_ok=True)
    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    review_total = 0.0
    research_total = 0.0
    for req in REQUESTS:
        n = int(req["request_id"].split("/")[-1])
        path = os.path.join(REPO_REQ_DIR, f"{n:03d}.json")
        with open(path, "w") as fh:
            json.dump(req, fh, indent=2)
            fh.write("\n")
        c = cost(req["setup"]["particles"], req["setup"]["duration"])
        if req["account"] == "review":
            review_total += c
        else:
            research_total += c
    print(f"review credits planned: {review_total:.2f} / 15")
    print(f"research credits planned: {research_total:.2f} / 40")

    with open(os.path.join(REPO_GRANT_DIR, f"{LAB}.json"), "w") as fh:
        json.dump(GRANT, fh, indent=2)
        fh.write("\n")

    preds = predict_all()
    with open(os.path.join(ANALYSIS_DIR, "predictions_round1.json"), "w") as fh:
        json.dump(preds, fh, indent=2)
        fh.write("\n")
    for p in preds:
        print(json.dumps(p))

    # grant main event: lattice prediction
    gp = [p["species"] for p in GRANT["setup"]["particles"]]
    gx = [p["pos"] for p in GRANT["setup"]["particles"]]
    xg1, mg1 = simulate(gx, gp, GRANT["setup"]["duration"], f_power)
    xg2, mg2 = simulate(gx, gp, GRANT["setup"]["duration"], f_screen)
    print("grant H1 min pair sep:", round(mg1, 3), " H2:", round(mg2, 3))
    print("grant max |H1-H2| displacement:", round(float(np.max(np.abs(xg1 - xg2))), 3))


if __name__ == "__main__":
    main()
