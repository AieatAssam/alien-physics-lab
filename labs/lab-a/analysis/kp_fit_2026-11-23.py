"""Joint K-P fit for A-A pairs at rest (P-0024 exponent test).

Model (per particle, equal masses): a_i = K * d / |d|^(P+1), d = x_j - x_i.
So |a| = K / r^P toward the partner. Initial velocities zero.
Integrator: RK4, dt = 1e-3 (finer than sample_dt, so sampling is exact at 0.001 grid).

For each P on a grid, K is fitted by 1-D search minimising SSE over all tracker
samples and both coordinates of every requested run. chi2 = SSE / sigma^2 with
sigma = 0.05 (tracker noise per coordinate, from notebook; not a fitted quantity).

Usage: python3 -I kp_fit_2026-11-23.py <repo_root> <req_dir_rel> <res_dir_rel> <nnn> [<nnn> ...]
"""
import json
import math
import os
import sys

SIGMA = 0.05


def load_run(repo, req_rel, res_rel, nnn):
    req = json.load(open(os.path.join(repo, req_rel, nnn + ".json")))
    res = json.load(open(os.path.join(repo, res_rel, nnn + ".json")))
    assert res["status"] == "ok", (nnn, res.get("reason"))
    parts = req["setup"]["particles"]
    pos0 = [tuple(p["pos"]) for p in parts]
    vel0 = [tuple(p["vel"]) for p in parts]
    samples = []
    for s in res["samples"]:
        byid = {p["id"]: p["pos"] for p in s["particles"]}
        samples.append((s["t"], [tuple(byid[i]) for i in range(len(parts))]))
    return {"id": nnn, "pos0": pos0, "vel0": vel0, "samples": samples,
            "dur": req["setup"]["duration"], "dt_s": req["setup"]["sample_dt"]}


def accel(x, K, P):
    (x0, y0), (x1, y1) = x
    dx, dy = x1 - x0, y1 - y0
    r = math.hypot(dx, dy)
    f = K / r ** (P + 1)
    return [(f * dx, f * dy), (-f * dx, -f * dy)]


def simulate(run, K, P, h=1e-3):
    """Return positions at each sample time (RK4 with step h, samples on the grid)."""
    x = [list(p) for p in run["pos0"]]
    v = [list(p) for p in run["vel0"]]
    out = {}
    targets = {round(t, 9): None for t, _ in run["samples"]}
    n_steps = int(round(run["dur"] / h))
    tgrid = {round(i * h, 9): i for i in range(n_steps + 1)}
    out[0.0] = [tuple(p) for p in x]
    t = 0.0
    for step in range(n_steps):
        def f(xx):
            return accel([tuple(p) for p in xx], K, P)
        a1 = f(x)
        x2 = [[x[i][c] + 0.5 * h * v[i][c] for c in range(2)] for i in range(2)]
        v2 = [[v[i][c] + 0.5 * h * a1[i][c] for c in range(2)] for i in range(2)]
        a2 = f(x2)
        x3 = [[x[i][c] + 0.5 * h * v2[i][c] for c in range(2)] for i in range(2)]
        v3 = [[v[i][c] + 0.5 * h * a2[i][c] for c in range(2)] for i in range(2)]
        a3 = f(x3)
        x4 = [[x[i][c] + h * v3[i][c] for c in range(2)] for i in range(2)]
        v4 = [[v[i][c] + h * a3[i][c] for c in range(2)] for i in range(2)]
        a4 = f(x4)
        for i in range(2):
            for c in range(2):
                x[i][c] += h / 6 * (v[i][c] + 2 * v2[i][c] + 2 * v3[i][c] + v4[i][c])
                v[i][c] += h / 6 * (a1[i][c] + 2 * a2[i][c] + 2 * a3[i][c] + a4[i][c])
        t = (step + 1) * h
        key = round(t, 9)
        if key in targets:
            out[key] = [tuple(p) for p in x]
    return out


def sse_run(run, K, P):
    traj = simulate(run, K, P)
    s = 0.0
    for t, obs in run["samples"]:
        pred = traj[round(t, 9)]
        for i in range(2):
            for c in range(2):
                s += (obs[i][c] - pred[i][c]) ** 2
    return s


def sse_all(runs, K, P):
    return sum(sse_run(r, K, P) for r in runs)


def best_K(runs, P, lo=1.0, hi=40.0):
    """Golden-section search on K (SSE is unimodal in K over this range)."""
    gr = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = sse_all(runs, c, P), sse_all(runs, d, P)
    for _ in range(40):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = sse_all(runs, c, P)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = sse_all(runs, d, P)
    K = 0.5 * (a + b)
    return K, sse_all(runs, K, P)


def main():
    repo, req_rel, res_rel = sys.argv[1], sys.argv[2], sys.argv[3]
    nnns = sys.argv[4:]
    runs = [load_run(repo, req_rel, res_rel, n) for n in nnns]
    n_points = sum(len(r["samples"]) for r in runs) * 4
    print("runs", nnns, "data points", n_points)
    grid = [round(0.80 + 0.02 * i, 3) for i in range(0, 101)]  # P in [0.80, 2.80]
    prof = {}
    for P in grid:
        K, s = best_K(runs, P)
        prof[P] = (K, s / SIGMA ** 2)
        print(f"P={P:.2f}  K={K:.4f}  chi2={s / SIGMA ** 2:.2f}")
    Pbest = min(prof, key=lambda p: prof[p][1])
    chi_best = prof[Pbest][1]
    print("best P", Pbest, "K", round(prof[Pbest][0], 4), "chi2", round(chi_best, 2))
    for Pc in (2.10, 2.50):
        if Pc in prof:
            print(f"P={Pc}: K={prof[Pc][0]:.4f} chi2={prof[Pc][1]:.2f} dchi2 vs best={prof[Pc][1] - chi_best:.2f}")
    # 1-sigma band on P: dchi2 <= 1
    ok = [p for p in prof if prof[p][1] - chi_best <= 1.0]
    print("P 1-sigma band (dchi2<=1):", min(ok), max(ok))
    print("reduced chi2 at best:", round(chi_best / n_points, 4))


if __name__ == "__main__":
    main()
