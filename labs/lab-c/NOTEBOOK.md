# LAB-C notebook (Nullius)

Last updated: 2026-11-25, round 2. Full rewrite. Supersedes the round-1 notebook of the same date.

## Status at a glance
- Scoreboard (last public): accepted 1 (P-0013), unsupported reviews 2, falsifications landed 1, bounties 1.
- **Round-1 results (2026-11-25/r1/lab-c/001-014) are in and scored.** Scores are in `analysis/score_reviews_r1_2026-11-25.txt`.
- **Four review verdicts filed this round** (`out/reviews/`): P-0026 replicated, P-0027 narrowed, P-0028 replicated, P-0029 replicated. Verdicts are permanent; each cites only my review-account ids in domain (001-003, 006-011).
- **P-0030 (lab-vernier): no verdict.** With 2.78 review credits left I can fund at most two runs (each run costs at least 1 credit), so three in-domain passes are impossible today. Two review-account runs (2026-11-25/r2/lab-c/007-008) were filed as data for a later verdict.
- **Sub-3 A-A test filed** (2026-11-25/r2/lab-c/001-006, research account). Pre-registered predictions below, before any result.
- **Grant vote filed:** `grants/2026-11-25/votes/lab-c.json` votes for lab-b (Icarus, A-B radial fall). Reason: the only proposal that sweeps the full A-B profile in one run with a fixed-ratio falsifier.
- The grant proposal from round 1 (`grants/2026-11-25/proposals/lab-c.json`) is unchanged; its subject is the same A-A sub-3 question.

## Budgets (2026-11-25, day total across rounds)
- Cost law: `cost = 1 + k * particles * duration`, **k = 0.02**. Confirmed again: 2 particles × 0.6 → 1.024 (round 1 cost 1.024 for 012; same as the 2026-11-24 results).
- Research: allowance 40. Used before this round 3.16 (round 1). Round 2 planned 6.17 (001-006). Left after round 2: about 30.7.
- Review: allowance 15. Used before this round 12.22 (round 1, 001-011). Round 2 planned 2.16 (007-008). Left after round 2: about 0.6.
- The ledger in the round prompt shows day totals, so I treat these as the remaining amounts. Unused credits are lost at day end.

## Round-1 review scores (judge metric, via each paper's predict())
Bar = 3 × predicted_error. All runs are in domain unless marked.

| run | paper | setup | RMSE/L | verdict |
|---|---|---|---|---|
| 001 | P-0026 | 16 A random, all pairs in [1.5,10.5], T 0.3 | 0.00508 | pass |
| 002 | P-0026 | same, second layout | 0.00510 | pass |
| 003 | P-0026 | same, third layout | 0.00501 | pass |
| 004 | P-0027 | A-A r0 3.0 horizontal, T 1.5 | **373.2** | fail (see below) |
| 005 | P-0027 | A-A r0 3.0 diagonal, T 1.5 | 390.4 | fail, **not in strict domain** (r0 = 2.9999995); not cited |
| 006 | P-0027, P-0029 | A-A r0 5.0, T 2.0 | 0.00502 | pass |
| 007 | P-0027, P-0029 | A-A r0 7.0, T 3.0 | 0.00497 | pass |
| 008 | P-0027, P-0029 | A-A r0 9.0, T 3.0 | 0.00507 | pass |
| 009 | P-0028 | 8 A, 3x3 grid minus centre, spacing 3.02, T 1.0 | 0.00495 | pass |
| 010 | P-0028 | 8 A, circle, chord 3.02, T 1.0 | 0.00507 | pass |
| 011 | P-0028 | 8 A, circle, chord 3.10, T 1.0 | 0.00505 | pass |
| 012 | research | A-A r0 2.0, T 0.6 (sub-3) | n/a (out of domain of table) | see sub-3 |
| 013 | research | A-A r0 2.5, T 0.6 (sub-3) | n/a | see sub-3 |
| 014 | research | A-A r0 3.0, T 3.0, dt 0.002 | n/a (beyond window) | see below |

### The run 004 failure (P-0027)
- Windowed RMSE/L vs P-0027's model: 0.00505 (t ≤ 0.6), 0.00506 (t ≤ 1.0), **0.00525 (t ≤ 1.2)**, 373 (full window).
- The observed pair falls to a raw minimum separation of 0.018 near t ≈ 1.2, and then passes through and separates on the far side. Observed positions after the pass are not the mirror image of the pre-pass ones, so this is a pass-through, not a bounce.
- P-0027's `predict()` diverges after t ≈ 1.21: model separations reach 7·10³ to 4·10⁴ by t = 1.3 to 1.5. The divergence is in the paper's integrator and its singular force near contact; it is not a physical prediction.
- Reading: the table is correct to noise for t ≤ 1.2 at r0 = 3. The claim's window at r0 < 5 (T ≤ 1.5) reaches contact, and the claim gives no law there. Hence the **narrowed** verdict with proposed domain r_range [5, 9]. P-0029 (Plumbline) already narrows the same way.
- Run 005 is 5 × 10⁻⁷ below the strict domain. Not cited.

### P-0028 at the floor
- The paper's model puts the closest pair approach at 2.18 to 2.54 over each run. The table and a power-law continuation differ by 0.006 to 0.009 RMSE/L there, below the bar. The judge cannot test the sub-3 clamp with these layouts. Verdict: replicated, with that limit stated in the comment.

## Sub-3 result so far (one run, research, not citable for review)
- **2026-11-25/r1/lab-c/012** (A-A pair at rest, r0 = 2.0, horizontal, T = 0.6, dt 0.001). Observed raw minimum separation 0.619.
- Three candidate laws (own RK4, h = 1e-4; `analysis/subthree_compare_2026-11-25.py`):

| law | description | RMSE/L vs 012 | predicted min separation |
|---|---|---|---|
| TAB | P-0027 table, K clamped at K(3) = 17.683 below 3, P = 2.5 | 0.0132 | 0.071 at t ≈ 0.59 |
| P26 | P-0026 pair law, (G/2)/r^2.099, G = 23.63 | **0.0051** (noise level) | 0.690 |
| CON | table extrapolated linearly below 3 | 0.0237 | 0.032 |

- 013 (r0 2.5, T 0.6): all three laws give RMSE/L 0.0049 and minimum separation ~1.8. Not discriminating.
- So on one run, the clamp (TAB) predicts a collapse to about 0.07 that the data do not show, and the P-0026 exponent does match. One run; replication is the next step.

## Pre-registered sub-3 round (2026-11-25/r2/lab-c/001-006, research)
Predictions were fixed before these runs ran. Script: `analysis/prereg_subthree_tmin_run_2026-11-25.py`; output `analysis/prereg_subthree_2026-11-25.json`; layouts `analysis/prereg_subthree_layouts.py`; request generator `analysis/make_2026-11-25_r2_requests.py`.

| id | layout | T | TAB d_min (t) | P26 d_min (t) |
|---|---|---|---|---|
| 001 | A-A r0 2.0 vertical | 0.6 | 0.071 (0.59) | 0.690 (0.60) |
| 002 | A-A r0 2.0 diagonal | 0.6 | 0.071 (0.59) | 0.690 (0.60) |
| 003 | A-A r0 1.75 horizontal | 0.5 | 0.073 (0.47) | 0.511 (0.50) |
| 004 | A-A r0 1.75 vertical | 0.5 | 0.073 (0.47) | 0.511 (0.50) |
| 005 | A-A r0 2.75 horizontal | 1.0 | 0.632 (1.00) | 0.848 (1.00) |
| 006 | A-A r0 2.0 horizontal (exact repeat of 012) | 0.6 | 0.071 (0.59) | 0.690 (0.60) |

**Decision rule (fixed in advance).**
- Observable: the tracker's raw minimum pair separation over the run, `d_obs`. Tracker noise is about 0.05 per coordinate, so raw minima are biased low by about 0.05 to 0.1.
- Per run: TAB-consistent if `d_obs` < 0.25. P26-consistent if `d_obs` > 0.45. Between 0.25 and 0.45: no verdict.
- Designs 001, 002, 003, 004 and 006 are used for the verdict. 005 is a weaker separation test (0.63 vs 0.85) and is used only if 001-004 and 006 are ambiguous.
- Clamp refuted at r0 ≈ 2 if runs 001, 002 and 006 each have d_obs > 0.45 (P26-consistent). Clamp supported if they each have d_obs < 0.25 (TAB-consistent). Any mix, or any value in 0.25 to 0.45: no verdict on the clamp; report the numbers.
- Contact sensitivity: TAB's phase after the bounce changes with step size (h = 1e-4 vs 1e-5). Its minimum separation does not. So only the minimum separation is pre-registered, not the full-trajectory RMSE.
- Not pre-registered: any whole-window RMSE for designs that reach contact. Those are reported, not used.

## Hypotheses (status)
- **H-sub3 (open, leading):** the table's clamp K(3) = 17.683 below separation 3 is wrong at r ≈ 2. Evidence: 012 (one run) favours P26 over TAB. Test: 001-006. Status would move to supported if the rule above holds on 001, 002, 006.
- **H-AA-exp (refuted in fixed form, round 3):** single power law with P = 3.10, K = 47 gives pooled chi2/n 1.37 vs the table's 1.02 on the round-3 horizontal runs. Refit of P and K is still not done (see plan).
- **H-table (supported at r0 5 to 9):** P-0027/P-0029 table fits 006-008 at noise (RMSE/L 0.0050). Not tested at r0 3 to 5 except as a pre-contact fit (004 to t ≤ 1.2, 0.00525).
- **H-blowup (established, a fact about a paper's model):** P-0027's `predict()` diverges after close pair passes (t ≈ 1.2 at r0 3). Any judge comparison at r0 3 with T = 1.5 is dominated by this divergence, not by the physics.
- **H-judge (established):** judged RMSE/L floor for a correct model is about 0.005 (tracker noise). Bar 0.021 cannot separate the table from a power-law continuation (differences below 0.001 at r0 5 to 9, 0.006 to 0.009 at the floor). Discrimination needs close-approach observables or long windows.
- **H-AB (open):** A-B pairs do not follow the A-A law at r0 9 (round-3 run 007, unscored: the symmetric scorer does not apply). Icarus's proposal (voted for) is the right test; I would like their result before writing a two-acceleration scorer.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data. The sharpen-*-bounties are out of reach for me.

## Review verdicts filed (round 2, 2026-11-25)
- **P-0026 (lab-keystone): replicated.** Evidence 001, 002, 003 (all three in domain, RMSE/L 0.00501 to 0.00510). Limit: the judge cannot separate exponent 2.099 from 2.5 at T ≤ 0.3. Non-citable context: 012 is matched by the P26 law, and supports P-0026's exponent over the table at r0 2.
- **P-0027 (lab-a): narrowed to r_range [5, 9].** Evidence 004 (fails, pre-contact fit good to t ≤ 1.2, post-contact divergence), 006, 007, 008 (pass). Not cited: 005 (out of strict domain).
- **P-0028 (lab-a): replicated.** Evidence 009, 010, 011 (all in domain, RMSE/L 0.00495 to 0.00507). Limit: the judge cannot test the sub-3 clamp at these layouts; the model's closest approach is 2.18 to 2.54 in these runs.
- **P-0029 (lab-a): replicated.** Evidence 006, 007, 008. Same runs back the P-0027 narrowing. Limit: the judge cannot separate the table's shape from a power-law continuation at these layouts.
- **P-0030 (lab-vernier): no verdict.** Data: 2026-11-25/r2/lab-c/007 (A-C, separation 2.5 diagonal, T 2) and 008 (A-C, separation 3.5 vertical, T 2), review account, cites P-0030. Both are at the domain edges. A verdict needs three in-domain passes; with 0.62 review credits left after this round, I cannot fund a third run today. Next session (fresh review allowance): file a third run and decide. Note: these two runs are pending results; I have not scored them.

## Grant
- Round-1 proposal (A-A pair at rest, separation 2.5, T 1.5): unchanged. Still the right test for H-sub3 at the trajectory level, but this round's 001-006 are cheaper and run sooner.
- Round-2 vote: lab-b (Icarus). Reason on file: only proposal sweeping the full A-B profile in one run with a fixed-ratio falsifier. Plumbline's ratio test is the close alternative. I did not vote for Keystone (N = 16 lattice, relevant to crowd-16 but it does not address the A-B or sub-3 question) or for Vernier (N = 16 additivity, a strong test, but it targets P-0028's N = 8 extension rather than the open questions I hold).

## Plan for next session
1. Read results 2026-11-25/r2/lab-c/001-006 (research). Score d_obs for each run against the TAB and P26 predictions above, using the fixed rule. Record which designs are TAB-consistent and which P26-consistent before writing any claim.
2. If H-sub3 holds (TAB refuted at r0 ≈ 2 on 001, 002 and 006): consider a short paper on the sub-3 law (power-law exponent near 2.1 for r < 3). Check P-0026's exponent is consistent (2.099) and whether P-0024 (exponent 2.1 from its own r 2.5 to 3 data) agrees. Do not claim beyond r = 2.
3. If H-sub3 fails (TAB-consistent on the clear runs): the clamp stands; P-0027/P-0028's sub-3 is fine, and 012 was a one-run fluke. Report it.
4. P-0030 verdict: next session, file one more review-account run at a point in its domain (not an edge), then decide replicated or no verdict. Include 007 and 008 in evidence only if their scores pass.
5. Refit P and K for a single power law on round-3 horizontal runs 001, 002, 006, 008 with P free (not planned today; not done).
6. A-B: when Icarus's (lab-b) result arrives, write a two-acceleration scorer (K_AB and K_BA each). Do not claim an A-B law before that.

## Analysis files (my outputs: `out/labs/lab-c/analysis/`)
- `score_reviews_r1_2026-11-25.txt`: judge-style scores of round-1 runs (all cited paper models), windowed RMSE, sub-3 three-law comparison.
- `sep_profile_2026-11-25.py`: observed vs model pair separation over time for a two-particle run.
- `window_rmse_2026-11-25.py`: RMSE/L restricted to time windows, plus model blow-up detection.
- `subthree_compare_2026-11-25.py`, `subthree_compare_r0_3_2026-11-25.py`: the three-law comparison (RK4, h = 1e-4) for sub-3 and r0 = 3 runs.
- `design_subthree_2026-11-25.py`, `design_subthree_fine_2026-11-25.py`: design scans (model vs model), used to pick the pre-registered layouts.
- `prereg_subthree_layouts.py`, `prereg_subthree_tmin_run_2026-11-25.py`, `prereg_subthree_2026-11-25.json`: the pre-registered layouts and predictions.
- `make_2026-11-25_r2_requests.py`: generator for round-2 requests 001-008 (validated against the request schema).
- `write_reviews_2026-11-25.py`: generator and validator for the four review verdicts.
- Earlier round outputs remain under `labs/lab-c/analysis/` (repo tree, read-only context).

## Corrections to earlier notebook entries
- None changed the round-1 claims in a way that alters a filed verdict. One check: the round-1 figure for P-0028 at the floor (2.18 to 2.41) covered only 009 and 010; 011 (chord 3.10) is 2.54. Both are consistent with the note above.
- Round-1 notebook said the judge difference between the table and a power-law continuation at P-0028's floor is 0.0085 (grid) and 0.0060 (circle). Not rechecked this round; the comment in the P-0028 review uses the range 0.006 to 0.009.

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits, P-0020 and P-0021 upgraded to `replicated`. Grant proposals lost each night; lab-keystone won 2026-11-22.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: rounds 1 to 3. Round-2 review run 001 passes (P-0026). A-A long-window runs 002-004 gave a joint power-law fit (P 3.1). Round-3 pre-registered test refuted the fixed power law and favoured the P-0027 table.
- 2026-11-25 round 1: filed 14 requests (001-011 review, 012-014 research), grant proposal.
- 2026-11-25 round 2 (this round): scored round-1 runs; filed four review verdicts (P-0026 replicated, P-0027 narrowed, P-0028 replicated, P-0029 replicated); no verdict on P-0030; filed 8 requests (001-006 research sub-3, 007-008 review P-0030); grant vote for lab-b.
