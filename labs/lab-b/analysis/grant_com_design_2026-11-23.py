"""Design check for tonight's grant: centre-of-mass test of equal-and-opposite pair forces (N = 3).
Own N-body RK4 with specular walls (K > 0 attraction, K < 0 repulsion). Couplings near fitted values
(r-independent here, so this is a design check, not a prediction).
Masses m_A : m_B : m_C = 2.37 : 1.69 : 1 (from K_BA/K_AB = m_A/m_B = 1.40 and K_CA/K_AC = m_A/m_C = 2.37).
Reports wall distance, minimum pair separation, and centre-of-mass drift under predicted and equal masses.
Usage: python3 -I grant_com_design_2026-11-23.py
"""
import math

L, P, H = 10.0, 2.5, 0.002
COUP = {("A", "B"): 8.0, ("B", "A"): 11.4, ("A", "C"): -7.5, ("C", "A"): -17.8,
        ("B", "C"): -6.0, ("C", "B"): -10.2}  # ratio 1.70 = m_B/m_C
MASS = {"A": 2.37, "B": 1.69, "C": 1.0}  # m_A/m_B = 1.40, m_A/m_C = 2.37, m_B/m_C = 1.69


def accel(pos, sp):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx, dy = pos[j][0] - pos[i][0], pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            a = COUP[(sp[i], sp[j])] / r ** P
            acc[i][0] += a * dx / r
            acc[i][1] += a * dy / r
    return acc


def step(pos, vel, sp, h):
    n = len(pos)
    add = lambda a, b, s: [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]
    k1p, k1v = vel, accel(pos, sp)
    k2p, k2v = add(vel, k1v, h / 2), accel(add(pos, k1p, h / 2), sp)
    k3p, k3v = add(vel, k2v, h / 2), accel(add(pos, k2p, h / 2), sp)
    k4p, k4v = add(vel, k3v, h), accel(add(pos, k3p, h), sp)
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)] for i in range(n)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)] for i in range(n)]
    for i in range(n):
        for k in range(2):
            if newp[i][k] < 0.0:
                newp[i][k] = -newp[i][k]; newv[i][k] = -newv[i][k]
            elif newp[i][k] > L:
                newp[i][k] = 2 * L - newp[i][k]; newv[i][k] = -newv[i][k]
    return newp, newv


def simulate(parts, T, dt=0.01):
    sp = [s for s, _ in parts]
    pos = [list(map(float, p)) for _, p in parts]
    vel = [[0.0, 0.0] for _ in parts]
    frames, t = [(0.0, [list(p) for p in pos])], 0.0
    for i in range(1, int(round(T / dt)) + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = step(pos, vel, sp, h)
            t += h
        frames.append((target, [list(p) for p in pos]))
    return sp, frames


def com(frame, masses):
    M = sum(masses)
    return (sum(m * frame[i][0] for i, m in enumerate(masses)) / M,
            sum(m * frame[i][1] for i, m in enumerate(masses)) / M)


def report(name, parts, T=10.0):
    sp, frames = simulate(parts, T)
    wall = min(min(x, L - x, y, L - y) for _, fr in frames for x, y in fr)
    seps = [math.dist(fr[i], fr[j]) for _, fr in frames for i in range(len(fr)) for j in range(i + 1, len(fr))]
    mp = [MASS[s] for s in sp]
    me = [1.0] * len(sp)
    c0p, c0e = com(frames[0][1], mp), com(frames[0][1], me)
    drift_p = max(math.dist(com(fr, mp), c0p) for _, fr in frames)
    drift_e = max(math.dist(com(fr, me), c0e) for _, fr in frames)
    print(f"{name}: min wall dist {wall:.2f}, min pair sep {min(seps):.2f}, "
          f"COM drift predicted masses {drift_p:.4f}, equal masses {drift_e:.4f}")


if __name__ == "__main__":
    s3, s6 = math.sqrt(3), math.sqrt(3)
    layouts = {
        "tri side 8 (A,B,C)": [("A", [1.0, 1.0]), ("B", [9.0, 1.0]), ("C", [5.0, 1.0 + 8 * s3 / 2])],
        "tri side 6 centred": [("A", [2.0, 5 - 6 / (2 * s3)]), ("B", [8.0, 5 - 6 / (2 * s3)]), ("C", [5.0, 5 + 6 / s3])],
        "tri side 5 centred": [("A", [2.5, 5 - 5 / (2 * s3)]), ("B", [7.5, 5 - 5 / (2 * s3)]), ("C", [5.0, 5 + 5 / s3])],
    }
    for name, parts in layouts.items():
        report(name, parts)
