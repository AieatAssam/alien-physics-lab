# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-24, round 1.

## Status

- **Accepted papers: 2** (scoreboard). Submitted: **P-0024** (A-A pair at rest, r0 in [1.25, 3.0], exponent 2.10, window T <= 0.3 / 0.6), **P-0026** (A-A crowd, up to 16 particles at rest, T <= 0.3, summed pair law, predicted error 0.007; new today). Paper numbers are provisional; refer to papers by title if renumbered.
- **Unsupported reviews: 3** (scoreboard). Caveat for the round-2 reviews (P-0017, P-0018, P-0022, P-0023): their T <= 0.8 runs sit at the tracker noise floor and do not test K or P.
- **Grants:** won round 3 (2026-11-23, 3 votes to lab-b's 2, title "Eight A-A pairs at once"). Award 120 credits on `grant`, usable in round 3 of that date. Tonight's proposal is filed for round 1 (see below).
- **Open bounties I can address:** crowd-8 (bounty 3): P-0026 is a candidate (max_particles 16). sharpen-A/B/C need predicted_error <= 0.0025, which is below the judged noise floor (~0.005) for single-run claims. I have not attempted them.

## Round 1 actions (2026-11-24)

1. **Scored round-3 extension runs 2026-11-23/r3/lab-keystone/002-007** (A-A at rest, centre (5,5), r0 in {4,5,6} x {H,V}, T = 1.0, sample_dt 0.0025). Script `out/labs/lab-keystone/analysis/score_r3_extension_2026-11-24.py`, diagnostics `diag_r3_extension_2026-11-24.py`. Outputs in the matching `.txt` files.
2. **Scored the N = 16 grant run 2026-11-23/r3/lab-keystone/001** against the pre-registered full additive prediction. Result: per-coordinate rms 0.0512 (noise 0.05). Pass (rule was <= 0.06).
3. **Published P-0026** (`out/papers/P-0026/`): A-A crowd up to 16, T <= 0.3, pairwise sum of the P-0024 law, predicted error 0.007, evidence 2026-11-23/r3/lab-keystone/001. `model.py` reproduces that run at RMSE/L = 0.0051 (`check_P0026_2026-11-24.txt`).
4. **Tonight's grant proposal** (`out/grants/2026-11-24/proposals/lab-keystone.json`): 8 A in four horizontal pairs, r0 = 2.5, at rest, centres (2.25|7.75, 2.25|7.75), T = 0.6, sample_dt 0.003, tracker. Pre-registered prediction: `grant_prereg_prediction_2026-11-24.json`, setup `grant_setup_2026-11-24.json`, script `grant_crowd8_2026-11-24.py`. Min pairwise distance over the run is about 1.98, so no close approach. Pass rule: per-coordinate rms <= 0.06. The window is inside P-0024 (r0 in [2.5, 3.0], T <= 0.6), so a fail points at multi-body terms.
5. **Requests filed today** (`out/requests/2026-11-24/r1/lab-keystone/`):
   - 001-003 (**review account, cites_paper P-0025**, 1.08 each): A-B edge checks for Icarus' paper. 001: r0 = 4.0 horizontal (A at (3,5), B at (7,5)). 002: r0 = 8.0 horizontal (A at (1,5), B at (9,5)). 003: r0 = 8.0 vertical (A at (5,1), B at (5,9)). T = 2.0, sample_dt 0.002, tracker. All in domain (2 particles, species A/B, distances exactly 4.0 and 8.0 = bounds, inclusive). Review budget used 3.24 of 15.
   - 004-005 (research, 1.10 each): replicates of 2026-11-23/r3/lab-keystone/001 for P-0026. Not yet cited.
   - Research credits used today: 2.19 of 40 (plus the grant request, filed in round 3).
6. **Not filed:** the grant main event itself. It is one request per night in round 3 on the `grant` account. The round-3 request file must carry the proposal's setup unchanged.

## Results and what they say

### Round-3 extension runs (2026-11-23/r3/lab-keystone/002-007; T = 1.0; tracker)

Projected separation on the initial axis, against P-0024's 1D law (G = 23.63, P = 2.099; M1). Tracker noise on the projected separation is about 0.071.

| run | r0 | orientation | rms (t <= 1) | mean residual, t in [0.8, 1.0) |
|---|---|---|---|---|
| 002 | 4.0 | H | 0.083 | +0.072 |
| 003 | 4.0 | V | 0.076 | +0.056 |
| 004 | 5.0 | H | 0.081 | +0.072 |
| 005 | 5.0 | V | 0.075 | +0.060 |
| 006 | 6.0 | H | 0.081 | +0.058 |
| 007 | 6.0 | V | 0.086 | +0.075 |

- **Pre-registered rule, as written:** pooled rms 0.080 <= 0.09 passes. The drift clause (no run past t = 0.5 by more than 0.1) passes when read as a binned mean (all bins with t > 0.5 at or below +0.075). I first coded it as the max single-sample residual after t = 0.5, which gives 0.29 and fails. That is per-sample noise, not drift, so the coded version was wrong and is not the rule's intent. Recorded here so the record is clear.
- **What the rule misses:** all six runs have the same-sign residual. It is about zero for t < 0.4 (bin means -0.011 to +0.041, scattered) and rises to +0.04 to +0.05 at t in [0.6, 0.8) and +0.06 to +0.075 at t in [0.8, 1.0). Measured separation is larger than M1, so M1 pulls too hard. The bin-mean standard error is about 0.008, so the bias is significant. Best-fit G at P = 2.099 comes out at 0.85 to 0.90 of 23.63 (grid edge hit at 20.0 for several runs; the scan was not widened).
- **Reading:** the P-0024 law at r0 = 4 to 6 is biased by roughly 15 percent in acceleration by t ~ 0.8, and the bias starts near t ~ 0.4. This agrees with the T = 2 result (effective acceleration 10 to 30 percent below M1 at r = 4 to 6). The pre-registered pass rule is too loose to catch it. **Decision: no narrowed exponent claim for t <= 1 at r0 = 4 to 6.** A claim for t <= 0.3 at these radii would be honest but sits below the judged noise floor, so it would not test anything the judge measures.

### N = 16 grant run (2026-11-23/r3/lab-keystone/001; T = 0.3)

- Full pairwise-additive prediction, pre-registered 2026-11-23. Per-coordinate rms **0.0512** (noise 0.05). No particle has a mean residual above about 0.015. Pass.
- The run tests additivity and the pair law at r = 2 to 10 jointly. Cross-pair displacements at T = 0.3 are up to about 0.18, so a pass does not isolate either part. P-0026 says so.

## Things I learned this round

- **Per-particle factor.** P-0024's law is (G/2)/q^P on each particle, which gives relative acceleration G/q^P. When I first wrote the N-body model I used G/q^P per particle, which doubled the acceleration and gave RMSE/L 0.019 against the N = 16 run. The corrected factor gives 0.0051. Check the factor against P-0024's `model.py` before reusing any pair-sum code.
- **Close approach.** Power-law attraction with P ~ 2.1 makes a pair from rest collapse in finite time, so windows must stop before that. With the corrected per-particle factor (see above), the 4-pair, N = 8 layout at r0 = 2.5 keeps its minimum separation at about 2.0 over T = 0.6 but falls to about 0.45 by T = 1.0 (layout scan `layout_scan_2026-11-24.py`). The 4-pair layout at r0 = 2.0 drops to about 0.07 by T = 1.0 with the wrong factor; not re-checked with the right one. Keep grant and claim windows at T <= 0.6 for r0 >= 2.5 and T <= 0.3 for crowds.
- **Crowd size.** A 16-particle 10 x 10 box with pairs at r0 >= 2 has many cross distances of 2 to 4. Any run longer than about 0.3 becomes strongly coupled and close-approach limited, so N = 16 tests belong at T = 0.3.

## Hypotheses

- **P-0024-c1 (submitted, mine):** A-A pair at rest, r0 in [1.25, 3.0], G = 23.63, P = 2.10, window T <= 0.3 (r0 < 2.5) or T <= 0.6 (r0 in [2.5, 3.0]). predicted_error 0.006. The judged metric is at noise and does not test P.
- **P-0026-c1 (submitted today, mine):** up to 16 A at rest, all pairwise distances in [1.5, 10.5], T <= 0.3, pairwise sum of the P-0024 law. One run (001) at RMSE/L 0.0051. Replicates 004-005 are in flight.
- **H-tonight (grant, round 3 if won):** pair law and additivity at N = 8, r0 = 2.5, T = 0.6. Pre-registered prediction in `grant_prereg_prediction_2026-11-24.json`. A pass would support a crowd-8 claim. A fail is attributable to multi-body terms, since the pair law is inside its own window.
- **H-exponent-extension (rejected as written; t <= 1 version rejected by round-3 bias):** the P-0024 law holds to r0 = 4 to 6 at t <= 1. The bias above rejects it at the ~15 percent level from t ~ 0.8.
- **H-additive (N >= 3):** supported at noise for N = 3 to 5 and N = 16 at T = 0.3. Untested at N = 8 with cross gaps of 3. The tonight grant is that test.
- **H-close-approach:** power laws fail at close approach. For r0 = 4 the pair closes near t = 2.0 (min separation 0.14). For r0 = 1.25 the close approach is near t = 0.32.
- **H-K-constancy (weakly supported):** A-B at r = 7 constant to 5 to 10 percent over T = 6 (P-0021). No new claim.
- **H-no-factor at 2.5 to 3.5 (P-0014, submitted):** unchanged.
- **H-scale-1.5 (lab-c, consistent):** unchanged.

## Reviews

- **P-0025 (lab-b, A-B pair at r0 in [4, 8], T <= 2, K_B/K_A = 1.41 with interpolated K_A table; predicted error 0.007).** Review due. Requests 001-003 filed today on the review account. The review will cite those ids only, after they run. Verdict depends on the results. Points to test: the r0 = 4.0 and 8.0 edges, orientation (H vs V at r0 = 8), and whether the K_A nodes hold. Remember the judge does not check duration. Use only T <= 2 runs for this claim, and state that the claim makes no statement beyond T = 2.
- **Round-2 reviews (P-0017, P-0018, P-0022, P-0023):** caveat unchanged. Their runs do not test K or P.

## Things we know about the metric

- Judged metric is at noise for short runs (T <= 0.8). Errors are about 0.005 to 0.007 and do not test K or P. Say so in every comment.
- Judged metric is K-sensitive at T = 6 to 10. A 10 percent K change moves the P-0021 error from 0.0050 to 0.0083.
- Domain check is exact (`lo <= distance <= hi`). Use `tools/domain.py`. The judge does **not** check duration, so the window must be stated in the claim and enforced in `model.py`.
- Tracker noise is about 0.05 per coordinate. Projected separation noise is about 0.071. Judged RMSE/L for a perfect model is about 0.005. So a predicted_error below about 0.005 cannot be met honestly by a single-run claim.
- Noise bias: the norm of a noisy relative vector is biased upward at small r. Project onto the initial axis.

## Plan for the next session

1. **Round 2:** score requests 004-005 (replicates of the N = 16 run). If both are at RMSE/L <= 0.01, revise P-0026 to cite all three runs.
2. **Round 2:** score review requests 001-003 for P-0025 (lab-b). If all three fall at or below 0.021 (3 x predicted_error), file a "replicated" review citing them, and say which edges were tested. If one edge fails above 0.021, file "narrowed" with the proposed domain, citing only in-domain runs.
3. **Round 3:** file the grant main event `2026-11-24/r3/lab-keystone/001` on the `grant` account, using the proposal's setup unchanged. Pass rule: per-coordinate rms <= 0.06 against `grant_prereg_prediction_2026-11-24.json`. Report per-pair residuals; a fail goes to the r0 = 2.5 pairs first.
4. **Do not publish** a new exponent or extension claim at r0 = 4 to 6 for t > 0.3 until a G-fitted law is tested on fresh runs.
5. If a review says P-0024 or P-0026 is narrowed, accept it and update under a new number.

## Files

- Scoring: `out/labs/lab-keystone/analysis/score_r3_extension_2026-11-24.py` (+ `.txt`), `diag_r3_extension_2026-11-24.py` (+ `.txt`).
- P-0026 check: `check_P0026_model_2026-11-24.py` (+ `.txt`). Model: `out/papers/P-0026/model.py`.
- Tonight's grant: `grant_crowd8_2026-11-24.py`, `grant_setup_2026-11-24.json`, `grant_prereg_prediction_2026-11-24.json`. Proposal `out/grants/2026-11-24/proposals/lab-keystone.json`.
- Layout scan (close approaches): `layout_scan_2026-11-24.py`.
- Earlier: `extension_r0_4_6_2026-11-23.py`, `extension_diag_2026-11-23.py`, `extension_full_T_2026-11-23.py`, `grant_prereg_2026-11-23.py`, `prereg_2026-11-23_r3.json`, `judge_round2_2026-11-23.py`, `score_round3_slope_2026-11-23.py`.
- Papers: `out/papers/P-0026/{paper.md,claim.json,model.py}`. P-0024 is in the repo at `papers/P-0024/`.
- Requests today: `out/requests/2026-11-24/r1/lab-keystone/001-005.json`.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0024 beyond two A particles, at rest, r0 in [1.25, 3.0], or beyond its windows.
- Do not extend P-0026 beyond species A, at rest, T <= 0.3, or the 1.5 to 10.5 pairwise range.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account with `cites_paper`.
- Do not publish a shape or exponent claim from fits whose signal is below noise, or from the M1 law at t > 0.3 for r0 >= 4.
- Do not present the N = 16 grant result as a pure additivity test without the r > 3 caveat.
