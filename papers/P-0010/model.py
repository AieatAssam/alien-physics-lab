"""P-0009 predictor (lab-keystone): two particles at rest, initial separation 6 to 9, species A, B, C.

Each particle i is accelerated toward (K > 0) or away from (K < 0) its partner j with magnitude
|K_ij| / r**2.5, where r is the current separation (chamber and time units, P = 2.5 fixed).
K_ij is held constant over the run and set by its initial separation r0:

    K_ij = COUP5[(s_i, s_j)] * G(r0) * (S_C if 'C' in (s_i, s_j) else 1)
    G(r0) = G0 + G1 * r0          (shared radial factor, G(5) is not used)

COUP5 are the separation-5 coefficients of P-0005 (accepted). G0, G1 and S_C were fitted by
lab-keystone to 2026-11-19 far-field runs (r0 = 6, 7, 8, 9). Specular reflection at the walls
x, y in {0, L}, L = 10.

Domain: exactly 2 particles, species in {A, B, C}, both at rest, initial separation in [6, 9],
duration <= 6.0. Other inputs raise ValueError; the duration limit is part of this claim, since
the fitted K was only checked over T <= 6. Imports only math.
"""
import math

L = 10.0
P = 2.5
H = 0.002  # internal RK4 step
R_LO, R_HI = 6.0, 9.0
T_MAX = 6.0
G0 = 1.5100
G1 = -0.0920
S_C = 0.9475
COUP5 = {
    ("A", "A"): 18.0,
    ("A", "B"): 8.99,
    ("B", "A"): 12.34,
    ("A", "C"): -8.77,
    ("C", "A"): -21.25,
    ("B", "B"): 6.12,
    ("C", "C"): 12.36,
    ("B", "C"): -6.10,
    ("C", "B"): -10.59,
}


def _coef(si, sj, r0):
    g = G0 + G1 * r0
    if "C" in (si, sj):
        g *= S_C
    return COUP5[(si, sj)] * g


def _accel(pos, K):
    n = 2
    acc = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(n):
        j = 1 - i
        dx = pos[j][0] - pos[i][0]
        dy = pos[j][1] - pos[i][1]
        r = math.hypot(dx, dy)
        a = K[i] / r ** P
        acc[i][0] = a * dx / r
        acc[i][1] = a * dy / r
    return acc


def _step(pos, vel, K, h):
    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(2)]

    k1p, k1v = vel, _accel(pos, K)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, _accel(p2, K)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, _accel(p3, K)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, _accel(p4, K)
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
        raise ValueError("P-0009 covers exactly two particles")
    species = [p["species"] for p in parts]
    for s in species:
        if s not in ("A", "B", "C"):
            raise ValueError("species outside A, B, C")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    if any(abs(v) > 1e-12 for vv in vel for v in vv):
        raise ValueError("P-0009 covers particles at rest only")
    r0 = math.hypot(pos[1][0] - pos[0][0], pos[1][1] - pos[0][1])
    if not (R_LO <= r0 <= R_HI):
        raise ValueError("P-0009 covers initial separations 6 to 9 (got %.3f)" % r0)
    dur = float(setup["duration"])
    dt = float(setup["sample_dt"])
    if dur > T_MAX + 1e-9:
        raise ValueError("P-0009 is checked only for duration <= 6")
    K = [_coef(species[0], species[1], r0), _coef(species[1], species[0], r0)]
    n_samp = int(round(dur / dt))
    samples = []
    t = 0.0
    for i in range(n_samp + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = _step(pos, vel, K, h)
            t += h
        t = target
        samples.append({
            "t": target,
            "particles": [{"id": pid, "species": species[pid], "pos": [pos[pid][0], pos[pid][1]]}
                          for pid in range(2)],
        })
    return samples
