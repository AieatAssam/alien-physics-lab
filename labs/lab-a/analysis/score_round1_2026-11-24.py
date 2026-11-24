"""Score lab-a round 1, 2026-11-24 (results r1/001-020).

- 001-008: judge-style RMSE/L of papers/P-0025/model.py predict() against each run (review of P-0025).
- 009-018: per-run K fit for A-A at P = 2.5 (two-body, equal masses, RK4 h = 2e-3, sigma 0.05,
  initial positions from the request setup, zero initial velocity). Sep 3..9 table.
- 019-020: crowd-8 ring. RMSE/L of (a) pairwise table-K model (K(r) nodes 3,5,7,9 from H30) and
  (b) pairwise constant K = 17.7 model. Also judged error for P-0003 model on 009-010.

Usage: python3 -I score_round1_2026-11-24.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

ROOT = sys.argv[1]
RES = os.path.join(ROOT, "results/2026-11-24/r1/lab-a")
REQ = os.path.join(ROOT, "requests/2026-11-24/r1/lab-a")
L = 10.0
SIG = 0.05
H = 2e-3


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


def load_model(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def judge_rmse_over_L(pred_X, meas_X):
    d = pred_X - meas_X
    return float(math.sqrt(np.mean(d ** 2)) / L)


def pair_sim(p0, K, times, P=2.5):
    """Two-body equal-mass central force K/r^P, at rest; positions at times."""
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


NODES_R = np.array([3.0, 5.0, 7.0, 9.0])
NODES_K = np.array([17.68, 17.83, 15.12, 11.62])


def many_sim(p0, kfun, times, P=2.5):
    """N-body pairwise central force sum, all at rest, no walls (crowd check only)."""
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


def main():
    out = {}

    # ---- P-0025 review runs 001-008 -------------------------------------------------
    m25 = load_model(os.path.join(ROOT, "papers/P-0025/model.py"), "p0025")
    print("== P-0025 (lab-b) judge-style RMSE/L, runs 001-008 ==")
    rows25 = []
    for n in range(1, 9):
        req, res, t, X, p0 = load(n)
        pred = m25.predict(req["setup"])
        PX = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in pred], float)
        m = min(len(PX), len(X))
        e = judge_rmse_over_L(PX[:m], X[:m])
        r0 = math.dist(p0[0], p0[1])
        sp = "".join(p["species"] for p in req["setup"]["particles"])
        rows25.append(dict(run=f"2026-11-24/r1/lab-a/{n:03d}", r0=round(r0, 4), species=sp,
                           orient=req["purpose"], n_samples=[len(X), len(PX)], rmse_over_L=round(e, 5),
                           pass_21=e <= 0.021))
        print(f"{n:03d} r0 {r0:.4f} {sp} samples {len(X)}/{len(PX)} RMSE/L {e:.5f} "
              f"{'<=0.021' if e <= 0.021 else '>0.021'}  | {req['purpose'][:70]}")
    out["P0025_review"] = rows25

    # ---- A-A K(r) table, runs 009-018 -----------------------------------------------
    print("\n== A-A per-run K fit, P = 2.5 (runs 009-018) ==")
    m3 = load_model(os.path.join(ROOT, "papers/P-0003/model.py"), "p0003") if os.path.exists(
        os.path.join(ROOT, "papers/P-0003/model.py")) else None
    rows_k = []
    for n in range(9, 19):
        req, res, t, X, p0 = load(n)
        K, c2 = fit_K_pair(p0, t, X)
        r0 = math.dist(p0[0], p0[1])
        orient = "horizontal" if abs(p0[0, 1] - p0[1, 1]) < 1e-9 else "diagonal"
        rows_k.append(dict(run=f"2026-11-24/r1/lab-a/{n:03d}", r0=round(r0, 4), T=req["setup"]["duration"],
                           orient=orient, K=round(K, 4), chi2_per_dof=round(c2, 4)))
        print(f"{n:03d} sep {r0:.3f} T {req['setup']['duration']} {orient:10s} K {K:.4f} chi2/dof {c2:.3f}")
        if n in (9, 10) and m3 is not None:
            try:
                pr = m3.predict(req["setup"])
                PX = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in pr], float)
                mm = min(len(PX), len(X))
                print(f"     P-0003 model judged RMSE/L {judge_rmse_over_L(PX[:mm], X[:mm]):.5f}")
            except Exception as ex:  # own-paper check only, not a review
                print("     P-0003 model not evaluated:", ex)
    out["AA_K_fits"] = rows_k

    # ---- Crowd-8 ring, runs 019-020 -------------------------------------------------
    print("\n== Crowd-8 ring (runs 019-020) ==")
    rows_c = []
    for n in (19, 20):
        req, res, t, X, p0 = load(n)
        Xt = many_sim(p0, lambda r: float(np.interp(r, NODES_R, NODES_K)), t)
        Xc = many_sim(p0, lambda r: 17.7, t)
        e_t = judge_rmse_over_L(Xt[1:], X[1:])
        e_c = judge_rmse_over_L(Xc[1:], X[1:])
        dmin = min(math.dist(p0[i], p0[j]) for i in range(8) for j in range(i + 1, 8))
        rows_c.append(dict(run=f"2026-11-24/r1/lab-a/{n:03d}", table_RMSE_over_L=round(e_t, 5),
                           constK_RMSE_over_L=round(e_c, 5), min_initial_pair=round(dmin, 4)))
        print(f"{n:03d} table-K RMSE/L {e_t:.5f}   constK(17.7) RMSE/L {e_c:.5f}")
    # Replicate agreement of the two ring runs (noise-only check)
    _, _, t19, X19, _ = load(19)
    _, _, t20, X20, _ = load(20)
    rep = judge_rmse_over_L(X19[1:], X20[1:])
    print(f"ring run 019 vs 020 RMSE/L (replicate spread) {rep:.5f}")
    out["crowd8"] = rows_c
    out["crowd8_replicate_spread"] = round(rep, 5)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "score_round1_2026-11-24.json"), "w") as f:
        json.dump(out, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
