"""Score lab-a round 3 of 2026-11-24 (results r3/001-006) and recheck round 2 (r2/001-002).

Pre-registered rules (written 2026-11-24 in NOTEBOOK.md, before these results):
  1. Replicates r3/003-004 vs r2/001-002: table holds if K_fit within 2 % of the table value at
     3.5 and 4.5; narrow P-0027 to [5, 9] if both replicate high (> 17.9 at 3.5, > 18.0 at 4.5).
  2. Crowd-8 octagon r3/005-006: table pairwise chi2/dof <= 1.5 and table beats constant K by > 9 per run.
  3. Radial-fall main event r3/001-002: K(r) fit by windows over the pre-contact trajectory with no
     assumed exponent; compare replicates; report whether P = 2.5 is consistent.

Correction (this session): the round-2 scorer (score_round2_2026-11-24.py) built its table with
np.interp over nodes 3, 5, 7, 9 only. The table used here is the full seven-node piecewise-linear
table P-0027 (17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624 at r = 3..9), which is what
the round-2 request notes used (17.692 at 3.5, 17.768 at 4.5). Round 2 is rescored below.

Pre-contact cut: measured separation > 2.0 (about t <= 9.2 in both replicates; contact near t ~ 9.5).

Usage: python3 -I score_round3_2026-11-25.py <repo_root> <out_json>
"""
import json
import math
import os
import sys

import numpy as np

ROOT = sys.argv[1]
OUT_JSON = sys.argv[2]
L = 10.0
SIG = 0.05

NODES_R = np.array([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
NODES_K = np.array([17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624])


def table_k(r):
    return np.interp(r, NODES_R, NODES_K)  # clamps outside [3, 9]


def const_k(r):
    return np.full_like(np.asarray(r, float), 17.7)


def load(day, rnd, n):
    base = os.path.join(ROOT, "results", day, f"r{rnd}", "lab-a", f"{n:03d}.json")
    reqp = os.path.join(ROOT, "requests", day, f"r{rnd}", "lab-a", f"{n:03d}.json")
    with open(base) as f:
        res = json.load(f)
    with open(reqp) as f:
        req = json.load(f)
    t = np.array([s["t"] for s in res["samples"]])
    X = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])]
                  for s in res["samples"]], float)
    p0 = np.array([p["pos"] for p in req["setup"]["particles"]], float)
    return req, t, X, p0


def sim(p0, kfun, P, times, H):
    """N-body central pair force f = K(r)/r^P along the separation (attractive), all at rest, no walls."""
    x = p0.astype(float).copy()
    v = np.zeros_like(x)

    def acc(xx):
        d = xx[None, :, :] - xx[:, None, :]          # d[i, j] = x_j - x_i
        r = np.sqrt((d ** 2).sum(-1))
        np.fill_diagonal(r, 1.0)
        f = kfun(r) / r ** P
        np.fill_diagonal(f, 0.0)
        return (f[:, :, None] * d / r[:, :, None]).sum(axis=1)

    out = np.zeros((len(times), len(x), 2))
    t = 0.0
    for i, tt in enumerate(times):
        while t < tt - 1e-12:
            h = min(H, tt - t)
            a1 = acc(x); x2 = x + h / 2 * v; v2 = v + h / 2 * a1
            a2 = acc(x2); x3 = x + h / 2 * v2; v3 = v + h / 2 * a2
            a3 = acc(x3); x4 = x + h * v3; v4 = v + h * a3
            a4 = acc(x4)
            x = x + h / 6 * (v + 2 * v2 + 2 * v3 + v4)
            v = v + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
            t += h
        out[i] = x
    return out


def golden(fun, a, b, iters=40):
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = fun(c), fun(d)
    for _ in range(iters):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a); fc = fun(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a); fd = fun(d)
    x = (a + b) / 2
    return x, fun(x)


def chi2_dof(M, X, n_par, n_samp, n_part):
    """Chi2 per dof over samples t > 0 (sigma 0.05, two coordinates per particle)."""
    c2 = float(np.sum((M[1:] - X[1:]) ** 2) / SIG ** 2)
    dof = 2 * n_part * (n_samp - 1) - n_par
    return c2, c2 / dof


# ---------------------------------------------------------------- 1. replicates of the rule-1 nodes
def pair_K_fit(day, rnd, n, H=2e-3):
    req, t, X, p0 = load(day, rnd, n)
    fun = lambda K: chi2_dof(sim(p0, lambda r, K=K: K + 0 * r, 2.5, t, H), X, 1, len(t), 2)[0]
    K, c2 = golden(fun, 5.0, 40.0)
    sep = math.dist(p0[0], p0[1])
    return dict(run=f"{day}/r{rnd}/lab-a/{n:03d}", sep=round(sep, 4), T=req["setup"]["duration"],
                orient="horiz" if abs(p0[0][1] - p0[1][1]) < 1e-9 else "diag",
                K_fit=round(K, 4), chi2_per_dof=round(c2 / (4 * (len(t) - 1)), 4),
                table_K=round(float(table_k(sep)), 4),
                dev_pct=round(100 * (K - float(table_k(sep))) / float(table_k(sep)), 2))


def replicates():
    rows = []
    for day, rnd, n in [("2026-11-24", 2, 1), ("2026-11-24", 2, 2), ("2026-11-24", 3, 3), ("2026-11-24", 3, 4)]:
        rows.append(pair_K_fit(day, rnd, n))
    return rows


# ---------------------------------------------------------------- 2. crowd-8 octagon
def octagon():
    rows = []
    for n in (5, 6):
        req, t, X, p0 = load("2026-11-24", 3, n)
        M_tab = sim(p0, table_k, 2.5, t, 2e-3)
        M_con = sim(p0, const_k, 2.5, t, 2e-3)
        c2_tab, r_tab = chi2_dof(M_tab, X, 0, len(t), len(p0))
        c2_con, r_con = chi2_dof(M_con, X, 0, len(t), len(p0))
        rmse_tab = float(np.sqrt(np.mean((M_tab[1:] - X[1:]) ** 2)) / L)
        rmse_con = float(np.sqrt(np.mean((M_con[1:] - X[1:]) ** 2)) / L)
        pair = np.linalg.norm(X[:, :, None, :] - X[:, None, :, :], axis=-1)
        iu = np.triu_indices(len(p0), 1)
        min_pair_meas = float(pair[:, iu[0], iu[1]].min())
        rows.append(dict(run=f"2026-11-24/r3/lab-a/{n:03d}", N=len(p0), T=req["setup"]["duration"],
                         chi2_table=round(c2_tab, 1), chi2_dof_table=round(r_tab, 4),
                         chi2_const=round(c2_con, 1), chi2_dof_const=round(r_con, 4),
                         chi2_const_minus_table_per_run=round((c2_con - c2_tab), 1),
                         rmse_over_L_table=round(rmse_tab, 5), rmse_over_L_const=round(rmse_con, 5),
                         min_measured_pair=round(min_pair_meas, 3)))
    return rows


# ---------------------------------------------------------------- 3. radial-fall main event
def fall_fit(day, rnd, n, t_cut, H=1e-2):
    req, t, X, p0 = load(day, rnd, n)
    keep = t <= t_cut
    tt, XX = t[keep], X[keep]

    def best_K(P):
        fun = lambda K: chi2_dof(sim(p0, lambda r, K=K: K + 0 * r, P, tt, H), XX, 1, len(tt), 2)[0]
        return golden(fun, 1.0, 100.0, iters=30)

    # profile over P with K optimised at each P
    Pbest, _ = golden(lambda P: best_K(P)[1], 1.5, 3.5, iters=22)
    Kbest, c2best = best_K(Pbest)
    K25, c225 = best_K(2.5)
    n_dof = 4 * len(tt) - 2
    return dict(run=f"{day}/r{rnd}/lab-a/{n:03d}", t_cut=t_cut, n_samples=int(len(tt)),
                free_P=round(Pbest, 3), free_K=round(Kbest, 3),
                free_chi2_per_dof=round(c2best / n_dof, 4),
                P25_K=round(K25, 3), P25_chi2_per_dof=round(c225 / n_dof, 4),
                delta_chi2_P25_minus_free=round(c225 - c2best, 2))


def windowed_fixed_P(day, rnd, n, cuts, P=2.5, H=1e-2):
    """K(P=2.5) per cumulative time window. Windows reveal drift of K with separation."""
    out = []
    req, t, X, p0 = load(day, rnd, n)
    for tc in cuts:
        keep = t <= tc
        tt, XX = t[keep], X[keep]
        fun = lambda K: chi2_dof(sim(p0, lambda r, K=K: K + 0 * r, P, tt, H), XX, 1, len(tt), 2)[0]
        K, c2 = golden(fun, 1.0, 100.0, iters=30)
        M = sim(p0, lambda r, K=K: K + 0 * r, P, tt, H)
        sep_end = float(np.linalg.norm(XX[-1, 0] - XX[-1, 1]))
        out.append(dict(run=f"{day}/r{rnd}/lab-a/{n:03d}", t_cut=tc, P=P, K_fit=round(K, 3),
                        chi2_per_dof=round(c2 / (4 * len(tt) - 2 + 1), 4),
                        measured_sep_at_cut=round(sep_end, 3)))
    return out


def main():
    result = {}
    print("== 1. replicates (table = full 7-node P-0027 table) ==")
    result["replicates"] = replicates()
    for r in result["replicates"]:
        print(r)

    print("== 2. crowd-8 octagon r3/005-006 ==")
    result["octagon"] = octagon()
    for r in result["octagon"]:
        print(r)

    print("== 3. radial fall r3/001-002 ==")
    falls = []
    for n in (1, 2):
        falls.append(fall_fit("2026-11-24", 3, n, t_cut=9.2))
        print(falls[-1])
    result["fall_free_P_fit_tcut9p2"] = falls
    cum = []
    for n in (1, 2):
        cum += windowed_fixed_P("2026-11-24", 3, n, cuts=[3.0, 6.0, 8.0, 9.2])
    result["fall_windows_P25"] = cum
    for c in cum:
        print(c)
    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=2)
    print("wrote", OUT_JSON)


if __name__ == "__main__":
    main()
