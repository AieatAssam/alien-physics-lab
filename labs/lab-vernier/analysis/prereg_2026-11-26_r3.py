"""Pre-registration for round 3, 2026-11-26 (lab-vernier). Pure math, no numpy.

Law (P-0026 / P-0035): acceleration on each A particle toward the other is (G/2)/r^P, G=23.63, P=2.099.
Integrated with RK4, step 1e-5, no clamp. Walls ignored here (all test pairs sit >= 2 from walls).

Outputs:
  (a) review-edge prediction: judged RMSE/L of the law vs the noise floor for horizontal and vertical
      2.75 pairs at T=0.6 (the P-0035 claim's upper edge, exact binary coordinates).
  (b) contact-probe design: time at which the law's separation falls through 0.8, 0.6, 0.5, 0.4, 0.3
      for an A-A pair at rest from r0=2.0; and the RMSE/L of alternative contact laws (softened,
      r_min cutoff, G 2% high) against the pure law, over windows ending at each threshold.
"""
import math

L = 10.0
G = 23.63
P = 2.099
H = 1e-5


def accel_rel(r):
    return (G / 2.0) / r ** P


def integrate(r0, T, dt_out, law=None, n_eps=None):
    """Relative coordinate x = (pos1 - pos0) integrated as 1D radial motion along the x axis.
    Each particle accelerates toward the other with a(r); relative accel is 2a(r) toward the other."""
    if law is None:
        law = accel_rel
    # horizontal pair: particle 0 at -r0/2, particle 1 at +r0/2, both at rest
    x0 = -r0 / 2.0
    x1 = r0 / 2.0
    v0 = v1 = 0.0
    out = []
    t = 0.0
    n_out = int(round(T / dt_out))
    k = 0
    while k <= n_out:
        target = round(k * dt_out, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            # RK4 on (x0, v0, x1, v1)
            s = (x0, x1, v0, v1)
            def d(s):
                xa, xb, va, vb = s
                r = xb - xa
                a = law(r)
                return (va, vb, a, -a)  # xa accelerates toward xb (+a), xb toward xa (-a)
            k1 = d(s)
            k2 = d(tuple(s[i] + h / 2 * k1[i] for i in range(4)))
            k3 = d(tuple(s[i] + h / 2 * k2[i] for i in range(4)))
            k4 = d(tuple(s[i] + h * k3[i] for i in range(4)))
            s = tuple(s[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4))
            x0, x1, v0, v1 = s
            t += h
            if x1 - x0 < 0.05:  # guard, stop before singularity
                return out
        out.append((target, x0, x1, x1 - x0))
        k += 1
    return out


if __name__ == "__main__":
    # (b) separation crossing times for the pure law from r0 = 2.0
    traj = integrate(2.0, 1.2, 0.0005)
    def cross(th):
        for tt, a, b, r in traj:
            if r <= th:
                return tt
        return None
    print("pure law, r0=2.0: time r first <= threshold")
    for th in (1.5, 1.0, 0.8, 0.6, 0.5, 0.4, 0.3):
        print(f"  r <= {th}: t = {cross(th)}")
    print("  positions (x) at t=0.6:", [round(v, 4) for v in [traj[1200][1], traj[1200][2]]], "r =", round(traj[1200][3], 4))
