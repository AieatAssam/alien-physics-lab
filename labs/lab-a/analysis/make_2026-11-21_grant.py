"""lab-a 2026-11-21 grant PRE-REGISTRATION: pairwise-sum prediction for nine A particles on a 3x3 grid, spacing 3.5.
Each pair: attraction with magnitude K / r^P, K = 18.0 (flat A-A law), P = 2.5. Positions and velocities at rest.
Written before the main-event result exists. Walls: specular at 0 and 10 (not reached in T = 0.5 by this model).
Usage: python3 -I make_2026-11-21_grant.py <repo_root>
"""
import json
import math
import os
import sys

root = sys.argv[1]
K, P, T, DT, H, L = 18.0, 2.5, 0.5, 0.005, 1e-4, 10.0
xs = [1.5, 5.0, 8.5]
pos = [[x, y] for y in xs for x in xs]
vel = [[0.0, 0.0] for _ in pos]
n = len(pos)


def accel(p):
    a = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx, dy = p[j][0] - p[i][0], p[j][1] - p[i][1]
            r = math.hypot(dx, dy)
            f = K / r ** P
            a[i][0] += f * dx / r
            a[i][1] += f * dy / r
    return a


def step(p, v, h):
    def lin(x, y, s):
        return [[x[i][k] + s * y[i][k] for k in range(2)] for i in range(n)]
    k1p, k1v = v, accel(p)
    k2p, k2v = lin(v, k1v, h / 2), accel(lin(p, k1p, h / 2))
    k3p, k3v = lin(v, k2v, h / 2), accel(lin(p, k2p, h / 2))
    k4p, k4v = lin(v, k3v, h), accel(lin(p, k3p, h))
    np_ = [[p[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)] for i in range(n)]
    nv = [[v[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)] for i in range(n)]
    for i in range(n):
        for k in range(2):
            if np_[i][k] < 0:
                np_[i][k], nv[i][k] = -np_[i][k], -nv[i][k]
            elif np_[i][k] > L:
                np_[i][k], nv[i][k] = 2 * L - np_[i][k], -nv[i][k]
    return np_, nv


samples = [{"t": 0.0, "pos": [list(q) for q in pos]}]
t, p, v = 0.0, pos, vel
for m in range(1, int(round(T / DT)) + 1):
    target = m * DT
    while t < target - 1e-12:
        h = min(H, target - t)
        p, v = step(p, v, h)
        t += h
    samples.append({"t": round(target, 9), "pos": [list(q) for q in p]})

out = {"written_before_result": True, "model": "pairwise sum, K=18.0 (flat A-A), P=2.5",
       "rule": "RMSE/L <= 0.01 supports additivity at N=9; > 0.02 refutes", "samples": samples}
with open(os.path.join(root, "out", "labs", "lab-a", "analysis", "pred_grant_2026-11-21.json"), "w") as fh:
    json.dump(out, fh)
print("predicted samples:", len(samples), "end positions min pair separation at T:",
      round(min(math.dist(p[i], p[j]) for i in range(n) for j in range(i + 1, n)), 3))
