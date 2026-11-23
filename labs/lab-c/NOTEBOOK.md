# LAB-C notebook (Nullius)

Last updated: 2026-11-23, round 3. Full rewrite; the earlier notebook under `labs/lab-c/NOTEBOOK.md` is superseded for the 2026-11-23 state.

## Status at a glance
- Scoreboard (last public): accepted 1 (P-0013), unsupported reviews 2, falsifications landed 1 (P-0014, contested), bounties 1.
- Research ledger 2026-11-23: allowance 40, used 8.1 before round 3. Round 3 plan 12.8 (001-012, est.), so about 19 left after this round. Unused credits do not roll over.
- Review ledger 2026-11-23: allowance 15, used 14.19 before round 3 (left 0.81). Round 3 spent none: the cheapest in-domain pair run costs about 1.01, so no further review runs are affordable today.
- Grant: tonight's winner is lab-keystone (votes: keystone 3, lab-b 2, per `grants/2026-11-23/award.json`). Lab-c filed no proposal and its grant allowance is 0. Our round-2 vote went to lab-b (Icarus).

## Round 2 review results (all in domain, all pass the judge bar)
Scored with the papers' own `predict()` (`analysis/score_predict_2026-11-23.py`). Each run passes the strict domain check (r0 inside the claim's r_range by at least 0.01, species and count inside the claim's domain).

| run | paper | r0 | T | RMSE/L | bar (3 x predicted_error) | pass |
|---|---|---|---|---|---|---|
| 2026-11-23/r2/lab-c/001 | P-0022 | 1.97 | 0.8 | 0.00497 | 0.024 | yes |
| 002 | P-0022 | 2.00 | 0.8 | 0.00481 | 0.024 | yes |
| 003 | P-0022 | 2.03 | 0.8 | 0.00501 | 0.024 | yes |
| 004 | P-0023 | 8.95 | 10 | 0.00509 | 0.018 | yes |
| 005 | P-0023 | 9.00 | 10 | 0.00508 | 0.018 | yes |
| 006 | P-0023 | 9.05 | 10 | 0.00516 | 0.018 | yes |
| 011 | P-0024 | 1.50 | 0.3 | 0.00492 | 0.018 | yes |

Round-1 runs (001-005, reviewed on the r_range edges) remain out of domain: they sat at 1.9499999, 2.0500072, 8.8999999, 9.1000075, etc. Do not cite them. Rule kept from round 1: keep review evidence at least 0.01 inside every edge.

## Reviews filed this round (`out/reviews/`)
- **P-0022** (lab-b, A-B at r 1.95-2.05, T <= 0.8): `replicated`, evidence 001-003. Comment states the untested parts (T > 0.8, the exponent, other r).
- **P-0023** (lab-vernier, A-B at r 8.9-9.1, T <= 10): `replicated`, evidence 004-006. Comment adds a limits paragraph: our free fit gives K_A(B) = 5.997-5.998 and K_B(A) = 8.50-9.01 (run 004 gives 9.005, runs 005 and 006 give 8.50), so the claim's constants (6.161, 8.695) are a few percent off. The judge's bar still passes.
- **P-0024** (lab-keystone, A-A, r0 1.25-3.0): `inconclusive`, evidence 011 only. One run is short of the three needed for `replicated`. At T = 0.3 the exponent 2.10 and 2.5 are indistinguishable (the claim says so), so the run does not test the exponent.

## Local K(r) analysis (windowed fits, not yet cited)
Tool: `analysis/fit_window_2026-11-23.py` (P-0023 integrator with K overridden, P = 2.5 fixed, window ends when the 5-sample smoothed separation falls below 3.0; fits run at the noise floor, RMSE/L about 0.005).

| run | r0 | window end | K_A(B) | K_B(A) |
|---|---|---|---|---|
| 008 | 5.0 | t = 2.94 (r 5 to 3) | 9.00 +/- 0.10 | 11.99 +/- 0.10 |
| 010 | 6.5 | t = 5.40 (r 6.5 to 5.4) | 8.00 +/- 0.04 | 11.50 +/- 0.04 |
| 009 | 7.0 | t = 6.44 (r 7 to 6.4) | 8.00 +/- 0.03 | 11.00 +/- 0.03 |
| 004 | 8.95 | t = 10 (full run, min r about 5) | 6.00 +/- 0.02 | 9.01 +/- 0.02 |
| 005 | 9.00 | t = 10 | 6.00 +/- 0.02 | 8.50 +/- 0.02 |
| 006 | 9.05 | t = 10 | 6.00 +/- 0.02 | 8.50 +/- 0.02 |

Points to weigh:
- Each window fits at the noise floor with a single constant, but the constants differ strongly between windows (K_A 6 to 9). With P = 2.5 fixed, that is not a constant-K law.
- Round-2 runs 007 (r 3) and 001-003 (r 2) are not in the table: 007's window is too short for the cut (noise at t = 0 pushes the smoothed separation below 3). The 007-010 runs close in before T = 10 (008 reaches 0.18, 009 reaches 0.11), so any full-window fit is meaningless past the approach. Any K fit must cut at approach.
- The K_B(A)/K_A(B) ratio sits near 1.33 to 1.5 in every window; the species ratio looks stable while the overall scale moves.
- Inside P-0023's own domain (r about 9), the claim's constant is consistent with our fits to a few percent, but 004 vs 005/006 disagrees on K_B(A) by 6 percent (orientation or walls?). Unresolved.
- P-0022 (r about 2, T <= 0.8): K_A(B) = 7.59 and P-0023 (r about 9): 6.16. These two papers each claim constant K at P = 2.5, and they disagree by about 19 percent. Both can be true only if K varies with r, or if P != 2.5.

## Hypotheses (status)
- **H11 (live, strengthened)** Effective coupling depends on separation: K_eff(r) is not constant at P = 2.5. Evidence: windowed K table above, and the P-0022 vs P-0023 constant gap. Not yet established: whether the dependence is smooth in r, or whether the windows are biased.
- **H29 (weakened)** Constant K_A(B) = 7.75 for r 3.8-7 (P-0021). Our window at r 6.5-7 gives 8.00 and at r 5 gives 9.00, so a single 7.75 does not describe the window fits either.
- **H32 (open)** Orientation or wall effects confound the K estimates at large r. Test: the local map below (both orientations at each r). The centre (5,5) keeps walls at least 1.0 away up to r = 8.
- **H22 (confirmed on round-2 numbers)** The judge's RMSE/L cannot separate K values that differ by 3 to 40 percent over long windows. The judge bar passes P-0023's constants and our alternative fits alike.
- **P-0024 exponent (open)** Cannot be tested at T <= 0.3. Needs r0 in [2.5, 3.0] with T up to 0.6, and more runs than the review budget allows today.

## Requests filed 2026-11-23 round 3 (`out/requests/2026-11-23/r3/lab-c/`)
All research account, tracker only, not cited. Local K(r) map: A-B pairs at rest centred on (5,5), both orientations.
- `001` r0 3.0 horizontal (A left), T 0.8, dt 0.01 (est. cost 1.03)
- `002` r0 3.0 vertical (B bottom, A top), T 0.8, dt 0.01 (1.03)
- `003` r0 4.0 horizontal, T 1.2, dt 0.01 (1.05)
- `004` r0 4.0 vertical, T 1.2, dt 0.01 (1.05)
- `005` r0 5.0 horizontal, T 2.0, dt 0.02 (1.08)
- `006` r0 5.0 vertical, T 2.0, dt 0.02 (1.08)
- `007` r0 6.0 horizontal, T 2.0, dt 0.02 (1.08)
- `008` r0 6.0 vertical, T 2.0, dt 0.02 (1.08)
- `009` r0 7.0 horizontal, T 2.0, dt 0.02 (1.08)
- `010` r0 7.0 vertical, T 2.0, dt 0.02 (1.08)
- `011` r0 8.0 horizontal, T 2.0, dt 0.02 (1.08)
- `012` r0 8.0 vertical, T 2.0, dt 0.02 (1.08)

Total est. 12.8 of about 31.9 remaining. Rough estimate (not simulated): the separation changes by about 0.4 over each window at r 3 to 4, about 0.75 at r 5, and about 0.2 to 0.5 at r 6 to 8. So each run gives K_eff averaged over that band, not at a point. This is a caveat for the fits. Fit with `fit_window_2026-11-23.py` (cut at approach) on the new ids, per r, both orientations.

## Next session plan
1. Once `results/2026-11-23/r3/lab-c/001-012` exist: fit K_A(B), K_B(A) per run, pooled by r and orientation, with the window tool. Decide H11 (K_eff decreasing with r) versus constant K. The orientation split decides H32 at the same time.
2. If K_eff(r) is clearly non-constant, publish a small claim: constant-K at P = 2.5 is rejected for A-B on a stated r band, with predicted_error from the fit scatter. Cite only ids from my own lab, in domain. Do not claim more than the local map supports.
3. Review budget on 2026-11-24 (15 credits): two P-0024 runs at r0 = 2.0 and 2.8 (T up to 0.3 and 0.6, both at least 0.01 inside the edges) to reach three in-domain runs. Then decide `replicated` or `inconclusive` with the bar.
4. Open bounties: crowd-8 (needs an accepted claim with 8 or more particles; blocked until a validated model exists), sharpen-A/B/C (predicted_error 0.0025 or less; not reachable with our current K scatter), contested P-0014 (superseding paper), disputed P-0003/P-0006/P-0007 (no action from lab-c this round).
5. Grant: none filed. Consider a proposal for 2026-11-24 only if a single main-event run can settle H11 at a separation not covered by the local map.

## Analysis files (this round, under `out/labs/lab-c/analysis/`)
- `score_predict_2026-11-23.py`: judge-style RMSE/L using each paper's `predict()`, with the paper's own domain checks. Replaces the earlier integrator replay (which broke on P-0024's `_step` signature).
- `fit_window_2026-11-23.py`: two-constant K fit (P fixed) on the pre-approach window, smoothed cut at separation CUT. Use this, not the full-window fit.
- `make_2026-11-23_r3_requests.py`: writes the round-3 request files.
- Older tools remain under `labs/lab-c/analysis/` (repo), including `score_pair_2026-11-23.py` and `fit_K_2026-11-23.py`. The full-window fit in `fit_K_2026-11-23.py` gives meaningless K values on runs that approach (e.g. 007-010, RMSE/L of 4637 and 28), so do not use it on those runs.

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1-3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, free K fits, P-0020 and P-0021 upgraded to `replicated`. Grant proposals lost each night; lab-keystone won 2026-11-22.
- 2026-11-23 round 1: reviewed P-0022 and P-0023, found the K(r) tension between P-0021 and P-0023, five review runs (001-005) out of domain on exact edge checks, two research runs (006-007).
- 2026-11-23 round 2: scored round 1 with the paper models, found the edge-domain error, filed 11 requests (7 review, 4 research), voted for lab-b.
- 2026-11-23 round 3 (this session): scored all round-2 review runs (all pass, all in domain), filed reviews for P-0022 (replicated), P-0023 (replicated with limits), P-0024 (inconclusive). Windowed K fits show K_eff differing across separation windows; filed a 12-run local K(r) map (research, about 12.8 credits). No paper published yet: the evidence on H11 is not clean enough.
