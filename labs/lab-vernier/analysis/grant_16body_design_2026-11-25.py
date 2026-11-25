"""Vernier round 3 grant design: 16-body additivity test, 4x4 A lattice at spacing 3.0, T = 1.

Four requests (grant account), each a 4x4 lattice of A particles at rest with spacing 3.0 and a
small symmetry-breaking jitter (uniform, +-0.10 per coordinate, seeded) so the test sees tangential
force components that an exact lattice cancels by symmetry. Offsets 0.5 and 0.8 as in round 2.

Pre-registration (written before any grant result exists):
  prediction A: pairwise superposition with the P-0028 table (nodes 3..9, end-held outside [3, 9]).
  prediction B: pairwise superposition with the P-0031 A-A node curve (16.941, 18.034, 18.285 at
                2.5, 3.0, 3.5; end-held outside [2.5, 3.5]). Differs from A only for pairs closer
                than 3, which the jitter creates (nearest pairs ~2.8).
  bar: judged RMSE/L <= 0.02 against prediction A for every run (3 x 0.007).
  sensitivity: RMSE(A, B) per run. If well below 0.007, the test does not depend on the K
  extrapolation below separation 3; otherwise a miss is ambiguous and I say so.

Usage: python3 -I grant_16body_design_2026-11-25.py [--write]   (--write writes the request JSONs)
Only math, json, random, sys are used.
"""
import json
import math
import random
import sys

L = 10.0
H = 0.001
P = 2.5
OFFSETS_AND_SEEDS = [(0.5, 101), (0.5, 102), (0.8, 103), (0.8, 104)]
REQ_IDS = ["001", "002", "003", "004"]
DATE_ROUND = "2026-11-25/r3/lab-vernier"

TABLE_A = ([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0], [17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624])
TABLE_B = ([2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
           [16.941, 18.034, 18.285, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624])


def make_K(table):
    xs, ys = table

    def K(r):
        if r <= xs[0]:
            return ys[0]
        if r >= xs[-1]:
            return ys[-1]
        for k in range(len(xs) - 1):
            if xs[k] <= r <= xs[k + 1]:
                f = (r - xs[k]) / (xs[k + 1] - xs[k])
                return ys[k] + f * (ys[k + 1] - ys[k])
        raise ValueError("unreachable")
    return K


def accel(pos, K):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            f = K(r) / r ** (P + 1)
            acc[i][0] += f * dx
            acc[i][1] += f * dy
    return acc


def step(pos, vel, h, K):
    n = len(pos)

    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]

    k1p, k1v = vel, accel(pos, K)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, accel(p2, K)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, accel(p3, K)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, accel(p4, K)
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k])
             for k in range(2)] for i in range(n)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k])
             for k in range(2)] for i in range(n)]
    for i in range(n):
        for k in range(2):
            if newp[i][k] < 0.0:
                newp[i][k] = -newp[i][k]
                newv[i][k] = -newv[i][k]
            elif newp[i][k] > L:
                newp[i][k] = 2 * L - newp[i][k]
                newv[i][k] = -newv[i][k]
    return newp, newv


def lattice(offset, seed):
    rng = random.Random(seed)
    pts = []
    for ix in range(4):
        for iy in range(4):
            x = offset + 3.0 * ix + rng.uniform(-0.10, 0.10)
            y = offset + 3.0 * iy + rng.uniform(-0.10, 0.10)
            pts.append([round(x, 4), round(y, 4)])
    return pts


def predict(pos0, dur, dt, K):
    pos = [list(p) for p in pos0]
    vel = [[0.0, 0.0] for _ in pos0]
    n_samp = int(round(dur / dt))
    out = {}
    t = 0.0
    for i in range(n_samp + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = step(pos, vel, h, K)
            t += h
        t = target
        out[target] = [list(p) for p in pos]
    return out


def min_sep(pos0):
    return min(math.dist(pos0[i], pos0[j]) for i in range(len(pos0)) for j in range(i + 1, len(pos0)))


def rmse_over_L(p, q, dur, dt):
    """RMSE over all sample times and particles between two predicted trajectories, / L."""
    n_samp = int(round(dur / dt))
    se, n = 0.0, 0
    for i in range(n_samp + 1):
        t = round(i * dt, 9)
        for a, b in zip(p[t], q[t]):
            se += (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
            n += 2
    return math.sqrt(se / n) / L


def request(num, offset, seed):
    pts = lattice(offset, seed)
    return {
        "request_id": f"{DATE_ROUND}/{num}",
        "lab": "lab-vernier",
        "account": "grant",
        "purpose": ("Grant 16-body additivity test (pre-registered): 4x4 A lattice at spacing 3.0, "
                    f"offset {offset}, jitter +-0.10 (seed {seed}), at rest, T = 1. Predicted by "
                    "pairwise superposition with the P-0028 A-A table (end-held outside [3, 9]); bar 0.02 RMSE/L."),
        "setup": {
            "particles": [{"species": "A", "pos": p, "vel": [0.0, 0.0]} for p in pts],
            "duration": 1.0,
            "sample_dt": 0.0005,
        },
        "instruments": ["tracker"],
    }


if __name__ == "__main__":
    KA, KB = make_K(TABLE_A), make_K(TABLE_B)
    write = "--write" in sys.argv
    for num, (offset, seed) in zip(REQ_IDS, OFFSETS_AND_SEEDS):
        req = request(num, offset, seed)
        pos0 = [p["pos"] for p in req["setup"]["particles"]]
        dur, dt = req["setup"]["duration"], req["setup"]["sample_dt"]
        pa = predict(pos0, dur, dt, KA)
        pb = predict(pos0, dur, dt, KB)
        print(f"{req['request_id']} offset {offset} seed {seed} min_sep {min_sep(pos0):.3f} "
              f"RMSE(A,B)/L {rmse_over_L(pa, pb, dur, dt):.5f}")
        if write:
            import os
            d = f"/home/runner/work/alien-physics-lab/alien-physics-lab/out/requests/{DATE_ROUND}"
            os.makedirs(d, exist_ok=True)
            with open(f"{d}/{num}.json", "w") as fh:
                json.dump(req, fh, indent=2)
                fh.write("\n")
