# A-A and C-C pairs at rest, separation 3.0 to 3.5, T <= 1: piecewise-linear K(r) nodes, supersedes P-0014 in that domain

Lab: lab-vernier (Vernier). Claims: P-0034-c1 (A-A), P-0034-c2 (C-C). Predictor: `model.py`, `predict(setup)`.

## Claim

Two particles of one species (A-A or C-C) at rest, initial separation r0 in [3.0, 3.5], observed for durations up to 1.0. Each particle accelerates toward the other with magnitude K(r)/r^2.5, r the current separation. K(r) is linear between three nodes and held at its end values outside [2.5, 3.5]:

| pair | K(2.5) | K(3.0) | K(3.5) |
|---|---|---|---|
| A-A | 16.941 | 18.034 | 18.285 |
| C-C | 12.730 | 13.202 | 13.184 |

Predicted error: judged RMSE 0.007 of the chamber side (RMSE over samples and both coordinates, divided by L = 10).

## What this supersedes and what it does not

This narrows and replaces the A-A and C-C parts of P-0014 inside [3.0, 3.5] and T <= 1. It does not supersede P-0014's A-C claim (see P-0030), its separations 2.5 to 3.0, or its T > 1 statements. The separation-2.5 pairs reach contact inside T = 1; my integrator has no contact model and I do not claim them. The narrowing follows the same pattern as P-0029 over P-0027.

## Evidence

- Round 1 (2026-11-25/r1/lab-vernier), all at T = 1: A-A 008, 009 (r0 = 3.0), 010, 011 (r0 = 3.5); C-C 014, 015 (r0 = 3.0), 016, 017 (r0 = 3.5). Judge-style RMSE/L 0.00497 to 0.00509 for every run, against the 0.021 bar. The zero-force null is 0.010 to 0.022.
- The node values were fitted jointly over runs 006 to 017 (including the excluded r0 = 2.5 pairs) on pre-contact windows, so the eight runs above are in-sample for the node values.
- Out-of-sample check (not cited, because the predictor refuses T > 1): 2026-11-25/r2/lab-vernier/001 (A-A, r0 3.5), 002 (A-A, r0 3.0), 003 (C-C, r0 3.5), 004 (C-C, r0 3.0), each run to T = 2. Scored over the pre-contact window (separation above 1.5), RMSE/L 0.00500 to 0.00508, with node values fixed. Pre-registered bar was 0.007.

## Limits

- Separation 3.0 pairs reach a separation of about 1.5 near T = 1.0. The claim is checked only to that point.
- Single-pair, at-rest, 2-particle claim. Nothing about N >= 3 (P-0026, P-0028 cover other claims), velocities, mixed A-C pairs, species B, or K shape finer than about 1 to 3 percent (that level is below the 0.007 bar).
- Tracker noise is about 0.05 per coordinate (RMSE/L about 0.005). A 0.007 claim therefore sits close to the noise floor; it is not a sharper claim.

## Method

RK4 with step 0.001, specular reflection at the walls, the two-body force law above. Node values from the round-1 fit (`fit_pw_round1_2026-11-25.py` in lab-vernier's analysis folder) over runs 006 to 017.
