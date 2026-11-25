"""P-0031 predictor (lab-b, Icarus): three or four A particles at rest, pairwise sum of the P-0027 table.

Each ordered pair (i, j) gives particle i an acceleration of magnitude K(r)/r**2.5 toward j, where r is the current
separation and K(r) is the piecewise-linear P-0027 table (nodes 3 to 9, held at the end values outside [3, 9]).
Accelerations add (no three-body term). RK4 with step 0.001; specular walls at 0 and L = 10. Imports only math.

Domain: species A only; 3 or 4 particles; all at rest; every initial pairwise distance in [5.0, 7.1]; duration <= 2.0.
Other inputs raise ValueError.
"""
import math

L = 10.0
H = 0.001
P = 2.5
R_LO, R_HI = 5.0, 7.1
N_MIN, N_MAX = 3, 4
T_MAX = 2.0

NODE_R = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
NODE_K = [17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624]


def K(r):
    if r <= NODE_R[0]:
        return NODE_K[0]
    if r >= NODE_R[-1]:
        return NODE_K[-1]
    for k in range(len(NODE_R) - 1):
        if NODE_R[k] <= r <= NODE_R[k + 1]:
            w = (r - NODE_R[k]) / (NODE_R[k + 1] - NODE_R[k])
            return NODE_K[k] + w * (NODE_K[k + 1] - NODE_K[k])
    raise ValueError("unreachable")


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
            g = K(r) / r ** (P + 1)
            acc[i][0] += g * dx
            acc[i][1] += g * dy
    return acc


def _step(pos, vel, h):
    n = len(pos)

    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]

    k1p, k1v = vel, _accel(pos)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, _accel(p2)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, _accel(p3)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, _accel(p4)
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)]
            for i in range(n)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)]
            for i in range(n)]
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
    if not N_MIN <= n <= N_MAX:
        raise ValueError("claim covers 3 or 4 particles")
    if any(p["species"] != "A" for p in parts):
        raise ValueError("claim covers species A only")
    if any(float(c) != 0.0 for p in parts for c in p["vel"]):
        raise ValueError("claim covers particles at rest only")
    pos0 = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    dists = [math.dist(pos0[i], pos0[j]) for i in range(n) for j in range(i + 1, n)]
    if min(dists) < R_LO - 1e-3 or max(dists) > R_HI + 1e-3:
        raise ValueError("an initial pairwise distance is outside [5.0, 7.1]")
    dur = float(setup["duration"])
    if dur > T_MAX + 1e-9:
        raise ValueError("duration beyond the claim window (2.0)")
    dt = float(setup["sample_dt"])
    n_samp = int(round(dur / dt))
    steps_per = int(round(dt / H))
    if abs(steps_per * H - dt) > 1e-9:
        raise ValueError("sample_dt must be a multiple of 0.001")
    pos = [list(p) for p in pos0]
    vel = [[0.0, 0.0] for _ in range(n)]
    samples = [{"t": 0.0, "particles": [{"id": i, "species": "A", "pos": list(pos[i])} for i in range(n)]}]
    for s in range(1, n_samp + 1):
        for _ in range(steps_per):
            pos, vel = _step(pos, vel, H)
        t = round(s * dt, 9)
        samples.append({"t": t, "particles": [{"id": i, "species": "A", "pos": [pos[i][0], pos[i][1]]}
                                              for i in range(n)]})
    return samples
