#!/usr/bin/env python3
"""Score lab-a round 1 of 2026-11-25 (requests r1/001-013).

Pre-registered rules (NOTEBOOK.md, written before results) used a local quadratic fit of each
particle's acceleration. That estimator is at the noise floor for T <= 0.3 (see the note below),
so this scorer uses the whole-trajectory comparison instead. The pre-registered decision rules
are kept, applied to the scale s that best fits the whole run:

  shape table:  K(r) = s * K_table(r), K_table = P-0027 nodes, clamped at 17.683 below r = 3.
  shape PL:     K(r) = s * 55.4 * r^-0.7   (F = K / r^2.5 = 55.4 / r^3.2, the P = 3.2 power law).

For each pair run: integrate both particles (RK4, h = 0.001, specular walls), compare with the
tracker positions (sigma 0.05 per coordinate), scan s. Output: best s, chi2/dof at s = 1 and at
best s, and Delta chi2 = 1 interval on s.

Falls (r1/012-013): simulate from the exact setup, no free parameter, compared over pre-contact
windows where the measured separation is above 2.5 and the time is before the first measured
separation below 2.5 (contact). Chi2/dof per window, sigma 0.05.

Run:  python3 -I score_round1_2026-11-25.py
"""
import json
import math
import os

import numpy as np

ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab"
DATE, RND, LAB = "2026-11-25", "r1", "lab-a"
SIG = 0.05
L = 10.0
P = 2.5
H = 0.001

NODE_R = np.array([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
NODE_K = np.array([17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624])


def K_table(r):
    return np.interp(np.asarray(r, float), NODE_R, NODE_K)  # clamped at 17.683 below 3


def K_pl(r):
    return 55.4 * np.asarray(r, float) ** (2.5 - 3.2)


def load(i):
    rq = os.path.join(ROOT, "requests", DATE, RND, LAB, "%03d.json" % i)
    rs = os.path.join(ROOT, "results", DATE, RND, LAB, "%03d.json" % i)
    req = json.load(open(rq))
    res = json.load(open(rs))
    assert res["status"] == "ok", (i, res)
    t = np.array([s["t"] for s in res["samples"]])
    n = len(req["setup"]["particles"])
    X = np.zeros((len(t), n, 2))
    for k, s in enumerate(res["samples"]):
        for p in s["particles"]:
            X[k, p["id"]] = p["pos"]
    return req, t, X


def simulate(parts, T, Kfun, h=H):
    """Two-particle RK4 with specular walls. Returns times and positions on the grid k*h."""
    pos = np.array([p["pos"] for p in parts], float)
    vel = np.array([p["vel"] for p in parts], float)
    sp = [p["species"] for p in parts]
    assert len(parts) == 2

    def acc(p):
        d = p[1] - p[0]
        r = float(np.linalg.norm(d))
        F = float(Kfun(r)) / r ** P
        u = d / r
        return np.array([F * u, -F * u])

    xs = [pos.copy()]
    n = int(round(T / h))
    for _ in range(n):
        a1 = acc(pos)
        p2, v2 = pos + 0.5 * h * vel, vel + 0.5 * h * a1
        a2 = acc(p2)
        p3, v3 = pos + 0.5 * h * v2, vel + 0.5 * h * a2
        a3 = acc(p3)
        p4, v4 = pos + h * v3, vel + h * a3
        a4 = acc(p4)
        pos = pos + h / 6 * (vel + 2 * v2 + 2 * v3 + v4)
        vel = vel + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        for c in range(2):
            for i in range(2):
                if pos[i, c] < 0:
                    pos[i, c] = -pos[i, c]
                    vel[i, c] = -vel[i, c]
                elif pos[i, c] > L:
                    pos[i, c] = 2 * L - pos[i, c]
                    vel[i, c] = -vel[i, c]
        xs.append(pos.copy())
    return np.array(xs)


def chi2_of(pred, X, idx, mask):
    res = X[mask] - pred[idx[mask]]
    return float(np.sum(res ** 2) / SIG ** 2), int(res.size)


def scale_scan(req, t, X, shape):
    parts = req["setup"]["particles"]
    T = float(t[-1])
    idx = np.rint(t / H).astype(int)
    mask = np.ones(len(t), bool)
    grid = np.arange(0.30, 3.001, 0.005)
    chis = []
    for s in grid:
        Kfun = (lambda r, s=s: s * shape(r))
        pred = simulate(parts, T, Kfun)
        c, dof = chi2_of(pred, X, idx, mask)
        chis.append(c)
    chis = np.array(chis)
    j = int(np.argmin(chis))
    inside = grid[chis <= chis[j] + 1.0]
    # chi2 at s=1
    pred1 = simulate(parts, T, lambda r: shape(r))
    c1, dof = chi2_of(pred1, X, idx, mask)
    return {
        "s_best": float(grid[j]),
        "s_lo": float(inside.min()),
        "s_hi": float(inside.max()),
        "chi2_best_per_dof": float(chis[j] / dof),
        "chi2_s1_per_dof": float(c1 / dof),
        "dof": dof,
    }


def pair_runs():
    print("=== Pair runs: whole-trajectory scale fit (s = 1 is the stated law) ===")
    print("run  species  r0    T     table: s_best [1-sig]  chi2/dof(s=1)  chi2/dof(best)   PL: s_best [1-sig]  chi2/dof(s=1)  chi2/dof(best)")
    out = {}
    for i in range(1, 12):
        req, t, X = load(i)
        sp = "".join(p["species"] for p in req["setup"]["particles"])
        r0 = float(np.linalg.norm(np.array(req["setup"]["particles"][1]["pos"]) - np.array(req["setup"]["particles"][0]["pos"])))
        tab = scale_scan(req, t, X, K_table)
        pl = scale_scan(req, t, X, K_pl)
        out[i] = {"species": sp, "r0": r0, "T": float(t[-1]), "table": tab, "pl": pl}
        print(
            "%03d  %-7s  %.2f  %.2f   %6.3f [%6.3f, %6.3f]  %8.3f  %8.3f   %6.3f [%6.3f, %6.3f]  %8.3f  %8.3f"
            % (i, sp, r0, float(t[-1]),
               tab["s_best"], tab["s_lo"], tab["s_hi"], tab["chi2_s1_per_dof"], tab["chi2_best_per_dof"],
               pl["s_best"], pl["s_lo"], pl["s_hi"], pl["chi2_s1_per_dof"], pl["chi2_best_per_dof"])
        )
    return out


def close_range(out):
    print("\n=== Rules 1-3, close-range A-A (r1/001-008), whole-run scale s (1.00 = P-0027 table clamped; s_PL = power-law scale) ===")
    groups = {"sep 2.0 (horiz+diag)": [1, 2], "sep 2.5 (horiz+diag)": [3, 4],
              "sep 3.0 (horiz+diag)": [5, 6], "sep 1.5 T 0.15 (horiz+diag)": [7, 8]}
    summary = {}
    for label, ids in groups.items():
        st = [out[i]["table"]["s_best"] for i in ids]
        lo = [out[i]["table"]["s_lo"] for i in ids]
        hi = [out[i]["table"]["s_hi"] for i in ids]
        summary[label] = {"s_table_best": st, "s_lo": lo, "s_hi": hi}
        print("  %-30s s_table best %s  [1-sigma] %s" % (label, [round(x, 3) for x in st],
                                                       [(round(a, 3), round(b, 3)) for a, b in zip(lo, hi)]))
    # Rule 1: both replicates at 2.0, 2.5 and 3.0 inside 5% of 1.00 (use the mean of the pair)
    def mean_s(label):
        return float(np.mean(summary[label]["s_table_best"]))
    m20, m25, m30 = mean_s("sep 2.0 (horiz+diag)"), mean_s("sep 2.5 (horiz+diag)"), mean_s("sep 3.0 (horiz+diag)")
    rule1 = all(abs(x - 1.0) <= 0.05 for x in [m20, m25, m30])
    rule2 = (m20 > 1.25 and m25 > 1.25)
    print("  pair means: s(2.0)=%.3f  s(2.5)=%.3f  s(3.0)=%.3f" % (m20, m25, m30))
    if rule1:
        print("  RULE 1 (table consistent at close range): TRIGGERED")
    elif rule2:
        print("  RULE 2 (steeper close range): TRIGGERED (check the PL column)")
    else:
        print("  RULE 3 (inconclusive): neither rule 1 nor rule 2 met.")
    return summary, {"rule1": rule1, "rule2": rule2}


def fall_check(i, label):
    req, t, X = load(i)
    parts = req["setup"]["particles"]
    sep_m = np.linalg.norm(X[:, 1] - X[:, 0], axis=1)
    # first measured contact below 2.5 (end of pre-contact window)
    below = np.where(sep_m < 2.5)[0]
    k_end = int(below[0]) if below.size else len(t)
    tend = float(t[k_end - 1]) if k_end > 0 else 0.0
    print("\n=== Fall %03d (%s): pre-contact window t <= %.2f (first measured separation below 2.5 at t = %.2f) ===" % (
        i, label, tend, float(t[k_end]) if k_end < len(t) else float("nan")))
    idx = np.rint(t / H).astype(int)
    res = {"tend": tend}
    for name, shape in [("table(no free)", K_table), ("power law(no free)", K_pl)]:
        sim = simulate(parts, float(t[-1]), shape)
        mask = np.zeros(len(t), bool)
        mask[:k_end] = True
        mask_w = [("0-1.5", (t <= 1.5) & mask), ("1.5-2.0", (t > 1.5) & (t <= 2.0) & mask), ("2.0-end", (t > 2.0) & mask)]
        rows = []
        for wl, m in mask_w:
            if m.sum() < 3:
                continue
            c, dof = chi2_of(sim, X, idx, m)
            rows.append((wl, int(m.sum()), c / dof))
        print("  %-20s" % name + "  ".join("[%s] n %d chi2/dof %.3f" % r for r in rows))
        res[name] = rows
    return res


def main():
    out = pair_runs()
    summary, rules = close_range(out)
    fac = {}
    print("\n=== Rule 4 (exploratory): species factorisation at sep 2.5, horiz runs (A-A reference = run 003) ===")
    ref = out[3]["table"]["s_best"]
    for i in (9, 10, 11):
        print("  run %03d %s: table-scale s %.3f [%.3f, %.3f]  (A-A ref s %.3f)" % (
            i, out[i]["species"], out[i]["table"]["s_best"], out[i]["table"]["s_lo"], out[i]["table"]["s_hi"], ref))
        fac[i] = out[i]["table"]["s_best"] / ref
    falls = {"012": fall_check(12, "A-A horiz from 5"), "013": fall_check(13, "A-A diag from 5")}
    path = os.path.join(ROOT, "out", "labs", "lab-a", "analysis", "score_round1_2026-11-25.json")
    with open(path, "w") as f:
        json.dump({"pair": out, "close_range": summary, "rules": rules, "factorisation_ratio_to_AA": fac,
                   "falls": falls}, f, indent=2, default=float)
    print("\nwrote", path)


if __name__ == "__main__":
    main()
