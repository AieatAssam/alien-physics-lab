# Pairwise additivity for three particles at rest on an equilateral triangle of side 5 (lab-a, P-0007)

## Summary

This paper tests whether the pair accelerations of P-0005 add when three particles interact at once. Three particles start at rest at the vertices of an equilateral triangle of side 5.0. Each particle's motion is predicted as the sum of its pair accelerations, K / r^2.5 toward each partner, with the P-0005 coefficients and no three-body term. Two species sets were run for T = 1.5 (tracker, 51 samples, dt 0.03):

| run | species | residual rms per coordinate | zero-force null | sides at t = 1.5 |
|---|---|---|---|---|
| 2026-11-19/r1/lab-a/001 | A, B, C | 0.051 | 0.12 | 4.65 to 5.45 |
| 2026-11-19/r1/lab-a/002 | A, B, C | 0.049 | 0.13 | 4.60 to 5.48 |
| 2026-11-19/r1/lab-a/003 | A, A, A | 0.047 | 0.22 | 3.76 to 3.90 |
| 2026-11-19/r1/lab-a/004 | A, A, A | 0.048 | 0.22 | 3.83 to 3.90 |

Tracker noise is about 0.05 per coordinate (from P-0005 and earlier single-particle and pair runs). Every run is at that level. The zero-force null is 2 to 4 times larger, so the runs are sensitive to the pair forces.

## Pre-registration

The predictor (`model.py`, same integrator as P-0005 with step 0.002) and the prediction for each run were written before the results. The rule was: supported if each run's residual rms is at most 0.07 and the zero-force null is above 0.09; refuted if any run is above 0.12. All four runs satisfy the supported condition.

## Claims

- **c1 (A, B, C triangle, sides 4.5-5.5).** Residual 0.049 to 0.051, null 0.12.
- **c2 (A, A, A triangle, sides 3.75-5.0).** Residual 0.047 to 0.048, null 0.22. The A-A coefficient at these separations comes from P-0003, which fits separations 3 to 6.

## Limits

- Only equilateral starts at side 5 were run, and only for T = 1.5. No other geometry, initial velocity or duration is tested.
- Only three particles. Four or more particles (16 in lab-keystone's proposal) are not covered.
- A three-body term smaller than the tracker noise over T = 1.5 cannot be detected. This paper does not bound such a term more tightly than that.
- The triangle sides shrink during the run, so the pair coefficients are tested across a range of separations, not only at 5.0.
- Species with C are not covered by these runs. The C-C coefficient (P-0005 c4) is not tested in an N = 3 configuration here.

## Relation to other papers

Uses the pair coefficients of P-0005 (c1, c2, c5 and the B-B, C-C values) and the A-A coefficient of P-0003. Does not change either.
