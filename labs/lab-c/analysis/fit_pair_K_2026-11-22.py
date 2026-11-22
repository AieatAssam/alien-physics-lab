#!/usr/bin/env python3
"""Free-coupling chi2 fits of the two-body pre-contact window (lab-c, 2026-11-22).

Model: particle i accelerates toward j with magnitude K[(s_i, s_j)] / r**2.5 (P fixed at 2.5), at rest at t=0.
Fit: grid search on the couplings, chi2 on tracker positions with sigma = 0.05 per coordinate,
using only samples with t <= tmax, where tmax is the last time the measured separation stays >= 0.6.
Integrator: RK4, step 0.0005, no walls (the pairs stay near the chamber centre in these windows).
Run as: python3 -I fit_pair_K_2026-11-22.py REPO_ROOT
"""
import json, math, sys
from pathlib import Path

REPO = Path(sys.argv[1])
SIGMA = 0.05
P = 2.5
H = 0.0005


def load(rid):
    rq = json.loads((REPO / "requests" / (rid + ".json")).read_text())
    rs = json.loads((REPO / "results" / (rid + ".json")).read_text())
    return rq["setup"], rs["samples"]


def simulate(K, species, pos0, t_end):
    # two particles, at rest; K maps (species_i, species_j) -> coupling
    p = [list(pos0[0]), list(pos0[1])]
    v = [[0.0, 0.0], [0.0, 0.0]]
    out = {0.0: [list(p[0]), list(p[1])]}

    def acc(pp):
        dx = pp[1][0] - pp[0][0]
        dy = pp[1][1] - pp[0][1]
        r = math.hypot(dx, dy)
        a = [[0.0, 0.0], [0.0, 0.0]]
        k01 = K[(species[0], species[1])]
        k10 = K[(species[1], species[0])]
        f0 = k01 / r ** P
        f1 = k10 / r ** P
        a[0] = [f0 * dx / r, f0 * dy / r]
        a[1] = [-f1 * dx / r, -f1 * dy / r]
        return a

    n = int(round(t_end / H))
    for s in range(n):
        h = H
        k1v = acc(p)
        k1p = v
        p2 = [[p[i][k] + h / 2 * v[i][k] for k in range(2)] for i in range(2)]
        v2 = [[v[i][k] + h / 2 * k1v[i][k] for k in range(2)] for i in range(2)]
        k2v = acc(p2)
        p3 = [[p[i][k] + h / 2 * v2[i][k] for k in range(2)] for i in range(2)]
        v3 = [[v[i][k] + h / 2 * k2v[i][k] for k in range(2)] for i in range(2)]
        k3v = acc(p3)
        p4 = [[p[i][k] + h * v3[i][k] for k in range(2)] for i in range(2)]
        v4 = [[v[i][k] + h * k3v[i][k] for k in range(2)] for i in range(2)]
        k4v = acc(p4)
        p = [[p[i][k] + h / 6 * (k1p[i][k] + 2 * v2[i][k] + 2 * v3[i][k] + v4[i][k]) for k in range(2)] for i in range(2)]
        v = [[v[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)] for i in range(2)]
        out[round((s + 1) * H, 9)] = [list(p[0]), list(p[1])]
    return out


def tmax_window(samples):
    # last time the measured separation has stayed >= 0.6
    last = 0.0
    for s in samples:
        a, b = s["particles"][0]["pos"], s["particles"][1]["pos"]
        if math.dist(a, b) >= 0.6:
            last = s["t"]
        else:
            break
    return last


def chi2(K, species, setup, samples, tfit):
    pos0 = [p["pos"] for p in setup["particles"]]
    sim = simulate(K, species, pos0, tfit)
    tot, n = 0.0, 0
    for s in samples:
        if s["t"] > tfit + 1e-12 or s["t"] == 0.0:
            continue
        key = round(s["t"], 9)
        if key not in sim:
            continue
        for i, p in enumerate(s["particles"]):
            q = sim[key][i]
            tot += ((q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2) / SIGMA ** 2
            n += 2
    return tot, n


def fit_two(species, setup, samples, tfit, grid_a, grid_b):
    best = None
    for a in grid_a:
        for b in grid_b:
            K = {(species[0], species[1]): a, (species[1], species[0]): b}
            c, n = chi2(K, species, setup, samples, tfit)
            if best is None or c < best[0]:
                best = (c, a, b, n)
    return best


def frange(lo, hi, step):
    x, out = lo, []
    while x <= hi + 1e-9:
        out.append(round(x, 4))
        x += step
    return out


def main():
    print("run, species, orientation, tfit, n_obs, K_fit(on_i_from_j), K_fit(on_j_from_i), chi2/n")
    # A-B runs: (request id, orientation)
    ab_runs = ["2026-11-20/r1/lab-c/002", "2026-11-21/r1/lab-c/002", "2026-11-21/r2/lab-c/002",
               "2026-11-22/r1/lab-c/004", "2026-11-22/r1/lab-c/005"]
    for rid in ab_runs:
        setup, samples = load(rid)
        sp = "".join(p["species"] for p in setup["particles"])
        tfit = min(0.15, tmax_window(samples))  # fit window: the claim's T <= 0.15, pre-contact
        best = fit_two(tuple(p["species"] for p in setup["particles"]), setup, samples, tfit,
                       frange(3.0, 8.0, 0.1), frange(4.0, 11.0, 0.1))
        c, a, b, n = best
        # refine
        best2 = fit_two(tuple(p["species"] for p in setup["particles"]), setup, samples, tfit,
                        frange(a - 0.1, a + 0.1, 0.01), frange(b - 0.1, b + 0.1, 0.01))
        c, a, b, n = best2
        print(f"{rid} {sp} tfit={tfit:.3f} n={n} K_{sp[0]}({sp[1]})={a:.2f} K_{sp[1]}({sp[0]})={b:.2f} chi2/n={c/n:.3f}")
    # B-B runs: single coupling K (both directions equal)
    bb_runs = ["2026-11-21/r1/lab-c/004", "2026-11-21/r2/lab-c/004", "2026-11-21/r2/lab-c/007"]
    for rid in bb_runs:
        setup, samples = load(rid)
        tfit = min(0.3, tmax_window(samples))
        best = None
        for k in frange(3.0, 5.0, 0.01):
            K = {("B", "B"): k}
            c, n = chi2(K, ("B", "B"), setup, samples, tfit)
            if best is None or c < best[0]:
                best = (c, k, n)
        c, k, n = best
        print(f"{rid} BB tfit={tfit:.3f} n={n} K_BB={k:.2f} chi2/n={c/n:.3f}")


if __name__ == "__main__":
    main()
