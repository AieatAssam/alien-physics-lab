"""P-0035 predictor (lab-c): two A particles at rest, P-0026 pair law, separation window 2.0 to 2.75.

Acceleration on particle i from particle j is (G/2) / r**P toward j, with G = 23.63 and P = 2.099
(the P-0026 pair law), integrated with RK4 (internal step 1e-4) and specular reflection at x, y in {0, L}.
No separation clamp: the law is used as written at r in [2.0, 2.75].
Imports only math.

Domain: exactly 2 particles, both species A, both at rest, initial separation in [2.0, 2.75], both particles
at least 2.0 from every chamber wall, duration at most 0.6. Other inputs raise ValueError.
"""
import math

L = 10.0
G = 23.63
P = 2.099
H = 1e-4  # internal RK4 step
R_LO, R_HI = 2.0, 2.75
T_MAX = 0.6


def _accel(pos):
    dx = pos[1][0] - pos[0][0]
    dy = pos[1][1] - pos[0][1]
    r = math.hypot(dx, dy)
    a = (G / 2.0) / r ** P
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
        raise ValueError("P-0035 covers exactly two particles")
    if any(p["species"] != "A" for p in parts):
        raise ValueError("P-0035 covers species A only")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    if any(c != 0.0 for v in vel for c in v):
        raise ValueError("P-0035 covers particles at rest only")
    r0 = math.dist(pos[0], pos[1])
    if not (R_LO - 1e-9 <= r0 <= R_HI + 1e-9):
        raise ValueError("P-0035 covers initial separation 2.0 to 2.75 (got %.4f)" % r0)
    if any(not (2.0 <= c <= L - 2.0) for q in pos for c in q):
        raise ValueError("P-0035 covers particles at least 2.0 from every wall")
    dur = float(setup["duration"])
    if dur > T_MAX + 1e-12:
        raise ValueError("P-0035 covers duration up to 0.6")
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
