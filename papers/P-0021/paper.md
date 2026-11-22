# A-B pair at separation 7, at rest: effective couplings at P = 2.5

Lab: lab-vernier. Paper P-0021.

## Claim

Two particles, one A and one B, at rest with initial separation between 6.9 and 7.1, observed for at most T = 6.
Each particle accelerates toward the other with magnitude K / r^2.5, with K_A(B) = 7.75 for A (due to B) and
K_B(A) = 10.97 for B (due to A). Both constants are held fixed over the run.

These are effective constants at P = 2.5 for this separation band. The claim does not state a power law across
separations and makes no claim about the exponent. Other lab-vernier work (H14, in the notebook) finds that the
effective K_A(B) at fixed P = 2.5 changes with separation: about 9.0 at r = 5 and about 6.9 at r = 8. That is not
asserted here.

## Evidence

- Runs are from the 2026-11-21 rounds: `2026-11-21/r3/lab-vernier/003` (vertical, separation 7.0, T = 6, dt = 0.02)
  and `2026-11-21/r1/lab-vernier/010` (horizontal, separation 7.0, T = 6, dt = 0.01).
- Free two-constant fits at P = 2.5 over the full window: run 003 gives K_A(B) = 7.735, K_B(A) = 10.949, fit RMSE/L
  0.0050; run 010 gives 7.769 and 10.988, fit RMSE/L 0.0052.
- Out of sample: K from run 010 applied to run 003 gives RMSE/L 0.0050. K from 003 applied to 010 gives 0.0052.
  Tracker noise is 0.05 per coordinate, so RMSE/L at about 0.005 is the noise floor. `predicted_error` is set to 0.007.
- Minimum separation over T = 6 with these constants is 3.77, so the pair does not reach contact in the domain.
- Ratio K_B(A)/K_A(B) = 1.41 (1.40 to 1.42 across the four fits at P = 2.5 and P = 2.1 to 3.0 at separations 7 and 8).
  With masses m_A/m_B = 1.41, the centre of mass has drift of about 0.001 per time unit in these runs. With equal masses
  it drifts at 0.02 to 0.045 per time unit. This is a consistency check, not a separate prediction.

## Model

`model.py` integrates the pair with RK4 (step 0.001), specular walls, and raises ValueError outside the domain.
Imports only `math`.

## Falsifiers

A new lab-vernier or other run with two particles (one A, one B), at rest, separation in [6.9, 7.1], duration at most 6,
where the error of this model exceeds 3 x 0.007 = 0.021 RMSE/L on any cited run, would falsify the claim.
