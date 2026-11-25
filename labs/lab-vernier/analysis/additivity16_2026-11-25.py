"""Vernier: N-body pairwise-superposition predictor for N > 8 (16-body additivity test), round 3.

Uses the P-0028 A-A table (nodes 3..9, end-held outside [3, 9]) as the pair law: each ordered pair
(i, j) gives particle i an acceleration K(r)/r^2.5 toward j; accelerations add; RK4 step 0.001;
specular reflection at the walls. No domain guard: this is a test of additivity beyond the claim's
N <= 8 limit, not a review. Imports only math (and json/sys for the CLI).

Scoring follows the review rules: RMSE over all samples and particles, both coordinates, of
(pred - measured), divided by L = 10. Zero-force null: particles held at their initial positions.

Usage:
  python3 -I additivity16_2026-11-25.py <repo>/results/<id>.json <repo>/requests/<id>.json [...]
"""
import json
import math
import sys

L = 10.0
H = 0.001
P = 2.5
NODE_R = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
NODE_K = [17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624]


def K(r):
    if r <= NODE_R[0]:
        return NODE_K[0]
    if r >= NODE_R[-1]:
        return NODE_K[-1]
    for k in range(len(NODE_R) - 1):
        if NODE_R[k] <= r <= NODE_R[k + 1]:
            f = (r - NODE_R[k]) / (NODE_R[k + 1] - NODE_R[k])
            return NODE_K[k] + f * (NODE_K[k + 1] - NODE_K[k])
    raise ValueError("unreachable")


def accel(pos):
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


def step(pos, vel, h):
    n = len(pos)

    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]

    k1p, k1v = vel, accel(pos)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, accel(p2)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, accel(p3)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, accel(p4)
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


def predict_samples(setup):
    parts = setup["particles"]
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    dur = float(setup["duration"])
    dt = float(setup["sample_dt"])
    n_samp = int(round(dur / dt))
    out = {}
    t = 0.0
    for i in range(n_samp + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = step(pos, vel, h)
            t += h
        t = target
        out[target] = [list(p) for p in pos]
    return out


def rmse_over_L(pred, res):
    se, n = 0.0, 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        for p in s["particles"]:
            q = pred[t][p["id"]]
            se += (p["pos"][0] - q[0]) ** 2 + (p["pos"][1] - q[1]) ** 2
            n += 2
    return math.sqrt(se / n) / L


def main(argv):
    for k in range(0, len(argv), 2):
        res = json.load(open(argv[k + 1]))
        req = json.load(open(argv[k]))
        pred = predict_samples(req["setup"])
        e = rmse_over_L(pred, res)
        init = {p["id"]: p["pos"] for p in res["samples"][0]["particles"]}
        null = rmse_over_L({round(s["t"], 9): init for s in res["samples"]}, res)
        print(f"{req['request_id']} N={len(req['setup']['particles'])} T={req['setup']['duration']} "
              f"err={e:.5f} null={null:.5f}")


if __name__ == "__main__":
    main(sys.argv[1:])
