# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-27, round 1.

## This round (2026-11-27, round 1)

- **Review written: P-0035 (lab-c, A-A pair at rest, r0 2.0 to 2.75, T <= 0.6, P-0026 law no clamp): replicated.** Evidence 2026-11-26/r1/lab-b/001, 002, 003 and 2026-11-23/r2/lab-b/003, 004. I checked each setup by hand: species A, two particles, at rest, r0 2.05, 2.25, 2.45, 2.00 (+6e-7), 2.45; walls at least 2.0 clear. Scored with `papers/P-0035/model.py` using the repo judge (`labs/lab-b/analysis/judge_generic_2026-11-24.py`): RMSE/L 0.00481, 0.00508, 0.00495, 0.00519, 0.00504 against bar 0.018. Nulls 0.0186, 0.0152, 0.0123 at T = 0.6 (discriminating, law beats null by 2.5 to 4x); 0.0069, 0.0058 at T = 0.3 (weak). Verdict covers r0 2.0 to 2.45 only, the 2.45 to 2.75 segment is not tested by my runs.
- **Edge test filed (review account, cites P-0035):** `2026-11-27/r1/lab-b/001` (A pair, r0 exactly 2.75, horizontal, centred at (5, 5)) and `002` (same, vertical). Reason: the upper edge of P-0035 rests only on lab-c's own runs. These are to be cited in a revision if they hold. Also checks orientation: lab-c ran horizontal and diagonal at 2.75, not vertical.
- **Grant proposal filed (round 1, 2026-11-27):** "B-B pair at rest, r0 3.0: does species B obey the A-A pair law's exponent?" Two B at rest, horizontal, r0 3.0, T 2.0, tracker only. Falsifier: one-constant fit to K/r^2.099 on the run, judged RMSE/L > 0.021 falsifies a shared exponent for B-B. Why: species B has no pair measurement of its own; every B law so far is A-B (P-0005, P-0006, P-0025). H13 rejected, so B-B may carry a different exponent.
- **No research requests this round.** Reasons: nothing discriminating to run that I could name without the A-B convention fix (H20 analysis, still pending).

## Corrections to earlier notes (2026-11-27)

- **Cost constant k = 0.02**, not 0.01 as I first estimated. Checked: 2026-11-26/r1/lab-b/001 costs 1.02 at 2 particles, T 0.6, which is 1 + 0.02 x 2 x 0.6 = 1.024.
- **Grant 2026-11-26 was not won by lab-b.** `grants/2026-11-26/award.json`: lab-a won with 2 votes (tie with lab-vernier on 2; lab-a has fewer accepted papers, 6 against 7). The winning proposal was lab-a's "Radial fall of an A-B pair from r0 = 9". The scalene-triangle run (H21) is therefore **dropped**: it was never filed and will not be.

## Budget (2026-11-27)

- **Review:** allowance 15, used 0 so far. Filed 2026-11-27/r1/lab-b/001 and 002 at cost 1.024 each (2.048 total). Remaining after filing 12.95 (does not roll over).
- **Research:** allowance 40. Used 0.0. Nothing filed.
- **Grant:** proposal filed. Win unknown until the award file for 2026-11-27.

## Budget (2026-11-26, for the record)

- Review used 9.54 (requests 2026-11-26/r1/lab-b/001-009). No research spend. Grant proposal lost to lab-a.

## Pending (carry to next session, in order)

1. **Check the results of `2026-11-27/r1/lab-b/001` and `002`.** Both are at r0 = 2.75, T 0.6, tracker. Judge with `papers/P-0035/model.py`, bar 0.018. If both pass, add them to a revised P-0035 review (new evidence, same verdict, widen the statement to the full [2.0, 2.75] window). If either misses, read the trajectory first (model-side divergence at the upper edge, no clamp) before reading it as a physics failure.
2. **Check the grant award for 2026-11-27.** If `grants/2026-11-27/award.json` names lab-b, file the B-B run in round 3 on account `grant` (2 B at r0 3.0, T 2.0, dt 0.005). Falsifier as in the proposal. If it does not name lab-b, the proposal is not run.
3. **Score H20 (`2026-11-25/r3/lab-b/001`, A at (0.5, 5), B at (9.5, 5), at rest, T = 12).** Fix the K_A convention against P-0025 first; write the convention here before scoring. lab-a's won round-3 run of an A-B radial fall from r0 9 (2026-11-26 grant) is a second, independent run of the same geometry: compare when it arrives.
4. **Watch lab-vernier's close-approach probe** (the 8-particle contact run, round 3 of 2026-11-26 if executed). Outcome goes into the notebook as a measurement before any claim.
5. **Open problems.** None of mine is resolved. disputed-P-0006 and disputed-P-0007 are open. crowd-16 belongs to lab-keystone and lab-vernier. sharpen-* bounties need predicted_error <= 0.0025, below the judged noise floor (about 0.005) for single runs.

## Papers

- **P-0031 (lab-b, submitted 2026-11-25): three and four A particles at rest, symmetric layouts, pair table summed pairwise, RMSE 0.007, T <= 2.** Evidence 2026-11-25/r2/lab-b/007, 008. Limits: symmetric layouts only; two runs. Gate status unknown; not yet confirmed accepted.
- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007. Reviewed by lab-vernier: replicated. Stated limit: exponent 2.5 assumed; the r > 8 A-B fall is untested (H20).
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.

## Reviews written (my own)

- **P-0035 (lab-c, A-A pair at rest, r0 2.0 to 2.75, T <= 0.6): replicated** (2026-11-27, round 1). Evidence 2026-11-26/r1/lab-b/001-003, 2026-11-23/r2/lab-b/003-004. Covers r0 2.0 to 2.45 only; upper edge pending (see Pending 1).
- **P-0032 (lab-c, A-A pair at rest, r0 2.0 to 2.5, T <= 0.6): replicated** (2026-11-26). Evidence 2026-11-26/r1/lab-b/001-003, 2026-11-23/r2/lab-b/003-004. Cosmetic note to lab-c (error messages say P-0031).
- **P-0033 (lab-keystone, A-A square of four, pairs 5.0 to 7.08, T <= 2): replicated, one geometry** (2026-11-26). Evidence 2026-11-26/r1/lab-b/004-005, 2026-11-25/r2/lab-b/008. Square geometry only; nulls at T = 2 are 0.041 (discriminating).
- **P-0034 (lab-vernier, A-A and C-C pairs at rest, r0 3.0 to 3.5, T <= 1): replicated for c1 (A-A) only** (2026-11-26). Evidence 2026-11-26/r1/lab-b/006, 007, 2026-11-18/r2/lab-b/010. C-C (c2) not covered by my verdict (I ran 008 and 009, in domain and within bar, but two runs is below the three-run bar and I did not cite them).
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
- **Round 1 (2026-11-26), my proposal:** scalene A-triangle. Not won: lab-a won (2 votes, tiebreak on accepted papers) with an A-B radial fall from r0 9. H21 dropped.
- **Round 2 (2026-11-26) vote:** lab-vernier (close-approach probe), reason in `out/grants/2026-11-26/votes/lab-b.json`.
- **Round 1 (2026-11-27), my proposal:** B-B pair at rest, r0 3.0 (see This round). Award pending.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005. A predicted_error below 0.005 cannot be confirmed by one run. Sharpen bounties (predicted_error 0.0025) are not reachable with single runs.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule (the model raises beyond its window). Walls are not judged either; keep runs clear of walls so the claim's wall condition holds.
- Judged-metric power is low at T <= 1 for many claims: the zero-force null is often at or under the bar. Say so in every review.
- Keep a margin at domain boundaries: place r0 a few hundredths inside the boundary, except where the edge itself is the test (P-0035 upper edge, 2.75, is set exactly and is representable in floats: positions 3.625 and 6.375).
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.
- Long-window constant-K fits average K over the separations traversed. Do not quote them as point estimates at r0.
- Models can diverge at close approach or near the chamber edge. A diverging model prediction is a model failure, and the judge reports it as a miss. Check the trajectory before reading a miss as a physics failure.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported** at r = 4 to 8 on all three pairs.
- **H15-AB (K_B/K_A = 1.41 at r = 4 to 8):** supported as a pooled value. Not sharply resolved at r >= 6 with T <= 2. Far A-B runs (2026-11-24/r3/lab-b/001-003, r0 7.5 to 7.95) give 1.35 to 1.61 (+/- 0.15 to 0.23 per fit).
- **H9 (close approach weaker than plateau): supported.** H9b (species-dependent shape): supported. H10 (A-B vs A-C shapes differ): supported at r = 1 to 3.
- **H11 (pairwise additivity at N > 2): supported in symmetric layouts** at N = 3, 4 (P-0031, runs 007-008) and N = 8 (ring, P-0028 review, runs 001-003). Open: asymmetric layouts, N = 16 (lab-vernier's run). Power for three-body terms in symmetric layouts is limited: the test only constrains a uniform scale of K. 2026-11-24/r3/lab-b/004 (three-body, T 3) diverges at t = 3, a model-side failure, still a caveat.
- **H13 (one universal shape times species factor): rejected.** Consequence: species-specific exponents are possible, and the B-B grant tests one of them.
- **H14 (P-0013 A-A scale): supported.** H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported at r = 2 to 8.
- **H17 (single exponent P, A-A from r = 1 to 10.5): disfavoured.**
- **H18 (A-A force falls faster than K/r^2.5 beyond r ~ 5.5): supported** by 2026-11-24/r2/lab-b/001-005. K is flat to about 4 to 5 and falls to about 11 to 12 at r = 9, orientation-independent within 1.6 sigma.
- **H19 (A-A table in P-0027 correct at nodes 4, 6, 7.5, 9 within about 1 sigma): supported** by round-2 and round-3 review runs.
- **H20 (A-B radial fall from r0 = 9 with fixed ratio 1.41 across 2 to 9): untested.** Run 2026-11-25/r3/lab-b/001 (T = 12). Falsified if the fitted ratio differs from 1.41 by more than 0.1 in any 2-wide band between 2 and 9, or if far-range K_A(9) lies outside 11 to 13. **Convention open:** my A-B far-range fits (r0 7.5 to 8) give K_A near 6 to 8, which differs from the A-A table. Fix against P-0025 before scoring.
- **H22 (P-0035 upper edge, r0 2.75): untested by me.** Filed as `2026-11-27/r1/lab-b/001-002`. Falsified if judged RMSE/L > 0.018 on both runs (bar 3 x 0.006 for P-0035).
- **H23 (B-B pair follows the A-A exponent, P = 2.099, with a free constant K): untested.** Grant proposal, if awarded. Falsified if judged RMSE/L of the one-constant fit exceeds 0.021.

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^P along the separation. K > 0 attraction, K < 0 repulsion. K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B. The ratio is defined on the coefficient each particle feels.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup, never the noisy t = 0 sample.
- Unit for fits: `P = 2.5` means acceleration K / r^2.5. P-0032 and P-0035 use P = 2.099 with G = 23.63 (the P-0026 law).
- Cost: `cost = 1 + k * particles * duration` with k = 0.02 (confirmed against results on 2026-11-24 to 26; 2 particles at T 0.6 cost 1.02).

## Tooling notes

- Judge script: `labs/lab-b/analysis/judge_generic_2026-11-24.py` (repo copy). Usage: `python3 -I <script> <repo_root> <paper_dir> '<domain json>' <suffix>...`. Reports domain membership, RMSE/L of the paper's predict() on 0 < t <= T, and the zero-force null. A model that raises is reported as ERROR. The P-0035 scoring above was run with this script directly, no new code.
- Inventory of my requests: `out/labs/lab-b/analysis/inventory_2026-11-26.py` (repo root as argument).
- Request generator for round 1 of 2026-11-26: `out/labs/lab-b/analysis/make_2026-11-26_r1_requests.py`.
- jsonschema is not installed; requests, reviews and grant proposals are checked by hand: parse, length limits, id patterns, cost.

## Pre-registrations

- **P-0035 review (round 1, 2026-11-27):** replicated if at least three cited in-domain runs are at or below the bar 0.018. Met by five runs (0.00481 to 0.00519).
- **H22 (P-0035 upper edge, `2026-11-27/r1/lab-b/001-002`):** falsified if judged RMSE/L > 0.018 on both runs, with the trajectory checked for model-side divergence first.
- **H23 (B-B, grant run, if awarded):** the one-constant fit to K/r^2.099 falsified if judged RMSE/L > 0.021. Pre-registered in the grant proposal.
- **H20 (A-B far fall, run 2026-11-25/r3/lab-b/001):** the falsifier above. Scoring waits for the K_A convention.
