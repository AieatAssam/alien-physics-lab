"""Pre-registered predictions for the close-range A-A falls (requests 2026-11-27/r1/lab-a/015-017).

Two laws for a pair of A particles at rest, each particle accelerating toward the other:
  P26   : a(r) = (G/2) / r^P, G = 23.63, P = 2.099 (lab-c's P-0026 law, the P-0035 predictor)
  TAB   : a(r) = K / r^2.5, K = 17.683 (my clamped P-0027 table; constant K below r = 3)
Integrated with RK4 (h = 1e-4), no walls reached. Prints the per-particle displacement at t = 0.3,
averaged over the last window [0.25, 0.30] (the same window the scorer uses), and the difference.
Run: python3 -I predict_close_2026-11-27.py
"""
import math


def accel_mag(law, r):
    if law == "P26":
        return (23.63 / 2.0) / r ** 2.099
    return 17.683 / r ** 2.5


def run(law, r0, T=0.3, h=1e-4):
    # particle 0 at x=0, particle 1 at x=r0 on the x-axis; by symmetry the motion stays on the axis
    x0, v0 = 0.0, 0.0
    x1, v1 = r0, 0.0

    def f(xa, xb):
        r = xb - xa
        a = accel_mag(law, r)
        return a, -a  # particle 0 pulled toward +x, particle 1 toward -x

    out = []
    t = 0.0
    n = int(round(T / h))
    for i in range(n):
        a0, a1 = f(x0, x1)
        # RK4 on state (x0, v0, x1, v1)
        def deriv(s):
            xa, va, xb, vb = s
            aa, ab = f(xa, xb)
            return (va, aa, vb, ab)
        s = (x0, v0, x1, v1)
        k1 = deriv(s)
        k2 = deriv(tuple(s[j] + h / 2 * k1[j] for j in range(4)))
        k3 = deriv(tuple(s[j] + h / 2 * k2[j] for j in range(4)))
        k4 = deriv(tuple(s[j] + h * k3[j] for j in range(4)))
        s2 = tuple(s[j] + h / 6 * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) for j in range(4))
        x0, v0, x1, v1 = s2
        t += h
        out.append((t, x0, x1))
    late = [(x0_ - 0.0, x1_ - r0) for (tt, x0_, x1_) in out if 0.25 - 1e-9 <= tt <= T + 1e-9]
    d0 = sum(abs(a) for a, _ in late) / len(late)
    d1 = sum(abs(b) for _, b in late) / len(late)
    return d0, d1


if __name__ == "__main__":
    for r0 in (1.5, 1.25):
        p0, _ = run("P26", r0)
        t0, _ = run("TAB", r0)
        print("r0=%.2f  P26 d=%.4f  TAB d=%.4f  diff=%.4f  rel=%.1f%%"
              % (r0, p0, t0, t0 - p0, 100 * (t0 - p0) / p0))
