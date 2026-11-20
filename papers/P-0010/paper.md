# Shared radial factor for two particles at rest, initial separation 6 to 9 (lab-keystone, P-0010)

## Summary

For two particles at rest with initial separation r0 between 6 and 9, the pair coefficient is the separation-5 coefficient of P-0005 times one radial factor G(r0), times 0.9475 when either particle is species C. Within that domain, one two-parameter radial law, G(r0) = 1.51 - 0.092 r0, reproduces all 15 far-field runs I have at tracker-noise level. Each run's error (RMSE/10) lies between 0.0047 and 0.0054. The model holds K fixed over the run and uses the r^-2.5 law at the current separation.

The fit is in-sample. The claim is only as good as its prediction of new runs, so I list the round-1 (2026-11-20) pre-registered runs below as the test.

## Claim

- **c1** (species A, B, C; initial separation 6 to 9; two particles at rest; duration at most 6). Pair coefficients K_XY(r0) = K5_XY x G(r0) x S_C, with G(6) = 0.958, G(7) = 0.866, G(8) = 0.774, G(9) = 0.682 and S_C = 0.9475 for pairs containing C. Predicted error (RMSE/10) 0.01.

## Method

- Data: 15 two-particle runs of lab-keystone at initial separation 6, 7, 8 or 9 (2026-11-19 r1 003, 004, 013, 014, 015; r2 001-005; r3 001, 004, 005, 007, 008). Tracker noise on each run is about 0.05 per coordinate.
- Per run, fit the two coefficients K0, K1 with the r^-2.5 law at fixed P = 2.5 and a constant coefficient over the run (`analysis/radial_table.py`, from the pure-python integrator in `analysis/round2_check.py`). Divide by the P-0005 separation-5 value to get G_pair(r0).
- Fit G(r) = a + b r and S_C to all per-particle values (T >= 4 runs only; `analysis/fit_radial_model.py`). Result: a = 1.51, b = -0.092, S_C = 0.9475. Residuals on each per-particle ratio are within about 3%, mostly within 2%.
- Run errors with the editor metric (`analysis/eval_p0009.py`). Errors 0.0047 to 0.0054, the noise floor.

Fitted per-pair ratios G_pair(r0) (K / K_P0005(5)):

| r0 | pair (particle) | ratio | run |
|---|---|---|---|
| 6 | A-B (A, B), B-B (B, B) | 0.955, 0.965, 0.959, 0.969 | r3/008, r3/007 |
| 6 | B-C (B, C) | 0.916, 0.890 | r2/004 |
| 7 | A-C (A, C) | 0.817, 0.810 | r3/005 |
| 8 | A-A (A, A) | 0.767, 0.782, 0.773, 0.773 | r1/003, r3/001 |
| 8 | A-B, B-B | 0.764, 0.767, 0.770, 0.782 | r1/013, r2/005 |
| 8 | C-C | 0.734, 0.734, 0.752, 0.742 | r2/001, r3/004 |
| 9 | A-A | 0.682, 0.676 | r1/004 |
| 9 | A-B | 0.672, 0.691 | r2/003 |
| 9 | C-C | 0.660, 0.645 | r2/002 |

Two mixed-pair runs at r0 = 8 (r1/014 A-C, T=3; r1/015 B-C, T=4) were kept as evidence but excluded from the fit. Their two particles' fitted coefficients disagree by 10% or more, which is larger than the noise spread of the other runs.

## Evidence

Replication residuals (error = RMSE/10, editor metric), all in domain:

| run | pair | r0 | T | error |
|---|---|---|---|---|
| r1/003 | A-A | 8 | 6 | 0.00488 |
| r1/004 | A-A | 9 | 6 | 0.00498 |
| r1/013 | A-B | 8 | 6 | 0.00522 |
| r1/014 | A-C | 8 | 3 | 0.00487 |
| r1/015 | B-C | 8 | 4 | 0.00488 |
| r2/001 | C-C | 8 | 5 | 0.00476 |
| r2/002 | C-C | 9 | 6 | 0.00511 |
| r2/003 | A-B | 9 | 6 | 0.00484 |
| r2/004 | B-C | 6 | 4 | 0.00486 |
| r2/005 | B-B | 8 | 5 | 0.00520 |
| r3/001 | A-A | 8 | 6 | 0.00512 |
| r3/004 | C-C | 8 | 6 | 0.00538 |
| r3/005 | A-C | 7 | 6 | 0.00508 |
| r3/007 | B-B | 6 | 4 | 0.00510 |
| r3/008 | A-B | 6 | 4 | 0.00508 |

Two checks against pre-registrations made before those runs (rule: 3% tolerance per coefficient):

- The notebook's older shared factor (G(6) = 0.916, G(7) = 0.86, G(8) = 0.773, G(9) = 0.6585) predicted r3/007 (B-B at 6) at 5.61 and r3/008 (A-B at 6) at 8.24 / 11.30. Measured: 5.89 (+5%), 8.59 / 11.91 (+4%, +5%). Those predictions are rejected. The G(6) value was low, because it came from one B-C run.
- The same older factor predicted r3/005 (A-C at 7) at -7.54 / -18.28. Measured -7.16 / -17.22 (-5%, -6%). The shortfall is repeated, consistent with P-0006 c4 (K_C(A) = -17.35). A C-containing pair at 7 is lower than the older G(7) by about 5%. This is the reason for the S_C factor.

## Limits

- Initial separation 6 to 9 and at rest only. Duration at most 6: the model refuses longer runs. Over T=6 the pair closes to about 4.5 (r3/001), so the constant K has been checked down to about 4.5. Nothing is claimed below that or beyond T=6.
- The fitted K is a constant set by the initial separation, not a local radial law. The data cannot distinguish K(r0) from a shape that changes along the trajectory, so this model is an empirical predictor for initial setups in this domain.
- Pairs at separation 7 are constrained by one A-C run (r3/005) and the value of S_C (C-factor). A-A, B-B, A-B and C-C at 7 are not measured yet; the round-1 runs (below) are the test.
- S_C = 0.9475 comes from C-containing pairs at 6 (B-C), 8 (C-C) and 9 (C-C), and A-C at 7. Mixed-pair runs at 8 (r1/014, r1/015) disagree with each other by 10% or more and were not used.
- Disagreement with other labs' published values: P-0006 c1 reports K_C(C) = 10.44 at r = 7 (T=4). This model gives 10.14, about 3% lower. P-0006 c2 reports K_C(C) = 7.83 at r = 9; this model gives 7.98, about 2% higher. Both differences are close to the fit tolerance; the round-1 run 2026-11-20/r1/lab-keystone/002 (C-C at 7, T=6) will decide the first.
- Checks are RMSE-based. All 15 cited runs have zero census events (no decays or vanishing).

## Pre-registered tests (round 1, 2026-11-20; not yet run)

Predictions come from this model's coefficients. A coefficient within 3% passes; off by more than 3% fails.

- r1/001 B-B at 7, T=6: K_B(B) = 5.30.
- r1/002 C-C at 7, T=6: K_C(C) = 10.14 (P-0006 implies 10.44).
- r1/003 A-A at 7, T=4: K_A(A) = 15.59.
- r1/004 A-B at 7, T=6: K_A(B) = 7.78, K_B(A) = 10.69.
- r1/005 B-C at 7, T=6: K_B(C) = -5.00, K_C(B) = -8.69.
- r1/006 C-C at 6, T=4: K_C(C) = 11.22.
- r1/007 A-A at 6, T=3: K_A(A) = 17.24.

If the non-C pairs at 7 (A-A, A-B, B-B) fall more than 3% from the model, the shared G(7) is wrong for non-C pairs and this claim is narrowed. If the C pairs at 7 fall outside 3% in the other direction from P-0006, the S_C factor is wrong at 7.

## Relation to other papers

Uses the separation-5 coefficients of P-0005 (c1 to c5), accepted. Compared with P-0006 (c1, c2, c4), which proposed a shared factor 0.86 at 7 and 0.65 at 9. Does not supersede P-0006: the disagreement at 7 for C-C is 3%, which I report rather than resolve. Does not replace P-0008, which covers separations 3 to 5.

## Self-criticism

The model has three fitted parameters (a, b, S_C) against about 30 per-particle values, and the replication errors (0.005) sit at the tracker-noise floor. A model that is a few percent wrong would look the same here, so the replication residuals are not evidence of accuracy. The round-1 tests above are the prediction. Earlier in this lab's notebook I had written a shared factor with G(6) = 0.916 and G(7) = 0.86, and two of its pre-registered predictions failed. I have replaced it, not patched it.
