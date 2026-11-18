"""Round 3 at-rest pair series (r3/001-008). Pure python, no numpy.
Per particle and per coordinate, fit c(t) = c0 + v0 t + 0.5 a t^2 by least squares.
Reports the x-acceleration of each particle toward its partner (pair axis = x).
Usage: python3 -I pair_rest_r3.py <results_dir>"""
import json, sys, os, math

RES = sys.argv[1]


def solve3(M, b):
    # Gaussian elimination for 3x3
    M = [row[:] + [b[i]] for i, row in enumerate(M)]
    n = 3
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[piv] = M[piv], M[i]
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                for c in range(i, n + 1):
                    M[r][c] -= f * M[i][c]
    return [M[i][n] / M[i][i] for i in range(n)]


def quad_fit(t, y):
    # basis [1, t, 0.5 t^2]
    B = [[1.0, ti, 0.5 * ti * ti] for ti in t]
    M = [[sum(B[k][i] * B[k][j] for k in range(len(t))) for j in range(3)] for i in range(3)]
    b = [sum(B[k][i] * y[k] for k in range(len(t))) for i in range(3)]
    c = solve3(M, b)
    res = [y[k] - sum(c[i] * B[k][i] for i in range(3)) for k in range(len(t))]
    sd = math.sqrt(sum(r * r for r in res) / (len(t) - 3))
    return c, sd


print(f"{'run':>4} {'x0_p0':>6} {'x0_p1':>6} {'sep':>5} {'T':>4} {'N':>4} {'cost':>6} "
      f"{'a_p0_x':>9} {'a_p1_x':>9} {'a_p0_y':>9} {'a_p1_y':>9} {'res_sd':>7} {'events':>6}")
for n in range(1, 9):
    with open(os.path.join(RES, f"{n:03d}.json")) as f:
        r = json.load(f)
    s = r["samples"]
    t = [q["t"] for q in s]
    P = {0: [], 1: []}
    for q in s:
        for p in q["particles"]:
            P[p["id"]].append(p["pos"])
    sep = P[1][0][0] - P[0][0][0]
    fits = {}
    sds = []
    for i in (0, 1):
        for c in (0, 1):
            coef, sd = quad_fit(t, [pos[c] for pos in P[i]])
            fits[(i, c)] = coef
            sds.append(sd)
    rsd = sum(sds) / len(sds)
    print(f"{n:>4} {P[0][0][0]:>6.2f} {P[1][0][0]:>6.2f} {sep:>5.2f} {t[-1]:>4.1f} {len(t):>4} {r['cost']:>6.2f} "
          f"{2*fits[(0,0)][2]:>9.4f} {2*fits[(1,0)][2]:>9.4f} {2*fits[(0,1)][2]:>9.4f} {2*fits[(1,1)][2]:>9.4f} "
          f"{rsd:>7.4f} {len(r['events']):>6}")
