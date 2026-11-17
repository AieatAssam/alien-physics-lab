# Free flight of a lone species-A particle with specular wall reflection

Lab: lab-b. Paper: P-0001. Evidence: 2026-11-17/r1/lab-b/001.

## Claim

A single species-A particle, with no other particle in the chamber, moves in a straight line at constant velocity between wall collisions. At each wall it reflects specularly: the normal velocity component flips sign and the tangential component is kept. The chamber is [0, 10] x [0, 10].

## Evidence

Request 001: one A particle at (2.0, 2.0) with nominal velocity (1.0, 0.5), duration 10.0, sample_dt 0.1, 101 tracker samples, 0 census events.

- The best-fit velocity from a grid search is (0.9995, 0.4985). The nominal velocity (1.0, 0.5) is within 0.001 of this.
- The x-coordinate reflects off the wall at x = 10 near t = 8 and returns to 7.996 at t = 10. The unfolded billiard model reproduces this.
- Residuals of the reflected-line model: x mean 0.004, sd 0.053; y mean -0.002, sd 0.052; max |residual| 0.15. Mean residuals in four 25-sample segments are all within about 0.02 of zero, so no drift is visible.
- Against the noisy truth, the nominal model has RMSE 0.075 (normalized by chamber side 10: 0.0075). The predicted_error of 0.01 gives a margin.

## What this does not establish

- Only one trajectory, one species, one speed (about 1.1), one run length (10), and one wall reflection were observed.
- Nothing about corners, multiple walls, long durations, or higher speeds. Round 2 request 005 tests a species-C particle at speed 3.6 over duration 40 to probe those edges.
- Nothing about pairs. The pair probe (request 002) shows strong interaction between an A and a B particle, so this claim applies only when no other particle is in the chamber.
- The noise sd of 0.05 comes from one run. Gaussianity is not tested.

## Falsification

A lone species-A particle whose tracker positions depart from the reflected-line model by more than 3 times the predicted_error (RMSE above 0.03 in chamber units, i.e. 0.3 absolute) at any setup inside the stated domain would falsify this claim.
