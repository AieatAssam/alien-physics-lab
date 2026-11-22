# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-22, round 2.

## Status

- **Accepted papers: 1** (P-0010, scoreboard). **Submitted: P-0014** (two particles of species A or C at separation 2.5 to 3.5, no radial factor).
- **Unsupported reviews: 3** (scoreboard, unchanged). Standing reviews: P-0011 (replicated), P-0004 (replicated), P-0007 (narrowed), P-0009 (replicated), P-0012 (replicated), P-0015 (replicated), P-0013 (narrowed).
- **No new claim published.** The A-A exponent evidence is not yet strong enough (see below).
- **Round-2 filed this session:** review P-0016 (replicated, see below); votes; requests r2 001-012.

## Round 2 actions (2026-11-22)

1. **Vote:** `out/grants/2026-11-22/votes/lab-keystone.json` votes for **lab-vernier** (single-pair far-field infall). Reason: it tests the P = 2.5 assumption over r 9 to about 4, the separation range nobody else is probing, with pre-set falsifiers. My own close-range fits dispute P at r 1 to 2, so the far-field test answers the most useful open question. (I did not vote for my own proposal.)
2. **Review P-0016 (lab-vernier, A-C at r0 = 1.0, T <= 0.6): replicated.** `out/reviews/P-0016/lab-keystone.json`, evidence 2026-11-22/r1/lab-keystone 007, 008, 009. Judged errors 0.00446, 0.00491, 0.00502 against bar 3 x 0.006 = 0.018. Comment states the metric is K-insensitive: 5% K scale moves the error by about 0.0005, 10% by at most 0.0012 (checked this session, `out/labs/lab-keystone/analysis/score_round1_2026-11-22.py`).
3. **Requests filed (round 2, date 2026-11-22):** `out/requests/2026-11-22/r2/lab-keystone/`:
   - 001-003 research: A-A exponent replicate at r0 = 1.0, T = 0.1, dt 0.001, horizontal / vertical / diagonal.
   - 004-006 research: A-A exponent replicate at r0 = 2.0, T = 0.3, dt 0.005, horizontal / vertical / diagonal.
   - 007-009 review (cites P-0019): B-B at r0 = 1.000 / 0.999 / 1.001, T = 0.3 (the claim's T edge).
   - 010-012 review (cites P-0021): A-B at sep 6.901 / 7.000 / 7.099, T = 6 (the claim's domain edges and full duration).
   - Generator: `out/labs/lab-keystone/analysis/make_requests_round2_2026-11-22.py`. Cost about 6.0 research and 6.6 review (review budget 11.94 remaining before filing).
   - Results come next session. **Do not file the P-0019 or P-0021 reviews until they have results.**

## Exponent test: round 1 results (2026-11-22/r1/lab-keystone 001-006)

**The model-free method I pre-registered does not work at these designs.** Tracker noise is about 0.05 per coordinate (judged RMSE/L 0.005 corresponds to RMSE about 0.05 in position units; I had written 0.005 before, which was the judged unit). A quadratic-plus-quartic fit to the 0.03 and 0.1 windows gave |a| values of 500 to 6000 with residual rms 0.06 to 0.07, which is noise, not signal. The 0.5 pairs move only about 0.05 in 0.03 time, which is below the noise per sample. Lesson: a local-acceleration estimate needs a signal (displacement 1/2 a t^2) well above 0.05 per coordinate. Check that before pre-registering a ratio test.

**Trajectory fit instead** (`out/labs/lab-keystone/analysis/exponent_fit_2026-11-22.py`, `exponent_ratio_2026-11-22.py`): relative radial law q'' = -g/q^P, fitted on |p1 - p0| by grid search, pooled over orientations, RK4 at sample_dt/5.

| r0 | runs | fitted g (P = 2.5) | 1-sigma interval | a(r0) = g/r0^2.5 | rms (noise-like) |
|---|---|---|---|---|---|
| 0.5 | 001, 002 | 14.30 | [8.81, 18.90] | 80.9 +/- 28.6 | 0.067 |
| 1.0 | 003, 004 | 20.95 | [18.56, 22.75] | 20.95 +/- 2.1 | 0.070 |
| 2.0 | 005, 006 | 30.93 | [29.38, 32.41] | 5.47 +/- 0.27 | 0.064 |

- **a(1.0)/a(2.0) = 3.83 +/- 0.43.** P = 2.5 predicts 5.66 (about 1.8 sigma away). Local exponent 1.9 predicts 3.7 (consistent). This favours a local exponent below 2.5 at r 1 to 2, weakly.
- **a(0.5)/a(1.0) = 3.86 +/- 1.42.** Not constraining.
- Free-exponent fits (P varied) are flat: rms unchanged across P, and P runs to the grid edges. **These runs do not measure P by themselves.** The conclusion rests on the local acceleration at each r0, which depends on the P = 2.5 shape only weakly over these windows (displacement is small). It is not model-free.
- **Caveats:** sigma is taken from the best-fit rms; the Delta-rms interval is approximate; the r0 = 2 window is 0.3 long with displacement about 0.5 in relative separation. Not a publishable exponent result yet.
- **Consistency with the old knots:** the f-knots gave local exponent about 1.9. The new a(1)/a(2) ratio agrees.

Round-2 requests 001-006 are the replicate: pre-registered P = 2.5 predicts a(1.0)/a(2.0) = 5.66; local exponent 1.9 predicts 3.7; decision rule: a combined ratio (round 1 and round 2 pooled) outside 5.66 +/- 15% rejects P = 2.5 at close range, and inside 3.7 +/- 15% supports a local exponent near 1.9. Pool the 1.0 and 2.0 groups separately across rounds; do not pool across r0.

## Review of other papers: what is in hand

| paper | claim (domain) | my status |
|---|---|---|
| P-0016 (lab-vernier, A-C r0 = 1.0, T <= 0.6) | K_AC, K_CA | **filed, replicated** (metric K-insensitive) |
| P-0017 (lab-b, B-B r0 = 1.0, T <= 0.15) | K = 3.98 | not reviewed (T at the claim edge is short; replicates would be K-insensitive) |
| P-0018 (lab-b, C-C r0 = 1.0, T <= 0.15) | K = 9.31 | not reviewed (same) |
| P-0019 (lab-a, B-B r0 = 1.0, T <= 0.3) | K = 3.86 | runs 007-009 filed, pending results |
| P-0020 (lab-b, A-B r0 = 1.0, T <= 0.15) | K_AB, K_BA | not reviewed |
| P-0021 (lab-vernier, A-B sep 6.9-7.1, T <= 6) | K_A(B) 7.75, K_B(A) 10.97 | runs 010-012 filed, pending results. Longest run; most sensitive to K and to constancy as the pair closes from 7 to about 4.4 |

Rule for each: `replicated` needs 3 in-domain runs (not the paper's own evidence) with error <= 3 x predicted_error. Use `narrowed` when the failing window is named. Do not file an unsupported review.

## Hypotheses (state after round 2)

- **H-P2.5-close (open, weakened):** the close-range A-A force scales as r^-2.5. Current evidence: a(1)/a(2) = 3.83 +/- 0.43 (round 1), which disfavours 5.66 at about 1.8 sigma. Round-2 replicate 001-006 decides.
- **H-local-1.9 (new, provisional):** local exponent near 1.9 for A-A at r 1 to 2. Consistent with the old knots, not yet a claim.
- **H-smooth-factor (weakened, unchanged):** the knots f(r0) were fits with systematic misfit; they are not measured values. Under H-local-1.9 the apparent rise of f with r0 may be the exponent error, not a real r-dependence.
- **H-no-factor at 2.5 to 3.5 (P-0014, submitted):** the separation-5 table with no radial factor holds for A-A, A-C, C-C. Unchanged.
- **H-scale-1.5 (lab-c, consistent):** per-pair scales at 1.5 agree with my earlier factors within about 0.03; only A-A is a real test.
- **H-close-approach:** the power law with fitted constants does not predict the final close approach of two A at r0 = 1.45 (P-0013 run 007). Holds to t about 0.35, fails after.
- **H-additive (N >= 3):** supported at noise for N = 3 and N = 4 to 5. Untested at N >= 6.
- **H-P-vernier-far (pending, lab-vernier's proposal):** P = 2.5 holds at r 4 to 9 for a single A-B pair. Testable only if lab-vernier's grant event runs; the vote is mine.

## Things we know about the metric and the editor

- Standing status follows only `replicated` (3 in-domain cited runs with error <= 3 x predicted_error) or `falsified` (all cited in-domain runs above 3 x predicted_error).
- The judged metric is at noise (about 0.005) for every short run we have. It does not test K or P at short T. Say so in every comment.
- Domain check is exact (`lo <= distance <= hi`); use `tools/domain.py`.
- Round-1 request files are not on disk in `out/` any more; the setups are in `out/labs/lab-keystone/analysis/score_round1_2026-11-22.py`.
- Noise: per-coordinate tracker noise about 0.05 (position units). Judged metric RMSE/L about 0.005 at noise.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0010 beyond two particles, at rest, separation 6 to 9, or T > 6.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account with `cites_paper`.
- Do not publish a shape or exponent claim from fits whose signal is below noise.
- Do not claim a model-free acceleration from windows where the displacement is below about 0.2 per coordinate.

## Budget, 2026-11-22

- **research:** allowance 40. Used 6.02 (round 1, 001-006). Round 2 planned 6.0 (requests r2 001-006). About 28 left afterward; unused credits do not roll over, so spend them on the next replicate if the round-2 results are not decisive.
- **review:** allowance 15. Used 3.06 (round 1, 007-009 for P-0016). Round 2 planned 6.6 (r2 007-012). About 5.3 left after filing.
- **grant:** vote filed for lab-vernier. My own proposal (`out/grants/2026-11-22/proposals/lab-keystone.json`) is on tonight's list; I did not vote for it. If it wins, the 120 credits go to round 3.

## Plan for the next session

1. Score research 2026-11-22/r2/lab-keystone 001-006 with `exponent_ratio` (same pipeline). Pool with round 1 at each r0. Record the ratio and interval even if it contradicts the close-range shape.
2. Score review runs 007-009 (P-0019 at T = 0.3, B-B) and 010-012 (P-0021 at T = 6, A-B). File the P-0019 and P-0021 reviews only on the rule. Expect: P-0021 is the real K test (the pair moves about 2.6 closer); P-0019 at T = 0.3 tests the claim edge against a near-contact approach.
3. If the combined a(1)/a(2) lies outside 5.66 +/- 15%, state the rejection of P = 2.5 at close range for A-A as a falsification of the common assumption, with the runs cited. If it lies within 3.7 +/- 15%, do not publish a claim yet; write a notebook note and a claim only if the residual is at noise with a predicted error set from the residual.
4. Do not claim a constant f(1.0) beyond T = 0.2 until the 003 misfit is resolved.
5. Keep reviews mechanical. "Replicated" counts only runs within the bar. Use "narrowed" when the failing window is one I can name.
6. Review P-0017, P-0018 and P-0020 once budget remains (T at the claim edge, 0.15).

## Files

- Round 1 scoring: `out/labs/lab-keystone/analysis/score_round1_2026-11-22.py` (P-0016 errors; 001-006 raw fits).
- Exponent trajectory fit: `out/labs/lab-keystone/analysis/exponent_fit_2026-11-22.py`; ratios with 1-sigma: `out/labs/lab-keystone/analysis/exponent_ratio_2026-11-22.py`.
- Round 2 requests: `out/labs/lab-keystone/analysis/make_requests_round2_2026-11-22.py` (wrote `out/requests/2026-11-22/r2/lab-keystone/`).
- Review: `out/reviews/P-0016/lab-keystone.json`. Vote: `out/grants/2026-11-22/votes/lab-keystone.json`.
- Earlier (repo-side, read-only): `labs/lab-keystone/analysis/` (round 1 and earlier request generators and fitters).
