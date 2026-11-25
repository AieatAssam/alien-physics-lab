# A-A pair at rest, separation 5 to 9: piecewise-linear K(r) table at P = 2.5, narrows and supersedes P-0027

Lab: lab-a (Plumbline). Claim: P-0029-c1 (see claim.json). Predictor: model.py. Supersedes P-0027.

## Claim

Two A particles at rest, initial separation r0 in [5.0, 9.0]. Each accelerates toward the other with magnitude K(r)/r^2.5,
where r is the current separation. K(r) is linear between these nodes (per-separation means at P = 2.5):

| r | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|
| K | 17.834 | 16.617 | 15.121 | 13.432 | 11.624 |

Duration windows: T <= 2.0 for r0 < 7, T <= 3.0 for r0 >= 7. Predicted error 0.007 (judged RMSE/L).

## Why this narrows P-0027

P-0027 claimed the same table over separations 3 to 9. Its K at 3 and 4 (17.683, 17.701) came from short runs and were not
replicated. Round 2 (`2026-11-24/r2/lab-a/001-002`) measured K = 18.25 at separation 3.5 and 18.20 at 4.5. Round 3
(`2026-11-24/r3/lab-a/003-004`) repeated both in the other orientation and got 18.18 at 3.5 and 18.24 at 4.5. Each pair agrees
within 0.5% of its own mean, and each is 2.5 to 3.2% above the table value at that separation (17.692 at 3.5 and 17.768 at 4.5,
linear interpolation of the P-0027 nodes). The fitted K(r) is 18.2 at both 3.5 and 4.5, which is not the P-0027 table. The
pre-registered rule (narrow if both replicate high) therefore applies, and the [3, 5) part of P-0027 is withdrawn.

The judged metric would not have shown this, since a 3% error in K moves RMSE/L by far less than the bar. The narrowing rests on
per-run K fits with reduced chi2 0.99 to 1.02, not on the judge.

## Evidence

All cited runs are A-A, two particles, at rest, tracker only, with initial separation in [5, 9] and duration inside the window above.
Per-run K fits give reduced chi2 0.98 to 1.10 for the in-window runs.

- r = 5 (T = 2): `2026-11-23/r3/lab-a/005-008`. Mean K 17.834 (replicate spread 0.4%).
- r = 5.5 (T = 2): `2026-11-24/r2/lab-a/003`. K 17.304 against table 17.226 (+0.5%).
- r = 5.99 (T = 2): `2026-11-24/r1/lab-a/009-010`. K 16.538, 16.670.
- r = 6 (T = 2): `2026-11-24/r1/lab-a/017-018`. K 16.592, 16.642, mean 16.617.
- r = 6.5 (T = 2): `2026-11-24/r2/lab-a/004-005`. Horizontal and diagonal K 15.808 and 15.858 (orientation difference 0.3%).
- r = 7 (T = 3): `2026-11-23/r3/lab-a/009-012`. Mean K 15.121 (spread 0.4%).
- r = 7.5 (T = 3): `2026-11-24/r2/lab-a/006`. K 14.278 against table 14.277 (0.0%).
- r = 8 (T = 3): `2026-11-24/r1/lab-a/013-016`. Mean K 13.432 (spread 1.7%).
- r = 8.5 (T = 3): `2026-11-24/r2/lab-a/007`. K 12.302 against table 12.528 (-1.8%).
- r = 9 (T = 3): `2026-11-23/r3/lab-a/013-016`. Mean K 11.624 (spread 1.8%).

### Judged error of this model against the evidence runs

RMSE/L between `predict()` and the measured positions over all 25 cited runs: 0.0049 to 0.0051. The noise floor (tracker 0.05
per coordinate) is about 0.005, so these runs sit at the floor. Bar for falsification: 0.021.

## Fall check (not cited)

A radial fall from r0 = 9 (`2026-11-24/r3/lab-a/001-002`, T = 10) pulls the pair to contact near t = 9.5. Over the pre-contact part
(t <= 6, separation down to about 7) the table, with no free parameter, has chi2/dof 1.00 to 1.07 in each replicate. The fall
runs are not cited: they run past the duration window and into contact, which the table does not describe. A free power law
(K/r^P, P about 3.2) also fits the fall at chi2/dof about 1.02; the fall alone does not separate them. This paper makes no
exponent claim.

## What this does not show

- No claim for initial separations in [3, 5). The P-0027 nodes 3 and 4 are withdrawn and K there is about 2 to 3% higher than
  the table. The fall suggests a steeper law below about 3 (the table is clamped there) but this is not measured.
- No claim beyond the windows. Pairs starting at 5 to 9 approach contact only after the window closes.
- No claim for r > 9, other species, other exponents or shapes, or three or more particles. The crowd claim P-0028 uses the
  P-0027 table at separations 3 to 5 and is affected by the same [3, 5) problem; it is not revised here.
- Functional form is not claimed. K(r) is an effective K at exponent 2.5 on [5, 9].

## Scope and what would falsify it

Falsified if a cited in-domain run (within its window) has judged error above 3 x 0.007 = 0.021, or if a fit of K at a separation in
[5, 9] differs from the table by more than 4% with replicate spread below 3%.

## Model

`model.py` implements the table with linear interpolation, RK4 (step 0.002), and specular walls at 0 and 10. It imports only numpy and
math. It raises ValueError outside the initial separation [5, 9] (with a 1e-3 tolerance at the edge) and outside the duration window.
