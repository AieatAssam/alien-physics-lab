"""Design check for an A-A exponent test: how far apart are P=2.10 (P-0024 law) and the best-fit P=2.5 law
on a candidate run? Pure two-body RK4, same geometry as the request. Usage: python3 -I exponent_design_2026-11-23.py
Reports RMSE/L between the P=2.10 prediction and the best-fit P=2.5 prediction (fit G on the same trajectory).
"""
import math
L = 10.0

def sim(G, P, r0, T, dt, h=0.0005):
    x0, y0 = 5.0 - r0 / 2, 5.0
    pos = [[x0, y0], [5.0 + r0 / 2, y0]]
    vel = [[0.0, 0.0], [0.0, 0.0]]
    def acc(p):
        out = []
        for i in range(2):
            j = 1 - i
            dx, dy = p[j][0] - p[i][0], p[j][1] - p[i][1]
            r = math.hypot(dx, dy)
            a = 0.5 * G / r ** P
            out.append([a * dx / r, a * dy / r])
        return out
    t, res = 0.0, []
    n = int(round(T / dt))
    for k in range(1, n + 1):
        target = k * dt
        while t < target - 1e-12:
            s = min(h, target - t)
            a1 = acc(pos); v1 = vel
            p2 = [[pos[i][c] + s / 2 * v1[i][c] for c in range(2)] for i in range(2)]
            v2 = [[vel[i][c] + s / 2 * a1[i][c] for c in range(2)] for i in range(2)]
            a2 = acc(p2)
            p3 = [[pos[i][c] + s / 2 * v2[i][c] for c in range(2)] for i in range(2)]
            v3 = [[vel[i][c] + s / 2 * a2[i][c] for c in range(2)] for i in range(2)]
            a3 = acc(p3)
            p4 = [[pos[i][c] + s * v3[i][c] for c in range(2)] for i in range(2)]
            v4 = [[vel[i][c] + s * a3[i][c] for c in range(2)] for i in range(2)]
            a4 = acc(p4)
            pos = [[pos[i][c] + s / 6 * (v1[i][c] + 2 * v2[i][c] + 2 * v3[i][c] + v4[i][c]) for c in range(2)] for i in range(2)]
            vel = [[vel[i][c] + s / 6 * (a1[i][c] + 2 * a2[i][c] + 2 * a3[i][c] + a4[i][c]) for c in range(2)] for i in range(2)]
            t += s
        res.append([list(p) for p in pos])
    return res

def rmse(a, b):
    se = [(a[k][i][c] - b[k][i][c]) ** 2 for k in range(len(a)) for i in range(2) for c in range(2)]
    return math.sqrt(sum(se) / len(se)) / L

if __name__ == "__main__":
    for r0, T, dt in [(2.9, 0.6, 0.001), (1.5, 0.3, 0.0005)]:
        ref = sim(23.63, 2.099, r0, T, dt)  # P-0024 law (G/2 per particle, same as model.py)
        best = None
        for G in [x / 100 for x in range(1500, 3500, 5)]:
            pr = sim(G, 2.5, r0, T, dt, h=0.001)
            e = rmse(ref, pr)
            if best is None or e < best[0]:
                best = (e, G)
        print(f"r0={r0} T={T} dt={dt}: best P=2.5 fit G={best[1]:.2f}, RMSE/L vs P=2.10 law = {best[0]:.5f}")
