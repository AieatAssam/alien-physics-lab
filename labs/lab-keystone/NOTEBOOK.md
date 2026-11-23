# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-23, round 2.

## Status

- **Accepted papers: 1** (P-0010, scoreboard). **Submitted: P-0024** (A-A pair, r0 in [1.25, 3.0], power law with exponent 2.10). Paper number is provisional; refer to it by title if renumbered.
- **Unsupported reviews: 3** (scoreboard). Round-2 reviews below are judged on the paper's metric with in-domain runs.
- **Round-2 reviews filed (all four replicated):**
  - P-0017 (lab-b, B-B r0 = 1.000, T <= 0.15): runs 007, 008, 009; RMSE/L 0.00745, 0.00696, 0.00650; bar 0.024.
  - P-0018 (lab-b, C-C r0 = 1.000, T <= 0.15): runs 010, 011, 012; RMSE/L 0.00706, 0.00696, 0.00703; bar 0.024.
  - P-0022 (lab-b, A-B r0 = 2.000, T <= 0.8): runs 013, 014, 015; RMSE/L 0.00722, 0.00700, 0.00690; bar 0.024.
  - P-0023 (lab-vernier, A-B r0 = 9.0, T <= 10): runs 016, 017, 018; RMSE/L 0.00738, 0.00737, 0.00764; bar 0.018.
  - Scoring script: `out/labs/lab-keystone/analysis/judge_round2_2026-11-23.py`. All in domain (checked with `tools/domain.py`).
  - **Caveat for all four:** T <= 0.15 and T <= 0.8 runs sit at the tracker noise floor (about 0.005), so those "replicated" verdicts only show the trajectory is reproduced. They do not test K or P. P-0023 (T = 10) is the one K-sensitive review.
- **Round-2 vote:** lab-b (Icarus), centre-of-mass test of equal-and-opposite pair forces. Reason: shape-free, cheap, and sharp (drift below 0.01 against 0.14 for equal masses), and it tests the central, third-law structure that pair-law synthesis relies on. File: `out/grants/2026-11-23/votes/lab-keystone.json`.
- **Round-1 grant proposal (ours):** 16 A in 8 horizontal pairs, additivity at N = 16. Not yet decided whether it wins; see grant ledger. The award (if any) is usable in round 3 of 2026-11-23 on account `grant`.

## Round-1 reviews to note

- The round-1 review runs (007-018) were the four reviews above. They were filed on the review account with `cites_paper` (cost 13.35 of 15 credits today).
- Review budget left after round 2: 1.65 (lapses at day end).

## Round-3 slope result (from round 1, pre-registered rule)

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

- **Weighted slope s = -2.099 +/- 0.036** (chi2 6.9, 5 dof; a single power law fits the seven radii).
- **|s + 2.5| = 0.40 against 3 sigma = 0.11: P = 2.5 rejected** at the pre-registered level.
- **|s + 1.9| = 0.20 against the 0.15 band: the 1.9 local exponent is not accepted.** Retired.
- **Isotropy: pass.** Largest per-orientation |z| = 1.82.
- **Shape check (free P, coarse grid):** inconclusive. The rejection comes from the radius slope, not from the shape check.

Reading: **A-A close-range power law exponent 2.10 +/- 0.04 (statistical), over r = 1.0 to 3.0.** Systematic error is not quantified; say so when quoting.

## Claims and hypotheses

- **P-0024-c1 (submitted, mine):** A-A at rest, r0 in [1.25, 3.0], relative acceleration G/q^P, G = 23.63, P = 2.10 (P = 2.099 +/- 0.036 statistical), P = 2.5 rejected by the slope. Window T <= 0.3 (r0 < 2.5), T <= 0.6 (r0 in [2.5, 3.0]). predicted_error 0.006.
  - **Caveat:** the judged metric is at noise for these runs and does not test P. Falsification is possible only through the radius slope or the time window.
- **H-P2.5-close (rejected for A-A, r0 = 1 to 3):** s = -2.10 +/- 0.04 against -2.5.
- **H-local-1.94 (retired):** do not cite 1.94.
- **H-additive (N >= 3):** supported at noise for N = 3 and 4-5. Untested at N >= 6. Our grant proposal (16 A in 8 pairs) is the first N = 16 test.
- **H-exponent-extension (open):** the power law holds beyond r0 = 3. Test: research 001-006 at r0 = 4, 5, 6 (T = 2). Predicted separation at t = 2 from the P-0024 law is 4.8 for r0 = 6 (no close approach). A P = 2.5 law with the same G at r = 1 gives a different separation at t = 2; compute the discriminating prediction once the runs are scored.
- **H-K-constancy (weakly supported):** A-B at r = 7 constants (P-0021) constant to 5-10 percent over T = 6. No new claim.
- **H-close-approach:** power laws (P = 2.5 or 2.10) fail at the final close approach. For r0 = 1.25 this is near t = 0.32; the claim window is set below it.
- **H-no-factor at 2.5 to 3.5 (P-0014, submitted):** unchanged.
- **H-scale-1.5 (lab-c, consistent):** unchanged.

## Things we know about the metric

- **Judged metric is at noise for short runs** (T <= 0.8). Errors are about 0.005 to 0.007 and do not test K or P. Say so in every comment.
- **Judged metric is K-sensitive at T = 6-10.** A 10 percent K change moves the P-0021 error from 0.0050 to 0.0069 to 0.0083. Use long runs when the claim is about K.
- Domain check is exact (`lo <= distance <= hi`). Use `tools/domain.py`.
- Tracker noise is about 0.05 per coordinate; judged RMSE/L at noise is about 0.005. A predicted_error below about 0.005 is below the noise floor and cannot be met honestly by single-run claims.
- Norm of a noisy relative vector is biased upward at small r; project onto the initial axis instead.

## Plan for the next session

1. Score research 001-006 (exponent extension to r0 = 4, 5, 6). Compare each run with the P-0024 law and with a P = 2.5 law fitted to the r = 1-3 data. If the P-0024 law holds, consider widening its domain in a new paper and say so.
2. If the grant winner is ours, file the 16-particle additivity request on the `grant` account with the design unchanged, and log the id here. If not, do not file it.
3. Watch for reviews of P-0024. If a review says narrowed, accept it and update the claim under a new number.
4. Do not publish a new exponent claim until the extension runs are scored.
5. If a new radius (for example 4.0) enters the slope fit, rerun `score_round3_slope_2026-11-23.py` with the new GROUPS.

## Files

- Round-2 review judge: `out/labs/lab-keystone/analysis/judge_round2_2026-11-23.py`. Usage: `python3 -I <script> <repo_root>`.
- Round-3 slope and isotropy script: `out/labs/lab-keystone/analysis/score_round3_slope_2026-11-23.py`.
- Review judge (P-0020): `out/labs/lab-keystone/analysis/judge_reviews_2026-11-23.py`.
- Round-1 request generator: `out/labs/lab-keystone/analysis/make_requests_round1_2026-11-23.py`.
- Paper P-0024: `out/papers/P-0024/{paper.md,claim.json,model.py}`.
- Reviews: `out/reviews/P-0020/lab-keystone.json`, `out/reviews/P-0017/`, `P-0018/`, `P-0022/`, `P-0023/` (each `lab-keystone.json`).
- Grant proposal: `out/grants/2026-11-23/proposals/lab-keystone.json`.
- Grant vote: `out/grants/2026-11-23/votes/lab-keystone.json` (vote lab-b).

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0024 beyond two A particles, at rest, r0 in [1.25, 3.0], or beyond its windows.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account with `cites_paper`.
- Do not publish a shape or exponent claim from fits whose signal is below noise.
- Do not claim a model-free acceleration from windows where the displacement is below about 0.2 per coordinate.
