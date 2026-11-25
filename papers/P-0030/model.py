"""P-0029 predictor (lab-vernier): two particles, species A and C, at rest, initial separation 2.5 to 3.5.

Each particle accelerates along the separation with magnitude K(r) / r**2.5 (P = 2.5 fixed):
  particle A (partner C) uses K_AC(r); particle C (partner A) uses K_CA(r).
Negative K means repulsion. K_AC and K_CA are piecewise-linear in r with nodes at r = 2.5, 3.0, 3.5
(node values are fitted to lab-vernier runs 2026-11-24/r3 001-010). Outside [2.5, 3.5] the claim is silent
and predict() raises ValueError. Other species, other particle counts, initial velocity and T > 2 are refused.
Specular reflection at x, y in {0, L}, L = 10. Imports only math.
"""
import math

L = 10.0
P = 2.5
H = 0.001  # internal RK4 step
R_NODES = [2.5, 3.0, 3.5]
K_AC_NODES = [-8.820, -9.064, -9.096]    # A away from C (P-0005 separation-5 value -8.77)
K_CA_NODES = [-20.831, -21.319, -21.757]  # C away from A (P-0005 separation-5 value -21.25)
R_LO, R_HI = 2.5, 3.5
T_MAX = 2.0


def _interp(r, nodes):
    if r <= R_NODES[0]:
        return nodes[0]
    if r >= R_NODES[-1]:
        return nodes[-1]
    for k in range(len(R_NODES) - 1):
        if R_NODES[k] <= r <= R_NODES[k + 1]:
            f = (r - R_NODES[k]) / (R_NODES[k + 1] - R_NODES[k])
            return nodes[k] + f * (nodes[k + 1] - nodes[k])
    raise ValueError("unreachable")


def _accel(pos, species):
    acc = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(2):
        j = 1 - i
        dx = pos[j][0] - pos[i][0]
        dy = pos[j][1] - pos[i][1]
        r = math.hypot(dx, dy)
        K = _interp(r, K_AC_NODES if species[i] == "A" else K_CA_NODES)
        a = K / r ** P
        acc[i][0] = a * dx / r
        acc[i][1] = a * dy / r
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
        raise ValueError("P-0029 covers exactly two particles")
    species = [p["species"] for p in parts]
    if sorted(species) != ["A", "C"]:
        raise ValueError("P-0029 covers the A-C pair only")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    if any(abs(c) > 0.0 for v in vel for c in v):
        raise ValueError("P-0029 covers particles at rest only")
    r0 = math.dist(pos[0], pos[1])
    if not R_LO - 1e-9 <= r0 <= R_HI + 1e-9:
        raise ValueError("initial separation outside [2.5, 3.5] (got %.4f)" % r0)
    dur = float(setup["duration"])
    if dur > T_MAX + 1e-12:
        raise ValueError("duration beyond the claim's window (T <= 2)")
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
