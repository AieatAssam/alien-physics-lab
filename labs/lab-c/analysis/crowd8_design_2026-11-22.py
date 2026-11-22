"""Design check for a crowd-of-eight claim (lab-c, round 3, 2026-11-22).

Pairwise-sum predictor with the P-0008 coefficients (r^-2.5, no three-body term), applied to
8 particles on an octagon of radius 3.5 centred at (5, 5). Pure math; no numpy.
Reports, for each candidate arrangement and duration: minimum pairwise separation over the run
(contact check, judge does not model contact), and the motion sensitivity to a +-15 % scale of the
couplings (the P-0021 paper reports coupling drift with separation, so this is the honest spread).

Usage: python3 -I crowd8_design_2026-11-22.py
"""
import math

L = 10.0
P = 2.5
H = 0.002
COUP = {
    ("A", "A"): 18.0, ("A", "B"): 8.99, ("B", "A"): 12.34, ("A", "C"): -8.77, ("C", "A"): -21.25,
    ("B", "B"): 6.12, ("C", "C"): 12.36, ("B", "C"): -6.10, ("C", "B"): -10.59,
}


def accel(pos, species, scale):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            a = scale * COUP[(species[i], species[j])] / r ** P
            acc[i][0] += a * dx / r
            acc[i][1] += a * dy / r
    return acc


def step(pos, vel, species, h, scale):
    n = len(pos)

    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]

    k1p, k1v = vel, accel(pos, species, scale)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, accel(p2, species, scale)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, accel(p3, species, scale)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, accel(p4, species, scale)
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k])
             for k in range(2)] for i in range(n)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k])
             for k in range(2)] for i in range(n)]
    for i in range(n):
        for k in range(2):
            if newp[i][k] < 0.0:
                newp[i][k] = -newp[i][k]
                newv[i][k] = -newv[i][k]
            elif newp[i][k] > L:
                newp[i][k] = 2 * L - newp[i][k]
                newv[i][k] = -newv[i][k]
    return newp, newv


def run(pos0, species, T, dt, scale=1.0):
    """Return list of (t, positions) at multiples of dt, and min pairwise separation over the run."""
    pos = [list(p) for p in pos0]
    vel = [[0.0, 0.0] for _ in pos]
    n_samp = int(round(T / dt))
    out = [(0.0, [list(p) for p in pos])]
    t = 0.0
    minsep = min(math.dist(pos[i], pos[j]) for i in range(len(pos)) for j in range(i + 1, len(pos)))
    for i in range(1, n_samp + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = step(pos, vel, species, h, scale)
            t += h
            ms = min(math.dist(pos[a], pos[b]) for a in range(len(pos)) for b in range(a + 1, len(pos)))
            minsep = min(minsep, ms)
        t = target
        out.append((t, [list(p) for p in pos]))
    return out, minsep


def octagon(R=3.5, c=(5.0, 5.0), phase_deg=0.0):
    pts = []
    for k in range(8):
        a = math.radians(phase_deg + 45.0 * k)
        pts.append([c[0] + R * math.cos(a), c[1] + R * math.sin(a)])
    return pts


if __name__ == "__main__":
    arrangements = {
        "S1": ["A", "B", "C", "A", "B", "C", "A", "B"],
        "S2": ["C", "C", "A", "A", "B", "B", "A", "C"],
        "S3": ["B", "A", "A", "C", "B", "C", "B", "A"],
    }
    for name, sp in arrangements.items():
        for phase in (0.0, 22.5):
            pos0 = octagon(phase_deg=phase)
            seps = sorted({round(math.dist(pos0[i], pos0[j]), 3) for i in range(8) for j in range(i + 1, 8)})
            for T in (2.0, 5.0):
                _, ms = run(pos0, sp, T, 0.01)
                _, ms_hi = run(pos0, sp, T, 0.01, scale=1.15)
                _, ms_lo = run(pos0, sp, T, 0.01, scale=0.85)
                print(f"{name} phase={phase:5.1f} T={T}: min sep nominal={ms:.3f} (x1.15 {ms_hi:.3f}, x0.85 {ms_lo:.3f})  "
                      f"initial sep range {seps[0]}..{seps[-1]}")
