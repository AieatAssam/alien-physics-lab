# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-25, round 3.

## This round (2026-11-25, round 3)

- **Reviews written** (both from my own request ids):
  - `out/reviews/P-0028/lab-b.json`: **replicated** (lab-a, A-A crowd, N <= 8, T <= 1). Evidence 2026-11-25/r2/lab-b/001, 002, 003. Judged RMSE/L 0.00498, 0.00482, 0.00497 against bar 0.021. Power caveat: the zero-force nulls are 0.018 to 0.022, at or under the bar, so this says "consistent at N = 8", not "K(r) resolved". Measured pair separations dipped to about 2.6 to 2.9 near t = 0.9 to 1.0, i.e. into the clamped r < 3 region; the judged error stays at the floor there, so I record that but do not count it as a failure.
  - `out/reviews/P-0030/lab-b.json`: **replicated** (lab-vernier, A-C pair, r0 2.5 to 3.5). Evidence 2026-11-25/r2/lab-b/004, 005, 006 (new, out of sample) plus 2026-11-18/r2/lab-b/014 and 2026-11-18/r3/lab-b/016. Judged RMSE/L 0.00490 to 0.00502 against bar 0.024. Power caveat: at T = 1 the nulls are 0.012 to 0.022; run 016 (T = 2, null 0.052) carries most of the discrimination. Cosmetic note to lab-vernier: model.py docstring and error message say "P-0029".
- **Additivity at N = 3 and N = 4 (H11): scored, supported in symmetric layouts.** Pre-registration in `out/labs/lab-b/analysis/PREREG_additivity_N34_2026-11-25.md`, written before scoring; script `out/labs/lab-b/analysis/additivity_N34_2026-11-25.py`.
  - 007 (equilateral triangle, side 6.0, T = 2): RMSE/L 0.00492, null 0.0226.
  - 008 (square, side 5.0, T = 1.5): RMSE/L 0.00477, null 0.0222.
  - Both are under the bar of 0.021 and above the no-force null. A joint global factor on K gives f = 0.996 +/- 0.004 (|f - 1|/sigma = 0.98). chi2/dof = 0.94.
  - Limits: symmetric layouts only. A three-body term that does not look like a uniform scale of K is not constrained by the f test. The 2026-11-24/r3/lab-b/004 divergence at t = 3 is a model-side failure and still stands as a caveat.
- **New paper: P-0031 (lab-b), "Three and four A particles at rest, symmetric layouts: the P-0027 pair table summed pairwise predicts positions to 0.007 (T <= 2)".** Files `out/papers/P-0031/{paper.md,claim.json,model.py}`. Domain: species A, r in [5.0, 7.1], max_particles 4. predicted_error 0.007. Evidence 2026-11-25/r2/lab-b/007, 008. Cites P-0027, P-0028. model.py imports only math; it reproduces the scores above and refuses N = 2 and N >= 5. The paper number may be renumbered by the gate; refer to it by title until the final id is known.
- **Research run filed for H20 (A-B fall beyond r = 8):** `out/requests/2026-11-25/r3/lab-b/001.json`, account research, 2 particles (A at (0.5, 5), B at (9.5, 5), both at rest), T = 12, sample_dt 0.01, tracker. Cost about 1.48. This is the setup from my lost grant proposal, now run on research credits. Scoring waits for the convention fix below.
- **Grant:** Vernier won tonight (16-body additivity test). My A-B proposal did not win, so there is no grant run this round. My round-2 vote for Vernier is recorded in `grants/2026-11-25/votes/lab-b.json`.
- **Process:** `out/` held only round-3 files at the start of this session. Earlier-round reviews (P-0027 narrowed, P-0029 replicated, P-0026 replicated) are summarised below from the previous notebook. Keep all new output under `out/`.

## Budget (2026-11-25)

- **Research:** allowance 40. Round-2 requests 007-008 used 2.24. Round-3 request 001 costs about 1.48. Remaining about 36.3 after filing.
- **Review:** allowance 15. Round-2 requests 001-006 used 6.6 (results show budget_remaining 8.40 after 006). No review requests filed this round. Remaining 8.4 (unused, does not roll over).
- **Grant:** none this round (lost).

## Pending (carry to next session, in order)

1. **Read `results/2026-11-25/r3/lab-b/001`** when it exists. Score against H20 (below). Do not score until the convention below is fixed and written here.
2. **Fix the K_A convention for H20 against P-0025** before reading 001. Write the chosen convention into this notebook first, with the P-0025 page or equation it comes from.
3. **Check P-0031 at the gate.** Note the final paper id and whether it was accepted, retracted or renumbered. Read any review of it by another lab. Do not review my own paper.
4. **Watch lab-vernier's N = 16 run** (grant, round 3). It is the strongest pending test of H11 beyond N = 8. If it misses the bar, read the trajectory first for a model-side defect (the P-0027 table clamp at r < 3 is one candidate), then record the honest verdict.
5. **Open problems.** None of mine is resolved yet. disputed-P-0006 and disputed-P-0007 are open (see lab-a and lab-c notebooks). crowd-16 is lab-keystone's and lab-vernier's to resolve. sharpen-* bounties need predicted_error <= 0.0025, which is below the judged noise floor (0.005) for single runs.

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^P along the separation. **K > 0 attraction, K < 0 repulsion.** K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B. The ratio is defined on the coefficient each particle feels.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup, never the noisy t = 0 sample.
- Unit for fits: `P = 2.5` means acceleration K / r^2.5, the convention in P-0022, P-0025, P-0027, P-0028, P-0030, P-0031 and our rounds 1 to 3.
- Cost: `cost = 1 + k * particles * duration` with **k = 0.02** (round-2 results: 8 particles, T = 1, cost 1.16; 3 particles, T = 2, cost 1.12; 2 particles, T = 1, cost 1.04).

## Tooling notes

- Judge script: `labs/lab-b/analysis/judge_generic_2026-11-24.py` (repo copy). Usage: `python3 -I <script> <repo_root> <paper_dir> '<domain json>' <suffix>...`. It reports domain membership, RMSE/L of the paper's predict() on 0 < t <= T, and the zero-force null. A model that raises is reported as ERROR. Duration is not checked by the judge; check it yourself.
- `/tmp/lab-b-pylib` (numpy and scipy) is not present in this session. P-0028, P-0030 and P-0031 import only math and run without it. P-0027 and P-0025 need numpy, so reinstall before judging those.
- Scoring for P-0031 and H11: `out/labs/lab-b/analysis/additivity_N34_2026-11-25.py` (pure python, about 10 s).
- jsonschema is not installed; requests and reviews were checked by hand against the schemas (field names, id patterns, evidence type).

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported** at r = 4 to 8 on all three pairs.
- **H15-AB (K_B/K_A = 1.41 at r = 4 to 8):** supported as a pooled value. Not sharply resolved at r >= 6 with T <= 2. The far A-B runs (2026-11-24/r3/lab-b/001-003, r0 7.5 to 7.95) are consistent with the ratio at 1.35 to 1.61 (+/- 0.15 to 0.23 per fit).
- **H9 (close approach weaker than plateau): supported.** H9b (species-dependent shape): supported. H10 (A-B vs A-C shapes differ): supported at r = 1 to 3.
- **H11 (pairwise additivity at N > 2): supported in symmetric layouts at N = 3, 4 (P-0031, runs 007-008) and N = 8 (ring, P-0028 evidence reviewed by me, runs 001-003).** Open: asymmetric layouts; N = 16 (Vernier grant run). The 2026-11-24/r3/lab-b/004 three-body run is consistent through t = 2.5 (RMSE/L 0.005 to 0.01); it is not a test beyond t = 2.5, where the pair reaches r = 1.45. Power for three-body terms in symmetric layouts is limited: the f test only constrains a uniform scale of K.
- **H13 (one universal shape times species factor): rejected.**
- **H14 (P-0013 A-A scale): supported.** H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported at r = 2 to 8.
- **H17 (single exponent P, A-A from r = 1 to 10.5): disfavoured.**
- **H18 (A-A force falls faster than K/r^2.5 beyond r ~ 5.5): supported** by round-2 runs 001-005 (earlier notebook).
- **H19 (A-A table in P-0027 correct at nodes 4, 6, 7.5, 9 within about 1 sigma): supported** by round-2 and round-3 review runs.
- **H20 (A-B radial fall from r0 = 9 with fixed ratio 1.41 across 2 to 9): untested, run filed** (2026-11-25/r3/lab-b/001). Falsified if the fitted ratio differs from 1.41 by more than 0.1 in any 2-wide band between 2 and 9, or if far-range K_A(9) lies outside 11 to 13. **Convention open:** my own A-B far-range fits (r0 7.5 to 8) give K_A near 6 to 8 in my convention, which differs from the A-A table. The K_A convention in H20 must be fixed against P-0025 before 001 is scored (pending item 2).

## Papers

- **P-0031 (lab-b, submitted 2026-11-25): three and four A particles at rest, symmetric layouts, pair table summed pairwise, RMSE 0.007, T <= 2.** Evidence 2026-11-25/r2/lab-b/007, 008. Limits: symmetric layouts only; two runs.
- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007. Reviewed by lab-vernier: replicated. Judged in round 2 against 2026-11-24/r3/lab-b/001-003 (r0 7.5 and 7.95): RMSE/L 0.0047 to 0.0050. Stated limit: exponent 2.5 assumed; the r > 8 A-B fall is untested (H20, run filed).
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.
- **P-0026 (lab-keystone): A-A crowd at rest, up to 16 particles, T <= 0.3.** Reviewed by me 2026-11-24: replicated, with a power caveat (the zero-force null passes the bar on 3 of 4 runs).
- **P-0027 (lab-a): A-A pair at rest, r0 in [3, 9], K(r) table at P = 2.5.** Reviewed by me 2026-11-24: **narrowed** to r0 in [3.5, 9.0]. The r0 = 3.0 edge misses the bar (RMSE/L 0.096), a model-side non-convergence of the table at that edge (H = 0.001 leaves the chamber, H = 0.0002 does not).
- **P-0028 (lab-a): A-A crowd at rest, up to 8 particles, T <= 1.** Reviewed by me 2026-11-25: **replicated** (see above).
- **P-0029 (lab-a): A-A pair at rest, r0 in [5, 9], P = 2.5 table, supersedes P-0027.** Reviewed by me 2026-11-24: replicated (eight in-domain runs at 0.0048 to 0.0052).
- **P-0030 (lab-vernier): A-C pair at rest, r0 in [2.5, 3.5], K_AC and K_CA repulsive table.** Reviewed by me 2026-11-25: **replicated** (see above).

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

- H18 supported: K(r) is flat to about 4 to 5 and falls to about 11 to 12 at r = 9, orientation-independent within 1.6 sigma.
- Constant-K fits over T = 2 average K over the separations the pair traverses. Quote them as averages.

### Power of the judged metric

The judged RMSE/L between the table model and the same model with K scaled, noise-free (2026-11-24): a 5% K change is seen only near r0 = 3 (about 0.15). Elsewhere in P-0027's domain the 5% change is 0.0004 to 0.0013, under the bar. The zero-force null is under the bar at most nodes r >= 6. A replication verdict therefore means "consistent", not "precise". Say so in every review.

### Edge of P-0027 at r0 = 3.0

The table model's trajectory at r0 = 3.0, T = 1.5 is not converged: at H = 0.001 it leaves the chamber, at H = 0.0002 it still does. This is a model-side defect at the edge. The review narrows the domain instead of falsifying the table.

## Grant

- **Round 1 (2026-11-24), my proposal:** "One A-A pair, released at rest, traced for 100 time units across the whole chamber". Not won.
- **Round 2 (2026-11-24) vote:** lab-b voted for Plumbline (radial fall from r0 = 9, T = 10). Plumbline won 3 votes, lab-b 1, lab-keystone 1. Plumbline's grant run is lab-a's; I do not run it.
- **Round 1 (2026-11-25), my proposal:** "A-B radial fall from r0 = 9" (`out/grants/2026-11-25/proposals/lab-b.json`). Not won.
- **Round 2 (2026-11-25) vote:** lab-vernier (16-body additivity test). Vernier won tonight. Reason in `grants/2026-11-25/votes/lab-b.json`.
- The H20 setup (A at (0.5, 5), B at (9.5, 5), at rest, T = 12, dt 0.01) is now run on research credits as 2026-11-25/r3/lab-b/001.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005. A predicted_error below 0.005 cannot be confirmed by one run. Sharpen bounties (predicted_error 0.0025) are not reachable with single runs.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule (the model raises beyond its window). Keep runs inside the window.
- Judged-metric power is low at T <= 1 for many claims: the zero-force null is often already under the 0.021 bar. Say so in every review.
- Keep a margin at domain boundaries: place r0 a few hundredths inside the boundary, except where the edge itself is the test.
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.
- Long-window constant-K fits average K over the separations traversed. Do not quote them as point estimates at r0.
- Models can diverge at close approach or near the chamber edge. A diverging model prediction is a model failure, and the judge reports it as a miss. Check the trajectory before reading a miss as a physics failure.

## Pre-registrations (written before results)

- **H20 (A-B far fall, run 2026-11-25/r3/lab-b/001):** the falsifier above (ratio 1.41 within 0.1 in any 2-wide band over 2 to 9; far-range K_A(9) in 11 to 13). Scoring waits for the K_A convention to be fixed against P-0025 and written here.
- **Additivity N = 3 and N = 4 (007-008): done.** Predictor and falsifiers are in `PREREG_additivity_N34_2026-11-25.md`. Result: neither falsifier fires (RMSE/L 0.0049 and 0.0048 against 0.021; |f - 1|/sigma = 0.98).
