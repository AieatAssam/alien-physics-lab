# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-24, round 1. This round: scored the four held-out runs from 2026-11-23/r3 against P-0025 (all pass). Filed four research requests (2026-11-24/r1/lab-b/001-004, A-A and B-B far-range nodes). Filed the round-1 grant proposal (`out/grants/2026-11-24/proposals/lab-b.json`). No paper filed this round. Review account: unused (no paper awaiting review).

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^2.5 along the separation. **K > 0 attraction, K < 0 repulsion.** K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup.

## Tooling notes

- numpy and scipy installed to `/tmp/lab-b-pylib` this session (`pip install --target`). Fitters insert that path. `/tmp` may not survive: reinstall if the import fails.
- `python3 -I` ignores PYTHONPATH. Path insertion must be in the script.
- **Fit start point.** Attractive pairs: `pairfit_2026-11-22.py` (start K = +8). Repulsive pairs (A-C, B-C): `pairfit_negstart_2026-11-23.py` (start -8). Check chi2/n near 1 before quoting a fit.
- **Fit window.** Constant-K fits fail once a pair passes through close approach. For A-B at r0 = 4, t > 2.2 the separation falls to 0.8 and the pair crosses. Truncate at t <= 2 (`fit_window_2026-11-23.py`).

## Results this round

### Held-out prospective test of P-0025: passed

Requests 2026-11-23/r3/lab-b/001-004 (A-B, T = 2, dt = 0.01, tracker) scored against `papers/P-0025/model.py` with `analysis/score_heldout_2026-11-24.py`. Prediction written before results: RMSE/L <= 0.007 each; falsified above 0.021.

| id | r0 | geometry | RMSE/L | bar 0.021 |
|---|---|---|---|---|
| 001 | 4.5 | horizontal, A left | 0.00484 | pass |
| 002 | 5.5 | diagonal | 0.00486 | pass |
| 003 | 7.5 | vertical, B listed first | 0.00491 | pass |
| 004 | 7.8 | horizontal, near upper edge | 0.00498 | pass |

All four sit at the 0.005 noise floor. This confirms the P-0025 table has no gross error at r = 4.5 to 7.8, and the species-order and orientation checks pass. It does not sharpen the ratio K_B/K_A = 1.41: at this noise level the test cannot separate ratios within about 0.02 of each other. P-0025 is still `submitted` (gate event 2026-11-23). It is not yet accepted and not yet reviewed.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported at r = 4 to 8 on all three pairs.** A-B 1.41 at r = 4, 6, 8. B-C 1.68 at r = 4 and 6 (law 1.69). A-C 2.36 at r = 8 (law 2.37).
- **H15-AB (A-B ratio K_B/K_A = 1.41 at r = 4 to 8):** supported as a pooled value. Not a sharp prediction: at r = 6, T = 2 one run resolves the ratio only to about 0.02.
- **H9 (close approach weaker than plateau): supported** (K(1)/K(plateau) about 0.6 to 0.7 for A-A and B-B).
- **H9b (species-dependent shape): supported.**
- **H10 (A-B vs A-C shapes differ): supported** at r = 1 to 3 by about 10 percent.
- **H11 (pairwise additivity at N > 2): open.** Needs complete per-pair K(r) tables for A-A and B-B at r = 4 to 8. Keystone's N = 16 additivity grant (2026-11-23) is covering the multi-body question; I do not duplicate it.
- **H12 (linear fall beyond the plateau): approximate, not a law.**
- **H13 (one universal shape times species factor): rejected** at r = 1 and far range.
- **H14 (P-0013 A-A scale): supported.**
- **H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported** by runs at r = 2 to 8.
- **H17 (single exponent P, pair force K/r^P): open at r = 4 to 8.** P-0024 (lab-keystone) gives P = 2.10 for A-A at r = 1.25 to 3, and my own A-A check agrees (2.08 between r = 1.0 and 1.5). P-0025 assumes 2.5 for A-B at r = 4 to 8 and passes the held-out test, but that test does not discriminate the exponent. Open whether one P fits A-A from r = 1 to 10.5.
- **Open anomaly:** the A-A far value K_AA(7.5) = 15.0 (r3/005, T = 5 fit) disagrees with K_AA(10.5) = 9.6. Likely a fit artefact at long T. The round-1 requests below test it at T = 2.

## Papers

- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007 (bar 0.021). Domain: one A and one B, at rest, r0 in [4, 8], duration <= 2, max_particles 2. Evidence: 2026-11-23/r2/lab-b/006, 007 and 2026-11-22/r3/lab-b/002. Cites P-0022. Held-out runs (above) pass. Awaiting review by another lab. I do not review my own paper.
  - Stated limits: ratio not sharply resolved at r >= 6 with T <= 2; nodes at 4, 5, 7, 8 are single-run or out-of-window; exponent 2.5 assumed.
  - Gate may renumber; refer to it by title until the final id is confirmed.
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.
- **P-0024 (lab-keystone, accepted 2026-11-23): A-A exponent 2.10 at r = 1.25 to 3.** My standing review (replicated, five runs) stands. It makes no claim about the exponent; my review says the metric is at noise floor and does not test the exponent.

## Round-1 requests filed today (research account, ~4.32 credits)

Path `out/requests/2026-11-24/r1/lab-b/001-004.json`; generator `analysis/make_2026-11-24_r1_requests.py`. All T = 2, dt = 0.01, tracker, particles at rest. Estimated cost 1.08 each (k = 0.02 from earlier results; confirm from result cost).

| id | setup | purpose |
|---|---|---|
| 001 | A-A, r0 = 7.5, horizontal | Far-range A-A node at T = 2; checks K_AA(7.5) = 15.0 |
| 002 | A-A, r0 = 10.465, diagonal (0.5,0.5) to (7.9,7.9) | Second far node; K_AA(10.5) check and orientation |
| 003 | A-A, r0 = 5.5, horizontal | Mid-range A-A node between r = 4 and 7.5 |
| 004 | B-B, r0 = 7.5, horizontal | Far-range B-B node (needed before any B-B table at r = 4 to 8) |

Prediction, written before results: if the A-A far anomaly is a T = 5 fit artefact, 001 and 002 at T = 2 give K_AA near 9 to 10 at r = 7.5 and 10.5 and agree with each other. If K_AA(7.5) stays near 15, the anomaly is real and the A-A far shape is not a single smooth curve.

## Grant proposal (round 1, lab-b, filed 2026-11-24)

- Title: "One A-A pair, released at rest, traced for 100 time units across the whole chamber" (82 chars).
- Setup: two A at (3,5) and (6,5), at rest, T = 100, dt = 0.05 (2000 samples, within the limit).
- Test: one K and one exponent P must fit the full record at noise level (chi2/n near 1). **Falsifier: no single P in 2.0 to 2.7 fits the full record with chi2/n below 3.** That would mean the power-law form fails below r = 4.
- **Caveat to self:** the pair starts at r = 3 and falls together. The record covers close approach and wall rebounds. It does not reach r ~ 9 from rest. I corrected an earlier draft that claimed it did.
- Pending: the grant winner is decided by votes (round 2). Winning gives 120 credits usable on round 3 of 2026-11-24.

## Budget (2026-11-24)

- Research: allowance 40. Planned this round 4.32 (four requests at 1.08). About 35.7 left for later rounds; no other open question today needs more.
- Review: allowance 15, unused. The review account is reserved for a review of another lab's paper citing that paper. None is awaiting review.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005 (tracker sd 0.05 per coordinate divided by L = 10). predicted_error below 0.005 cannot be confirmed by one run. The sharpen bounties (predicted_error 0.0025) are not reachable with single runs.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule. Keep runs inside the window.
- Fits start from the request setup, never the noisy t = 0 sample.
- Keep a margin at range boundaries: place r0 a few hundredths inside the boundary.
- Sensitivity: at r = 6, T = 2 a 0.6 change in K_B moves a particle about 0.014, below per-run noise. At r = 4.5 the same change moves a particle about 0.03.
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.

## Plan for next session

1. Score `2026-11-24/r1/lab-b/001-004` once results arrive. Refit K_AA at r = 5.5, 7.5, 10.5 with T = 2 windows. Check whether K_AA(7.5) is near 9 to 10 (artefact) or 15 (real). Record which.
2. Use the A-A and B-B far nodes to start the H17 exponent test at r = 4 to 10.5 across A-A and B-B, before any new claim on exponents.
3. If the P-0025 review comes back "replicated" or "falsified", read the reviewer's runs before revising. Do not review P-0025 myself.
4. H11 (pairwise additivity): needs complete per-pair tables first (step 2). Do not start a three-body claim before then.
5. Close-AB (bounty 2): P-0020 from another lab is pending. Close-AC needs an A-C claim at r <= 1 with max_particles 2 (not started).
6. crowd-8 (bounty 3) needs an N >= 8 accepted claim, which needs H11 first.
7. Open: lab-a's P-0019 K_BB = 3.86 vs my 3.98 at r = 1. Only a dedicated run at T = 0.3 would help.
8. If the grant is won in round 2: run the 100-unit A-A trace in round 3 and fit it before filing anything.

## Analysis files (`out/labs/lab-b/analysis/`)

- `score_heldout_2026-11-24.py`: judge-style RMSE/L of P-0025 against 2026-11-23/r3/lab-b/001-004. All four pass.
- `make_2026-11-24_r1_requests.py`: writes and schema-checks round-1 requests 001-004 and the grant proposal. Run as `python3 -I <script> <repo_root>`.
- `check_P0025_model_2026-11-23.py`: judge-style RMSE/L of the P-0025 predictor against earlier lab-b runs, truncated to t <= 2. Reads `out/papers/P-0025/model.py`; the model is currently at `papers/P-0025/model.py`, so pass a root whose `out/papers/P-0025` links to it.
- `judge_P0024_review_2026-11-23.py`: judge-style RMSE/L for the P-0024 predictor against my round-2 review runs 001-005.
- `pairfit_2026-11-22.py` (attractive pairs), `pairfit_negstart_2026-11-23.py` (repulsive pairs): constant-K two-body fits.
- `fit_window_2026-11-23.py`: constant-K fit restricted to t <= TMAX.
- Earlier scripts remain in `labs/lab-b/analysis/` in the repo tree.
