# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

Judge notes that govern my claims:
- The domain check covers species, particle count and initial pair separations only. Duration is not in the domain, so a run at a different T can count as in-domain. I still cite runs at the claim's stated T, to keep reviews clean.
- Boundary runs: a run placed exactly on a domain edge can fail the paper's own check by float rounding (seen 2026-11-23 with `1.95` read as `1.94999...`). Place edge runs 0.01 inside the edge. Verify with the paper's `predict()` before filing.
- Noise floor of the judged metric: tracker noise is about 0.05 per coordinate, so a correct model scores RMSE/L about 0.005. A replicate bar of 3 x predicted_error is only informative when predicted_error is above about 0.0025. Most of today's replicate verdicts sit at this floor, so they test the stated error bound, not the constants.
- Review evidence is judged on my own request ids only. Review-account runs (`account: review`, `cites_paper`) are the convention for runs that test a paper.

## Budget ledger

### Closed days
- 2026-11-17: research used 23.30 of 40; review 6.00.
- 2026-11-18: research used 30.38 of 40; review 6.20 (review of P-0002).
- 2026-11-19: research used 13.12 of 40; grant award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Voted lab-keystone.
- 2026-11-20: research used 9.19 of 40; review 13.90 of 15 (P-0008; P-0010 and P-0011); grant 1.02 of 120. Voted lab-keystone.
- 2026-11-21: research used 31.37 of 40 (rounds 1-3); review 12.42 of 15 (P-0013 to P-0016 filings); grant 1.09 of 120 (9-A main event, `2026-11-21/r3/lab-a/001`). Voted lab-vernier.
- 2026-11-22: research used 32.32 of 40; review 6.75 of 15. Grant allowance 0 (tonight's award went to Keystone).

### 2026-11-23 (today)
- Round 1 research: 20.34 of 40 (`r1/009-024`, plus `r1/001-008` on review account). Results all `ok`. Remaining research after round 1: 19.66.
- Round 1 review: 9.72 of 15 (`r1/001-008`, both papers under review).
- Round 2 filed (review account, cites P-0024): `r2/001-004`, 4 x 1.024 = 4.10. Review total after filing: 13.82 of 15. Research unused in round 2 (19.66 remain for round 3).
- Grant: proposal filed in round 1 (`out/grants/2026-11-23/proposals/lab-a.json`). Round 2 vote filed for lab-keystone. No grant spend today.

## Established (accepted-level claims, or runs I trust)

Convention: K_XY = acceleration coefficient of species X toward species Y, P = 2.5 unless stated.

| pair | K values | runs | status |
|---|---|---|---|
| A-A | 17.7 to 18.0 | P-0003 (domain sep 3 to 6) | established at sep 3 to 6 only; see "Distance law" below |
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
- Noise: tracker noise per coordinate about 0.05.

## Round 1 results (2026-11-23), scored today

All requests returned `ok`. Scoring used the paper's own `predict()` for the reviews, and the pre-registration in `analysis/prereg_2026-11-23.json` (written before results) for the controls.

### Reviews on today's runs
- **P-0022** (lab-b, A-B sep 2, T <= 0.8): four in-domain runs (`r1/001-004`, sep 1.96 and 2.04, horizontal, vertical, diagonal). RMSE/L 0.00504, 0.00492, 0.00521, 0.00491 against bar 0.024. Replicated on the judged metric. Errors sit at the noise floor, so this does not test K_A(B) or K_B(A) finer than a few percent. Contact region (sep below 1.9) not probed.
- **P-0023** (lab-vernier, A-B sep 9, T <= 10): four in-domain runs (`r1/005-008`, sep 8.92 and 9.08). RMSE/L 0.00529, 0.00521, 0.00521, 0.00519 against bar 0.018. Replicated on the judged metric. The paper's own 5% drift over T = 10 is not visible at the noise floor, so it is not tested here.

### Pre-registered controls
- **Close-AC orientation (`r1/009-014`, diagonal, vs horizontal `2026-11-22/r3/lab-a/009-012`)**: fit with `out/labs/lab-a/analysis/prereg_scoring_2026-11-23.py`.
  - Diagonal K_AC: -6.1, -5.6, -5.4, -5.9, -6.1, -5.1 (mean -5.70). K_CA: -13.2, -14.2, -13.4, -13.7, -13.9, -13.7 (mean -13.68).
  - Horizontal K_AC mean -5.75; K_CA mean -13.60.
  - Gap K_AC -0.9%, K_CA +0.6%. Both within 5%. SE of pooled mean about 2.7% (within 3%).
  - **Clause (no run more than 10% from pooled mean) FAILS**: run 014 (K_AC -5.1) is 10.5% from -5.70.
  - Result: close-AC stays held. Orientation is consistent at the 1% level on the mean, but one run is an outlier by the rule. I do not drop it after the fact.
- **Close-CC vertical (`r1/015-018`)**: K_CC 9.32, 9.32, 9.78, 9.66, mean 9.52. Pre-registered horizontal reference 9.50 (`2026-11-21/r1/lab-a/003, 004`): gap +0.2%, inside the 5% band. **Passes.** Caveat: my re-fit of the horizontal reference gives 9.67 (9.62, 9.72), 1.8% above the stored 9.50. The reference is method-dependent at about 2%. Vertical sits -1.6% against the re-fit. Close-CC isotropy supported at about 2% precision, not 1%.
- **A-A at separation 7 and 9 (`r1/021-024`, T = 4, constant-K fit)**:
  - Sep 7: K_AA = 15.36, 15.42 (ratio 0.87 to 17.7).
  - Sep 9: K_AA = 11.64, 11.96 (ratio 0.66 to 17.7).
  - Within each separation the two runs agree to about 1%. **Clause FAILS**: neither is within 5% of 17.7. The constant-K reference is refuted for A-A at separations 7 and 9 under a P = 2.5 constant-K fit. Note that P-0003's domain is sep 3 to 6, so this does not contradict P-0003 as published. See "Distance law" below.
- **Nine A, T = 10 (`r1/019-020`)**: the pre-registered test (uniform pairwise-sum law, K = 17.7, P = 2.5) cannot be evaluated cleanly.
  - My uniform-K integrator diverges for K = 12, 17.0, 25 (RMSE/L in the millions). The divergence is at close approach.
  - Measured trajectories: minimum pair separation 0.004 (run 019, at t = 2.7) and 0.011 (run 020, at t = 6.95). Separations at t = 2 were 0.01 and 0.07. The cluster collapses within the first 2 time units.
  - By the pre-registered rule, RMSE/L > 0.024 counts as "refuted", but my integrator produces a numerical blow-up rather than a measurement-based error. I record it as **not evaluable**, not as a refutation of the law.
  - Either way the outcome is the pre-registered one for the crowd claim: **no crowd-8 claim is published**. Our law is unvalidated at separations below about 0.5, and these runs live there.

## Distance law (A-A)
- K_AA constant-K fits: sep 3 to 6 gives 17.7 (P-0003, and our isotropy checks at sep 4). Sep 7 gives 15.4. Sep 9 gives 11.8.
- Under a single power law with P = 2.5, K should not drop by 25% from sep 7 to sep 9. Either the exponent is not 2.5 over 3 to 9, or the constant-K fit over T = 4 is biased by the trajectory's own change in separation.
- Hypothesis H30 (new, open): A-A is not a single P = 2.5 power law over separation 3 to 9. Test: a set of A-A runs at separations 3, 5, 7, 9 at the same T, fitted for K and P jointly. Not filed yet; to be designed before results.
- P-0024 (lab-keystone) reports P = 2.10 for A-A at separation 1.25 to 3. Exponent differs from the 2.5 window at larger separation. Both can hold only if P varies with separation, which is what H30 would test.

## Close range

### A-B at r0 = 1.0: held (rule failed on one run)
Pre-registration in `analysis/prereg_2026-11-22_r3.json`, written before round-3 results. Rule clauses: (i) SE of the mean <= 3%; (ii) horizontal vs diagonal within 5%; (iii) no run more than 10% from the pooled mean.

Round-3 scoring (all 28 runs: r1 001-008 at (5,5), r2 001-012 at (3,3), r3 001-008 at (5,5)):

| set | horizontal K_AB | diagonal K_AB | horizontal K_BA | diagonal K_BA |
|---|---|---|---|---|
| r1 (5,5) | 5.585 (n 4) | 5.220 (n 4) | 7.900 | 7.660 |
| r3 (5,5) replicate | 5.540 (n 4) | 5.520 (n 4) | 7.745 | 8.020 |
| r2 (3,3) | 5.517 (n 6) | 5.517 (n 6) | 7.880 | 7.653 |

Pooled 28 runs:
- **K_AB**: mean 5.488, sd 0.239, SE 0.82%. (i) pass. Horizontal vs diagonal gap -1.98%. (ii) pass. Max deviation 11.44% (`2026-11-22/r1/lab-a/005`, K_AB 4.86). **(iii) FAIL.**
- **K_BA**: mean 7.804, sd 0.268, SE 0.65%. (i) pass. Gap -1.11%. (ii) pass. Max deviation 7.39% (`r3/008`). (iii) pass.

Close-AB stays held. Run 005 is not excluded post hoc, and no runs are added to dilute it. K_BA alone passes every clause; a pair claim needs both K values.

### C-C at r0 = 1.0: orientation resolved for vertical
Horizontal mean 9.50, diagonal mean 8.99 (5.4% lower at T 0.15). Vertical 9.52 (today). Diagonal-vs-horizontal gap is still the open number. Horizontal-vs-vertical gap is inside 5%. A diagonal repeat is not filed.

### A-A at r0 = 1.0
Six-vs-six control at (5,5): horizontal K 11.10, diagonal 10.92, difference -0.9 SE. Pooled 12-run K = 11.01. P-0012's K = 11.3 sits about 2.5% above the pool (recorded as a known offset). A-A K at r0 0.85 to 2.0 is not constant: about 10.3 (0.85), 10.3 to 11.5 (1.0), 12.4 (1.25), 14.0 (1.5), 15.6 (2.0).

### Close-AC (held)
Horizontal pilot (`2026-11-22/r3/lab-a/009-012`): K_AC -5.75, K_CA -13.6, RMSE/L about 0.005. Diagonal control (`r1/009-014`): K_AC -5.70, K_CA -13.68, but one run at 10.5% from mean fails the pre-registered clause (iii). Held. A future claim needs a repeat with a pre-registered rule that does not depend on the single outlier.

### Crowd of nine (crowd-8): not published
- Earlier T = 0.5 runs (`2026-11-21/r3/lab-a/001, 002`): insensitive to K over 12 to 25. Only "no interaction" separates (0.008).
- T = 10 runs (`r1/019-020`): not evaluable with the uniform law (see above). The cluster collapses within 2 time units.
- Open: a crowd claim needs a validated law below separation 0.5, which I do not have. Held.
- Earlier notebook figure 0.0071 for the 9-A layout from the P-0003 model file does not match my uniform-K re-check (0.0050). Not reconciled. Not cited as a crowd result.

## Reviews

### Filed 2026-11-23 (round 2, today)
- **P-0022** (lab-b, A-B sep 2, T <= 0.8): replicated. Evidence `2026-11-23/r1/lab-a/001-004`. Bar 0.024, errors 0.0049-0.0052.
- **P-0023** (lab-vernier, A-B sep 9, T <= 10): replicated. Evidence `2026-11-23/r1/lab-a/005-008`. Bar 0.018, errors 0.0052-0.0053.
- **P-0024** (lab-keystone, A-A sep 1.25 to 3, exponent 2.10): replicated, scoped. Evidence `2026-11-20/r1/lab-a/003`, `2026-11-21/r1/lab-a/005`, `006`, `2026-11-21/r2/lab-a/004` (all in domain, at sep 1.25 to 1.5, T <= 0.3). Bar 0.018, errors 0.0050-0.0051. The review says explicitly that the exponent is not tested by the judged metric, and the sep 2.5 to 3 window is untested by my runs.

### Filed 2026-11-22 (round 3)
- P-0021 (lab-vernier, A-B sep 7, T <= 6): replicated. Evidence `2026-11-22/r2/lab-a/013-015`. Error 0.0049-0.0050 against bar 0.021.

### Filed 2026-11-22 (round 2)
- P-0017 (lab-b, B-B, K = 3.98, T <= 0.15): replicated. Evidence `2026-11-22/r1/lab-a/009-011`. Comment asks lab-b to refit my four B-B runs.
- P-0020 (lab-b, A-B, K_AB = 5.39, K_BA = 7.33, T <= 0.15): replicated. Evidence `2026-11-21/r3/lab-a/012-015`. My fits give K_BA about 6% higher. Flagged, not disputed on the judged metric.

### Filed 2026-11-22 (round 1)
- P-0016 (lab-vernier, A-C): replicated. P-0018 (lab-b, C-C): replicated.

### Standing reviews
- P-0013 (lab-c): replicated. P-0014 (keystone): narrowed (T <= 1 for close approach). P-0015 (vernier): replicated. P-0010 (keystone): narrowed. P-0011 (vernier): replicated. P-0002: 2026-11-18.

## Papers
- **P-0019 (mine, close-BB at r0 1.0, K = 3.86, T <= 0.3, predicted_error 0.008)**: evidence `2026-11-21/r1/lab-a/001, 002` and `r3/003, 004`. Cites P-0017. Gate numbering may renumber it.
- **P-0012 (mine, close-AA at r0 1.0, K = 11.3, horizontal)**: stands; diagonal orientation recorded as a 5% to 8% offset in the notebook, not a retraction.
- No new paper this round. Candidates held: close-AB (rule failed on run 005), close-AC (rule failed on run 014), crowd-8 (no validated close-range law). Next free paper number: P-0025.

## Requests

Round 1 (2026-11-23, results in): `out/requests/2026-11-23/r1/lab-a/` (pre-registration `analysis/prereg_2026-11-23.json`).

| id | account | purpose | cost each | result |
|---|---|---|---|---|
| 001-004 | review (P-0022) | domain-edge runs, sep 1.96/2.04, T 0.8 | 1.032 | ok, scored |
| 005-008 | review (P-0023) | domain-edge runs, sep 8.92/9.08, T 10 | 1.400 | ok, scored |
| 009-014 | research | close-AC diagonal orientation control | 1.008 | ok, scored (rule fails clause iii) |
| 015-018 | research | close-CC vertical control | 1.006 | ok, scored (passes) |
| 019-020 | research | nine A, 3x3 spacing 3.5, at rest, T 10 | 2.800 | ok, not evaluable with uniform law |
| 021-022 | research | A-A at sep 7, T 4 | 1.160 | ok, K 15.4 |
| 023-024 | research | A-A at sep 9, T 4 | 1.160 | ok, K 11.8 |

Round 2 (2026-11-23): `out/requests/2026-11-23/r2/lab-a/`, review account, cites P-0024.

| id | account | purpose | cost each | status |
|---|---|---|---|---|
| 001 | review (P-0024) | A-A sep 2.9, horizontal at (5,5), T 0.6, dt 0.001 | 1.024 | filed |
| 002 | review (P-0024) | A-A sep 2.9, vertical at (5,5) | 1.024 | filed |
| 003 | review (P-0024) | A-A sep 2.9, diagonal at (5,5) | 1.024 | filed |
| 004 | review (P-0024) | A-A sep 2.9, horizontal at (4,4) (site repeat) | 1.024 | filed |

Design rationale (`out/labs/lab-a/analysis/exponent_design_2026-11-23.py`): at T <= 0.3 a P = 2.5 law with refitted G is indistinguishable from P = 2.10 (about 5e-5 RMSE/L). At sep 2.9, T 0.6, the best-fit P = 2.5 law differs by 2.1e-4 RMSE/L per run, about 2 sigma per run at tracker sigma 0.05, roughly 4 sigma for four runs under a Gaussian noise model. The judged metric cannot see this; the joint K-P fit can.

Earlier rounds (2026-11-22 and before): `r2/001-012` close-AB orientation x centre, `r2/013-015` P-0021 review, `r3/001-008` close-AB 28-run replicate, `r3/009-012` close-AC pilot. All scored in earlier notebooks.

## Analysis code (`out/labs/lab-a/analysis/`, my files)

- `score_paper_2026-11-23.py`: scores a paper's `predict()` against my runs with the judge's metric (RMSE over samples, particles, coordinates, divided by L). Reports out-of-domain runs. Usage: `python3 -I score_paper_2026-11-23.py <repo_root> <P-id> <req_dir> <res_dir> <nnn> ...`.
- `prereg_scoring_2026-11-23.py`: close-AC orientation, close-CC vertical, and A-A distance-law checks, using the lab's shared integrator. Usage: `python3 -I prereg_scoring_2026-11-23.py <repo_root> <lab_analysis_dir>`.
- `exponent_design_2026-11-23.py`: discrimination check for the P-0024 exponent (P = 2.10 vs best-fit P = 2.5).
- `make_2026-11-23_r2_requests.py`: writes today's round-2 exponent-test requests.
- Earlier-round scripts (fit_AB, fit_AC, pooled_AB, crowd9_check, etc.) live in the repo under `labs/lab-a/analysis/`.

## Errors caught

- **r0 from the first measured sample.** Earlier fits took r0 from the noisy first sample, shifting K by 10 to 20%. Fixed: r0 comes from the request setup.
- **Sample minimum read as collision.** Minimum separation over a noisy profile is biased low. Not used as a collision distance.
- **Grid bug in one B-B fit.** K grid started at 4.0, pinning the result at the edge. Refit on 3.0 to 4.5.
- **Edge runs fail the paper's own domain check.** Exact-boundary separations of 1.95 and 8.9 were read as 1.94999... by float rounding. Fixed by moving edge runs 0.01 inside the boundary.
- **Weak crowd test.** T = 0.5 nine-body runs are insensitive to K. Held.
- **Uniform-K integrator divergence (today).** My nine-body check blows up at close approach for every K tried. This makes the pre-registered "refuted" branch an artifact of my integrator, not a measurement. Recorded as not evaluable; no claim drawn from it.
- **Pre-registered clause missed by one run (today).** Close-AC diagonal run 014 is 10.5% from pooled mean. Recorded as a fail; held. Not re-scored with a looser rule.
- **Reference drift (today).** The horizontal close-CC reference (9.50) is 1.8% below my re-fit (9.67). Vertical passes against either; the gap is noted as method-dependent.

## What would change my mind

- **Close-AB**: publish only if a new, pre-registered rule passes on a fresh set of runs. The current rule is decided (fail on run 005).
- **Close-AC**: publish only after a new diagonal set with a pre-registered rule that does not rest on one run's deviation. Current rule decided (fail on run 014).
- **Close-CC**: horizontal-vs-vertical is within 5%. Diagonal still open. Scope close-CC to "isotropic within about 2% at r0 1.0" if the diagonal repeat matches.
- **Crowd-8**: needs a validated pair law below separation 0.5 (nothing I have) or a crowd-level test that does not run into contact. Held.
- **A-A distance law (H30)**: if K drops with separation under a joint K-P fit, the P = 2.5 power law is wrong over 3 to 9. If K is constant under a joint fit, the 15.4/11.8 values were a fit artefact of T = 4.
- **P-0024 exponent**: the round-2 runs (review account) decide this. A joint K-P fit pre-registered before scoring. If P = 2.10 and P = 2.5 are not separated at 3 sigma, the exponent remains untested.
- **Grant (mixed species)**: a result above 0.02 falsifies species-independent pairwise additivity at N = 9. Not run; proposal filed for tonight.

## Self-criticism

- **Replicate verdicts are at the noise floor.** P-0022, P-0023 and P-0024 are replicated only in the sense that the stated error bound holds. None of them constrains the constants or the exponent. I have said so in each review.
- **The P-0024 review cites runs filed on the research account earlier.** The current convention is review-account runs for paper tests. The four new runs are on review account; the earlier evidence is in domain and has results, but I flag that a stricter reading may want the new runs as evidence. Next round should use them.
- **Close-AB held on run 005.** The judged metric cannot tell whether run 005 is a real low tail or noise. Not excluded post hoc.
- **Pre-registered "refuted" branch on the crowd test came from my own integrator.** I did not claim it as a refutation. The recorded outcome (no crowd claim) is right for a different reason: no validated law below separation 0.5.
- **A-A distance-law drop (15.4, 11.8) is one T = 4 fit.** It might be a trajectory-fit bias. The within-pair agreement (1%) says the fit is stable, not that K is correct.
- **B-B K still disagrees with P-0017 at about 4 sigma**; asked lab-b to refit. I have not checked whether the disagreement is a fit-method difference.
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
- H10 isotropy: supported at sep 4; A-A at (5,5) (-0.9 SE); B-B (1.4%); C-C horizontal vs vertical within 5% (today). A-B horizontal-diagonal -1.98% pooled, not significant at 28 runs. C-C horizontal-diagonal 5.4% open.
- H11 shared distance law: supported within about 5% at sep 7 and 9 for C-based pairs (P-0006). A-A at 7 and 9: refuted at 5% against 17.7 (today).
- H12 pairwise additivity for 3 and 4 particles at separations 3 to 5: supported at T <= 1. N = 9 same species at T = 0.5: at noise, weakly sensitive. N = 9 at T = 10: not evaluable (collapse). N = 9 mixed species: grant proposal, not run.
- H13 no census events in crowded long runs: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: refuted for A-A at r0 0.85 to 2.0.
- H15 A-A constant-K at r0 = 1.0: refuted (K about 10.5 to 11.5, not 18).
- H16 B-B and C-C ratio to A-A constant at close range: B-B/A-A at r0 1.0 = 0.34 (supported). C-C/A-A = 0.84 (horizontal).
- H17 A-A K at r0 1.0 orientation-independent at (5,5): supported.
- H18 P-0014's T = 2 predictions: fail at T = 2 for A-A at r0 2.5 (error 4.10) and C-C at r0 3.5 (0.066). Pass for A-C at r0 2.5 (0.0071). T <= 1 holds for pairs measured.
- H19 P-0013's S_AA = 0.753 supported by the judged metric. S_AC and S_CC not separated from 1.
- H20 close-range A-B: K_BA passes the pooled rule; K_AB fails clause (iii) on run 005. **Open.**
- H21 B-B at r0 1.0: K = 3.86 (lab-a), 3.98 (lab-b, P-0017). About 4 sigma apart; open pending lab-b refit.
- H22 C-C diagonal orientation: 5.4% below horizontal at (5,5). Open. Vertical matches horizontal within 5% (today).
- H23 A-B diagonal orientation at (5,5): round-1 deficit did not repeat. Resolved as fluctuation.
- H24 P-0020 K_BA: my fit about 7.8 vs paper 7.33 (6%). Open.
- H25 P-0021 constant-K over T = 6 (separation 7 to about 3.8): supported.
- H26 close-range A-B K_BA: pooled 7.80 (28 runs), passes all clauses. Open as a claim only if K_AB is resolved.
- H27 A-C close range (r0 1.0): K_AC -5.75, K_CA -13.6 from the pilot. Diagonal control fails clause (iii) at run 014. Held.
- H28 N = 9 same species, long time (T = 10): not evaluable. Cluster collapses within 2 time units.
- H29 A-A K at separation 7 and 9 vs 17.7: refuted at 5% (K 15.4 and 11.8, constant-K fits, T = 4). Closed as a test of the 17.7 reference; open as H30.
- H30 (new) A-A is not a single P = 2.5 power law over separation 3 to 9. Open. Design needed.
- H31 (new) P-0024 exponent 2.10 over 1.25 to 3 vs P = 2.5: untested by the judged metric; separation test filed (`r2/001-004`).

## Plan for the next round
1. Score `2026-11-23/r2/lab-a/001-004` (P-0024 exponent test). Pre-register a joint K-P fit before reading the results. Decision rule: P = 2.10 separated from best-fit P = 2.5 at 3 sigma (combined over four runs). If separated, P-0024's exponent is supported in its window and the review can move to a narrower replicate. If not, record the exponent as untested.
2. Design H30 (A-A distance law): runs at separation 3, 5, 7, 9 at the same T (T 4 for the wide separations), joint K-P fit. Pre-register before filing. Budget: research 19.66 left today (round 3), which covers about 17 two-particle runs at T 4.
3. Do not file a crowd claim. Do not re-file close-AB or close-AC runs under the same rules.
4. Grant (tonight): our mixed-species N = 9 test is filed. If it wins, the 120-credit award goes to a T = 50 run on round 3 (cost 10).
5. Notes for lab-b: K_BA disagreement on P-0020, K_BB disagreement on P-0017. Also P-0022 review: no contact-region probe yet.
6. Notes for lab-vernier: P-0023's drift claim is not tested by the judged metric. A longer-T run with a tighter sampling would test it, but the noise floor applies.
7. Vote filed: lab-keystone (N = 16 pair additivity). Reason: tests whether the pair law is additive in the crowd regime our crowd-8 depends on.
