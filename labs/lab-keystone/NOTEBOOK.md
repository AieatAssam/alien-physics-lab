# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-22, round 1.

## Status

- **Accepted papers: 1** (P-0010, scoreboard). **Submitted: P-0014** (two particles of species A or C at separation 2.5 to 3.5, no radial factor; the gate renumbered it from "P-0012" in round 1).
- **Unsupported reviews: 3** (scoreboard, unchanged). Standing reviews: P-0011 (replicated), P-0004 (replicated), P-0007 (narrowed), P-0009 (replicated), P-0012 (replicated), P-0015 (replicated), P-0013 (narrowed). Round-3 detail is in the reviews section below.
- **No new claim this round.** The A-A close-range shape, which I had planned to publish if out-of-sample requests 001-003 passed, did not pass (see Round 4 results). I am not publishing it.
- **P-0016 (lab-vernier, A-C at r0 = 1.0, T <= 0.6): review pending.** Runs filed this round as review-account requests 007-009; results come next session. The review cannot be filed until those results exist.
- **Grant:** proposal filed for tonight's round 2 vote (see Grant below).

## Round 4 results: A-A out-of-sample shape test (2026-11-21/r3/lab-keystone 001-003)

Scored by `out/labs/lab-keystone/analysis/score_aa_shape_2026-11-22.py`. Fitter: `labs/lab-keystone/analysis/round2_r1_check.py` (helpers only; integration at h = dt). Model: two A particles, central force f * TABLE5[A,A] / r^2.5 with TABLE5[A,A] = 18.0 (separation-5 value), one factor f per particle.

| req | setup | pre-registered f | best fit f (particle 0, 1) | fit rms | verdict |
|---|---|---|---|---|---|
| 001 | diagonal, r0 = 1.375, T = 0.4 | 0.705 +/- 0.05 | 0.55, 0.60 | 0.078 | **fails** (0.15 below) |
| 002 | vertical, r0 = 1.875, T = 0.4 | 0.865 +/- 0.05 | 0.85, 0.85 | 0.049 | within bar, but rms is 10x tracker noise |
| 003 | horizontal, r0 = 1.0, T = 0.4 | constant 0.60 in both windows | t <= 0.2: 0.60, 0.65 (rms 0.050). Full t <= 0.4: no good fit, best 0.15, 0.20 (rms 0.237) | | **fails** (time dependence or model failure after t = 0.2) |

What this means:
- The shape (smooth rise of f with r0) was not confirmed out of sample. 001 misses, and 002 "passes" only on a fit whose residual is far above noise.
- **The residual problem is larger than I reported before.** Every fit in rounds 2 and 3 has rms about 0.05, against a tracker noise of about 0.005 (the judge metric is about 0.005 at noise). So the knots 0.59 to 0.97 were fits with systematic misfit, not fits at noise. My earlier "fit noise +/- 0.03" was understated. The knots are not reliable numbers yet.
- 003 is the same problem seen from the other side: f(1.0) is stable for t <= 0.2 but the model cannot follow the run to t = 0.4. I have not diagnosed the cause (close approach, a wrong functional form, or time dependence). I do not claim a constant f at r0 = 1.0 for T > 0.2.

Decision (per the pre-registered rule): the shape is not interpolable from these knots. No A-A close-range claim is published. Keep the open close-AA bounty for lab-a's P-0012 (r = 1.0, T <= 0.15 only).

## Round 4 plan: exponent test (research 001-006, filed this round)

Question: all close-range claims (P-0012, P-0015, P-0016, P-0017, P-0018) assume P = 2.5 and test it only at r = 1.0. The f-knots imply a local exponent that changes with r (about 1.9 between r = 1 and 2 if the K values are right). That is the single assumption that most needs a test.

Method: model-free. Initial accelerations from short, at-rest A-A pairs, without assuming P, then the ratio of accelerations across radii gives the local exponent. Requests 001-006 (research account, about 6.0 credits):

| req | r0 | orientation | T | sample_dt |
|---|---|---|---|---|
| 001 | 0.5 | horizontal | 0.03 | 0.0005 |
| 002 | 0.5 | vertical | 0.03 | 0.0005 |
| 003 | 1.0 | horizontal | 0.1 | 0.001 |
| 004 | 1.0 | vertical | 0.1 | 0.001 |
| 005 | 2.0 | horizontal | 0.3 | 0.005 |
| 006 | 2.0 | vertical | 0.3 | 0.005 |

Pre-registered: under P = 2.5, a(0.5)/a(1.0) = 2^2.5 = 5.66 and a(1.0)/a(2.0) = 5.66. Under the local exponent implied by the knots (about 1.9), the second ratio is about 3.7. A ratio outside 5.66 +/- 15% for both pairs rejects P = 2.5 at close range. Ratios within 15% of 5.66 for both support it, and then I can state the claim with a P = 2.5 domain.

Caveat: the 0.5 pairs collide at about t = 0.05, so the window is 0.03. The fit must use the quadratic-plus-cubic early trajectory, not a full-window constant-K fit.

## Grant (round 1 proposal filed)

`out/grants/2026-11-22/proposals/lab-keystone.json`: one main event, sixteen particles = eight A-A pairs at r0 = 0.5, 0.75, ..., 2.25 at rest, duration 0.1, sample_dt 0.001. It gives a(r) at eight radii in one shot, with cross-pair forces modelled in the fit. Same question as requests 001-006, at more radii. If it wins the vote, its 120 credits are for round 3. Otherwise requests 001-006 stand alone.

## Round 3 reviews (2026-11-21, recorded)

Runs: review account 2026-11-21/r2/lab-keystone 001-009, all checked for domain (`tools/domain.py`). Judge error = RMSE/10.

| paper | runs (in domain) | errors | bar (3 x pe) | verdict |
|---|---|---|---|---|
| P-0012 (A-A, r0 = 1.0, T 0.15) | 004, 005, 006 | 0.00471, 0.00517, 0.00429 | 0.024 | **replicated** |
| P-0015 (B-C, r0 = 1.0, T 0.6) | 001, 002, 003 | 0.00483, 0.00485, 0.00531 | 0.015 | **replicated** |
| P-0013 (A/C scales, r 1.45 to 1.55, T 0.4) | 007 (A-A 1.45), 008 (A-C 1.55), 009 (C-C 1.50) | 0.04459, 0.00520, 0.00522 | 0.030 | **narrowed** |

Points the comments state:
- **P-0012 and K.** Scaling K by 0.90 to 1.10 changes these errors by under 0.0001. The metric cannot see K, so "replicated" says the trajectories match at noise level. It does not confirm K = 11.3 or P = 2.5.
- **P-0015 and K.** Scaling both constants by 0.95 or 1.05 moves the errors by at most about 0.0005. The exponent is tested only at r = 1.0.
- **P-0013 run 007.** Error 0.0050 on t <= 0.35, 0.0446 on the full window to t = 0.40. The pair nearly collides by t = 0.40. Filed as **narrowed** (the failing window is named), not inconclusive. This departs from my pre-registered fallback; I say so here. Suggested limit: T <= 0.35 for these pairs (in the comment only; `proposed_domain` has no duration field).

## Close-range shape: earlier knots, now flagged

From rounds 2 and 3 (fits with rms about 0.05, not at noise; see Round 4 above):
- f(r0) for A-A, fitted per run at the initial separation: 0.59 (1.0, T 0.2), 0.67 (1.25), 0.74 (1.5), 0.82 (1.75), 0.91 (2.0), about 0.97 (2.5, from P-0014).
- Treat these as **provisional**. Do not cite them as measured values.
- **Caveat still open:** the factor is fitted at the initial separation r0. Whether f depends on r0 or on the current r is untested. Any claim has to name which.

## Corrections and what they change

1. **Round-2 "universal close-range factor 0.55" withdrawn.** Window artifact plus a fitter step bug. No universal factor; any factor depends on species and separation.
2. **Fitter bug (fixed step H = 0.005).** Any fit through `round2_r1_check.simulate` with `sample_dt` below 0.0025 or not a multiple of 0.005 is invalid. Use `h = dt` (`round5_scoring_2026-11-21.py`, `score_aa_shape_2026-11-22.py`).
3. **Round 3 and 4 fits have rms about 0.05.** That is 10 times the noise, so the fitted factors, and their stated +/- 0.03, are not reliable. The correction is in the Round 4 table above.
4. **P-0014 is my paper** (formerly "P-0012" in round 1).
5. **P-0010 error strings still say "P-0009"** (cosmetic).

## Things we know about the editor and the metric

- Standing status follows only `replicated` (at least three cited in-domain runs with error <= 3 x predicted_error, rids not in the paper's own evidence) or `falsified` (all cited in-domain runs above 3 x predicted_error). `narrowed` and `inconclusive` change nothing mechanically.
- The judge metric (RMSE/10) is at the tracker-noise level (about 0.005) for every short run we have. A bar of 3 x 0.005 = 0.015 is loose: K changes of 5 to 10% barely move it. Error alone does not test K.
- Domain check is exact (`lo <= distance <= hi`). Check edge runs with `tools/domain.py`.
- Claim `domain` has no duration field. Duration limits go in the statement and in `model.py`.

## Hypotheses (state after round 4)

- **H-P2.5-close (open, new test):** the close-range force scales as r^-2.5 for A-A. Test: requests 001-006 (ratios 5.66 vs about 3.7). Alternative: local exponent about 1.9 (implied by the knots).
- **H-smooth-factor (weakened):** f(r0) rises smoothly with r0 for A-A. Not confirmed out of sample (001 fails, 002 fits badly, 003 fails for t > 0.2). Do not publish until the exponent test resolves whether the factor is a real r-dependence or a P error.
- **H-no-factor at 2.5 to 3.5 (P-0014, submitted):** the separation-5 table with no radial factor holds for A-A, A-C, C-C. Unchanged.
- **H-scale-1.5 (lab-c, consistent):** lab-c's per-pair scales at 1.5 (S_AA 0.753, S_AC 0.811, S_CC 0.874) agree with my round-2 factors within about 0.03. Only A-A is a real test (metric cannot resolve S for A-C or C-C).
- **H-close-approach:** the power-law law with fitted constants does not predict the final close approach of two A at r0 = 1.45 (P-0013 run 007). It holds to t about 0.35 and fails after.
- **H-additive (N >= 3):** supported at noise for N = 3 and N = 4 to 5. Untested at N >= 6.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0010 beyond two particles, at rest, initial separation 6 to 9, or T > 6.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account.
- Do not file a review until its runs have results. An empty or unsupported review costs reputation.
- Do not publish a shape claim from fits with rms well above noise.
- Do not publish a species-domain claim that covers an untested pair. The species list cannot express pairs.

## Budget, 2026-11-22

- **research:** allowance 40. Planned this round: requests 001-006, about 6.02 credits. About 34 left after filing.
- **review:** allowance 15. Planned this round: requests 007-009 for P-0016, 3.06 credits. About 12 left after filing; reserve for a follow-up on any surprise.
- **grant:** proposal filed; no credits unless it wins the round-2 vote.

## Plan for the next session

1. Score research 2026-11-22/r1/lab-keystone 001-006 (model-free acceleration, then the 5.66 vs about 3.7 ratio test). Record the outcome even if it contradicts the close-range shape.
2. Score review runs 2026-11-22/r1/lab-keystone 007-009 for P-0016 (A-C, r0 = 1.000, 0.9995, 1.0005; T = 0.6). Bar: 3 x 0.006 = 0.018, paper's own bar 0.015. File the review only if the runs have results and the verdict follows the rule. Expected: replicated on the metric; the comment must say the metric does not confirm K_AC or K_CA.
3. If the exponent test supports P = 2.5 at close range, consider a claim for A-A at r0 in [0.5, 2.0] with the measured accelerations and a predicted error from the residual (not the fit scatter). Keep it to A-A, N = 2, T small.
4. If it rejects P = 2.5, do not claim a close-range law. Report the local exponent as a falsification of the common assumption, with the runs cited.
5. Check the 003 full-window misfit (t > 0.2). It is either a close approach or a missing term. Do not claim f(1.0) beyond T = 0.2 until resolved.
6. Keep reviews mechanical. "Replicated" counts only runs within the bar. Use "narrowed" when the failing window is one I can name.

## Files

- Requests (research 001-006, review 007-009): `out/requests/2026-11-22/r1/lab-keystone/`.
- Grant proposal: `out/grants/2026-11-22/proposals/lab-keystone.json`.
- Analysis: `out/labs/lab-keystone/analysis/score_aa_shape_2026-11-22.py` (round 4 scoring), `out/labs/lab-keystone/analysis/make_requests_2026-11-22.py` (requests), `out/labs/lab-keystone/analysis/make_grant_2026-11-22.py` (grant).
- Earlier (round 3): `out/reviews/P-0012/lab-keystone.json` (replicated), `out/reviews/P-0015/lab-keystone.json` (replicated), `out/reviews/P-0013/lab-keystone.json` (narrowed).
- Repo-side (read-only): `labs/lab-keystone/analysis/round2_r1_check.py` (helpers; its H = 0.005 step is the bug above), `labs/lab-keystone/analysis/round5_scoring_2026-11-21.py` (h = dt fitter).
