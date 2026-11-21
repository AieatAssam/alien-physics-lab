# Two-body pair law at separation 1.5, at rest (species A and C)

Lab: lab-c (Nullius). Status: a narrow claim. It covers one separation and short times only.

## Claim
Two particles at rest, species A/A, A/C or C/C, separated by 1.45 to 1.55, both at least 2 from every wall, observed for T <= 0.4. The pair acceleration is `S_XY * COUP[(X,Y)] / r^2.5`, using the P-0008 coefficient table, with per-pair scales

| pair | S (round-2 fit) | round-3 replicate | replicate scale |
|---|---|---|---|
| A-A | 0.753 | 2026-11-20/r3/lab-c/006 | 0.749 |
| A-C | 0.811 | 2026-11-20/r3/lab-c/008 | 0.806 |
| C-C | 0.874 | 2026-11-20/r3/lab-c/014 | 0.869 |

Predicted judged error 0.01. This is about 1.4 times the tracker noise floor of 0.0071 (sqrt 2 x 0.05 / 10).

## Method
- Runs: 2026-11-20/r2/lab-c/004, 005, 006 (AA, AC, CC at 1.5, T = 0.4, dt = 0.0002), and their round-3 replicates 2026-11-20/r3/lab-c/006, 008, 014.
- Scales were fitted on the round-2 runs only, by a chi-square fit of the measured separation (sigma 0.071 per sample) over the samples before the prediction's own separation drops below 0.6. The time-block jackknife SE is about 0.01. The round-3 replicates were predicted with the round-2 scales and agree within 0.005.
- Judged error (RMSE of positions over matched (t, id) pairs, divided by the side 10) for the model in `model.py`:

| run | pair | judged error | unscaled P-0008 |
|---|---|---|---|
| r2/004 | AA | 0.00717 | 0.06836 |
| r2/005 | AC | 0.00705 | 0.00778 |
| r2/006 | CC | 0.00704 | 0.00770 |
| r3/006 | AA | 0.00715 | 0.06834 |
| r3/008 | AC | 0.00706 | 0.00782 |
| r3/014 | CC | 0.00704 | 0.00776 |

## What the judged metric can and cannot show
- **AA:** the unscaled P-0008 law fails by about 10 times the noise floor (0.068). The scale is needed and resolved.
- **AC and CC:** the unscaled law also scores 0.0077 to 0.0078 on these runs, so the judged metric does not discriminate S = 0.81 or 0.87 from 1 at T = 0.4. The scales come from the separation fit, not from the judged score. A reviewer who relies on the judged metric alone will not see a difference for AC and CC.
- The displacements are small at these pair strengths over T = 0.4, so the judged error is dominated by tracker noise. Longer runs at this separation would be needed to resolve S for AC and CC through the judge.

## Limits (enforced in model.py, which raises ValueError outside them)
- Exactly two particles, at rest, species A or C.
- Separation 1.45 to 1.55; both particles at least 2 from every wall.
- Duration up to 0.4.
- Not covered: B species, other separations (the P-0008 power law is not valid at r < 2.95 for other pairs; the scale changes with r, see below), longer times, and collisions.

## Context: the scale depends on separation (not claimed here)
From my round-2 and round-3 fits, the AA scale rises with separation: 0.61 (r0 1.0, T 0.3), 0.75 (1.5), 0.85 (2.0), 0.92 (2.5), 0.96 (3.0), 1.00 (3.5), 1.01 (4.0). For AC and CC at r0 2.5 and 3.0, and BB at 2.5, the scales are 0.98 to 1.05. So the short-range deficit appears to be confined to the AA-dominated range and to r < 2.5 for the other pairs. This is a fitted trend, not a claim. It is not tested as a shape law.

## Relation to prior work
P-0008's coefficients are used unchanged except for S. This paper does not assert that P-0008 is wrong at its own domain, r from 3 to 5. The round-3 runs at r0 = 3.0 and 3.5 give AA scales of 0.96 and 1.00, consistent with 1 within about 0.04.

## Reproduction
`model.py` is self-contained (math only). The fit and judged-error scripts are in the lab's analysis directory: `out/labs/lab-c/analysis/judge_P0012_2026-11-21.py` and `control_unscaled_P0012_2026-11-21.py`, and `score_r3_2026-11-20.py` for the round-3 fits.
