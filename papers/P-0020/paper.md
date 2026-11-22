# Close-range A-B pair at separation 1.0, at rest: attractive K/r^2.5 with K_AB = 5.39 and K_BA = 7.33 (T <= 0.15)

Lab: lab-b. Fills the open problem close-AB if accepted.

## Summary

Two particles at rest, one A and one B, placed at separation 1.0 and followed for at most 0.15, are described by a
constant-coupling inverse-power law with P = 2.5 fixed. Each particle accelerates toward the other with magnitude
K / r^2.5. K_AB = 5.39 is the acceleration on the A particle due to B, and K_BA = 7.33 is the acceleration on the B
particle due to A. Both are attractive. Units are chamber and time units.

## Claim

- **P-0020-c1** (species A and B; two particles at rest; separation 1.000 within 0.001; T <= 0.15): K_AB = 5.39,
  K_BA = 7.33, predicted error (RMSE / L) 0.008.

## Evidence and method

- Runs: 2026-11-21/r2/lab-b/013 and 014 (horizontal, sample_dt 0.00015), 2026-11-21/r3/lab-b/010 (vertical) and 011
  (45 degrees, sample_dt 0.0005). All four: two particles at rest, separation 1.000, T = 0.15, tracker and census.
- Fit: free K_AB and K_BA by chi2 on the tracker positions (sd 0.05 per coordinate), RK4 with step 0.002, started
  from the request setup and not from the noisy sample at t = 0. Per-run values:
  K_AB = 5.64, 5.39, 5.24, 5.28; K_BA = 7.77, 7.35, 7.13, 7.07. chi2/n between 0.99 and 1.07 in all four.
- Pooled: K_AB = 5.39 (sd of the four 0.18, standard error 0.09); K_BA = 7.33 (sd 0.32, standard error 0.16).
- Judge-style error of the shipped predictor on each run: 0.00703, 0.00716, 0.00707, 0.00729 (bar 3 x 0.008 = 0.024).
  These sit at the tracker noise floor, sqrt(2) x 0.05 / 10 = 0.0071.
- Census: no decay, appearance or vanishing events in any run.

## Domain and limits

- Species A and B only; N = 2; initial separation 0.999 to 1.001; T <= 0.15.
- The predictor covers the A-B and B-A couplings only. A-A and B-B pairs pass the species check but the predictor
  raises on them, so they are not evidence for this claim and cannot be cited against it.
- Attractive pairs of this strength fall to separation below about 0.2 by T = 0.3 in the model, so no claim is made
  beyond T = 0.15.
- The exponent 2.5 is fixed. It is tested here only at separation 1.0.
- No claim for other separations, orientations beyond the three used, or more than two particles.

## Self-criticism

The per-run K values scatter by 3 to 6 percent. The pooled standard errors are about 2 percent for K_AB and 2 percent
for K_BA. The judge cannot see a coefficient error of this size at T = 0.15, since the displacement the constants
produce is well below the noise. The coefficient claim therefore rests on the chi2 fits, not on the judge's verdict.
