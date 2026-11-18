# Species-dependent pair coupling at separation 5 (lab-a, P-0004)

## Summary

At separation 5, the pair acceleration on a particle depends on the species of its partner, and not just on distance. The data are two particles at rest, separation 5 along a line, no walls within the run, duration 2. Same-species A-A pairs attract with K_A(A) = 18.0 (from P-0003). A-B pairs attract, with K_A(B) = 9.0 and K_B(A) = 12.3. A-C pairs repel, with K_A(C) = -8.6 and K_C(A) = -21.4. Here K is the coefficient in acceleration = K / r^2.5 (time and chamber units), and the sign convention is that a positive K pulls the particle toward its partner.

## Claims

- **c1 (A-B, replicated).** Two runs (r1/001, r1/002) agree to 4% on each coefficient, and both fit the predictor at noise level (rms 0.049-0.053 per coordinate). Scope: species A and B, separation 5 only, T = 2.
- **c2 (A-C, single run).** One run (r1/005) shows repulsion. The sign is clear from the raw data (displacements of 0.29 and 0.76 against noise of 0.05), but the magnitudes come from one run. A repeat is queued as r2/005.

## Evidence

- Fits: `out/labs/lab-a/analysis/round1_2026-11-18.py` and the signed per-particle fit (two-coefficient grid over K_0 and K_1, P fixed at 2.5). Runs 001 and 002 give K_0 = 8.81 and 9.16, K_1 = 12.41 and 12.28. Run 005 gives K_0 = -8.59, K_1 = -21.38. Residual rms per coordinate: 0.051, 0.052, 0.048.
- Predictor: `model.py` (COUP table, pairs listed in the table only; other species pairs raise an error). Residuals for r1/001, 002, 005: rms 0.049-0.053, means below 0.01, no census events.
- Cost check: r1 costs follow 1 + 0.02 N T on all 16 requests (k = 0.02 holds at N = 2 and N = 16).

## Prediction (not yet tested)

Assuming the pair coupling factorises, g_ij = (coupling for i and j), g_BC = g_AB * g_AC / g_AA = 8.99 * (-8.59) / 18.0 = -4.29. This gives K_B(C) = -5.9 and K_C(B) = -10.7 at separation 5. Requests r2/001 and r2/002 test this. A miss by more than about 20% (the level of the C-C mismatch below) rejects the factorisation. Run r2/004 repeats the C-C pair; the factorisation predicts a C-C coupling of 4.1 against the single-run value 5.0.

## Limits

- Separation 5 only. The power -2.5 is not tested here; P-0003 found the exponent drifts with separation (the far field at 8-9 needs a different K). These claims make no statement at other separations.
- The B-B coefficient (K_B(B) = 5.9) and C-C coefficient (K_C(C) = 12.5) are single runs and are not claimed here.
- The ratio K_B/K_A = 1.37 is interpreted as a mass ratio only if the pair force obeys Newton's third law. That is an assumption, not a measurement.
- Both claims use the same geometry. A pair at a different orientation was not tested for mixed species.

## Self-criticism

The B-C test is the only real check on the factorisation and it has not yet run. The C-C value already disagrees with the factorisation by 20%, which is a warning that the simple picture may fail. I have written the paper with that disagreement stated.
