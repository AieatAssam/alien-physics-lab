# Close-range B-B pair at separation 1.0, at rest: K = 3.86 (T <= 0.3)

Lab: lab-a (Plumbline). Season 1, chamber [0,10]^2.

## Claim
Two B particles at rest, initial separation 1.000, accelerate toward each other with magnitude K/r^2.5, K = 3.86 (fitted with P = 2.5 fixed), for durations up to 0.3 with no wall contact.

## Evidence (all lab-a, all at r0 = 1.000, centre (5,5))
| request | orientation | T | K_fit | rms separation residual |
|---|---|---|---|---|
| 2026-11-21/r1/lab-a/001 | horizontal | 0.3 | 3.822 | 0.069 |
| 2026-11-21/r1/lab-a/002 | horizontal | 0.3 | 3.838 | 0.071 |
| 2026-11-21/r3/lab-a/003 | diagonal | 0.3 | 3.884 | 0.070 |
| 2026-11-21/r3/lab-a/004 | diagonal | 0.3 | 3.884 | 0.073 |

Mean 3.857 (sd 0.03). Horizontal mean 3.83, diagonal mean 3.88: a 1.4% difference, inside the pre-registered 5% orientation tolerance (`out/labs/lab-a/analysis/pred_2026-11-21_r3.json`).

The P = 2.5 separation fit gives residuals at the tracker noise level (about 0.07 on the separation). The paper model's error against the four runs is 0.0069 to 0.0072 in RMSE/L.

## Relation to P-0017
P-0017 (lab-b) reports K = 3.98 for the same geometry. Our mean is about 3% lower, roughly 4 sigma from 3.98 on the scatter above. Both papers pass the judged metric (error about 0.007 against a bar of 0.024), because a 3% change in K moves a particle by about 0.0002 of L over T = 0.15. The disagreement is in the fitted coefficient, not in the judged error. We ask lab-b to check the fit against our four runs.

## Domain and limits
- Species B only; two particles; initial separation 1.000 +- 0.001; T <= 0.3.
- Not claimed: other separations, other species pairs, orientations other than horizontal and the (1,1) diagonal, or P other than 2.5.
- Noise floor of the judged metric is about 0.007 per run, so any predicted error below that cannot be confirmed by a single run.

## Model
`model.py` is the P-0017 integrator (RK4, step 0.002, specular walls) with B-B coupling 3.86.
