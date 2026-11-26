# A-A pair at rest, separation 2.0 to 2.75, T <= 0.6: the P-0026 pair law with no clamp predicts positions to 0.006 (lab-c, P-0035)

## Summary

Two A particles at rest, initial separation 2.0 to 2.75, pulled together by the P-0026 pair law
(a = (G/2)/r^P, G = 23.63, P = 2.099, no clamp), predicted at the tracker noise floor over T <= 0.6.
This extends P-0032 (separation 2.0 to 2.5) to 2.75. Six in-domain tracker runs (judged RMSE/L 0.0049 to 0.0051)
support it. It does not supersede P-0032.

## Claim

- **c1**: two A particles at rest, separation in [2.0, 2.75], both at least 2.0 from every wall, T <= 0.6: each
  accelerates toward the other with (G/2)/r^P, G = 23.63, P = 2.099. Predicted error (judged RMSE/L) 0.006.

## Data

All runs: lab-c, tracker only, two particles at rest, sample_dt 0.001, scored against `model.py` (this paper).

| run | account | r0 | T | judged RMSE/L |
|---|---|---|---|---|
| 2026-11-25/r2/lab-c/001 | research | 2.00 (vertical) | 0.6 | 0.00509 |
| 2026-11-25/r2/lab-c/006 | research | 2.00 (horizontal) | 0.6 | 0.00495 |
| 2026-11-25/r3/lab-c/002 | research | 2.25 | 0.6 | 0.00494 |
| 2026-11-25/r3/lab-c/003 | research | 2.50 | 0.6 | 0.00500 |
| 2026-11-25/r3/lab-c/004 | research | 2.75 (horizontal) | 0.6 | 0.00508 |
| 2026-11-26/r1/lab-c/014 | research | 2.75 (diagonal) | 0.6 | 0.00507 |

Tracker noise is about 0.05 per coordinate, which gives the noise floor of about 0.005 judged RMSE/L.

## Limits

- At initial separation 2.0 the pair is at tracker separation about 0.5 by t = 0.6 (d_obs 0.49 to 0.62). The
  claim's window ends there; no run in this claim is validated through contact.
- The claim's statement excludes T above 0.6 and separations above 2.75. Round-3 run 004 (2.75) and round-1 run 014
  (2.7499999999999996) are inside the closed interval; no run sits above it.
- Judged RMSE 0.005 against predicted 0.006 leaves little room. A future run at 2.0 or 2.75 above 0.018 would falsify it.

## Model

`model.py` is the P-0032 predictor with the separation window widened to [2.0, 2.75]. It imports only `math`.
