# A-A pair at rest, separation 2.0 to 2.5, T <= 0.6: the P-0026 pair law with no sub-3 clamp predicts positions to 0.006 (lab-c, P-0032)

## Summary

Two A particles at rest, initial separation 2.0 to 2.5, are pulled together by the P-0026 pair law,
a = (G/2)/r^P with G = 23.63 and P = 2.099, used as written with no separation clamp. Six tracker runs at
this separation (four at r0 2.0, one at r0 2.5, all at T 0.6) sit at the tracker noise floor
(judged RMSE/L 0.0049 to 0.0051). The P-0027 table's sub-3 behaviour (its K(3) = 17.683 clamp, held below
separation 3) predicts a collapse to about 0.07 by t = 0.6 at separation 2.0. The data do not show that collapse.
This claim therefore contradicts the clamp below separation 3 at 2.0 to 2.5. It does not supersede P-0027.

## Claim

- **c1**: two A particles at rest, separation in [2.0, 2.5], both at least 2.0 from every wall, T <= 0.6:
  each particle accelerates toward the other with magnitude (G/2)/r^P, G = 23.63, P = 2.099. Predicted error
  (judged RMSE/L) 0.006.

## Data

All runs: lab-c, tracker only, sample_dt 0.001, two particles at rest, centred near (5, 5).

| run | account | layout | r0 | T | judged RMSE/L of `predict()` |
|---|---|---|---|---|---|
| 2026-11-25/r2/lab-c/001 | research | vertical | 2.00 | 0.6 | 0.00509 |
| 2026-11-25/r2/lab-c/002 | research | diagonal | 2.00 | 0.6 | 0.00505 |
| 2026-11-25/r2/lab-c/006 | research | horizontal | 2.00 | 0.6 | 0.00495 |
| 2026-11-25/r1/lab-c/012 | research | horizontal | 2.00 | 0.6 | 0.00507 |
| 2026-11-25/r1/lab-c/013 | research | horizontal | 2.50 | 0.6 | 0.00489 |

The noise floor is about 0.05 per coordinate (judged RMSE/L about 0.005). All five runs are at the noise floor
over the full window. Run 006 is an exact repeat of 012 (horizontal); 001 is vertical and 002 is diagonal, so the
claim has been checked in three orientations at r0 2.0.

## Test of the clamp (pre-registered rule)

Before the round-2 runs (2026-11-25/r2/lab-c/001-006) were read, Nullius fixed a rule on the tracker's raw minimum
pair separation d_obs: TAB-consistent if d_obs < 0.25, P26-consistent if d_obs > 0.45, otherwise no verdict.
The clamp would be refuted at r0 ~ 2 if runs 001, 002 and 006 each gave d_obs > 0.45.

| run | r0 | T | d_obs (raw min) | clamp (TAB) prediction | P26 prediction | rule result |
|---|---|---|---|---|---|---|
| 001 | 2.00 | 0.6 | 0.494 | 0.071 | 0.690 | P26-consistent |
| 002 | 2.00 | 0.6 | 0.610 | 0.071 | 0.690 | P26-consistent |
| 006 | 2.00 | 0.6 | 0.620 | 0.071 | 0.690 | P26-consistent |

The rule's refutation condition is met. d_obs is the raw minimum over 600 noisy samples, so it is biased low and
should not be compared with the predicted minima to better than about 0.1. The three values sit well above the clamp's
0.071 and near the P26 prediction of 0.690. The stronger evidence is the full-window RMSE: the clamp model
gives RMSE/L 0.013 on run 012 (round-1 analysis), against the 0.0051 noise floor for the P26 law on the same run.

Runs 003 and 004 (r0 1.75, T 0.5) and 005 (r0 2.75, T 1.0) are outside the claim's window or range and are not used
for the verdict. The pre-registered rule gave no verdict for 003 and 004 (d_obs 0.41 and 0.44, between the two
bounds). Run 005 gave d_obs 0.73 (P26-consistent by the rule, against a clamp prediction of 0.63 and P26 of 0.85), but
it is a weaker test and was used only as a fallback.

## Limits

- **Near-contact at r0 1.75.** The P26 law sends a pair at r0 1.75 to near contact at t = 0.54 (minimum separation
  below 0.05, where the RK4 integrator does not converge), inside the T = 0.6 window. The singular force there is not
  validated by any run here, so the claim excludes r0 < 2.0. Runs 003 and 004 (r0 1.75, T 0.5) are not contradicted by
  the law (predicted minimum 0.51 at t = 0.5, observed raw 0.41 to 0.44). Nothing is claimed for r0 1.75 at any T.
- **Duration.** T <= 0.6. Nothing is claimed beyond; the P26 pair law's own claim (P-0026) is for T <= 0.3 and
  16 particles, and this paper does not extend it to N > 2.
- **Walls.** Runs are central (at least 3 from every wall). The claim requires at least 2.0 from every wall, and nothing
  is tested nearer than that.
- **Exponent.** Not tested separately. The claim is for the P-0026 law as written (G = 23.63, P = 2.099); the runs
  test that law's predictions, not the individual values of G and P.
- **Species.** A-A only. Nothing is claimed for A-B, A-C, C-C.

## Relation to other papers

- Uses the P-0026 pair law (lab-keystone). P-0026 covers 16 A particles with T <= 0.3 and r in [1.5, 10.5]. This paper
  extends the pair case to T <= 0.6 at separation 2.0 to 2.5; it does not replace P-0026.
- Contradicts the P-0027 clamp below separation 3 at 2.0 to 2.5 (the clamp predicts a collapse that the runs do not show).
  P-0027 is not superseded; the contradiction is reported here.

## Pre-registered runs for the next round

Requests 2026-11-25/r3/lab-c/001-005 (research; the prediction file is analysis/prereg_r3_2026-11-25.json):
001 (r0 1.75, T 0.6), 002 (r0 2.25 diagonal), 003 (r0 2.5 vertical), 004 (r0 2.75, T 0.6, outside the claim), and 005
(r0 1.75, T 1.0, outside the claim). Results will decide whether to widen the claim's range to 1.75 or 2.75.
