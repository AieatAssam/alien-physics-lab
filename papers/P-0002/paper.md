# Free flight of a lone species-C particle over 40 time units with specular wall reflection

Lab: lab-b. Paper: P-0002. Evidence: 2026-11-17/r2/lab-b/005. Extends P-0001 (species A, duration 10, speed about 1.1) to species C, speed 3.6 and duration 40.

## Claim

A single species-C particle, with no other particle in the chamber, moves in a straight line at constant velocity between wall collisions and reflects specularly at each wall. The reflected-line law is the same as for P-0001. Within the tested run, I see no drag and no drift.

## Evidence

Request 005: one C particle at (1.0, 1.0), velocity (3.0, 2.0), duration 40.0, sample_dt 0.1, 401 tracker samples, 0 census events.

- A grid search over velocity gives (3.0000, 2.0000), exactly the nominal velocity.
- Residuals at the nominal velocity: x mean -0.000, sd 0.052; y mean +0.003, sd 0.050; max |residual| 0.175.
- Mean residual in each of four 10-unit segments is within 0.005 of zero in both coordinates. No drift is visible.
- Against the noisy truth, the model has RMSE 0.051 absolute per coordinate (0.0051 normalized, chamber side 10). That equals the tracker noise sd, so the model is within noise. predicted_error 0.01 (normalized) is set at about twice the observed RMSE.

## What this does not establish

- One trajectory, one speed (3.6), one run length (40). Speed and duration dependence beyond this run are not tested.
- No pair data. Round 2 shows a pair of C with an A (r2/006) repels, so this claim holds only for a lone particle.
- Gaussianity of the noise is not tested.

## Falsification

A lone species-C particle whose tracker positions depart from the reflected-line model by more than 3 times predicted_error (RMSE above 0.03 normalized, 0.3 absolute) at any setup inside the stated domain would falsify this claim. A drift of the mean residual beyond 0.05 over a run of 40 would also count against it.
