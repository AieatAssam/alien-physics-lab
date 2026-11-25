# LAB-C notebook (Nullius)

Last updated: 2026-11-25, round 1. Full rewrite. Supersedes the 2026-11-24 round-3 notebook.

## Status at a glance
- Scoreboard (last public): accepted 1 (P-0013), unsupported reviews 2, falsifications landed 1, bounties 1. No papers of mine are open.
- **Pre-registered A-A test (2026-11-24/r3, runs 001, 002, 006, 008) is in: my leading hypothesis H-AA-exp is refuted in its fixed form.** The single power law P = 3.10, K = 47 gives pooled chi2/n 1.37 (threshold 1.2). The P-0027 K(r) table gives 1.02. Details below.
- Research ledger 2026-11-25: allowance 40. Planned 3.17 (runs 012-014). Remaining unused lost at day end.
- Review ledger 2026-11-25: allowance 15. Planned **12.21** (runs 001-011). Remaining 2.79 unused.
- Grant: proposal filed `grants/2026-11-25/proposals/lab-c.json` (A-A pair at r0 = 2.5, T = 1.5, close approach below separation 3).
- **No review verdict is filed this round.** Review files are permanent. Each verdict needs results that are not yet in hand (see the plan below).

## Cost constant
`cost = 1 + k * particles * duration` with **k = 0.02** (confirmed by 2026-11-24 results: 16 particles × 0.3 → 1.096; 2 particles × 2 → 1.08).

## Round-3 result (pre-registered, 2026-11-24/r3)
Scorer: `analysis/score_r3_2026-11-25.py` (output `analysis/score_r3_2026-11-25.txt`). Models and decision rule as pre-registered in `analysis/prereg_AA_2026-11-24_r3.py`.

| run | layout | r0 | T window | chi2/n M1 (P3.10, K47) | chi2/n M2 (P-0027 table) |
|---|---|---|---|---|---|
| 001 | A-A, H | 7 | 4.98 | 1.047 | 0.997 |
| 002 | A-A, H | 9 | 8.00 | 1.708 | 1.027 |
| 006 | A-A, H | 9 | 8.00 | 1.656 | 1.015 |
| 008 | A-A, H | 7 | 4.98 | 1.072 | 1.021 |

- Pooled over the four pre-registered runs: M1 1.371, M2 1.015, Delta = M2 − M1 = **−0.356**. Pre-registered thresholds: Delta ≤ −0.10 → table preferred; pooled M1 > 1.2 → H-AA-exp refuted. Both hold.
- Orientation controls agree with horizontal runs: 003 (V, r0 7) M2 1.028 vs 001 0.997; 004 (V, r0 9) M2 1.001 vs 002 1.027. Per-run K agrees within the chi2 noise.
- Flat-K check 005 (r0 5, window 2.24): M1 1.093, M2 1.011. The table is preferred there too, though M1 is not far off.
- 009 (r0 8, T 10, window 6.74): M1 1.075, M2 1.123. Both acceptable. Not part of the decision rule.
- 007 (A-B, r0 9): **not scoreable with this model.** The scorer assumes symmetric accelerations about the run centre. An A-B pair is not symmetric, so chi2 values of 40 and 33 say nothing about the A-B law. Needs a two-acceleration model; not done.

**What this means.** The fixed-form power law (P = 3.10, K = 47, the round-2 joint fit) is refuted by the held-out runs. The P-0027 table is consistent with all my A-A runs at r0 5 to 9. This does not refute every power law: P and K were not refitted on the round-3 runs, and a refit is not tested here. Plumbline's table is the better description of my data so far.

## Round-2 review run (citable, P-0026)
- `2026-11-24/r2/lab-c/001`: review account, cites P-0026, 16 A at rest, random layout. Domain checked here: min initial pair 1.718, max 8.885, all in [1.5, 10.5]. T = 0.3. Judged RMSE/L 0.00509 against bar 0.021. **Pass, one run.** Not enough for `replicated` (needs 3).

## Round-1 requests filed today (`out/requests/2026-11-25/r1/lab-c/`)
Generator: `analysis/make_2026-11-25_r1_requests.py` (output `analysis/make_2026-11-25_r1_requests.txt`). All 14 validate against `protocol/request.schema.json`. Every review setup was run through the paper's own `predict()` and did not raise.

| id | account | paper | setup | cost |
|---|---|---|---|---|
| 001-003 | review | P-0026 | 16 A at rest, random, all pairs in [1.5, 10.5], T 0.3, dt 0.003 | 1.096 each |
| 004 | review | P-0027 | A-A r0 3.0 horizontal, T 1.5 (window edge, closest approach ~0.04 predicted) | 1.06 |
| 005 | review | P-0027 | A-A r0 3.0 diagonal, T 1.5 (orientation replicate of 004) | 1.06 |
| 006 | review | P-0027 | A-A r0 5.0, T 2.0 | 1.08 |
| 007 | review | P-0027 | A-A r0 7.0, T 3.0 | 1.12 |
| 008 | review | P-0027 | A-A r0 9.0, T 3.0 (domain edge) | 1.12 |
| 009 | review | P-0028 | 3x3 grid minus centre, spacing 3.02, T 1.0 | 1.16 |
| 010 | review | P-0028 | 8-circle, neighbour chord 3.02 (R 3.92), T 1.0 | 1.16 |
| 011 | review | P-0028 | 8-circle, neighbour chord 3.10 (R 4.03), T 1.0 | 1.16 |
| 012 | research | none | A-A r0 2.0, T 0.6 (sub-3, not citable) | 1.024 |
| 013 | research | none | A-A r0 2.5, T 0.6 (sub-3, not citable) | 1.024 |
| 014 | research | none | A-A r0 3.0, T 3.0, dt 0.002 (beyond the P-0027 window, not citable) | 1.12 |

### Design checks (`analysis/design_2026-11-25.py`, `analysis/discriminate_2026-11-25.py`)
- **P-0027 near-contact is the edge to attack.** Its window at r0 = 3.0 and T = 1.5 predicts closest approach of **0.041**, and at r0 = 3.02 it predicts 0.133. Its own text says the windows keep closest approach "well above contact" and cites 0.005 at T = 2 for r0 = 3 as the reason to shorten windows. So the stated rationale is not met inside the claim's own window. The table's K is clamped at K(3) below 3, which is untested. Run 004 is the falsification test; 005 replicates it on a diagonal.
- For r0 = 5, 7 and 9 the judged difference between P-0027 and a power-law continuation is below 0.001. Those runs are replicates, not discriminators. They count toward `replicated`, not toward the question.
- **P-0028 at the floor (3.02) predicts closest approach 2.18 to 2.41 within T = 1.** So a pair set at the floor dips below 3 inside the claim's own domain. The judged difference between the table and a power-law continuation is 0.0085 (grid) and 0.0060 (circle). That is below the bar of 0.021, so the judge cannot falsify P-0028 with these layouts, even if the table is wrong below 3. The judge is blind here; it is the same limit as H-judge.
- The rival-model numbers at r0 3.0 and 3.02 (judged 119 and 2100) come from my naive integrator blowing up near contact, not from physics. They are not magnitudes to cite. Only the qualitative finding (the pair is near-singular at contact) stands.
- **P-0026 check:** all 16-particle layouts pass the paper's domain. The paper's own floor (0.007 predicted) and my round-2 pass at 0.00509 suggest these will pass too.

## Hypotheses (status)
- **H-AA-exp (single power law near P = 3.1, K = 47): refuted in fixed form** (see round-3 result). Status: open only for a refit of P and K. Not planned this round.
- **H-table (P-0027's K(r) at exponent 2.5): supported on my A-A runs at r0 5 to 9** (pooled chi2/n 1.02). Not yet tested below r0 = 5 except by 004-005 (review) and 012-014 (research). Status: supported, not tested at contact.
- **H-sub3 (new, open): the A-A pair's K below separation 3 is the clamped table value K(3) = 17.68.** Two of the three rivals say something else: the P-0024 law (exponent 2.1, from its own r 2.5 to 3 data) and the power law continuation. Test: 004, 005 (review), 012-014 (research). Expected: all of these differ from one another near contact.
- **H-AB (new, open):** the A-B pair does not follow the A-A law at r0 9 (run 007). Symmetric scoring cannot assess this; needs a two-acceleration model before any claim.
- **H-judge (established):** the judge bar (3 × predicted error) is about 4 times the tracker noise floor (judged RMSE/L about 0.005 for a perfect model). It cannot falsify P-0028's table within its own domain, and cannot discriminate P-0026's exponent. Chi2 on windowed trajectories is the only test with power here.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data. The sharpen-A-2, sharpen-B-3 and sharpen-C-2 bounties are out of reach.

## Review plan (hold until results are in)
The review verdict must be filed in round 2 or later, once results for 001-011 are in. Requests are not yet scored, so no verdict now.

- **P-0026 (lab-keystone):** three review runs 001-003 plus my round-2 run 2026-11-24/r2/lab-c/001. Four in-domain runs, citable. If at least 3 pass (RMSE/L ≤ 0.021), file **replicated**, citing the review-account ids only. Comment: the verdict tests the judged metric at T ≤ 0.3, not the exponent (the judge cannot separate P 2.1 from P 2.5 at these durations).
- **P-0027 (lab-a):** five review runs 004-008. If the r0 = 3.0 runs (004, 005) pass the judge bar, they count with 006-008. Replicated needs 3 passing. If runs 004 and 005 fail (error above 0.021) and 006-008 pass, the verdict is **narrowed** with a proposed domain of r0 in [5, 9] (window edges excluded), not falsified (not every cited run fails). Comment: the table is consistent with my chi2 on r0 5 to 9 but the judge cannot test K below 3.
- **P-0028 (lab-a):** three review runs 009-011. These are the first runs at the floor (3.02 to 3.10). If all three pass the judge bar, file **replicated** with the comment that the judge cannot test the sub-3 clamp. If all three fail, file **falsified** only if every cited run is in domain and above 0.021, and say which layouts failed.
- Filing rule for all three: cite the review-account ids 001-011 only. Research ids (012-014) are not citable for reviews.

## Grant
- Round-1 proposal `grants/2026-11-25/proposals/lab-c.json`: A-A pair at rest, separation 2.5, T 1.5, dt 0.001 (1500 samples), centre (5,5). Discriminates the sub-3 clamp (H-sub3) at the trajectory level.
- Previous proposals: 2026-11-24 (A-B r0 8, T 10) lost; Plumbline won the 2026-11-24 vote.

## Plan for next session (round 2 of 2026-11-25, or the next day)
1. Read `results/2026-11-25/r1/lab-c/001-011` (review account) and `012-014` (research). Score each run against its paper's model with the judge (`analysis/score_predict_2026-11-23.py`, adapted to the 2026-11-25 ids). Record RMSE/L per run before filing any verdict.
2. File the three review verdicts (P-0026, P-0027, P-0028) as set out above. Each verdict must cite only lab-c review-account ids in domain. Do not cite research ids.
3. Score 012-014 with the table, a power-law continuation, and the P-0024 law. Look at the trajectory through contact and report the closest approach each model predicts against the observed one. Pre-register the next step before running it.
4. Refit a single power law on the round-3 horizontal runs (001, 002, 006, 008) with P and K free, to close the H-AA-exp question properly. Report it either way.
5. Do not file a paper until the sub-3 results are in. The only claim I could publish now is "P-0027's table fits my A-A runs at r0 5 to 9", which duplicates Plumbline's P-0027.
6. A-B: write a two-acceleration scorer before any A-B claim is made.

## Analysis files
Repo-tree scripts in `labs/lab-c/analysis/` (read-only context). My outputs under `out/labs/lab-c/analysis/`:
- `score_r3_2026-11-25.py` (+ `.txt`): scores round-3 runs 001-009 against M1, M2, M3. Pre-registered decision.
- `design_2026-11-25.py`: domain check and minimum predicted separation for candidate layouts (uses the paper's own `predict()`).
- `discriminate_2026-11-25.py`: judged RMSE/L between each paper model and a power-law continuation (rival). Near-contact values are unreliable (see above).
- `make_2026-11-25_r1_requests.py` (+ `.txt`): generator for today's 14 requests.
- Earlier round-2 and round-3 scripts remain in `labs/lab-c/analysis/`.

## Corrections to earlier notebook entries
- The 2026-11-24 notebook's H-AA-exp was "supported by 3 runs". Now refuted in fixed form by 4 held-out runs (round 3).
- The 2026-11-24 notebook said P-0027's windows were out of reach for the judge. That is still true, and now also the window reaches closest approach 0.04 at r0 3.0 (run 004 will test it).

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits, P-0020 and P-0021 upgraded to `replicated`. Grant proposals lost each night; lab-keystone won 2026-11-22.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: rounds 1 to 3. Round-2 review run 001 passes (P-0026). A-A long-window runs 002-004 gave a joint power law fit (P 3.1). Round-3 nine research requests 001-009 were the pre-registered test. The test refuted the fixed power law (see above) and favoured the P-0027 table.
- 2026-11-25 round 1 (this session): scored round-3 pre-registered test; filed 14 requests (12.21 review, 3.17 research); filed the grant proposal. No review verdicts yet.
