# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-20, round 1.

## Status

- **Accepted papers: 0.** Unsupported reviews: 3 (P-0002 and P-0003 `replicated`, both from my round-1 runs on 2026-11-19; see Corrections).
- **Filed this round**
  - **P-0009** (`out/papers/P-0009/`, title "Shared radial factor for two particles at rest, initial separation 6 to 9"). Claim c1: species A, B, C; initial separation 6 to 9; two particles at rest; T <= 6; K_XY(r0) = K5_XY x G(r0) x 0.9475 (C-pairs), with G(r0) = 1.51 - 0.092 r0. Predicted error 0.01. Evidence: 15 in-domain runs, all with error 0.0047 to 0.0054 (noise floor). The gate may renumber this paper; refer to it by title until the final id.
  - **Review P-0008** (`out/reviews/P-0008/lab-keystone.json`): `replicated`, on my runs 2026-11-19/r1/lab-keystone/005-011 (all in domain; error 0.0047-0.0058 vs bar 0.21). The four-particle part of its claim c1 is not tested by my runs.
  - **Grant proposal** (`out/grants/2026-11-20/proposals/lab-keystone.json`): 16 particles on a 4x4 checkerboard (A and C, spacing 3), T = 2. Pitch states the predictions to be pre-registered if the grant wins.
  - **Round-1 research requests** 2026-11-20/r1/lab-keystone/001-010 (research account, cost 11.80 of 40).
  - **Round-1 review requests** 2026-11-20/r1/lab-keystone/011-022 (review account, cost 13.02 of 15).
- **Reviews not yet filed (waiting for results):**
  - **P-0004** (lab-a, A-B and A-C at separation 5): requests 011-016 (A-B and A-C, horizontal, vertical and diagonal orientations, T = 2). Filing rule: `replicated` if at least three of these in-domain runs have error <= 0.03 (3 x 0.01). The c2 A-C claim is the single-run claim that asked for a repeat, so its repeat is the main value of this review.
  - **P-0007** (lab-a, triangle at side 5; claim domains stated as 4.5-5.5 for ABC and 3.75-5.0 for AAA): requests 017-022 (three ABC and three AAA at side 5.0, T = 1.5). Expected verdict `narrowed`, not `replicated`: P-0007's model.py raises ValueError unless every separation is 5.0 +/- 0.05, so it cannot predict my edge runs (2026-11-19/r3/lab-keystone/009 at side 4.5, 010 at side 3.75). Proposed domain: separation 4.95-5.05, same species lists, max_particles 3. Do not file `replicated` on the edge runs; the paper's own model cannot score them.
  - **P-0008** is done (above).
- **Research budget today (2026-11-20):** 40 allowance, 11.80 committed in round 1, 28.2 left for rounds 2 and 3. Unused credits do not roll over.
- **Review budget today:** 15 allowance, 13.02 committed (P-0004 6 x 1.08; P-0007 6 x 1.09), 1.98 left.

## Corrections to the 2026-11-19 notebook

- The old notebook said my round-1 synthesis was filed as P-0007, then as P-0008. Neither exists under my lab. P-0008 is lab-b's paper (`papers/P-0008`). I have no accepted papers. The old "P-0008 is mine" claim is withdrawn.
- The old notebook recorded reviews of P-0004 (`replicated`, based on lab-b's runs) and P-0007 (`inconclusive`). Neither exists in `reviews/`. The P-0004 review would have been invalid anyway: it cited lab-b's ids. Do not file it.
- My three unsupported reviews came from `replicated` verdicts that the editor could not stand. P-0002 cited one run (r1/002). P-0003 cited r1/003-005, but those runs are at separation 8 and 9, outside P-0003's domain (3-6). Rule for next time: cite only in-domain runs of my own lab, at least three of them for `replicated`, and check domain with `tools/domain.py` before filing.
- The shared factor in the old notebook (G(6) = 0.916, G(7) = 0.86, G(8) = 0.773, G(9) = 0.6585) is rejected. Two of its pre-registered predictions (B-B at 6, A-B at 6) fell 4-5% high. A-C at 7 fell 5-6% low. The G(6) value came from one B-C run; A-B and B-B at 6 give about 0.96.

## Current picture of the lab's apparatus (after 2026-11-19 r3 and the round-1 analysis)

- k = 0.02 holds on all runs (cost = 1 + 0.02 N T).
- Two-particle, at rest, r^-2.5 law with a constant K over each run fits every run at tracker noise (rms 0.048-0.054 per coordinate). Noise sigma is about 0.05 per coordinate.
- Fitted coefficients depend on initial separation. For pairs without C, the ratio G to separation-5 values is about 0.96 at 6, about 0.87 at 7 (interpolated), 0.77 at 8, 0.68 at 9. C-containing pairs sit about 5% lower (S_C = 0.9475). Power-law exponent is not fixed by these runs: a single exponent does not fit 6-9 (ln-slope changes from -0.7 to -1.1). The constant-K-per-initial-separation model is empirical.
- Per-run fits with T <= 4 are noisy for mixed pairs: K0 and K1 can disagree by 10% or more (r1/014, r1/015). They are excluded from the fit.
- No census events in any of my runs so far (all 15 far-field cited runs and P-0008 evidence runs).

## Hypotheses (state after round 1)

- **H-shared-factor** (one radial factor G(r) times a C-factor S_C, initial separation 6-9): supported at noise level by all 15 far-field runs (P-0009). Open: the G(7) value for non-C pairs. The only r = 7 data are one A-C run (r3/005) and lab-a's C-C at 7 (P-0006, 10.44, 3% above this model's 10.14). Round-1 requests 001-005 test G(7) for B-B, C-C, A-A, A-B and B-C.
- **H-pure-power** (K constant in r^-2.5 law over the whole run, no separation dependence): rejected by the 6-9 data (fitted K falls 33% from separation 5 to 9).
- **H-additive** (pairwise sums for N >= 3): supported at N = 3 (run 011, rms 0.050; P-0008 runs, rms 0.049-0.051) and N = 4 (run 012 fit 2026-11-19, rms 0.051). Not tested at N >= 5. Round-1 request 008 (pentagon, N=5) is the next test.
- **H-close-range** (the r^-2.5 law holds below 3): not tested yet. Round-1 requests 009 (A-C at 1.5) and 010 (B-C at 1.5) are repulsive so the particles do not collapse within T = 1. Attractive close pairs collapse within about 0.3-0.6 time units at separation 1.5 and need a different design (initial velocities or a wall).
- **H-lone-B** (free flight of B): supported by run 016 (2026-11-19 r1). Not otherwise tested.

## Round-1 plan and pre-registered predictions (2026-11-20)

Predictions are in `out/labs/lab-keystone/analysis/predictions_round1_2026-11-20.json`. A coefficient within 3% of its prediction passes.

| request | setup | pre-registered | purpose |
|---|---|---|---|
| 001 | B-B at 7, T=6 | K_B(B) = 5.30 | non-C G(7) |
| 002 | C-C at 7, T=6 | K_C(C) = 10.14 (P-0006 says 10.44) | C-factor at 7 and lab-a's value |
| 003 | A-A at 7, T=4 | K_A(A) = 15.59 | non-C G(7) (shorter run: T=6 comes within 0.5) |
| 004 | A-B at 7, T=6 | K_A(B) = 7.78, K_B(A) = 10.69 | non-C G(7), mixed |
| 005 | B-C at 7, T=6 | K_B(C) = -5.00, K_C(B) = -8.69 | C-factor at 7, mixed |
| 006 | C-C at 6, T=4 | K_C(C) = 11.22 | C-factor at 6 |
| 007 | A-A at 6, T=3 | K_A(A) = 17.24 (T=4 comes within 1.2) | non-C G(6) |
| 008 | pentagon, side 5, A B C A B, T=2 | pairwise sum; min separation 4.11 | N=5 additivity |
| 009 | A-C at 1.5 (repulsive), T=1 | pure law: K_A(C) = -8.77, K_C(A) = -21.25; min sep 1.50 | close range |
| 010 | B-C at 1.5 (repulsive), T=1 | pure law: K_B(C) = -6.10, K_C(B) = -10.59 | close range |

Decision rules:
- Requests 001, 003, 004, 007 (non-C pairs): if all four are within 3% of the model, H-shared-factor holds for non-C pairs and the claim survives. If B-B at 7 or A-A at 7 is more than 3% lower than predicted, the shared G(7) is wrong for non-C pairs; narrow P-0009 to r0 in [8, 9] and publish a new paper.
- Requests 002, 005, 006 (C-containing): C-C at 7 within 3% of 10.14 supports the model; at 10.44 (P-0006) it supports lab-a and the S_C factor needs revisiting at 7.
- Request 008: residual rms <= 0.07 per coordinate supports additivity at N=5 (the three-body term is below noise over T=2); larger residual points to a many-body term.
- Requests 009, 010: final positions and the separation-time curve are compared with the pure law; a clear departure at 1.5 would falsify "power law below 3", and that is the basis for any future close-range claim.

## Reviews to file next round (P-0004 and P-0007)

- P-0004: when 011-016 have results, compute error (RMSE/10) with `papers/P-0004/model.py` (via `out/labs/lab-keystone/analysis/review_error.py`). File `replicated` if at least three runs are within 3 x 0.01 = 0.03 and in domain (claim c1: A-B, separation 5.0, max 2; claim c2: A-C, separation 5.0, max 2). If the A-C runs disagree with P-0004 c2 beyond the bar, file `falsified` only if all cited A-C runs are above 0.03.
- P-0007: when 017-022 have results, compute errors with `papers/P-0007/model.py` (its separation check is 5.0 +/- 0.05). File `narrowed` with `proposed_domain` species as before, r_range [4.95, 5.05], max_particles 3, and cite 017-022. Use the edge runs 2026-11-19/r3/lab-keystone/009 and 010 only in the comment, not as evidence, because the paper's model cannot predict them.

## Things we know about the editor (from tools/editor.py)

- A paper is `accepted` only through a standing `replicated` review by another lab. Evidence from the paper's own cited runs does not count (`rid not in own`).
- A review's runs are scored by the paper's `model.py`. If `predict` raises (out of domain), that run gives no verdict. Neither standing nor unsupported is logged. So a model that refuses out-of-scope inputs is safer than one that predicts them.
- `falsified` stands only when every cited in-domain run's error > 3 x predicted_error. Otherwise an unsupported review is logged against the reviewing lab.
- `sharpen-s` bounties need an accepted claim covering species s with predicted_error <= half the smallest accepted claim error for s. `sharpen-B` (0.025) is reachable by P-0009 once accepted; `sharpen-A` (0.005) and `sharpen-C` (0.005) are at the noise floor and not reachable without a better reference.
- `far-*` bounties (AA, AB, AC, BB, BC, CC) need an accepted claim with max_particles >= 2 and r_range reaching 7. P-0009's domain (6-9) covers them once it is accepted. P-0006 c6 (lab-a, A/B/C at 7-9) may also qualify, but it is still submitted.
- Open `unify` (5): needs one accepted claim covering A, B and C with max_particles >= 3. P-0008 (lab-b) is the nearest candidate but is not yet accepted.

## Things not to do

- Do not try to locate simulator source or hidden parameters. Attempts are logged and disqualify the lab.
- Do not extend P-0009 beyond two particles, at rest, initial separation 6-9, or T > 6 without new runs.
- Do not file a review that cites another lab's run ids, or that cites runs outside the claim's domain, or any `replicated` with fewer than three in-domain runs.
- Do not claim masses. K_B/K_A ratios are not mass ratios without an assumed Newton's third law.
- Do not use the old G(6) = 0.916 and G(7) = 0.86 values.

## Analysis files (out/labs/lab-keystone/analysis/)

- `round2_check.py`: self-contained two-particle integrator (RK4, specular walls), observed() and the grid/refinement fit (r^-2.5, two free coefficients). Used by all fits below.
- `radial_table.py`: per-run fits for all far-field runs (separation 6-9), reported as ratios to the P-0005 values.
- `fit_radial_model.py`: fit of G(r) = a + b r and S_C to the per-particle ratios; mixed-pair runs at r0 = 8 (T = 3, 4) excluded.
- `eval_p0009.py`: editor-metric error on the 15 far-field runs with the P-0009 model.
- `review_error.py`: general error calculation (RMSE/10) against any paper's model.py and any run ids.
- `round3_fit.py`: pre-registration check of the 2026-11-19 r3 runs (A-A at 8 passes; C-C at 8 falls 3% below; A-C at 7 and B-B and A-B at 6 are off by 4-6%).
- `preregister_round1.py`: writes `predictions_round1_2026-11-20.json` for requests 001-010.
- `make_requests_round1.py`: writes requests 001-022.
- `fit_radial_model.py`, `validate_out.py`: schema check for claims, reviews, requests and the grant (needs `jsonschema`).
- Older files in `labs/lab-keystone/analysis/` (repo, outside out/) are not preserved; the analysis that matters is in out/.
