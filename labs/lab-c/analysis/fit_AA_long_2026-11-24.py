#!/usr/bin/env python3
"""A-A pair at rest, centre (5,5), horizontal, T = 6 (runs 2026-11-24/r2/lab-c/002-004).

Model: each particle accelerates toward the other with K / r^P (relative accel 2K/r^P).
Symmetric 1-D relative motion r(t), r(0) = r0, v(0) = 0; centre fixed at 5.
Fit window: samples with measured separation >= 3.0 (same rule as the A-B map).
Noise: tracker sigma = 0.05 per coordinate (assumed). chi2/n uses sigma = 0.05.
Run with: python3 -I fit_AA_long_2026-11-24.py REPO_ROOT
"""
import json, math, sys
from pathlib import Path

REPO = Path(sys.argv[1])
RIDS = ["002", "003", "004"]
SIG = 0.05
R_MIN = 3.0


def load(nnn):
    req = json.loads((REPO / "requests/2026-11-24/r2/lab-c" / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results/2026-11-24/r2/lab-c" / f"{nnn}.json").read_text())
    return req, res


def traj_r(r0, K, P, times, h=0.0005):
    """Relative separation r(t) by RK4 on r'' = -2K / r^P, r'(0)=0."""
    out = {}
    r, v, t = r0, 0.0, 0.0
    tmax = max(times)
    targets = sorted(times)
    idx = 0
    while idx < len(targets) and targets[idx] <= 0.0:
        out[targets[idx]] = r; idx += 1
    def f(rr): return -2.0 * K / max(rr, 1e-3) ** P
    while idx < len(targets):
        # step, but land exactly on next target
        tn = targets[idx]
        while t < tn - 1e-12:
            step = min(h, tn - t)
            k1r, k1v = v, f(r)
            r2, v2 = r + step / 2 * k1r, v + step / 2 * k1v
            k2r, k2v = v2, f(r2)
            r3, v3 = r + step / 2 * k2r, v + step / 2 * k2v
            k3r, k3v = v3, f(r3)
            r4, v4 = r + step * k3r, v + step * k3v
            k4r, k4v = v4, f(r4)
            r += step / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
            v += step / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            t += step
            if r <= 0.05:
                return None
        out[tn] = r; idx += 1
    return out


def residual_sum(data, K, P):
    se = 0.0; n = 0
    times = [s["t"] for s in data["samples"] if s["t"] > 0]
    rt = traj_r(data["r0"], K, P, times)
    if rt is None:
        return None, 0
    for s in data["samples"]:
        if s["t"] <= 0:
            continue
        x = [p["pos"] for p in s["particles"]]
        r_meas = math.dist(x[0], x[1])
        if r_meas < R_MIN:
            continue
        half = rt[s["t"]] / 2
        # predicted: x0 = 5 - half, x1 = 5 + half along x, centre fixed at the designed (5,5)
        pred0 = (5.0 - half, 5.0)
        pred1 = (5.0 + half, 5.0)
        for k, pp in ((0, pred0), (1, pred1)):
            for c in range(2):
                se += (x[k][c] - pp[c]) ** 2; n += 1
    return se, n


def fit_K(data, P):
    lo, hi = 1.0, 60.0
    def cost(K):
        se, n = residual_sum(data, K, P)
        return float("inf") if se is None else se
    # coarse scan then golden section
    grid = [lo + i * (hi - lo) / 240 for i in range(241)]
    vals = [cost(K) for K in grid]
    i = min(range(len(grid)), key=lambda j: vals[j])
    a, b = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    gr = (math.sqrt(5) - 1) / 2
    c_, d_ = b - gr * (b - a), a + gr * (b - a)
    fc, fd = cost(c_), cost(d_)
    for _ in range(80):
        if fc < fd:
            b, d_, fd = d_, c_, fc
            c_ = b - gr * (b - a); fc = cost(c_)
        else:
            a, c_, fc = c_, d_, fd
            d_ = a + gr * (b - a); fd = cost(d_)
    K = (a + b) / 2
    se, n = residual_sum(data, K, P)
    return K, se, n


runs = []
for nnn in RIDS:
    req, res = load(nnn)
    p = req["setup"]["particles"]
    r0 = math.dist(p[0]["pos"], p[1]["pos"])
    # window: keep samples up to (excluding) the first one with measured separation < R_MIN
    keep = []
    for smp in res["samples"]:
        x = [q["pos"] for q in smp["particles"]]
        if math.dist(x[0], x[1]) < R_MIN:
            break
        keep.append(smp)
    print(f"{nnn}: window t <= {keep[-1]['t']:.2f} ({len(keep)} samples of {len(res['samples'])})")
    runs.append({"rid": nnn, "r0": r0, "samples": keep})

print("Per-run fit at fixed P (window r >= 3):")
for P in (2.5, 2.9, 3.0, 3.1):
    print(f"P = {P}")
    for d in runs:
        K, se, n = fit_K(d, P)
        print(f"  {d['rid']} r0={d['r0']:.2f}  K={K:.3f}  n={n}  chi2/n={se/(SIG*SIG)/n:.3f}")

print("\nJoint fit (one K across the three runs) vs P:")
best = None
for P100 in range(250, 321, 5):
    P = P100 / 100
    tot_se = 0.0; tot_n = 0; Ks = []
    # joint K: scan K minimising total SSE
    def cost(K):
        s = 0.0
        for d in runs:
            se, n = residual_sum(d, K, P)
            if se is None:
                return float("inf")
            s += se
        return s
    grid = [5 + i * 0.25 for i in range(0, 221)]
    vals = [cost(K) for K in grid]
    i = min(range(len(grid)), key=lambda j: vals[j])
    a, b = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    gr = (math.sqrt(5) - 1) / 2
    c_, d_ = b - gr * (b - a), a + gr * (b - a)
    fc, fd = cost(c_), cost(d_)
    for _ in range(60):
        if fc < fd:
            b, d_, fd = d_, c_, fc; c_ = b - gr * (b - a); fc = cost(c_)
        else:
            a, c_, fc = c_, d_, fd; d_ = a + gr * (b - a); fd = cost(d_)
    K = (a + b) / 2
    tot = cost(K)
    n_tot = sum(residual_sum(d, K, P)[1] for d in runs)
    chi2n = tot / (SIG * SIG) / n_tot
    print(f"  P={P:.2f}  K_joint={K:.3f}  chi2/n={chi2n:.4f}  n={n_tot}")
