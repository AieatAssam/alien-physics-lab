"""Two-body integrated fit of per-particle coefficients for an at-rest pair.

Usage: python3 -I pair_fit_integrated.py <request.json> <result.json> <tmax> [P]

Model: particle i accelerates toward partner j with magnitude K_i / r^P
(K_i is the per-particle coefficient, i.e. a_i(j) = K_i / r^P at separation r).
Initial state (positions, zero velocity) comes from the request file.
Fits K_0, K_1 (2D grid, then refinement) to the tracker positions for
0 < t <= tmax, both coordinates, minimising the sum of squared residuals.
Also reports the rms residual per coordinate at the best fit.
Pure Python, RK4 with step 0.002 (internal; samples are taken at their own times
by interpolating from the integrated grid, step set so each sample time is hit).
"""
import json
import math
import sys


def simulate(x0, K, P, times):
    """Integrate the two particles from rest at x0; return positions at each time."""
    pos = [list(x0[0]), list(x0[1])]
    vel = [[0.0, 0.0], [0.0, 0.0]]

    def acc(p):
        dx = p[1][0] - p[0][0]
        dy = p[1][1] - p[0][1]
        r = math.hypot(dx, dy)
        if r < 1e-9:
            return [[0.0, 0.0], [0.0, 0.0]]
        f0 = K[0] / r ** P
        f1 = K[1] / r ** P
        return [[f0 * dx / r, f0 * dy / r], [-f1 * dx / r, -f1 * dy / r]]

    out = []
    t = 0.0
    h0 = 0.002
    for target in times:
        while t < target - 1e-12:
            h = min(h0, target - t)
            a1 = acc(pos)
            p2 = [[pos[i][k] + 0.5 * h * vel[i][k] for k in range(2)] for i in range(2)]
            v2 = [[vel[i][k] + 0.5 * h * a1[i][k] for k in range(2)] for i in range(2)]
            a2 = acc(p2)
            p3 = [[pos[i][k] + 0.5 * h * v2[i][k] for k in range(2)] for i in range(2)]
            v3 = [[vel[i][k] + 0.5 * h * a2[i][k] for k in range(2)] for i in range(2)]
            a3 = acc(p3)
            p4 = [[pos[i][k] + h * v3[i][k] for k in range(2)] for i in range(2)]
            v4 = [[vel[i][k] + h * a3[i][k] for k in range(2)] for i in range(2)]
            a4 = acc(p4)
            for i in range(2):
                for k in range(2):
                    pos[i][k] += h / 6 * (vel[i][k] + 2 * v2[i][k] + 2 * v3[i][k] + v4[i][k])
                    vel[i][k] += h / 6 * (a1[i][k] + 2 * a2[i][k] + 2 * a3[i][k] + a4[i][k])
            t += h
        out.append([[pos[0][0], pos[0][1]], [pos[1][0], pos[1][1]]])
    return out


def sse(x0, K, P, data):
    times = [t for t, _ in data]
    traj = simulate(x0, K, P, times)
    s = 0.0
    n = 0
    for (t, obs), sim in zip(data, traj):
        for i in range(2):
            for k in range(2):
                s += (obs[i][k] - sim[i][k]) ** 2
                n += 1
    return s, n


def main():
    req = json.load(open(sys.argv[1]))
    res = json.load(open(sys.argv[2]))
    tmax = float(sys.argv[3])
    P = float(sys.argv[4]) if len(sys.argv) > 4 else 2.5
    parts = req["setup"]["particles"]
    x0 = [p["pos"] for p in parts]
    species = [p["species"] for p in parts]
    data = []
    for s in res["samples"]:
        t = float(s["t"])
        if 0 < t <= tmax + 1e-12:
            data.append((t, [s["particles"][0]["pos"], s["particles"][1]["pos"]]))

    best = None
    # coarse grid
    for a in range(0, 41):
        K0 = 0.5 * a
        for b in range(0, 41):
            K1 = 0.5 * b
            v, n = sse(x0, (K0, K1), P, data)
            if best is None or v < best[0]:
                best = (v, K0, K1)
    # refinement
    v0, K0c, K1c = best
    step = 0.5
    while step > 0.01:
        improved = True
        while improved:
            improved = False
            for dK0, dK1 in [(step, 0), (-step, 0), (0, step), (0, -step), (step, step), (-step, -step), (step, -step), (-step, step)]:
                K0n, K1n = K0c + dK0, K1c + dK1
                v, n = sse(x0, (K0n, K1n), P, data)
                if v < v0:
                    v0, K0c, K1c = v, K0n, K1n
                    improved = True
        step /= 2
    _, n = sse(x0, (K0c, K1c), P, data)
    rms = math.sqrt(v0 / n)
    print(f"{req['request_id']} species {species} r0={math.dist(x0[0], x0[1]):.2f} tmax={tmax:g} P={P:g} "
          f"n_samples={len(data)} K0={K0c:.3f} ({species[0]} on {species[1]}) "
          f"K1={K1c:.3f} ({species[1]} on {species[0]}) rms/coord={rms:.4f}")


if __name__ == "__main__":
    main()
