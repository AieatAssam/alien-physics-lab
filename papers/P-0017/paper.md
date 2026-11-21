# Close-range B-B pair at separation 1.0, at rest: attractive K/r^2.5 law with K = 3.98 (T <= 0.15)

## Summary

Two B particles at rest, placed at separation 1.0 and followed for at most 0.15, are described by a constant-K
inverse-power law a = K / r^2.5 with P = 2.5 fixed and K = 3.98 on each particle (attractive). The predictor covers
only the B-B pair.

## Claim

- **c1** (species B; two particles at rest; separation 1.0; duration at most 0.15): K = 3.98, predicted error (RMSE/L) 0.008.

## Method

- Data: 2026-11-21/r1/lab-b/007, 2026-11-21/r2/lab-b/009, 2026-11-21/r2/lab-b/010. Two B particles at rest, sample_dt 0.0005, tracker and census.
- Fit: one K, chi2 on the tracker positions (sd 0.05 per coordinate), RK4 with step 0.002, starting from the request setup
  and not from the noisy sample at t = 0.
- Per-run fits: K = 4.13, 3.86, 3.97 (chi2, sd 0.05; per-run 1-sigma about 0.21). Pooled mean 3.98, standard error about 0.1.
- The shipped predictor's judge-style error is at the tracker noise floor, about 0.007 on each run.
- Census: no decay, appearance or vanishing events.

## Limits

- One separation (1.0) and duration T <= 0.15. At T = 0.3 an attractive pair of this strength comes within about 0.1 of itself
  in the model, so no claim is made beyond 0.15.
- P = 2.5 is fixed and tested only at r = 1.0.
- No claim for other species, mixed pairs, other separations, or more than two particles.

## Self-criticism

The per-run fit uncertainty is 2 to 5 percent, so the pooled K is good to roughly 2 to 3 percent. The predicted error 0.008
sits at the judged noise floor, which cannot see a 3 percent coefficient change at this duration.
