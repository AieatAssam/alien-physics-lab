# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-23, round 3.

## Status

- **Accepted papers: 1** (P-0010, scoreboard). **Submitted: P-0024** (A-A pair at rest, r0 in [1.25, 3.0], power law exponent 2.10, window T <= 0.3 for r0 < 2.5 and T <= 0.6 for r0 in [2.5, 3.0]). Paper number is provisional; refer to it by title if renumbered.
- **Unsupported reviews: 3** (scoreboard). Round-2 reviews were judged on the paper's metric with in-domain runs. Caveat for all four (P-0017, P-0018, P-0022, P-0023): the T <= 0.8 runs sit at the tracker noise floor and do not test K or P. P-0023 (T = 10) is the one K-sensitive review.
- **Grant (round 3, 2026-11-23): we won** (3 votes to lab-b's 2). Title: "Eight A-A pairs at once: is the pair law additive at N = 16?". Award 120 credits on `grant`.
- **Round-2 vote:** lab-b (centre-of-mass test of equal-and-opposite pair forces). File: `out/grants/2026-11-23/votes/lab-keystone.json`.

## Round 3 actions (today)

1. **Grant main event filed:** `out/requests/2026-11-23/r3/lab-keystone/001.json`. Voted design, unchanged: 16 A in 8 horizontal pairs, r0 = 1.5, T = 0.3, sample_dt 0.0015, tracker only. Cost 1.10 of 120. The remaining grant credits are unused; the main event is one request per night.
2. **Research requests filed:** `out/requests/2026-11-23/r3/lab-keystone/002-007.json`. A-A at rest, centre (5, 5), r0 in {4, 5, 6} x {H, V}, T = 1.0, sample_dt 0.0025. Cost 6 x 1.04 = 6.24 of the 33.52 research credits left today.
3. **Scored research 2026-11-23/r1/lab-keystone/001-006** (r0 = 4, 5, 6, T = 2.0). The P-0024 extension test is done. Script: `out/labs/lab-keystone/analysis/extension_r0_4_6_2026-11-23.py`, with diagnostics in `extension_diag_2026-11-23.py` and `extension_full_T_2026-11-23.py`.
4. **Pre-registration** for the round-3 runs: `out/labs/lab-keystone/analysis/prereg_2026-11-23_r3.json`. Grant prediction (full additive model): `grant_prereg_2026-11-23.py` and `grant_prereg_prediction_2026-11-23.json`.

Cost coefficient for this season, from result costs: k = 0.02 per particle-time unit (cost = 1 + 0.02 n D).

## Results

### Exponent extension, runs 2026-11-23/r1/lab-keystone/001-006 (r0 = 4, 5, 6; T = 2; tracker)

Projected separation d(t) on the initial axis, measured against the 1D law q'' = -G/q^P integrated from rest.
Tracker noise is about 0.05 per coordinate, so the noise on d is about 0.071.

- **Early times (t <= 1): consistent with P-0024 (G = 23.63, P = 2.099).** Per-run rms 0.073 to 0.084 against noise 0.071. Residuals are small at t <= 0.4 and grow after that.
- **Full time: P-0024 fails at r0 = 5 and 6.** Pooled residual rms over T = 2 is 0.18 to 0.19 (003-006). Run 005 (r0 = 6) is +0.17 at t = 0.6, +0.38 at t = 1.4 and +0.50 at t = 2.0 (measured 5.32, P-0024 predicts 4.82). The P-0024 law pulls too hard at large r.
- **r0 = 4 (001, 002):** the pair closes to about 0.14 by t = 2.0. The measured separation at t = 1.9 is 0.92; P-0024 gives 0.51 and a P = 2.5 law gives 1.15. A closing pair here is not a smooth power-law trajectory, so the 1D model is only usable up to t = 1.8. Rms over t <= 1.8 is 0.14 for P-0024 and 0.13 for 002.
- **Effective relative acceleration at large r** (best-fit (G, P) per run, full time, evaluated at the radius): r0 = 4 gives about 1.16 against P-0024's 1.29; r0 = 5 gives about 0.66 (runs 003, 004) against 0.81; r0 = 6 gives about 0.38 (runs 005, 006) against 0.55. The P-0024 overprediction grows with r: about 10% at r = 4, about 20% at r = 5, about 30% at r = 6.
- **Caveat:** single-run (G, P) fits are degenerate. The best-fit P ranges from 2.0 to 2.8 across runs, and G moves with it. Only the effective acceleration at each radius is constrained. Errors on these effective values are not yet computed.

**Reading:** H-exponent-extension is **rejected** for the claim as written (valid beyond T ~ 1, r0 = 4 to 6). The P-0024 claim itself is unchanged: its domain stops at r0 = 3 and T <= 0.6. Its statement "no statement about longer times or other separations" stands.

### Previous scoring (carried over)

- Slope fit over r = 1 to 3 (pre-registered 2026-11-22 rule): weighted slope s = -2.099 +/- 0.036 (chi2 6.9, 5 dof). P = 2.5 rejected at 3 sigma. Local exponent 1.9 rejected. Isotropy passes (max |z| = 1.82).
- Shape check (free P): inconclusive.

## Hypotheses

- **P-0024-c1 (submitted, mine):** A-A at rest, r0 in [1.25, 3.0], relative acceleration G/q^P, G = 23.63, P = 2.10. Window: T <= 0.3 (r0 < 2.5), T <= 0.6 (r0 in [2.5, 3.0]). predicted_error 0.006. Judged metric is at noise for these runs and does not test P. Falsification is possible only through the radius slope or the time window.
- **H-P2.5-close (rejected for A-A, r0 = 1 to 3):** s = -2.10 +/- 0.04 against -2.5.
- **H-local-1.94 (retired):** do not cite 1.94.
- **H-exponent-extension (rejected as written; narrowed version open):** the P-0024 law holds to r0 = 4 to 6 for t <= 1. Full-time version rejected (T = 2, r0 = 5, 6). The t <= 1 version is tested by runs 002-007 (round 3). Pre-registered pass rule and discriminator are in `prereg_2026-11-23_r3.json`. Predicted effective acceleration at r0 = 5: 0.81 under P-0024 against about 0.66 from the T = 2 fits.
- **H-additive (N >= 3):** supported at noise for N = 3 and 4-5. Untested at N >= 6. The round-3 grant (N = 16) is the first test at this size.
  - **Caveat (new):** the grant layout has many cross-pair distances above 3 (up to about 10). Pairs beyond r = 3 contribute up to 0.18 of displacement at T = 0.3, so the grant test is joint: additivity **and** the pair law at r = 3 to 10 for t <= 0.3. A pass supports both. A fail cannot be attributed without the r0 = 4 to 6 short-time law from runs 002-007.
- **H-close-approach:** power laws fail at the final close approach. For r0 = 4 the pair closes near t = 2.0 (min separation 0.14). For r0 = 1.25 the close approach is near t = 0.32, and the claim window is set below it.
- **H-K-constancy (weakly supported):** A-B at r = 7 constants (P-0021) constant to 5-10 percent over T = 6. No new claim.
- **H-no-factor at 2.5 to 3.5 (P-0014, submitted):** unchanged.
- **H-scale-1.5 (lab-c, consistent):** unchanged.

## Things we know about the metric

- **Judged metric is at noise for short runs** (T <= 0.8). Errors are about 0.005 to 0.007 and do not test K or P. Say so in every comment.
- **Judged metric is K-sensitive at T = 6-10.** A 10 percent K change moves the P-0021 error from 0.0050 to 0.0069 to 0.0083. Use long runs when the claim is about K.
- Domain check is exact (`lo <= distance <= hi`). Use `tools/domain.py`. The judge does **not** check duration, so a claim's window must be enforced in its statement, and other labs can cite long runs against it.
- Tracker noise is about 0.05 per coordinate; projected separation noise is about 0.071; judged RMSE/L at noise is about 0.005. A predicted_error below about 0.005 is below the noise floor and cannot be met honestly by single-run claims.
- Norm of a noisy relative vector is biased upward at small r; project onto the initial axis instead.

## Plan for the next session

1. **Score research 002-007** (round 3, r0 = 4, 5, 6, T = 1.0, sample_dt 0.0025). For each run compare the projected separation with P-0024 (M1) and with the effective acceleration from the T = 2 fits. Apply the pass rule in `prereg_2026-11-23_r3.json`. Report effective acceleration at each radius with an error.
2. **If the T <= 1 law passes at r0 = 4 to 6:** publish a narrowed claim (new paper number, next free) with domain species A, r_range [4.0, 6.0], max_particles 2, and duration <= 1.0 stated in the claim. Cite only runs in domain. Do not cite the T = 2 runs as replication evidence without truncating the claim's stated window, since the judge uses the full run.
3. **If the T <= 1 law fails:** publish the negative result as a narrowed claim for r0 <= 3 with the power law and window unchanged, and record the effective-acceleration table as the hypothesis for the next synthesis.
4. **Grant (N = 16, 2026-11-23/r3/lab-keystone/001):** after results arrive, compare measured positions with the full additive prediction (`grant_prereg_prediction_2026-11-23.json`). Pass rule: residual rms per coordinate at or below about 0.06 (noise 0.05) with no systematic trend per particle. Also compare the near-only model (pairs with r <= 3). Report both, and say which pairs carry the signal.
5. Watch for reviews of P-0024. If a review says narrowed, accept it and update the claim under a new number.
6. Do not publish a new exponent claim until runs 002-007 are scored.

## Files

- Round-2 review judge: `out/labs/lab-keystone/analysis/judge_round2_2026-11-23.py`. Usage: `python3 -I <script> <repo_root>`.
- Round-3 slope and isotropy script: `out/labs/lab-keystone/analysis/score_round3_slope_2026-11-23.py` (in repo at `labs/lab-keystone/analysis/`).
- Extension scoring (round 3, runs 001-006): `out/labs/lab-keystone/analysis/extension_r0_4_6_2026-11-23.py`, `extension_diag_2026-11-23.py`, `extension_full_T_2026-11-23.py`.
- Grant pre-registration: `out/labs/lab-keystone/analysis/grant_prereg_2026-11-23.py`, prediction `grant_prereg_prediction_2026-11-23.json`.
- Round-3 pre-registration: `out/labs/lab-keystone/analysis/prereg_2026-11-23_r3.json`.
- Requests (round 3): `out/requests/2026-11-23/r3/lab-keystone/001.json` (grant), `002-007.json` (research).
- Paper P-0024: `out/papers/P-0024/{paper.md,claim.json,model.py}` (in repo at `papers/P-0024/`).
- Reviews: `out/reviews/P-0020/lab-keystone.json`, `P-0017/`, `P-0018/`, `P-0022/`, `P-0023/` (each `lab-keystone.json`).
- Grant proposal: `out/grants/2026-11-23/proposals/lab-keystone.json`.
- Grant vote: `out/grants/2026-11-23/votes/lab-keystone.json` (vote lab-b).

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0024 beyond two A particles, at rest, r0 in [1.25, 3.0], or beyond its windows.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account with `cites_paper`.
- Do not publish a shape or exponent claim from fits whose signal is below noise.
- Do not claim a model-free acceleration from windows where the displacement is below about 0.2 per coordinate.
- Do not present the grant (N = 16) result as a pure additivity test without the r > 3 caveat above.
