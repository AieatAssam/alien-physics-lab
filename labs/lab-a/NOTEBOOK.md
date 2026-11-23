# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

Judge notes that govern my claims:
- The domain check covers species, particle count and initial pair separations only. Duration is not in the domain, so a run at a different T can count as in-domain. I still cite runs at the claim's stated T, to keep reviews clean.
- Boundary runs: a run placed exactly on a domain edge can fail the paper's own check by float rounding (seen 2026-11-23 with `1.95` read as `1.94999...`). Place edge runs 0.01 inside the edge. Verify with the paper's `predict()` before filing.
- Noise floor of the judged metric: tracker noise is about 0.05 per coordinate, so a correct model scores RMSE/L about 0.005. A replicate bar of 3 x predicted_error is only informative when predicted_error is above about 0.0025. Most replicate verdicts sit at this floor, so they test the stated error bound, not the constants.
- Review evidence is judged on my own request ids only. Review-account runs (`account: review`, `cites_paper`) are the convention for runs that test a paper.
- Cost is `1 + 0.02 * N * T`. The flat "1" dominates for short runs, so many short, dense runs are cheap per information.

## Budget ledger

### Closed days
- 2026-11-17: research used 23.30 of 40; review 6.00.
- 2026-11-18: research used 30.38 of 40; review 6.20 (review of P-0002).
- 2026-11-19: research used 13.12 of 40; grant award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Voted lab-keystone.
- 2026-11-20: research used 9.19 of 40; review 13.90 of 15 (P-0008; P-0010 and P-0011); grant 1.02 of 120. Voted lab-keystone.
- 2026-11-21: research used 31.37 of 40; review 12.42 of 15; grant 1.09 of 120 (9-A main event). Voted lab-vernier.
- 2026-11-22: research used 32.32 of 40; review 6.75 of 15. Grant allowance 0.

### 2026-11-23 (today)
- Round 1 research: 20.34 of 40 (`r1/009-024`, plus `r1/001-008` on review account).
- Round 1 review: 9.72 of 15 (`r1/001-008`, P-0022 and P-0023).
- Round 2 review: 4.10 (`r2/001-004`, P-0024 exponent test, review account). Review total 13.82 of 15. Review allowance is now effectively unusable: no paper is awaiting my review.
- Grant: my mixed-species proposal lost. Keystone won tonight's grant (120). No grant spend.
- Round 3 research: 17.44 estimated of the 19.66 remaining (`r3/001-016`, H30). Total research today: 37.78 of 40 if the estimate holds.

## Established (accepted-level claims, or runs I trust)

Convention: K_XY = acceleration coefficient of species X toward species Y, P = 2.5 unless stated.

| pair | K values | runs | status |
|---|---|---|---|
| A-A | 17.7 to 18.0 | P-0003 (domain sep 3 to 6) | established at sep 3 to 6 only; see H30 |
| A-B | see Close range | | close-AB held |
| A-C | -5.75 (K_AC), -13.6 (K_CA) at r0 1.0, horizontal | `2026-11-22/r3/lab-a/009-012` | pilot clean; orientation control scored, not passed |
| B-B | 6.12 | 4 values, spread about 9% | |
| C-C | 12.36 | 4 values, spread about 5% | |
| B-C | -6.10 and -10.59 | pre-registered prediction passed | |

Other established results:
- Free flight with specular walls (P-0001, P-0002): A, B, C at speeds up to 8.6, T up to 100. Supported.
- Isotropy at separation 4 (A-A along diagonal, y, horizontal): K = 17.67, 17.71, 17.70. Supported at sep 4.
- Pairwise additivity for 3 and 4 particles at separations 3 to 5 (T <= 1): at noise level.
- Shared distance law at separations 7 and 9 for C-based pairs (P-0006): within about 5%.
- P-0021 constant K over T = 6 (A-B at sep 7 falling to about 3.8): supported (`2026-11-22/r2/lab-a/013-015`). Global K scale 1.000, uncertainty about 2%.
- No census event (decay or appearance) in about 70 runs, including 16 particles at T = 100.
- Cost law cost = 1 + 0.02 N T: supported at N = 1, 2, 3, 4, 9, 16.
- Noise: tracker noise per coordinate about 0.05. A joint fit to four A-A runs gives reduced chi2 1.01 at sigma 0.05 (`analysis/kp_fit_2026-11-23.py`), so the stated noise is consistent with the data.

## Round 2 result: P-0024 exponent test (2026-11-23, `r2/001-004`): NULL

Runs: A-A at rest, separation 2.9 (centre (5,5)), T = 0.6, dt 0.001, tracker. Horizontal (001, 004 at (4,4) site repeat), vertical (002), diagonal (003). All `ok`, 601 samples each.

Joint K-P fit (`out/labs/lab-a/analysis/kp_fit_2026-11-23.py`, RK4 with h = 1e-3, sigma 0.05, K refitted at each P on a 0.02-step grid over P in [0.8, 2.8]):
- Reduced chi2 at best fit 1.01, so the noise model is adequate.
- chi2(P) is almost flat. The whole range P = 0.8 to 2.8 changes chi2 by about 5 units, and the minimum sits at the grid edge (P = 0.8).
- P = 2.10 (K = 11.77): chi2 9754.42. P = 2.50 (K = 17.86): chi2 9755.89. Delta chi2 = 1.47, about 1.2 sigma.
- The pre-registered rule (P = 2.10 separated from best-fit P = 2.5 at 3 sigma, Delta chi2 >= 9) is **not met**. The exponent is **untested** by these runs.

Honesty notes:
- The decision rule was written after the round-2 results were already on disk. It is the rule I had set in the plan, but it was not pre-registered in the strict sense. The outcome is far from the threshold, so the ordering question does not change the verdict.
- My design note (`analysis/exponent_design_2026-11-23.py`) predicted about 4 sigma. That estimate was wrong by roughly a factor of 3 in sigma. The reason: over T = 0.6 the separation only falls from 2.9 to about 2.3. That narrow range of r is absorbed by K, so P and K are strongly degenerate. A short run cannot constrain P. Lesson: test the exponent with a long, wide-range trajectory or with local accelerations at several separations, not one short run.
- P-0024's existing review stands as written: replicated within its stated bar, with the exponent explicitly not tested by the judged metric. No new claim from me on the exponent.

## Round 1 results (2026-11-23), scored today

All requests returned `ok`. Scoring used the paper's own `predict()` for the reviews, and the pre-registration in `analysis/prereg_2026-11-23.json` (written before results) for the controls.

### Reviews on today's runs
- **P-0022** (lab-b, A-B sep 2, T <= 0.8): four in-domain runs (`r1/001-004`). RMSE/L 0.00492 to 0.00521 against bar 0.024. Replicated on the judged metric. Errors sit at the noise floor, so this does not test K_A(B) or K_B(A) finer than a few percent. Contact region (sep below 1.9) not probed.
- **P-0023** (lab-vernier, A-B sep 9, T <= 10): four in-domain runs (`r1/005-008`). RMSE/L 0.00519 to 0.00529 against bar 0.018. Replicated on the judged metric. The paper's own 5% drift over T = 10 is not visible at the noise floor.

### Pre-registered controls
- **Close-AC orientation (`r1/009-014`, diagonal, vs horizontal `2026-11-22/r3/lab-a/009-012`)**: diagonal K_AC mean -5.70, K_CA mean -13.68; horizontal K_AC -5.75, K_CA -13.60. Gaps -0.9% and +0.6%. **Clause (no run more than 10% from pooled mean) FAILS**: run 014 (K_AC -5.1) is 10.5% from the mean. Close-AC stays held.
- **Close-CC vertical (`r1/015-018`)**: K_CC 9.52 vs horizontal reference 9.50 (stored) or 9.67 (my re-fit). Passes against the stored value. Reference is method-dependent at about 2%.
- **A-A at separation 7 and 9 (`r1/021-024`, T = 4, constant-K fit)**: sep 7 K = 15.4 (ratio 0.87 to 17.7); sep 9 K = 11.8 (ratio 0.66). Within each separation the two runs agree to about 1%. Clause FAILS against 17.7. P-0003's domain is sep 3 to 6, so this does not contradict P-0003. Leads to H30.
- **Nine A, T = 10 (`r1/019-020`)**: not evaluable. My uniform-K integrator blows up at close approach (min sep 0.004 and 0.011; the cluster collapses within 2 time units). Recorded as not evaluable, not as a refutation of the law. No crowd-8 claim.

## Distance law (A-A): H30, filed today

Observation: constant-K fits over T = 4 give K = 17.7 at sep 3 to 6 (P-0003) but 15.4 at sep 7 and 11.8 at sep 9. Under a single P = 2.5 law these cannot both hold. Two explanations: (a) the exponent is not 2.5 over 3 to 9; (b) the T = 4 constant-K fit is biased because the separation falls a lot during the run.

Design (`analysis/design_H30_2026-11-23.py`): local accelerations. Two A at rest, short T so the pair moves only a few percent of r0 (so the trajectory is near the initial-acceleration regime and the constant-K bias is small). Dense sampling (1990 samples). Horizontal and diagonal at each separation.

| separation | T | horizontal runs | diagonal runs | predicted local a (K 17.7, P 2.5) | min sep (pred) |
|---|---|---|---|---|---|
| 3 | 1.0 | 001, 002 | 003, 004 | 1.14 | 1.58 |
| 5 | 2.0 | 005, 006 | 007, 008 | 0.317 | 3.56 |
| 7 | 3.0 | 009, 010 | 011, 012 | 0.137 | 5.66 |
| 9 | 3.0 | 013, 014 | 015, 016 | 0.0728 | 8.32 |

Why this should discriminate: at sep 9 the reference predicts a = 0.0728, the 11.8-K alternative predicts a = 0.0486. Relative difference 33%. Expected precision per run on a from the 1990-sample design: about 0.5% at sep 9 (estimated, sd of a = sigma / sqrt(N T^4 / 20) per coordinate, pooled over two particles). Replicated, that is far below the 33% effect. The sep 3 run has the same structure with about 0.4% precision.

Pre-registration: `analysis/prereg_H30_2026-11-23.json`, written before any H30 result exists. Decision rule:
- **Supported** (single P = 2.5, K = 17.7 over sep 3 to 9): every separation's mean K_fit within 4% of 17.7, and both orientations agree within 3%.
- **Refuted** (K depends on separation): any separation mean K_fit off 17.7 by more than 8%, with replicates agreeing within 3%.
- **Inconclusive** otherwise. I will not claim either way.
- Secondary (not decisive): free-P slope P = ln(a3/a9)/ln 3 from local accelerations.

Cost: 17.44 estimated. Min separation is at least 1.58 under the reference model, so no run is near the integrator-failure zone.

Note on the round-2 finding: H30 is not a K-P joint fit. It fits K at a fixed P = 2.5 from short runs, plus a free-P slope as a secondary. The joint-fit design failed for P-0024, so H30 relies on the local-acceleration regime, not on fitting P from one trajectory.

## Close range

### A-B at r0 = 1.0: held (rule failed on one run)
Pre-registration in `analysis/prereg_2026-11-22_r3.json`. Pooled 28 runs: K_AB 5.488 (SE 0.82%, pass), horizontal vs diagonal -1.98% (pass), max deviation 11.44% on `2026-11-22/r1/lab-a/005` (fail). K_BA 7.804 (SE 0.65%, all clauses pass). Close-AB stays held. Run 005 is not excluded post hoc.

### C-C at r0 = 1.0: orientation resolved for vertical
Horizontal mean 9.50, diagonal mean 8.99 (5.4% lower at T 0.15). Vertical 9.52. Diagonal repeat not filed. Scope to "isotropic within about 2% at r0 1.0" only if the diagonal repeat matches.

### A-A at r0 = 1.0
Six-vs-six control at (5,5): horizontal K 11.10, diagonal 10.92. Pooled K = 11.01. P-0012's K = 11.3 sits about 2.5% above the pool (recorded as a known offset). A-A K at r0 0.85 to 2.0 is not constant: about 10.3 (0.85), 10.3 to 11.5 (1.0), 12.4 (1.25), 14.0 (1.5), 15.6 (2.0).

### Close-AC (held): see above.

### Crowd of nine (crowd-8): not published
- T = 0.5 runs: insensitive to K over 12 to 25. Only "no interaction" separates.
- T = 10 runs: not evaluable with the uniform law (collapse within 2 time units).
- A crowd claim needs a validated law below separation 0.5, which I do not have. Held.

## Reviews

### Filed 2026-11-23 (round 2, today)
- **P-0022** (lab-b, A-B sep 2, T <= 0.8): replicated. Evidence `2026-11-23/r1/lab-a/001-004`. Bar 0.024, errors 0.0049-0.0052.
- **P-0023** (lab-vernier, A-B sep 9, T <= 10): replicated. Evidence `2026-11-23/r1/lab-a/005-008`. Bar 0.018, errors 0.0052-0.0053.
- **P-0024** (lab-keystone, A-A sep 1.25 to 3, exponent 2.10): replicated, scoped. Evidence `2026-11-20/r1/lab-a/003`, `2026-11-21/r1/lab-a/005`, `006`, `2026-11-21/r2/lab-a/004` (in domain, sep 1.25 to 1.5, T <= 0.3). Bar 0.018, errors 0.0050-0.0051. The review says explicitly that the exponent is not tested by the judged metric. Round-2 runs (`2026-11-23/r2/lab-a/001-004`) show the exponent is also not tested by a joint fit at T = 0.6, sep 2.9: **the exponent remains untested**.

### Filed 2026-11-22 (round 3)
- P-0021 (lab-vernier, A-B sep 7, T <= 6): replicated. Evidence `2026-11-22/r2/lab-a/013-015`. Error 0.0049-0.0050 against bar 0.021.

### Filed 2026-11-22 (round 2)
- P-0017 (lab-b, B-B, K = 3.98, T <= 0.15): replicated. Evidence `2026-11-22/r1/lab-a/009-011`. Asks lab-b to refit my four B-B runs.
- P-0020 (lab-b, A-B, K_AB = 5.39, K_BA = 7.33, T <= 0.15): replicated. Evidence `2026-11-21/r3/lab-a/012-015`. My fits give K_BA about 6% higher. Flagged, not disputed on the judged metric.

### Filed 2026-11-22 (round 1)
- P-0016 (lab-vernier, A-C): replicated. P-0018 (lab-b, C-C): replicated.

### Standing reviews
- P-0013 (lab-c): replicated. P-0014 (keystone): narrowed (T <= 1 for close approach). P-0015 (vernier): replicated. P-0010 (keystone): narrowed. P-0011 (vernier): replicated. P-0002: 2026-11-18.

## Papers
- **P-0019 (mine, close-BB at r0 1.0, K = 3.86, T <= 0.3, predicted_error 0.008)**: evidence `2026-11-21/r1/lab-a/001, 002` and `r3/003, 004`. Cites P-0017. Gate numbering may renumber it.
- **P-0012 (mine, close-AA at r0 1.0, K = 11.3, horizontal)**: stands; diagonal orientation recorded as a 5% to 8% offset, not a retraction.
- No new paper today. Candidates held: close-AB (rule failed on run 005), close-AC (rule failed on run 014), crowd-8 (no validated close-range law), exponent (untested). Next free paper number: P-0025. H30 can only become a claim after its results are scored under the pre-registered rule.

## Requests

Round 1 (2026-11-23, results in): `out/requests/2026-11-23/r1/lab-a/` (pre-registration `analysis/prereg_2026-11-23.json`).

| id | account | purpose | cost each | result |
|---|---|---|---|---|
| 001-004 | review (P-0022) | domain-edge runs, sep 1.96/2.04, T 0.8 | 1.032 | ok, scored |
| 005-008 | review (P-0023) | domain-edge runs, sep 8.92/9.08, T 10 | 1.400 | ok, scored |
| 009-014 | research | close-AC diagonal orientation control | 1.008 | ok, scored (rule fails clause iii) |
| 015-018 | research | close-CC vertical control | 1.006 | ok, scored (passes) |
| 019-020 | research | nine A, 3x3 spacing 3.5, at rest, T 10 | 2.800 | ok, not evaluable |
| 021-022 | research | A-A at sep 7, T 4 | 1.160 | ok, K 15.4 |
| 023-024 | research | A-A at sep 9, T 4 | 1.160 | ok, K 11.8 |

Round 2 (2026-11-23, results in): `out/requests/2026-11-23/r2/lab-a/`, review account, cites P-0024.

| id | account | purpose | cost each | result |
|---|---|---|---|---|
| 001-004 | review (P-0024) | A-A sep 2.9, T 0.6, dt 0.001 (horizontal, vertical, diagonal, site repeat) | 1.024 | ok. Joint K-P fit: null (Delta chi2 1.5) |

Round 3 (2026-11-23, filed today): `out/requests/2026-11-23/r3/lab-a/001-016`, research account, H30 (validated against `protocol/request.schema.json`).

| id | sep | T | orient | cost each |
|---|---|---|---|---|
| 001-002 | 3 | 1.0 | horizontal | 1.04 |
| 003-004 | 3 | 1.0 | diagonal | 1.04 |
| 005-006 | 5 | 2.0 | horizontal | 1.08 |
| 007-008 | 5 | 2.0 | diagonal | 1.08 |
| 009-010 | 7 | 3.0 | horizontal | 1.12 |
| 011-012 | 7 | 3.0 | diagonal | 1.12 |
| 013-014 | 9 | 3.0 | horizontal | 1.12 |
| 015-016 | 9 | 3.0 | diagonal | 1.12 |

Total 17.44 estimated, of 19.66 research credits left today. Results expected next session. Score them with the pre-registered rule; do not change the rule after the results.

## Analysis code (`out/labs/lab-a/analysis/`, my files)

- `kp_fit_2026-11-23.py`: joint K-P fit by RK4 for A-A pairs at rest, P profile on a grid, chi2 at sigma 0.05. Usage: `python3 -I kp_fit_2026-11-23.py <repo_root> <req_dir_rel> <res_dir_rel> <nnn> ...`. Takes about 40 s on four runs.
- `design_H30_2026-11-23.py`: H30 design. Writes the round-3 requests and `prereg_H30_2026-11-23.json`, checks predicted min separation with the reference model. Run with `-I` and the `out/` dir.
- `score_paper_2026-11-23.py`, `prereg_scoring_2026-11-23.py`, `exponent_design_2026-11-23.py`, `make_2026-11-23_r2_requests.py`: earlier today (in `labs/lab-a/analysis/` in the repo).
- Earlier-round scripts (fit_AB, fit_AC, pooled_AB, crowd9_check, etc.) are in the repo under `labs/lab-a/analysis/`.

Note: the earlier notebook gave `out/labs/lab-a/analysis/` as the home of my analysis files. Only today's new files are there. Older scripts remain under `labs/lab-a/analysis/` in the repo.

## Errors caught

- **r0 from the first measured sample.** Earlier fits took r0 from the noisy first sample, shifting K by 10 to 20%. Fixed: r0 comes from the request setup.
- **Sample minimum read as collision.** Minimum separation over a noisy profile is biased low. Not used as a collision distance.
- **Grid bug in one B-B fit.** K grid started at 4.0, pinning the result at the edge. Refit on 3.0 to 4.5.
- **Edge runs fail the paper's own domain check.** Exact-boundary separations of 1.95 and 8.9 were read as 1.94999... by float rounding. Fixed by moving edge runs 0.01 inside the boundary.
- **Weak crowd test.** T = 0.5 nine-body runs are insensitive to K. Held.
- **Uniform-K integrator divergence.** My nine-body check blows up at close approach for every K tried. Recorded as not evaluable; no claim drawn from it.
- **Pre-registered clause missed by one run.** Close-AC diagonal run 014 is 10.5% from pooled mean. Recorded as a fail; held. Not re-scored with a looser rule.
- **Reference drift.** The horizontal close-CC reference (9.50) is 1.8% below my re-fit (9.67). Noted as method-dependent.
- **Exponent sensitivity overestimated (today).** My design note predicted about 4 sigma for the P-0024 exponent test. The joint fit gives about 1.2 sigma. The short run cannot separate P from K; the design assumption (wide r range inside one run) was false. Recorded as null. Future exponent tests need wide-r or multi-separation designs.
- **Exponent decision rule not pre-registered (today).** The rule was set in the plan, but the data existed when I wrote the fit. Disclosed here; the verdict does not depend on the threshold.

## What would change my mind

- **Close-AB**: publish only if a new, pre-registered rule passes on a fresh set. Current rule decided (fail on run 005).
- **Close-AC**: publish only after a new diagonal set with a pre-registered rule that does not rest on one run's deviation.
- **Close-CC**: horizontal-vs-vertical within 5%. Diagonal still open.
- **Crowd-8**: needs a validated pair law below separation 0.5, or a crowd-level test that does not run into contact.
- **H30 (A-A distance law)**: if local accelerations match K = 17.7 at sep 3 to 9 within the rule, the 15.4 and 11.8 values were T = 4 fit bias, and P-0003's law extends to sep 9. If K falls with separation by more than 8% with replicate agreement, the single P = 2.5 law is refuted over 3 to 9. Inconclusive otherwise.
- **P-0024 exponent**: untested. Needs wide-r or multi-separation runs. Not a priority this round.

## Self-criticism

- **Replicate verdicts are at the noise floor.** P-0022, P-0023 and P-0024 are replicated only in the sense that the stated error bound holds. None of them constrains the constants or the exponent.
- **The exponent test was a null after a design I got wrong.** I should have checked the design's sensitivity against the actual trajectory (r range) before filing. I did not, and the note in `exponent_design_2026-11-23.py` overstated it.
- **The P-0024 review cites runs filed on the research account earlier.** The current convention is review-account runs for paper tests. The round-2 runs are on review account, but their result is null; the review stands on the earlier evidence.
- **Close-AB held on run 005.** The judged metric cannot tell whether run 005 is a real low tail or noise. Not excluded post hoc.
- **B-B K still disagrees with P-0017 at about 4 sigma**; asked lab-b to refit. I have not checked whether the gap is a fit-method difference.
- **K_BA for P-0020 is about 6% above my own fits.** Flagged; not resolved.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2 to 8.6. B at high speed not tested.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 9, 16.
- H4 no decay: no event in about 70 runs.
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported at separations 3 to 9 as a shared-scale law (C-based, P-0006). A-A at 7 and 9 gives K 15.4 and 11.8 under constant-K fits (see H30).
- H8 pair force identical for all species pairs: refuted at sep 5.
- H9 coupling factorises as g_ij = q_i q_j: partially supported. Not claimed.
- H10 isotropy: supported at sep 4; A-A at (5,5) (-0.9 SE); B-B (1.4%); C-C horizontal vs vertical within 5%. A-B horizontal-diagonal -1.98% pooled, not significant at 28 runs. C-C horizontal-diagonal 5.4% open.
- H11 shared distance law: supported within about 5% at sep 7 and 9 for C-based pairs (P-0006). A-A at 7 and 9: refuted at 5% against 17.7 under constant-K T = 4 fits. Pending H30.
- H12 pairwise additivity for 3 and 4 particles at separations 3 to 5: supported at T <= 1. N = 9 same species at T = 0.5: at noise. N = 9 at T = 10: not evaluable. N = 9 mixed species: proposal lost tonight; not run.
- H13 no census events in crowded long runs: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: refuted for A-A at r0 0.85 to 2.0.
- H15 A-A constant-K at r0 = 1.0: refuted (K about 10.5 to 11.5, not 18).
- H16 B-B and C-C ratio to A-A constant at close range: B-B/A-A at r0 1.0 = 0.34 (supported). C-C/A-A = 0.84 (horizontal).
- H17 A-A K at r0 1.0 orientation-independent at (5,5): supported.
- H18 P-0014's T = 2 predictions: fail at T = 2 for A-A at r0 2.5 (error 4.10) and C-C at r0 3.5 (0.066). Pass for A-C at r0 2.5 (0.0071). T <= 1 holds for pairs measured.
- H19 P-0013's S_AA = 0.753 supported by the judged metric. S_AC and S_CC not separated from 1.
- H20 close-range A-B: K_BA passes the pooled rule; K_AB fails clause (iii) on run 005. **Open.**
- H21 B-B at r0 1.0: K = 3.86 (lab-a), 3.98 (lab-b, P-0017). About 4 sigma apart; open pending lab-b refit.
- H22 C-C diagonal orientation: 5.4% below horizontal at (5,5). Open. Vertical matches horizontal within 5%.
- H23 A-B diagonal orientation at (5,5): round-1 deficit did not repeat. Resolved as fluctuation.
- H24 P-0020 K_BA: my fit about 7.8 vs paper 7.33 (6%). Open.
- H25 P-0021 constant-K over T = 6 (separation 7 to about 3.8): supported.
- H26 close-range A-B K_BA: pooled 7.80 (28 runs), passes all clauses. Open as a claim only if K_AB is resolved.
- H27 A-C close range (r0 1.0): K_AC -5.75, K_CA -13.6. Diagonal control fails clause (iii) at run 014. Held.
- H28 N = 9 same species, long time (T = 10): not evaluable. Cluster collapses within 2 time units.
- H29 A-A K at separation 7 and 9 vs 17.7: refuted at 5% under constant-K T = 4 fits. Open as H30.
- H30 A-A is a single P = 2.5 power law with K = 17.7 over sep 3 to 9. **Open. Filed round 3 (`r3/001-016`), pre-registered, results next session.**
- H31 P-0024 exponent 2.10 over 1.25 to 3 vs P = 2.5: **untested.** Joint fit of `r2/001-004` gives Delta chi2 1.5 (about 1.2 sigma), below the 9 needed; the profile is flat in P over 0.8 to 2.8. Not claimable either way.

## Plan for the next round
1. Score `2026-11-23/r3/lab-a/001-016` (H30) when results arrive. Use `analysis/prereg_H30_2026-11-23.json`. Fit K at P = 2.5 for each run (local, first-part trajectory) and report per-separation means and orientation agreement, then apply the pre-registered rule. Also report the secondary free-P slope.
2. If H30 is supported, a claim on the A-A law over sep 3 to 9 (predicted_error to be set from the replicate scatter, probably about 0.0025 or below) would be a sharpen-A-2 candidate. Check its domain against the claim schema first.
3. If H30 is refuted, the next step is a separation scan at sep 4, 6, 8 with the same short-T design, then a claim scoped to the separations where K is constant.
4. Exponent (H31): not a priority. If revisited, use a single run long enough that r sweeps a wide range (T about 4 at sep 3, or several separations), with a pre-registered joint fit.
5. Do not file a crowd claim. Do not re-file close-AB or close-AC runs under the same rules.
6. Notes for lab-b: K_BA disagreement on P-0020; K_BB disagreement on P-0017. P-0022 review: no contact-region probe yet.
7. Notes for lab-vernier: P-0023's drift claim is not tested by the judged metric.
8. Notes for lab-keystone: the round-2 exponent runs are null (see above). P-0024's exponent remains untested. Their closing grant should be spent on a wide-r exponent test if they want one.
9. Vote filed earlier for lab-keystone. Keystone won the grant; their 120 credits are theirs to spend.
