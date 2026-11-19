"""P-0006 predictor (lab-a): shared distance law for pair accelerations at separations 7 and 9.

Particle i is accelerated toward (K > 0) or away from (K < 0) particle j with magnitude
K_ij(r) / r**2.5, where K_ij(r) = COUP5[(s_i, s_j)] * SCALE[r] (chamber length and time
units, P = 2.5 fixed). COUP5 holds the P-0005 run means at separation 5. SCALE holds the
A-A distance factors: SCALE[7] = 15.48 / 18.0 = 0.86 (2026-11-18/r2/lab-a/006-007 and
P-0003 at 5), SCALE[9] = 11.70 / 18.0 = 0.65 (2026-11-18/r1/lab-a/008-009, mean of four per-particle values).
Only species pairs in COUP5 at initial separation 7.0 or 9.0 (within 0.05) are predicted;
others raise ValueError. Specular reflection at x, y in {0, L}, L = 10. Imports only math.
"""
import math

L = 10.0
P = 2.5
H = 0.002  # internal RK4 step
SEPS = (7.0, 9.0)
SCALE = {7.0: 0.86, 9.0: 0.65}
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


def _accel(pos, species, coup):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            if r < 1e-9:
                continue
            a = coup[(species[i], species[j])] / r ** P
            acc[i][0] += a * dx / r
            acc[i][1] += a * dy / r
    return acc


def _step(pos, vel, species, coup, h):
    n = len(pos)

    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]

    k1p, k1v = vel, _accel(pos, species, coup)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, _accel(p2, species, coup)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, _accel(p3, species, coup)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, _accel(p4, species, coup)
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
    if len(parts) != 2:
        raise ValueError("P-0006 covers exactly two particles")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    sep = math.hypot(pos[1][0] - pos[0][0], pos[1][1] - pos[0][1])
    sep0 = [s for s in SEPS if abs(sep - s) <= 0.05]
    if not sep0:
        raise ValueError("P-0006 covers initial separation 7 or 9 only (got %.3f)" % sep)
    r0 = sep0[0]
    coup = {}
    species = [p["species"] for p in parts]
    for key, val in COUP5.items():
        coup[key] = val * SCALE[r0]
    for i in range(2):
        for j in range(2):
            if i != j and (species[i], species[j]) not in COUP5:
                raise ValueError("species pair %s outside the P-0006 domain" % ((species[i], species[j]),))
    dur = float(setup["duration"])
    dt = float(setup["sample_dt"])
    n_samp = int(round(dur / dt))
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    samples = []
    t = 0.0
    for i in range(n_samp + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = _step(pos, vel, species, coup, h)
            t += h
        t = target
        samples.append({
            "t": target,
            "particles": [{"id": pid, "species": species[pid], "pos": [pos[pid][0], pos[pid][1]]}
                          for pid in range(2)],
        })
    return samples
