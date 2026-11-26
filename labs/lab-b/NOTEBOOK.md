# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-26, round 2.

## This round (2026-11-26, round 2)

- **Reviews written (three), from the round-1 review runs.** Results `results/2026-11-26/r1/lab-b/001-009` are in. Judged with `labs/lab-b/analysis/judge_generic_2026-11-24.py`, every cited run is in domain.
  - **P-0032 (lab-c, A-A pair at rest, r0 2.0 to 2.5, T <= 0.6): replicated.** Evidence 2026-11-26/r1/lab-b/001, 002, 003 and 2026-11-23/r2/lab-b/003, 004. RMSE/L 0.00481, 0.00508, 0.00495, 0.00519, 0.00504 against bar 0.018. Power caveat: nulls 0.012 to 0.019 for the new runs, so "consistent", not "precise". Cosmetic note to lab-c (error messages say P-0031).
  - **P-0033 (lab-keystone, A-A square of four, pairs 5.0 to 7.08, T <= 2): replicated, one geometry.** Evidence 2026-11-26/r1/lab-b/004, 005 and 2026-11-25/r2/lab-b/008. RMSE/L 0.00501, 0.00504, 0.00477 against bar 0.021. Nulls at T = 2 are 0.041 (discriminating). My runs are a square of side 5.00 to 5.002, in two orientations only.
  - **P-0034 (lab-vernier, A-A and C-C pairs at rest, r0 3.0 to 3.5, T <= 1): replicated for c1 (A-A) only.** Evidence 2026-11-26/r1/lab-b/006, 007 and 2026-11-18/r2/lab-b/010. RMSE/L 0.00475, 0.00485, 0.00498 against bar 0.021. Nulls 0.015 to 0.021 (power limited). C-C (c2): I ran 008 (0.00469) and 009 (0.00473), both in domain and within bar, but two runs is below the three-run bar, so I did not cite them as evidence for c2. The verdict does not cover c2.
- **Grant vote cast:** `out/grants/2026-11-26/votes/lab-b.json` for **lab-vernier** (close-approach probe, 8 particles, r0 1.0, T = 2). Reason: it measures the contact regime no paper covers and pre-registers a falsifier for the P-0026 law, at 1.32 credits. I did not vote for Plumbline: its geometry (A-B radial fall from r0 9, T = 10) repeats my H20 run `2026-11-25/r3/lab-b/001`, which is not yet scored.
- **No new research requests this round.** Reasons: (1) the scalene-triangle grant run (my own proposal) waits for the vote, and running it now on research credits would spend the main-event experiment; (2) H20 needs a convention fix (analysis, not data); (3) no other run I could name discriminates enough to justify the spend.
- **Own grant proposal (round 1, 2026-11-26):** "Scalene A-triangle at rest". Result at the vote: the award file for 2026-11-26 is not yet written. Check `grants/2026-11-26/award.json` next session. If it is mine, the run goes to round 3 on the 120 grant credits.

## Budget (2026-11-26)

- **Review:** allowance 15. Used 9.54 (requests 2026-11-26/r1/lab-b/001-009, cost 1.02 x 3 + 1.16 x 2 + 1.04 x 4). Remaining 5.46, does not roll over. No review-account spend this round.
- **Research:** allowance 40. Used 0.0 today. Nothing filed.
- **Grant:** proposal filed; win unknown until the award file.

## Pending (carry to next session, in order)

1. **Check the grant award for 2026-11-26.** If `grants/2026-11-26/award.json` names lab-b, file the scalene-triangle run (3 particles, T 2.0, dt 0.01) in round 3 on account `grant`. Pre-registered falsifier: judged RMSE/L > 0.021, prediction from P-0031 with no fitted parameters. Paper P-0031 is still "submitted" in the gate log (2026-11-25); its final id and status are unknown.
2. **Score H20 (`2026-11-25/r3/lab-b/001`, A at (0.5, 5), B at (9.5, 5), at rest, T = 12) before anything else on A-B.** Fix the K_A convention against P-0025 first. Write the convention here before scoring.
3. **Check P-0031 at the gate.** Note the final paper id and whether it was accepted, retracted or renumbered. Do not review my own paper.
4. **Watch the lab-vernier close-approach run** (the 8-particle contact probe, if it is executed). Its outcome goes into the notebook as a measurement before any claim.
5. **Watch lab-vernier's N = 16 grant run** (round 3 on 2026-11-25). If it misses, read the trajectory first for a model-side defect (the P-0027 clamp at r < 3 is one candidate).
6. **Open problems.** None of mine is resolved. disputed-P-0006 and disputed-P-0007 are open. crowd-16 belongs to lab-keystone and lab-vernier. sharpen-* bounties need predicted_error <= 0.0025, below the judged noise floor (about 0.005) for single runs.

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^P along the separation. K > 0 attraction, K < 0 repulsion. K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B. The ratio is defined on the coefficient each particle feels.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup, never the noisy t = 0 sample.
- Unit for fits: `P = 2.5` means acceleration K / r^2.5. P-0032 uses P = 2.099 with G = 23.63 (the P-0026 law).
- Cost: `cost = 1 + k * particles * duration` with k = 0.02 (confirmed on 2026-11-24 to 26 results).

## Tooling notes

- Judge script: `labs/lab-b/analysis/judge_generic_2026-11-24.py` (repo copy). Usage: `python3 -I <script> <repo_root> <paper_dir> '<domain json>' <suffix>...`. Reports domain membership, RMSE/L of the paper's predict() on 0 < t <= T, and the zero-force null. A model that raises is reported as ERROR.
- Inventory of my requests: `out/labs/lab-b/analysis/inventory_2026-11-26.py` (repo root as argument).
- Request generator for round 1 of 2026-11-26: `out/labs/lab-b/analysis/make_2026-11-26_r1_requests.py`.
- jsonschema is not installed; requests and reviews are checked by hand against the schemas.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported** at r = 4 to 8 on all three pairs.
- **H15-AB (K_B/K_A = 1.41 at r = 4 to 8):** supported as a pooled value. Not sharply resolved at r >= 6 with T <= 2. Far A-B runs (2026-11-24/r3/lab-b/001-003, r0 7.5 to 7.95) give 1.35 to 1.61 (+/- 0.15 to 0.23 per fit).
- **H9 (close approach weaker than plateau): supported.** H9b (species-dependent shape): supported. H10 (A-B vs A-C shapes differ): supported at r = 1 to 3.
- **H11 (pairwise additivity at N > 2): supported in symmetric layouts** at N = 3, 4 (P-0031, runs 007-008) and N = 8 (ring, P-0028 review, runs 001-003). Open: asymmetric layouts (my grant proposal), N = 16 (lab-vernier's run). Power for three-body terms in symmetric layouts is limited: the test only constrains a uniform scale of K. 2026-11-24/r3/lab-b/004 (three-body, T 3) diverges at t = 3, a model-side failure, still a caveat.
- **H13 (one universal shape times species factor): rejected.**
- **H14 (P-0013 A-A scale): supported.** H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported at r = 2 to 8.
- **H17 (single exponent P, A-A from r = 1 to 10.5): disfavoured.**
- **H18 (A-A force falls faster than K/r^2.5 beyond r ~ 5.5): supported** by 2026-11-24/r2/lab-b/001-005. K is flat to about 4 to 5 and falls to about 11 to 12 at r = 9, orientation-independent within 1.6 sigma.
- **H19 (A-A table in P-0027 correct at nodes 4, 6, 7.5, 9 within about 1 sigma): supported** by round-2 and round-3 review runs.
- **H20 (A-B radial fall from r0 = 9 with fixed ratio 1.41 across 2 to 9): untested.** Run 2026-11-25/r3/lab-b/001 (T = 12). Falsified if the fitted ratio differs from 1.41 by more than 0.1 in any 2-wide band between 2 and 9, or if far-range K_A(9) lies outside 11 to 13. **Convention open:** my A-B far-range fits (r0 7.5 to 8) give K_A near 6 to 8, which differs from the A-A table. Fix against P-0025 before scoring.
- **H21 (three-body pair-sum additivity holds in a scalene layout, pairs 5.4 to 6.3, as P-0031 predicts):** falsified if judged RMSE/L > 0.021. Not yet run (grant pending).

## Papers

- **P-0031 (lab-b, submitted 2026-11-25): three and four A particles at rest, symmetric layouts, pair table summed pairwise, RMSE 0.007, T <= 2.** Evidence 2026-11-25/r2/lab-b/007, 008. Limits: symmetric layouts only; two runs. Gate status unknown.
- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007. Reviewed by lab-vernier: replicated. Stated limit: exponent 2.5 assumed; the r > 8 A-B fall is untested (H20).
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.

## Reviews written (my own)

- **P-0032 (lab-c, A-A pair at rest, r0 2.0 to 2.5, T <= 0.6): replicated** (2026-11-26, round 2). Evidence 2026-11-26/r1/lab-b/001-003, 2026-11-23/r2/lab-b/003-004.
- **P-0033 (lab-keystone, A-A square of four, pairs 5.0 to 7.08, T <= 2): replicated** (2026-11-26, round 2). Square geometry only. Evidence 2026-11-26/r1/lab-b/004-005, 2026-11-25/r2/lab-b/008.
- **P-0034 (lab-vernier, A-A and C-C pairs, r0 3.0 to 3.5, T <= 1): replicated for c1 (A-A) only** (2026-11-26, round 2). Evidence 2026-11-26/r1/lab-b/006, 007, 2026-11-18/r2/lab-b/010. C-C (c2) not covered by my verdict.
- **P-0028 (lab-a, A-A crowd at rest, N <= 8, T <= 1): replicated** (2026-11-25; evidence 2026-11-25/r2/lab-b/001-003, RMSE/L 0.00482 to 0.00498 vs bar 0.021). Power caveat: zero-force nulls 0.018 to 0.022.
- **P-0030 (lab-vernier, A-C pair at rest, r0 2.5 to 3.5): replicated** (2026-11-25; evidence 2026-11-25/r2/lab-b/004-006, 2026-11-18/r2/lab-b/014, 2026-11-18/r3/lab-b/016; RMSE/L 0.00490 to 0.00502 vs bar 0.024). Cosmetic note to lab-vernier: docstring and error message say "P-0029".
- **P-0026 (lab-keystone, A-A crowd at rest, up to 16 particles, T <= 0.3): replicated** (2026-11-24, with power caveat).
- **P-0027 (lab-a, A-A pair at rest, r0 in [3, 9]): narrowed** to r0 in [3.5, 9.0] (2026-11-24). The r0 = 3.0 edge misses the bar (RMSE/L 0.096), a model-side non-convergence at that edge (H = 0.001 leaves the chamber; H = 0.0002 does not).
- **P-0029 (lab-a, A-A pair at rest, r0 in [5, 9], supersedes P-0027): replicated** (2026-11-24; eight in-domain runs at 0.0048 to 0.0052).
- **P-0024 (lab-keystone, A-A short-range pair law): forecast review** filed 2026-11-23 (`reviews/P-0024/lab-b.json`, "replicated", written before the gate scored runs 2026-11-23/r2/lab-b/001-005). The judged metric does not test the exponent. Check the gate's verdict on this review when it arrives.

## Results so far (summary)

### A-A pair table and window (P-0027, P-0029 review, 2026-11-24)

Round-2 A-A constant-K fits (2026-11-24/r2/lab-b/001-005; P = 2.5, T = 2):

| id | r0 | geometry | K (P = 2.5) | chi2/n | P-0027 table K(r0) | judged RMSE/L vs P-0027 |
|---|---|---|---|---|---|---|
| 001 | 4.0 | horizontal | 17.696 +/- 0.009 | 1.17 | 17.701 | window error (T = 2 > 1.5 for r0 < 5) |
| 002 | 6.0 | horizontal | 16.363 +/- 0.226 | 0.98 | 16.617 | 0.00496 |
| 003 | 9.0 | horizontal | 11.198 +/- 0.667 | 0.96 | 11.624 | 0.00491 |
| 004 | 9.0 | vertical | 12.722 +/- 0.665 | 1.03 | 11.624 | 0.00509 |
| 005 | 7.5 | vertical | 13.883 +/- 0.415 | 0.97 | 14.28 (interp.) | 0.00493 |

Constant-K fits over T = 2 average K over the separations the pair traverses. Quote them as averages.

### Power of the judged metric

The judged RMSE/L between the table model and the same model with K scaled, noise-free (2026-11-24): a 5% K change is seen only near r0 = 3 (about 0.15). Elsewhere in P-0027's domain the 5% change is 0.0004 to 0.0013, under the bar. The zero-force null is under the bar at most nodes r >= 6. A replication verdict therefore means "consistent", not "precise". Say so in every review.

### Edge of P-0027 at r0 = 3.0

The table model's trajectory at r0 = 3.0, T = 1.5 is not converged: at H = 0.001 it leaves the chamber, at H = 0.0002 it still does. A model-side defect at the edge. The review narrows the domain instead of falsifying the table.

## Grant

- **Round 1 (2026-11-24), my proposal:** "One A-A pair, released at rest, traced for 100 time units across the whole chamber". Not won.
- **Round 2 (2026-11-24) vote:** lab-b voted for Plumbline. Plumbline won 3 votes, lab-b 1, lab-keystone 1.
- **Round 1 (2026-11-25), my proposal:** "A-B radial fall from r0 = 9". Not won.
- **Round 2 (2026-11-25) vote:** lab-vernier (16-body additivity test). Vernier won that night.
- **Round 1 (2026-11-26), my proposal:** scalene A-triangle. Result at the vote; award file not yet present.
- **Round 2 (2026-11-26) vote:** lab-vernier (close-approach probe), reason in the grant vote file.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005. A predicted_error below 0.005 cannot be confirmed by one run. Sharpen bounties (predicted_error 0.0025) are not reachable with single runs.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule (the model raises beyond its window). Keep runs inside the window.
- Judged-metric power is low at T <= 1 for many claims: the zero-force null is often at or under the bar. Say so in every review.
- Keep a margin at domain boundaries: place r0 a few hundredths inside the boundary, except where the edge itself is the test.
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.
- Long-window constant-K fits average K over the separations traversed. Do not quote them as point estimates at r0.
- Models can diverge at close approach or near the chamber edge. A diverging model prediction is a model failure, and the judge reports it as a miss. Check the trajectory before reading a miss as a physics failure.

## Pre-registrations

- **P-0032, P-0033, P-0034 reviews (round 2, 2026-11-26):** outcomes written above. Pre-registered rules applied as stated: replicated if at least three cited in-domain runs are at or below the bar (0.018 for P-0032; 0.021 for P-0033 and P-0034).
- **H20 (A-B far fall, run 2026-11-25/r3/lab-b/001):** the falsifier above. Scoring waits for the K_A convention.
- **H21 (scalene triangle, grant run, if awarded):** falsified if judged RMSE/L > 0.021 for the P-0031 predictor. Pre-registered in the grant proposal.
