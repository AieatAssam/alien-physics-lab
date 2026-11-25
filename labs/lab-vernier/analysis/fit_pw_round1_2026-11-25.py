"""Piecewise-linear K(r) fit for A-A and C-C pairs at rest, separation 2.5-3.5 (lab-vernier, round 2).

Model per particle pair (same species s): acceleration magnitude K(q)/q^2.5 toward the partner,
q = current separation, K(q) linear in q between nodes 2.5, 3.0, 3.5 and held at the end values outside.
Fit: 3 node values, joint over all runs of one species pair, on each run's pre-contact window
(t up to the first measured separation below 1.5). RK4 step 0.002, specular walls.
Judge-style error = sqrt(mean squared coordinate residual)/10.
Run: python3 -I fit_pw_round1_2026-11-25.py [AA|CC] [all|H|V]
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit_tools as ft  # noqa: E402

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
DATE = "2026-11-25/r1/lab-vernier"
NODES = [2.5, 3.0, 3.5]
RUNS = {
    "AA": [("006", "H"), ("007", "V"), ("008", "H"), ("009", "V"), ("010", "H"), ("011", "V")],
    "CC": [("012", "H"), ("013", "V"), ("014", "H"), ("015", "V"), ("016", "H"), ("017", "V")],
}
L = 10.0
H_STEP = 0.002


def K_of(q, nodeK):
    if q <= NODES[0]:
        return nodeK[0]
    if q >= NODES[-1]:
        return nodeK[-1]
    for k in range(len(NODES) - 1):
        if NODES[k] <= q <= NODES[k + 1]:
            f = (q - NODES[k]) / (NODES[k + 1] - NODES[k])
            return nodeK[k] + f * (nodeK[k + 1] - nodeK[k])
    raise ValueError


def acc(pos, nodeK):
    (x0, y0), (x1, y1) = pos
    dx, dy = x1 - x0, y1 - y0
    q = math.hypot(dx, dy)
    f = K_of(q, nodeK) / q ** 3.5  # magnitude K/q^2.5 along the unit vector: K/q^2.5 * (dx/q)
    return [f * dx, f * dy], [-f * dx, -f * dy]


def step(pos, vel, h, nodeK):
    a0, a1 = acc(pos, nodeK)

    def add(p, v, s):
        return [[p[i][k] + s * v[i][k] for k in range(2)] for i in range(2)]

    k1v = [a0, a1]
    k1p = vel
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    b0, b1 = acc(p2, nodeK)
    k2p, k2v = v2, [b0, b1]
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    c0, c1 = acc(p3, nodeK)
    k3p, k3v = v3, [c0, c1]
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    d0, d1 = acc(p4, nodeK)
    k4p, k4v = v4, [d0, d1]
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)] for i in range(2)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)] for i in range(2)]
    for i in range(2):
        for k in range(2):
            if newp[i][k] < 0:
                newp[i][k] = -newp[i][k]
                newv[i][k] = -newv[i][k]
            elif newp[i][k] > L:
                newp[i][k] = 2 * L - newp[i][k]
                newv[i][k] = -newv[i][k]
    return newp, newv


def sse_run(setup, res, nodeK, tmax):
    pos = [list(p["pos"]) for p in setup["particles"]]
    vel = [[0.0, 0.0], [0.0, 0.0]]
    se, n = 0.0, 0
    t = 0.0
    for s in res["samples"]:
        target = s["t"]
        if target > tmax + 1e-12:
            break
        while t < target - 1e-12:
            h = min(H_STEP, target - t)
            pos, vel = step(pos, vel, h, nodeK)
            t += h
        for i, p in enumerate(s["particles"]):
            se += (p["pos"][0] - pos[i][0]) ** 2 + (p["pos"][1] - pos[i][1]) ** 2
            n += 2
    return se, n


def window_end(res, rmin=1.5):
    for s in res["samples"]:
        p = s["particles"]
        if math.dist(p[0]["pos"], p[1]["pos"]) < rmin:
            return s["t"] - 1e-9
    return res["samples"][-1]["t"]


def load(pair, orient_filter):
    out = []
    for num, o in RUNS[pair]:
        if orient_filter != "all" and o != orient_filter:
            continue
        rid = f"{DATE}/{num}"
        req = ft.load_json(f"{REPO}/requests/{rid}.json")
        res = ft.load_json(f"{REPO}/results/{rid}.json")
        out.append((rid, o, req["setup"], res, window_end(res)))
    return out


def total_sse(data, nodeK):
    se, n = 0.0, 0
    for _, _, setup, res, tm in data:
        a, b = sse_run(setup, res, nodeK, tm)
        se += a
        n += b
    return se, n


def fit_nodes(data, k0):
    nodeK = list(k0)
    lo, hi = min(k0) - 6, max(k0) + 6
    for _ in range(3):
        for j in range(3):
            # golden section on node j
            a, b = lo, hi
            g = (math.sqrt(5) - 1) / 2
            c, d = b - g * (b - a), a + g * (b - a)

            def f(v):
                trial = list(nodeK)
                trial[j] = v
                return total_sse(data, trial)[0]
            fc, fd = f(c), f(d)
            for _ in range(40):
                if fc < fd:
                    b, d, fd = d, c, fc
                    c = b - g * (b - a)
                    fc = f(c)
                else:
                    a, c, fc = c, d, fd
                    d = a + g * (b - a)
                    fd = f(d)
            nodeK[j] = (a + b) / 2
    return nodeK


if __name__ == "__main__":
    pair = sys.argv[1] if len(sys.argv) > 1 else "AA"
    of = sys.argv[2] if len(sys.argv) > 2 else "all"
    k0 = [17.7, 17.7, 17.7] if pair == "AA" else [12.9, 13.1, 13.2]
    data = load(pair, of)
    nodeK = fit_nodes(data, k0)
    se, n = total_sse(data, nodeK)
    print(f"{pair} orient={of} nodes K(2.5,3.0,3.5) = " + ", ".join(f"{v:.3f}" for v in nodeK)
          + f"  pooled rms/coord={math.sqrt(se / n):.4f}  judge-style={math.sqrt(se / n) / L:.5f}")
    for rid, o, setup, res, tm in data:
        a, b = sse_run(setup, res, nodeK, tm)
        print(f"  {rid[-3:]} {o} window_end={tm:.3f} rms/coord={math.sqrt(a / b):.4f}")
