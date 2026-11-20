#!/usr/bin/env python3
"""Round 3 (2026-11-20): coupling-scale fit of the P-0008 law on the short-range pair runs 004-007.

Run with: python3 -I scale_fit_short_range.py REPO_ROOT

Model: P-0008 pairwise law with every coefficient multiplied by s (a = s * COUP / r^2.5),
integrated with P-0008's own RK4 step, initial state from the request.
Data: measured separation |pos0 - pos1| per sample. Noise on a separation: 0.071.
Window: samples up to the time at which the s = 1 prediction reaches its minimum (the predicted
contact), for runs whose s = 1 prediction rebounds (004, 007). For 005 and 006 the window is the
whole run. Post-contact predicted motion is an integrator artefact of the singular force and is
excluded.
chi2(s) = sum (meas - pred(s))^2 / 0.071^2. The best s and its 1-sigma width come from a parabola
on s in {0.80 ... 1.10} (delta chi2 = 1).
This is a post-hoc window choice, made after the pre-registered windows were found to be
contaminated by the rebound. It is reported as such.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
SIGMA = 0.071
GRID = [round(0.60 + 0.02 * i, 2) for i in range(26)]  # 0.60 .. 1.10
SCALES_CHECK = GRID
H = 0.0005

spec = importlib.util.spec_from_file_location("p0008", REPO / "papers" / "P-0008" / "model.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
COUP0 = dict(mod.COUP)

RUNS = {
    "004": ("AA", 1.5, 0.4, 0.0002),
    "005": ("AC", 1.5, 0.4, 0.0002),
    "006": ("CC", 1.5, 0.4, 0.0002),
    "007": ("AA", 2.5, 1.0, 0.0005),
}


def sep(p):
    d = {q["id"]: q["pos"] for q in p}
    return math.dist(d[0], d[1])


def integrate(species, r0, T, dt, s):
    mod.COUP = {k: s * v for k, v in COUP0.items()}
    pos = [[5.0 - r0 / 2, 5.0], [5.0 + r0 / 2, 5.0]]
    vel = [[0.0, 0.0], [0.0, 0.0]]
    n = int(round(T / dt))
    t = 0.0
    out = {}
    for i in range(n + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = mod._step(pos, vel, species, h)
            t += h
        t = target
        out[f"{target:.4f}"] = math.dist(pos[0], pos[1])
    return out


def contact_cut(pr, T, floor=0.6):
    """Trust a prediction only until its separation first drops below `floor` (near-contact is where
    the singular 1/r^2.5 force makes the integrator unreliable). Rebound-independent."""
    for k in sorted(pr):
        if pr[k] < floor:
            return float(k)
    return T


def fit_parabola(xs, ys):
    """Least-squares quadratic through (xs, ys); returns vertex and curvature a."""
    m = len(xs)
    Sx = sum(xs); Sx2 = sum(x * x for x in xs); Sx3 = sum(x ** 3 for x in xs); Sx4 = sum(x ** 4 for x in xs)
    Sy = sum(ys); Sxy = sum(x * y for x, y in zip(xs, ys)); Sx2y = sum(x * x * y for x, y in zip(xs, ys))
    M = [[Sx4, Sx3, Sx2], [Sx3, Sx2, Sx], [Sx2, Sx, m]]
    v = [Sx2y, Sxy, Sy]

    def det(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
                - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    d = det(M)
    coef = []
    for col in range(3):
        mk = [row[:] for row in M]
        for i in range(3):
            mk[i][col] = v[i]
        coef.append(det(mk) / d)
    a, b, _c = coef
    return -b / (2 * a), a


def best_scale(window_pts, pair, r0, T, dt, grid, block_k=None):
    """Chi2 over the grid, each scale cut at its own predicted contact. Returns (s0, chi2/n at s=1, n)."""
    chis = []
    for s in grid:
        pr = integrate(list(pair), r0, T, dt, s)
        tcut = contact_cut(pr, T)
        c = 0.0
        n = 0
        for t, m in window_pts:
            if t > tcut + 1e-9:
                continue
            c += (m - pr[f"{round(t, 4):.4f}"]) ** 2
            n += 1
        chis.append(c / SIGMA ** 2 / max(n, 1))
    i0 = min(range(len(grid)), key=lambda i: chis[i])
    lo, hi = max(0, i0 - 3), min(len(grid), i0 + 4)
    s0, a = fit_parabola(grid[lo:hi], chis[lo:hi])
    return s0, chis


def main():
    for key, (pair, r0, T, dt) in RUNS.items():
        res = json.loads((REPO / "results" / "2026-11-20" / "r2" / "lab-c" / f"{key}.json").read_text())
        meas = [(s["t"], sep(s["particles"])) for s in res["samples"]]
        s0, chis = best_scale(meas, pair, r0, T, dt, GRID)
        pr1 = integrate(list(pair), r0, T, dt, 1.0)
        tcut1 = contact_cut(pr1, T)
        n1 = sum(1 for t, _ in meas if t <= tcut1 + 1e-9)
        # time-block jackknife (5 blocks over the run) for an honest width
        tmax = max(t for t, _ in meas)
        blocks = [[] for _ in range(5)]
        for t, m in meas:
            blocks[min(4, int(5 * t / (tmax + 1e-12)))].append((t, m))
        jk = []
        for b in range(5):
            rest = [pt for j in range(5) if j != b for pt in blocks[j]]
            sb, _ = best_scale(rest, pair, r0, T, dt, GRID)
            jk.append(sb)
        mj = sum(jk) / 5
        se = math.sqrt(4 / 5 * sum((x - mj) ** 2 for x in jk))
        i1 = SCALES_CHECK.index(1.0) if 1.0 in SCALES_CHECK else None
        print(f"{key} {pair} r0={r0} T={T}  cut at s=1: t<={tcut1:.4f} (n={n1})  "
              f"best s={s0:.3f}  jackknife SE={se:.3f}")
        print("    chi2/n by s: " + "  ".join(f"{s:.2f}:{c:.2f}" for s, c in zip(GRID, chis)))


if __name__ == "__main__":
    main()
