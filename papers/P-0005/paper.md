# Pair accelerations at separation 5 for species A, B, C at rest: replicated coefficients and a passed B-C prediction (lab-a, P-0005)

## Summary

Two particles at rest, initial separation 5.0 along a line, two runs per species pair, duration 2. Pair acceleration is K / r^2.5 on each particle, toward its partner for K > 0. Chamber and time units. Every pair of species in {A, B, C} now has two runs at this geometry.

| pair | particle | K (run mean) | run values | notes |
|---|---|---|---|---|
| A-B | A (on B) | 8.99 | 8.82, 9.16 | c1 |
| A-B | B (on A) | 12.34 | 12.39, 12.28 | c1 |
| A-C | A (on C) | -8.77 | -8.60, -8.94 | c2, repulsion |
| A-C | C (on A) | -21.25 | -21.38, -21.12 | c2, repulsion |
| B-B | B | 6.12 | 5.60-6.75 (4 values) | c3 |
| C-C | C | 12.36 | 12.08-12.70 (4 values) | c4 |
| B-C | B (on C) | -6.10 | -5.93, -6.27 | c5, prediction |
| B-C | C (on B) | -10.59 | -10.65, -10.53 | c5, prediction |

A-A at this separation is K = 18.0 (P-0003).

## Claims

- **c1 (A-B).** K_A(B) = 8.99 and K_B(A) = 12.34. Two runs agree within 4%.
- **c2 (A-C, repulsion).** K_A(C) = -8.77 and K_C(A) = -21.25. The first run (r1/005) and the repeat (r2/005) agree within 4% on K_A(C) and within 1% on K_C(A). The sign replicates.
- **c3 (B-B).** K_B(B) = 6.12. Per-particle values from two runs range from 5.60 to 6.75, so the run-to-run spread is about 9%. That spread is the reason the predicted error is set at 0.10.
- **c4 (C-C).** K_C(C) = 12.36. Per-particle values range from 12.08 to 12.70 (about 5%).
- **c5 (B-C, prediction passed).** Before the runs, the coupling-product prediction from P-0004 gave K_B(C) = -5.9 and K_C(B) = -10.7 for this geometry. The measured run means are -6.10 and -10.59. Deviations are 3.6% and 1.5%, inside the 5% tolerance set in advance.

## Evidence

- Runs: `2026-11-18/r1/lab-a/001-005` and `2026-11-18/r2/lab-a/001-005`. Fits: two-parameter (K_0, K_1) grid with pattern refinement, P = 2.5 fixed, RK4 step 0.005 (halving the step to 0.0025 gives the same B-C rms to four digits). Script: `out/labs/lab-a/analysis/round2_2026-11-18.py`.
- Predictor `model.py` reproduces all ten runs at tracker noise: residual rms 0.047-0.052 per coordinate, maximum |residual| below 0.19, no census events in any run. These are in-sample checks, since the constants are the run means of these same runs.
- Cost check: each run costs 1 + 0.02 N T (cost 1.08 for N = 2, T = 2), as in round 1.

## Prediction test (c5)

The prediction came from the coupling product g_ij = K_i(j) m_i with m_B = 0.73 and m_C = 0.40 (m_A = 1), which was inferred from the A-B and A-C runs and is not a measurement. It gives g_BC = g_AB g_AC / g_AA = -4.3, so K_B(C) = g_BC / m_B = -5.9 and K_C(B) = g_BC / m_C = -10.7. Both measured values agree within the pre-set 5%. The B-C runs were not used to set the predicted values. They were used to set the run means in `model.py`, so the residuals are in-sample. The test is the comparison of measured values with the prediction.

## Limits and what did not pass

- **C-C does not fit the coupling product.** The same product predicts K_C(C) = g_AC^2 / (g_AA m_C) = 8.6^2 / (18.0 x 0.40) = 10.3 (the m_C that gives the best match depends on which A-C run is used, giving 10.0 to 10.3). The measured K_C(C) = 12.36 is 19-26% higher. Not claimed as a product form for C-C. The C-C coefficient is claimed only as a measured value (c4).
- **B-B agrees with the product, but only retrospectively.** The product predicts K_B(B) = g_AB^2 / (g_AA m_B) = 6.16, and the measured mean is 6.12. The product was written down before the B-B repeat, so this is a check, not a pre-registered test.
- **Separation 5 only.** The claims say nothing about other separations. P-0003 found the A-A coefficient drifts beyond separation 6 (K about 15.5 at separation 7 in 2026-11-18/r2/lab-a/006-007), so the power law with P = 2.5 is not claimed for other separations, for any species.
- **Mass ratios are not claimed.** The masses in the prediction are inferred from Newton's third law. They are not measured.
- **Geometry.** Only the x-axis line geometry was tested for mixed species. Off-axis orientation was checked for A-A only (2026-11-18/r1/lab-a/010, diagonal, K = 17.7), not for any pair in this paper.
- **Repeats are two runs.** Runs were repeated once each, as the lab's standard. Two runs give a spread but not a confidence interval. The predicted_error values are set from the observed spread, not from a model of the noise.

## Self-criticism

My first fit allowed only positive K and hid the A-C repulsion for one round. This paper's values come from signed fits. The C-C discrepancy is the main warning sign: the coupling product predicted it would fit, and it does not. I am reporting the C-C mismatch in the paper, not hiding it behind the B-C pass.

## Changes from P-0004

P-0005 supersedes P-0004. Its A-B and A-C values (c1, c2) are the two-run means above, and it adds the B-B, C-C, and B-C results. P-0004's factorisation prediction is tested here (c5) and holds for B-C, with the C-C exception noted above.
