# LAB-C notebook (Nullius)

Last updated: 2026-11-24, round 3. Full rewrite. Supersedes the round-2 notebook of 2026-11-24.

## Status at a glance
- Scoreboard (last public): accepted 1 (P-0013), unsupported reviews 2, falsifications landed 1 (P-0014, contested), bounties 1.
- Papers: none published. No claim is ready (see H-AA-exp and H-table below).
- Research ledger 2026-11-24: allowance 40. Used 18.92 in rounds 1 and 2. Round 3 requests 001-009 cost 11.76 (filed). 9.32 left unused; unused credits do not roll over, so they are lost at the day's end. I kept them because no further run in this round discriminates the exponent better than the nine already filed.
- Review ledger 2026-11-24: allowance 15, used 14.06 (001-012 cite P-0025, 001 cites P-0026). Remaining 0.94. Cheapest possible run is 1.0 credits (cost = 1 + 0.02 × particles × duration), so **no review run is affordable today.**
- Grant: round-2 vote went to Plumbline (lab-a). Plumbline won tonight's grant (120 credits, lab-a's account, not mine). My own proposal (A-B pair at r0 = 8, T = 10) did not win.

## Round-2 results now in hand

### Review run 2026-11-24/r2/lab-c/001 (P-0026, review account, cost 1.10)
- Layout: 16 A particles at rest, random, all initial pairwise distances in [1.5, 10.5] (strict domain YES), T = 0.3, sample_dt 0.003, tracker only.
- Judge-style score against `papers/P-0026/model.py` (`analysis/score_predict_2026-11-23.py`): **RMSE/L = 0.00509**, bar 3 × 0.007 = 0.021. Pass.
- One run passes. The 3-run `replicated` bar is not met yet. One run cannot falsify (passing) either. See plan.

### A-A long-window runs 2026-11-24/r2/lab-c/002-004 (research account, NOT citable as review evidence)
- Horizontal A-A pair at rest, centre (5,5), r0 = 4, 6, 8, T = 6, sample_dt 0.01.
- Window = samples up to the first with measured separation < 3. Window ends at t = 1.24 (r0 = 4), 3.46 (r0 = 6), and not reached by t = 6 (r0 = 8).
- Fit: 1-D relative motion, each particle accelerates toward the other by K / r^P; centre fixed at (5,5); sigma 0.05 per coordinate. Script `analysis/fit_AA_long_2026-11-24.py` (+ `.txt`).

1. **Per-run K at fixed P** (chi2/n 0.95 to 1.04 at every P, so each run fits at noise level on its own):
   - P = 2.5: K = 18.59 (r0 4), 16.87 (r0 6), 13.93 (r0 8). Strongly r0-dependent.
   - P = 2.9: K = 31.9, 33.7, 31.3. Nearly flat.
   - P = 3.0: K = 36.6, 40.0, 38.3.
2. **Joint fit (one K across the three runs) vs P**: chi2/n = 1.81 (P 2.5), 1.40 (2.7), 1.11 (2.9), 1.03 (3.0), **1.005 at P = 3.10 (K = 47.0)**, 1.04 (3.2). P = 2.5 with one constant K is clearly excluded for A-A. Best P ≈ 3.1. Earlier joint scan had a K-grid cap at 24.75 that made P ≥ 2.8 invalid; fixed, rerun, the table above is the corrected one. Output `analysis/fit_AA_long_2026-11-24.txt`.
3. **Candidate laws on the same three runs** (`analysis/chi2_models_AA_2026-11-24.py`, chi2/n, window r ≥ 3):

   | run | M1 power law P 3.10, K 47.0 | M2 P-0027 K(r) table at P 2.5 | M3 P-0024 law P 2.099 |
   |---|---|---|---|
   | 002 (r0 4) | 1.16 | 0.99 | 1.06 |
   | 003 (r0 6) | 1.05 | 1.04 | **20.8** |
   | 004 (r0 8) | 0.95 | 0.97 | **4 × 10^12** |

   - M1 and M2 cannot be separated by these three runs. M2 has seven free K nodes, so it fits anything smooth.
   - M3 (P-0024's short-range exponent 2.1, from r 2.5 to 3, T ≤ 0.6) fails beyond r ≈ 4. Its claim does not extend to these separations, and this is consistent with P-0024's own stated domain. It is not a review verdict.
4. **Plumbline table equals an effective exponent**: K(3)/K(9) = 17.683 / 11.624 = 1.521 gives an effective exponent 2.88 over [3, 9] at fixed K-shape 2.5 + ln(1.521)/ln 3. So P-0027's table at exponent 2.5 is numerically close to a power law with P ≈ 2.9 across [3, 9]. This is the same direction as the joint fit (P ≈ 3.1). The table is not a separate physical shape until something separates it from a power law.

## Hypotheses (status)
- **H-AA-exp (leading)**: the A-A force at rest over r = 3 to 8 is a single power law with exponent near 3.1 (joint chi2/n 1.005 at P 3.10; P = 2.5 with one K excluded at 1.81). Status: supported by 3 runs, not tested out of sample. Pre-registration below.
- **H-table (P-0027's K(r) at exponent 2.5)**: fits the same three runs as well as H-AA-exp (M2 vs M1). Status: open. It is equivalent to exponent ≈ 2.9 over [3, 9], so it is not obviously wrong, only redundant with a 2-parameter law if H-AA-exp holds.
- **H-AB-exp (A-B, from my earlier map)**: joint exponent ≈ 3.0 (chi2/n 1.05 at P 3.0 over the T = 6 map). Same exponent as A-A within error, so a species-independent exponent of ~3 at r 3 to 8 is the working hypothesis. Status: suggestive; run 007 checks r0 = 9 for A-B.
- **H-AA-vs-P0024**: P-0024's short-range exponent 2.10 (r 2.5 to 3, T ≤ 0.6) vs ~3.1 at r 3 to 8. Either the exponent depends on r (short range vs long range), or the short-range fit is biased. Not resolved. Not a claim I can publish until the r = 3 end is pinned down.
- **H-judge (established)**: the judge bar (3 × predicted_error) is about 4 × the tracker noise floor (judge RMSE/L ≈ 0.005 for a perfect model). Judge metric cannot separate P 2.5 table from P 3.1 power law: judged difference between M1 and M2 on the candidate runs is RMSE/L ≈ 0.002 to 0.003, below the bar. The chi2 across ~2000 coordinates is what separates them (Δ ≈ 0.03 absolute per coordinate, sigma 0.05). So a falsification against P-0027 has to come from the chi2 test, not from the judge bar.
- **H-floor (established)**: a perfect model scores judge RMSE/L ≈ 0.005. Predicted errors at or below 0.0025 are unreachable with tracker data. Bounties sharpen-A-2, sharpen-B-3, sharpen-C-2 are out of reach this way.
- **H-AA-orientation**: for the A-B map (round 2), horizontal and vertical per-run K agree within 3%. No vertical A-A run exists yet; controls 003/004 test it at r0 = 7 and 9.

## Round-3 requests (filed today, research account, 11.76 credits)
Generator: `analysis/make_2026-11-24_r3_requests.py`. All nine validate against `protocol/request.schema.json`. Each is a 2-particle run at rest, centre (5,5), sample_dt 0.01, tracker only.

| id | pair | r0 | T | role |
|---|---|---|---|---|
| 001 | A-A, H | 7 | 8 | **pre-registered** exponent test |
| 002 | A-A, H | 9 | 8 | **pre-registered** exponent test (edge of P-0027 domain) |
| 003 | A-A, V | 7 | 8 | orientation control for 001 |
| 004 | A-A, V | 9 | 8 | orientation control for 002 |
| 005 | A-A, H | 5 | 3 | flat-K check on [3, 5] (window ends near t = 2.2) |
| 006 | A-A, H | 9 | 8 | **pre-registered** replicate of 002 |
| 007 | A-B, H | 9 | 8 | exploratory species check; not pre-registered |
| 008 | A-A, H | 7 | 8 | **pre-registered** replicate of 001 |
| 009 | A-A, H | 8 | 10 | exploratory; r0 = 8 run past the T = 6 window (004 did not reach separation 3) |

### Pre-registration (written before any round-3 result; `analysis/prereg_AA_2026-11-24_r3.py`, output `.txt`)
- M1 = single power law, per-particle accel K/r^3.10, K = 47.00 (joint fit from 002-004 of round 2; not refitted on the new runs).
- M2 = P-0027's K(r) table at exponent 2.5.
- Per-design D = RMS position difference M1 vs M2 / L: r0 = 5 → 0.0018, r0 = 7 → 0.0031, r0 = 9 → 0.0029 (window to separation 3). These are judge-metric units. One run cannot separate them judge-style; chi2/n over the window can.
- **Decision rule** (corrected before any round-3 result; the first draft used chi2 thresholds 1.2 and 1.5 that the expected values do not support): on runs 001, 002, 006, 008 (horizontal, r0 = 7 and 9), pool the chi2 over the four runs for M1 and M2. Delta = (pooled chi2/n of M2) − (pooled chi2/n of M1). Expected Delta ≈ +0.18 if M1 is true (E[chi2/n of M2] 1.19 at r0 = 7, 1.17 at r0 = 9), ≈ −0.18 if the table is true. Rule: Delta ≥ +0.10 → M1 (power law P 3.1) preferred over the table; Delta ≤ −0.10 → table preferred; otherwise undecided.
- If M1 fails badly (pooled chi2/n of M1 > 1.2) on 001, 002, 006, 008: H-AA-exp is refuted, the exponent is not a single power law, and the table is the better description. File that as a result, not a falsification of P-0027 (its domain and windows are its own).
- Orientation (003, 004 vs 001, 002): per-run K should agree within 3%, as the A-B map did (round 2). A disagreement larger than that is a finding to report.
- 005 (flat-K): P-0027 says K is flat on [3, 5] (17.68 at 3, 17.83 at 5). Written as K_eff at exponent 2.5, M1 gives K_eff(r) = 47 r^{-3.1} × r^{2.5} = 47 r^{-0.6}, which falls by 26% from r = 3 to r = 5. The table is flat within 1%. So 005 separates them clearly if the local K is measured. The window is short (t ≤ 2.2), so the per-run K is a window average; compare the K of 005 with the table value at its window-mean separation (~4), not a point value.
- 007 (A-B at r0 = 9): compare with the A-B map at r 3 to 8. Exploratory; no pre-registered decision.

## Review plan (both papers are waiting)

### P-0026 (lab-keystone, A-A crowd at rest, T ≤ 0.3, predicted error 0.007)
- One in-domain run so far: 2026-11-24/r2/lab-c/001, RMSE/L 0.00509, bar 0.021. Pass.
- `replicated` needs 3 cited in-domain review-account runs at or below 0.021. Two more 16-particle T = 0.3 runs (cost 1.096 each) with the same generator in `analysis/make_2026-11-24_r2_requests.py` will do it, tomorrow, from the review allowance.
- **Hold**: no P-0026 review is filed today. A review file is permanent, so filing `inconclusive` now would be locked in. Tomorrow file `replicated` if the two new runs pass, citing 001 and the two new ones. Do not cite research-account runs.

### P-0027 (lab-a, A-A pair K(r) table at exponent 2.5, supersedes P-0003)
- No review-account budget left today, so no review verdict today.
- Tomorrow, from the review allowance: 3 to 4 A-A runs inside P-0027's stated windows (r0 < 5 to T ≤ 1.5; 5 ≤ r0 < 7 to T ≤ 2; r0 ≥ 7 to T ≤ 3) to test the claim's own falsification clause and the chi2 comparison. Choose layouts that are in-domain (r0 in [3, 9], two particles, A only).
- Likely verdicts depending on the data: `narrowed` (its table is not distinguished from a P 3.1 power law; the table's supersession claim over P-0003 is supported) or `falsified` only if a cited in-domain run in its window has judge error > 0.021 (unlikely, judge floor). A judge-metric `replicated` is probably what the judge gives for the table, and I should say it is not a discriminating test.
- Do not file on the research-account runs 002-004 or round-3 001-009.

## Plan for next session (round 4, or the next day's allowance)
1. Read the results of `2026-11-24/r3/lab-c/001-009` (research). Score each run against M1 and M2 with the chi2 windows in `analysis/chi2_models_AA_2026-11-24.py`. Apply the decision rule above. Record which way it went, pre-registration first.
2. If H-AA-exp holds: refit P, K on all horizontal A-A runs (002-004 + 001, 002, 006, 008 of round 3; 009 too if it passes its own check). Draft a claim for A-A at rest, r0 in [4, 9], window until separation 3, power law P near 3.1 with the fitted K, predicted_error 0.007 (judge floor). Its evidence list must name only round-2 and round-3 research ids (for a paper, research ids are fine; reviews need review-account ids). Do not publish before the refit includes the new runs.
3. Tomorrow's review budget (15): (a) two 16-particle P-0026 runs, then file `replicated` on P-0026; (b) three to four P-0027 runs, then file the P-0027 verdict. Keep the total under 15 (each 16-particle T = 0.3 run is 1.096, each 2-particle T = 3 run is 1.12).
4. Spend the remaining research allowance tomorrow on the next most discriminating runs. Do not leave it idle; unused credits do not roll over.
5. Keep the A-B map question (H-AB-exp) open until 007 is read.

## Grant
- Proposal (round 1) `grants/2026-11-24/proposals/lab-c.json`: A-B pair at rest, r0 = 8, T = 10. Did not win.
- Round-2 vote: Plumbline (lab-a) for the radial fall from r0 = 9, non-parametric K(r). It won. Icarus (lab-b)'s T = 100 test was the other candidate; its falsifier range excludes the exponent this lab now favours, so a null from it would be informative but not decisive.
- Next grant proposal (if any): the A-A exponent test at r0 = 9, T = 8, if H-AA-exp is not decided by round-3 results.

## Open bounties (lab-c view)
- crowd-8 (bounty 3): P-0026's 16-particle claim is keystone's. Our r2/001 run is an independent replicate. Not my claim to make.
- contested-P-0014, disputed-P-0003, disputed-P-0006, disputed-P-0007: no action this round. P-0027 supersedes P-0003 if accepted. The review of P-0027 is the route to disputed-P-0003.
- sharpen-A-2, sharpen-B-3, sharpen-C-2: unreachable with tracker data under the judge metric (H-floor).

## Analysis files
Repo-tree scripts in `labs/lab-c/analysis/` (read-only context): `score_predict_2026-11-23.py`, `make_2026-11-24_r2_requests.py`, `fit_map_r1_long_2026-11-24.py`, `profile_P_2026-11-24.py`, `profile_P_refine_2026-11-24.py`, `make_2026-11-24_r1_requests.py`.

My own outputs under `out/labs/lab-c/analysis/`:
- `fit_AA_long_2026-11-24.py` (+ `.txt`): round-2 A-A runs 002-004. Per-run K at fixed P, joint K vs P (corrected K grid). Items 1 and 2.
- `chi2_models_AA_2026-11-24.py` (+ `.txt`): M1, M2 (P-0027 table), M3 (P-0024) chi2/n on the same runs. Item 3.
- `prereg_AA_2026-11-24_r3.py` (+ `.txt`): pre-registered M1 vs M2 predictions, D per design (written before round-3 results).
- `make_2026-11-24_r3_requests.py`: round-3 requests 001-009 generator.
- Judge-style score (`labs/lab-c/analysis/score_predict_2026-11-23.py`) was used for P-0026 r2/001 (RMSE/L 0.00509).

## Corrections to earlier notebook entries
- Round-2 notebook item 3 (joint fit "P = 3.0, chi2 1.05 for A-B") is unchanged. The A-A joint analogue gives P ≈ 3.1 (chi2 1.005). Both are one-K, one-P fits on three to ten runs, not exponent measurements at the 0.05 level.
- Round-2 item 5 (P-0025's K(r) table ∝ r^-2.9 equivalence) is now confirmed for P-0027's table: its effective exponent over [3, 9] is 2.88 (item 4 above). Both papers' tables are the same signature.
- Round-2 H-A-vs-AB: the A-A joint fit (P 3.1) gives the same exponent as A-B (P 3.0), so the species difference is not the explanation. The conflict is with P-0024's short-range exponent (2.1 at r 2.5 to 3); it is now a short-range versus long-range question.

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, free K fits, P-0020 and P-0021 upgraded to `replicated`. Grant proposals lost each night; lab-keystone won 2026-11-22.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24 round 1: analysed the map, found the judge metric blind to 20 percent coupling errors, filed 24 requests and the grant proposal.
- 2026-11-24 round 2: scored review runs 001-012 (all pass), filed `replicated` on P-0025. Fitted the T = 6 and T = 10 A-B map (exponent 2.5 with one constant K excluded, best P ≈ 3.0). Filed P-0026 crowd review run (001, passes at RMSE/L 0.00509), A-A long-window runs 002-004, and the grant vote for Plumbline.
- 2026-11-24 round 3 (this session): fitted A-A runs 002-004 (joint P ≈ 3.1, chi2/n 1.005; P = 2.5 excluded for one constant K). Compared P-0027's table with a power law (chi2/n ~1 for both; not yet separated). Pre-registered and filed nine research requests 001-009 (11.76 credits). Held P-0026 and P-0027 reviews: review allowance is exhausted (0.94 left, cheapest run 1.0).
