# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely, and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-27, round 1 (review of P-0035, contact probe, grant proposal).

## Round 1 summary (2026-11-27)

- **Review of P-0035 (lab-c, A-A pair at rest, r0 2.0 to 2.75, T <= 0.6), filed as `out/reviews/P-0035/lab-vernier.json`: verdict replicated.**
  - Scored with `analysis/judge_score.py` (run with `python3 -I`) on four of my own in-domain runs: 2026-11-26/r1/lab-vernier/008 (r0 2.00 horizontal) 0.00503; 009 (2.50) 0.00498; 010 (2.25 diagonal) 0.00500; 011 (2.00 diagonal) 0.00502. Bar 0.018. All at the noise floor.
  - **Scope gap, stated in the review:** none of the four cited runs sits at the claim's upper edge, r0 = 2.75. The review says it covers 2.0 to 2.5 until the edge runs report.
  - **Pending edge runs (filed today, results next round):** 2026-11-27/r1/lab-vernier/003 (2.75 horizontal), 004 (2.75 vertical), 005 (2.75 at the 2.0 wall corner, both particles exactly 2.0 from the left and bottom walls). All three pass the paper's own `predict()` domain check. Pre-registered: each scores at the noise floor (RMSE/L 0.004 to 0.006, bar 0.018). If any scores above 0.018, the review must be updated (it is a standing review).
  - **Wall clause:** the "at least 2.0 from every wall" condition is non-binding for an attracting pair at rest, which moves inward. Run 005 tests the boundary anyway.
- **Contact probe (exploratory, no claim), requests 001 and 002, research account, 1.024 credits each:** A-A pair at rest at r0 1.0 (4.5/5.5, y = 5) and r0 1.5 (4.25/5.75, y = 5), T = 0.6, tracker only, sample_dt 0.0003.
  - **Pre-registered predictions** (from `analysis/contact_prereg_2026-11-27.py`, the P-0026 law integrated as r'' = -G/r^P, G = 23.63, P = 2.099, no contact model):

    | r0 | separation 0.5 at | separation 0.3 at | separation 0.1 at | relative speed at 0.3 |
    |---|---|---|---|---|
    | 1.0 | t = 0.186 | t = 0.209 | t = 0.223 | 10.9 |
    | 1.5 | t = 0.386 | t = 0.407 | t = 0.421 | 11.6 |

  - The law as written has a finite collapse time, t about 0.23 for r0 1.0 and about 0.42 for r0 1.5, and a diverging speed at contact. So the simulator must do something other than the bare law at contact: pass through, bounce, soften, or stop. The question is which, and at what separation the bare law stops describing the data.
  - **Discriminators (fixed before results):**
    - *Pass-through with the law continuing:* tracker separation falls to the noise floor (about 0.1) near t = 0.23, then re-expands roughly symmetrically about that time.
    - *Hard-core bounce:* separation returns to a finite value (a few tenths) after a minimum, with the two particles moving apart at contact.
    - *Softened or capped force:* the pre-contact trajectory departs from the bare law before separation 0.3 (observed separation at t = 0.21 well above 0.3).
  - Tracker separation noise is about 0.07 (two coordinates at 0.05), so separations below about 0.15 cannot be told from contact.
- **Grant proposal filed tonight:** `out/grants/2026-11-27/proposals/lab-vernier.json`. Four A-A pairs at r0 1.0, pair centres 5 apart in x, 8 particles, T = 2.0, sample_dt 0.001 (cost 1.32). Pitch shortened to 506 characters (limit 600) after the first draft ran to 710.
  - **Changed from last round's proposal:** the falsifier now applies only before the first tracker separation below 0.5, at RMSE/L 0.02. Last round's falsifier ran through T = 2 and would have been dominated by post-contact integrator artifacts (the paper models have no contact rule), so it could not discriminate the pair law from the contact rule.
- **Research credits:** 40 allowed; 2.05 spent (001, 002). 37.95 unused and lost at day end. Accepted: no other pre-registered run is ready at the 0.007 bar.
- **Review credits:** 15 allowed; 3.07 committed to 003 to 005 (if all three are accepted at 1.024 each; the review account is charged on results).

## Pre-registered predictions for the round-1 (today) runs

Written before any result exists. Results will be scored next round.

| request | setup | account | prediction | bar |
|---|---|---|---|---|
| 001 | A-A r0 1.0, T = 0.6 | research | pre-contact follows the bare law; separation reaches 0.5 at t = 0.19. Under the bare law continued through the origin, the pair returns to separation 1.0 at t about 0.46 (time-symmetric about t_c = 0.23) and falls again. Measured behaviour after t about 0.23 is one of: pass-through (the symmetric return, separation back near 1.0 by t about 0.46), bounce (a finite minimum, then separation grows), or softened (departure from the bare law before separation 0.3) | exploratory |
| 002 | A-A r0 1.5, T = 0.6 | research | pre-contact follows the bare law to separation 0.5 at t = 0.39; collapse time about 0.42 | exploratory |
| 003 | A-A r0 2.75 horizontal, T = 0.6 | review (P-0035) | RMSE/L about 0.005 (noise floor) | 0.018 |
| 004 | A-A r0 2.75 vertical, T = 0.6 | review (P-0035) | RMSE/L about 0.005 | 0.018 |
| 005 | A-A r0 2.75 at the 2.0 wall corner, T = 0.6 | review (P-0035) | RMSE/L about 0.005 | 0.018 |

Prior-round predictions for 008 to 011 were recorded in the round-2 notes; the results matched (see below).

## Round-2 summary (2026-11-26), kept for the record

- Review runs scored (round 1 of 2026-11-26, cost 1.02 to 1.16 each, 12.08 of 15 review credits): every in-domain run sits at the noise floor.
  - **P-0031 (lab-b), 001-004:** RMSE/L 0.00501 to 0.00506; bar 0.021. Nulls 0.018 to 0.040.
  - **P-0033 (lab-keystone), 005-007:** RMSE/L 0.00499 to 0.00504; bar 0.021. Nulls 0.041 to 0.042.
  - **P-0032 (lab-c), 008-011:** RMSE/L 0.00498 to 0.00503; bar 0.018. Nulls 0.014 to 0.021.
- Reviews filed: P-0031 replicated (4 of 4 in-domain); P-0033 replicated (3 of 3); P-0032 replicated (4 of 4). All evidence is my own round-1 review ids.
- Close approach from P-0032 runs: in 008 and 011 (T = 0.6, r0 = 2.0) the tracker minimum separation is 0.57 and 0.51. The paper's own predict gives 0.69 at T = 0.6. The unclamped law fits to the noise floor through that near-contact at T = 0.6.
- Grant vote cast (`out/grants/2026-11-26/votes/lab-vernier.json`): **lab-keystone** (A-B pair at 2.5, first cross-species test). Did not vote for my own proposal. The 2026-11-26 award went to lab-a (title: radial fall of an A-B pair from r0 = 9; votes lab-a 2, lab-vernier 2, lab-keystone 1; winner lab-a).

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. State which verdict is being made and check the bar for that verdict. State any unreached part of the domain in the comment.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions (4.5, 5.5, 2.75, 4.75, ...) for exact-edge domains, or sit a small margin inside the edge. Run each setup through the paper's own `predict()` before filing (a one-line check on `papers/<P>/model.py`).
4. **Dense sampling.** The cost is `1 + k * particles * duration`, independent of sample count. Always set `sample_dt = duration / 2000` (the cap).
5. **Pre-contact windows for attractive pairs.** A full-window fit or prediction through a close pass is invalid when the integrator diverges (roughly after separation 0.5 in my own A-A runs at r0 2.5). Scores for my own fits use the window before the first measured separation below 1.5. The judge scores the full run, so check the pre-contact prediction separately when the run closes.
6. **Bars are loose at T <= 0.3 and in general at the 0.007 level.** A constant-K versus table-K difference of 1 to 3 percent moves predicted positions by only about 0.001 to 0.003 RMSE/L, far below the 0.021 bar. Falsification needs a regime change: close approach, long time, N, or a new pair.
7. **Label K by the window's mean separation**, not by the start separation.
8. **Judge domain excludes duration, but predictors do.** Several predictors refuse durations outside their window (P-0024, P-0028 T > 1.0, P-0029: T > 2 for r0 < 7 and T > 3 for r0 >= 7; P-0031 T > 2; P-0032 T > 0.6; P-0035 T > 0.6). A refused run cannot be scored, so it is not cited as evidence.
9. **Write only under `out/`.** Analysis code and fits go in `out/labs/lab-vernier/analysis/`. The older source folder `labs/lab-vernier/analysis/` is read-only reference.
10. **Pre-register before results.** Predictions for each new run are written in this notebook before its results are read.
11. **Asymmetric layouts are in the judge domain but not in a paper's claim** when the claim says so. A miss there is a "narrowed" verdict, not a falsification, unless the paper's stated scope includes them.
12. **Do not vote for own proposal; vote on information value.** Pick the proposal whose result would move the most hypotheses; note redundancy with my own runs.
13. **Reviews are standing and permanent.** If an edge run contradicts a review already filed, update the review rather than leave it.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result. Independent of `sample_dt`. Examples: 2 particles at T = 0.6 costs 1.024; 2 at T = 1 costs 1.04; 4 at T = 2 costs 1.16; 8 at T = 2 costs 1.32; 16 at T = 1 costs 1.32; 16 at T = 3 costs 1.96.

Budgets: research 40/day; review 15/day (only with `cites_paper`); grants 120 on the award night, usable the next round.

## Results and analysis

### Review runs (2026-11-26 round 1), scored round 2

| run | paper | pair range | T | RMSE/L | null | bar | verdict input |
|---|---|---|---|---|---|---|---|
| 001 | P-0031 | 5.5 (equilateral) | 2.0 | 0.00503 | 0.0311 | 0.021 | pass |
| 002 | P-0031 | 6.9 (equilateral) | 2.0 | 0.00506 | 0.0179 | 0.021 | pass |
| 003 | P-0031 | 5.3/6.1/6.9 (scalene) | 2.0 | 0.00501 | 0.0226 | 0.021 | pass (not claimed) |
| 004 | P-0031 | 5.02 to 7.10 (square, rot 30) | 2.0 | 0.00502 | 0.0399 | 0.021 | pass |
| 005 | P-0033 | 5.005 to 7.078 (square) | 2.0 | 0.00502 | 0.0416 | 0.021 | pass |
| 006 | P-0033 | 5.005 to 7.078 (square, rot 30) | 2.0 | 0.00504 | 0.0411 | 0.021 | pass |
| 007 | P-0033 | 5.005 to 7.078 (square, rot 15) | 2.0 | 0.00499 | 0.0407 | 0.021 | pass |
| 008 | P-0032 | 2.0 horizontal | 0.6 | 0.00503 | 0.0214 | 0.018 | pass; tracker min sep 0.57 |
| 009 | P-0032 | 2.5 horizontal | 0.6 | 0.00498 | 0.0140 | 0.018 | pass; tracker min sep 1.66 |
| 010 | P-0032 | 2.25 diagonal | 0.6 | 0.00500 | 0.0177 | 0.018 | pass; tracker min sep 1.15 |
| 011 | P-0032 | 2.0 diagonal | 0.6 | 0.00502 | 0.0214 | 0.018 | pass; tracker min sep 0.51 |

Re-scored against P-0035 (2026-11-27, `judge_score.py`): runs 008 to 011 are all in P-0035's domain (N = 2, species A, r0 2.00 to 2.50); RMSE/L 0.00498 to 0.00503, bar 0.018.

Scripts: `analysis/minsep_round1_review_2026-11-26.py` (closest approach and wall clearance from result files), `analysis/judge_score.py` (judge scorer), `analysis/contact_prereg_2026-11-27.py` (contact-time predictions).

### Round-3 grant (earlier, unchanged): H32 (N = 16, jittered lattice, T = 1)

Runs 2026-11-25/r3/lab-vernier/001-004 score against the P-0028 pair table at 0.00499 to 0.00501 (bar 0.02; nulls 0.041 to 0.044). H13 and H32 supported at N = 16, T = 1, with tangential force structure.

### A-A and C-C at 3.0 to 3.5, T up to 2 (round 2 runs 001 to 004; round 1 runs 006 to 017)

Piecewise-linear nodes from `analysis/fit_pw_round1_2026-11-25.py`:

| pair | K(2.5) | K(3.0) | K(3.5) |
|---|---|---|---|
| A-A | 16.941 | 18.034 | 18.285 |
| C-C | 12.730 | 13.202 | 13.184 |

Pre-contact scores (window before first separation below 1.5): all four runs at 0.00498 to 0.00508, against bar 0.007. H30 supported (A-A and C-C piecewise nodes) within T <= 1, where windows reach separation 1.5 only at T about 1.0 to 1.58.

### Round-1 A-A and C-C at 2.5 (not claimed)

Runs 006, 007 (A-A) and 012, 013 (C-C) at r0 2.5 reach separations of 0.02 to 0.6 within T = 1. Predictions diverge there (RMSE/L in the hundreds; the integrator has no contact model). Excluded from all claims. The P-0032 review runs (008, 011) show the unclamped law holds through near-contact at T = 0.6, which suggests the earlier divergence comes from the T = 1 integration after contact, not from the law at contact. Not tested beyond T = 0.6.

### A-C (P-0030 out-of-sample check, round 2)

Runs 001 to 005, 018, 019 (round 1) at separations 2.5 to 3.5 match P-0030's node interpolation within 1.0 percent (K_AC) and 1.5 percent (K_CA). H28 supported. H29 (P-0014's 4 percent bound on the A side at 3.5) open and untestable at the 0.007 bar.

### P-0029 judge scores (round 3, unchanged)

| run | r0 | T | RMSE/L | null | status |
|---|---|---|---|---|---|
| r2/101 | 5.0 | 2.0 | 0.00499 | 0.0238 | pass |
| r2/102 | 9.0 | 3.0 | 0.00505 | 0.0086 | pass |
| r2/103 | 7.0 | 3.0 | 0.00500 | 0.0155 | pass |
| r2/104 | 8.0 | 3.0 | 0.00501 | 0.0115 | pass |

Verdict: replicated (four cited, bar needs three).

## Papers

- **P-0034** (round 3, A-A and C-C at 3.0 to 3.5, T <= 1, supersedes P-0014 inside that domain). Claims P-0034-c1 (A-A), P-0034-c2 (C-C); domain r_range [3.0, 3.5], max_particles 2; predicted error 0.007. Status: **submitted** (2026-11-25), not accepted at the last check. Renumbering: refer to it by title until the gate assigns the final id.
- **P-0030** (round 1, A-C at 2.5 to 3.5; predicted error 0.008). Not P-0029, which is lab-a's A-A table.
- **Standing reviews (mine):** P-0012, P-0017, P-0024 (replicated, round 1); P-0028 (replicated, round 1); P-0026 (replicated, 2026-11-24); P-0029 (replicated, round 3); P-0031, P-0033, P-0032 (replicated, round 2 of 2026-11-26); **P-0035 (replicated over r0 2.0 to 2.5, filed 2026-11-27; edge runs pending).**

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported (P-0011); residuals 0.050 per coordinate.
- **H2** (species-independent noise): supported.
- **H3** (no clipping near a wall): supported.
- **H4** (no sample-timing offset): supported.
- **H5** (stationarity over T = 100): mean supported; x-spread variation not reproduced.
- **H6** (P-0003 domain): separation 3 fails for P-0003 (r1/007). Separations 4 and 5 pass.
- **H7** (P-0006 shared-law factor at separation 9): supported within 3 percent.
- **H8** (P-0008 coefficients flat over separations 3 to 5): supported for A-B and B-C; not for A-A at 3 and 4.
- **H9** (P-0010 far-field G(r0)): replicated at all three pairs and A-A at 6.
- **H10** (A-A coefficient at separation 4 is 17.70): supported by the diagonal replicate.
- **H11** (close-range B-C): supported (P-0015).
- **H12** (A-B and B-B not constant-K over the first 0.3 time units at r = 1): open.
- **H13** (pairwise superposition, N > 2): supported at N = 16, T = 1; and at N = 3, 4 for the P-0031 and P-0033 layouts.
- **H15** (P-0004-c2 magnitude): consistent with P-0030 at 2.5 to 3.5.
- **H16** (contact failure, close approach): **narrowed.** The unclamped P-0032 law fits to noise at T = 0.6 with tracker minimum separations of 0.51 to 0.57 (paper prediction 0.69). **Now probed directly** by requests 001 and 002 (r0 1.0 and 1.5, T = 0.6): the question is what happens after the bare law's collapse (t about 0.23 for r0 1.0), which no claim covers. Still open.
- **H17** (K_B(A)/K_A(B) = 1.41): supported at round-3 windows; ratios 1.37 to 1.52.
- **H20** (state dependence): not supported at the 3-SE rule (round 2, n = 16).
- **H21** (orientation invariance for A-B): not falsified at 3 percent.
- **H24** (K_eff(r) for A-B at P = 2.5 is not constant): supported at 6 SE between r about 1.4 and 2.4.
- **H25** (A-A exponent differs from A-B exponent): not supported at present.
- **H26** (A-B force shape is not a single power law): open. Keystone's proposal (A-B at 2.5) is the candidate test I voted for.
- **H27** (B-B K at r = 1 is 3.86 (P-0019) or 3.98 (P-0017)): open. Round-2 B-B runs not yet fitted with a pre-contact window.
- **H28** (A-C node coefficients change 3 to 4 percent across 2.5 to 3.5): supported out-of-sample (seven runs, all within 1.0 percent).
- **H29** (P-0014's "within 4%" A-C bound fails on the A side at 3.5): open; not testable at the 0.007 bar.
- **H30** (A-A and C-C piecewise nodes at 3.0 to 3.5, T <= 1): supported out-of-sample (four runs, all at the noise floor).
- **H31**: 1 to 3 percent differences in K are below the 0.007 bar. Shape claims at that level are not falsifiable by a 0.007 claim; use regime tests.
- **H32** (P-0028 pair table holds at N = 16 with tangential force structure, T = 1): supported.
- **H33** (P-0032 law holds for r0 2.0 to 2.5 through T = 0.6, including near-contact): **supported** (review runs 008 to 011, replicated).
- **H34** (P-0031 table holds for asymmetric N = 3, 5.3/6.1/6.9): **supported** (review run 003, in domain though not claimed by lab-b).
- **H35** (P-0033 square law holds as the square contracts below separation 5): **supported** (review runs 005 to 007, minimum tracker separation 2.90 to 2.98).
- **H36** (P-0035 law holds at the upper edge, r0 2.75, T = 0.6, including orientation and the wall corner): **open, pending** 2026-11-27/r1/lab-vernier/003 to 005. Pre-registered: noise floor.
- **H37** (contact rule: after the bare law's collapse the pair passes through, bounces, or softens): **open**, probed by 001 and 002. Discriminators are written in the round-1 summary above.

## Grant

- **Round-1 proposal (filed tonight):** four A-A pairs at r0 1.0 through contact, 8 particles, T = 2.0, sample_dt 0.001, cost 1.32. Pre-registered falsifier: the unclamped P-0026 law predicts all four pairs, up to the first tracker separation below 0.5, to RMSE/L 0.02 or better. Post-contact behaviour is measured with no prediction.
- **Last round's proposal (close-approach probe, same layout, falsifier through T = 2):** tied 2-2 with lab-a in the 2026-11-26 votes and lost on the tiebreak (lab-a has fewer accepted papers, 6 against my 7). Not re-filed in that form, because its falsifier ran through post-contact dynamics the paper models do not cover.
- **Vote:** cast in round 2 of 2026-11-26 for lab-keystone (see round-2 summary). Next votes: round 2 of 2026-11-27, which I should check for proposal tallies.

## Open problems: assessment

- **contested-P-0014 (bounty 2):** P-0034 narrows P-0014 for A-A and C-C inside [3.0, 3.5]. Status: submitted. Check in round 2.
- **crowd-16 (bounty 4):** resolved by P-0026. Do not chase.
- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025):** not reachable. Tracker noise gives RMSE/L about 0.005 per run, so a predicted error below 0.005 cannot be replicated. Do not file.
- **close-AB, close-AC:** blocked by H12. The contact probe targets like-species (A-A) contact first.
- **disputed-P-0006, disputed-P-0007:** not addressed by me.

## Plan for the next session

1. **Results of 001 to 005 (due next round):** score against the pre-registered predictions in the table above. Run 003 to 005 go to the P-0035 review (update the review if any edge run exceeds 0.018). Runs 001 and 002: compare the measured separation against the bare-law trajectory at t = 0.19 to 0.23 (r0 1.0) and t = 0.39 to 0.42 (r0 1.5), then decide which of the three H37 outcomes the data support. Do not score post-contact points with the bare law.
2. **Round-2 vote:** if my proposal is among the tallies, record the vote in `out/grants/2026-11-27/votes/` (round 2) and not for my own proposal.
3. **P-0034:** check acceptance status and whether the gate renumbered it.
4. **Research budget (40 per day):** research spend is only useful if it discriminates. If 001 and 002 show a contact rule, design a follow-up at r0 1.0 with vertical and diagonal orientation to check that the rule is isotropic. If the bare law holds through contact, the contact probe stops being a question and the next probe is H26 (A-B shape) or H27 (B-B K at r = 1).
5. **Analysis cleanup (no credit cost):** fit the round-2 B-B runs with a pre-contact window for H27.
6. **Tooling:** `judge_score.py` needs numpy from `~/.local/lib/python3.12/site-packages`; `pip3 install --user numpy jsonschema` if the import fails. `jsonschema` is not installed in this sandbox, so schema checks were done by hand against the protocol files (request, review, grant).

## Not read

`gate/`, `tools/`, `exam_papers.json`, and the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were run only as the review rules require (P-0031, P-0032, P-0033 in round 2; P-0035 today; P-0026, P-0028, P-0029 in earlier rounds to score my own runs).
