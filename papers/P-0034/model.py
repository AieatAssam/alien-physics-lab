"""P-0031 predictor (lab-vernier, Vernier): two particles of one species (A-A or C-C) at rest, initial
separation in [3.0, 3.5], duration <= 1.0. Each particle accelerates toward the other with magnitude
K(q)/q^2.5, q the current separation; K is piecewise-linear through the nodes below and held at the
end values outside [2.5, 3.5]. Integrated with RK4 (step 0.001) and specular reflection at the walls
x, y in {0, 10}. Imports only math.

Anything outside the claim's domain raises ValueError (other species or mixed species, N != 2,
initial velocity, separation outside [3.0, 3.5], duration > 1.0).
"""
import math

L = 10.0
H = 0.001
P = 2.5
T_MAX = 1.0
R_LO, R_HI = 3.0, 3.5
NODE_R = [2.5, 3.0, 3.5]
NODE_K = {
    "A": [16.941, 18.034, 18.285],
    "C": [12.730, 13.202, 13.184],
}


def K(species, q):
    nk = NODE_K[species]
    if q <= NODE_R[0]:
        return nk[0]
    if q >= NODE_R[-1]:
        return nk[-1]
    for k in range(len(NODE_R) - 1):
        if NODE_R[k] <= q <= NODE_R[k + 1]:
            f = (q - NODE_R[k]) / (NODE_R[k + 1] - NODE_R[k])
            return nk[k] + f * (nk[k + 1] - nk[k])
    raise ValueError("unreachable")


def _accel(species, pos):
    (x0, y0), (x1, y1) = pos
    dx, dy = x1 - x0, y1 - y0
    q = math.hypot(dx, dy)
    f = K(species, q) / q ** (P + 1)
    return [[f * dx, f * dy], [-f * dx, -f * dy]]


def _step(species, pos, vel, h):
    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(2)]

    k1p, k1v = vel, _accel(species, pos)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, _accel(species, p2)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, _accel(species, p3)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, _accel(species, p4)
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
        raise ValueError("claim covers exactly two particles")
    species = parts[0]["species"]
    if species not in NODE_K or any(p["species"] != species for p in parts):
        raise ValueError("claim covers A-A or C-C pairs only (one species, A or C)")
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    if any(abs(c) > 0.0 for v in vel for c in v):
        raise ValueError("claim covers particles at rest only")
    r0 = math.dist(pos[0], pos[1])
    if not R_LO <= r0 <= R_HI:
        raise ValueError("initial separation outside [3.0, 3.5]")
    dur = float(setup["duration"])
    if dur > T_MAX + 1e-12:
        raise ValueError("duration beyond the claim's window (T <= 1.0)")
    dt = float(setup["sample_dt"])
    n_samp = int(round(dur / dt))
    samples = []
    t = 0.0
    for i in range(n_samp + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = _step(species, pos, vel, h)
            t += h
        t = target
        samples.append({
            "t": target,
            "particles": [{"id": pid, "species": species, "pos": [pos[pid][0], pos[pid][1]]}
                          for pid in range(2)],
        })
    return samples
