"""P-0022 predictor (lab-b): one A and one B at rest, initial separation 1.95 to 2.05, duration at most 0.8.

Acceleration of particle i toward partner j is K[s_i] / r**P, with P = 2.5 fixed, K['A'] = K_A(B) = 7.59
(acceleration of A due to B) and K['B'] = K_B(A) = 10.59 (acceleration of B due to A). Effective constants
for this separation band and this time window only. No claim about other separations, durations or exponent.
Specular reflection at walls x, y in {0, L}, L = 10. Imports only math. Other inputs raise ValueError.
"""
import math

L = 10.0
P = 2.5
K = {"A": 7.59, "B": 10.59}
H = 0.001  # internal RK4 step
R_LO, R_HI = 1.95, 2.05
T_MAX = 0.8


def _accel(pos, species):
    acc = [[0.0, 0.0], [0.0, 0.0]]
    dx = pos[1][0] - pos[0][0]
    dy = pos[1][1] - pos[0][1]
    r = math.hypot(dx, dy)
    a0 = K[species[0]] / r ** P
    a1 = K[species[1]] / r ** P
    acc[0] = [a0 * dx / r, a0 * dy / r]
    acc[1] = [-a1 * dx / r, -a1 * dy / r]
    return acc


def _step(pos, vel, species, h):
    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(2)]

    k1p, k1v = vel, _accel(pos, species)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, _accel(p2, species)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, _accel(p3, species)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, _accel(p4, species)
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
        raise ValueError("P-0022 covers exactly two particles")
    species = [p["species"] for p in parts]
    if sorted(species) != ["A", "B"]:
        raise ValueError("P-0022 covers one A and one B only")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    if any(v != 0.0 for p in parts for v in p["vel"]):
        raise ValueError("P-0022 covers particles at rest only")
    sep = math.hypot(pos[1][0] - pos[0][0], pos[1][1] - pos[0][1])
    if not (R_LO <= sep <= R_HI):
        raise ValueError("P-0022 covers separation 1.95 to 2.05 (got %.3f)" % sep)
    dur = float(setup["duration"])
    if dur > T_MAX + 1e-12:
        raise ValueError("P-0022 covers duration up to 0.8")
    dt = float(setup["sample_dt"])
    n_samp = int(round(dur / dt))
    samples = []
    t = 0.0
    for i in range(n_samp + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = _step(pos, vel, species, h)
            t += h
        t = target
        samples.append({
            "t": target,
            "particles": [{"id": pid, "species": species[pid], "pos": [pos[pid][0], pos[pid][1]]}
                          for pid in range(2)],
        })
    return samples
