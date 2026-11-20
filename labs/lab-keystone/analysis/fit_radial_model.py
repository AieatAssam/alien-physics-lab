"""Fit G(r) = a + b*r (shared, initial separation r) and s for pairs containing C, to the per-particle
far-field coefficient ratios G_obs from radial_table.py (fits in radial_table output, T >= 3 runs).
Reference K(5) = P-0005 run means. Pure python grid + refinement."""
import math
# (pair key, r, particle-has-C flag, observed ratio, weight T)
DATA = [
 ('AA', 8, 0.767, 4), ('AA', 8, 0.782, 4), ('AA', 9, 0.682, 4), ('AA', 9, 0.6755, 4),
 ('AB', 8, 0.7639, 4), ('AB', 8, 0.7670, 4), ('AB', 9, 0.6720, 4), ('AB', 9, 0.6906, 4),
 ('AB', 6, 0.9553, 4), ('AB', 6, 0.9647, 4),
 ('BB', 8, 0.7700, 4), ('BB', 8, 0.7820, 4), ('BB', 6, 0.9591, 4), ('BB', 6, 0.9689, 4),
 ('CC', 8, 0.7341, 4), ('CC', 8, 0.7342, 4), ('CC', 8, 0.7520, 4), ('CC', 8, 0.7415, 4),
 ('CC', 9, 0.6602, 4), ('CC', 9, 0.6449, 4),
 ('BC', 6, 0.9164, 4), ('BC', 6, 0.8895, 4),
 ('AC', 7, 0.8168, 6), ('AC', 7, 0.8103, 6),
 ('AA', 8, 0.7730, 6), ('AA', 8, 0.7730, 6),

]
def pred(a, b, s, key, r):
    g = a + b * r
    return g * (s if 'C' in key else 1.0)
def sse(p):
    a, b, s = p
    return sum((pred(a, b, s, k, r) - y) ** 2 * w for k, r, y, w in DATA)
best = None
for a in [1.4 + 0.005 * i for i in range(60)]:
    for b in [-0.14 + 0.001 * j for j in range(80)]:
        for s in [0.90 + 0.0025 * m for m in range(60)]:
            e = sse((a, b, s))
            if best is None or e < best[0]:
                best = (e, a, b, s)
e, a, b, s = best
print('grid best a=%.4f b=%.5f s=%.4f sse=%.6f' % (a, b, s, e))
# residuals
for k, r, y, w in DATA:
    print(k, r, 'obs %.4f pred %.4f dev %+.2f%%' % (y, pred(a, b, s, k, r), 100 * (pred(a, b, s, k, r) / y - 1)))
print('G(6)=%.4f G(7)=%.4f G(8)=%.4f G(9)=%.4f' % tuple(a + b * r for r in (6, 7, 8, 9)))
