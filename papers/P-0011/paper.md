# Tracker noise for a lone particle: white, Gaussian, sd 0.050 per coordinate, species-independent, no wall clipping (lab-vernier, P-0011)

## Summary

For a single particle the tracker's position error is zero-mean, white, Gaussian-shaped and has standard deviation 0.050 per coordinate. The sd does not depend on species within 2.5% (A, B, C). The tracker does not censor at the wall: a particle 0.05 from x = 0 reports negative x in 17% of samples with no change in the residual mean. All statements are for the tracker only; no claim is made about the dynamics here.

## Data

Seven lone-particle runs (N = 1), all with the tracker and no census events:

| request | species | start | velocity | T | dt | sd x | sd y |
|---|---|---|---|---|---|---|---|
| 2026-11-19/r1/lab-vernier/001 | A | (5,5) | 0 | 20 | 0.01 | 0.0499 | 0.0512 |
| 2026-11-19/r1/lab-vernier/002 | A | (0.3,9.7) | 0 | 20 | 0.01 | 0.0505 | 0.0506 |
| 2026-11-19/r1/lab-vernier/003 | C | (5,5) | 0 | 20 | 0.01 | 0.0500 | 0.0487 |
| 2026-11-19/r1/lab-vernier/004 | B | (5,5) | 0 | 20 | 0.01 | 0.0500 | 0.0499 |
| 2026-11-19/r1/lab-vernier/006 | A | (5,5) | 0 | 100 | 0.05 | 0.0503 | 0.0503 |
| 2026-11-19/r2/lab-vernier/002 | A | (5,5) | 0 | 100 | 0.05 | 0.0494 | 0.0509 |
| 2026-11-19/r3/lab-vernier/003 | A | (0.05,5.0) | 0 | 20 | 0.01 | 0.0516 | 0.0499 |

The residual is the reported position minus the start position. The predictor (model.py) is the reflected-line law with zero velocity, so the residual is the noise.

## Results

- **c1 (pooled).** 28,014 residuals: sd 0.0502 per coordinate, mean -0.00005, kurtosis 3.02 (Gaussian is 3.00). Per-run means are within 0.002 of zero (standard error about 0.001). Lag-1 autocorrelation of x residuals: from -0.022 to +0.024 across runs (standard error about 0.022), so no detectable correlation at this resolution.
- **c2 (species).** A 0.0505 (20,010 residuals), B 0.0499 (4,002, one run), C 0.0493 (4,002, one run). Spread 2.4% of the mean. B and C have one run each.
- **c3 (walls).** At x = 0.05 the residual mean in x is -0.0000 (standard error 0.0012), and sd is 0.0516, about 2 standard errors above 0.050. Not significant at the 3-sigma level. 335 of 2001 x values are negative.

## Limits

- One start position for most runs ((5,5)). The corner run (002) and the wall run (003) cover the edges at one position each.
- No run here tests whether the noise depends on speed. The sample-timing question (a constant offset in the sample times) is not settled here; run 2026-11-20/r1/lab-vernier/004 tests it and is not used for any claim in this paper.
- B and C have one run each. The species statement in c2 is weaker for them.
- The tracker has no velocity readout, so nothing here is about velocity noise.
- No claim about the clipping of velocities or behaviour beyond the walls.
