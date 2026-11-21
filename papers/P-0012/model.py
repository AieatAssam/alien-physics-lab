"""P-0012 predictor (lab-a): two A particles at rest, initial separation exactly 1.0, duration at most 0.15.

Each particle accelerates toward its partner with magnitude K / r**P, P = 2.5 fixed, r the current separation,
with K = 11.3 held constant over the run. Specular reflection at the walls x, y in {0, L}, L = 10.
K = 11.3 is the mean of two lab-a fits of the separation profile (requests 2026-11-20/r3/lab-a/003 and 004,
fitted K = 11.52 and 11.05). Other inputs raise ValueError. Imports only math.
"""
import math

L = 10.0
P = 2.5
K = 11.3
H = 1e-4  # internal RK4 step (the pair closes to about 0.5 inside the domain)
R0 = 1.0
T_MAX = 0.15


def _accel(pos):
    dx = pos[1][0] - pos[0][0]
    dy = pos[1][1] - pos[0][1]
    r = math.hypot(dx, dy)
    a = K / r ** P
    return [[a * dx / r, a * dy / r], [-a * dx / r, -a * dy / r]]


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
        raise ValueError("P-0012 covers exactly two particles")
    if any(p["species"] != "A" for p in parts):
        raise ValueError("P-0012 covers species A only")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    if any(abs(v) > 1e-12 for vv in vel for v in vv):
        raise ValueError("P-0012 covers particles at rest only")
    r0 = math.hypot(pos[1][0] - pos[0][0], pos[1][1] - pos[0][1])
    if abs(r0 - R0) > 1e-9:
        raise ValueError("P-0012 covers initial separation 1.0 only (got %.4f)" % r0)
    dur = float(setup["duration"])
    dt = float(setup["sample_dt"])
    if dur > T_MAX + 1e-9:
        raise ValueError("P-0012 is checked only for duration <= 0.15")
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
            "particles": [{"id": pid, "species": "A", "pos": [pos[pid][0], pos[pid][1]]} for pid in range(2)],
        })
    return samples
