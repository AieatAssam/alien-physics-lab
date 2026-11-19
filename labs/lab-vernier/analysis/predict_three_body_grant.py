"""Vernier: pre-registered pairwise-superposition prediction for the round-1 grant setup.

Initial accelerations of A, B, C at rest on a triangle of side 5 (positions as in
make_round1_requests.py), predicted by summing P-0005 pair couplings, K_i(j)/r^2.5,
along each pair direction. This is the instantaneous (t=0) prediction only; the
grant's T=2 run needs a full RK4 integration, which is not written yet.
Run as: python3 -I predict_three_body_grant.py
"""
import math

pos = {"A": (2.5, 2.5), "B": (7.5, 2.5), "C": (5.0, 2.5 + 5.0 * math.sqrt(3) / 2)}
# P-0005 run-mean couplings: K[(i, j)] is the coefficient on particle i from partner j.
K = {("A", "B"): 8.99, ("A", "C"): -8.77, ("B", "A"): 12.34,
     ("B", "C"): -6.10, ("C", "A"): -21.25, ("C", "B"): -10.59}

if __name__ == "__main__":
    for i in pos:
        ax = ay = 0.0
        for j in pos:
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            k = K[(i, j)] / r ** 2.5
            ax += k * dx / r
            ay += k * dy / r
        print(f"{i} initial accel = ({ax:+.4f}, {ay:+.4f})")
