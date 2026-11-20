"""P-0009 predictor (lab-a): three particles of species B and C at separation 5.

Each particle i is accelerated toward every partner j by COUP[(s_i, s_j)] / r**2.5
(chamber length and time units). The coefficients are the P-0005 run means at separation 5
(B-B 6.12, B-C -6.10, C-B -10.59, C-C 12.36). The motion is the pairwise sum over partners.
No three-body term. Specular reflection at x, y in {0, L}, L = 10.

Domain: 2 or 3 particles, species in {B, C}, every pairwise initial separation in [4.99, 5.01].
Other inputs raise ValueError. Imports only math.
"""
import math

L = 10.0
P = 2.5
H = 0.002  # internal RK4 step
R_LO, R_HI = 4.99, 5.01
COUP = {
    ("B", "B"): 6.12,
    ("B", "C"): -6.10,
    ("C", "B"): -10.59,
    ("C", "C"): 12.36,
}


def _accel(pos, species):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            a = COUP[(species[i], species[j])] / r ** P
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
    n = len(parts)
    if n not in (2, 3):
        raise ValueError("P-0009 covers 2 or 3 particles")
    species = [p["species"] for p in parts]
    for s in species:
        if s not in ("B", "C"):
            raise ValueError("species outside B, C")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    for a in range(n):
        for b in range(a + 1, n):
            sep = math.hypot(pos[b][0] - pos[a][0], pos[b][1] - pos[a][1])
            if not (R_LO <= sep <= R_HI):
                raise ValueError("P-0009 covers pairwise separations 4.99 to 5.01 (got %.3f)" % sep)
    dur = float(setup["duration"])
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
                          for pid in range(n)],
        })
    return samples
