# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-22, round 3 (last round of the day).

## Status

- **Accepted papers: 1** (P-0010, scoreboard). **Submitted: P-0014** (two particles of species A or C at separation 2.5 to 3.5, no radial factor). Unchanged.
- **Unsupported reviews: 3** (scoreboard). No new unsupported reviews this round.
- **No new claim published this round.** The A-A exponent result is now a candidate claim (below), but it rests on three radii only; I want the round-3 radius curve before publishing. Next session: publish it or write it off.
- **Reviews filed this round:** P-0019 (replicated), P-0021 (replicated). **Pending:** P-0020 (runs `2026-11-22/r3/lab-keystone/019-021` filed; file the review only after they return).
- **Grant:** Keystone won tonight (title in the round prompt). Grant request `2026-11-22/r3/lab-keystone/001` is filed with the voted design unchanged. See "Grant design caveat" below.

## Round 3 actions (2026-11-22)

1. **Scored round-2 research 001-006 (A-A exponent replicate).** Pooled with round 1 at each r0. Results in the table below.
2. **Review P-0019 (lab-a, B-B r0 = 1.0, T <= 0.3): replicated.** `out/reviews/P-0019/lab-keystone.json`, evidence `2026-11-22/r2/lab-keystone/007, 008, 009`. Judged errors 0.00498, 0.00506, 0.00491 against bar 3 x 0.008 = 0.024. All three in domain (exact check with `tools/domain.py`; 008 sits at r0 = 0.999 and 009 at 1.001). The metric does not test K here: scaling K from 0.95x to 1.05x moves the error by less than 0.0001. Comment says so.
3. **Review P-0021 (lab-vernier, A-B sep 6.9-7.1, T <= 6): replicated.** `out/reviews/P-0021/lab-keystone.json`, evidence `2026-11-22/r2/lab-keystone/010, 011, 012`. Judged errors 0.00504, 0.00499, 0.00504 against bar 3 x 0.007 = 0.021. All three in domain (r0 = 6.901, 7.000, 7.099). **This long run is K-sensitive:** scaling both constants by 0.9 gives judged errors 0.0069 to 0.0083; by 1.1 gives 0.0076 to 0.0080 (baseline about 0.0050). So these runs constrain the pair constants to roughly 5 to 10 percent. This is the first K-sensitive check I have done on any claim.
4. **Requests filed, round 3:** `out/requests/2026-11-22/r3/lab-keystone/` (001-024). Generator: `out/labs/lab-keystone/analysis/make_requests_round3_2026-11-22.py`.
   - 001 grant (see caveat).
   - 002-016 research: A-A at five new radii (1.25, 1.5, 1.75, 2.5, 3.0), each horizontal / vertical / diagonal, centre (5,5). Durations 0.2, 0.25, 0.3, 0.6, 0.6; dt 0.002 to 0.006; 101 samples each.
   - 017 research: A-A diagonal r0 = 1.0 at centre (3,7), T = 0.1 (second-centre anchor).
   - 018 research: A-A vertical r0 = 2.0 at centre (7,3), T = 0.3 (second-centre anchor).
   - 022-024 research: A-A r0 = 3.0 H/V/D at second centres (lever-arm replicates; the weakest-signal point).
   - 019-021 review (cites P-0020): A-B at r0 = 1.000, T = 0.15, horizontal (A left), vertical (B on top), diagonal. **Not yet a review; file after results.**
   - Costs: research 20.32 (of 27.95 left), review 3.02 (of 5.19 left), grant 1.03 (of 120). Cost formula confirmed: cost = 1 + 0.02 x particles x duration.

## Round-2 exponent result (A-A, pooled across rounds, projected fit)

Method: each run is fitted with the radial law q'' = -g/q^2.5 (g = 2K, relative acceleration), RK4 at dt/5, grid search on g, 1-sigma from delta-rms. **Fix this round:** the separation was the norm |p1 - p0|, which is biased upward by about s^2/(2r) for tracker noise. The fit now projects the noisy relative vector onto the initial axis (linear in noise). The ratio did not move. Script: `out/labs/lab-keystone/analysis/score_round3_2026-11-22.py`.

| r0 | runs (round/run) | g (P = 2.5 shape) | a(r0) = g / r0^2.5 | rms (noise-like) |
|---|---|---|---|---|
| 0.5 | r1/001, 002 | 17.6 [11.9, 22.1] | 99.7 +/- 28.9 | 0.068 |
| 1.0 | r1/003, 004; r2/001, 002, 003 | 20.95 [19.90, 22.58] | 20.95 +/- 1.34 | 0.070 |
| 2.0 | r1/005, 006; r2/004, 005, 006 | 30.93 [29.75, 31.73] | 5.47 +/- 0.17 | 0.066 |

- **a(1.0)/a(2.0) = 3.83 +/- 0.27.** P = 2.5 predicts 5.66; local exponent 1.9 predicts 3.73. Outside the 5.66 +/- 15% window (4.81 to 6.51), and inside the 3.73 +/- 15% window (3.17 to 4.29). The round-1-only value was 3.83 +/- 0.43 (norm fit); round-2 replicates tightened it.
- Local exponent from the ratio: log2(3.83) = **1.94 +/- 0.10**.
- a(0.5)/a(1.0) = 4.8 +/- 1.4 (projected fit). The r0 = 0.5 pairs are unconstrained at T = 0.03 (noise-limited, see below). **No claim at r0 = 0.5.**
- Reading: the pre-registered decision rule from round 2 is met. **The combined ratio rejects P = 2.5 at close range for A-A (r0 = 1 to 2) at the stated rule.** This is provisional until the round-3 radius curve (below) comes back, because the ratio comes from two radii only.

## Pre-registration for round-3 research (written before results)

Analysis, fixed now:

1. Per radius (1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0): pool orientations, fit g(r) with the P = 2.5 shape (same fitter), a(r) = g / r^2.5 with 1-sigma.
2. **Primary statistic:** weighted least-squares slope s of log a(r) against log r over the seven radii, with sigma_s.
3. **Predictions:** P_eff = 2.5 gives s = -2.5. A local exponent near 1.9 gives s = -1.9.
4. **Decision:**
   - Reject P = 2.5 at close range if |s + 2.5| > 3 sigma_s.
   - Accept a local exponent of 1.9 +/- 0.15 if s lies in that band and P = 2.5 is rejected.
   - If s is within 1 sigma of -2.5, **retract the exponent hypothesis** and say so in the notebook (the round-1/2 ratio was then a systematic).
5. **Isotropy check:** orientation spread within each radius must be within 2 sigma. If it is not, drop the affected radius from the slope and report it.
6. **Shape check (cheap):** a free-P fit per radius (two parameters, g and P). The notebook history says free-P fits were flat at r 1-2 with T = 0.1 and 0.3. Here I use the longer T = 0.6 runs at r = 2.5, 3.0 where the displacement (about 0.25) is above noise. If the free-P fits there are not flat, use them and report.

What would change my mind: a slope near -2.5 with small sigma, or orientation-dependent accelerations.

## Grant design caveat (2026-11-22 grant, request 001)

The voted design says "short duration, so no close approach." **That is wrong for the r0 = 0.5 pair.** A one-body check (`out/labs/lab-keystone/analysis/collapse_check_2026-11-22.py`, g = 20.95, P = 2.5, no cross-pair terms) gives:

- r0 = 0.5: separation 0.33 at t = 0.05, 0.22 at t = 0.06 (reaches 0.25 r0 at t = 0.065).
- r0 = 0.75: 0.50 at t = 0.10.
- r0 = 1.0: 0.89 at t = 0.10.

Cross-pair forces are also not negligible. The r0 = 2.25 pair sees about 0.8 per particle from the pair above at distance about 2.8, against about 1.4 of its own. So the 8-pair run tests the additive N-body assumption (H-additive, untested at N >= 6) as well as the exponent.

I filed the grant **unchanged** because the vote chose that design, and changing a voted design unilaterally is not mine to do. The pre-registered analysis for request 001 is therefore:

1. Mask samples where any pair separation is below 0.3. This keeps the r0 = 0.5 pair to t about 0.055 and the others for the full 0.1.
2. Fit the eight pairs jointly, with the additive pairwise model (K/r^P per particle toward each other particle), free K and P. Primary: P from the joint fit, with the masked data.
3. Cross-check: single-pair fits for r0 = 1.0 and 2.0 within the joint fit should agree with the round-3 single-pair values within 10%. If they do not, the additivity assumption is failing and the grant result is inconclusive on P.
4. Pre-registered predictions: P = 2.5 and P = 1.9 at fixed K from the research runs. Compare chi-square at the noise floor (per-coordinate tracker noise about 0.05).

Expected outcome: the r0 = 0.5 and 0.75 pairs carry the most signal; the r0 = 2.25 pair is confounded.

## Hypotheses (state after round 3 scoring)

- **H-P2.5-close (provisionally rejected for A-A, r0 = 1 to 2):** a(1.0)/a(2.0) = 3.83 +/- 0.27 against 5.66. Confirmed or retracted by the round-3 slope.
- **H-local-1.94 (new, provisional):** the local exponent for A-A at r0 = 1 to 2 is 1.94 +/- 0.10. Candidate claim for next session, with the domain: A-A, 2 particles, at rest, r in [1.0, 2.0], T <= 0.3. Not published yet: the judged metric cannot separate P = 2.5 from P = 1.94 at these durations (estimated change in judged error < 0.001), so the claim rests on the ratio and must say so.
- **H-K-constancy (new, weakly supported):** for the A-B pair at r = 7, the constants in P-0021 are constant to 5-10% over T = 6. The judged metric is sensitive to K at T = 6, so this is a real test. No new claim.
- **H-smooth-factor (retired as stated):** the old knots f(r0) were fits with systematic misfit, not measured values. The local-1.94 result supersedes them at r0 = 1 to 2.
- **H-no-factor at 2.5 to 3.5 (P-0014, submitted):** the separation-5 table with no radial factor holds for A-A, A-C, C-C. Unchanged; no new data.
- **H-scale-1.5 (lab-c, consistent):** per-pair scales at 1.5 agree with my earlier factors within about 0.03. Only A-A is a real test.
- **H-close-approach:** the power law with fitted constants does not predict the final close approach of two A at r0 = 1.45 (P-0013 run 007). Holds to t about 0.35, fails after.
- **H-additive (N >= 3):** supported at noise for N = 3 and N = 4 to 5. Untested at N >= 6. The 16-particle grant run is the first N >= 6 test.
- **H-P-vernier-far (lab-vernier's proposal):** P = 2.5 holds at r 4 to 9 for a single A-B pair. Not tested by my runs.

## Things we know about the metric (this round)

- **Judged metric is at noise for short runs.** Errors are about 0.005 for every run at T <= 0.3 and do not test K or P. Say so in every comment.
- **Judged metric is K-sensitive at T = 6** (P-0021 runs: 10% K change gives 0.0069 to 0.0083 against baseline 0.0050). Use long runs when the claim is about K.
- Domain check is exact (`lo <= distance <= hi`). Use `tools/domain.py`. Edge runs at 0.999 and 1.001 (P-0019) and 6.901 and 7.099 (P-0021) pass.
- Tracker noise is about 0.05 per coordinate; judged RMSE/L at noise is about 0.005.
- Norm of a noisy relative vector is biased upward at small r; project onto the initial axis instead.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0010 beyond two particles, at rest, separation 6 to 9, or T > 6.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account with `cites_paper`.
- Do not publish a shape or exponent claim from fits whose signal is below noise.
- Do not claim a model-free acceleration from windows where the displacement is below about 0.2 per coordinate.
- Do not file the P-0020 review until 019-021 have results.

## Budget, 2026-11-22

- **research:** allowance 40. Used 12.05 before round 3 (round 1 6.02, round 2 6.03). Round 3 requests 002-018 and 022-024 total 20.32. Remaining after filing: 7.6 (lapses at day end).
- **review:** allowance 15. Used 9.81 before round 3. Round 3 requests 019-021 (P-0020) total 3.02; remaining after filing: 2.17 (lapses at day end).
- **grant:** 120 credits. Request 001 costs 1.03; one main-event experiment per night, so the remainder is not usable.

## Plan for the next session

1. Score round-3 research 002-018 and 022-024 with the pre-registered slope rule. Record s, sigma_s, the isotropy check, and the shape check. Decide H-P2.5-close and H-local-1.94 per the rule.
2. Score grant request 001 with the pre-registered mask and joint fit. Record whether the additive assumption held (cross-check within 10%).
3. Score review runs 019-021 and file the P-0020 review on the rule (3 in-domain runs, error at or below 0.024). Expect replicated, with the metric at noise; say so.
4. If the slope rule accepts the local exponent, publish a narrow claim: A-A, 2 particles, at rest, r in [1.0, 2.0], T <= 0.3, local exponent 1.94, with predicted error set from the residuals. If it rejects, retract and write a notebook note.
5. Keep reviews mechanical. "Replicated" counts only runs within the bar. Use "narrowed" when the failing window is one I can name.
6. Review P-0017 and P-0018 when budget allows (T at the claim edge, 0.15; metric at noise).

## Files

- Round-3 scoring (reviews and exponent, projected fit): `out/labs/lab-keystone/analysis/score_round3_2026-11-22.py`.
- K sensitivity of judged error: `out/labs/lab-keystone/analysis/kscale_2026-11-22.py`.
- Two-body collapse check for the grant design: `out/labs/lab-keystone/analysis/collapse_check_2026-11-22.py`.
- Round-3 requests: `out/labs/lab-keystone/analysis/make_requests_round3_2026-11-22.py` (wrote `out/requests/2026-11-22/r3/lab-keystone/001-024.json`).
- Reviews: `out/reviews/P-0019/lab-keystone.json`, `out/reviews/P-0021/lab-keystone.json`.
- Earlier (round 1-2 fitters, read-only): `labs/lab-keystone/analysis/` (`exponent_fit_2026-11-22.py`, `exponent_ratio_2026-11-22.py`, `score_round1_2026-11-22.py`).
- Round-2 review of P-0016 and round-2 vote (for lab-vernier): filed in round 2. The repo-side copies are `reviews/P-0016/lab-keystone.json` and `grants/2026-11-22/votes/lab-keystone.json`; they are not in `out/` in this checkout.
