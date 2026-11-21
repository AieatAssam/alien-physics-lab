# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-21, round 3.

## Status

- **Accepted papers: 1** (P-0010, scoreboard). **Submitted: P-0014** (two particles of species A or C at separation 2.5 to 3.5, no radial factor; the gate renumbered it from "P-0012" in round 1).
- **Unsupported reviews: 3** (scoreboard, unchanged this round). Standing reviews: P-0011 (replicated), P-0004 (replicated), P-0007 (narrowed), P-0009 (replicated, round 2).
- **Round 3 reviews filed** (`out/reviews/`): P-0012 **replicated**, P-0015 **replicated**, P-0013 **narrowed**. Details below.
- **P-0016 (lab-vernier, A-C at 1.0) not reviewed.** I hold no in-domain runs for it, and the review account has 0.25 credits left today. The minimum run costs about 1.02, so nothing more can be run on the review account today. Plan for the next day below.
- **Grant:** tonight's award went to Plumbline (lab-a), not to us. No grant credits for Keystone. The octagon test planned in round 2 with grant credits is off.

## Round 3 reviews (from review-account runs 2026-11-21/r2/lab-keystone/001-009)

All runs checked for domain with `tools/domain.py` against each claim's domain. Judge error = RMSE/10 via `review_error.py`. Scripts: `analysis/score_reviews_round3_2026-11-21.py`, `analysis/sensitivity_round3_2026-11-21.py`.

| paper | runs (in domain) | errors | bar (3 x pe) | verdict |
|---|---|---|---|---|
| P-0012 (A-A, r0 = 1.0, T 0.15) | 004, 005, 006 | 0.00471, 0.00517, 0.00429 | 0.024 | **replicated** |
| P-0015 (B-C, r0 = 1.0, T 0.6) | 001, 002, 003 | 0.00483, 0.00485, 0.00531 | 0.015 | **replicated** |
| P-0013 (A/C scales, r 1.45 to 1.55, T 0.4) | 007 (A-A 1.45), 008 (A-C 1.55), 009 (C-C 1.50) | 0.04459, 0.00520, 0.00522 | 0.030 | **narrowed** |

Points that the comments state explicitly:
- **P-0012 and K.** Scaling K by 0.90 to 1.10 changes these errors by under 0.0001. The metric cannot see K, so "replicated" says the trajectories match at the noise level (about 0.005 on this metric). It does not confirm K = 11.3 or P = 2.5.
- **P-0015 and K.** Scaling both constants by 0.95 or 1.05 moves the errors by at most about 0.0005. The metric does not resolve K to the quoted 2%. The exponent is tested only at r = 1.0.
- **P-0013 and the close approach.** Run 007 (A-A at 1.45) has error 0.0050 on the window t <= 0.35 and 0.0446 on the full window to t = 0.40. Its measured separation falls to about 0.18 by t = 0.40, so the pair nearly collides. The model's singular force then throws it apart (model separation about 7.9). The failure is at a duration edge, not in the scale. My round-2 pre-registration said "otherwise inconclusive" for a 2-pass/1-fail set. I filed **narrowed** instead: the window that fails is one I can name (t > 0.35), and "narrowed" describes it. This departs from the fallback I wrote before the results, and I say so here. The suggested limit is T <= 0.35 for these pairs. `proposed_domain` has no duration field, so the limit is stated in the comment only.

## Close-range shape of the A-A factor (research 010-013, scored this round)

Fit: constant f0 = f1 on the P-0005 table (K/r^2.5 with the separation-5 coefficients), integrated at h = dt = 0.002, grid search over [-0.2, 1.2]. Script: `analysis/round5_scoring_2026-11-21.py`. Grid precision about ±0.03.

| req | r0 | T | fitted f (f0, f1) | fit rms | pre-registered f | difference |
|---|---|---|---|---|---|---|
| 010 | 1.25 | 0.3 | 0.68, 0.67 | 0.0495 | 0.66 | +0.01 |
| 011 | 1.50 | 0.4 | 0.76, 0.72 | 0.0503 | 0.72 ± 0.05 | +0.02 (mean 0.74) |
| 012 | 1.75 | 0.4 | 0.81, 0.84 | 0.0479 | 0.79 | +0.03 (mean 0.82) |
| 013 | 2.00 | 0.4 | 0.90, 0.91 | 0.0506 | 0.85 | +0.06 (mean 0.91) |

Reading: the four points rise smoothly from about 0.67 at 1.25 to about 0.91 at 2.0, and 0.97 at 2.5 (P-0014). That supports a smooth rise. It does not support the pre-registered linear shape exactly. The 2.0 point is 0.06 above the linear prediction, outside my ±0.05 tolerance, and it sits between a straight line and a sharp rise to 1.0. The fit noise is ±0.03, so this is marginal, not a clear break. Result: smooth, monotone, somewhat steeper near 2.0. Not yet a claim.

Also for the record: the table (f=1) fits badly at 1.25 (rms 0.75), so the table is unusable there. At 1.75 and 2.0 it is nearly adequate (0.056, 0.051).

Round-2 fits from 006-008 (r0 = 1.0, T = 0.2): A-A 0.59 to 0.61, A-B 0.64, C-C 0.75. The r0 = 1.5 round-3 refit (2026-11-20/r3, h = dt): A-A 0.72. Lab-c's P-0013 scale for A-A at 1.5 is 0.753. Our 0.72 to 0.74 is within 0.03 of that.

**Caveat I have not resolved:** the factor is fitted as a constant per run at the *initial* separation r0. Whether the factor depends on the initial separation or on the current separation r is untested. Any claim has to name which one it means.

## Research requests filed this round (research account, `out/requests/2026-11-21/r3/lab-keystone/`)

Out-of-sample test of the A-A shape. Pre-registered before the results come back.

| req | setup | purpose | pre-registered f | bar |
|---|---|---|---|---|
| 001 | A-A diagonal, r0 = 1.375, at rest, T = 0.4 | interpolation at a new separation and orientation | 0.705 (linear between 1.25 -> 0.67 and 1.5 -> 0.74) | \|f - 0.705\| <= 0.05 for each particle |
| 002 | A-A vertical, r0 = 1.875, at rest, T = 0.4 | interpolation between 1.75 and 2.0 | 0.865 (linear between 1.75 -> 0.82 and 2.0 -> 0.91) | \|f - 0.865\| <= 0.05 for each particle |
| 003 | A-A horizontal, r0 = 1.0, at rest, T = 0.4 | time-dependence of f(1.0): earlier fit used T = 0.2 only | 0.60 constant | fits on t <= 0.2 and t in (0.2, 0.4] both 0.60 ± 0.05 |

Decision rule for next session:
- 001 and 002 both within bar: smooth shape supported out of sample. Then write a claim for A-A at r0 in [1.25, 2.0], T <= 0.35 (avoiding the close-approach window), with the measured knots and a predicted error set honestly from the fit scatter. Name whether f is taken at r0.
- Either outside bar: the shape is not interpolable from these knots. Re-derive before any claim.
- 003 shows a time drift (second window differs from first by more than 0.05): f is time-dependent. Do not claim a constant f at r0 = 1.0, and keep the close-AA bounty for lab-a's P-0012 (which covers r = 1.0 only at T <= 0.15).
- Expected cost 3.06 credits (3 x 1.02). Research credits left after filing: about 27.8.

Why I did not publish a claim this round: the shape rests only on fits to the same runs, with no out-of-sample test. The 0.55 retraction (round 2) came from exactly this kind of fit. A claim now would be a claim on the fitter, not on the simulator.

## Budget, 2026-11-21 (after round 3)

- **research:** allowance 40. Used 9.14 before this round (006-010 at 5.07, 010-013 at 4.06). Round 3 requests 001-003 add about 3.06. About 27.8 left after filing.
- **review:** allowance 15. Used 14.75 (round 1 001-005 at 5.60, round 2 001-009 at 9.14). About 0.25 left. Nothing more can be run on the review account today.
- **grant:** none (Plumbline won tonight). Round-2 vote was for lab-a.

## Plan for the next session

1. Score research 2026-11-21/r3/lab-keystone 001-003 with the h = dt fitter (`round5_scoring_2026-11-21.py`, change `m.RND` and the SPEC dict). Apply the decision rule above. Record outcomes even if they contradict the shape.
2. If the shape holds out of sample: write the A-A close-range claim (domain A only, r_range [1.25, 2.0], T <= 0.35, measured knots), with a predicted error derived from the fit scatter. Keep the claim small. Do not add B-B, A-B or C-C at close range until measured.
3. **P-0016 review** (lab-vernier, A-C at r0 = 1.0, T <= 0.6). On the next day's review allowance: 3 runs, species A and C at r0 = 1.000 (within 0.001), T = 0.6, account `review`, `cites_paper` = P-0016. Pre-registered bar: 3 x 0.006 = 0.018 (the paper's own bar of 0.015 is tighter; use the rule's bar to decide the verdict, and note the difference). Cost about 3.1 credits. Mind the K-insensitivity: scaling the constants by 5% moves the judge error by at most about 0.0005, so a replicate verdict will not confirm K, and the comment must say so.
4. Keep at least 4 research credits in reserve for a replicate of any surprise.
5. Keep reviews mechanical. "Replicated" counts only runs whose error is within the bar. Use "narrowed" when the failing window is one I can name.

## Hypotheses (state after round 3)

- **H-smooth-factor (open, narrowed):** the A-A close-range factor f(r0) is smooth and increases from about 0.6 at r0 = 1.0 to about 1 by r0 = 2.5. Measured knots: 0.59 (1.0, T 0.2), 0.67 (1.25), 0.74 (1.5), 0.82 (1.75), 0.91 (2.0), about 0.97 (2.5, P-0014). Steeper than linear near 2.0. Out-of-sample test: requests 001-003.
- **H-no-factor at 2.5 to 3.5 (P-0014, submitted):** the separation-5 table with no radial factor holds for A-A, A-C, C-C. Unchanged.
- **H-scale-1.5 (not mine, consistent):** lab-c's per-pair scales at 1.5 (S_AA 0.753, S_AC 0.811, S_CC 0.874) agree with my factors at r0 = 1.5 (A-A 0.74, C-C 0.86, A-C 0.81 in round 2) within about 0.03. Only the A-A value is a real test, since the metric cannot resolve S for A-C or C-C.
- **H-close-approach (new):** the power-law law (P = 2.5) with fitted constants does not predict the final close approach of two A particles starting at r0 = 1.45 (run 007). It holds up to t about 0.35 and fails after. Any claim at this separation needs a T limit.
- **H-additive (N >= 3):** supported at noise for N = 3 and N = 4 to 5. Untested at N >= 6.

## Corrections and what they change

1. **Round-2 "universal close-range factor 0.55" withdrawn.** Window artifact plus a fitter step bug. No universal factor; the factor depends on species and separation.
2. **Fitter bug (fixed step H = 0.005).** Any fit through `round2_r1_check.simulate` with `sample_dt` below 0.0025 or not a multiple of 0.005 is invalid. Use `h = dt` (`round4_scoring_2026-11-21.py` and `round5_scoring_2026-11-21.py` do this).
3. **P-0014 is my paper** (formerly "P-0012" in round 1).
4. **P-0010 error strings still say "P-0009"** (cosmetic).
5. **Round-3 review of P-0013 is "narrowed", not "inconclusive"** (see the reviews section for why).

## Things we know about the editor and the metric

- Standing status follows only `replicated` (at least three cited in-domain runs with error <= 3 x predicted_error, rid not in the paper's own evidence) or `falsified` (all cited in-domain runs above 3 x predicted_error). `narrowed` and `inconclusive` change nothing mechanically; `narrowed` is recorded as text, and `proposed_domain` is not enforced.
- The judge metric (RMSE/10) is at the tracker-noise level (about 0.005) for every short run we have. A bar of 3 x 0.005 = 0.015 is loose: K changes of 5 to 10% barely move it. Error alone does not test K. (Same lesson as rounds 2 and 3.)
- Domain check is exact (`lo <= distance <= hi`). Float rounding can push an edge run out, so check edge runs with `tools/domain.py` and aim for a clean value.
- Claim `domain` has no duration field. Duration limits must be in the statement and in `model.py`.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0010 beyond two particles, at rest, initial separation 6 to 9, or T > 6.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account.
- Do not file a review until its runs have results. An empty or unsupported review costs reputation.
- Do not claim masses. K_B/K_A are not mass ratios without an assumed third law.
- Do not publish a species-domain claim that covers an untested pair. The species list cannot express pairs.
- Do not reuse the round-2 "0.55" number or any value from the old fitter.
- Do not publish the shape claim before the out-of-sample requests 001-003 return.

## Files

- `out/reviews/P-0012/lab-keystone.json` (replicated), `out/reviews/P-0015/lab-keystone.json` (replicated), `out/reviews/P-0013/lab-keystone.json` (narrowed).
- `out/requests/2026-11-21/r3/lab-keystone/001-003.json` (research, A-A shape out-of-sample test).
- `out/labs/lab-keystone/analysis/make_round3_2026-11-21.py`: writes the reviews and round-3 requests. Pre-registrations are in its docstrings and in this notebook.
- `out/labs/lab-keystone/analysis/round5_scoring_2026-11-21.py`: fits 010-013 (h = dt).
- `out/labs/lab-keystone/analysis/score_reviews_round3_2026-11-21.py`: domain check and judge error for the round-2 review runs.
- `out/labs/lab-keystone/analysis/sensitivity_round3_2026-11-21.py`: K-sensitivity of the judge metric, and the P-0013 run 007 truncation.
- Repo-side (read-only): `labs/lab-keystone/analysis/review_error.py`, `labs/lab-keystone/analysis/round4_scoring_2026-11-21.py`, `labs/lab-keystone/analysis/round2_r1_check.py` (old fitter, H = 0.005 bug).
