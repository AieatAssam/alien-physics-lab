# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely, and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-26, round 2 (review filing and grant vote).

## Round 2 summary (2026-11-26)

- **Round-1 review runs scored (all 11 returned, cost 1.02 to 1.16 each, 12.08 of 15 review credits spent; 2.92 left):** every in-domain run sits at the noise floor. Scored with `judge_score.py` (copy in `analysis/`), run with `python3 -I`.
  - **P-0031 (lab-b), 001-004:** RMSE/L 0.00501 to 0.00506; bar 0.021. Nulls 0.018 to 0.040.
  - **P-0033 (lab-keystone), 005-007:** RMSE/L 0.00499 to 0.00504; bar 0.021. Nulls 0.041 to 0.042.
  - **P-0032 (lab-c), 008-011:** RMSE/L 0.00498 to 0.00503; bar 0.018. Nulls 0.014 to 0.021.
- **Reviews filed (out/reviews/):** P-0031 replicated (4 of 4 in-domain runs pass); P-0033 replicated (3 of 3); P-0032 replicated (4 of 4). All evidence cites my own round-1 review ids. No review is near its bar; none is unsupported.
- **Close approach from P-0032 runs (new, relevant to my grant pitch):** in 008 and 011 (T = 0.6, r0 = 2.0) the tracker minimum separation is 0.57 and 0.51. Those minima are noise-biased low; the paper's own predict gives 0.69. The unclamped P-0026/P-0032 law fits to the noise floor through that near-contact at T = 0.6. The contact gap is therefore narrower than my pitch assumed: it is a T > 0.6 or sub-0.5 question, not a sub-2 question. The close-approach grant still tests sub-2 starts at T = 2, where no paper claims anything.
- **Grant vote cast (out/grants/2026-11-26/votes/lab-vernier.json):** voted **lab-keystone** (A-B pair at 2.5, first cross-species test, s = 1 +/- 0.05 falsifier, cost 1.02). Reason: a cheap test of whether mixed pairs reuse the A-A law, which blocks close-AB and H26. Did not vote for my own proposal (rule). Did not vote for Icarus: the scalene N = 3 layout repeats my round-1 run 003 (5.3/6.1/6.9), which already passes.
- **Research (round 2):** none filed. Reason: no discriminating pre-registered run is ready at the 0.007 bar that is not already covered by the grant or by the round-1 reviews. Credits (40) are lost at day end; accepted cost of that choice noted.
- **P-0034 (my round-3 paper, A-A and C-C at 3.0 to 3.5, T <= 1, supersedes P-0014 inside that domain):** still "submitted" in `events.jsonl` (2026-11-25). Not accepted. Not yet renumbered. Check in the next round.

## Pre-registered predictions for the round-1 review runs (kept for the record)

Written before results. Measured results in the table above.

| request | paper | setup | predicted min pair separation | expected RMSE/L if law holds | observed |
|---|---|---|---|---|---|
| 001 | P-0031 | equilateral 5.5, T = 2 | 3.80 | about 0.005 | 0.00503 |
| 002 | P-0031 | equilateral 6.9, T = 2 | 6.12 | about 0.005 | 0.00506 |
| 003 | P-0031 | scalene 5.3/6.1/6.9, T = 2 | 3.82 | about 0.005 | 0.00501 |
| 004 | P-0031 | square 5.02, rot 30, T = 2 | 3.13 | about 0.005 | 0.00502 |
| 005 to 007 | P-0033 | square 5.005, T = 2 | 3.09 | about 0.005 | 0.00499 to 0.00504 |
| 008 | P-0032 | r0 2.0, T = 0.6 | 0.69 | uncertain (main test) | 0.00503 (tracker min 0.57) |
| 009 | P-0032 | r0 2.5, T = 0.6 | 1.81 | about 0.005 | 0.00498 |
| 010 | P-0032 | r0 2.25 diag, T = 0.6 | 1.34 | about 0.005 to 0.01 | 0.00500 |
| 011 | P-0032 | r0 2.0 diag, T = 0.6 | 0.69 | as 008 | 0.00502 (tracker min 0.51) |

Null (zero-force) RMSE/L behaved as predicted for T = 2 (0.02 to 0.04). For T = 0.6 the nulls were 0.014 to 0.021, not all below the bar. Runs 009 and 010 therefore test the law's shape rather than whether a force exists.

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. State which verdict is being made and check the bar for that verdict.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions (4.5, 5.5, ...) for exact-edge domains, or sit a small margin inside the edge. Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling.** The cost is `1 + k * particles * duration`, independent of sample count. Always set `sample_dt = duration / 2000` (the cap).
5. **Pre-contact windows for attractive pairs.** A full-window fit or prediction through a close pass is invalid when the integrator diverges (roughly after separation 0.5 in my own A-A runs at r0 2.5). Scores for my own fits use the window before the first measured separation below 1.5. The judge scores the full run, so check the pre-contact prediction separately when the run closes.
6. **Bars are loose at T <= 0.3 and in general at the 0.007 level.** A constant-K versus table-K difference of 1 to 3 percent moves predicted positions by only about 0.001 to 0.003 RMSE/L, far below the 0.021 bar. Falsification needs a regime change: close approach, long time, N, or a new pair.
7. **Label K by the window's mean separation**, not by the start separation.
8. **Judge domain excludes duration, but predictors do.** Several predictors refuse durations outside their window (P-0024, P-0028 T > 1.0, P-0029: T > 2 for r0 < 7 and T > 3 for r0 >= 7; P-0031 T > 2; P-0032 T > 0.6). A refused run cannot be scored, so it is not cited as evidence.
9. **Write only under `out/`.** Analysis code is in `out/labs/lab-vernier/analysis/`. The older source folder `labs/lab-vernier/analysis/` is read-only reference.
10. **Pre-register before results.** Predictions for each new run are written in this notebook before its results are read.
11. **Asymmetric layouts are in the judge domain but not in a paper's claim** when the claim says so. A miss there is a "narrowed" verdict, not a falsification, unless the paper's stated scope includes them.
12. **Do not vote for own proposal; vote on information value.** Pick the proposal whose result would move the most hypotheses; note redundancy with my own runs.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result. Independent of `sample_dt`. Examples: 2 particles at T = 0.6 costs 1.024; 2 at T = 1 costs 1.04; 4 at T = 2 costs 1.16; 8 at T = 2 costs 1.32; 16 at T = 1 costs 1.32; 16 at T = 3 costs 1.96.

Review budget on 2026-11-26: 15 allowed, 12.08 spent in round 1 (research and grant spending are separate), 2.92 left after round-1 review runs.

## Results and analysis

### Review runs (round 1 of 2026-11-26), new this session

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

Scripts: `analysis/minsep_round1_review_2026-11-26.py` (closest approach and wall clearance from result files), `judge_score.py` (judge scorer).

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

Runs 006, 007 (A-A) and 012, 013 (C-C) at r0 2.5 reach separations of 0.02 to 0.6 within T = 1. Predictions diverge there (RMSE/L in the hundreds; integrator has no contact model). Excluded from all claims. The P-0032 review runs (008, 011) show the unclamped law holds through near-contact at T = 0.6, which suggests the earlier divergence comes from the T = 1 integration after contact, not from the law at contact. Not tested beyond T = 0.6.

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

- **P-0034** (round 3, A-A and C-C at 3.0 to 3.5, T <= 1, supersedes P-0014 inside that domain). Claims P-0034-c1 (A-A), P-0034-c2 (C-C); domain r_range [3.0, 3.5], max_particles 2; predicted error 0.007. Status: **submitted** (2026-11-25), not accepted at the time of this round.
- **P-0030** (round 1, A-C at 2.5 to 3.5; predicted error 0.008). Not P-0029, which is lab-a's A-A table.
- **Standing reviews (mine):** P-0012, P-0017, P-0024 (replicated, round 1); P-0028 (replicated, round 1); P-0026 (replicated, 2026-11-24); P-0029 (replicated, round 3); **P-0031, P-0033, P-0032 (replicated, filed round 2 of 2026-11-26)**.

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
- **H13** (pairwise superposition, N > 2): supported at N = 16, T = 1; and at N = 3, 4 for the P-0031 and P-0033 layouts (round-2 review runs, as well as lab-b's and lab-keystone's own evidence).
- **H15** (P-0004-c2 magnitude): consistent with P-0030 at 2.5 to 3.5.
- **H16** (contact failure, close approach): **narrowed.** The unclamped P-0032 law fits to noise at T = 0.6 with tracker minimum separations of 0.51 to 0.57 (paper prediction 0.69). Beyond T = 0.6 and for sub-0.5 contact: still open. The grant probe tests sub-2 starts at T = 2.
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

## Grant

- **Tonight's proposal (mine, round 1):** close-approach probe, four A pairs at rest, initial separation 1.0, pair centres 5 apart, T = 2, 8 particles, 1.32 credits. Pre-registered falsifier: the unclamped P-0026 law predicts all four pairs to RMSE/L 0.02 or better through T = 2. A miss marks the contact gap and is reported as a measurement first.
- **Outcome:** not known until the round-2 votes are tallied. If it wins, the 120 credits go to the grant account, usable in round 3. Before filing that run, write the prediction (including pair coupling through the tables) into this notebook.
- **Caveat from the review runs:** T = 2 with sub-0.6 contact is now less novel than the pitch implied. Keep the falsifier unchanged; expect the probe to be dominated by what happens after contact (the integrator has no contact model).
- **Vote cast:** lab-keystone (see round 2 summary).

## Open problems: assessment

- **contested-P-0014 (bounty 2):** P-0034 narrows P-0014 for A-A and C-C inside [3.0, 3.5]. Status: submitted. Check in round 3.
- **crowd-16 (bounty 4):** resolved by P-0026. Do not chase.
- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025):** not reachable. Tracker noise gives RMSE/L about 0.005 per run, so a predicted error below 0.005 cannot be replicated. Do not file.
- **close-AB, close-AC:** blocked by H12. The close-approach grant targets like-species contact first.
- **disputed-P-0006, disputed-P-0007:** not addressed by me.

## Plan for the next session

1. **Round 3 grant:** if the close-approach probe wins, pre-register the prediction in this notebook, then file the grant run (8 particles, T = 2). If it does not win, skip it.
2. **P-0034:** check acceptance status and whether the gate renumbered it. If accepted, consider whether any of my later runs can test its edge (A-A or C-C at 3.0 to 3.5 with T > 1 is outside its domain, so that is not a test of the claim).
3. **Research budget (40 per day):** no pre-registered discriminating run is ready at the 0.007 bar. Candidates for a future round: H27 (B-B K at r = 1, needs a pre-contact fit of the round-2 B-B runs first, which costs no credits), H26 (A-B shape, competes with the Keystone grant), and a T > 0.6 test of the P-0032 law at contact (not yet designed).
4. **Analysis cleanup (no credit cost):** fit the round-2 B-B runs with a pre-contact window for H27.
5. **Tooling:** `judge_score.py` needs numpy from `~/.local/lib/python3.12/site-packages`; `pip3 install --user numpy jsonschema` if the import fails. The schema check was not run this round (jsonschema not installed); the review and vote files were checked by hand against their schemas.

## Not read

`gate/`, `tools/`, `exam_papers.json`, and the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were run only as the review rules require (P-0031, P-0032, P-0033 for the reviews this round; P-0026, P-0028, P-0029 in earlier rounds to score my own runs).
