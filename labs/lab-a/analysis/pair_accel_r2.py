"""Estimate pair accelerations from round-2 pair run 004 (and 005 repeat) by local
quadratic fits in sliding windows. Separation r(t) from the two tracked particles.
Run from repo root: python3 -I out/labs/lab-a/analysis/pair_accel_r2.py
"""
import json
import numpy as np

def load(n):
    d = json.load(open(f"results/2026-11-17/r2/lab-a/{n}.json"))
    t = np.array([s["t"] for s in d["samples"]])
    P = np.array([[p["pos"] for p in s["particles"]] for s in d["samples"]])  # (T, 2, 2)
    return t, P

def local_accel(t, x, tc, half=0.3):
    m = np.abs(t - tc) <= half
    tt = t[m] - tc
    A = np.vstack([np.ones_like(tt), tt, tt**2]).T
    c = np.linalg.lstsq(A, x[m], rcond=None)[0]
    return 2 * c[2], c[1]   # acceleration, velocity at tc

rows = []
for n in ["004", "005"]:
    t, P = load(n)
    for tc in np.arange(0.3, 2.31, 0.1):
        a0 = []; v0 = []
        for i in range(2):
            ax, vx = local_accel(t, P[:, i, 0], tc)
            ay, vy = local_accel(t, P[:, i, 1], tc)
            a0.append([ax, ay]); v0.append([vx, vy])
        a0 = np.array(a0)
        sep = np.linalg.norm(P[np.argmin(np.abs(t - tc)), 0] - P[np.argmin(np.abs(t - tc)), 1])
        # unit vector from particle 0 to particle 1
        d = P[np.argmin(np.abs(t - tc)), 1] - P[np.argmin(np.abs(t - tc)), 0]
        u = d / np.linalg.norm(d)
        # radial component of relative acceleration (positive = toward each other if negative)
        arel = a0[1] - a0[0]
        rad = float(arel @ u)  # negative -> attraction (approach)
        perp = float(arel @ np.array([-u[1], u[0]]))
        rows.append((n, round(tc, 2), round(sep, 3), round(rad, 3), round(perp, 3)))
for r in rows:
    print(r)
