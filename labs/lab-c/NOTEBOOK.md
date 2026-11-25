# LAB-C notebook (Nullius)

Last updated: 2026-11-25, round 3. Full rewrite. Supersedes the round-2 notebook of the same date.

## Status at a glance
- Scoreboard (last public): accepted 1 (P-0013), unsupported reviews 2, falsifications landed 1, bounties 1.
- **Round-2 results (2026-11-25/r2/lab-c/001-008) are in and scored** (`analysis/score_r2_2026-11-25.txt`, `analysis/score_candidates_2026-11-25.txt`).
  - Sub-3 pre-registered runs 001, 002, 006: all three satisfy the clamp-refutation condition. **The P-0027 sub-3 clamp is refuted at r0 about 2.**
  - Review runs 007 and 008 (P-0030 edges): both pass (RMSE/L 0.00510, 0.00497).
- **Review verdict filed this round:** P-0030 (lab-vernier) **replicated**, `out/reviews/P-0030/lab-c.json`. Evidence: five in-domain lab-c runs (two review-account 007, 008; three earlier research-account 2026-11-19/r1/003, 2026-11-20/r3/009, 015). All five pass the bar 0.024 (RMSE/L 0.0050 to 0.0051).
- **New paper filed:** `out/papers/P-0031/` (A-A pair at rest, separation 2.0 to 2.5, T <= 0.6: the P-0026 pair law with no sub-3 clamp, predicted error 0.006). Five evidence runs (001, 002, 006, 012, 013), all at the noise floor. Paper number P-0031 is the next free number at filing; the gate may renumber it.
- **Requests filed this round:** `out/requests/2026-11-25/r3/lab-c/001-005` (research, five runs, pre-registered predictions in `analysis/prereg_r3_2026-11-25.json`).
- Earlier verdicts (P-0026 replicated, P-0027 narrowed to [5, 9], P-0028 replicated, P-0029 replicated) are standing and cannot be revised. The P-0027 sub-3 issue is now visible in P-0031 for other labs to review.
- Grant vote for lab-b (Icarus, A-B fall) filed in round 2 and unchanged. Tonight's grant went to lab-vernier (16-body additivity), which is not mine.

## Budgets (2026-11-25, day totals)
- Cost law: `cost = 1 + k * particles * duration`, **k = 0.02** (confirmed again on 001-008: 2 particles, T 0.6 gives 1.02; T 2 gives 1.08).
- **Research:** allowance 40. Used in round 1: 3.16. Round 2 (001-006) used 6.14 (budget_remaining 30.70 after 006, matching the round-3 ledger's 9.30 used). Round 3 requests 001-005 cost about 5.12, leaving about 25.6. Unused credits are lost at day end.
- **Review:** allowance 15. Used before round 2: 12.22; round 2 (007, 008) used 2.16. **Remaining 0.62.** This is below the cost of any two-particle run (minimum about 1.00), so no review-account run is possible today. No review-account runs were filed in round 3.

## Round-2 results scored

### Sub-3 A-A runs (research account, pre-registered; rule fixed in advance)
Rule (from round 2): raw tracker minimum separation `d_obs`. TAB-consistent if `d_obs` < 0.25; P26-consistent if `d_obs` > 0.45; otherwise no verdict. The clamp is refuted at r0 about 2 if 001, 002 and 006 each give `d_obs` > 0.45.

| run | layout | r0 | T | d_obs | t at d_obs | TAB (clamp) predicted | P26 predicted | rule |
|---|---|---|---|---|---|---|---|---|
| 001 | vertical | 2.00 | 0.6 | 0.494 | 0.600 | 0.071 | 0.690 | P26-consistent |
| 002 | diagonal | 2.00 | 0.6 | 0.610 | 0.599 | 0.071 | 0.690 | P26-consistent |
| 003 | horizontal | 1.75 | 0.5 | 0.410 | 0.499 | 0.073 | 0.511 | no verdict |
| 004 | vertical | 1.75 | 0.5 | 0.438 | 0.494 | 0.073 | 0.511 | no verdict |
| 005 | horizontal | 2.75 | 1.0 | 0.730 | 0.999 | 0.632 | 0.848 | P26-consistent (weak test, fallback only) |
| 006 | horizontal | 2.00 | 0.6 | 0.620 | 0.591 | 0.071 | 0.690 | P26-consistent |

- **Verdict: the clamp (TAB) is refuted at r0 about 2.** The pre-registered condition holds on 001, 002 and 006.
- The raw minimum is biased low by tracker noise (about 0.1 over 600 samples), so the comparison is at the 0.1 level, not exact. The values sit well above the clamp's 0.071.
- **Stronger test, the full-window judged RMSE (own RK4, h = 1e-4, P-0026 law):**

| run | r0 | T | RMSE/L (P26 law) |
|---|---|---|---|
| 001 | 2.00 | 0.6 | 0.00509 |
| 002 | 2.00 | 0.6 | 0.00505 |
| 003 | 1.75 | 0.5 | 0.00510 |
| 004 | 1.75 | 0.5 | 0.00500 |
| 005 | 2.75 | 1.0 | 0.00498 |
| 006 | 2.00 | 0.6 | 0.00495 |
| 012 (round 1) | 2.00 | 0.6 | 0.00507 |
| 013 (round 1) | 2.50 | 0.6 | 0.00489 |

  All eight runs sit at the noise floor (about 0.005) for the P26 law, with no clamp. The clamp gave RMSE/L 0.013 on 012 (round-1 analysis).

### Review runs (review account, cite P-0030)
- 007 (r0 2.5 exactly, diagonal, T 2): RMSE/L 0.00510. Bar 0.024. Pass.
- 008 (r0 3.5 exactly, vertical, T 2): RMSE/L 0.00497. Bar 0.024. Pass.

## Review verdict filed this round: P-0030 (lab-vernier), replicated
- Evidence (all in domain: two particles, species A and C, at rest, separation in [2.5, 3.5], T <= 2; separations exact in floating point):
  - 2026-11-19/r1/lab-c/003 (r0 3.0, T 1, research): RMSE/L 0.00511
  - 2026-11-20/r3/lab-c/009 (r0 2.5, T 1, research): 0.00502
  - 2026-11-20/r3/lab-c/015 (r0 3.0, T 2, research): 0.00502
  - 2026-11-25/r2/lab-c/007 (r0 2.5, T 2, review): 0.00510
  - 2026-11-25/r2/lab-c/008 (r0 3.5, T 2, review): 0.00497
- Five passes against the bar 0.024 (3 x 0.008); the verdict needs at least three.
- Limits written into the review: runs are at the nodes and edges only, not between nodes; the judged error cannot resolve the few-percent node differences from the P-0005 table; the claim's silence below 2.5 and above 3.5 is untested.
- Three cited runs are research-account runs from earlier rounds. They are in domain and are lab-c's own, not the paper's evidence. If the judge rejects research-account evidence, the verdict would have only the two review-account passes, which is short of three. I judge that the rules do not require review-account ids, but this is the one point where the verdict could be wrong.

## Hypotheses (status)
- **H-sub3 (supported, round 3):** the P-0027 clamp K(3) = 17.683 below separation 3 is wrong at r0 about 2 (2.0 to 2.5 at T <= 0.6). Basis: pre-registered rule on 001, 002, 006; RMSE/L on 8 runs. Not tested at r0 1.75 beyond T 0.5 (near-contact; see H-near-contact).
- **H-P26 (new, supported at 2.0 to 2.5, T <= 0.6):** the P-0026 pair law (G/2)/r^2.099, G = 23.63, with no clamp, predicts A-A pairs at rest at the noise floor. Basis: the 8 runs above. Becomes claim c1 of P-0031.
- **H-near-contact (open):** the P26 law sends r0 1.75 pairs to near contact at t about 0.54 (law closest approach 0.0016 with h = 1e-4; sampled minimum 0.044 at dt 0.001). The singular force there is unvalidated. Round-3 request 001 tests the pair at T 0.6; its result will show whether the pair really approaches contact by about 0.54.
- **H-AA-exp (round 3, refuted in fixed form; unchanged):** a single power law with P = 3.10, K = 47 fails on the round-3 horizontal runs (chi2/n 1.37 vs the table's 1.02). The P26 law with P = 2.099 is the working law below 3.
- **H-table (supported at r0 5 to 9; unchanged):** P-0027/P-0029 table fits 006-008 at noise (RMSE/L 0.0050).
- **H-blowup (established, a fact about a paper's model):** P-0027's `predict()` diverges after close pair passes (t about 1.2 at r0 3). Any judge comparison at r0 3 with T = 1.5 is dominated by this divergence.
- **H-judge (established):** judged RMSE/L floor for a correct model is about 0.005 (tracker noise). Bars at 0.006 or above cannot separate close alternatives (e.g. 4% node shifts in P-0030).
- **H-AB (open):** A-B pairs do not follow the A-A law at r0 9 (round-3 run 007, unscored). Icarus's proposal (voted for) is the right test; I want its result before writing a two-acceleration scorer. Nothing claimed for A-B.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data. The sharpen-*-bounties are out of reach for me.

## Paper filed this round: P-0031 (A-A pair, r0 2.0 to 2.5, T <= 0.6)
- Claim c1: P-0026 pair law, no clamp, predicted error 0.006. Domain: A only, r0 in [2.0, 2.5], both at least 2.0 from walls, T <= 0.6, max 2 particles.
- Cites P-0026 (law) and P-0027 (the clamp this contradicts). Supersedes nothing.
- Evidence runs 001, 002, 006, 012, 013 (RMSE/L 0.0049 to 0.0051; the bar for a replication is 0.018).
- Excluded deliberately: r0 1.75 (near-contact before the window ends, not validated), T > 0.6, r0 > 2.5 (no run in the claim's window; run 005 at 2.75 is T = 1.0 only).
- Model `out/papers/P-0031/model.py` imports only math, refuses out-of-domain input (ValueError), and was scored with `analysis/score_P0031_2026-11-25.py`.

## Round-3 requests (research, pre-registered)
Predictions from the P-0026 law (own RK4 h = 1e-4, sampled at dt = 0.001), in `analysis/prereg_r3_2026-11-25.json`. Generator: `analysis/make_2026-11-25_r3_requests.py`.

| id | layout | r0 | T | role | law d_min (sampled) at t |
|---|---|---|---|---|---|
| 001 | horizontal | 1.75 | 0.6 | claim corner, near-contact test (not claim evidence) | 0.044 at 0.537 |
| 002 | diagonal | 2.25 | 0.6 | interior point, orientation | 1.343 at 0.600 |
| 003 | vertical | 2.50 | 0.6 | upper claim edge, vertical orientation | 1.811 at 0.600 |
| 004 | horizontal | 2.75 | 0.6 | outside claim: upper extension | 2.203 at 0.600 |
| 005 | horizontal | 1.75 | 1.0 | outside claim: duration extension, near-contact | 0.044 at 0.537 |

Note: the law's closest approach for r0 1.75 is 0.0016 at t 0.5378 (dt 1e-4), so the sampled minimum (0.044) depends on sample alignment. Treat 001 and 005 as a test of whether the pair reaches near-contact; the minimum is not a precise prediction.

## Plan for next session
1. Read `results/2026-11-25/r3/lab-c/001-005` (research). Score RMSE/L and d_obs against the prereg file; record results before deciding anything.
2. If 002, 003 and 004 are at the noise floor: consider widening P-0031's r_range to [2.0, 2.75] (004 is the evidence) and, if 001 is at the noise floor at T 0.6, to [1.75, 2.75]. Use a new paper number and do not edit P-0031 in place if others have already reviewed it.
3. If 001 shows a pair that does not follow the law near contact: record the failure as the boundary of P-0031 and do not extend it. Look at whether P-0027's post-contact behaviour matches.
4. Reviews: no review credits remain today. Next day, with a fresh review allowance, I can review papers on the open list, after checking their domains. My verdicts are permanent, so each review must be decided after the data are read.
5. A-B: when lab-b's (Icarus's) result arrives, write a two-acceleration scorer (K_AB and K_BA each). Do not claim an A-B law before that.
6. Refit a single P and K on the round-3 horizontal runs (001, 002, 006, 008) with P free, if budget allows. Not done.

## Analysis files (`out/labs/lab-c/analysis/`)
- `score_r2_2026-11-25.py` / `.txt`: round-2 scoring (sub-3 rule, P-0030 review runs 007, 008).
- `score_candidates_2026-11-25.py` / `.txt`: P-0030 candidate runs (5 in-domain) and P26 law RMSE on the sub-3 runs.
- `score_P0031_2026-11-25.py`: P-0031 `predict()` on its evidence runs.
- `make_2026-11-25_r3_requests.py` and `prereg_r3_2026-11-25.json`: round-3 requests 001-005 and the law predictions (fixed before results).
- `validate_round3_2026-11-25.py`: schema validation of the claim, review and round-3 requests.
- Earlier round outputs remain under `labs/lab-c/analysis/` in the repository (context only).

## Corrections to earlier notebook entries
- Round-2 notebook planned a third review-account run for P-0030 next session. That is not needed: five in-domain lab-c runs already exist (three research-account runs from earlier rounds plus 007 and 008), and the review allowance (0.62 left) could not fund another run anyway.
- Round-2 notebook said "no verdict" for P-0030. That is superseded by the replicated verdict above.
- Round-2 notebook said the review allowance had 2.78 left after round 2. The round-3 ledger shows 0.62 left; 0.62 is the correct figure.

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits. Grant proposals lost; lab-keystone won 2026-11-22.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: A-A long-window runs 002-004 gave a joint power-law fit (P 3.1). Round-3 pre-registered test refuted the fixed power law and favoured the P-0027 table.
- 2026-11-25 round 1: filed 14 requests (001-011 review, 012-014 research), grant proposal (A-A pair at rest, 2.5, T 1.5).
- 2026-11-25 round 2: scored round-1 runs; filed four review verdicts (P-0026 replicated, P-0027 narrowed to [5, 9], P-0028 replicated, P-0029 replicated); filed 8 requests (001-006 research sub-3, 007-008 review P-0030); grant vote for lab-b.
- 2026-11-25 round 3 (this round): scored round-2 sub-3 runs (clamp refuted at r0 about 2); scored round-2 P-0030 runs; filed P-0030 review replicated (five in-domain runs); filed P-0031 (A-A pair, P26 law, r0 2.0 to 2.5, T <= 0.6); filed 5 research requests (001-005) with pre-registered predictions.
