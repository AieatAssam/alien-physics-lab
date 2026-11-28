# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely, and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-28, round 2 (scored round-1 review runs and the dt matched test; filed reviews for P-0036 and P-0037; filed round-2 requests; voted on the grant).

## Round 2 summary (2026-11-28)

- **Reviews filed (standing).**
  - **P-0036 (lab-a, mixed pairs): replicated** (pre-contact scope). Five cited in-domain runs (2026-11-28/r1/lab-vernier/005 to 009) all sit at judged RMSE/L 0.00496 to 0.00504 against the bar 0.021. Disclosed scope failure: 2026-11-23/r3/lab-vernier/015 and 016 (A-B, r0 3.0, T 2) are in domain by the judge rule and `predict()` does not refuse them. The pair reaches separation 0.2 to 0.3 near t 1.5 and crosses; judged error 3.88. Suggested fix in the review: refuse below contact, or add an exclusion.
  - **P-0037 (lab-keystone, A-A 3.5 to 9): replicated.** Three cited runs (2026-11-28/r1/lab-vernier/010 to 012) at 0.00500 to 0.00504. The zero-force null is above the bar only for 011, so 010 and 012 alone do not reject no-force. The fit is the replication.
  - Files: `out/reviews/P-0036/lab-vernier.json`, `out/reviews/P-0037/lab-vernier.json`.
- **dt matched test (2026-11-28/r1/001 to 004, sample_dt 0.001, same geometry as 2026-11-27/r3/002 to 006 at 0.0003).** The pre-registered prediction FAILED. The falsifier (one tight cluster, sd < 0.05) did not fire.
  - dt 0.001 at t = 0.60 (0.02-bin mean): 0.426, 0.404, 0.515, 1.629. **Three of four are below 1.0.**
  - dt 0.0003 at t = 0.60 (r3/002 to 006): 1.451, 1.165, 1.299, 1.166, 1.715. **None below 1.0.**
  - Run-level Fisher test, one-sided: 3/4 vs 0/5 gives p about 0.05. Small n; the r3/001 grant (dt 0.001, four pairs, one run) also has all four pairs below 1.0 at t = 0.60 (0.39 to 0.54). Those pairs are not independent of each other.
  - **Consequence.** H4 (sample timing does not matter) is reopened, not closed. The dt 0.001 runs give post-contact separation mostly below 1.0 and the dt 0.0003 runs give 1.17 to 1.72. Whether this is a sample-grid effect or chance is what the round-2 sweep tests (below).
- **Round-2 grant vote:** lab-c (Nullius). See "Grant" below.
- **Budget.** Research: 4.08 spent today (round 1) plus 16.38 filed this round (`r2/001` to `016`) = 20.46 of 40. Review: 8.60 spent today (`r1/005` to `012`) plus 1.08 (`r2/017`) = 9.68 of 15. Grant: no proposal award today (2026-11-28 allowance 0; the 2026-11-27 award was 120, used 1.32 in round 3 of that date).
- **No paper filed.** The dt effect is not yet a solid claim (the round-2 sweep is needed first). The review-level results are already in the reviews.

## Round-1 review and dt runs, scored (2026-11-28/r1)

Tools: `out/labs/lab-vernier/analysis/judge_score.py` (a copy of `labs/lab-vernier/analysis/judge_score.py`) and `out/labs/lab-vernier/analysis/score_dt_matched_2026-11-28.py`. numpy installed to the user site (`pip install --user numpy`, 2.5.5). Run with `python3 -I`.

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

## dt matched test, 2026-11-28/r1/001 to 004 vs 2026-11-27/r3/002 to 006 (geometry: A-A at rest, x 4.5 and 5.5 (r0 1.0), y 5.0, T 0.6)

Primary metric: 0.02-bin mean separation at t = 0.60. (The primary metric is a single instant during oscillation, so the round-2 sweep also reports a phase-robust secondary metric: the mean separation over t in [0.5, 0.6].)

| dt | runs | separation at t = 0.60 | below 1.0 |
|---|---|---|---|
| 0.001 | r1/001 to 004 | 0.426, 0.404, 0.515, 1.629 | 3 of 4 |
| 0.0003 | r3/002 to 006 | 1.451, 1.165, 1.299, 1.166, 1.715 | 0 of 5 |

Pre-registered (round 1, 2026-11-28): (a) the dt 0.001 runs spread over at least 0.2, with one run in each band and none below 1.0. **Result: spread 1.22, but three runs below 1.0. Prediction fails.** (b) Falsifier: all four dt 0.001 runs in one cluster (sd < 0.05) that differs from dt 0.0003. **Result: sd 0.59, not fired.**

## Round-2 pre-registration (filed 2026-11-28, written before any result)

Requests `out/requests/2026-11-28/r2/lab-vernier/001` to `016` (research, 16 runs at 1.024 each): the same geometry as r1/001 (two A at rest, x 4.5 and 5.5, y 5.0, T 0.6, tracker only), at four sample_dt values, four runs each.

| requests | sample_dt | samples | purpose |
|---|---|---|---|
| 001 to 004 | 0.001 | 601 | replicate of r1/001 to 004 (is the 3-of-4 base rate reproducible?) |
| 005 to 008 | 0.0003 | 2000 | replicate of r3/002 to 006 |
| 009 to 012 | 0.002 | 301 | new dt level |
| 013 to 016 | 0.0005 | 1201 | new dt level |

- **Prediction P1 (sample_dt controls the contact outcome):** at dt 0.001 and at dt 0.002, at least 3 of the 4 new runs each are below 1.0 at t = 0.60 (primary metric). At dt 0.0003, 0 of the 4 new runs are below 1.0.
- **Falsifier F1 (the 3-of-4 result was chance; no dt effect at 0.001):** at most 1 of the 4 new dt 0.001 runs is below 1.0 at t = 0.60. If that holds, H4 is closed for this geometry (per-run variation only).
- **Falsifier F2 (no dt effect at 0.0003 either):** at least 1 of the 4 new dt 0.0003 runs is below 1.0. Then the 0-of-5 split was chance.
- **Dose-response points (no prediction):** dt 0.0005 is reported as a point between 0.0003 and 0.001. Report the fraction below 1.0 and the secondary metric for every dt.
- **Pass criteria are on the primary metric. The secondary metric (mean over [0.5, 0.6]) is reported alongside. A disagreement between the two is reported, not resolved.**

Review run `out/requests/2026-11-28/r2/lab-vernier/017` (review account, cites P-0036, cost 1.08): A-B at rest, r0 5.0 horizontal (A x 2.5, B x 7.5, y 5.0), T 2.0, sample_dt 0.001.
- **Pre-registered:** in domain, `predict()` does not refuse, judged error at most 0.0075 (noise floor 0.005). The paper model predicts the pair drifts from 5.0 to about 4.18 by t = 2.0 (no contact; minimum separation 4.18 at t = 2.0). Falsifier: judged error above 0.021 (bar), or a contact that `predict()` does not refuse.

## Grant

- **Tonight's grant, my proposal (not voted on by me).** Four A-A pairs at r0 1.0, post-contact sample-timing test at sample_dt 0.0003, T 0.6 (eight particles; the r3/001 geometry). File: `out/grants/2026-11-28/proposals/lab-vernier.json`. Cost 1.096. Its pre-registration was: each pair's smoothed separation (0.02 bins) at t ≤ 0.6 matches r3/001 (dt 0.001) to 0.05 or better. The round-2 sweep now tests the dt question more directly (single pairs, replicated, four dt values). If the proposal is awarded in round 3, the four-pair run is worth doing only if the sweep does not already settle the dt question. Re-check before filing.
- **Round-2 vote: lab-c (Nullius).** `out/grants/2026-11-28/votes/lab-vernier.json`. Reason: the proposal tests whether sample_dt sets the contact outcome (directly the H4 question my dt runs raise), it costs 1.4, and it is not one of my runs. Other proposals considered: Keystone's four-body additivity test (weak discriminating power: a scale fit at sigma 0.05, so a pass at scale 1 is not much evidence), Icarus's N = 16 asymmetric grid (N = 16 additivity was already supported in my 2026-11-25 run at T 1, so partly redundant), and Plumbline's full-chamber run (cost 33, prediction not claimed; the early-time falsifier is useful but the run is expensive).

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported (P-0011). Residuals 0.050 per coordinate. Consequence: the judged-RMSE noise floor is about 0.005 of L, so sharpen bounties (predicted_error ≤ 0.0025) are not claimable here.
- **H2** (species-independent noise): supported.
- **H3** (no clipping near a wall): supported.
- **H4** (no sample-timing effect on the outcome of a contact encounter): **reopened** (2026-11-28). dt 0.001 gives 3 of 4 below 1.0 at t = 0.60; dt 0.0003 gives 0 of 5. Round-2 sweep (P1, F1, F2 above) decides it.
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
- **H30** (A-A and C-C piecewise nodes at 3.0 to 3.5, T ≤ 1): supported out-of-sample.
- **H31** (1 to 3 percent differences in K are below the 0.007 bar): use regime tests.
- **H32** (P-0028 pair table holds at N = 16, T = 1): supported.
- **H33** (P-0032 law holds for r0 2.0 to 2.5 through T = 0.6, including near-contact): supported.
- **H34** (P-0031 table holds for asymmetric N = 3): supported.
- **H35** (P-0033 square law holds as the square contracts below separation 5): supported.
- **H36** (P-0035 law holds at the upper edge, r0 2.75, T = 0.6): supported.
- **H37** (post-contact outcome of A-A at rest, r0 1.0): **open.** Pre-contact is the bare law to noise. Post-contact separation at t = 0.60 is a spread (1.17 to 1.72 at dt 0.0003; 0.40 to 0.52 in three of four dt 0.001 runs, and 1.63 in the fourth). A distribution claim is the only candidate (Standing rule 15), and it depends on H4.
- **H_dt** (dt = 0.001 runs confined below separation 1.0 for t in [0.5, 2]): falsified on 2026-11-27/r3/007 to 010 (max 1.04 to 1.40). Kept as history.
- **P-0036 scope (new).** Pre-contact law fits my own mixed-pair runs to noise (18 in-domain runs: 13 from earlier sessions plus 2026-11-28/r1/005 to 009). A-B at r0 3.0, T 2 reaches contact at t about 1.5 and then diverges (2026-11-23/r3/015, 016). Far-edge A-B at r0 5.0, T 2: run 2026-11-28/r2/017 pending.
- **P-0037 scope (new).** A-A 3.5 to 9 fits my own runs at noise (twelve in-domain runs with `predict()` not refusing). `predict()` refuses the three runs that come within 2.5. Edge: r0 3.5 only at T 1.

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. State which verdict is being made and check the bar for that verdict. State any unreached part of the domain in the comment, and disclose in-domain runs that fail even when they are not cited.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions for exact-edge domains, or sit a small margin inside the edge. Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling.** The cost is `1 + k * particles * duration`, independent of sample count. Use `sample_dt = duration / 2000` unless a matched dt test needs otherwise, and then stay within the 2000-sample cap.
5. **Pre-contact windows for attractive pairs.** A full-window fit through a close pass is invalid when the integrator diverges. Scores for my own fits use the window before the first measured separation below 1.5 (or below 0.5 for contact runs). The judge scores the full run, so check the pre-contact prediction separately.
6. **Bars are loose at T ≤ 0.3 and in general at the 0.007 level.** Falsification needs a regime change: close approach, long time, N, or a new pair.
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
18. **Use a phase-robust metric for post-contact separation.** A single-instant bin mean during oscillation can sit below the mean. Report a window mean alongside the primary metric.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result. Independent of `sample_dt`. Two particles at T = 0.6 cost 1.024; at T = 2.0 cost 1.08; at T = 10 cost 1.40; eight at T = 0.6 cost 1.096; 16 at T = 0.6 costs 1.19.

Budgets: research 40/day; review 15/day (only with `cites_paper`; unused credits do not roll over); grants 120 on the award night, usable in round 3 of that date.

Ledger for 2026-11-28 (after round 2 filing): research 20.46 of 40 (round 1: 4.08; round 2: 16.38); review 9.68 of 15 (round 1: 8.60; round 2: 1.08); grant: no award today.

## Tooling

- `out/labs/lab-vernier/analysis/file_round2_2026-11-28.py`: writes this round's requests (`r2/001` to `017`) and the grant vote. Run with `python3 -I`.
- `out/labs/lab-vernier/analysis/score_dt_matched_2026-11-28.py`: scores the dt matched test (r1/001 to 004 against r3/002 to 006) with the pre-registered checks. Run with `python3 -I`.
- `labs/lab-vernier/analysis/judge_score.py` (read-only reference): runs a paper's `model.py` and scores one of my runs by the judge rule. Usage in its docstring; `python3 -I labs/lab-vernier/analysis/judge_score.py P-0036 P-0036-c1 <request ids>`. numpy is in the user site.
- Older analysis (read-only reference): `labs/lab-vernier/analysis/score_r3_contact_2026-11-28.py`, `scan_inscope_2026-11-28.py`, `p0036_ab_fall_2026-11-28.py`, `file_round1_2026-11-28.py`.

## Not read

`gate/`, `tools/`, `exam_papers.json`, and the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were run only as the review rules require (P-0036 and P-0037, on my own runs).

## Plan for the next session

1. **Score the round-2 sweep (`r2/001` to `016`).** Use `score_dt_matched_2026-11-28.py` extended with the phase-robust metric (mean over [0.5, 0.6]). Decide P1, F1, F2 against the pre-registration above. Report the dt 0.0005 and 0.002 points.
2. **Score `r2/017` (P-0036, A-B r0 5.0, T 2).** If in domain and within 0.0075, add `2026-11-28/r2/lab-vernier/017` to the P-0036 review as evidence (review file is standing; update it, Standing rule 13). If it contacts, record that as scope evidence and update the comment.
3. **Decide the H37 claim type after the sweep.** If dt matters (P1 holds), publish a sample-timing claim first: the fraction of A-A r0 1.0 runs below separation 1.0 at t = 0.60, as a function of sample_dt, with n and an interval. If dt does not matter (F1 holds), publish a distribution claim for post-contact separation at t = 0.60 with n and quantiles.
4. **Grant (if awarded and it wins its vote):** re-check whether the sweep already settles the dt question before filing the four-pair run (Standing rule 14).
5. **Vote on info value next round.** Nullius's long-run contact check (lab-c) answers whether coarse steps matter over T = 10; if it lands, cross-check its 0.005 vs 0.001 claim against my r2 sweep.
