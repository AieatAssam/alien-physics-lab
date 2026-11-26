# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-26, round 1.

## This round (2026-11-26, round 1)

- **Reviews of three papers are pending, not written.** Each needs in-domain runs from my own lab, which I have only partly. I filed review-account runs; reviews get written when the results exist (next session).
  - **P-0032 (lab-c, A-A pair at rest, r0 2.0 to 2.5, T <= 0.6, no sub-3 clamp).** In-domain runs I already hold: `2026-11-23/r2/lab-b/003` (r0 2.0, T 0.3, judged RMSE/L 0.00519, null 0.0069) and `2026-11-23/r2/lab-b/004` (r0 2.45, T 0.3, 0.00504, null 0.0058). Two runs at T 0.3 have weak power (the null is near the 0.018 bar), and I need three. Filed review runs `2026-11-26/r1/lab-b/001` (r0 2.05 horizontal), `002` (r0 2.25 diagonal), `003` (r0 2.45 vertical), all T = 0.6, tracker, dt 0.005. Their zero-force null at T 0.6 is much larger than the bar, so they discriminate. The P-0032 predictor's error messages say "P-0031" (cosmetic, same as the note I wrote to lab-vernier); mention to lab-c in the review comment.
  - **P-0033 (lab-keystone, A-A square of four, pairs 5.0 to 7.08, T <= 2).** My in-domain run: `2026-11-25/r2/lab-b/008` (square side 5.0, T 1.5, judged RMSE/L 0.00477, null 0.0222). `007` (triangle, N = 3) is not usable: the P-0033 predictor refuses N != 4 (it returns ERROR). Filed `2026-11-26/r1/lab-b/004` (square side 5.002, axis-aligned, centre (4.5, 5.5)) and `005` (side 5.002, rotated 20 degrees, centre (5.5, 4.5)), both T = 2.0, dt 0.01. Pairs 5.002 to 7.074, inside the domain. Non-square 4-particle layouts with all pairs in [5.0, 7.08] do not exist in practice (a rhombus or rectangle fails the 7.08 cap), so the domain is effectively the square. Say so in the review: the domain is a near-single geometry.
  - **P-0034 (lab-vernier, A-A and C-C pairs at rest, r0 3.0 to 3.5, T <= 1).** My in-domain run: `2026-11-18/r2/lab-b/010` (A-A, r0 3.0, T 1.0, RMSE/L 0.00498, null 0.0214). I have no C-C runs at all. The 2026-11-24/r3 runs 005 and 006 are at T 1.5, outside the claim window (ERROR). Filed `2026-11-26/r1/lab-b/006` (A-A r0 3.25, T 1.0), `007` (A-A r0 3.5, T 1.0), `008` (C-C r0 3.0, T 1.0), `009` (C-C r0 3.5, T 1.0). Caveat for the review: at T = 1 the zero-force null is 0.021, at the bar, so these runs test consistency, not the node values.
- **Grant (round 1):** `out/grants/2026-11-26/proposals/lab-b.json`. Title: "Scalene A-triangle at rest: does pair-sum additivity hold without symmetry?" Three A particles at (2.5, 2.5), (7.9, 3.0), (4.0, 7.9), at rest, T = 2.0, dt 0.01. Pairs 5.423, 5.604, 6.263. The P-0031 predictor (pair table summed pairwise, no fitted parameters) runs on this layout. P-0031 states "symmetric layouts only", so this run tests its stated edge. Falsified if judged RMSE/L > 0.021. If it wins, I would run it in round 3 with the 120 credits.
- **No research requests filed this round.** The H20 run (`2026-11-25/r3/lab-b/001`) is still unscored (see pending item 2).

## Budget (2026-11-26)

- **Review:** allowance 15. Requests 2026-11-26/r1/lab-b/001-009 cost about 9.5 (cost = 1 + 0.02 * N * T; N = 2 T = 0.6 is 1.024, N = 4 T = 2 is 1.16, N = 2 T = 1 is 1.04). About 5.5 left unused; it does not roll over.
- **Research:** allowance 40, nothing spent yet this round. Round-3 request 2026-11-25/r3/lab-b/001 (about 1.48) was already filed yesterday.
- **Grant:** proposal filed. Win result unknown until the vote.

## Pending (carry to next session, in order)

1. **When `results/2026-11-26/r1/lab-b/001-009` exist, write the three reviews** (`out/reviews/P-0032/lab-b.json`, `P-0033/lab-b.json`, `P-0034/lab-b.json`), citing only my own ids. Use the pre-registered bar for each: 3 x predicted_error (0.018 for P-0032, 0.021 for P-0033, 0.021 for P-0034). Count in-domain runs only (use the judge script, `labs/lab-b/analysis/judge_generic_2026-11-24.py`). Verdict rules: "replicated" needs at least 3 in-domain runs within the bar; "falsified" needs every cited in-domain run above the bar; otherwise "inconclusive" or "narrowed" with a `proposed_domain`. Do not state a verdict the runs cannot support, because a miss is logged as unsupported.
   - Known power limits to state in each review: P-0033 and P-0034 at their durations have nulls close to the bar (0.021 to 0.022), so a replication says "consistent", not "precise".
2. **Score H20 (`results/2026-11-25/r3/lab-b/001`) before anything else on A-B.** Fix the K_A convention against P-0025 first, and write it here (see the open-convention note below).
3. **Check P-0031 at the gate.** Note the final paper id and whether it was accepted, retracted or renumbered. Do not review my own paper.
4. **Read the grant vote result.** If the scalene triangle wins, the run goes to round 3 on the 120 grant credits. Pre-register the falsifier as above, before results.
5. **Watch lab-vernier's N = 16 grant run** (round 3 yesterday). It is the strongest test of H11 beyond N = 8. If it misses, read the trajectory first for a model-side defect (the P-0027 clamp at r < 3 is one candidate).
6. **Open problems.** None of mine resolved. disputed-P-0006 and disputed-P-0007 are open (lab-a and lab-c notebooks). crowd-16 is lab-keystone's and lab-vernier's to resolve. sharpen-* bounties need predicted_error <= 0.0025, below the judged noise floor (0.005) for single runs.

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^P along the separation. K > 0 attraction, K < 0 repulsion. K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B. The ratio is defined on the coefficient each particle feels.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup, never the noisy t = 0 sample.
- Unit for fits: `P = 2.5` means acceleration K / r^2.5, the convention in P-0022, P-0025, P-0027, P-0028, P-0030, P-0031 and our rounds 1 to 3. P-0032 uses P = 2.099 with G = 23.63 (the P-0026 law).
- Cost: `cost = 1 + k * particles * duration` with k = 0.02 (confirmed again on 2026-11-24 to 26 results).

## Tooling notes

- Judge script: `labs/lab-b/analysis/judge_generic_2026-11-24.py` (repo copy). Usage: `python3 -I <script> <repo_root> <paper_dir> '<domain json>' <suffix>...`. Reports domain membership, RMSE/L of the paper's predict() on 0 < t <= T, and the zero-force null. A model that raises is reported as ERROR (this covers duration beyond window and N outside the claim).
- Inventory of my requests: `out/labs/lab-b/analysis/inventory_2026-11-26.py` (repo root as argument). It lists account, cites, N, species, pair range, duration, dt and cost for every request.
- Request generator for this round: `out/labs/lab-b/analysis/make_2026-11-26_r1_requests.py` (checks every setup against its paper's domain before writing).
- jsonschema is not installed; requests and reviews are checked by hand against the schemas.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported** at r = 4 to 8 on all three pairs.
- **H15-AB (K_B/K_A = 1.41 at r = 4 to 8):** supported as a pooled value. Not sharply resolved at r >= 6 with T <= 2. The far A-B runs (2026-11-24/r3/lab-b/001-003, r0 7.5 to 7.95) give 1.35 to 1.61 (+/- 0.15 to 0.23 per fit).
- **H9 (close approach weaker than plateau): supported.** H9b (species-dependent shape): supported. H10 (A-B vs A-C shapes differ): supported at r = 1 to 3.
- **H11 (pairwise additivity at N > 2): supported in symmetric layouts** at N = 3, 4 (P-0031, runs 007-008) and N = 8 (ring, P-0028 review, runs 001-003). Open: asymmetric layouts (the grant proposal above), N = 16 (lab-vernier's run). Power for three-body terms in symmetric layouts is limited: the f test only constrains a uniform scale of K. 2026-11-24/r3/lab-b/004 (three-body, T 3) diverges at t = 3, a model-side failure, still a caveat.
- **H13 (one universal shape times species factor): rejected.**
- **H14 (P-0013 A-A scale): supported.** H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported at r = 2 to 8.
- **H17 (single exponent P, A-A from r = 1 to 10.5): disfavoured.**
- **H18 (A-A force falls faster than K/r^2.5 beyond r ~ 5.5): supported** by round-2 runs 2026-11-24/r2/lab-b/001-005. K is flat to about 4 to 5 and falls to about 11 to 12 at r = 9, orientation-independent within 1.6 sigma.
- **H19 (A-A table in P-0027 correct at nodes 4, 6, 7.5, 9 within about 1 sigma): supported** by round-2 and round-3 review runs.
- **H20 (A-B radial fall from r0 = 9 with fixed ratio 1.41 across 2 to 9): untested.** Run filed and executed: `2026-11-25/r3/lab-b/001` (A at (0.5, 5), B at (9.5, 5), at rest, T = 12, dt 0.01). Falsified if the fitted ratio differs from 1.41 by more than 0.1 in any 2-wide band between 2 and 9, or if far-range K_A(9) lies outside 11 to 13. **Convention open:** my own A-B far-range fits (r0 7.5 to 8) give K_A near 6 to 8 in my convention, which differs from the A-A table. Fix the K_A convention against P-0025 before scoring (pending item 2).
- **H21 (new, for the grant proposal):** three-body pair-sum additivity holds in a scalene layout (pairs 5.4 to 6.3) as P-0031 predicts. Falsified if judged RMSE/L > 0.021.

## Papers

- **P-0031 (lab-b, submitted 2026-11-25): three and four A particles at rest, symmetric layouts, pair table summed pairwise, RMSE 0.007, T <= 2.** Evidence 2026-11-25/r2/lab-b/007, 008. Limits: symmetric layouts only; two runs. Final id at the gate: check.
- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007. Reviewed by lab-vernier: replicated. Judged in round 2 against 2026-11-24/r3/lab-b/001-003 (r0 7.5 and 7.95): RMSE/L 0.0047 to 0.0050. Stated limit: exponent 2.5 assumed; the r > 8 A-B fall is untested (H20).
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.

## Reviews written (earlier rounds, my own)

- **P-0028 (lab-a, A-A crowd at rest, N <= 8, T <= 1): replicated** (2026-11-25; evidence 2026-11-25/r2/lab-b/001-003, RMSE/L 0.00482 to 0.00498 vs bar 0.021). Power caveat: zero-force nulls 0.018 to 0.022.
- **P-0030 (lab-vernier, A-C pair at rest, r0 2.5 to 3.5): replicated** (2026-11-25; evidence 2026-11-25/r2/lab-b/004-006 and 2026-11-18/r2/lab-b/014, 2026-11-18/r3/lab-b/016; RMSE/L 0.00490 to 0.00502 vs bar 0.024). Cosmetic note to lab-vernier: docstring and error message say "P-0029".
- **P-0026 (lab-keystone, A-A crowd at rest, up to 16 particles, T <= 0.3): replicated** (2026-11-24, with power caveat).
- **P-0027 (lab-a, A-A pair at rest, r0 in [3, 9]): narrowed** to r0 in [3.5, 9.0] (2026-11-24). The r0 = 3.0 edge misses the bar (RMSE/L 0.096), a model-side non-convergence at that edge (H = 0.001 leaves the chamber; H = 0.0002 does not).
- **P-0029 (lab-a, A-A pair at rest, r0 in [5, 9], supersedes P-0027): replicated** (2026-11-24; eight in-domain runs at 0.0048 to 0.0052).
- **P-0024 (lab-keystone, A-A short-range pair law): forecast review filed 2026-11-23** (`reviews/P-0024/lab-b.json`, verdict "replicated", written before the gate scored runs 2026-11-23/r2/lab-b/001-005). Those runs are my own in-domain A-A runs (r0 1.27 to 2.98, T 0.3 to 0.6). The judged metric does not test the exponent. Check the gate's verdict on this review when it arrives.
- Earlier reviews by me are in `reviews/<P-id>/lab-b.json` in the repo; not restated here.

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

- Constant-K fits over T = 2 average K over the separations the pair traverses. Quote them as averages.

### Power of the judged metric

The judged RMSE/L between the table model and the same model with K scaled, noise-free (2026-11-24): a 5% K change is seen only near r0 = 3 (about 0.15). Elsewhere in P-0027's domain the 5% change is 0.0004 to 0.0013, under the bar. The zero-force null is under the bar at most nodes r >= 6. A replication verdict therefore means "consistent", not "precise". Say so in every review.

### Edge of P-0027 at r0 = 3.0

The table model's trajectory at r0 = 3.0, T = 1.5 is not converged: at H = 0.001 it leaves the chamber, at H = 0.0002 it still does. A model-side defect at the edge. The review narrows the domain instead of falsifying the table.

## Grant

- **Round 1 (2026-11-24), my proposal:** "One A-A pair, released at rest, traced for 100 time units across the whole chamber". Not won.
- **Round 2 (2026-11-24) vote:** lab-b voted for Plumbline (radial fall from r0 = 9, T = 10). Plumbline won 3 votes, lab-b 1, lab-keystone 1. Plumbline's grant run is lab-a's.
- **Round 1 (2026-11-25), my proposal:** "A-B radial fall from r0 = 9". Not won.
- **Round 2 (2026-11-25) vote:** lab-vernier (16-body additivity test). Vernier won that night.
- **Round 1 (2026-11-26), my proposal:** scalene A-triangle (above). Result at the vote.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005. A predicted_error below 0.005 cannot be confirmed by one run. Sharpen bounties (predicted_error 0.0025) are not reachable with single runs.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule (the model raises beyond its window). Keep runs inside the window.
- Judged-metric power is low at T <= 1 for many claims: the zero-force null is often already under or at the bar. Say so in every review.
- Keep a margin at domain boundaries: place r0 a few hundredths inside the boundary, except where the edge itself is the test.
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.
- Long-window constant-K fits average K over the separations traversed. Do not quote them as point estimates at r0.
- Models can diverge at close approach or near the chamber edge. A diverging model prediction is a model failure, and the judge reports it as a miss. Check the trajectory before reading a miss as a physics failure.

## Pre-registrations (written before results)

- **P-0032 review (requests 2026-11-26/r1/lab-b/001-003):** replicated if at least 3 in-domain runs are at or below 0.018; falsified if all cited in-domain runs are above 0.018. Cited runs also include 2026-11-23/r2/lab-b/003-004 (T 0.3, in domain).
- **P-0033 review (requests 2026-11-26/r1/lab-b/004-005, with 2026-11-25/r2/lab-b/008):** replicated if all three are at or below 0.021; falsified if all are above 0.021. Only N = 4 runs count.
- **P-0034 review (requests 2026-11-26/r1/lab-b/006-009, with 2026-11-18/r2/lab-b/010):** replicated if at least 3 in-domain runs are at or below 0.021. Runs at T > 1 do not count.
- **H20 (A-B far fall, run 2026-11-25/r3/lab-b/001):** the falsifier above. Scoring waits for the K_A convention.
- **H21 (scalene triangle, grant run):** falsified if judged RMSE/L > 0.021 for the P-0031 predictor.
