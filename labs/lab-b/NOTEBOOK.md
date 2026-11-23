# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-23, round 2 (filed: review of P-0024, research 006-009, grant vote for lab-keystone). No paper filed this round.

## Sign and unit conventions

- Pair force on particle i from j: acceleration K_ij / r^2.5 along the separation. **K > 0 attraction, K < 0 repulsion.** K_ij is the acceleration of i due to j.
- Newton's third law for a central pair: m_i K_ij = -m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j.
- Fits: tracker sd 0.05 per coordinate, P = 2.5 fixed, specular walls, start state from the request setup. Scripts in `out/labs/lab-b/analysis/`.

## Tooling notes (2026-11-23)

- numpy and scipy are not installed system-wide. They were installed to `/tmp/lab-b-pylib` (pip --target). `pairfit_2026-11-22.py` inserts that path. `/tmp` may not survive a session: reinstall if the import fails.
- `python3 -I` ignores PYTHONPATH. Put the path in the script with `sys.path.insert`.
- **pairfit's start point is K = +8 for both particles.** For repulsive pairs (B-C, A-C) this starts on the wrong branch. Round-1 run 008 converged to an attractive minimum with chi2/n = 255. `pairfit_negstart_2026-11-23.py` starts at K = -8. Use it for any repulsive pair and check chi2/n near 1 before quoting a fit.

## Verified this round

- **P-0023 review (filed round 1 as a forecast) now checked.** Runs `2026-11-23/r1/lab-b/001-004` are all in domain (A and B, separation 8.92 to 9.05, T = 10). Judge RMSE/L 0.00523, 0.00510, 0.00514, 0.00514 against the bar 0.018. The review stands. Its evidence is 001-004 as filed.

## Round-1 research runs (005-009) fitted

Constant-K fits, chi2/n in brackets. Ratio = K_second / K_first; law from the masses 2.37 : 1.69 : 1.

| run | pair | sep | T | K_first | K_second | ratio | ratio 1-sigma (from fit errors) | law | chi2/n |
|---|---|---|---|---|---|---|---|---|---|
| r1/006 | A-B | 6.0 | 4 | K_AB 8.435 +/- 0.052 | K_BA 11.971 +/- 0.051 | **1.419** | 0.011 | 1.40 | 0.96 |
| r1/009 | A-B | 8.0 | 5 | K_AB 6.744 +/- 0.068 | K_BA 9.564 +/- 0.067 | **1.418** | 0.017 | 1.40 | 0.94 |
| r1/008 | B-C | 4.0 | 3 | K_B -6.438 +/- 0.055 | K_C -10.818 +/- 0.057 | **1.680** | 0.017 | 1.69 | 1.02 |
| r1/005 | B-C | 6.0 | 5 | K_B -5.708 +/- 0.040 | K_C -9.604 +/- 0.041 | **1.683** | 0.014 | 1.69 | 1.01 |
| r1/007 | A-C | 8.0 | 5 | K_A -6.476 +/- 0.077 | K_C -15.264 +/- 0.079 | **2.357** | 0.031 | 2.37 | 1.02 |

Run 008 used the corrected negative start (see tooling notes). The first pass (positive start) is discarded.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported at r = 4 to 8 on all three pairs.** New ratios: A-B 1.42 at r = 6 and 8 (law 1.40); B-C 1.68 and 1.68 at r = 4 and 6 (law 1.69); A-C 2.36 at r = 8 (law 2.37). The earlier r = 6 A-B break (see next section) is **not** confirmed by 006.
- **Open conflict at A-B r = 6 (window dependence).** r3/002 (T = 2): K_AB 8.95, K_BA 11.36, ratio 1.27. r1/006 (T = 4): K_AB 8.44, K_BA 11.97, ratio 1.42. Both have chi2/n about 1. The K_AB values differ by 0.5, about 10 sigma from their own errors. The fit errors cannot reconcile them, so the constant-K model is misspecified over the trajectory, and its ratio depends on the time window at the 0.1 level. The earlier "ratio is path-robust" statement was too strong. Replicates 006-008 (this round's requests) decide between a real T=2 effect and a fluke in r3/002.
- **H9 (close approach weaker than plateau): supported** (K(1)/K(plateau) about 0.6 to 0.7 for A-A, B-B; 0.7 for C-C).
- **H9b (species-dependent shape): supported.**
- **H10 (A-B vs A-C shapes differ): supported at r = 1 to 3 by about 10 percent.**
- **H11 (pairwise additivity at N > 2): open.** Needs a per-pair shape first. The COM grant test probes the mass law at N = 3 without a shape model.
- **H12 (linear fall beyond the plateau): approximate, not a law.**
- **H13 (one universal shape times species factor): rejected** at r = 1 and far range.
- **H14 (P-0013 A-A scale): supported.**
- **H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported** by runs at r = 2 to 8.
- **H17 (P = 2.5 exponent): rejected at close range by lab-keystone (P-0024), not by me.** My own rough check: K_AA(r = 1.0) = 11.11 and K_AA(r = 1.5) = 13.18, both fitted at P = 2.5. The implied power law between r = 1 and 1.5 is P = ln(2.32)/ln(1.5) = 2.08. That agrees with P-0024's 2.10. It is a consistency check on two fits with different windows, not a test.

## Coupling table (constant K at P = 2.5, positive = attraction)

Rows from earlier rounds are not re-verified. Check ids before citing.

| pair | r | T | runs | K (fit) | status |
|---|---|---|---|---|---|
| A-A | 1.0 | 0.15 | r1/005, 008, r2/001, 002 | 11.11 +/- 0.09 | P-0012 (lab-a) claims 11.3, about 2 sigma high |
| C-C | 1.0 | 0.15 | r1/006, r2/011, 012 | 9.31 +/- 0.13 | filed |
| B-B | 1.0 | 0.15 | r1/007, r2/009, 010 | 3.98 +/- 0.12 | filed; P-0019 (lab-a) 3.86 |
| A-B | 1.0 | 0.15 | r2/013, 014, r3/010, 011 | K_AB 5.39 +/- 0.09, K_BA 7.33 +/- 0.16 | filed (P-0020 pending for close-AB) |
| A-B | 2.0 | 0.8 | r1/001, r2/005 | K_AB 7.59, K_BA 10.59 | P-0022 filed |
| A-B | 3.0 | 1.5 | r1/002 | K_AB 8.65, K_BA 12.29 | one run |
| A-B | 4.0 | 2.0 | r2/006 | K_AB 9.24, K_BA 12.85 | one run (ratio 1.39) |
| A-B | 4.0 | 3.0 | 2026-11-23/r2/lab-b/009 (filed) | pending | ratio check at r = 4, longer T |
| A-B | 5.0 | 2.0 | r2/007 | K_AB 9.26, K_BA 12.60 | one run (ratio 1.36) |
| A-B | 6.0 | 2.0 | r3/002 | K_AB 8.95, K_BA 11.36 | ratio 1.27; **conflict with 2026-11-23/r1/006** |
| A-B | 6.0 | 4.0 | 2026-11-23/r1/006 | K_AB 8.44, K_BA 11.97 | ratio 1.42 |
| A-B | 6.0 | 2.0 | 2026-11-23/r2/006 (filed, repeat of r3/002) | pending | decides the conflict |
| A-B | 6.0 | 2.0 | 2026-11-23/r2/007 (filed, vertical) | pending | orientation check |
| A-B | 6.0 | 4.0 | 2026-11-23/r2/008 (filed, vertical) | pending | orientation check at T = 4 |
| A-B | 7.0 | 6 | lab-vernier P-0021 (their runs); lab-b r2/001-004 | K_AB 7.75 | P-0021 replicated by me |
| A-B | 8.0 | 2.0 | r3/005 | K_AB 6.95, K_BA 9.64 | weak (large error on K) |
| A-B | 8.0 | 5.0 | 2026-11-23/r1/009 | K_AB 6.74, K_BA 9.56 | ratio 1.42 |
| A-B | 9.0 | 10 | lab-vernier P-0023 (their runs) | K_AB 6.16, K_BA 8.70 | P-0023 reviewed by me, verified |
| A-C | 1.0 | 0.6 | r3/001-003 (round 1) | K_AC -6.19, K_CA -14.67 | P-0016 replicated by me |
| A-C | 2.0 | 0.8 | r2/008 | K_AC -8.22, K_CA -19.51 | one run |
| A-C | 3.0 | 1.5 | r1/003 | K_AC -9.01, K_CA -21.31 | one run |
| A-C | 5.0 | 2.0 | r3/003 | K_AC -8.57, K_CA -20.67 | ratio 2.41 |
| A-C | 8.0 | 5.0 | 2026-11-23/r1/007 | K_AC -6.48, K_CA -15.26 | ratio 2.36 |
| B-C | 1.0 | 0.6 | r2/006-008 | K_BC -4.27, K_CB -7.20 | P-0015 claims -4.32 / -7.31 |
| B-C | 3.0 | 1.5 | r2/009 | K_BC -6.25, K_CB -10.66 | one run |
| B-C | 4.0 | 3.0 | 2026-11-23/r1/008 | K_BC -6.44, K_CB -10.82 | ratio 1.68 (negative start) |
| B-C | 6.0 | 2.0 | r3/004 | K_BC -5.96, K_CB -9.66 | ratio 1.62 |
| B-C | 6.0 | 5.0 | 2026-11-23/r1/005 | K_BC -5.71, K_CB -9.60 | ratio 1.68 |
| A-A | 1.5 | 0.4 | r2/003 | 13.18 +/- 0.04 | P-0013 narrowed |
| A-A far | 7.5 / 10.5 | 6 / 8 | r3/005, 006 (round 2) | 15.00 / 9.63 | H12 test |
| C-C far | 7.5 / 10.5 | 6 / 8 | r3/007, 008 (round 2) | 9.94 / 6.34 | H12 test |
| B-B far | 10.5 | 10 | r3/009 (round 2) | 3.36 | H12 test |

A-B shape (K_AB vs r): 1.0 5.39, 2.0 7.59, 3.0 8.65, 4.0 9.24, 5.0 9.26, 6.0 8.95 (T=2) or 8.44 (T=4), 7.0 7.75, 8.0 6.74 to 6.95, 9.0 6.16. Rises to a flat top near 4 to 5, then falls. Not a single power law at P = 2.5. The T dependence at r = 6 is the open problem above.

## Review of P-0024 (lab-keystone, A-A pair, r0 1.25 to 3.0): filed as a forecast

- **Verdict filed: replicated.** Evidence: `2026-11-23/r2/lab-b/001-005` (review account, cites P-0024). Verdict is a forecast; the gate scores the runs after this round.
- Pre-check (`judge_P0024_forecast_2026-11-23.py`): the P-0024 predictor against my existing in-domain A-A runs, truncated to the claim window. RMSE/L 0.00497 (2026-11-21/r2/003, r0 1.5), 0.00512 (2026-11-21/r3/004, r0 1.5), 0.00495 (2026-11-18/r2/004, r0 1.5), 0.00502 (2026-11-18/r2/017, r0 2.0), 0.00496 (2026-11-18/r2/010, r0 3.0, window 0.6). Bar 0.018. All at the noise floor.
- Filed runs 001-005 test the edges: r0 1.27 (lower edge, T 0.3, near the collapse the claim sets at t about 0.32), 2.98 (upper edge, T 0.6), 2.0 diagonal, and 2.45 and 2.6 either side of the 2.5 window switch.
- **Limits I stated in the review:** the judged metric is at the tracker noise floor, so it does not test the exponent (P = 2.10 vs 2.5). I make no statement on the exponent. Not tested: other species, N > 2, durations beyond the window, close approach after t = 0.3.
- If the gate scores fewer than three of 001-005 at or under 0.018, the review is unsupported. Record that here and do not file further reviews on this basis.

## Grant

- **Round 2 vote: lab-keystone.** Reason: N = 16 pair additivity with a clear falsifier (residuals above about 0.05 per coordinate), about 1.1 credits, and it addresses the multi-body question crowd-8 needs.
- Not voted: Vernier's A-B test at separation 2. It checks my own claim P-0022 directly, and I did not weigh it higher on that basis. Its test is a precision test in the pair domain, not a discriminating one. Plumbline (N = 9 at T = 50): chaos would blur the 0.02 cut.
- My own proposal (COM test, masses 2.37 : 1.69 : 1) is pending the round-2 result. If it wins, the 120 credits are usable in round 3.

## Budget (2026-11-23)

- Research: allowance 40. Round 1 used 5.88. Round 2 planned 4.44 (006-009). Total about 10.3, about 29.7 left. I am not spending the rest: no open question today needs more runs than these four.
- Review: allowance 15. Used 5.6 (P-0023 runs 2026-11-23/r1/001-004). Round 2 planned 5.08 (2026-11-23/r2/001-005). Total about 10.7, about 4.3 left.
- Requests are in `out/requests/2026-11-23/r2/lab-b/001-009.json` (validated against `protocol/request.schema.json`). Review requests 001-005 cite P-0024; research 006-009 do not.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor 0.005 (tracker sd 0.05 per coordinate divided by L = 10). A predicted_error below 0.005 cannot be confirmed by one run; the sharpen bounties (predicted_error 0.0025) are not reachable.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule; the model raises beyond it. Keep runs inside the window.
- Fits start from the request setup, never the noisy t = 0 sample.
- Keep a margin at range boundaries (a run at the edge of r_range was rejected once). Use r0 a few hundredths inside the boundary.
- Repulsive pairs (A-C, B-C) push particles toward walls within a few time units at r <= 4. Keep them short or centred.
- Attractive pairs at r = 1 collapse by T = 0.3. At r = 2 the separation falls to about 0.45 by T = 0.8.

## Plan for next session

1. Score the P-0024 review runs `2026-11-23/r2/lab-b/001-005` with `judge_P0024_forecast_2026-11-23.py` adapted to the real duration (the runs already have duration equal to the window). Confirm three or more are at or under 0.018. Record the result here.
2. Fit the A-B r = 6 replicates: 2026-11-23/r2/lab-b/006 (horizontal, T = 2, repeat of r3/002), 007 (vertical, T = 2), 008 (vertical, T = 4). Use `pairfit_2026-11-22.py`. If 006 comes back near 1.27 at T = 2, the T = 2 vs T = 4 difference is real: the constant-K model is misspecified and the mass law needs a shape model before any claim. If 006 comes back near 8.9 and 11.4 with ratio about 1.27, r3/002 stands. If 006 gives 1.40 to 1.42 again, r3/002 was a fluke: pool the T = 2 runs.
3. Fit 009 (A-B at r = 4, T = 3): ratio at r = 4 with a longer window.
4. Decide on a paper for the mass-ratio law only after step 2. Candidate scope: ratios at r = 4 to 8, with a model that interpolates K(r) from the pooled table. Do not file a far-range claim without a model that fits r = 2 to 8 in one function.
5. Use the 120 credits only if my COM proposal wins (round 3 credit account `grant`). Test: COM drift below 0.01 under the mass law, about 0.14 under equal masses.
6. crowd-8 (bounty 3) needs an N >= 8 accepted claim, which needs H11 first. The COM test and Keystone's N = 16 test (if it wins) are the steps.
7. close-AB (bounty 2): P-0020 from another lab is pending. close-AC needs an A-C claim at r <= 1 with max_particles 2 (A-C at 1.0 from round-1 runs, not started).
8. Open: lab-a's P-0019 K_BB = 3.86 vs my 3.98 at r = 1. Only a dedicated run at T = 0.3 would help.

## Analysis files (`out/labs/lab-b/analysis/`)

- `make_2026-11-23_r2_requests.py`: writes today's requests 001-009 to `out/requests/`.
- `judge_P0024_forecast_2026-11-23.py`: judge-style RMSE/L for the P-0024 predictor against my A-A runs, truncated to the claim window.
- `pairfit_2026-11-22.py`: constant-K two-body fit (needs numpy and scipy).
- `pairfit_negstart_2026-11-23.py`: same, starting at K = -8 for repulsive pairs. Use this for B-C and A-C.
- `judge_P0023_2026-11-23.py`: judge-style RMSE/L for P-0023 (verified this round).
- `mixed_grid_2026-11-23.py`: 2-D grid check of two-coupling fits and ratio 1-sigma.
- `grant_com_design_2026-11-23.py`: N-body centre-of-mass design check.
