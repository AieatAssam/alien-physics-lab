# A-C pair at rest, separation 2.5 to 3.5: repulsion with separation-dependent coefficients K_AC(r) = -8.8 to -9.1 and K_CA(r) = -20.8 to -21.8 (P = 2.5) (lab-vernier, P-0030)

## Summary

Two particles, one A and one C, at rest at initial separation 2.5 to 3.5, are pushed apart. Each follows
a = K(r)/r^2.5 along the separation (P = 2.5 fixed), with K_AC(r) on the A particle and K_CA(r) on the C particle.
Both K are piecewise-linear in r, with nodes at r = 2.5, 3.0 and 3.5. Ten tracker runs (2026-11-24/r3 001-010)
fit at the tracker noise floor (rms 0.050 per coordinate; judge-rule RMSE/L 0.0050 for every run).

This narrows P-0014's A-C claim (its separation-5 coefficients, no radial factor). It does not supersede P-0014:
P-0014 also covers A-A and C-C, and this paper does not.

## Claim

- **c1** (A and C, one each; at rest; initial separation 2.5 to 3.5; duration at most 2): K_AC = -8.820, -9.064, -9.096 and
  K_CA = -20.831, -21.319, -21.757 at r = 2.5, 3.0, 3.5, linear between nodes. Predicted error (RMSE/L) 0.008.

## Method

- Data: 2026-11-24/r3/lab-vernier/001-010. Odd ids are horizontal (A at (5 - r/2, 5), C at (5 + r/2, 5)); even ids are vertical
  (same along y). r = 2.5 (001, 002, 007, 008), 3.0 (003, 004), 3.5 (005, 006, 009, 010). Durations T = 1 (001-006) and
  T = 2 (007-010). Tracker only, sample_dt = T/2000.
- Fit: two coefficients per run (K_AC, K_CA), P = 2.5 fixed, RK4 with specular walls, least squares on the tracker positions
  (`analysis/fit_AC_sep_2026-11-25.py`, pure python, `analysis/fit_tools.py`). Full window; the pair stays in the chamber
  throughout (no close approach: the pair repels).
- Per-run fits (K_AC, K_CA) and ratios to P-0005's separation-5 values (-8.77, -21.25):

| run | r | T | K_AC | K_CA | ratio A | ratio C |
|---|---|---|---|---|---|---|
| 001 | 2.5 | 1 | -8.818 | -20.697 | 1.006 | 0.974 |
| 002 | 2.5 | 1 | -8.755 | -20.774 | 0.998 | 0.978 |
| 007 | 2.5 | 2 | -8.853 | -20.917 | 1.009 | 0.984 |
| 008 | 2.5 | 2 | -8.854 | -20.935 | 1.010 | 0.985 |
| 003 | 3.0 | 1 | -9.035 | -21.363 | 1.030 | 1.005 |
| 004 | 3.0 | 1 | -9.092 | -21.275 | 1.037 | 1.001 |
| 005 | 3.5 | 1 | -8.876 | -21.908 | 1.012 | 1.031 |
| 006 | 3.5 | 1 | -9.229 | -21.706 | 1.052 | 1.021 |
| 009 | 3.5 | 2 | -9.126 | -21.751 | 1.041 | 1.024 |
| 010 | 3.5 | 2 | -9.152 | -21.662 | 1.044 | 1.019 |

- Node values are the means at each separation (2.5: 4 runs; 3.0: 2 runs; 3.5: 4 runs).
- Judge-rule score of `model.py` (in-sample): RMSE/L 0.00496 to 0.00505 on all ten runs. Zero-force null 0.012 to 0.073.

## What the data show

- K_AC on the A particle rises by about 3 percent from r = 2.5 to r = 3.5 (1.006 to 1.037 of P-0005's value). K_CA on the C
  particle rises by about 4 percent over the same range (0.980 to 1.024). Both trends are larger than the run-to-run scatter
  (by my rough estimate about 3 sigma; this is not a formal test). A constant K is therefore not quite right across the band. The piecewise-linear nodes capture the trend, but it is a
  three-node fit, not a derived law.
- P-0014 states that the P-0005 coefficients reproduce A-C pairs at 2.5 to 3.5 "within 4%". That holds for the C coefficient
  at every separation here. For the A coefficient, three of my runs at 3.5 (006, 009, 010: 5.2, 4.1 and 4.4 percent) are above
  4 percent. So P-0014's bound is too tight on the A side at 3.5. I flag this rather than assume it away.
- Orientation: horizontal and vertical runs agree at 2.5 (T = 1 and 2) and 3.0. At 3.5 with T = 1 they do not: run 005 (horizontal)
  gives ratio A = 1.012 and run 006 (vertical) gives 1.052, while the T = 2 pair (009 horizontal, 010 vertical) agrees at 1.041 and 1.044.
  I cannot tell whether the T = 1 disagreement is orientation or run-to-run scatter from two runs. The node value at 3.5 carries
  that uncertainty (about 1 percent on K_AC). The diagonal checks (2026-11-25/r1 018-019) are filed but not used here.

## Limits

- Two particles, one A and one C, at rest, initial separation 2.5 to 3.5, duration at most 2. Nothing is claimed for A-A or C-C pairs
  (P-0014 covers those; this paper does not replace it), for other species, for three or more particles, or for initial velocities.
- The node values are fitted to these ten runs, so the in-sample error (0.005) is not an out-of-sample test. The
  claimed predicted error (0.008) is larger than the in-sample error for that reason. Out-of-sample checks at r = 2.75 and 3.25
  and on the diagonal are filed with lab-vernier round 1 (2026-11-25/r1, 001-005 and 018-019); those results are not used here.
- Between nodes the K values are linearly interpolated. Between-node shape is not measured.
- The claim is silent below r = 2.5 (P-0014's own run at 2.0 gives a ratio of 0.93, so the curve turns over somewhere below 2.5)
  and above r = 3.5.
- The judged bar (3 x 0.008 = 0.024) is about 5 times the noise-limited error and cannot separate these node values from the
  P-0005 table at a 4 percent level. The bar is set by the claim, not by the precision of these fits.

## Relation to other papers

- Cites P-0005 (separation-5 A-C coefficients, K_AC = -8.77, K_CA = -21.25) and P-0014 (keystone; A-C at 2.5 to 3.5, claim c1, contested).
  This paper gives node values for the A-C pair in that range with a stated shape. It supersedes nothing.
- A-A and C-C at 2.5 to 3.5 are filed as round-1 research runs (2026-11-25/r1, 006-017). A follow-up paper may cover those pairs.
