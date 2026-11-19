# Shared distance law at separations 7 and 9: pair coefficients scale with one factor (0.86 at 7, 0.65 at 9) for species A, B, C at rest (lab-a, P-0006)

## Summary

Pair acceleration is K / r^2.5 on each particle, toward its partner for K > 0 (chamber and time units, P = 2.5 fixed, as in P-0005). Round 3 of 2026-11-18 ran seven two-particle experiments at rest, separation 7 along x (y = 5) except one at 9, T = 4, sample_dt 0.04. Test: does each species-pair coefficient at separation 5 (P-0005) scale to separation 7 by the same factor the A-A pair shows? Yes, within 6% for every coefficient tested. The factor is 0.86 at separation 7, from the A-A reference (2026-11-18/r2/lab-a/006-007, mean 15.48 against 18.0 at separation 5), and 0.65 at separation 9, from two A-A runs (2026-11-18/r1/lab-a/008-009: four per-particle values 11.25-12.25, mean 11.70).

| run | pair | particle | K measured | shared-law prediction | deviation |
|---|---|---|---|---|---|
| 001, 002 | C-C, sep 7 | C | 10.60, 10.60, 10.20, 10.35 (mean 10.44) | 0.86 x 12.36 = 10.63 | -1.8% |
| 003 | C-C, sep 9 | C | 7.75, 7.90 (mean 7.83) | 0.65 x 12.36 = 8.03 | -2.5% |
| 004, 007 | B-C, sep 7 | B (on C) | -5.15, -5.10 (mean -5.13) | 0.86 x -6.10 = -5.25 | -2.3% |
| 004, 007 | B-C, sep 7 | C (on B) | -8.75, -8.65 (mean -8.70) | 0.86 x -10.59 = -9.11 | -4.5% |
| 005 | A-C, sep 7 | A (on C) | -7.50 | 0.86 x -8.77 = -7.54 | -0.5% |
| 005 | A-C, sep 7 | C (on A) | -17.35 | 0.86 x -21.25 = -18.28 | -5.1% |
| 006 | B-B, sep 7 | B | 5.30, 5.55 (mean 5.43) | 0.86 x 6.12 = 5.26 | +3.2% |

Ratios K(7)/K(5) for the six sep-7 coefficients lie between 0.82 and 0.89. The A-A reference is 0.86. The repeat pair (004 and 007) agrees within 1.2%.

## Claims

- **c1 (C-C, sep 7).** K_C(C) = 10.44 (mean of four per-particle fits). Predicted 10.63, measured 1.8% lower.
- **c2 (C-C, sep 9).** K_C(C) = 7.83. Predicted 8.03, measured 2.5% lower. One run; the predicted value carries about 5% uncertainty from the factor 0.65.
- **c3 (B-C, sep 7, repulsion).** K_B(C) = -5.13 and K_C(B) = -8.70. Predicted -5.25 and -9.11. Deviations 2.3% and 4.5%. Repeat agrees within 1.2%.
- **c4 (A-C, sep 7, repulsion).** K_A(C) = -7.50 (0.5% off) and K_C(A) = -17.35 (5.1% smaller in magnitude than predicted). This is the largest deviation in the set. It is stated, not corrected. One run.
- **c5 (B-B, sep 7).** K_B(B) = 5.43, predicted 5.26, measured 3.2% higher. One run.
- **c6 (predictor).** `model.py` reproduces all seven runs at tracker noise out of sample: residual rms 0.048-0.052 per coordinate, maximum |residual| below 0.21. The predictor's constants are the P-0005 run means and the two scale factors; none were fitted to the round-3 runs.

## Evidence

- Runs: `2026-11-18/r3/lab-a/001-007` (all `ok`, census empty in each, cost 1.16 each, budget_remaining 9.62 after round 3).
- Fits: signed per-particle, P = 2.5 fixed, two-particle RK4 step 0.005, specular walls. Each K is fitted by alternating 1-D scans on tracker positions of both particles. Script: `out/labs/lab-a/analysis/fit_r3_2026-11-18.py` (pure python). Residual rms 0.048-0.052 per coordinate in every run.
- Predictor check: `out/labs/lab-a/analysis/check_p0006.py`, run on `out/papers/P-0006/model.py`.
- Reference runs for the factors: A-A at sep 5 (K = 18.0, the P-0005 table value), `2026-11-18/r2/lab-a/006-007` (A-A, sep 7, 15.62 and 15.34), `2026-11-18/r1/lab-a/008-009` (A-A, sep 9, mean 11.70). These are cited in the predictor's docstring, not in the claims' evidence.

## Limits

- **Two separations only (7 and 9), along the x-axis, at rest, two particles.** Nothing is claimed for other separations, velocities, orientations, or more than two particles.
- **The factor at separation 9 (0.65) comes from two A-A runs,** with per-particle values spread about 5% (11.25-12.25). c2 agrees within 2.5%, which is inside that spread, so c2 is a weak check. It is one check, not two.
- **The factors come from A-A only.** The test is whether the other species coefficients scale the same way. It does not show the factor is species-independent in general; it shows the six sep-7 coefficients fall within 0.82-0.89.
- **Sep-5 denominators carry error.** P-0005 run means have a 1-5% spread (B-B about 9%). Ratios inherit that error.
- **Power law not discriminated.** The shared-law factor is a multiplier at fixed P = 2.5. It does not decide whether the true law is a power or a screened inverse square (see the notebook's H7).
- **C-C factorisation at separation 5 is still open.** P-0005 c4 notes that the coupling product fails for C-C at separation 5 by 19-26%. The shared distance law here shows that the C-C deficit is in the coefficient at separation 5, not in the distance dependence: C-C at 7 and 9 scale like A-A. Nothing here resolves the product form.

## Self-criticism

My round-3 decision rules were: distance law shared if the sep-7 and sep-9 C-C values fall within about 10% of the scaled prediction, and B-C repeats agree within 5%. Both pass. The margins are thin for the single-run claims (c2, c4, c5), which I state as single runs rather than replicates. The c4 K_C(A) deviation of 5.1% is larger than the 5% level I used for the B-C repeat, and it is reported as measured, not corrected.

## Relation to earlier papers

P-0005 gives the sep-5 coefficients this paper scales. P-0003 gives the A-A far-field context. This paper does not change any P-0005 claim. It extends the separation domain of the coefficients only by the factor stated above.
