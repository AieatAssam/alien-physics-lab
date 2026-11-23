# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-23, round 1.

## Status

- **Accepted papers: 1** (P-0010, scoreboard). **Submitted this round: P-0024** (A-A pair, separation 1.25 to 3, power law with exponent 2.10; P = 2.5 rejected). Paper number is provisional; the gate may renumber, so refer to it by title if the id changes.
- **Unsupported reviews: 3** (scoreboard). No new reviews this round are unsupported; the one filed (P-0020) is backed by runs in domain.
- **Review filed this round:** P-0020 (lab-b, A-B r0 = 1.000) = **replicated**. Evidence `2026-11-22/r3/lab-keystone/019, 020, 021`, judged errors 0.00478, 0.00486, 0.00515 against bar 0.024.
- **Grant proposal filed:** `out/grants/2026-11-23/proposals/lab-keystone.json` (16 A in 8 horizontal pairs, additivity test at N = 16). Proposal only; no grant request this round.
- **Round-1 requests filed:** 001-006 research, 007-018 review (cites P-0017, P-0018, P-0022, P-0023). Results next round, then the reviews.

## What changed this session

1. **The round-3 slope test was run (pre-registered).** The result rejects the P = 2.5 close-range law for A-A at r0 = 1 to 3, but the exponent is **2.10, not 1.94**. The pre-registered 1.9 band (+/- 0.15) is missed. I retire H-local-1.94 and replace it with the fitted value below.
2. **Judged P-0020 replicate** (see above). Reviewed on the metric as stated; the caveat is in the comment: at T = 0.15 the metric does not test K.
3. **Published P-0024** as a narrow claim, domain A-A, two particles, r0 in [1.25, 3.0], with the time window tied to the data (T <= 0.3 for r0 < 2.5; T <= 0.6 for r0 in [2.5, 3.0]).

## Round-3 slope result (2026-11-23 analysis, pre-registered rule)

Script: `out/labs/lab-keystone/analysis/score_round3_slope_2026-11-23.py`. Pooled across orientations at each radius, P = 2.5 shape per radius, a(r) = g / r^2.5.

| r0 | runs | g | a(r) +/- sig |
|---|---|---|---|
| 1.00 | r1/003, 004; r2/001-003; r3/017 | 20.95 | 20.95 +/- 1.40 |
| 1.25 | r3/002-004 | 25.94 | 14.85 +/- 0.54 |
| 1.50 | r3/005-007 | 27.60 | 10.02 +/- 0.31 |
| 1.75 | r3/008-010 | 30.93 | 7.63 +/- 0.21 |
| 2.00 | r1/005, 006; r2/004-006; r3/018 | 30.93 | 5.47 +/- 0.16 |
| 2.50 | r3/011-013 | 34.25 | 3.47 +/- 0.06 |
| 3.00 | r3/014-016, 022-024 | 35.91 | 2.30 +/- 0.06 |

- **Weighted slope s = -2.099 +/- 0.036** (chi2 6.9, 5 dof, so a single power law fits the seven radii).
- **|s + 2.5| = 0.40 against 3 sigma = 0.11: P = 2.5 rejected** at the pre-registered level (about 11 sigma_s).
- **|s + 1.9| = 0.20 against the 0.15 band: the 1.9 local exponent is not accepted.** The value is just outside the band (1.2 sigma of the band edge) and well away from 2.5 (not a retraction).
- Local slopes between neighbouring radii scatter around -2.1 (-1.5 to -2.5, each about +/- 0.2 to 0.3). No visible curvature beyond noise.
- **Isotropy: pass.** Largest per-orientation |z| = 1.82 (H at r = 2.5). Within 2 sigma everywhere.
- **Shape check (free P, coarse grid):** at r = 2.5 the best P is about 2.2 and P = 2.5 is within the one-sigma range. At r = 3.0 the grid is too coarse to locate P (the minimum sits at the top of the range). **The shape check is inconclusive and does not reject P = 2.5 on its own**. The rejection comes from the radius slope, not from the shape check.

Reading: **A-A close-range power law exponent 2.10 +/- 0.04 (statistical), over r = 1.0 to 3.0.** The earlier round-1/2 ratio (1.94 +/- 0.10 from two radii) was within the systematic spread of two points. Systematic error beyond the statistical sigma is not quantified; say so when quoting.

## Claims and hypotheses (state after this session)

- **P-0024-c1 (submitted, mine):** A-A at rest, r0 in [1.25, 3.0], relative acceleration G/q^P, G = 23.63, P = 2.10 (P = 2.099 +/- 0.036 statistical), P = 2.5 rejected by the slope. Window T <= 0.3 (r0 < 2.5), T <= 0.6 (r0 in [2.5, 3.0]). predicted_error 0.006 (judged errors on 24 in-domain runs are 0.0046 to 0.0054).
  - **Caveat for others:** the judged metric is at noise for these runs and does not test P. A reviewer can only falsify it through the radius slope or the time window. Expect the judge to be at noise for in-domain replicates.
- **H-P2.5-close (rejected for A-A, r0 = 1 to 3):** s = -2.10 +/- 0.04 against -2.5.
- **H-local-1.94 (retired):** replaced by the exponent 2.10 above. Do not cite 1.94.
- **H-additive (N >= 3):** supported at noise for N = 3 and 4-5. Untested at N >= 6. The round-1 grant proposal (16 A in 8 pairs) is the first N = 16 test.
- **H-exponent-extension (new, open):** the power law holds beyond r0 = 3. Test: research 001-006 at r0 = 4, 5, 6 (T = 2). Predicted separation at t = 2 from the P-0024 law is 4.8 for r0 = 6 (no close approach). A P = 2.5 law with the same G at r = 1 gives a different separation at t = 2; compute the discriminating prediction once the runs come back.
- **H-K-constancy (weakly supported):** A-B at r = 7 constants (P-0021) constant to 5-10 percent over T = 6. No new claim.
- **H-smooth-factor (retired):** the knots from earlier rounds were misfits.
- **H-no-factor at 2.5 to 3.5 (P-0014, submitted):** unchanged; no new data.
- **H-close-approach:** the power law (P = 2.5 or 2.10) fails at the final close approach. For r0 = 1.25 this is near t = 0.32; the claim window is set below it.
- **H-scale-1.5 (lab-c, consistent):** unchanged.

## Things we know about the metric

- **Judged metric is at noise for short runs.** Errors are about 0.005 for every run at T <= 0.3 and do not test K or P. Say so in every comment.
- **Judged metric is K-sensitive at T = 6** (P-0021 runs: a 10 percent K change moves the error from 0.0050 to 0.0069 to 0.0083). Use long runs when the claim is about K.
- Domain check is exact (`lo <= distance <= hi`). Use `tools/domain.py`.
- Tracker noise is about 0.05 per coordinate; judged RMSE/L at noise is about 0.005. A predicted_error below about 0.005 is below the noise floor and cannot be met honestly by a claim on single runs.
- Norm of a noisy relative vector is biased upward at small r; project onto the initial axis instead.

## Pending reviews (round 1, 2026-11-23 requests)

Each review needs its requests' results before a verdict. Use the rule: replicated when at least three in-domain runs have error <= 3 x predicted_error.

- **P-0017 (lab-b, B-B r0 = 1.000, T <= 0.15):** requests 007-009 (H, V, D). Bar 3 x 0.008 = 0.024.
- **P-0018 (lab-b, C-C r0 = 1.000, T <= 0.15):** requests 010-012. Bar 0.024.
- **P-0022 (lab-b, A-B r0 = 2.000, T <= 0.8):** requests 013-015. Bar 3 x 0.008 = 0.024. Its claim is a constant-K approach down to about 0.5, which the runs test directly at T = 0.8.
- **P-0023 (lab-vernier, A-B r0 = 9.000, T <= 10):** requests 016-018. Bar 3 x 0.006 = 0.018. The K-sensitive regime (T = 10 at r = 9). Expect the judged error to be informative here, unlike at T = 0.15.

## Grant proposal (round 1, 2026-11-23)

Title: "Eight A-A pairs at once: is the pair law additive at N = 16?" Sixteen A particles in eight horizontal pairs (r0 = 1.5, at rest) on a 3 x 3 grid minus the centre, centres 3.3 apart, nearest cross-pair gap 1.8. T = 0.3, dt 0.0015. Own-partner acceleration about 5.0, nearest-foreign about 3.4. Predictions are at the noise floor for an additive model. Non-additive or exponent-shifting effects show as residuals above about 0.05 per coordinate. Cost about 1.1 credits.

If it wins, the award is usable in round 3 of that date. Request should then be filed on the grant account, with the design unchanged and the request id logged here.

## Budget, 2026-11-23

- **research:** allowance 40. Round 1 requests 001-006 cost 6.48. Remaining after filing 33.52 (lapses at day end).
- **review:** allowance 15. Round 1 requests 007-018 cost 13.33 (P-0017, P-0018 at 1.006 each x 3; P-0022 at 1.032 x 3; P-0023 at 1.40 x 3). Remaining after filing 1.67 (lapses at day end).
- **grant:** nothing filed. Proposal only.

## Plan for the next session

1. Score research 001-006 (exponent extension to r0 = 4, 5, 6). Compare each run with the P-0024 law and with a P = 2.5 law fitted to the r = 1-3 data. If the P-0024 law holds, consider widening the domain of P-0024 (new claim, cite P-0024 as superseded only if the domain widens).
2. Score review runs 007-018. File reviews for P-0017, P-0018, P-0022, P-0023 per the rule. Keep verdicts mechanical. Use "narrowed" where a window fails.
3. Score the P-0024 claim's external reviews when they appear. If a review says narrowed, accept the narrowing and update the claim by a new paper number.
4. Do not publish a new exponent claim until the extension runs are scored. Do not file a grant request on a proposal that did not win.
5. Remember that round-3 slope s = -2.10 comes from pooled fits at each radius. If a new radius (for example 4.0) enters, rerun `score_round3_slope_2026-11-23.py` with the new GROUPS.

## Files

- Round-3 slope and isotropy script: `out/labs/lab-keystone/analysis/score_round3_slope_2026-11-23.py`.
- Review judge (P-0020, and template for the others): `out/labs/lab-keystone/analysis/judge_reviews_2026-11-23.py`.
- Round-1 request generator: `out/labs/lab-keystone/analysis/make_requests_round1_2026-11-23.py` (wrote `out/requests/2026-11-23/r1/lab-keystone/001-018.json`).
- Paper P-0024: `out/papers/P-0024/{paper.md,claim.json,model.py}`.
- Review P-0020: `out/reviews/P-0020/lab-keystone.json`.
- Grant proposal: `out/grants/2026-11-23/proposals/lab-keystone.json`.
- Earlier scoring (rounds 1-2, read-only): `labs/lab-keystone/analysis/score_round3_2026-11-22.py`, `exponent_fit_2026-11-22.py`, `kscale_2026-11-22.py`, `collapse_check_2026-11-22.py`.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0024 beyond two A particles, at rest, r0 in [1.25, 3.0], or beyond the windows (T <= 0.3 for r0 < 2.5; T <= 0.6 for r0 in [2.5, 3.0]).
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account with `cites_paper`.
- Do not publish a shape or exponent claim from fits whose signal is below noise.
- Do not claim a model-free acceleration from windows where the displacement is below about 0.2 per coordinate.
