"""Score lab-a round 2, 2026-11-24 (results r2/001-012). Rules were written before the results.

- 001-007: off-node A-A K(r) at P = 2.5. Per-run K fit (two-body, equal masses, RK4, sigma 0.05,
  zero initial velocity). Compared with the linear interpolation of the P-0027 nodes.
  Node passes if |K_fit - K_pred| / K_pred <= 2 % (and replicate spread < 3 % where two runs exist).
  Node fails if it misses by more than 4 %.
- 008-009: crowd-8 ring at T = 1.0. chi2/dof (sigma 0.05) of the pairwise table-K model and the
  pairwise constant-K 17.7 model. Table passes if chi2/dof <= 1.5. Prefer table if
  chi2(const) - chi2(table) > 9 per run.
- 010-012: P-0026 (lab-keystone) review runs. Judge-style RMSE/L of papers/P-0026/model.py predict()
  against each run. Bar 3 x 0.007 = 0.021. Replicated if >= 3 in-domain runs pass.

Usage: python3 -I score_round2_2026-11-24.py <repo_root> <out_json>
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

ROOT = sys.argv[1]
OUT_JSON = sys.argv[2]
RES = os.path.join(ROOT, "results/2026-11-24/r2/lab-a")
REQ = os.path.join(ROOT, "requests/2026-11-24/r2/lab-a")
L = 10.0
SIG = 0.05
H = 2e-3

# P-0027 table (17.683 at 3 ... 11.624 at 9), linear between nodes.
NODES_R = np.array([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
NODES_K = np.array([17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624])
TABLE_K = lambda r: float(np.interp(r, NODES_R[[0, 2, 4, 6]], NODES_K[[0, 2, 4, 6]]))


def load(n):
    with open(os.path.join(RES, f"{n:03d}.json")) as f:
        res = json.load(f)
    with open(os.path.join(REQ, f"{n:03d}.json")) as f:
        req = json.load(f)
    t = np.array([s["t"] for s in res["samples"]])
    X = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])]
                  for s in res["samples"]], float)
    p0 = np.array([p["pos"] for p in req["setup"]["particles"]], float)
    return req, res, t, X, p0


def pair_sim(p0, K, times, P=2.5):
    x = p0.copy()
    v = np.zeros((2, 2))

    def acc(xx):
        d = xx[1] - xx[0]
        r = math.hypot(d[0], d[1])
        f = K / r ** (P + 1)
        return np.array([f * d, -f * d])

    out = np.zeros((len(times), 2, 2))
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


def chi2_pair(K, p0, t, X):
    M = pair_sim(p0, K, t)
    return float(np.sum((M[1:] - X[1:]) ** 2) / SIG ** 2)


def fit_K_pair(p0, t, X):
    lo, hi = 5.0, 40.0
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = chi2_pair(c, p0, t, X), chi2_pair(d, p0, t, X)
    for _ in range(40):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a); fc = chi2_pair(c, p0, t, X)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a); fd = chi2_pair(d, p0, t, X)
    K = (a + b) / 2
    return K, chi2_pair(K, p0, t, X) / (4 * (len(t) - 1))


def many_sim(p0, kfun, times, P=2.5):
    """Pairwise central force sum, all at rest, no walls (ring stays inside the chamber)."""
    x = p0.copy()
    v = np.zeros_like(x)
    n = len(x)

    def acc(xx):
        a = np.zeros_like(xx)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                d = xx[j] - xx[i]
                r = math.hypot(d[0], d[1])
                a[i] += kfun(r) / r ** P * d / r
        return a

    out = np.zeros((len(times), n, 2))
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


def load_model(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    out = {"offnode": [], "crowd8": [], "P0026_review": []}

    # ---- off-node K, 001-007 --------------------------------------------------------
    print("== Off-node A-A K, P = 2.5 (r2/001-007) ==")
    for n in range(1, 8):
        req, res, t, X, p0 = load(n)
        K, c2 = fit_K_pair(p0, t, X)
        sep = math.dist(p0[0], p0[1])
        kp = TABLE_K(sep)
        rel = (K - kp) / kp
        out["offnode"].append(dict(run=f"2026-11-24/r2/lab-a/{n:03d}", sep=round(sep, 4),
                                   T=req["setup"]["duration"], purpose=req["purpose"],
                                   K_fit=round(K, 4), chi2_per_dof=round(c2, 4),
                                   K_pred_table=round(kp, 4), rel_dev=round(rel, 5)))
        print(f"{n:03d} sep {sep:.3f} T {req['setup']['duration']} K_fit {K:.4f} "
              f"pred {kp:.4f} dev {100 * rel:+.2f}%  chi2/dof {c2:.3f}")

    # replicate spread: 004 vs 005 (sep 6.5, horizontal vs diagonal);
    k4 = out["offnode"][3]["K_fit"]
    k5 = out["offnode"][4]["K_fit"]
    print(f"replicate 004 vs 005 (sep 6.5): spread {100 * abs(k4 - k5) / ((k4 + k5) / 2):.2f}%")
    out["replicate_6p5_spread_pct"] = round(100 * abs(k4 - k5) / ((k4 + k5) / 2), 3)

    # ---- crowd-8 ring, 008-009 ------------------------------------------------------
    print("\n== Crowd-8 ring T = 1.0 (r2/008-009) ==")
    for n in (8, 9):
        req, res, t, X, p0 = load(n)
        Xt = many_sim(p0, TABLE_K, t)
        Xc = many_sim(p0, lambda r: 17.7, t)
        dof = 2 * X[1:].shape[1] * X[1:].shape[0]
        c2t = float(np.sum((Xt[1:] - X[1:]) ** 2) / SIG ** 2) / dof
        c2c = float(np.sum((Xc[1:] - X[1:]) ** 2) / SIG ** 2) / dof
        dmin = min(math.dist(p0[i], p0[j]) for i in range(8) for j in range(i + 1, 8))
        diff = float(np.sum((Xc[1:] - X[1:]) ** 2) / SIG ** 2 - np.sum((Xt[1:] - X[1:]) ** 2) / SIG ** 2)
        out["crowd8"].append(dict(run=f"2026-11-24/r2/lab-a/{n:03d}", min_initial_pair=round(dmin, 4),
                                  chi2_dof_table=round(c2t, 4), chi2_dof_constK=round(c2c, 4),
                                  chi2_const_minus_table=round(diff, 3),
                                  rmse_over_L_table=round(math.sqrt(np.mean((Xt[1:] - X[1:]) ** 2)) / L, 5),
                                  rmse_over_L_constK=round(math.sqrt(np.mean((Xc[1:] - X[1:]) ** 2)) / L, 5)))
        print(f"{n:03d} min pair {dmin:.3f} chi2/dof table {c2t:.3f} constK {c2c:.3f} "
              f"(const - table) {diff:.2f}")

    # ---- P-0026 review, 010-012 -----------------------------------------------------
    print("\n== P-0026 (lab-keystone) judge-style RMSE/L (r2/010-012) ==")
    m26 = load_model(os.path.join(ROOT, "papers/P-0026/model.py"), "p0026")
    for n in (10, 11, 12):
        req, res, t, X, p0 = load(n)
        try:
            pred = m26.predict(req["setup"])
        except ValueError as ex:
            print(f"{n:03d} outside paper domain: {ex}")
            out["P0026_review"].append(dict(run=f"2026-11-24/r2/lab-a/{n:03d}", in_domain=False, err=str(ex)))
            continue
        PX = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in pred], float)
        m = min(len(PX), len(X))
        e = math.sqrt(np.mean((PX[:m] - X[:m]) ** 2)) / L
        dmin = min(math.dist(p0[i], p0[j]) for i in range(16) for j in range(i + 1, 16))
        dmax = max(math.dist(p0[i], p0[j]) for i in range(16) for j in range(i + 1, 16))
        out["P0026_review"].append(dict(run=f"2026-11-24/r2/lab-a/{n:03d}", in_domain=True,
                                        min_pair=round(dmin, 4), max_pair=round(dmax, 4),
                                        n_samples=[len(X), len(PX)], rmse_over_L=round(e, 5),
                                        pass_0021=bool(e <= 0.021)))
        print(f"{n:03d} min pair {dmin:.3f} max pair {dmax:.3f} samples {len(X)}/{len(PX)} "
              f"RMSE/L {e:.5f} {'<=0.021 PASS' if e <= 0.021 else '>0.021 FAIL'}")

    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=2)
        f.write("\n")
    print("\nwrote", OUT_JSON)


if __name__ == "__main__":
    main()
