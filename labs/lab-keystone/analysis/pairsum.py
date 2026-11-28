"""Pairwise-sum extension of the P-0036 charge-mass pair law to N bodies (lab-keystone, 2026-11-28).

Used only to predict the grant setup (4 particles) and to check the N-body discrimination.
Law per ordered pair (i, j): accel_i += q_i q_j K(r) / r**2.5 * (x_j - x_i) / r / m_i   (K, q, m as in P-0036 model.py).
Specular walls at 0 and 10, RK4 h = 1e-3. numpy-free so it runs with -I.
"""
import math

L = 10.0
P = 2.5
R_TAB = [5.0, 6.0, 7.0, 8.0, 9.0]
K_TAB = [17.834, 16.617, 15.121, 13.432, 11.624]
Q = {"A": 1.0, "B": 0.5, "C": -0.5}
M = {"A": 1.0, "B": 0.72, "C": 0.42}


def K(r):
    if r <= R_TAB[0]:
        return K_TAB[0]  # flat clamp below 5, as in P-0036
    if r >= R_TAB[-1]:
        return K_TAB[-1]
    for i in range(len(R_TAB) - 1):
        if R_TAB[i] <= r <= R_TAB[i + 1]:
            f = (r - R_TAB[i]) / (R_TAB[i + 1] - R_TAB[i])
            return K_TAB[i] + f * (K_TAB[i + 1] - K_TAB[i])


def simulate(species, pos, vel, T, dt, h=1e-3, kscale=1.0):
    n = len(species)
    pos = [list(p) for p in pos]
    vel = [list(v) for v in vel]

    def acc(p):
        a = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dx = p[j][0] - p[i][0]
                dy = p[j][1] - p[i][1]
                r = math.hypot(dx, dy)
                f = kscale * Q[species[i]] * Q[species[j]] * K(r) / r ** P / r / M[species[i]]
                a[i][0] += f * dx
                a[i][1] += f * dy
        return a

    def step(p, v, hh):
        a1 = acc(p)
        p2 = [[p[i][k] + hh / 2 * v[i][k] for k in range(2)] for i in range(n)]
        v2 = [[v[i][k] + hh / 2 * a1[i][k] for k in range(2)] for i in range(n)]
        a2 = acc(p2)
        p3 = [[p[i][k] + hh / 2 * v2[i][k] for k in range(2)] for i in range(n)]
        v3 = [[v[i][k] + hh / 2 * a2[i][k] for k in range(2)] for i in range(n)]
        a3 = acc(p3)
        p4 = [[p[i][k] + hh * v3[i][k] for k in range(2)] for i in range(n)]
        v4 = [[v[i][k] + hh * a3[i][k] for k in range(2)] for i in range(n)]
        a4 = acc(p4)
        np_ = [[p[i][k] + hh / 6 * (v[i][k] + 2 * v2[i][k] + 2 * v3[i][k] + v4[i][k]) for k in range(2)] for i in range(n)]
        nv = [[v[i][k] + hh / 6 * (a1[i][k] + 2 * a2[i][k] + 2 * a3[i][k] + a4[i][k]) for k in range(2)] for i in range(n)]
        for i in range(n):
            for k in range(2):
                if np_[i][k] < 0.0:
                    np_[i][k] = -np_[i][k]
                    nv[i][k] = -nv[i][k]
                elif np_[i][k] > L:
                    np_[i][k] = 2 * L - np_[i][k]
                    nv[i][k] = -nv[i][k]
        return np_, nv

    out = [[list(p) for p in pos]]
    t = 0.0
    nsamp = int(round(T / dt))
    for m_ in range(1, nsamp + 1):
        target = round(m_ * dt, 9)
        while t < target - 1e-12:
            hh = min(h, target - t)
            pos, vel = step(pos, vel, hh)
            t += hh
        t = target
        out.append([list(p) for p in pos])
    return out


def min_pair_dist(traj):
    best = 1e9
    for frame in traj:
        for i in range(len(frame)):
            for j in range(i + 1, len(frame)):
                best = min(best, math.dist(frame[i], frame[j]))
    return best
