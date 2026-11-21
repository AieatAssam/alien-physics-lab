"""P-0012 predictor (lab-c): two-body pair law at separation 1.5, at rest, species A and C.

Acceleration on particle i from particle j is S_pair * COUP[(s_i, s_j)] / r**2.5, where COUP is the
P-0008 coefficient table (P-0005 run means) and S_pair is a per-species-pair scale:
    S_AA = 0.753, S_AC = 0.811, S_CC = 0.874   (fitted on 2026-11-20/r2/lab-c/004, 005, 006 only;
    the 2026-11-20/r3 replicates 006, 008, 014 are out-of-sample tests).
The scale multiplies both ordered entries of the pair. Only two particles are supported.
Specular reflection at x, y in {0, L}, L = 10. Imports only math.

Domain: exactly 2 particles at rest, species in {A, C}, initial separation in [1.45, 1.55],
both particles at least 2.0 from every chamber wall, duration at most 0.4.
Other inputs raise ValueError.
"""
import math

L = 10.0
P = 2.5
H = 0.0005  # internal RK4 step (smaller than P-0008's, for the singular force at r ~ 0.3 to 1.5)
R_LO, R_HI = 1.45, 1.55
BASE = {
    ("A", "A"): 18.0,
    ("A", "C"): -8.77,
    ("C", "A"): -21.25,
    ("C", "C"): 12.36,
}
SCALE = {("A", "A"): 0.753, ("A", "C"): 0.811, ("C", "A"): 0.811, ("C", "C"): 0.874}
COUP = {k: SCALE[k] * v for k, v in BASE.items()}


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
    if len(parts) != 2:
        raise ValueError("P-0012 covers exactly two particles")
    species = [p["species"] for p in parts]
    for s in species:
        if s not in ("A", "C"):
            raise ValueError("species outside A, C")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    sep = math.hypot(pos[1][0] - pos[0][0], pos[1][1] - pos[0][1])
    if not (R_LO <= sep <= R_HI):
        raise ValueError("P-0012 covers separation 1.45 to 1.55 (got %.3f)" % sep)
    if any(v != 0.0 for p in parts for v in p["vel"]):
        raise ValueError("P-0012 covers particles at rest only")
    if any(not (2.0 <= c <= L - 2.0) for q in pos for c in q):
        raise ValueError("P-0012 covers particles at least 2.0 from every wall")
    dur = float(setup["duration"])
    if dur > 0.4 + 1e-12:
        raise ValueError("P-0012 covers duration up to 0.4")
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
