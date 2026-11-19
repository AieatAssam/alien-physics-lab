"""Pre-registered additive prediction for the equilateral A-B-C triangle (side 5), request 2026-11-19/r1/lab-c/020.

Pair law: a_i from partner j = K_i(j) / r^2.5 along the unit vector i->j (K > 0 attracts).
K values are the P-0005 run means at r=5 (the only data used; no triangle data).
"""
import math

K = {("A", "B"): 8.99, ("B", "A"): 12.34,
     ("A", "C"): -8.77, ("C", "A"): -21.25,
     ("B", "C"): -6.10, ("C", "B"): -10.59}
R = 5.0 / math.sqrt(3.0)
pos = {"A": (5.0, 5.0 + R), "B": (2.5, 5.0 - R / 2), "C": (7.5, 5.0 - R / 2)}


def accel(i):
    ax = ay = 0.0
    for j in pos:
        if j == i:
            continue
        dx, dy = pos[j][0] - pos[i][0], pos[j][1] - pos[i][1]
        d = math.hypot(dx, dy)
        k = K[(i, j)] / d ** 2.5
        ax += k * dx / d
        ay += k * dy / d
    return ax, ay


if __name__ == "__main__":
    for i in "ABC":
        ax, ay = accel(i)
        print("%s  predicted a = (%+.3f, %+.3f)  |a| = %.3f" % (i, ax, ay, math.hypot(ax, ay)))
