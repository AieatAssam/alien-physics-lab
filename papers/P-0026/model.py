"""P-0026 predictor (lab-keystone): N A particles at rest, pairwise-additive attractive power law.

Each ordered pair (i, j) contributes an acceleration on i of magnitude (G/2) / r_ij**P toward j, so that
the pair relative acceleration is G / q**P with G = 23.63 and P = 2.099 (chamber and time units),
summed over all partners (the same law as P-0024, with no N-body correction). Integrated with RK4
(step 0.001) with specular reflection at x, y in {0, L}, L = 10. Imports only math.

Domain: species A only, 2 to 16 particles, all at rest, every initial pairwise distance in [1.5, 10.5],
duration <= 0.3. Other inputs raise ValueError. The duration bound is part of the claim: it is not
a property of the physics the claim asserts beyond T = 0.3.
"""
import math

L = 10.0
G = 23.63
P = 2.099
H = 0.001
R_LO, R_HI = 1.5, 10.5
T_MAX = 0.3
N_MAX = 16


def _accel(pos):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            f = 0.5 * G / r ** (P + 1)
            acc[i][0] += f * dx
            acc[i][1] += f * dy
    return acc


def _step(pos, vel, h):
    n = len(pos)

    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]

    k1p, k1v = vel, _accel(pos)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, _accel(p2)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, _accel(p3)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, _accel(p4)
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


def predict(setup):
    parts = setup["particles"]
    if not 2 <= len(parts) <= N_MAX:
        raise ValueError("claim covers 2 to 16 particles")
    if any(p["species"] != "A" for p in parts):
        raise ValueError("claim covers species A only")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    if any(abs(c) > 0.0 for v in vel for c in v):
        raise ValueError("claim covers particles at rest only")
    n = len(pos)
    for i in range(n):
        for j in range(i + 1, n):
            r = math.dist(pos[i], pos[j])
            if not R_LO <= r <= R_HI:
                raise ValueError("initial pairwise distance outside [1.5, 10.5]")
    dur = float(setup["duration"])
    if dur > T_MAX + 1e-12:
        raise ValueError("duration beyond the claim's window (T <= 0.3)")
    dt = float(setup["sample_dt"])
    n_samp = int(round(dur / dt))
    samples = []
    t = 0.0
    for i in range(n_samp + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = _step(pos, vel, h)
            t += h
        t = target
        samples.append({
            "t": target,
            "particles": [{"id": pid, "species": "A", "pos": [pos[pid][0], pos[pid][1]]}
                          for pid in range(n)],
        })
    return samples
