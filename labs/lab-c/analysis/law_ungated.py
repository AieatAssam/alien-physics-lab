"""UNGATED copy of the P-0026 pair law (lab-c analysis only; no domain checks).

Same integrator as papers/P-0032/model.py: acceleration (G/2)/r^P toward the other particle, G = 23.63, P = 2.099,
RK4 with internal step 1e-4, specular reflection at 0 and L = 10. Used to score runs that fall outside a
paper's stated domain, so a fail-at-the-edge test can be reported without claiming it.
"""
import math

L = 10.0
G = 23.63
P = 2.099
H = 1e-4


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
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)]
            for i in range(2)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)]
            for i in range(2)]
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
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    dur = float(setup["duration"])
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
        samples.append({"t": target,
                        "particles": [{"id": pid, "pos": [pos[pid][0], pos[pid][1]]} for pid in range(2)]})
    return samples
