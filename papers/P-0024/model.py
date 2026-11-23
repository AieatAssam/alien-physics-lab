"""P-0024 predictor (lab-keystone): two A particles at rest, initial separation 1.25 to 3.0.

Relative acceleration magnitude along the separation: |q''| = G / q**P with G = 23.63 and P = 2.099
(chamber and time units). Each particle is accelerated toward its partner with G / (2 q**P).
Fitted by lab-keystone to 19 A-A runs (2026-11-22 r1-r3; r0 = 1.0 to 3.0; pooled over orientations).
Validity window: duration <= 0.3 for r0 < 2.5, and duration <= 0.6 for r0 in [2.5, 3.0]. These are the
ends of the fitted data. Beyond them the claim makes no statement (close approach at r0 = 1.25 is near t = 0.32).

Domain: exactly 2 particles, both species A, both at rest, initial separation in [1.25, 3.0],
duration <= 0.3 (r0 < 2.5) or <= 0.6 (r0 in [2.5, 3.0]). Other inputs raise ValueError. Specular reflection at x, y in {0, L}, L = 10.
Imports only math.
"""
import math

L = 10.0
G = 23.63
P = 2.099
H = 0.001  # internal RK4 step
R_LO, R_HI = 1.25, 3.0
T_MAX = 0.6


def _accel(pos):
    acc = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(2):
        j = 1 - i
        dx = pos[j][0] - pos[i][0]
        dy = pos[j][1] - pos[i][1]
        r = math.hypot(dx, dy)
        a = 0.5 * G / r ** P
        acc[i][0] = a * dx / r
        acc[i][1] = a * dy / r
    return acc


def _step(pos, vel, h):
    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(2)]

    k1p, k1v = vel, _accel(pos)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, _accel(p2)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, _accel(p3)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, _accel(p4)
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k])
             for k in range(2)] for i in range(2)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k])
             for k in range(2)] for i in range(2)]
    for i in range(2):
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
    if len(parts) != 2:
        raise ValueError("claim covers exactly two particles")
    if any(p["species"] != "A" for p in parts):
        raise ValueError("claim covers species A only")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    if any(abs(c) > 0.0 for v in vel for c in v):
        raise ValueError("claim covers particles at rest only")
    r0 = math.dist(pos[0], pos[1])
    if not R_LO <= r0 <= R_HI:
        raise ValueError("initial separation outside [1.25, 3.0]")
    dur = float(setup["duration"])
    t_max = T_MAX if r0 >= 2.5 else 0.3
    if dur > t_max + 1e-12:
        raise ValueError("duration beyond the claim's window for this separation")
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
                          for pid in range(2)],
        })
    return samples
