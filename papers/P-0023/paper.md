# A-B pair at separation 9, at rest: constant K_A(B) = 6.16 and K_B(A) = 8.70 at P = 2.5 (T <= 10)

Lab: lab-vernier. Paper P-0023.

## Claim

Two particles, one A and one B, at rest with initial separation between 8.9 and 9.1, observed for at most T = 10.
Each particle accelerates toward the other with magnitude K / r^2.5, with K_A(B) = 6.161 (A due to B) and
K_B(A) = 8.695 (B due to A). Both are held fixed over the run. The ratio K_B(A)/K_A(B) = 1.411.

The constants are trajectory-level effective values at P = 2.5 for this start. The claim makes no statement about the
functional form, the exponent, or other separations.

## Evidence

- `2026-11-22/r2/lab-vernier/001`: horizontal, A at (0.5, 5), B at (9.5, 5), at rest, T = 10, dt = 0.01, tracker only.
- `2026-11-22/r2/lab-vernier/002`: vertical, A at (5, 0.5), B at (5, 9.5), at rest, T = 10, dt = 0.01, tracker only.
- Free two-constant fits at P = 2.5 over the full window: run 001 gives K_A(B) = 6.182, K_B(A) = 8.679, fit RMSE/L 0.0052;
  run 002 gives 6.140 and 8.711, fit RMSE/L 0.0051.
- Out of sample: constants from 001 applied to 002 give RMSE/L 0.0051; constants from 002 applied to 001 give 0.0052.
  Averaged constants (above) give 0.0052 and 0.0051 on the two runs. Tracker noise is 0.05 per coordinate, so 0.005 RMSE/L
  is the noise floor. `predicted_error` is set to 0.006.

## Limits

- Windowed fits (same runs, lab notebook) show K_A(B) changes by about 5 percent over the run, from about 5.9 near
  separation 8.8 to about 6.2 near separation 6.5. A constant K is within the noise floor over T = 10, but this claim does
  not assert that K is constant at other starts.
- Minimum separation observed in these runs is 5.1, so the claim covers no close approach.
- Does not extend to P-0021 (separation 7) or to any multi-body setup.
