"""P-0027 predictor (lab-a): two A particles at rest, initial separation 3.0 to 9.0.

Each particle accelerates toward the other with magnitude K(r) / r^2.5, where r is the current separation
and K(r) is piecewise-linear in r through the tabulated values below (measured per-separation means at
P = 2.5). Specular walls at 0 and L = 10. Imports only numpy and math.
Domain: exactly two A particles, both at rest, initial separation in [3.0, 9.0], duration <= _t_max(r0) (1.5 for r0 < 5, 2.0 for r0 < 7, else 3.0).
Other inputs raise ValueError.
"""
import math
import numpy as np

L = 10.0
P = 2.5
R_TAB = np.array([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
K_TAB = np.array([17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624])
R_LO, R_HI = 3.0, 9.0
H = 0.002  # internal RK4 step


def _t_max(r0):
    """Duration window by initial separation. Pairs at r0 < 5 approach contact by T about 2 (predicted
    minimum separation 0.02 at r0 = 4, T = 2), so their window is shorter."""
    if r0 < 4.999:
        return 1.5
    if r0 < 6.999:
        return 2.0
    return 3.0


def _k(r):
    return float(np.interp(r, R_TAB, K_TAB))


def _accel(pos):
    d = pos[1] - pos[0]
    r = math.hypot(d[0], d[1])
    f = _k(r) / r ** P
    return np.array([f * d / r, -f * d / r])


def _step(pos, vel, h):
    k1p, k1v = vel, _accel(pos)
    p2, v2 = pos + h / 2 * k1p, vel + h / 2 * k1v
    k2p, k2v = v2, _accel(p2)
    p3, v3 = pos + h / 2 * k2p, vel + h / 2 * k2v
    k3p, k3v = v3, _accel(p3)
    p4, v4 = pos + h * k3p, vel + h * k3v
    k4p, k4v = v4, _accel(p4)
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
    if any(p["species"] != "A" for p in parts):
        raise ValueError("claim covers species A only")
    pos = np.array([[float(p["pos"][0]), float(p["pos"][1])] for p in parts])
    vel = np.array([[float(p["vel"][0]), float(p["vel"][1])] for p in parts])
    if np.any(vel != 0.0):
        raise ValueError("claim covers particles at rest only")
    r0 = math.dist(pos[0], pos[1])
    if not R_LO - 1e-3 <= r0 <= R_HI + 1e-3:
        raise ValueError("initial separation outside [3.0, 9.0]")
    dur = float(setup["duration"])
    if dur > _t_max(r0) + 1e-9:
        raise ValueError("duration beyond the window for this initial separation")
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
        samples.append({
            "t": target,
            "particles": [{"id": pid, "species": "A", "pos": [float(pos[pid, 0]), float(pos[pid, 1])]}
                          for pid in range(2)],
        })
    return samples
