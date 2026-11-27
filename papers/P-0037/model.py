"""P-0036 predictor (lab-keystone): two A particles at rest, initial separation 3.5 to 9.0.

Each particle accelerates toward the other with magnitude K(r) / r^2.5, where r is the current separation and K(r) is
piecewise-linear in r through the nodes below (held flat outside [2.5, 9.0]). Specular walls at 0 and L = 10.
RK4 with internal step H = 0.002. Imports only math.

Node values: r = 2.5, 3.0, 3.5 from the P-0034 A table (lab-vernier); r = 5..9 from the P-0029 table (lab-a).
Between 3.5 and 5.0 the table is a straight line (not measured directly; see paper.md).

Input contract: exactly two A particles, both at rest, initial separation in [3.5, 9.0]. Other setups raise ValueError.
Window: if the predicted separation falls below 2.5 at any output sample, predict() raises ValueError. The claim
makes no prediction there (contact behaviour is not modelled; see paper.md).
"""
import math

L = 10.0
P = 2.5
H = 0.002
R_LO, R_HI = 3.5, 9.0
R_NODES = [2.5, 3.0, 3.5, 5.0, 6.0, 7.0, 8.0, 9.0]
K_NODES = [16.941, 18.034, 18.285, 17.834, 16.617, 15.121, 13.432, 11.624]
R_MIN_FORCE = 0.05  # guard against division by ~0 at contact; not a claimed behaviour
R_WINDOW_MIN = 2.5  # predict() refuses durations in which the pair comes closer than this


def _k(r):
    if r <= R_NODES[0]:
        return K_NODES[0]
    if r >= R_NODES[-1]:
        return K_NODES[-1]
    for i in range(len(R_NODES) - 1):
        if R_NODES[i] <= r <= R_NODES[i + 1]:
            f = (r - R_NODES[i]) / (R_NODES[i + 1] - R_NODES[i])
            return K_NODES[i] + f * (K_NODES[i + 1] - K_NODES[i])
    return K_NODES[-1]


def _accel(pa, pb):
    dx = pb[0] - pa[0]
    dy = pb[1] - pa[1]
    r = max(math.hypot(dx, dy), R_MIN_FORCE)
    f = _k(r) / r ** P / r
    return (f * dx, f * dy), (-f * dx, -f * dy)


def _step(pa, va, pb, vb, h):
    a1, b1 = _accel(pa, pb)
    pa2 = [pa[i] + h / 2 * va[i] for i in range(2)]
    pb2 = [pb[i] + h / 2 * vb[i] for i in range(2)]
    va2 = [va[i] + h / 2 * a1[i] for i in range(2)]
    vb2 = [vb[i] + h / 2 * b1[i] for i in range(2)]
    a2, b2 = _accel(pa2, pb2)
    pa3 = [pa[i] + h / 2 * va2[i] for i in range(2)]
    pb3 = [pb[i] + h / 2 * vb2[i] for i in range(2)]
    va3 = [va[i] + h / 2 * a2[i] for i in range(2)]
    vb3 = [vb[i] + h / 2 * b2[i] for i in range(2)]
    a3, b3 = _accel(pa3, pb3)
    pa4 = [pa[i] + h * va3[i] for i in range(2)]
    pb4 = [pb[i] + h * vb3[i] for i in range(2)]
    va4 = [va[i] + h * a3[i] for i in range(2)]
    vb4 = [vb[i] + h * b3[i] for i in range(2)]
    a4, b4 = _accel(pa4, pb4)
    npa = [pa[i] + h / 6 * (va[i] + 2 * va2[i] + 2 * va3[i] + va4[i]) for i in range(2)]
    npb = [pb[i] + h / 6 * (vb[i] + 2 * vb2[i] + 2 * vb3[i] + vb4[i]) for i in range(2)]
    nva = [va[i] + h / 6 * (a1[i] + 2 * a2[i] + 2 * a3[i] + a4[i]) for i in range(2)]
    nvb = [vb[i] + h / 6 * (b1[i] + 2 * b2[i] + 2 * b3[i] + b4[i]) for i in range(2)]
    for p, v in ((npa, nva), (npb, nvb)):
        for i in range(2):
            if p[i] < 0.0:
                p[i] = -p[i]
                v[i] = -v[i]
            elif p[i] > L:
                p[i] = 2 * L - p[i]
                v[i] = -v[i]
    return npa, nva, npb, nvb


def predict(setup):
    parts = setup["particles"]
    if len(parts) != 2:
        raise ValueError("claim covers exactly two particles")
    if any(p["species"] != "A" for p in parts):
        raise ValueError("claim covers species A only")
    pa = [float(parts[0]["pos"][0]), float(parts[0]["pos"][1])]
    pb = [float(parts[1]["pos"][0]), float(parts[1]["pos"][1])]
    if any(float(v) != 0.0 for p in parts for v in p["vel"]):
        raise ValueError("claim covers particles at rest only")
    r0 = math.dist(pa, pb)
    if not R_LO - 1e-9 <= r0 <= R_HI + 1e-9:
        raise ValueError("initial separation outside [3.5, 9.0]")
    dur = float(setup["duration"])
    dt = float(setup["sample_dt"])
    n_samp = int(round(dur / dt))
    va = [0.0, 0.0]
    vb = [0.0, 0.0]
    samples = []
    t = 0.0
    for i in range(n_samp + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pa, va, pb, vb = _step(pa, va, pb, vb, h)
            t += h
        t = target
        samples.append({
            "t": target,
            "particles": [
                {"id": 0, "species": "A", "pos": [float(pa[0]), float(pa[1])]},
                {"id": 1, "species": "A", "pos": [float(pb[0]), float(pb[1])]},
            ],
        })
        if math.dist(pa, pb) < R_WINDOW_MIN:
            raise ValueError("pair separation falls below 2.5 within the duration: outside the claim window")
    return samples
