"""P-0025 predictor (lab-b): one A and one B particle at rest, initial separation 4.0 to 8.0, duration <= 2.0.

Each particle accelerates toward the other with magnitude K / r^2.5 (r the current separation), where
K_A = K_A(r) is the acceleration coefficient of A due to B, interpolated linearly in r from a table of
fitted values, and K_B = RATIO * K_A is the coefficient of B due to A. RATIO = K_B / K_A = m_A / m_B = 1.41.
Specular walls at 0 and L = 10. Imports only numpy and math.
Domain: exactly 2 particles, one A and one B, both at rest, initial separation in [4.0, 8.0], duration <= 2.0.
Other inputs raise ValueError.
"""
import math
import numpy as np

L = 10.0
P = 2.5
RATIO = 1.41
R_TAB = np.array([4.0, 5.0, 6.0, 7.0, 8.0])
K_TAB = np.array([9.10, 9.26, 8.52, 7.75, 6.85])  # K_A(r) at each tabulated separation
R_LO, R_HI = 4.0, 8.0
T_MAX = 2.0
H = 0.002  # internal RK4 step


def _k_a(r):
    return float(np.interp(r, R_TAB, K_TAB))


def _accel(pos, species):
    r_vec = pos[1] - pos[0]
    r = math.hypot(r_vec[0], r_vec[1])
    ka = _k_a(r)
    coef = {"A": ka, "B": RATIO * ka}
    a = np.zeros((2, 2))
    a[0] = coef[species[0]] / r ** P * r_vec / r
    a[1] = -coef[species[1]] / r ** P * r_vec / r
    return a


def _step(pos, vel, h, species):
    k1p, k1v = vel, _accel(pos, species)
    p2, v2 = pos + h / 2 * k1p, vel + h / 2 * k1v
    k2p, k2v = v2, _accel(p2, species)
    p3, v3 = pos + h / 2 * k2p, vel + h / 2 * k2v
    k3p, k3v = v3, _accel(p3, species)
    p4, v4 = pos + h * k3p, vel + h * k3v
    k4p, k4v = v4, _accel(p4, species)
    pos = pos + h / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
    vel = vel + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
    for i in range(2):
        for k in range(2):
            if pos[i, k] < 0.0:
                pos[i, k] = -pos[i, k]
                vel[i, k] = -vel[i, k]
            elif pos[i, k] > L:
                pos[i, k] = 2 * L - pos[i, k]
                vel[i, k] = -vel[i, k]
    return pos, vel


def predict(setup):
    parts = setup["particles"]
    if len(parts) != 2:
        raise ValueError("claim covers exactly two particles")
    species = [p["species"] for p in parts]
    if sorted(species) != ["A", "B"]:
        raise ValueError("claim covers one A and one B particle")
    pos = np.array([[float(p["pos"][0]), float(p["pos"][1])] for p in parts])
    vel = np.array([[float(p["vel"][0]), float(p["vel"][1])] for p in parts])
    if np.any(vel != 0.0):
        raise ValueError("claim covers particles at rest only")
    r0 = math.dist(pos[0], pos[1])
    if not R_LO <= r0 <= R_HI:
        raise ValueError("initial separation outside [4.0, 8.0]")
    dur = float(setup["duration"])
    if dur > T_MAX + 1e-12:
        raise ValueError("duration beyond 2.0")
    dt = float(setup["sample_dt"])
    n_samp = int(round(dur / dt))
    samples = []
    t = 0.0
    for i in range(n_samp + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = _step(pos, vel, h, species)
            t += h
        t = target
        samples.append({
            "t": target,
            "particles": [{"id": pid, "species": species[pid], "pos": [float(pos[pid, 0]), float(pos[pid, 1])]}
                          for pid in range(2)],
        })
    return samples
