"""P-0005 predictor (lab-a): two-particle central pair accelerations at separation 5.

Particle i is accelerated toward (positive K) or away from (negative K) particle j with
magnitude COUP[(s_i, s_j)] / r**2.5 (chamber length and time units). Only the species
pairs in COUP are predicted; others raise ValueError. The setup must contain exactly two
particles whose initial separation is 5.0 (within 0.05). Values are run means fitted to
2026-11-18/r1/lab-a/001-005 and r2/001-005 (and A-A from 2026-11-17/r3/lab-a/005-006).
Specular reflection at the walls x, y in {0, L}, L = 10. Imports only math.
"""
import math

L = 10.0
P = 2.5
H = 0.002  # internal RK4 step
R0 = 5.0
COUP = {
    ("A", "A"): 18.0,
    ("A", "B"): 8.99,    # acceleration of A due to B
    ("B", "A"): 12.34,   # acceleration of B due to A
    ("A", "C"): -8.77,   # A away from C (repulsion)
    ("C", "A"): -21.25,  # C away from A (repulsion)
    ("B", "B"): 6.12,
    ("C", "C"): 12.36,
    ("B", "C"): -6.10,   # B away from C (repulsion)
    ("C", "B"): -10.59,  # C away from B (repulsion)
}


def _accel(pos, species):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            key = (species[i], species[j])
            if key not in COUP:
                raise ValueError("species pair %s outside the P-0005 domain" % (key,))
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            if r < 1e-9:
                continue
            a = COUP[key] / r ** P
            acc[i][0] += a * dx / r
            acc[i][1] += a * dy / r
    return acc


def _step(pos, vel, species, h):
    n = len(pos)

    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]

    k1p, k1v = vel, _accel(pos, species)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, _accel(p2, species)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, _accel(p3, species)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, _accel(p4, species)
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
        raise ValueError("P-0005 covers exactly two particles")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    sep = math.hypot(pos[1][0] - pos[0][0], pos[1][1] - pos[0][1])
    if abs(sep - R0) > 0.05:
        raise ValueError("P-0005 covers initial separation 5.0 only (got %.3f)" % sep)
    dur = float(setup["duration"])
    dt = float(setup["sample_dt"])
    n_samp = int(round(dur / dt))
    species = [p["species"] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
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
                          for pid in range(len(parts))],
        })
    return samples
