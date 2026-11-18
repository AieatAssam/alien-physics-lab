# Attraction between two species-A particles at rest: per-particle acceleration about 17.7 r^-2.5 for separations 3 to 6

Lab: lab-a. Paper: P-0003. Evidence: 2026-11-17/r3/lab-a/001-008 (eight tracker runs, four separations, each repeated). Model: `model.py`.

## Claim

Two species-A particles that start at rest, with no other particles, accelerate toward each other with magnitude K / r^P per particle, where r is the separation in chamber units and K = 17.7, P = 2.5. The claim covers initial separations 3.0 to 6.0, durations 1 to 2 time units, and no wall contact. Within that domain the tracker data fit this model at noise level.

Domain: species A only, two particles, initial velocities zero.

## Evidence

Eight runs. Separations 3, 4, 5, 6 along x at y = 5, each repeated (001-002 at 3 with T=1; 003-004 at 4, 005-006 at 5, 007-008 at 6, all with T=2).

Fit of the central-force model (both particles, both coordinates, tracker noise assumed 0.05 per coordinate), integrating the two-body equations from the requested initial conditions:

| Exponent P | Best K | rms residual (per coordinate) |
|---|---|---|
| 2.00 | 9.39 | 0.062 |
| 2.25 | 13.05 | 0.054 |
| **2.50** | **17.74** | **0.051** |
| 2.75 | 23.87 | 0.055 |
| 3.00 | 32.15 | 0.064 |
| 4.00 | 102.1 | 0.121 |

Per-run check at P = 2.5, K = 17.74 (rms per coordinate): 001 0.054, 002 0.048, 003 0.050, 004 0.055, 005 0.052, 006 0.049, 007 0.052, 008 0.051. Per-run best K: 17.2, 17.7, 17.7, 17.8, 18.2, 17.9, 16.3, 16.8 (separations 3, 3, 4, 4, 5, 5, 6, 6). The repeats agree at each separation within the noise.

Predictor check (`model.py` run against all 8 runs): residual rms 0.047 to 0.059 per coordinate, mean residual below 0.005 in every run. The constants were fit to these same runs, so this is a consistency check, not a prediction test. The prediction tests are the round-1 requests `2026-11-18/r1/lab-a/001-013`.

The noise estimate (0.05 per coordinate) is taken from the lone-particle runs (see notebook) and agrees with the residual rms here.

## What the fit does and does not show

- **Power law vs. screened form.** A screened inverse square, K exp(-r/lambda) / r^2, fits as well: lambda = 8 gives SSE 7.26 against 7.49 for the power law (lambda = 5, 12, 20 give 8.15, 7.73, 8.65). With this data the exponent and the screening length cannot be separated. The power law is used as an effective description on separations 3 to 6, not as a physical law. Far-field runs at separation 8 and 9 (queued, lab-a round 1) are designed to discriminate: the two forms differ by about 15% there.
- **Closest approach.** Runs 003-004 bring the pair to separation about 0.14 at t = 2 (tracker). The fit still holds to that point, but the claim makes no statement below 0.14. Predicted separations below about 0.5 are not checked against data.
- **Velocity dependence.** Not tested here. Every run starts from rest. The moving-pair run 2026-11-17/r2/lab-a/004-005 (one moving particle) is not a clean test of this claim, and I do not use it as evidence.
- **Species.** Only species A. A-B, B-B, C-C and A-C pairs are requested in round 1 (2026-11-18/r1/lab-a/001-005).
- **Number of particles.** Two particles only. Three or more particles, and any wall-contact or multi-body effect, are not tested. The predictor sums pairwise forces for N > 2, but this is untested.
- **Time.** Durations 1 to 2. Longer runs at these separations are not tested.

## Falsification

Any two-particle species-A run at rest with separation 3 to 6 and duration at most 2 that departs from the predictor by more than 0.03 in normalized units (0.3 chamber units) per coordinate counts against the claim. A run whose best-fit K at P = 2.5 falls outside 15 to 20 would also count against the stated constants, even if the rms stays below that threshold.

## Relation to earlier work

Round 2 (2026-11-17/r2/lab-a/004-006) first showed attraction between two species-A particles (one moving, one stationary). Its force law was not fit and it is not used as evidence here. The round-3 at-rest series is the first attempt at a force law. The round-2 encounter, which reached separation about 0.8, lies outside this claim's domain; I have not checked the model against it.

## Code

`out/labs/lab-a/analysis/pair_rest_r3.py` (per-run quadratic fits, accelerations), `pair_central_fit_r3.py` (two-body integration), `pair_central_refine_r3.py` (golden-section K per P), `pair_form_compare_r3.py` (power law vs screened form). `model.py` is the predictor; it imports only math.
