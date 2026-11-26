#!/usr/bin/env python3
"""Score lab-a round 1 of 2026-11-26: species radial falls r1/013-019 against the A-A reference falls
2026-11-25/r1/012 (horizontal) and 013 (diagonal), same geometry.

Model: two-particle RK4 (h = 0.002), specular walls, K_ij(r) = s * K_table(r) with the P-0027 table
(clamped at 17.683 below r = 3), force K/r^2.5 on each particle (equal-mass symmetric, as in round 1).
For each run: one whole-window scale s over the pre-contact window (measured separation > 2.5, before
first measured separation < 2.5), plus separate s for the early (separation 5 to 3.5) and late
(3.5 to 2.5) windows. Each window's chi2 is computed on samples in that window only; the trajectory is
simulated once per s from the exact setup.

Ratio rule (NOTEBOOK plan, step 2): factorisation holds if K_ij/K_AA is constant to within 5 per cent
over the pre-contact part (rule a). Sigma 0.05 per coordinate. Scale grid 0.20 to 2.00 step 0.005.

Run: python3 -I score_species_falls_2026-11-26.py <repo_root>
"""
import json
import os
import sys

import numpy as np

ROOT = sys.argv[1]
SIG = 0.05
L = 10.0
P = 2.5
H = 0.002
NODE_R = np.array([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
NODE_K = np.array([17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624])


def K_table(r):
    return np.interp(float(r), NODE_R, NODE_K)


def load(date, rnd, lab, rid):
    req = json.load(open(os.path.join(ROOT, "requests", date, rnd, lab, rid + ".json")))
    res = json.load(open(os.path.join(ROOT, "results", date, rnd, lab, rid + ".json")))
    assert res["status"] == "ok", res
    t = np.array([s["t"] for s in res["samples"]])
    X = np.zeros((len(t), 2, 2))
    for k, s in enumerate(res["samples"]):
        for p in s["particles"]:
            X[k, p["id"]] = p["pos"]
    return req, t, X


def simulate(pos0, vel0, T, s):
    pos = np.array(pos0, float)
    vel = np.array(vel0, float)

    def acc(p):
        d = p[1] - p[0]
        r = float(np.linalg.norm(d))
        F = s * K_table(r) / r ** P
        u = d / r
        return np.array([F * u, -F * u])

    xs = [pos.copy()]
    for _ in range(int(round(T / H))):
        a1 = acc(pos)
        p2, v2 = pos + 0.5 * H * vel, vel + 0.5 * H * a1
        a2 = acc(p2)
        p3, v3 = pos + 0.5 * H * v2, vel + 0.5 * H * a2
        a3 = acc(p3)
        p4, v4 = pos + H * v3, vel + H * a3
        a4 = acc(p4)
        pos = pos + H / 6 * (vel + 2 * v2 + 2 * v3 + v4)
        vel = vel + H / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
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


def windows(t, X):
    sep = np.linalg.norm(X[:, 1] - X[:, 0], axis=1)
    below = np.where(sep < 2.5)[0]
    cut = below[0] if below.size else len(t)
    pre = np.arange(cut)
    pre = pre[sep[pre] > 2.5]
    early = pre[sep[pre] >= 3.5]
    late = pre[sep[pre] < 3.5]
    return {"all": pre, "early": early, "late": late}, sep


def fit(req, t, X):
    p0 = [p["pos"] for p in req["setup"]["particles"]]
    v0 = [p["vel"] for p in req["setup"]["particles"]]
    T = float(t[-1])
    W, _ = windows(t, X)
    idx = np.rint(t / H).astype(int)
    grid = np.arange(0.20, 2.0001, 0.005)
    chi = {k: [] for k in W}
    for s in grid:
        pred = simulate(p0, v0, T, s)
        for k, m in W.items():
            if m.size == 0:
                chi[k].append(np.nan)
                continue
            res = X[m] - pred[idx[m]]
            chi[k].append(float(np.sum(res ** 2) / SIG ** 2))
    out = {}
    for k, m in W.items():
        c = np.array(chi[k])
        if m.size == 0 or np.all(np.isnan(c)):
            out[k] = {"s": float("nan"), "lo": float("nan"), "hi": float("nan"), "chi2dof": float("nan"), "n": 0}
            continue
        j = int(np.nanargmin(c))
        ok = grid[c <= c[j] + 1.0]
        dof = 2 * 2 * m.size
        out[k] = {"s": float(grid[j]), "lo": float(ok.min()), "hi": float(ok.max()),
                  "chi2dof": float(c[j] / dof), "n": int(m.size)}
    return out


rows = {}
for rid, species, rnd_date, rnd, lab in []:
    pass

runs = [
    ("2026-11-25", "r1", "012", "AA horiz (reference)"),
    ("2026-11-25", "r1", "013", "AA diag (reference)"),
    ("2026-11-26", "r1", "013", "AB horiz"),
    ("2026-11-26", "r1", "014", "AB diag"),
    ("2026-11-26", "r1", "015", "BB horiz"),
    ("2026-11-26", "r1", "016", "BB diag"),
    ("2026-11-26", "r1", "017", "CC horiz"),
    ("2026-11-26", "r1", "018", "CC diag"),
    ("2026-11-26", "r1", "019", "AC horiz"),
]
for date, rnd, rid, label in runs:
    lab = "lab-a"
    req, t, X = load(date, rnd, lab, rid)
    out = fit(req, t, X)
    rows[(date, rid, label)] = out
    print("%s %s/%s %-22s T=%.2f" % (date, rnd, rid, label, float(t[-1])))
    for k in ["all", "early", "late"]:
        o = out[k]
        print("   %-6s n=%3d  s=%.3f [%.3f, %.3f]  chi2/dof=%.2f" % (k, o["n"], o["s"], o["lo"], o["hi"], o["chi2dof"]))

print()
print("Ratios against the A-A reference of the same geometry (horizontal ref = 2026-11-25 r1/012, diagonal ref = r1/013):")
ref_h = rows[("2026-11-25", "012", "AA horiz (reference)")]
ref_d = rows[("2026-11-25", "013", "AA diag (reference)")]
summary = {}
for (date, rid, label), out in rows.items():
    if "reference" in label:
        continue
    ref = ref_d if "diag" in label else ref_h
    line = []
    for k in ["all", "early", "late"]:
        if out[k]["n"] == 0 or ref[k]["n"] == 0:
            line.append("%s=n/a" % k)
            continue
        ratio = out[k]["s"] / ref[k]["s"]
        # propagate 1-sigma (Delta chi2 = 1 half-widths)
        e_r = np.hypot((out[k]["hi"] - out[k]["lo"]) / 2 / out[k]["s"], (ref[k]["hi"] - ref[k]["lo"]) / 2 / ref[k]["s"]) * ratio
        line.append("%s=%.3f+-%.3f" % (k, ratio, e_r))
        summary.setdefault(label, {})[k] = {"ratio": float(ratio), "err": float(e_r)}
    print("  %-10s %s" % (label, "  ".join(line)))

json.dump(summary, open(os.path.join(ROOT, "out", "labs", "lab-a", "analysis", "score_species_falls_2026-11-26.json"), "w"), indent=2)
