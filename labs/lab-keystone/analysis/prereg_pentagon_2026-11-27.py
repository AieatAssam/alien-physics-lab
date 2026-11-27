"""Pre-registered additive prediction for an N=5 A pentagon at rest (grant proposal, 2026-11-27).

Model: each particle accelerates toward each other particle with K(r)/r^2.5, K(r) piecewise-linear
in the P-0029 table (nodes 5..9). Pure Python (numpy not installed). Walls at 0 and 10, specular.
Prints min pair distance along the trajectory so the duration can be checked against close approach.
"""
import math

L = 10.0
P = 2.5
R_TAB = [5.0, 6.0, 7.0, 8.0, 9.0]
K_TAB = [17.834, 16.617, 15.121, 13.432, 11.624]
H = 0.001
SIDE = 5.0


def k_of_r(r):
    if r <= R_TAB[0]:
        return K_TAB[0]
    if r >= R_TAB[-1]:
        return K_TAB[-1]
    for i in range(len(R_TAB) - 1):
        if R_TAB[i] <= r <= R_TAB[i + 1]:
            f = (r - R_TAB[i]) / (R_TAB[i + 1] - R_TAB[i])
            return K_TAB[i] + f * (K_TAB[i + 1] - K_TAB[i])
    raise ValueError(r)


def pentagon(side=SIDE, centre=(5.0, 5.0)):
    R = side / (2.0 * math.sin(math.pi / 5.0))
    pts = []
    for k in range(5):
        th = math.pi / 2 + 2 * math.pi * k / 5
        pts.append([centre[0] + R * math.cos(th), centre[1] + R * math.sin(th)])
    return pts


def accel(pos):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            a = k_of_r(r) / r ** P
            acc[i][0] += a * dx / r
            acc[i][1] += a * dy / r
    return acc


def step(pos, vel, h):
    n = len(pos)
    k1v = accel(pos)
    p2 = [[pos[i][c] + h / 2 * vel[i][c] for c in range(2)] for i in range(n)]
    v2 = [[vel[i][c] + h / 2 * k1v[i][c] for c in range(2)] for i in range(n)]
    k2v = accel(p2)
    p3 = [[pos[i][c] + h / 2 * v2[i][c] for c in range(2)] for i in range(n)]
    v3 = [[vel[i][c] + h / 2 * k2v[i][c] for c in range(2)] for i in range(n)]
    k3v = accel(p3)
    p4 = [[pos[i][c] + h * v3[i][c] for c in range(2)] for i in range(n)]
    v4 = [[vel[i][c] + h * k3v[i][c] for c in range(2)] for i in range(n)]
    k4v = accel(p4)
    newp = [[pos[i][c] + h / 6 * (vel[i][c] + 2 * v2[i][c] + 2 * v3[i][c] + v4[i][c]) for c in range(2)] for i in range(n)]
    newv = [[vel[i][c] + h / 6 * (k1v[i][c] + 2 * k2v[i][c] + 2 * k3v[i][c] + k4v[i][c]) for c in range(2)] for i in range(n)]
    for i in range(n):
        for c in range(2):
            if newp[i][c] < 0.0:
                newp[i][c] = -newp[i][c]
                newv[i][c] = -newv[i][c]
            elif newp[i][c] > L:
                newp[i][c] = 2 * L - newp[i][c]
                newv[i][c] = -newv[i][c]
    return newp, newv


def run(pos, T, dt_out=0.001):
    vel = [[0.0, 0.0] for _ in pos]
    t = 0.0
    min_d = min(math.dist(pos[i], pos[j]) for i in range(len(pos)) for j in range(i + 1, len(pos)))
    samples = [(0.0, [list(p) for p in pos])]
    n_out = int(round(T / dt_out))
    for m in range(1, n_out + 1):
        target = m * dt_out
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = step(pos, vel, h)
            t += h
            for i in range(len(pos)):
                for j in range(i + 1, len(pos)):
                    min_d = min(min_d, math.dist(pos[i], pos[j]))
        samples.append((target, [list(p) for p in pos]))
    return samples, min_d


if __name__ == "__main__":
    import sys
    P0 = pentagon()
    for T in (1.0, 1.5, 2.0):
        s, md = run(P0, T, dt_out=0.1)
        print("T=%.1f  min pair distance over trajectory = %.3f  final centre-to-particle r = %.3f"
              % (T, md, math.dist(s[-1][1][0], [5.0, 5.0])))
