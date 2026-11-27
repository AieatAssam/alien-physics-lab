# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely, and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-27, round 3 (scored round-2 contact runs; filed the tonight's grant request and 9 research replicates; pre-registered the round-3 predictions).

## Round 3 summary (2026-11-27)

- **The contact outcome is not reproducible between identical runs.** `r1/001` and `r2/001` have identical requests (A-A at rest, r0 1.0 horizontal, T 0.6, dt 0.0003). They agree to tracker noise up to t = 0.24 (the pre-contact collapse), then diverge from t ≈ 0.32. At t = 0.60 they differ by 0.85 in separation (1.996 vs 1.146). Tracker noise on a separation is about 0.07, so this is a real difference in the simulator's state, not noise. Details in "Round-2 results" below.
- **Three distinct post-contact classes from the same setup.** (i) rise past 2.0 (`r1/001`); (ii) plateau near 1.15 to 1.2 (`r2/001`, and the vertical `r2/002` which agrees with `r2/001` within 0.06 post-contact); (iii) confined near-contact oscillation between about 0.0 and 0.75 with repeated dips below 0.3 (`r2/003`, dt 0.001, T 2.0).
- **H37 reframed.** The question is no longer "which contact rule" but "is the post-contact outcome a random draw per run (or per encounter), and does sample_dt matter". Round-3 requests (below) test both.
- **Tonight's grant filed** as the proposal was written (`out/requests/2026-11-27/r3/lab-vernier/001.json`, account `grant`, cost 1.32). Its four pairs give four post-contact outcomes in one run, which also tests whether outcomes are independent between pairs.
- **Research replicates filed**: 002 to 006 (exact r1/001 setup, five runs) and 007 to 010 (exact r2/003 setup, four runs). Cost 5.12 and 4.32.
- **P-0034 accepted** on 2026-11-26 (A-A and C-C at 3.0 to 3.5, T up to 1; supersedes P-0014). This appears to settle the open problem contested-P-0014 (P-0014 is now superseded; check problems.json to confirm the bounty).
- **No review was owed this round** (no paper awaiting review by me). The review account has 11.94 credits left for today.
- **No paper filed this round.** The contact non-reproducibility is a notebook finding for now. A paper on it would need a model that predicts the post-contact outcome, which this data cannot yet support. Publish after the round-3 replicates score.

## Round-2 results (2026-11-27/r2): scored against the pre-registration

Scripts: `out/labs/lab-vernier/analysis/score_r2_2026-11-27.py`, `traces_r2_2026-11-27.py`, `score_r2_extrema_2026-11-27.py` (stdlib, run with `python3 -I`).

| prediction (written in round 2, before results) | outcome |
|---|---|
| **r2/001** (exact replicate of r1/001): smoothed separation agrees with r1/001 within 0.02 | **Failed.** Pre-contact (t ≤ 0.24): max diff 0.019, as expected. Post-contact: max diff 0.85 at t = 0.60. Divergence exceeds 0.05 from t ≈ 0.32. A disagreement of this size means the simulator's contact outcome is not deterministic across identical requests. This is the instrument result the pre-registration named. |
| **r2/002** (vertical r0 1.0): same trace as r1/001 within 0.02; separation at t 0.60 about 2.0 | **Failed as written.** Against r1/001: max diff 0.81 post-contact; separation at 0.60 is 1.205, not 2.0. **But** r2/002 matches the replicate r2/001 within 0.06 for t in [0.30, 0.60]. So the orientation test passes against the replicate and fails against r1/001. The reference run r1/001 is the outlier, not the orientation. Isotropy is **not falsified**, but only the vertical-vs-replicate comparison is informative. |
| **r2/003** (T 2.0, dt 0.001): bound orbit, max separation 2.7 to 4.5 reached near t 1.0 to 1.5, then falls | **Failed.** No bound orbit at that scale. For t ≥ 0.3 the raw max separation is 0.91 (at t = 0.375); the smoothed max is 0.75. The pair keeps approaching to near-contact: separate dips below 0.3 at t = 0.54, 0.76, 1.08, 1.36, 1.54, 1.78; per-sample minimum 0.005 at t = 1.099. Not an ejection (separation never rises to 5 and the trace is not still rising at t = 2.0; it is 0.28 at t = 2.0). |

Pre-registration outcome for the proposal's pre-contact falsifier (unclamped P-0026 law, RMSE/L ≤ 0.02 up to first separation below 0.5): met by r1/001 and r2/001 (RMSE/L 0.007 each, earlier scoring). The pre-contact law is not the issue; the post-contact outcome is.

### Post-contact traces (smoothed separation, 0.02 bins)

| t | r1/001 (T 0.6, dt .0003) | r2/001 (replicate) | r2/002 (vertical) | r2/003 (T 2.0, dt .001) |
|---|---|---|---|---|
| 0.18 | 0.522 | 0.520 | 0.512 | 0.508 |
| 0.20 | 0.364 | 0.380 | 0.362 | 0.340 |
| 0.24 | 0.167 | 0.184 | 0.185 | 0.187 |
| 0.30 | 0.690 | 0.650 | 0.654 | 0.607 |
| 0.36 | 1.066 | 0.898 | 0.924 | 0.724 |
| 0.40 | 1.267 | 1.014 | 1.026 | 0.723 |
| 0.50 | 1.690 | 1.162 | 1.168 | 0.431 |
| 0.54 | 1.842 | 1.170 | 1.173 | 0.135 |
| 0.60 | 1.996 | 1.146 | 1.205 | 0.487 |
| 0.76 | — | — | — | 0.132 |
| 0.90 | — | — | — | 0.694 |
| 1.00 | — | — | — | 0.587 |

Reading: pre-contact (through t ≈ 0.24) all four runs are the same to noise. Divergence starts within 0.05 to 0.1 time units after the collapse. The three outcomes are different in kind, not just in timing.

## Round-3 requests and pre-registered predictions

Written before any round-3 result exists. Round-3 runs land in the next night's sim; score them next session.

| request | setup | account | cost | prediction and falsifier |
|---|---|---|---|---|
| r3/001 | tonight's grant: 4 A-A pairs at rest, r0 1.0 (x = 2, 3 and 7, 8 at y = 2.5 and 7.5), T 2.0, dt 0.001, 8 particles | grant | 1.32 | (a) Pre-contact: each pair's separation matches the unclamped P-0026 law to RMSE/L ≤ 0.02 up to the first separation below 0.5 (expected, already met elsewhere). (b) **Per-encounter randomness** predicts the four pairs do not all share one post-contact class. **Per-run randomness** predicts all four pairs share one class. A run with all four in the same class is consistent with per-run randomness only. |
| r3/002 to 006 | exact r1/001 setup (A-A at rest, r0 1.0 horizontal, T 0.6, dt 0.0003); five replicates | research | 5.12 | Classify each run by separation at t = 0.60 (0.02-bin mean). Existing classes: plateau in [1.10, 1.25] (r2/001 1.146, r2/002 1.205) and rise in [1.85, 2.15] (r1/001 1.996). **Falsifier:** any new run with separation at t = 0.60 outside both bands (a third class, or a class in between). **Distribution prediction:** the five runs fall into both classes (not all one class; probability about 6 % under 50:50 per-run randomness). |
| r3/007 to 010 | exact r2/003 setup (A-A at rest, r0 1.0 horizontal, T 2.0, dt 0.001); four replicates | research | 4.32 | Tests whether the dt = 0.001 oscillation recurs. **Prediction H_dt** (outcome set by dt): each new run stays below 1.0 for t in [0.5, 2.0] and dips below 0.3 at least twice. **Falsifier:** any new run with separation above 1.0 at some t in [0.5, 2.0]. A run that reaches 2.7 or more in [0.5, 2.0] would also falsify the oscillation class outright. |

Interpretation guide:
- If 002 to 006 are one-class (all plateau or all rise), and 007 to 010 all oscillate, the outcome looks determined by dt and not by randomness. Then the r1/001 vs r2/001 disagreement is the odd one; check whether something about the request (run index, request id) changes the sim.
- If 002 to 006 mix classes and 007 to 010 mix classes too, the outcome is per-run random and dt is not the controlling variable. Then no post-contact claim can be a point prediction; the claim becomes a distribution (class frequencies).
- If the grant's four pairs share a class, outcomes are per-run, not per-encounter. If they differ, per-encounter.

Cost check: research spend today is 5.16 (ledger) + 9.44 (this round) = 14.60 of 40. About 25.4 remains unused and does not roll over. Grant: 1.32 of 120. The rest of the grant (118.7) is not used by this design; it is outside the filed proposal, and spending it on a longer or larger design would be a new design the lab did not propose. Flag to the user if that is a problem.

## Round-2 requests (for the record)

- 2026-11-27/r2/lab-vernier/001: exact replicate of r1/001. Cost 1.02. Result: diverges post-contact (above).
- 2026-11-27/r2/lab-vernier/002: vertical r0 1.0 (5.0, 4.5) and (5.0, 5.5), T 0.6, dt 0.0003. Cost 1.02. Result: plateau class, matches r2/001 (above).
- 2026-11-27/r2/lab-vernier/003: horizontal r0 1.0, T 2.0, dt 0.001. Cost 1.08. Result: oscillation class (above).

## Round-1 requests (2026-11-27/r1)

- 001 (r0 1.0 contact, T 0.6, dt 0.0003) and 002 (r0 1.5, T 0.6): see round-1 record in the earlier notebook. Pre-contact matches the bare law to noise. r1/002 minimum 0.013 at t = 0.429 against bare collapse 0.42. Its post-contact trace was not replicated.
- 003 to 005 (P-0035 edge runs, review account): 0.00497, 0.00500, 0.00502 RMSE/L. Bar 0.018. Matches the paper's prediction.

## Papers

- **P-0034** (round 3, A-A and C-C at 3.0 to 3.5, T ≤ 1; supersedes P-0014 inside that domain). **Accepted 2026-11-26.** Claims P-0034-c1 (A-A), P-0034-c2 (C-C); domain r_range [3.0, 3.5], max_particles 2; predicted error 0.007. Standing replications: lab-b (2), lab-c (5), lab-keystone (4). Refer to it by title if the id changes.
- **P-0030** (round 1, A-C at 2.5 to 3.5; predicted error 0.008). Not P-0029, which is lab-a's A-A table.
- **Standing reviews (mine):** P-0012, P-0017, P-0024 (replicated, round 1); P-0028 (replicated, round 1); P-0026 (replicated, 2026-11-24); P-0029 (replicated, round 3); P-0031, P-0033, P-0032 (replicated, 2026-11-26); P-0035 (replicated over r0 2.0 to 2.75, T ≤ 0.6; updated 2026-11-27 with the edge runs).
- No paper is filed by me this round.

## Grant

- **Tonight's grant (2026-11-27), won with 3 votes**: four A-A pairs at r0 1.0 through contact. Filed as proposed: `out/requests/2026-11-27/r3/lab-vernier/001.json`, account `grant`, cost 1.32.
- **Round-2 vote** (2026-11-27): lab-c (Nullius). Reason: its dt-only replicate of r1-012 bears on whether the contact outcome is a sampling artefact. Not my own proposal.
- Past grants: 2026-11-25 award (120) used for round-3 runs 001 to 004 (H32, N = 16).

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported (P-0011); residuals 0.050 per coordinate.
- **H2** (species-independent noise): supported.
- **H3** (no clipping near a wall): supported.
- **H4** (no sample-timing offset): **reopened for contact runs.** r2/003 (dt 0.001) and the dt = 0.0003 runs disagree after the collapse. But r1/001 and r2/001 share dt and also disagree, so dt alone does not explain the split. Round-3 replicates test dt directly (007 to 010 vs 002 to 006).
- **H5** (stationarity over T = 100): mean supported; x-spread variation not reproduced.
- **H6** (P-0003 domain): separation 3 fails for P-0003 (r1/007). Separations 4 and 5 pass.
- **H7** (P-0006 shared-law factor at separation 9): supported within 3 percent.
- **H8** (P-0008 coefficients flat over separations 3 to 5): supported for A-B and B-C; not for A-A at 3 and 4.
- **H9** (P-0010 far-field G(r0)): replicated at all three pairs and A-A at 6.
- **H10** (A-A coefficient at separation 4 is 17.70): supported by the diagonal replicate.
- **H11** (close-range B-C): supported (P-0015).
- **H12** (A-B and B-B not constant-K over the first 0.3 time units at r = 1): open.
- **H13** (pairwise superposition, N > 2): supported at N = 16, T = 1; and at N = 3, 4 for the P-0031 and P-0033 layouts. N = 5 untested.
- **H16** (contact failure, close approach): narrowed. The unclamped P-0032 law fits to noise at T = 0.6 with minimum separations 0.51 to 0.57. Pre-contact is fine; post-contact is H37.
- **H17** (K_B(A)/K_A(B) = 1.41): supported at round-3 windows; ratios 1.37 to 1.52.
- **H20** (state dependence): not supported at the 3-SE rule (round 2, n = 16).
- **H21** (orientation invariance for A-B): not falsified at 3 percent.
- **H24** (K_eff(r) for A-B at P = 2.5 is not constant): supported at 6 SE between r about 1.4 and 2.4.
- **H25** (A-A exponent differs from A-B exponent): not supported at present.
- **H26** (A-B force shape is not a single power law): open.
- **H27** (B-B K at r = 1 is 3.86 (P-0019) or 3.98 (P-0017)): open. Icarus's B-B exponent proposal (lab-b) would also test this.
- **H28** (A-C node coefficients change 3 to 4 percent across 2.5 to 3.5): supported out-of-sample.
- **H30** (A-A and C-C piecewise nodes at 3.0 to 3.5, T ≤ 1): supported out-of-sample.
- **H31**: 1 to 3 percent differences in K are below the 0.007 bar. Use regime tests.
- **H32** (P-0028 pair table holds at N = 16, T = 1): supported.
- **H33** (P-0032 law holds for r0 2.0 to 2.5 through T = 0.6, including near-contact): supported (replicated).
- **H34** (P-0031 table holds for asymmetric N = 3): supported.
- **H35** (P-0033 square law holds as the square contracts below separation 5): supported.
- **H36** (P-0035 law holds at the upper edge, r0 2.75, T = 0.6): supported (0.00497 to 0.00502 against bar 0.018).
- **H37** (post-contact outcome of A-A at rest, r0 1.0): **reframed, open.** Pre-contact is the bare law to noise. Post-contact outcomes are not reproducible across identical runs (three classes: rise, plateau near 1.17, near-contact oscillation). Two sub-questions: (a) per-run or per-encounter randomness (grant run and 002 to 006 test this); (b) dt dependence (007 to 010 vs 002 to 006 test this).

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. State which verdict is being made and check the bar for that verdict. State any unreached part of the domain in the comment.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions for exact-edge domains, or sit a small margin inside the edge. Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling.** The cost is `1 + k * particles * duration`, independent of sample count. Always set `sample_dt = duration / 2000` (the cap).
5. **Pre-contact windows for attractive pairs.** A full-window fit or prediction through a close pass is invalid when the integrator diverges. Scores for my own fits use the window before the first measured separation below 1.5 (or below 0.5 for contact runs). The judge scores the full run, so check the pre-contact prediction separately.
6. **Bars are loose at T ≤ 0.3 and in general at the 0.007 level.** Falsification needs a regime change: close approach, long time, N, or a new pair.
7. **Label K by the window's mean separation**, not by the start separation.
8. **Judge domain excludes duration, but predictors do.** Several predictors refuse durations outside their window. A refused run cannot be cited as evidence.
9. **Write only under `out/`.** Analysis code and fits go in `out/labs/lab-vernier/analysis/`. The older source folder `labs/lab-vernier/analysis/` is read-only reference.
10. **Pre-register before results.** Predictions for each new run are written in this notebook before its results are read.
11. **Asymmetric layouts are in the judge domain but not in a paper's claim** when the claim says so. A miss there is "narrowed", not falsified, unless the paper's stated scope includes them.
12. **Do not vote for own proposal; vote on information value.** Note redundancy with my own runs.
13. **Reviews are standing and permanent.** If an edge run contradicts a filed review, update the review rather than leave it.
14. **Check whether a pending proposal's falsifier is already met by my own research runs** before spending grant credits on it.
15. **Identical requests are not guaranteed identical outcomes (new, round 3).** After a singular contact, two runs with the same request can differ by up to 0.85 in separation. A post-contact claim needs at least three replicates, and it must be stated as a distribution with its classes, not a point prediction. Pre-contact claims are unaffected.
16. **Score a replicate against the replicate, not only against a reference run.** Round 3 showed a reference run can itself be the outlier (r1/001). Report both comparisons.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result. Independent of `sample_dt`. Examples: 2 particles at T = 0.6 costs 1.024; 2 at T = 2.0 costs 1.08; 8 at T = 2 costs 1.32; 16 at T = 0.6 costs 1.19.

Budgets: research 40/day; review 15/day (only with `cites_paper`); grants 120 on the award night, usable in round 3 of that date.

Ledger for 2026-11-27 (as of round 3): research 5.16 spent before round 3 (per the ledger) + 9.44 filed this round = 14.60 of 40. Review 3.06 of 15 (no paper awaiting review). Grant 1.32 of 120 filed (round 3).

## Plan for the next session

1. **Score round-3 results** against the table above, before comparing to other data. Start with the r3/002 to 006 classes at t = 0.60 and the r3/007 to 010 oscillation check.
2. **Score the grant (r3/001)**: pre-contact for all four pairs first; then the per-pair post-contact class. Note the cross-pair forces (about 0.8 at separation 5) may shift a pair's contact time slightly; check the pre-contact fit per pair.
3. **Decide the claim type.** If the outcome is per-run random, publish a distribution claim (class frequencies with n, not a point prediction) and a repeatability caution for all labs running contacts. If it is dt-determined, publish a dt-dependence claim with the dt values and the classes they produce.
4. **Tooling:** `score_r2_2026-11-27.py`, `traces_r2_2026-11-27.py`, `score_r2_extrema_2026-11-27.py` are in `out/labs/lab-vernier/analysis/`. Run with `python3 -I` and the repo root as argument. Scripts are stdlib only.
5. **Icarus's B-B proposal (lab-b)**: still the most informative untested pair. Vernier would support it in a round-3 vote if it is still open.
6. **P-0035 review:** still current; no action unless a new in-domain run contradicts it.

## Not read

`gate/`, `tools/`, `exam_papers.json`, and the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were run only as the review rules require (P-0035 in round 1; P-0031, P-0032, P-0033 in round 2; P-0026, P-0028, P-0029 in earlier rounds to score my own runs).
