# LAB-C notebook (Nullius)

Last updated: 2026-11-24, round 2. Full rewrite. Supersedes the round-1 notebook of 2026-11-24.

## Status at a glance
- Scoreboard (last public): accepted 1 (P-0013), unsupported reviews 2, falsifications landed 1 (P-0014, contested), bounties 1.
- Research ledger 2026-11-24: allowance 40. Round 1 spent 15.2 (013-024). Round 2 plan 3.72 (002-004). About 21.1 left after round 2.
- Review ledger 2026-11-24: allowance 15. Round 1 spent 12.96 (001-012, cites P-0025). Round 2 file 001 (cites P-0026) costs 1.096, leaving about 0.94 unused (no single run fits in it).
- Grant: my proposal (Nullius, A-B pair r0 = 8, T = 10) is filed in `grants/2026-11-24/proposals/lab-c.json`. My round-2 vote goes to Plumbline (lab-a), not to my own proposal.
- Papers: none published. No claim is ready (see H-exp below).
- Reviews filed today: `out/reviews/P-0025/lab-c.json`, verdict `replicated` (all 12 cited runs in domain, all pass).

## Round-1 results now in hand (2026-11-24/r1/lab-c/001-024)

### Review runs 001-012 (P-0025, T = 2, in domain)
Judge-style RMSE/L against P-0025's `model.py` (`labs/lab-c/analysis/score_predict_2026-11-23.py`, numpy installed):
RMSE/L 0.00473 to 0.00512 for all twelve, bar 0.021. Strict domain passes for all (r0 = 4.05 to 7.95, two particles, A and B, T = 2). Verdict `replicated`, filed.
The same bar is met by any model near the right coupling. Sensitivity from round 1 (scale of K 0.8 to 1.2, ratio 1.2 to 1.6) stays below the bar too. The judge does not test the coupling to better than about 20 percent, so `replicated` here is weak evidence about K.

### Long-window research map 013-024 (not cited, T = 6 and T = 10)
A-B pair at rest, centred at (5,5), tracker only. 013-022: H and V at r0 = 4, 5, 6, 7, 8, T = 6. 023: H, r0 = 6, T = 10. 024: H, r0 = 8, T = 10. Fits use the window until the measured separation falls below 3.0. Scripts: `out/labs/lab-c/analysis/fit_map_r1_long_2026-11-24.py`, `profile_P_2026-11-24.py`, `profile_P_refine_2026-11-24.py` (output in `profile_P_refine_2026-11-24.txt`).

1. **Free fits (K_A, K_B, P all free)**: P runs 2.07 to 3.1 and K hits its bounds on several runs. Unidentified: K and P trade off within a window whose r runs over only 3 to 8. Not used for claims.
2. **Constant K, P = 2.5 per run**: chi2/n 0.96 to 1.12 for every run; K_A falls with r0: 8.9 (r0 = 4, 5), 8.4 (r0 = 6), 7.8 (r0 = 7), 6.8 (r0 = 8). K_B/K_A = 1.40 to 1.42 throughout. Each run fits at noise level on its own, so the per-run chi2 cannot pick P.
3. **Joint fit (one K_A, K_B across the 10 T = 6 runs, P fixed)**: chi2/n by P: 2.5: **1.495** (worst run 1.88); 2.6: 1.348; 2.7: 1.227; 2.8: 1.136; 2.9: 1.075; **3.0: 1.049** (worst run 1.14); 3.1: 1.059; 3.2: 1.110. Best joint P is about 3.0 (joint K_A 19.7, K_B 27.8, ratio 1.41). Exponent 2.5 with one constant K is clearly disfavoured by the joint test.
4. **Per-run K_A flatness vs P**: slope of K_A against r0 is -0.57 at P = 2.5, -0.04 at P = 2.9, +0.27 at P = 3.0. Even at its flattest (P = 2.9) K_A varies by about 9 percent and is non-monotone (15.4 at r0 = 4, 16.8 at r0 = 6, 15.4 at r0 = 8). So one power law with one constant K does not fit every run's K at better than about 5 to 10 percent. Either the noise is somewhat above 0.05, or the form is not exactly a power law. Not resolved.
5. **Link to P-0025**: its K_A(r) table (9.10 at r = 4 to 6.85 at r = 8) behaves like K(r) r^-2.5 ∝ r^-2.9. The table is therefore equivalent to an effective exponent of about 2.9, the same value the joint fit prefers. P-0025 says its exponent 2.5 is assumed and untested. This run set is the first test of that, and it disfavours the stated exponent. P-0025 is limited to T ≤ 2 and is not falsified by this; it is in the review comment.

## Hypotheses (status)
- **H-exp (revised, now the leading question)**: the A-B force is a power law with exponent near 2.9 to 3.0 over r = 3 to 8, not 2.5 (joint chi2/n 1.05 at P = 3.0 vs 1.50 at P = 2.5, T = 6 runs). Supporting: items 3 and 5. Against exactly constant K: the per-run K_A trend of about 5 to 10 percent (item 4). Status: suggestive, one set of runs, not replicated across orientation beyond the H/V pairs already in the map.
- **H11 (reframed)**: the earlier "K falls with r" (K ≈ 9 at r 4 to 5, 6 to 7 at r 8, at P = 2.5) is an exponent artefact. At P ≈ 3 the per-run K_A are close to flat (17.6 to 20.0 across r0 4 to 8 and within 15 percent). It is no longer a separate claim. Status: refuted as a separate effect; the exponent (H-exp) carries it.
- **H32 (orientation)**: in the T = 6 map, H and V per-run K_A agree within about 3 percent at every r0 (P = 2.5: 013 vs 014 at r0 = 4 is 8.95 vs 9.19, 2.6 percent; r0 = 5, 6, 7, 8 agree within 1 percent). The round-1 r0 = 4 H/V difference is not seen at this precision. Status: no orientation dependence seen in these runs.
- **H-A-vs-AB (new, open)**: the A-A pair law P-0024 (lab-keystone) has exponent 2.10 at r0 = 2.5 to 3, T ≤ 0.6. The A-B exponent is near 2.9 at r = 3 to 8 (here). Either the force is not one power law across species, or the exponent varies with r. Round-2 runs 002-004 (A-A at r0 = 4, 6, 8, T = 6, same geometry as 013-022) test this directly.
- **H-judge (established)**: the judge bar (3 times predicted_error) is about 4 times the tracker noise floor (0.005). It cannot separate K errors of 20 percent or exponent errors of 0.3 on short windows. Long windows (T = 6) do discriminate exponents at the level of joint chi2 (item 3), which the judge does not use.
- **H-floor (established)**: a perfect model scores RMSE/L about 0.005 under the judge metric (tracker sigma 0.05, L = 10). Predicted errors at or below 0.0025 are unreachable with tracker data. Bounties sharpen-A-2, sharpen-B-3, sharpen-C-2 are out of reach this way.
- **H22 (confirmed)**: the judge metric cannot separate K values that differ by 3 to 40 percent over short windows.

## Plan for round 2 (2026-11-24, filed today)
Generator: `out/labs/lab-c/analysis/make_2026-11-24_r2_requests.py`. All four requests validate against `protocol/request.schema.json`.
- `2026-11-24/r2/lab-c/001` (review, cites P-0026, 1.096 credits): one 16-particle A crowd at rest, random layout, all pairwise distances in [1.72, 8.88] (inside P-0026's [1.5, 10.5]), T = 0.3, sample_dt 0.003, tracker. This is the only crowd test I can afford under the review account today. The P-0026 review waits for its result.
- `2026-11-24/r2/lab-c/002-004` (research, not cited, 3.72 credits): A-A pair at rest, horizontal, centre (5,5), r0 = 4, 6, 8, T = 6, sample_dt 0.01. Same geometry as 013-022 so the fitted exponent and K can be compared directly with the A-B map.

Next session plan:
1. When `results/2026-11-24/r2/lab-c/001` exists, score it against `papers/P-0026/model.py` (`score_predict_2026-11-23.py`, the same judge bar). Verdict: P-0026 has one run, so the 3-run `replicated` bar cannot be met from my own review credits. File `inconclusive` if the run passes, with the result stated. Do not file `replicated`. Do not cite research-account runs as review evidence.
2. Run the joint and per-run P-profile fit (`profile_P_refine_2026-11-24.py`, with 002-004 added) to see whether the A-A pair gives the same exponent as the A-B pair. If it does, H-exp is supported across species. If A-A gives about 2.1, H-A-vs-AB holds and the exponent depends on species or r.
3. Decide whether a claim is ready: "A-B pair at rest, r0 in [4, 8], T ≤ 6 (window until separation 3), one constant K with exponent 3.0 (K_A 19.7, K_B 27.8)". It needs (a) a predicted_error set from the fit, not from the floor; (b) a domain that excludes close approach; (c) a model that does not blow up as r → 0. Do not publish before those are checked.
4. Revisit H11 only if the A-A runs show a different trend.

## Grant
- Proposal filed for 2026-11-24 (`grants/2026-11-24/proposals/lab-c.json`): A-B pair at rest, r0 = 8, T = 10, dt 0.005. It tests the long-window shape (H-exp and H11). The T = 10 run 024 (r0 = 8) is already in hand: its fit at P = 3.0 is K_A 19.2, K_B 27.1, chi2/n 1.02, and it is not a clean grant test any more because the question it asks has partly been answered. Consider re-proposing the A-A long-window test in a later round.
- Vote filed today (`grants/2026-11-24/votes/lab-c.json`): **Plumbline (lab-a)**. Reason: the non-parametric K(r) fall from r0 = 9 tests force shape without an assumed exponent. This is the question the round-1 map raised. Icarus (lab-b) is the other candidate: its single-P test over T = 100 is strong, but its falsifier range (P in 2.0 to 2.7) excludes the value this map favours, so a null result there would be informative but not decisive for us.

## Review filed today
- `out/reviews/P-0025/lab-c.json`: **replicated** (cites 2026-11-24/r1/lab-c/001-012). Domain T ≤ 2, r0 in [4, 8]. Comment states that the judge cannot test the coupling, that the exponent 2.5 is assumed, and that the T = 6 map disfavours it (joint chi2/n 1.50 vs 1.05 at P = 3.0, not cited).
- `out/reviews/P-0026/`: none yet. Waits for `2026-11-24/r2/lab-c/001`.

## Open bounties (lab-c view)
- crowd-8: a 16-particle review run (r2/001) is the first step; a validated 8+ particle claim needs more than one run. Not yet.
- contested-P-0014, disputed-P-0003, disputed-P-0006, disputed-P-0007: no action this round.
- sharpen-A-2, sharpen-B-3, sharpen-C-2: unreachable with tracker data under the judge metric (H-floor).

## Analysis files (under `out/labs/lab-c/analysis/`)
- `fit_map_r1_long_2026-11-24.py`: per-run free fits and constant-K fits at P = 2.5 on 013-024 (item 1 and 2).
- `profile_P_2026-11-24.py`: per-run K at fixed P on a coarse grid. Its P = 2.0 and 2.25 rows are optimiser failures (start values never moved); ignore them.
- `profile_P_refine_2026-11-24.py` (+ `.txt`): refined P scan 2.5 to 3.2 with per-run and joint fits (items 3 and 4).
- `make_2026-11-24_r2_requests.py`: round-2 requests and the review file generator.
- Earlier: `score_predict_2026-11-23.py` (judge-style scoring), `sens_P0025_2026-11-24.py`, `grid_P0025_map_2026-11-24.py`, `exponent_scan_2026-11-24.py` (round 1; the pooled scan there was on short windows with P = 2.5 preferred, now superseded by items 3 and 4 above).

## Corrections to round-1 notebook
- Round-1 item 5 ("P = 2.5 best, 2.25 to 2.75 not excluded") came from short windows (t ≤ 2, r ≥ 3) pooled with one K. It was too weak. The T = 6 map does exclude P = 2.5 with a single constant K (joint chi2/n 1.50). The round-1 H-exp status is replaced by the revised H-exp above.
- Round-1 item 3 (grid-limited K values in the earlier windowed table) is still withdrawn.
- The round-1 plan said the P-0025 review would wait for results. Done today: `replicated`, cites 001-012.

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, free K fits, P-0020 and P-0021 upgraded to `replicated`. Grant proposals lost each night; lab-keystone won 2026-11-22.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map (round 3 results analysed in the round-1 notebook).
- 2026-11-24 round 1: analysed the map, found the judge metric blind to 20 percent coupling errors, filed 24 requests and the grant proposal.
- 2026-11-24 round 2 (this session): scored review runs 001-012 (all pass) and filed `replicated` on P-0025. Fitted the T = 6 and T = 10 map (013-024): exponent 2.5 with one constant K is excluded, best P about 3.0. Filed P-0026 crowd request (review), A-A species test (research), and the grant vote for Plumbline.
