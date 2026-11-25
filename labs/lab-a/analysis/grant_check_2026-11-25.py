"""Radial-fall main event (r3/001-002): does the P-0027 table (P = 2.5) fit the whole pre-contact fall?

Compares, on the same samples:
  table  : K(r) = P-0027 full seven-node table, P = 2.5 (no free parameters)
  scale  : s * table(r) / r^2.5 with one free scale s (fit to the window)
  power  : K / r^P with K, P both free (fit to t <= 9.2 in score_round3_2026-11-25.py: P ~ 3.2)
Reports chi2/dof per time window (predictions propagated from t = 0; the replicate is the check).

Usage: python3 -I grant_check_2026-11-25.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

ROOT = sys.argv[1]
SIG = 0.05
H = 5e-3
NODES_R = np.array([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
NODES_K = np.array([17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624])


def table_k(r):
    return np.interp(r, NODES_R, NODES_K)


def load(n):
    base = os.path.join(ROOT, "results/2026-11-24/r3/lab-a", f"{n:03d}.json")
    reqp = os.path.join(ROOT, "requests/2026-11-24/r3/lab-a", f"{n:03d}.json")
    with open(base) as f:
        res = json.load(f)
    with open(reqp) as f:
        req = json.load(f)
    t = np.array([s["t"] for s in res["samples"]])
    X = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])]
                  for s in res["samples"]], float)
    p0 = np.array([p["pos"] for p in req["setup"]["particles"]], float)
    return t, X, p0


def sim(p0, kfun, P, times):
    x = p0.astype(float).copy()
    v = np.zeros_like(x)

    def acc(xx):
        d = xx[1] - xx[0]
        r = math.hypot(d[0], d[1])
        f = float(kfun(r)) / r ** P
        return np.array([f * d / r, -f * d / r])

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


def golden(fun, a, b, iters=30):
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


def main():
    windows = [(0.0, 3.0), (3.0, 6.0), (6.0, 8.0), (8.0, 9.2)]
    out = {}
    for n in (1, 2):
        t, X, p0 = load(n)
        keep = t <= 9.2
        t, X = t[keep], X[keep]
        M_tab = sim(p0, table_k, 2.5, t)
        # one free scale on the table shape: K = s * table_k(r)
        s_fit, c2_s = golden(lambda s: float(np.sum((sim(p0, lambda r, s=s: s * table_k(r), 2.5, t)[1:] - X[1:]) ** 2)) / SIG ** 2, 0.5, 2.0, iters=25)
        M_s = sim(p0, lambda r, s=s_fit: s * table_k(r), 2.5, t)
        rows = []
        for a, b in windows:
            m = (t > a) & (t <= b)
            c2_tab = float(np.sum((M_tab[m] - X[m]) ** 2) / SIG ** 2 / (4 * m.sum()))
            c2_sc = float(np.sum((M_s[m] - X[m]) ** 2) / SIG ** 2 / (4 * m.sum()))
            rows.append(dict(window=[a, b], n=int(m.sum()),
                             chi2_dof_table=round(c2_tab, 3), chi2_dof_scaled_table=round(c2_sc, 3)))
        # effective force ratio: free power law (P 3.2, K 55.4 from fall fit) vs table force at r
        rr = np.array([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
        ratio = (55.4 * rr ** -3.2) / (table_k(rr) * rr ** -2.5)
        out[f"r3-{n:03d}"] = dict(scale_s=round(s_fit, 4), chi2_dof_scaled_all=round(c2_s / (4 * len(t)), 3),
                                  windows=rows,
                                  force_ratio_powerlaw_over_table_at_r3_to_9=[round(float(x), 3) for x in ratio])
        print(f"run r3/{n:03d}")
        for r in rows:
            print("  ", r)
        print("   scale s =", round(s_fit, 4), " chi2/dof (all t<=9.2, scaled table) =", round(c2_s / (4 * len(t)), 3))
        print("   power-law / table force ratio at r=3..9:", out[f'r3-{n:03d}']['force_ratio_powerlaw_over_table_at_r3_to_9'])
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "grant_check_2026-11-25.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
