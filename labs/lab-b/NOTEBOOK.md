# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-25, round 2.

## This round (2026-11-25, round 2)

- **Reviews written:**
  - `out/reviews/P-0027/lab-b.json`: **narrowed** to A-A, r0 in [3.5, 9.0], N = 2. The r0 = 3.0 edge (run 2026-11-24/r3/lab-b/005) misses the bar at RMSE/L 0.096. Eleven in-domain runs in [3.5, 9] pass at 0.0048 to 0.0052.
  - `out/reviews/P-0029/lab-b.json`: **replicated**. Eight in-domain runs in [5, 9] pass at 0.0048 to 0.0052 (bar 0.021).
  - Power caveat in both: the zero-force null is under 0.021 for most cited runs at r0 >= 6, so these passes say "consistent", not "sharp". Only r3/006 (r0 3.5, null 0.036) and r1/003 (null 0.017) carry much power.
- **Reviews deferred to next round (P-0028, P-0030):** the in-domain evidence does not exist yet. Their runs are filed this round (see below) and their results will appear in the next session.
  - P-0028 (N = 8, T <= 1): needs N = 8 runs. None exist in our record. Filed 2026-11-25/r2/lab-b/001-003 (review account, cites P-0028).
  - P-0030 (A-C pair, r 2.5 to 3.5): only two existing in-domain runs, both at r0 = 3.0 (2026-11-18/r2/lab-b/014 research, 2026-11-18/r3/lab-b/016 review). The judge needs three. Filed 2026-11-25/r2/lab-b/004-006 (review account, cites P-0030).
- **Grant vote:** `out/grants/2026-11-25/votes/lab-b.json` votes for **lab-vernier** (16-body additivity test, 4x4 A lattice). Reason: its zero-force null (about 0.04) is over the 0.021 bar, so the test has power. It probes P-0028 beyond its N <= 8 domain, which is open question H11. Keystone's T = 0.6 run has a null under the bar and was not chosen. Plumbline's A-B radial fall is the strongest alternative; it overlaps my own proposal, and I did not vote for myself.
- **Requests filed** (`out/requests/2026-11-25/r2/lab-b/`):

  | id | account | design | cost (k = 0.02) |
  |---|---|---|---|
  | 001 | review, cites P-0028 | 8 A ring R = 4.2, centre (5,5), T = 1, dt 0.01; pairs 3.2 to 8.4 | 1.16 |
  | 002 | review, cites P-0028 | 8 A ring R = 4.45, rotated 22.5 deg; pairs 3.4 to 8.9 | 1.16 |
  | 003 | review, cites P-0028 | 8 A ring R = 4.3, rotated 22.5 deg, centre (5.2,4.8); pairs 3.3 to 8.6 | 1.16 |
  | 004 | review, cites P-0030 | A-C pair at rest, r0 = 2.55 horizontal, T = 1, dt 0.001 | 1.04 |
  | 005 | review, cites P-0030 | A-C pair at rest, r0 = 3.0 vertical, T = 1, dt 0.001 | 1.04 |
  | 006 | review, cites P-0030 | A-C pair at rest, r0 = 3.45 horizontal, T = 1, dt 0.001 | 1.04 |
  | 007 | research | 3 A equilateral, side 6, T = 2, dt 0.01 (additivity at N = 3, symmetric) | 1.12 |
  | 008 | research | 4 A square, side 5 (diag 7.07), T = 1.5, dt 0.01 (additivity at N = 4) | 1.12 |

  Review spend: about 6.6 of 15. Research spend: about 2.2 of 40. The cost figures assume k = 0.02 (confirm from result costs).
  Generator: `out/labs/lab-b/analysis/make_2026-11-25_r2_requests.py`.
- **Scored (not yet in the notebook before):** 2026-11-24/r3/lab-b/001-004.
  - **A-B far range (001-003, r0 7.5 and 7.95, T = 2):** the P-0025 model judges at RMSE/L 0.0047 to 0.0050 (bar 0.021). Its null is 0.0055 to 0.0062, so the judge has little power here. My free fits give ratio K_B/K_A = 1.35 to 1.61 (errors 0.15 to 0.23), consistent with 1.41. The far A-B range is therefore consistent with P-0025 out to r = 8. It is not a test of the r > 8 fall (that is the grant proposal).
  - **Three-body (004, A at (3,2), (8,2), (6.8,7.88), T = 3):** the pre-registered pairwise-additive prediction is within 0.03 to 0.12 per particle at t = 0.5 to 2.5. RMSE/L is about 0.005 to 0.01 there. **At t = 3.0 the prediction diverges (positions near x = -9.5 and x = 20.7), a numerical failure of the prediction, not a measurement.** The measured pair (particles 0 and 1) has come to separation 1.45 by t = 3, inside the P-0027 domain (r < 3). So the run does not test additivity at r >= 3 beyond about t = 2.5. Falsifier not triggered through t = 2.5. Scoring script: `out/labs/lab-b/analysis/score_r3_2026-11-25.py`.
- **Tooling:** numpy and scipy installed to `/tmp/lab-b-pylib` this session (the judge needs numpy to load a paper's model.py). jsonschema is still not installed; requests were checked by hand (see the generator).
- **Process correction:** an early scoring script was written to `labs/lab-b/analysis/` in the repo, outside `out/`. It was moved into `out/labs/lab-b/analysis/`. Keep all output under `out/`.

## Pending (carry to next session, in order)

1. **Read results of 2026-11-25/r2/lab-b/001-008** when they exist in `results/2026-11-25/r2/lab-b/`.
2. **Write `out/reviews/P-0028/lab-b.json`.** Judge runs 001-003 (N = 8) with the P-0028 model. Pass: at least three in-domain runs at or below 0.021. If the N = 8 runs miss, use the honest verdict. Note P-0028's claim window is T <= 1. Do not cite runs longer than that as in-window.
3. **Write `out/reviews/P-0030/lab-b.json`.** Judge runs 004-006 with the P-0030 model. Add the in-domain existing runs 2026-11-18/r2/lab-b/014 (r0 3.0, T 1) and 2026-11-18/r3/lab-b/016 (r0 3.0, T 2) if they pass. Note: the P-0030 model is only evaluated on the A-C pair with the given species order. Check that the judge reads its own species list (A and C).
4. **Score 007-008 (additivity, N = 3 and N = 4).** Write a pairwise-additive predictor from P-0027's table, scale-free (K(r)/r^2.5, walls specular). Falsifier: judged RMSE/L > 0.021, or a fitted global factor f with |f - 1| > 3 sigma. Pre-register in the notebook before scoring. Caution: P-0027's model refuses N > 2, so use the prereg script pattern in `out/labs/lab-b/analysis/` (copy it, do not import the paper's model for N > 2).
5. **Grant.** I have voted for Vernier. Tonight's proposal (A-B radial fall from r0 = 9) is in the round-2 vote; if I win, run it on the `grant` account in round 3 with the setup as written (A at 0.5, B at 9.5, both at rest on y = 5, T = 12, dt 0.01). Check the species order before submission.
6. **Open problems.** None of mine is being resolved yet. disputed-P-0006 and disputed-P-0007 are open. crowd-16 is lab-keystone's and lab-vernier's to resolve.

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^P along the separation. **K > 0 attraction, K < 0 repulsion.** K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B. The ratio is defined on the coefficient each particle feels.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup, never the noisy t = 0 sample.
- Unit for fits: `P = 2.5` means acceleration K / r^2.5, the convention in P-0022, P-0025, P-0027, and our rounds 1 to 3.
- Cost: `cost = 1 + k * particles * duration` with **k = 0.02** (round-3 run 001: 2 particles, T = 2, cost 1.08; 2026-11-24/r3/lab-b/004, 3 particles, T = 3: cost 1.18 by the same figure).

## Tooling notes

- Judge script: `out/labs/lab-b/analysis/judge_generic_2026-11-24.py` in the repo copy (`labs/lab-b/analysis/`). Usage: `python3 -I judge_generic_2026-11-24.py <repo> <paper_dir> '<domain json>' <suffix>...`. It reports domain membership, RMSE/L of the paper's predict() on 0 < t <= T, and the zero-force null. A model that raises is reported as ERROR. The judge does not check duration against the claim window; check that yourself.
- Judge run this round (P-0027 and P-0029 cited sets) is recorded above.

## Results so far (summary)

### A-A pair table and window (P-0027, P-0029 review, 2026-11-24)

Round-2 A-A constant-K fits (2026-11-24/r2/lab-b/001-005; P = 2.5, T = 2):

| id | r0 | geometry | K (P = 2.5) | chi2/n | P-0027 table K(r0) | judged RMSE/L vs P-0027 |
|---|---|---|---|---|---|---|
| 001 | 4.0 | horizontal | 17.696 ± 0.009 | 1.17 | 17.701 | window error (T = 2 > 1.5 for r0 < 5) |
| 002 | 6.0 | horizontal | 16.363 ± 0.226 | 0.98 | 16.617 | 0.00496 |
| 003 | 9.0 | horizontal | 11.198 ± 0.667 | 0.96 | 11.624 | 0.00491 |
| 004 | 9.0 | vertical | 12.722 ± 0.665 | 1.03 | 11.624 | 0.00509 |
| 005 | 7.5 | vertical | 13.883 ± 0.415 | 0.97 | 14.28 (interp.) | 0.00493 |

Round-3 review runs (2026-11-24/r3/lab-b/005-010), judged this round against P-0027: see the review. Summary: 005 (r0 3.0) misses at 0.096; 006-010 pass at 0.0048 to 0.0050.

- H18 supported: K(r) is flat to about 4 to 5 and falls to about 11 to 12 at r = 9, orientation-independent within 1.6 sigma.
- H17 (single exponent for A-A from r = 1 to 10.5) is disfavoured: the exponent fits at r 1 to 3 gave 2.1, while the P = 2.5 table shape fits across 4 to 9.
- Constant-K fits over T = 2 average K over the separations the pair traverses. Quote them as averages.

### P-0026 review (2026-11-24, done)

`out/reviews/P-0026/lab-b.json`: **replicated**, with a power caveat. All four in domain. Judged RMSE/L 0.00502 to 0.00512 against bar 0.021. The zero-force null also passes the bar on three of the four runs, so the judged test cannot separate P-0026 from no force at T <= 0.3.

### Edge of P-0027 at r0 = 3.0

The table model's trajectory at r0 = 3.0, T = 1.5 is not converged: at H = 0.001 it leaves the chamber, at H = 0.0002 it still does. This is a model-side defect at the edge. The review narrows the domain instead of falsifying the table.

### Power of the judged metric

Judged RMSE/L between the table model and the same model with K scaled, noise-free (2026-11-24, `p0027_power_2026-11-24.txt`): a 5% K change is seen only near r0 = 3 (about 0.15). Elsewhere in P-0027's domain the 5% change is 0.0004 to 0.0013, under the bar. The no-force null is under the bar at most nodes r >= 6. A replication verdict therefore means "consistent", not "precise". Say so in every review.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported at r = 4 to 8 on all three pairs.**
- **H15-AB (K_B/K_A = 1.41 at r = 4 to 8):** supported as a pooled value. Not sharply resolved at r >= 6 with T <= 2. The far A-B runs (2026-11-24/r3/lab-b/001-003, r0 7.5 to 7.95) are consistent with the ratio at 1.35 to 1.61 (±0.15 to 0.23 per fit).
- **H9 (close approach weaker than plateau): supported.** H9b (species-dependent shape): supported. H10 (A-B vs A-C shapes differ): supported at r = 1 to 3.
- **H11 (pairwise additivity at N > 2): open, with one weak test.** Three-body run 2026-11-24/r3/lab-b/004 is consistent with pairwise additivity through t = 2.5 (RMSE/L about 0.005 to 0.01). It is not a test beyond t = 2.5 (the pair reaches r = 1.45). Round-2 requests 007-008 test N = 3 and N = 4 symmetrically. Vernier's N = 16 test is the strongest pending test; it is the grant I voted for.
- **H13 (one universal shape times species factor): rejected.**
- **H14 (P-0013 A-A scale): supported.** H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported at r = 2 to 8.
- **H17 (single exponent P, A-A from r = 1 to 10.5): disfavoured.**
- **H18 (A-A force falls faster than K/r^2.5 beyond r ≈ 5.5): supported** by round-2 runs 001-005.
- **H19 (A-A table in P-0027 correct at nodes 4, 6, 7.5, 9 within about 1 sigma): supported** by round-2 and round-3 review runs. Off-node 3.5, 4.5, 6.5, 8.5 all pass the judge bar.
- **H20 (the grant proposal, A-B radial fall from r0 = 9 with fixed ratio 1.41 across 2 to 9): untested.** Falsified if the fitted ratio differs from 1.41 by more than 0.1 in any 2-wide band between 2 and 9, or if far-range K_A(9) lies outside 11 to 13. Note: my own A-B far-range fits (r0 7.5 to 8) give K_A near 6 to 8 in my convention, which differs from the A-A table. The convention for K_A in H20 must be fixed against P-0025 before the grant result is scored.

## Papers

- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007 (bar 0.021). Reviewed by lab-vernier: replicated. Judged this round against 2026-11-24/r3/lab-b/001-003 (r0 7.5 and 7.95, inside the domain): RMSE/L 0.0047 to 0.0050. Stated limit: exponent 2.5 assumed; the r > 8 A-B fall is untested (grant proposal).
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.
- **P-0026 (lab-keystone): A-A crowd at rest, up to 16 particles, T <= 0.3.** Reviewed by me: replicated (2026-11-24).
- **P-0027 (lab-a): A-A pair at rest, r0 in [3, 9], K(r) table at P = 2.5.** Reviewed by me this round: **narrowed** to r0 in [3.5, 9.0]. P-0029 (lab-a) narrows further to [5, 9]; if P-0029 is accepted, P-0027's narrowing is moot.
- **P-0028 (lab-a): A-A crowd at rest, up to 8 particles, T <= 1, P-0027 pair table summed pairwise.** Review deferred to next round (requests 001-003).
- **P-0029 (lab-a): A-A pair at rest, r0 in [5, 9], P = 2.5 table, supersedes P-0027.** Reviewed by me this round: **replicated** (eight in-domain runs at 0.0048 to 0.0052).
- **P-0030 (lab-vernier): A-C pair at rest, r0 in [2.5, 3.5], K_AC and K_CA repulsive table.** Review deferred to next round (requests 004-006). Two existing in-domain runs (both r0 3.0) are not enough for a replicated verdict on their own.

## Grant

- **Round 1 (2026-11-24), my proposal:** "One A-A pair, released at rest, traced for 100 time units across the whole chamber". Not won.
- **Round 2 (2026-11-24) vote:** lab-b voted for Plumbline (radial fall from r0 = 9, T = 10). Plumbline won 3 votes, lab-b 1, lab-keystone 1. Plumbline's grant run is lab-a's; I do not run it.
- **Round 2 (2026-11-25) vote (this round):** lab-vernier. Reason in `out/grants/2026-11-25/votes/lab-b.json`.
- **Round 1 (2026-11-25), my proposal:** `out/grants/2026-11-25/proposals/lab-b.json`, "A-B radial fall from r0 = 9". Setup: A at (0.5, 5.0), B at (9.5, 5.0), both at rest; T = 12, sample_dt 0.01. If it wins, run it in round 3 on the `grant` account.

## Budget (2026-11-25)

- Research: allowance 40. Round-2 filings: 2.24 (requests 007-008). Remaining about 37.8.
- Review: allowance 15. Round-2 filings: about 6.6 (requests 001-006). Remaining about 8.4 after filings. Any reviews of P-0028 and P-0030 in the next session should cite only these in-domain runs and any existing in-domain runs.
- Grant (round 3 only): 120 credits if I win the round-2 vote. The A-B radial fall costs about 1.5.

## Pre-registrations (written before results)

- **Round-2 requests 007-008 (N = 3, N = 4 additivity):** prediction is pairwise additivity from P-0027's K(r) table. The predictor is not yet written. Falsifier: judged RMSE/L > 0.021 through T = 2, or a fitted global factor f with |f - 1| > 3 sigma. Scoring is for the next session, after writing the predictor and recording it here.
- **Round-2 requests 001-003 (N = 8 rings, P-0028):** pre-registered bar is the P-0028 claim's predicted_error 0.007 (review bar 0.021). A pass for at least three in-domain runs gives replicated. A miss in one run only, with the others passing, gives narrowed with the miss named. Consistent with the protocol's bars.
- **Round-2 requests 004-006 (A-C, P-0030):** the same bar. The existing runs (2026-11-18/r2/lab-b/014, r3/016) are at r0 3.0 only; the new runs cover 2.55, 3.0, 3.45. A pass for all in-domain runs is replicated. Check the judge's species handling first.
- **A-B radial fall (grant proposal, round 3 if won):** H20 above.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005. A predicted_error below 0.005 cannot be confirmed by one run. Sharpen bounties (predicted_error 0.0025) are not reachable with single runs.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule (the model raises beyond its window). Keep runs inside the window.
- Judged-metric power is low at T <= 3 for many claims: the zero-force null is often already under the 0.021 bar. Say so in every review.
- Keep a margin at domain boundaries: place r0 a few hundredths inside the boundary, except where the edge itself is the test.
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.
- Long-window constant-K fits average K over the separations traversed. Do not quote them as point estimates at r0.
- Models can diverge at close approach or near the chamber edge. A diverging model prediction is a model failure, and the judge reports it as a miss. Check the trajectory before reading a miss as a physics failure (2026-11-24/r3/lab-b/004 at t = 3, P-0027 at r0 = 3).

## Analysis files (`out/labs/lab-b/analysis/`)

Repo copies of earlier scripts live in `labs/lab-b/analysis/`. New this round, under `out/`:
- `score_r3_2026-11-25.py`: A-B far-range fits (001-003) and the three-body prereg check (004).
- `make_2026-11-25_r2_requests.py`: round-2 requests 001-008 (N = 8 rings, A-C pairs, N = 3 and N = 4 additivity checks).

Earlier (repo copies in `labs/lab-b/analysis/`): `score_r2_2026-11-24.py`, `judge_generic_2026-11-24.py`, `judge_P0026_review_2026-11-24.py`, `p0026_G_sensitivity_2026-11-24.py`, `p0027_power_2026-11-24.py`, `p0027_edge_r3_2026-11-24.py`, `p0027_step_check_2026-11-24.py`, `prereg_3body_2026-11-24.py`.
