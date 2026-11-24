#!/usr/bin/env python3
"""Pre-registration for the A-A exponent test (round 3, lab-c). Written before any round-3 result exists.

M1: single power law, per-particle accel K/r^P, joint A-A fit from 2026-11-24/r2/lab-c/002-004:
    P = 3.10, K = 47.00  (joint chi2/n 1.005 on those three runs).
M2: the P-0027 (lab-a) K(r) table at exponent 2.5 (piecewise-linear K, nodes 3..9), accel K(r)/r^2.5.

For each candidate design (pair at rest, T = 6, window until measured separation < 3), this prints
  D = RMS difference between M1 and M2 predicted positions / L  (what one run can discriminate),
  and the expected judge-style RMSE/L of the right model under tracker noise sigma = 0.05 (floor ~ 0.005).
Usage: python3 -I prereg_AA_2026-11-24_r3.py
"""
import math

L = 10.0
SIG = 0.05
NODES = {3: 17.683, 4: 17.701, 5: 17.834, 6: 16.617, 7: 15.121, 8: 13.432, 9: 11.624}


def K_table(r):
    rs = sorted(NODES)
    if r <= rs[0]:
        return NODES[rs[0]]
    if r >= rs[-1]:
        return NODES[rs[-1]]
    for a, b in zip(rs, rs[1:]):
        if a <= r <= b:
            w = (r - a) / (b - a)
            return NODES[a] * (1 - w) + NODES[b] * w


def integrate(r0, accel_fn, T=6.0, h=0.0005, dt_out=0.01):
    """Relative r(t) for two equal particles at rest, symmetric about centre 5."""
    r, v, t = r0, 0.0, 0.0
    out = {0.0: r0}
    nout = int(round(T / dt_out))
    for k in range(1, nout + 1):
        tn = k * dt_out
        while t < tn - 1e-12:
            s = min(h, tn - t)
            f = lambda rr, vv: (vv, -2.0 * accel_fn(rr))
            k1 = f(r, v)
            k2 = f(r + s / 2 * k1[0], v + s / 2 * k1[1])
            k3 = f(r + s / 2 * k2[0], v + s / 2 * k2[1])
            k4 = f(r + s * k3[0], v + s * k3[1])
            r += s / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            v += s / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            t += s
            if r < 0.5:
                return out
        out[round(tn, 9)] = r
    return out


def m1(r):
    return 47.00 / max(r, 1e-3) ** 3.10


def m2(r):
    return K_table(r) / max(r, 1e-3) ** 2.5


def window_end(traj):
    """Last time with separation >= 3 (the fit window rule)."""
    ts = sorted(traj)
    last = 0.0
    for t in ts:
        if traj[t] >= 3.0:
            last = t
        else:
            break
    return last


DESIGNS = [
    ("H r0=5", 5.0, 6.0),
    ("H r0=7", 7.0, 6.0),
    ("H r0=9", 9.0, 6.0),
    ("H r0=6 (repeat, T=6)", 6.0, 6.0),
]
print(f"{'design':24s} {'win_end':>8s} {'D(M1,M2)/L':>11s} {'npts':>6s}")
for name, r0, T in DESIGNS:
    t1 = integrate(r0, m1, T)
    t2 = integrate(r0, m2, T)
    tend = min(window_end(t1), window_end(t2))
    ts = [t for t in sorted(t1) if 0 < t <= tend and t in t2]
    # each particle moves by half the separation change in opposite directions, so the per-coordinate
    # position difference between M1 and M2 is (r1 - r2) / 2
    rms_pos = math.sqrt(sum(((t1[t] - t2[t]) / 2) ** 2 for t in ts) / len(ts))
    print(f"{name:24s} {tend:8.2f} {rms_pos / L:11.5f} {len(ts):6d}")


# Expected chi2/n (sigma 0.05, window r >= 3, 4 coordinates per sample) if M1 is true, for the
# horizontal designs. The x-coordinates of the two particles differ between M1 and M2 by (r1-r2)/2 each; the
# y-coordinates do not differ. So E[chi2/n of M2 | M1 true] = 1 + 0.5 * mean(((r1-r2)/2)^2) / sigma^2.
print("\nExpected chi2/n for horizontal designs (window r >= 3):")
for name, r0, T in DESIGNS[:3]:
    t1 = integrate(r0, m1, T)
    t2 = integrate(r0, m2, T)
    tend = min(window_end(t1), window_end(t2))
    ts = [t for t in sorted(t1) if 0 < t <= tend and t in t2]
    mean_dx2 = sum(((t1[t] - t2[t]) / 2) ** 2 for t in ts) / len(ts)
    print(f"  {name:24s} E[chi2/n | M1 true] for M2 = {1 + 0.5 * mean_dx2 / SIG**2:.3f}  "
          f"(M1 itself: 1.000 in expectation)")
