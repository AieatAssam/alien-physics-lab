"""Pre-registered additivity prediction for 2026-11-18/r3/lab-b/006 (equilateral A,B,C, side 3, at rest).

Initial acceleration of particle i = sum over partners j of K_i(j) / r^2.5 * unit(i->j),
using the sep-3 per-particle coefficients from 2026-11-18/r2/lab-b/010-015 (pure Python).
Writes the predicted initial accelerations; compare with the fitted accelerations after the
result arrives (early_accel_fit.py / pair_fit_integrated.py style fit at t<=0.3).
"""
import math

# per-particle coefficients K_i(j) at separation 3 (r2/010-015, P=2.5, mean of the two particles)
K = {
    ("A", "A"): 17.67,   # r2/010: 17.75, 17.59
    ("B", "B"): 6.33,    # r2/011: 6.34, 6.33
    ("C", "C"): 13.20,   # r2/012: 13.19, 13.22
    ("A", "B"): 8.97,    # r2/013: K_A(B)
    ("B", "A"): 12.55,   # r2/013: K_B(A)
    ("A", "C"): -8.98,   # r2/014: K_A(C)
    ("C", "A"): -21.45,  # r2/014: K_C(A)
    ("B", "C"): -6.41,   # r2/015: K_B(C)
    ("C", "B"): -10.66,  # r2/015: K_C(B)
}
SPECIES = {"A": (4.0, 4.0), "B": (7.0, 4.0), "C": (5.5, 4.0 + 3 * math.sqrt(3) / 2)}


def main():
    r = 3.0
    scale = r ** -2.5
    for i in "ABC":
        ax = ay = 0.0
        for j in "ABC":
            if j == i:
                continue
            xi, yi = SPECIES[i]
            xj, yj = SPECIES[j]
            d = math.hypot(xj - xi, yj - yi)
            ux, uy = (xj - xi) / d, (yj - yi) / d
            k = K[(i, j)] * scale
            ax += k * ux
            ay += k * uy
        print(f"predicted initial accel of {i}: ({ax:+.4f}, {ay:+.4f}) |a|={math.hypot(ax, ay):.4f}")


if __name__ == "__main__":
    main()
