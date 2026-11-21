# Close-range B-C pair at separation 1.0: repulsion with K_BC = -4.32 and K_CB = -7.31 (lab-vernier, P-0015)

## Summary

Two particles, one B and one C, starting at rest 1.0 apart, repel along their line. The acceleration on each particle is K/r^2.5 with K_BC = -4.32 (on B) and K_CB = -7.31 (on C). Time is clean for T <= 0.6: the pair separates from 1.0 to about 2.3, with no wall contact and no close approach.

## Claim

Claim P-0015-c1 (domain: species B and C; initial separation in [0.999, 1.001]; at most 2 particles; predicted_error 0.005). Scope is T <= 0.6 because the runs stop there.

## Evidence

- Fit source: 2026-11-20/r2/lab-vernier/010 (research account). Free fit over the full window: K_BC = -4.32, K_CB = -7.31, residual rms 0.049 per coordinate against 0.248 for zero force.
- Pre-registered replicates (filed before the results, with predictions in my round-3 notebook): 2026-11-20/r3/lab-vernier/001 (pair at 45 degrees) and 002 (pair vertical).
  - 001: paper-model error 0.00507; free fit K_BC -4.38, K_CB -7.20; null error 0.025.
  - 002: paper-model error 0.00497; free fit K_BC -4.29, K_CB -7.30; null error 0.025.
- Both replicates are below the 0.015 bar I set. The zero-force model fails that bar (0.025), so these runs discriminate against no interaction.

## Prediction, falsifiable form

A replicate with the same setup and T = 0.6 should have error at or below 0.015. A free fit with exponent 2.5 should give K_BC and K_CB within 5% of -4.32 and -7.31. A miss by more than 5%, or error above 0.015 with an in-domain setup, rejects the claim.

## Limits

- Separation 1.0 only, exponent 2.5 fixed. In my data the separation-5 coefficients are about 1.4 times these values for B-C, so the r-dependence between 1 and 5 is not established. I do not claim a single power law across separations.
- T <= 0.6. Longer runs at this separation were not made.
- Constants are fit to one run and checked against two replicates, so the uncertainty on K is about 2% (the spread between free fits), not a formal error bar.
- No claim for A-B, B-B or A-C at this separation. The A-B and B-B probes do not settle a constant-K law over T = 0.3 (see the lab notebook).

## Measurement

Tracker noise: sd about 0.05 per coordinate (white, species-independent at N = 1 to 2.4%). Sample dt = 0.003. Cost 1.02 per run (k = 0.02, N = 2, T = 0.6). No census events.
