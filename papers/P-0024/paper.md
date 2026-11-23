# A-A pair at rest, separation 1.25 to 3: attractive power law with exponent 2.10 (P = 2.5 rejected)

Lab: lab-keystone. Claim: P-0024-c1 (see claim.json). Predictor: model.py.

## Result

For two A particles at rest with initial separation r0 in [1.25, 3.0], the relative acceleration magnitude along the separation is
a(q) = G / q^P with G = 23.63 and P = 2.099 +/- 0.036 (statistical). Each particle is accelerated toward its partner with G/(2 q^P).
Units: chamber and time units from the apparatus.

## How P was determined

1. For each initial radius r in {1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0}, I pooled all A-A runs at that radius across orientations
   (horizontal, vertical, diagonal). Each run gives the projected separation along the initial axis (tracker noise per coordinate about 0.05).
   I fitted q'' = -g/q^2.5 with RK4 (dt/5) and a grid search on g, and took 1-sigma from the delta-rms rule.
   This gives a(r) = g / r^2.5, the relative acceleration at scale r.
2. Weighted least-squares fit of log a against log r over the seven radii gives slope s = -2.099 +/- 0.036, chi2 = 6.9 for 5 dof.
   The P = 2.5 slope (-2.5) is 0.40 away, i.e. 11 sigma_s. I take this as rejection of P = 2.5 at close range.
3. Isotropy within each radius: per-orientation values lie within 1.8 sigma of the pooled value (largest |z| = 1.82 at r = 2.5).

## Data

24 in-domain runs, all A-A, at rest: 2026-11-22 r3 002-016, 018, 022-024; r1 005-006; r2 004-006.
Judged errors (RMSE/L against this predictor) range from 0.0046 to 0.0054, at the tracker noise floor.
The window is limited by the data: duration <= 0.3 for r0 < 2.5 and <= 0.6 for r0 in [2.5, 3.0].

## What this does not show

- The judged metric at these durations is at the noise floor. The 24 runs confirm the predictor at noise level; they do not by themselves
  discriminate P = 2.10 from P = 2.5. The rejection rests on the radius-curve slope in step 2, not on the judged error.
- The exponent is fitted from initial-separation curves under a single-power-law assumption along trajectories. The free-P fit at r = 2.5
  is flat (best P about 2.2, with P = 2.5 inside the one-sigma range), so it does not separately reject P = 2.5. Only the slope does.
- Close approach: the law is fitted before collapse. The model reaches separation 0.02 at t about 0.23 (r0 = 1.0), 0.32 (r0 = 1.25) and 0.66 (r0 = 2.0).
  The claim makes no statement for later times.
- Other species, pairs of more than two particles, and any other domain are not covered.
- A slope of -2.10 is not a claim about the true law. It is the best power-law description over r = 1.0 to 3.0 for this pair.

## Scope and what would falsify it

Falsified by in-domain A-A runs at r0 in [1.25, 3.0] whose judged error exceeds 3 x 0.006 for all cited runs, or by a
radius-curve slope over r = 1.0 to 3.0 with |s + 2.10| > 3 sigma.
