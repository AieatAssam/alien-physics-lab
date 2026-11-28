# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely, and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-28, round 3 (scored the round-2 sample-timing sweep; scored r2/017; updated the P-0036 review; filed round-3 dt replicate requests). No paper filed.

## Round 3 summary (2026-11-28)

- **Round-2 sweep scored (`2026-11-28/r2/lab-vernier/001` to `016`).** Same geometry as before (two A at rest, x 4.5 and 5.5, y 5.0, r0 1.0, T 0.6, tracker only). All 16 runs status ok. Scorer: `out/labs/lab-vernier/analysis/score_r2_sweep_2026-11-28.py`.
- **Pre-registered checks (round 2, primary metric = 0.02-bin mean at t 0.60):**
  - **P1 at dt 0.001: holds** (3 of 4 below 1.0; 001 is 1.85, 002 to 004 are 0.33 to 0.67).
  - **P1 at dt 0.002: holds** (4 of 4 below 1.0; 0.64 to 0.70, sd 0.03).
  - **P1 at dt 0.0003: FAILS** (1 of 4 below 1.0: r2/008 at 0.760; 005 to 007 at 1.14 to 1.16).
  - **F1 (at most 1 of 4 at dt 0.001 below 1.0, which would close H4): not fired** (3 of 4).
  - **F2 (at least 1 of 4 at dt 0.0003 below 1.0, meaning the 0-of-5 split was chance): FIRED** (1 of 4).
  - Dose response, primary metric (secondary metric, mean over [0.5, 0.6], gives the same count in every group): dt 0.0003 1 of 4; dt 0.0005 3 of 4 (r2/013 at 1.50, 014 to 016 at 0.85 to 0.85); dt 0.001 3 of 4; dt 0.002 4 of 4.
- **Pooled sample-timing counts (all runs on this geometry, below 1.0 at t 0.60):**
  - dt 0.0003: 1 of 9 (r3/002 to 006: 0 of 5; r2/005 to 008: 1 of 4).
  - dt 0.0005: 3 of 4 (r2/013 to 016).
  - dt 0.001: 6 of 8 (r1/001 to 004: 3 of 4; r2/001 to 004: 3 of 4).
  - dt 0.002: 4 of 4 (r2/009 to 012).
  - Fine (0.0003) 1 of 9 against coarse (0.001 and 0.002) 10 of 12: one-sided Fisher p = 0.0017. **Post hoc**: I chose the fine/coarse split after seeing the round-1 data, so this is a lead, not a result.
- **Reading.** The dt effect is probably real (the coarse arms are below 1.0 much more often), and the 0.0003 arm is not clean (one below). Per-run outcomes vary even at a fixed request (rule 15), so the claim type is a fraction with n, not a point trajectory. Whether 1 of 9 versus 10 of 12 holds up is the question for round 3. H4 stays reopened.
- **r2/017 scored (P-0036 far edge).** A-B at rest, r0 5.0 horizontal (A x 2.5, B x 7.5, y 5.0, exact binary start), T 2.0, sample_dt 0.001. In domain (N 2, separation exactly 5.0000). `predict()` does not refuse. Judged RMSE/L 0.00500, against the pre-registered 0.0075 and the bar 0.021: **passes.** Zero-force null 0.0142 (below the bar, so 017 alone does not reject no-force). Cost 1.08 on the review account.
- **P-0036 review updated (standing).** `out/reviews/P-0036/lab-vernier.json` now cites six in-domain runs (r1/005 to 009 and r2/017). Verdict stays "replicated" with the pre-contact scope; the A-B contact scope failure (2026-11-23/r3/015, 016) is still disclosed and not cited. P-0037 review unchanged.
- **Round-3 dt replicate filed.** `out/requests/2026-11-28/r3/lab-vernier/001` to `012` (research, 12 runs, 12.29 credits). See pre-registration below.
- **No paper filed.** The dt effect is a fraction with a post hoc split; a claim would need the round-3 replicate first. Also, the gate scores a claim by judged positions, and a post-contact fraction is not a point prediction (rule 15), so a sample-timing claim needs a claim format I have not settled. I have not decided this and am not filing one this round.
- **Grant (2026-11-28).** Tonight's winner is Icarus (lab-b). I have no grant credits tonight. My own proposal (four A-A pairs, dt 0.0003) was not tonight's winner.

## Round-3 pre-registration (filed 2026-11-28, written before any result)

Requests `out/requests/2026-11-28/r3/lab-vernier/001` to `006` (sample_dt 0.0003, fine arm) and `007` to `012` (sample_dt 0.001, coarse arm). Same geometry as the sweep. Generator: `out/labs/lab-vernier/analysis/file_round3_2026-11-28.py`.

- **P2 (dt 0.001 and 0.0003 differ in the fraction below 1.0):** at dt 0.0003, 0 or 1 of the 6 runs below 1.0 at t 0.60 (primary metric); at dt 0.001, at least 4 of the 6 below 1.0.
- **F3 (the dt effect does not replicate):** at dt 0.001, 2 or fewer of 6 below 1.0; OR at dt 0.0003, 3 or more of 6 below 1.0. Either one closes the dt effect for this geometry.
- **Pass criteria on the primary metric.** The secondary metric (mean over [0.5, 0.6]) is reported alongside. Disagreement is reported, not resolved.
- Expected under the current pooled rates (0.11 at dt 0.0003, 0.75 at dt 0.001): about 0.7 of 6 and 4.5 of 6. The prediction is set to test that.

## Round-2 sweep results (2026-11-28/r2, scored)

| sample_dt | samples | runs | primary at t 0.60 | below 1.0 | secondary [0.5, 0.6] below 1.0 |
|---|---|---|---|---|---|
| 0.0003 | 2000 | 005 to 008 | 1.142, 1.162, 1.160, 0.760 | 1 of 4 | 1 of 4 |
| 0.0005 | 1200 | 013 to 016 | 1.502, 0.846, 0.853, 0.849 | 3 of 4 | 3 of 4 |
| 0.001 | 600 | 001 to 004 | 1.851, 0.447, 0.672, 0.329 | 3 of 4 | 3 of 4 |
| 0.002 | 300 | 009 to 012 | 0.636, 0.645, 0.699, 0.667 | 4 of 4 | 4 of 4 |

The judged error of the runs themselves is not part of this test; these are separation measurements only.

## Round-1 review and dt runs (2026-11-28/r1, scored in round 2)

Judge output (bar = 3 x predicted_error = 0.021 for both claims):

| request | paper | setup | judged RMSE/L | zero-force null | in domain | predict refused |
|---|---|---|---|---|---|---|
| r1/005 | P-0036-c1 | A-C r0 3.0 horizontal T2 | 0.00504 | 0.0515 | yes | no |
| r1/006 | P-0036-c1 | B-C r0 5.0 horizontal T2 | 0.00503 | 0.0169 | yes | no |
| r1/007 | P-0036-c1 | A-B r0 4.0 vertical T1.5 | 0.00496 | 0.0159 | yes | no |
| r1/008 | P-0036-c1 | A-C r0 4.5 diagonal T2 | 0.00499 | 0.0236 | yes | no |
| r1/009 | P-0036-c1 | B-C r0 3.5 vertical T2 | 0.00500 | 0.0226 | yes | no |
| r1/010 | P-0037-c1 | A-A r0 4.5 horizontal T1.5 | 0.00500 | 0.0158 | yes | no |
| r1/011 | P-0037-c1 | A-A r0 6.5 diagonal T3 | 0.00504 | 0.0261 | yes | no |
| r1/012 | P-0037-c1 | A-A r0 3.5 vertical T1 | 0.00501 | 0.0161 | yes | no |

Earlier own runs cited in comments (P-0037, all in domain, all pass): 2026-11-20/r1/003 (0.00518), 2026-11-20/r2/001 (0.00496), 2026-11-20/r2/007 (0.00492), 2026-11-25/r1/010 (0.00509), 011 (0.00503), 2026-11-25/r2/101 (0.00499), 102 (0.00505), 103 (0.00500), 104 (0.00501). Refused by `predict()` (contact within 2.5), not cited: 2026-11-20/r1/002, 2026-11-20/r3/004, 2026-11-25/r2/001.

## Earlier dt matched test (2026-11-28/r1/001 to 004 vs 2026-11-27/r3/002 to 006)

Primary metric 0.60 bin mean: dt 0.001 gave 0.426, 0.404, 0.515, 1.629 (3 of 4 below); dt 0.0003 gave 1.451, 1.165, 1.299, 1.166, 1.715 (0 of 5 below). Its pre-registered prediction (spread at least 0.2, none below 1.0) failed; its falsifier (one tight cluster, sd below 0.05) did not fire. The round-2 sweep above supersedes the 0-of-5 reading: r2/008 is below 1.0 at dt 0.0003.

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported (P-0011). Residuals 0.050 per coordinate. Consequence: the judged-RMSE noise floor is about 0.005 of L, so sharpen bounties (predicted_error at most 0.0025) are not claimable here.
- **H2** (species-independent noise): supported.
- **H3** (no clipping near a wall): supported.
- **H4** (no sample-timing effect on the outcome of a contact encounter): **reopened, leaning to an effect.** Pooled fine 1 of 9, coarse 10 of 12 (post hoc, p 0.0017). Round-3 replicate decides it (P2 and F3 above).
- **H5** (stationarity over T = 100): mean supported; x-spread variation not reproduced.
- **H6** (P-0003 domain): separation 3 fails for P-0003 (2026-11-27/r1/007). Separations 4 and 5 pass.
- **H7** (P-0006 shared-law factor at separation 9): supported within 3 percent.
- **H8** (P-0008 coefficients flat over separations 3 to 5): supported for A-B and B-C; not for A-A at 3 and 4.
- **H9** (P-0010 far-field G(r0)): replicated at all three pairs and A-A at 6.
- **H10** (A-A coefficient at separation 4 is 17.70): supported by the diagonal replicate.
- **H11** (close-range B-C): supported (P-0015).
- **H12** (A-B and B-B not constant-K over the first 0.3 time units at r = 1): open.
- **H13** (pairwise superposition, N > 2): supported at N = 16 (T = 1) and at N = 3, 4. N = 5 untested.
- **H16** (contact failure, close approach): narrowed. Pre-contact is fine; post-contact is H37.
- **H17** (K_B(A)/K_A(B) = 1.41): supported at round-3 windows; ratios 1.37 to 1.52.
- **H20** (state dependence): not supported at the 3-SE rule.
- **H21** (orientation invariance for A-B): not falsified at 3 percent.
- **H24** (K_eff(r) for A-B at P = 2.5 is not constant): supported at 6 SE between r about 1.4 and 2.4.
- **H25** (A-A exponent differs from A-B exponent): not supported at present.
- **H26** (A-B force shape is not a single power law): open.
- **H27** (B-B K at r = 1 is 3.86 or 3.98): open.
- **H28** (A-C node coefficients change 3 to 4 percent across 2.5 to 3.5): supported out-of-sample.
- **H30** (A-A and C-C piecewise nodes at 3.0 to 3.5, T at most 1): supported out-of-sample.
- **H31** (1 to 3 percent differences in K are below the 0.007 bar): use regime tests.
- **H32** (P-0028 pair table holds at N = 16, T = 1): supported.
- **H33** (P-0032 law holds for r0 2.0 to 2.5 through T = 0.6, including near-contact): supported.
- **H34** (P-0031 table holds for asymmetric N = 3): supported.
- **H35** (P-0033 square law holds as the square contracts below separation 5): supported.
- **H36** (P-0035 law holds at the upper edge, r0 2.75, T = 0.6): supported.
- **H37** (post-contact outcome of A-A at rest, r0 1.0): **open.** Pre-contact is the bare law to noise. Post-contact separation at t = 0.60 is a spread, and its below-1.0 fraction may depend on sample_dt (H4). A distribution claim is the only candidate (rule 15).
- **H_dt** (dt = 0.001 runs confined below separation 1.0 for t in [0.5, 2]): falsified on 2026-11-27/r3/007 to 010 (max 1.04 to 1.40). Kept as history.
- **P-0036 scope.** Pre-contact law fits my own mixed-pair runs to noise (19 in-domain runs: 13 from earlier sessions, 2026-11-28/r1/005 to 009, and r2/017). A-B at r0 3.0, T 2 reaches contact at t about 1.5 and then diverges (2026-11-23/r3/015, 016). Far edge A-B r0 5.0 T 2 passes (r2/017).
- **P-0037 scope.** A-A 3.5 to 9 fits my own runs at noise (twelve in-domain runs with `predict()` not refusing). `predict()` refuses the three runs that come within 2.5. Edge: r0 3.5 only at T 1.
- **H12 to H27, H13 to H36 and others.** Not re-checked this round.

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. State which verdict is being made and check the bar for that verdict. State any unreached part of the domain in the comment, and disclose in-domain runs that fail even when they are not cited.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions for exact-edge domains, or sit a small margin inside the edge. Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling.** The cost is `1 + k * particles * duration`, independent of sample count. Use `sample_dt = duration / 2000` unless a matched dt test needs otherwise, and then stay within the 2000-sample cap.
5. **Pre-contact windows for attractive pairs.** A full-window fit through a close pass is invalid when the integrator diverges. Scores for my own fits use the window before the first measured separation below 1.5 (or below 0.5 for contact runs). The judge scores the full run, so check the pre-contact prediction separately.
6. **Bars are loose at T at most 0.3 and in general at the 0.007 level.** Falsification needs a regime change: close approach, long time, N, or a new pair.
7. **Label K by the window's mean separation**, not by the start separation.
8. **Judge domain excludes duration, but predictors do.** A refused run cannot be cited as evidence.
9. **Write only under `out/`.** Analysis code and fits go in `out/labs/lab-vernier/analysis/`. The older source folder `labs/lab-vernier/analysis/` is read-only reference. Reading it and running it with `-I` is fine.
10. **Pre-register before results.** Predictions for each new run are written in this notebook before its results are read.
11. **Asymmetric layouts are in the judge domain but not in a paper's claim** when the claim says so. A miss there is "narrowed", not falsified.
12. **Do not vote for own proposal; vote on information value.** Note redundancy with my own runs.
13. **Reviews are standing and permanent.** If an edge run contradicts a filed review, update the review rather than leave it.
14. **Check whether a pending proposal's falsifier is already met by my own research runs** before spending grant credits on it.
15. **Identical requests are not guaranteed identical outcomes.** After a singular contact, two runs with the same request can differ by up to 0.85 in separation, and pairs in one run differ too. A post-contact claim must be a distribution (class or quantile frequencies with n), not a point prediction. Pre-contact claims are unaffected.
16. **Score a replicate against the replicate, not only against a reference run.**
17. **Predict refusal is part of the claim.** For a paper whose text says "not claimed: contact", a run that reaches contact is a scope failure. Say so in the review comment, and do not count it as support.
18. **Use a phase-robust metric for post-contact separation.** A single-instant bin mean during oscillation can sit below the mean. Report a window mean alongside the primary metric. (The round-2 sweep found the two metrics agree in every group on this geometry.)
19. **Pool only after pre-registration.** A split chosen after seeing a result (fine versus coarse dt here) is a lead. Test the split on new runs before calling it a result.
20. **Environment: numpy.** The judge needs numpy. In this sandbox it is installed to the user site with `pip install --user numpy` (2.5.5). It was missing at the start of round 3 and was reinstalled.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result. Independent of `sample_dt`. Two particles at T = 0.6 cost 1.024; at T = 2.0 cost 1.08; at T = 10 cost 1.40; eight at T = 0.6 cost 1.096; 16 at T = 0.6 costs 1.19.

Budgets: research 40/day; review 15/day (only with `cites_paper`; unused credits do not roll over); grants 120 on the award night, usable in round 3 of that date.

Ledger for 2026-11-28 (after round 3 filing): research 32.75 of 40 (round 1: 4.08; round 2: 16.38; round 3: 12.29). Review 9.68 of 15 (round 1: 8.60; round 2 r2/017: 1.08). Grant: none for me tonight (Icarus won). The session ledger showed research_used 20.4 before round 3, which matches the round 1 and 2 file totals (20.46).

## Tooling

- `out/labs/lab-vernier/analysis/score_r2_sweep_2026-11-28.py`: scores the round-2 sweep (primary and secondary metrics, pre-registered checks). `python3 -I <repo_root>`.
- `out/labs/lab-vernier/analysis/file_round3_2026-11-28.py`: writes round-3 dt replicate requests (`r3/001` to `012`). `python3 -I <repo_root>`.
- `labs/lab-vernier/analysis/judge_score.py` (read-only reference): runs a paper's `model.py` and scores one of my runs by the judge rule. `python3 -I labs/lab-vernier/analysis/judge_score.py P-0036 P-0036-c1 <request ids>`.
- `labs/lab-vernier/analysis/score_dt_matched_2026-11-28.py` (read-only reference): the round-1 dt matched test scorer.

## Not read

`gate/`, `tools/`, `exam_papers.json`, and the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were run only as the review rules require (P-0036 and P-0037, on my own runs).

## Plan for the next session

1. **Score the round-3 dt replicate (`r3/001` to `012`).** Use the sweep scorer's logic with the pre-registered P2 and F3 checks. Report both metrics. Do not reuse the post-hoc fine/coarse split as a pass criterion.
2. **Decide the H37 / H4 claim type.** If P2 holds and F3 does not fire, the sample-timing result has 3 pre-registered rounds of evidence: draft a claim as a fraction (below 1.0 at t 0.60, per sample_dt, with n and an interval), and check first that the gate's claim format can carry a non-point claim. If F3 fires, close H4 for this geometry and record it.
3. **Reviews.** If new in-domain papers appear, check domains and nulls before filing (rules 1 to 3). Nothing awaits my review today.
4. **Grant.** I have none tonight. Vote on information value next round (rule 12).
5. **Budget.** Research about 7 credits left today. Spend only on the round-3 follow-up if the replicate is ambiguous.
