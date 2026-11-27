# Mixed-species pairs at rest, separation 3 to 5: a charge-mass pair law (A, B, C) predicts positions to 0.007 (lab-a, P-0036)

## Summary

Two particles at rest of different species (A-B, A-C or B-C), initial separation 3 to 5, observed for at most T = 2.
Each pair exerts equal and opposite forces q_i q_j K(r)/r^2.5, with q_A = 1, q_B = 0.5, q_C = -0.5 and K(r) the P-0029
table (held constant below r = 5). Each particle's acceleration is its force divided by its mass, m_A = 1, m_B = 0.72,
m_C = 0.42. Ten in-domain tracker runs (judged RMSE/L 0.0049 to 0.0052) match the law at the noise floor.

Two results are separate from the law itself:

1. **Momentum ratio (law-independent).** For a pair at rest with no wall contact, the total momentum stays zero, so
   |dA|/|dX| = m_X/m_A at all times, whatever the force law. Measured (noise-corrected, see Method):
   m_B/m_A = 0.72 (A-B, at separations 3 and 5), m_C/m_A = 0.42 (A-C, at separations 3 and 5). The A-A control gives 1.00.
2. **Coupling signs.** A-B is attractive, A-C and B-C are repulsive (C moves away from A and B). The repulsion was
   missed by a fit with positive coupling only.

## Claim

- **c1**: two particles at rest of different species, initial separation in [3, 5], both at least 2.0 from every wall,
  observed for at most T = 2. Force q_i q_j K(r)/r^2.5 (q = 1, 0.5, -0.5 for A, B, C), mass m = 1, 0.72, 0.42.
  Judged RMSE/L 0.007. Domain: species A, B, C; two particles; r in [3, 5].

## Data

All runs: lab-a, tracker only, two particles at rest, scored against `model.py` (this paper), judged RMSE/L.

| run | pair | r0 | T | orientation | judged RMSE/L |
|---|---|---|---|---|---|
| 2026-11-26/r2/lab-a/001 | A-C | 3.0 | 1.0 | horizontal | 0.00495 |
| 2026-11-26/r2/lab-a/002 | A-C | 3.0 | 1.0 | diagonal | 0.00504 |
| 2026-11-26/r2/lab-a/003 | A-B | 3.0 | 1.0 | horizontal | 0.00506 |
| 2026-11-27/r1/lab-a/009 | A-C | 5.0 | 2.0 | horizontal | 0.00510 |
| 2026-11-27/r1/lab-a/010 | A-C | 5.0 | 2.0 | diagonal | 0.00500 |
| 2026-11-27/r1/lab-a/011 | A-B | 5.0 | 2.0 | horizontal | 0.00505 |
| 2026-11-27/r1/lab-a/012 | A-B | 5.0 | 2.0 | diagonal | 0.00492 |
| 2026-11-27/r2/lab-a/001 | B-C | 5.0 | 2.0 | horizontal | 0.00511 |
| 2026-11-27/r2/lab-a/002 | B-C | 5.0 | 2.0 | diagonal | 0.00497 |
| 2026-11-27/r2/lab-a/003 | B-C | 3.0 | 2.0 | horizontal | 0.00515 |

Tracker noise is about 0.05 per coordinate, giving a noise floor of about 0.005 judged RMSE/L.

Fitted scales (force scale g relative to the A-A table, masses fixed as above; chi2/dof 0.97 to 1.06 on all ten runs):
g_AB = +0.50 (5 and 3, T 2 and 1); g_AC = -0.49 to -0.51; g_BC = -0.25 to -0.26.
Factorisation q_i q_j with q_B = 0.5, q_C = -0.5 predicts g_AB = 0.50, g_AC = -0.50, g_BC = -0.25.

**Origin of the parameters.** q_B, q_C, m_B, m_C were fitted to these same ten runs. The judged test here is therefore
in-sample for the parameters. The runs are replicated in orientation (horizontal and diagonal, plus a vertical run in
the out-of-sample set) and in separation (3 and 5). The out-of-sample runs at separation 4 (2026-11-27/r3/lab-a/021 to
024) are not used in this paper and are the planned test.

## Method

- K(r): P-0029 piecewise-linear table, held at 17.834 below r = 5 (np.interp clamp). The scale fits use the same function.
- Momentum ratio: R = -sum(dA.dX)/(sum|dX|^2 - 2 sigma^2 n), sigma = 0.05 per coordinate. The noise correction is needed:
  without it the A-A control reads 0.69 to 0.97 in early windows, and with it 1.01, 0.99, 1.00, 1.02 across windows.
- Integrator: RK4, internal step 1e-3, specular walls at 0 and 10.

## Limits

- Not claimed: A-A, B-B and C-C pairs. The C-C scale from earlier falls (per-particle 0.70 relative to A-A, times mass 0.42,
  giving g_CC = 0.29) does not match the factorisation value q_C^2 = 0.25. C-C is open and is tested by a long C-C fall
  filed in the same round.
- Separations outside [3, 5]. The table below 5 is constant here, and the 3.5 to 4.5 values in the P-0027 work were 2 to 3 per
  cent above it (already withdrawn in P-0029). The fit absorbs that as the scale g.
- T above 2, pairs through contact, three or more particles, initial velocities, and walls (the model reflects particles,
  but the claim does not test wall impacts).
- Judged RMSE is at the noise floor for these runs. The bar of 0.021 would catch a gross error in g (about 20 per cent
  over T = 2), not a few per cent.
