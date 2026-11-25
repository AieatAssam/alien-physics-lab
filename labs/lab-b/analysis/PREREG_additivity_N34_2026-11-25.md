# Pre-registration: pairwise additivity at N = 3 and N = 4 (requests 2026-11-25/r2/lab-b/007 and 008)

Written before scoring (2026-11-25, round 3). Predictor code: `additivity_N34_2026-11-25.py` in this directory.

## Predictor (no free parameters)

- Pairwise sum. Each ordered pair (i, j): particle i accelerates toward j with magnitude K(r)/r^2.5, r the current separation.
- K(r): the P-0027 piecewise-linear table, nodes r = 3..9 at 17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624 (copied from `papers/P-0027/model.py`, checked against P-0028's copy). Clamped outside [3, 9].
- Accelerations add (no three-body term). RK4 with step 0.001. Specular walls at 0 and 10.
- All particles at rest at t = 0 (start state from the request setup, not the noisy t = 0 sample).

## Runs

- 007: 3 A, equilateral, side 6.0, centre (5, 5), T = 2.0, sample_dt 0.01, tracker.
- 008: 4 A, square, side 5.0 (diagonal 7.07), centre (5, 5), T = 1.5, sample_dt 0.01, tracker.
- Both sit inside P-0028's domain (species A, N <= 8, every pair in [3, 9]): pair separations are 5.0 to 7.07 (run 007: 6.0 only).

## Judgement (fixed before scoring)

- Judged RMSE/L over 0 < t <= T, all particles, both coordinates, L = 10, noise sd 0.05 per coordinate.
- Falsifier 1: judged RMSE/L > 0.021 (3 x predicted_error 0.007, the review bar) in either run. Falsifies pairwise additivity at that N.
- Falsifier 2: a fitted global factor f on K (K -> f K over the whole run, one parameter for both runs jointly) with |f - 1| > 3 sigma_f, sigma_f from delta chi2 = 1 at sigma = 0.05.
- Supported (not confirmed): neither falsifier fires. Power caveat: the zero-force null is reported; if it is under 0.021, the judged test has no power for that run, and only falsifier 2 can discriminate.
- Not a test beyond the sampled geometry: symmetric configurations only.
