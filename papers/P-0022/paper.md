# A-B pair at separation 2, at rest: effective couplings at P = 2.5 (T <= 0.8)

Lab: lab-b. Paper P-0022.

## Claim

Two particles, one A and one B, at rest with initial separation between 1.95 and 2.05, observed for at most T = 0.8.
Each particle accelerates toward the other with magnitude K / r^2.5, with K_A(B) = 7.59 for A (due to B) and
K_B(A) = 10.59 for B (due to A). Both constants are held fixed over the run.

These are effective constants at P = 2.5 for this separation band and this time window. The claim does not state a
power law across separations, makes no claim about the exponent, and says nothing about separations other than
about 2 or times beyond 0.8. Over T = 0.8 from r = 2 the separation falls to about 0.45 (model value, still falling
at T = 0.8; the measured minimum is 0.5 within tracker noise). The claim therefore covers the constant-K approach
down to about 0.5. It makes no statement about separations below 0.5, where the coupling may differ.

## Evidence

- `2026-11-22/r1/lab-b/001`: horizontal, A at x = 4.0 and B at x = 6.0 (separation 2.0), at rest, T = 0.8, dt = 0.004.
  Free two-constant fit gives K_A(B) = 7.609 +/- 0.094 and K_B(A) = 10.576 +/- 0.089, chi2/n = 1.00.
- `2026-11-22/r2/lab-b/005`: vertical, A at y = 4.0 and B at y = 6.0 (separation 2.0), at rest, T = 0.8, dt = 0.004.
  Free fit gives K_A(B) = 7.577 +/- 0.094 and K_B(A) = 10.606 +/- 0.089, chi2/n = 1.05.
- Pooled constants used here: K_A(B) = 7.59, K_B(A) = 10.59. The two orientations agree within 0.5 percent,
  which is inside one sigma. Tracker noise is 0.05 per coordinate. The judge-style RMSE/L of this model against
  each run is about 0.005, the noise floor (0.05 / L = 0.005).
- Ratio K_B(A)/K_A(B) = 1.40 in both runs. This matches the mass ratio that the other separations and species in
  lab-b's notebook suggest. It is a consistency check here, not a prediction of this claim.
- `predicted_error` is 0.008, above the noise floor.

## Model

`model.py` integrates the pair with RK4 (step 0.001), specular walls, and raises ValueError outside the domain
(separation outside [1.95, 2.05], duration above 0.8, or any non-rest particle). Imports only `math`.

## Falsifiers

A new run with two particles (one A, one B), at rest, separation in [1.95, 2.05], duration at most 0.8, where the
RMSE/L of this model exceeds 3 x 0.008 = 0.024 on any run would falsify the claim.

Third in-domain replicate requested as `2026-11-22/r3/lab-b/001` (diagonal orientation), for a later update.
