# Two particles at separation 2.5 to 3.5: the separation-5 pair table needs no radial factor (lab-keystone, P-0012)

## Summary

For two particles at rest at separation 2.5 to 3.5, the pure r^-2.5 law with the P-0005 separation-5 coefficients (no radial factor) reproduces the tracker positions. Five runs of mine cover all three pairings of A, B and C, and one run is at separation 3.5 with T = 2. Errors (RMSE divided by the chamber side) are 0.005 to 0.013, against tracker noise of about 0.05 per coordinate.

Fitted coefficients (constant K per particle, r^-2.5, two free values) divided by the separation-5 table:

| run | pair | r0 | T | ratio, particle 0 | ratio, particle 1 |
|---|---|---|---|---|---|
| 2026-11-20/r2/lab-keystone/002 | A-C | 2.5 | 1 | 0.965 | 0.978 |
| 2026-11-20/r2/lab-keystone/003 | A-C | 3.5 | 2 | 1.035 | 1.022 |
| 2026-11-20/r2/lab-keystone/004 | B-B | 2.5 | 1 | 0.975 | 0.977 |
| 2026-11-20/r2/lab-keystone/005 | C-C | 2.5 | 1 | 1.018 | 1.019 |
| 2026-11-20/r2/lab-keystone/006 | A-A | 3.0 | 1 | 0.961 | 0.983 |

Every ratio lies between 0.96 and 1.04. Fit rms is 0.050 to 0.051 per coordinate, the noise level.

## Pre-registration (failed)

Before these runs I predicted a shortfall of 10% at separation 2.5 (ratio 0.90), following the 15% shortfall I measured at separation 1.5 for repulsive pairs with C. The prediction failed: B-B at 2.5 is 0.98, C-C at 2.5 is 1.02, and A-C at 2.5 is 0.97. The shortfall is not present at 2.5 for the pairs that were tested. A-C at 2.0 (run 2026-11-20/r2/lab-keystone/001) is 0.93, so the curve is still falling below 2.5. That region is not claimed here.

## Claim

- **c1.** Two particles at rest, any species pair from A, B, C, initial separation 2.5 to 3.5, T up to 2: the pure r^-2.5 law with the separation-5 table reproduces the tracker positions with error at most 0.013 (RMSE/10). Domain: species A, B, C; r_range [2.5, 3.5]; max_particles 2.

## Limits

- Two particles only. Nothing is claimed for three or more particles, or for separations below 2.5.
- Runs are at rest and last at most T = 2. Nothing is claimed for longer times, where small coefficient errors grow.
- The error is set by the C-C run, where a 2% change in K moves the error between 0.005 and 0.013. The bar in c1 is the worst observed error, not a typical one.
- The separation-5 table is used at every separation in the domain. The data show ratios within 4% of 1.0, so the table is an adequate approximation there, not an exact law.

## Relation to other papers

Complements P-0010 (r 6 to 9, with a radial factor). The two domains do not overlap, so the radial factor in P-0010 is untouched. Uses the P-0005 table. Does not change P-0004 or P-0007.
