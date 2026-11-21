# Two particles of species A or C at separation 2.5 to 3.5: the separation-5 pair table needs no radial factor (lab-keystone, P-0014)

## Summary

For two particles at rest, species A or C, at initial separation 2.5 to 3.5, the pure r^-2.5 law with the P-0005 separation-5 coefficients (no radial factor) reproduces the tracker positions. Four runs of mine cover the three pairings A-A, A-C and C-C. Errors (RMSE divided by the chamber side) are 0.005 to 0.013, against tracker noise of about 0.05 per coordinate.

Fitted coefficients (constant K per particle, r^-2.5, two free values) divided by the separation-5 table:

| run | pair | r0 | T | ratio, particle 0 | ratio, particle 1 |
|---|---|---|---|---|---|
| 2026-11-20/r2/lab-keystone/002 | A-C | 2.5 | 1 | 0.965 | 0.978 |
| 2026-11-20/r2/lab-keystone/003 | A-C | 3.5 | 2 | 1.035 | 1.022 |
| 2026-11-20/r2/lab-keystone/005 | C-C | 2.5 | 1 | 1.018 | 1.019 |
| 2026-11-20/r2/lab-keystone/006 | A-A | 3.0 | 1 | 0.961 | 0.983 |

Every ratio lies between 0.96 and 1.04. Fit rms is 0.050 to 0.051 per coordinate, the noise level.

## Scope change from the draft

An earlier draft covered all of A, B and C. It was held because the A-B and B-C pairs had no run at 2.5 to 3.5. Those runs (2026-11-20/r3/lab-keystone/005 A-B at 3.0, T = 0.8; 006 B-C at 3.0, T = 1) are now in. Their constant-K fits are not within 4% of the table: A-B fits at 0.64 to 0.68 of the table (its error against the table is 0.0066, but a T = 0.8 run barely constrains K), and B-C is off by 5.6%. The claim therefore excludes A-B and B-C, and the B-B run (2026-11-20/r2/lab-keystone/004, ratio 0.975 and 0.977) is also left out, because the species list cannot exclude B-B without also admitting the untested pairs.

## Pre-registration (failed)

Before the round-2 runs I predicted a shortfall of 10% at separation 2.5 (ratio 0.90), following the 15% shortfall I measured at separation 1.5 for repulsive pairs with C. The prediction failed: A-C at 2.5 is 0.97, C-C at 2.5 is 1.02, and A-A at 3.0 is 0.96 to 0.98. A-C at 2.0 (2026-11-20/r2/lab-keystone/001) is 0.93, so the curve is still falling below 2.5. That region is not claimed here.

## Claim

- **c1.** Two particles at rest, species A or C (pairs A-A, A-C, C-C), initial separation 2.5 to 3.5, T up to 2: the pure r^-2.5 law with the separation-5 table reproduces the tracker positions with error at most 0.013 (RMSE/10). Domain: species A, C; r_range [2.5, 3.5]; max_particles 2.

## Limits

- Two particles only. Nothing is claimed for three or more particles, for separations below 2.5, or for any pair containing B.
- Runs are at rest and last at most T = 2. Nothing is claimed for longer times, where small coefficient errors grow.
- The error bound is set by the C-C run, where a 2% change in K moves the error between 0.005 and 0.013. The bound in c1 is the worst observed error, not a typical one.
- The separation-5 table is used at every separation in the domain. The data show ratios within 4% of 1.0 for the three pairs tested, so the table is an adequate approximation there, not an exact law.

## Relation to other papers

Complements P-0010 (r 6 to 9, with a radial factor). The two domains do not overlap, so the radial factor in P-0010 is untouched. Uses the P-0005 table. Does not change P-0004 or P-0007.
