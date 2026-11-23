# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-23, round 3. Filed this round: paper P-0025 (A-B table, separation 4 to 8, T <= 2), four held-out research requests (2026-11-23/r3/lab-b/001-004), and the round-3 notebook. Review account: unused this round (no paper awaiting review).

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^2.5 along the separation. **K > 0 attraction, K < 0 repulsion.** K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup.

## Tooling notes

- numpy and scipy were installed to `/tmp/lab-b-pylib` this session (`pip --target`). The fitters insert that path. `/tmp` may not survive: reinstall if the import fails.
- `python3 -I` ignores PYTHONPATH. Path insertion must be in the script.
- **Fit start point.** `pairfit_2026-11-22.py` starts at K = +8 for both particles. For repulsive pairs (A-C, B-C) use `pairfit_negstart_2026-11-23.py` (starts at -8). Check chi2/n near 1 before quoting a fit.
- **Fit window.** Constant-K fits fail once a pair passes through close approach. For A-B at r0 = 4, t > 2.2 the separation falls to 0.8 and the pair crosses (`2026-11-23/r2/lab-b/009`). Fits must be truncated at t <= 2 for that run. Use `fit_window_2026-11-23.py`.

## Results this round (round 2 runs, now scored)

### P-0024 review (lab-keystone, A-A) scored

Review `reviews/P-0024/lab-b.json` was filed as "replicated" with evidence 2026-11-23/r2/lab-b/001-005. Pre-check against the paper's own predictor (`judge_P0024_review_2026-11-23.py`, judge-style RMSE/L over t > 0):

| run | r0 | T | RMSE/L | bar (3 x 0.006) |
|---|---|---|---|---|
| 001 | 1.27 | 0.3 | 0.00487 | 0.018 |
| 002 | 2.98 | 0.6 | 0.00508 | 0.018 |
| 003 | 2.00 | 0.3 | 0.00519 | 0.018 |
| 004 | 2.45 | 0.3 | 0.00504 | 0.018 |
| 005 | 2.60 | 0.6 | 0.00510 | 0.018 |

All five are under the bar, so the review's verdict stands on the metric. Scope caveat stated in the review still holds: the metric is at the noise floor and does not test the exponent (P-0024 says 2.10, my K_AA values give about 2.08 between r = 1 and 1.5). I make no statement on the exponent.

### A-B at separation 6: the r3/002 conflict is resolved

Windowed constant-K fits (`fit_window_2026-11-23.py`, truncated to t <= 2; K_A = acceleration coefficient of A due to B):

| run | orientation | window | K_A | K_B | ratio K_B/K_A | chi2/n |
|---|---|---|---|---|---|---|
| 2026-11-22/r3/lab-b/002 | horizontal | T=2 | 8.95 +/- 0.24 | 11.36 +/- 0.24 | **1.27** | 1.00 |
| 2026-11-23/r2/lab-b/006 | horizontal | T=2 | 8.45 +/- 0.24 | 11.94 +/- 0.24 | 1.413 | 0.96 |
| 2026-11-23/r2/lab-b/007 | vertical | T=2 | 8.28 +/- 0.24 | 11.75 +/- 0.24 | 1.418 | 1.05 |
| 2026-11-23/r2/lab-b/008 | vertical | T=2 (full T=4: ratio 1.403) | 8.64 +/- 0.34 | 11.65 +/- 0.33 | 1.349 | 1.01 |
| 2026-11-23/r1/lab-b/006 | horizontal | T=2 (full T=4: ratio 1.419) | 8.25 +/- 0.34 | 11.92 +/- 0.33 | 1.445 | 0.97 |

Reading: four of five runs agree at 1.35 to 1.45, centred near 1.41. r3/002 (1.27) is about 2 sigma from that centre and is the outlier. It is kept as evidence in P-0025 and not hidden. **The "ratio breaks at r = 6" hypothesis is not supported.** The ratio is the mass ratio, 1.41 +/- 0.02 from these runs, consistent with 2.37 / 1.69 = 1.40 from the three-pair fit.

### A-B at separation 4 (009) and window effects

- Full T = 3 window: K_A 5.64, K_B 10.36, chi2/n 58. **Misfit.** The pair reaches separation 0.8 at t about 2.5 and passes through (no events). Constant-K cannot describe this.
- Window t <= 2: K_A 9.05 +/- 0.10, K_B 13.09 +/- 0.10, ratio 1.447, chi2/n 0.91. Window t <= 1.5: K_A 8.89, K_B 13.28, ratio 1.495 (error larger, consistent).
- Earlier r2/006 (r=4, T=2) gave ratio 1.39. Ratio at r = 4 from the T <= 2 windows is 1.39 to 1.45. Not separately resolved from 1.41.

### Current A-B shape (K_A(r), P = 2.5, constant-K windows)

| r | K_A | source | status |
|---|---|---|---|
| 1.0 | 5.39 | r2/013, 014, r3/010, 011 | filed (P-0020 pending) |
| 2.0 | 7.59 | r1/001, r2/005 | P-0022 (mine) |
| 3.0 | 8.65 | r1/002 | one run |
| 4.0 | 9.05 (T <= 2) | 2026-11-23/r2/009 | window test above |
| 5.0 | 9.26 | r2/007 (earlier round) | one run |
| 6.0 | 8.52 (mean of five T <= 2 fits) | the runs in the table above | P-0025 node |
| 7.0 | 7.75 | lab-vernier P-0021 (T=6) and my r2/001-004 | not checked at T <= 2 |
| 8.0 | 6.85 | r1/009 (T=5) and r3/005 (T=2) | P-0025 node |
| 9.0 | 6.16 | lab-vernier P-0023 | reviewed, verified |

K_B / K_A = 1.41 at every separation tested for this pair (6, 4, and 8 within 0.04). Not tested at 2, 3, 5, 7, 9: the ratio is taken as constant in P-0025 only on the basis of the r = 4, 6, 8 values.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported at r = 4 to 8 on all three pairs.** A-B 1.41 at r = 4, 6, 8. B-C 1.68 at r = 4 and 6 (law 1.69). A-C 2.36 at r = 8 (law 2.37).
- **H15-AB (A-B ratio K_B/K_A = 1.41 at r = 4 to 8):** supported, see above. **Note:** at r = 6 and T = 2 the tracker cannot resolve the ratio sharper than about 0.02 per run. The ratio is a pooled consistency value, not a sharp prediction.
- **H9 (close approach weaker than plateau): supported** (K(1)/K(plateau) about 0.6 to 0.7 for A-A and B-B).
- **H9b (species-dependent shape): supported.**
- **H10 (A-B vs A-C shapes differ): supported** at r = 1 to 3 by about 10 percent.
- **H11 (pairwise additivity at N > 2): open.** Blocked on a complete per-pair K(r) table for A-A and B-B at r = 4 to 8. The A-A far values (K_AA(7.5) = 15.0 from r3/005) look inconsistent with K_AA(10.5) = 9.6. Needs re-checking before any additivity test. The COM grant test was my proposal and it lost to Keystone.
- **H12 (linear fall beyond the plateau): approximate, not a law.**
- **H13 (one universal shape times species factor): rejected** at r = 1 and far range.
- **H14 (P-0013 A-A scale): supported.**
- **H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported** by runs at r = 2 to 8.
- **H17 (P = 2.5 exponent): not tested by me.** P-0024 (lab-keystone) rejects 2.5 for A-A at r = 1.25 to 3 (exponent 2.10). My own A-A check agrees (2.08 between r = 1.0 and 1.5). Whether the exponent is 2.5 at r = 4 to 8 is open. The P-0025 model assumes 2.5 and does not test it.

## Papers

- **P-0025 (filed this round, lab-b): A-B pair, separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007 (bar 0.021). Domain: one A and one B, at rest, r0 in [4, 8], duration <= 2, max_particles 2. Evidence: 2026-11-23/r2/lab-b/006, 007 and 2026-11-22/r3/lab-b/002 (all T = 2, r0 = 6). Pre-check: RMSE/L 0.0048 to 0.0051 against each of these runs and against r2/008 and r1/006 truncated to t <= 2 and r2/009 truncated to t <= 2. Model file: `out/papers/P-0025/model.py`. Cites P-0022.
  - Limits stated in the paper: the ratio is not sharply resolved at r >= 6 with T <= 2; nodes at 4, 5, 7, 8 are single-run or out-of-window; exponent 2.5 assumed.
  - Use the paper number as filed by the gate. The repo has no P-0025 yet (checked at filing).
- **P-0022 (mine, earlier): A-B at separation 2, T <= 0.8.** Unchanged.

## Predictions for the held-out runs (prospective test of P-0025's table)

Requests `2026-11-23/r3/lab-b/001-004` (research, T = 2, dt = 0.01, tracker):

| id | r0 | geometry | tests |
|---|---|---|---|
| 001 | 4.5 | horizontal, A left | interpolation between nodes 4 and 5 |
| 002 | 5.5 | diagonal | nodes 5 and 6, orientation independence |
| 003 | 7.5 | vertical, **B listed first** | nodes 7 and 8, species order |
| 004 | 7.8 | horizontal, near upper edge | upper edge of domain |

Prediction (written before results): judge RMSE/L <= 0.007 for each run. A run above 0.021 falsifies the P-0025 table at that separation. Expected displacement at r = 4.5 over T = 2 is about 0.4 to 0.7 per particle, larger than at r = 6 (about 0.2), so r = 4.5 is the most sensitive point to the ratio.

## Budget (2026-11-23)

- Research: allowance 40. Used before this round 10.32 (round 1 5.88, round 2 4.44). Round 3 planned 4 requests at 1.08 each = 4.32. Total about 14.64, leaving about 25.4. I am not spending the rest: no open question today needs more runs than these.
- Review: allowance 15. Used 10.67 (P-0023 runs 5.57 in round 1 and P-0024 runs 5.1 in round 2). About 4.3 left. No paper awaiting review this round.
- Grant: I did not win. Keystone (lab-keystone) won tonight with its N = 16 pair-additivity proposal (120 credits). My COM proposal lost. No grant credits for lab-b.

## Round 2 grant vote (for the record)

- Voted for lab-keystone. Reason: N = 16 pair additivity with a clear falsifier (residuals above about 0.05 per coordinate), about 1.1 credits, and it addresses the multi-body question crowd-8 needs.
- Not voted: Vernier's A-B test at separation 2. It checks my own P-0022 directly. Its test is a precision test in the pair domain, not a discriminating one.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor 0.005 (tracker sd 0.05 per coordinate divided by L = 10). predicted_error below 0.005 cannot be confirmed by one run. The sharpen bounties (predicted_error 0.0025) are not reachable.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule. Keep runs inside the window.
- Fits start from the request setup, never the noisy t = 0 sample.
- Keep a margin at range boundaries. Use r0 a few hundredths inside the boundary. Run 009 sits exactly at r = 4.0 and was not cited in P-0025 for that reason.
- Sensitivity: at r = 6, T = 2 a 0.6 change in K_B moves a particle about 0.014, below the per-run noise. At r = 4.5 the same change moves a particle about 0.03.
- Repulsive pairs (A-C, B-C) push particles toward walls within a few time units at r <= 4. Keep them short or centred.

## Plan for next session

1. Score the held-out runs `2026-11-23/r3/lab-b/001-004` against `out/papers/P-0025/model.py` (`check_P0025_model_2026-11-23.py <root> 2026-11-23/r3/lab-b/00X`). Record RMSE/L and whether each is under 0.021. If the r4.5 run is above 0.021, the K_A(4)-(5) nodes are wrong: refit the table before any revision.
2. Watch the gate's result for P-0025. If another lab reviews it, read their runs before filing a revision. Do not review P-0025 myself.
3. Re-check the A-A far-range values (K_AA(7.5) = 15.0 vs K_AA(10.5) = 9.6). Likely a fit artefact at T = 6. A refit at T <= 2 would settle it. Do this before any additivity or A-A claim at r > 6.
4. For H11 (pairwise additivity): needs complete A-A, B-B and A-B tables at r = 4 to 8 before a three-body test. Not before step 3.
5. Close-AB (bounty 2): P-0020 from another lab is pending. close-AC needs an A-C claim at r <= 1 with max_particles 2 (A-C at 1.0 from round-1 runs, not started).
6. crowd-8 (bounty 3) needs an N >= 8 accepted claim, which needs H11 first.
7. Open: lab-a's P-0019 K_BB = 3.86 vs my 3.98 at r = 1. Only a dedicated run at T = 0.3 would help.

## Analysis files (`out/labs/lab-b/analysis/`)

- `judge_P0024_review_2026-11-23.py`: judge-style RMSE/L for the P-0024 predictor against my round-2 review runs 001-005. All under the 0.018 bar.
- `pairfit_2026-11-22.py`: constant-K two-body fit (needs numpy and scipy). Copied from the earlier lab tree.
- `fit_window_2026-11-23.py`: constant-K fit restricted to t <= TMAX. Used for the r = 4 and r = 6 window tests.
- `check_P0025_model_2026-11-23.py`: judge-style RMSE/L of the P-0025 predictor against lab-b runs, truncated to t <= 2. Pre-check for P-0025 and the held-out test.
- `make_2026-11-23_r3_requests.py`: writes and schema-validates the round-3 held-out requests 001-004.
- Earlier scripts (`judge_P0023_2026-11-23.py`, `judge_P0024_forecast_2026-11-23.py`, `pairfit_negstart_2026-11-23.py`, `mixed_grid_2026-11-23.py`, `grant_com_design_2026-11-23.py`) remain in `labs/lab-b/analysis/` in the repo tree. They are not copied into `out/`.
