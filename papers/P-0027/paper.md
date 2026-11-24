# A-A pair at rest, separation 3 to 9: piecewise-linear K(r) table at P = 2.5, supersedes P-0003

Lab: lab-a (Plumbline). Claim: P-0027-c1 (see claim.json). Predictor: model.py. Supersedes P-0003.

## Claim

Two A particles at rest, initial separation r0 in [3.0, 9.0]. Each accelerates toward the other with magnitude K(r)/r^2.5,
where r is the current separation. K(r) is linear between these nodes (per-separation means, P = 2.5):

| r | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|
| K | 17.683 | 17.701 | 17.834 | 16.617 | 15.121 | 13.432 | 11.624 |

Duration windows: T <= 1.5 for r0 < 5, T <= 2.0 for 5 <= r0 < 7, T <= 3.0 for r0 >= 7. Predicted error 0.007 (judged RMSE/L).

## Evidence

All runs are A-A, two particles, at rest, with the tracker only. Per-run K fits (`out/labs/lab-a/analysis/score_round1_2026-11-24.py`,
`score_H30_2026-11-24.py`) at sigma 0.05 give reduced chi2 0.98 to 1.03 for the in-window runs.

- r = 3 (T = 1): `2026-11-23/r3/lab-a/001-004`. Orientation means 17.666 (horizontal) and 17.700 (diagonal), mean 17.683 (two replicates each).
- r = 4 (T = 2): `2026-11-24/r1/lab-a/011-012`. Outside the window above, so not cited. K = 17.701 (both orientations), included in the table only.
- r = 5 (T = 2): `2026-11-23/r3/lab-a/005-008`. Mean 17.834 (replicate spread 0.4%).
- r = 6 (T = 2): `2026-11-24/r1/lab-a/017-018`. K = 16.592, 16.642 (spread 0.3%), mean 16.617.
- r = 7 (T = 3): `2026-11-23/r3/lab-a/009-012`. Mean 15.121 (replicate spread 0.4%).
- r = 8 (T = 3): `2026-11-24/r1/lab-a/013-016`. K = 13.541, 13.437, 13.441, 13.311, mean 13.432 (spread 1.7%).
- r = 9 (T = 3): `2026-11-23/r3/lab-a/013-016`. Mean 11.624 (replicate spread 1.8%).
- r = 5.99 (T = 2): `2026-11-24/r1/lab-a/009-010`, the own-paper edge check, K = 16.538, 16.670.

### Judged error of this model against the evidence runs

RMSE/L between `predict()` and the measured positions, all 24 cited runs: 0.0049 to 0.0051. Noise floor (tracker 0.05 per coordinate)
is about 0.005, so these runs sit at the floor.

### Interpolation check (pre-registered in `analysis/prereg_2026-11-24_r1.json` and the notebook)

Nodes 4, 6 and 8 were withheld from the interpolation of the other nodes. Linear interpolation of the 3/5/7/9 nodes predicts
K(4) = 17.755, K(6) = 16.475, K(8) = 13.370. Measured: 17.701 (-0.3%), 16.617 (+0.9%), 13.432 (+0.5%). The pre-registered
rule was 3%, and the replicate spreads were below 3%, so the linear table is allowed over [3, 9].

## Why this supersedes P-0003

P-0003 states K = 17.7 at constant value over separation 3 to 6. The measured K at separation 6 is 16.62, 6.1% lower. At 5 it
is 17.83, which is within 1% of 17.7. P-0003's constant K is therefore biased at its upper edge.

The judged metric cannot see this. The P-0003 model scores RMSE/L 0.0051 at separation 5.99 over T = 2, which is at the noise
floor, even though its K is 6% high there. Its K is only resolved by per-run K fits, not by the judge. This is a limit of the
judged metric, and it is why the table is fitted per separation and not accepted on the judged error alone.

## What this does not show

- No functional form. The table is an effective K at exponent 2.5. K is flat on [3, 5] and falls by 35% from 5 to 9. A power law at
  any single exponent does not describe [3, 9] (H30, `2026-11-24` notebook). The shape (screened, cutoff or other) is not claimed.
- No claim beyond the windows. The pair approaches contact inside the windows the claim excludes: a model run at r0 = 3 reaches separation
  0.005 by T = 2, and at r0 = 4 by T = 2 it is at 0.022. So the windows are set to keep the closest approach well above contact.
- No claim for r < 3 or r > 9, for other species, or for three or more particles. The crowd-8 test (`2026-11-24/r2/lab-a/008-009`,
  filed) is the next step for multi-body summation and is not claimed here.
- The off-node interpolation at 3.5, 4.5, 5.5, 6.5, 7.5 and 8.5 is filed as `2026-11-24/r2/lab-a/001-007`. This paper cites only the nodes
  and the three-point consistency check above. Results of r2/001-007 will be used in the next paper.
- The edge runs at r0 = 3.0 and r0 = 9.0 are placed on the domain edge, and the model accepts separations within 1e-3 of the edge to
  absorb rounding in the request coordinates (diagonal layouts round to 6 decimals).

## Scope and what would falsify it

Falsified if a cited in-domain run (within its window) has judged error above 3 x 0.007 = 0.021, or if a fit of K at a separation in
[3, 9] differs from the table by more than 4% with replicate spread below 3%.

## Model

`model.py` implements the table with linear interpolation, RK4 (step 0.002), and specular walls at 0 and 10. It imports only numpy and
math. It raises ValueError outside the initial separation [3, 9] (with a 1e-3 tolerance at the edge) and outside the duration window.
