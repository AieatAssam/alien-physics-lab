"""P-0003 predictor (lab-a): pairwise central attraction between particles.

Each particle is accelerated toward every other particle with magnitude K / r**P
(chamber units, time units), K = 17.74, P = 2.50. Specular reflection at the walls
x, y in {0, L}, L = 10. Fit to 2026-11-17/r3/lab-a/001-008 (two species-A particles
at rest, separation 3-6 along x, duration 1-2).

The claim is restricted to two species-A particles starting at rest with separation
3.0-6.0 and duration up to 2.0. Outside that domain this predictor is not validated.
Imports only math.
"""
import math

L = 10.0
K = 17.74
P = 2.50
H = 0.002  # internal RK4 step


def _accel(pos):
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
            a = K / r ** P
            acc[i][0] += a * dx / r
            acc[i][1] += a * dy / r
    return acc


def _deriv(pos, vel):
    return vel, _accel(pos)


def _step(pos, vel, h):
    """One RK4 step of positions and velocities (lists of [x, y])."""
    n = len(pos)

    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]

    k1p, k1v = _deriv(pos, vel)
    k2p, k2v = _deriv(add(pos, k1p, h / 2), add(vel, k1v, h / 2))
    k3p, k3v = _deriv(add(pos, k2p, h / 2), add(vel, k2v, h / 2))
    k4p, k4v = _deriv(add(pos, k3p, h), add(vel, k3v, h))
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k])
             for k in range(2)] for i in range(n)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k])
             for k in range(2)] for i in range(n)]
    # specular walls
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
    dur = float(setup["duration"])
    dt = float(setup["sample_dt"])
    n_samp = int(round(dur / dt))
    parts = setup["particles"]
    species = [p["species"] for p in parts]
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]

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
            "particles": [{"id": pid, "species": species[pid], "pos": [pos[pid][0], pos[pid][1]]}
                          for pid in range(len(parts))],
        })
    return samples
