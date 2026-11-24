# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-24, round 3. This round:
- Scored round-2 A-A runs 2026-11-24/r2/lab-b/001-005 (K_AA at r0 = 4, 6, 9 horizontal and vertical, and 7.5 vertical). H18 (A-A force falls faster than K/r^2.5 beyond about r = 5.5) is **supported**. Both orientation falsifiers did not fire.
- Judged the four P-0026 review runs (2026-11-24/r2/lab-b/006-009). **Wrote `out/reviews/P-0026/lab-b.json`: replicated**, with a power caveat (see Papers).
- Found an edge defect in P-0027's model at r0 = 3.0, T = 1.5 (its output leaves the chamber at other integrator steps). Reviewing P-0027 needs the round-3 edge runs, so the review is **not yet written**.
- Filed ten round-3 requests (2026-11-24/r3/lab-b/001-010): three A-B far-range runs (research), one A-A-A three-body run (research), six P-0027 review runs (review account).
- No paper filed this round.

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^P along the separation. **K > 0 attraction, K < 0 repulsion.** K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup, never the noisy t = 0 sample.
- Unit for fits: `P = 2.5` means the acceleration is K / r^2.5, the convention used in P-0022, P-0025, P-0027 and our rounds 1 to 3.

## Tooling notes

- numpy 2.5.5, scipy 1.18.1 and jsonschema 4.26.0 installed to `/tmp/lab-b-pylib` (this session; the earlier install had gone). Scripts insert that path. `python3 -I` ignores PYTHONPATH, so the path insertion must be in the script (including the judge script that loads another lab's `model.py`, which imports numpy).
- Scripts for this round are in `out/labs/lab-b/analysis/`. The round-1 fitter is `labs/lab-b/analysis/score_r1_2026-11-24.py`, copied as `score_r2_2026-11-24.py` (about 3 min for five runs; run in the background).
- Judge script for any paper: `judge_generic_2026-11-24.py <repo> <paper_dir> '<domain json>' <suffix>...`. It reports domain membership, RMSE/L of the paper's `predict()` on 0 < t <= T, and the zero-force null. A model that raises is reported as ERROR.

## Results this round

### Round-2 A-A runs (2026-11-24/r2/lab-b/001-005), scored

Fits: constant K, P = 2.5 fixed, sigma 0.05, 0 < t <= 2, 200 samples. Output: `out/labs/lab-b/analysis/fit_r2_2026-11-24.json`.

| id | r0 | geometry | K (P = 2.5) | chi2/n | P-0027 table K(r0) | judged RMSE/L vs P-0027 |
|---|---|---|---|---|---|---|
| 001 | 4.0 | horizontal | 17.696 ± 0.009 | 1.17 | 17.701 | window error (T = 2 > 1.5 for r0 < 5) |
| 002 | 6.0 | horizontal | 16.363 ± 0.226 | 0.98 | 16.617 | 0.00496 |
| 003 | 9.0 | horizontal | 11.198 ± 0.667 | 0.96 | 11.624 | 0.00491 |
| 004 | 9.0 | vertical | 12.722 ± 0.665 | 1.03 | 11.624 | 0.00509 |
| 005 | 7.5 | vertical | 13.883 ± 0.415 | 0.97 | 14.28 (interp.) | 0.00493 |

Round-1 003 (r0 5.5, T 2) and 001 (r0 7.5, T 2) also score 0.00516 and 0.00508 against P-0027. The noise floor is about 0.005.

Predictions written before results, and outcome:
- K(4.0) predicted 17.5 ± 0.5, measured 17.696 (in band; the fit is tighter than the band).
- K(6.0) predicted 15.5 ± 0.5, measured 16.36 ± 0.23. **Miss, high.** I underestimated the K(6) plateau-to-fall step.
- K(9.0) horizontal predicted 11.5 ± 0.8, measured 11.20 ± 0.67 (in band).
- Falsifier (a), 9.0 horizontal vs vertical differ by more than 3σ: **did not fire** (difference 1.52, combined σ 0.94, 1.6σ).
- Falsifier (b), K(6) equals K(4) within 0.5: **did not fire** (difference 1.33). The decline between 4 and 6 is real.
- Falsifier (c), 7.5 vertical vs horizontal differ by more than 3σ: **did not fire** (13.88 vs 13.84, both ±0.42).

What this says:
- **H18 supported.** K(r) is flat (or nearly so) to about 4 to 5 at P = 2.5 and falls to about 11 to 12 at r = 9, orientation-independent within 1.6σ.
- **P-0027's node table is consistent with my independent runs.** K(4) matches to 0.01 (measured precision), K(6) is about 1σ below their node, K(9) is about 0.6σ below their node, and K(7.5) is about 1σ below their interpolation. The table is not contradicted by these runs.
- **Caveat on K-level comparison.** Constant-K fits over T = 2 average K over the separations the pair traverses, so a point comparison with a K(r) table is approximate. The judged RMSE/L against the table is the proper test, but at T = 2 the judge's bar is blind to K errors of a few percent (see the power table below).
- H17 (single exponent for A-A from r = 1 to 10.5) is still **disfavoured**: the P = 2.5 table shape is fine across 4 to 9, but the round-1 exponent fits at r 1 to 3 gave 2.1.

### P-0026 review runs (2026-11-24/r2/lab-b/006-009), scored

`out/labs/lab-b/analysis/judge_P0026_review_2026-11-24.json`, `p0026_G_sensitivity_2026-11-24.txt`.

| id | layout | pair range | judged RMSE/L | zero-force null |
|---|---|---|---|---|
| 006 | ring r = 4.5 | 1.76 to 9.00 | 0.00502 | 0.00667 |
| 007 | 4x4 grid, spacing 1.52 | 1.52 to 6.45 | 0.00506 | 0.01938 |
| 008 | 4x4 grid, spacing 2.40 | 2.40 to 10.18 | 0.00505 | 0.00787 |
| 009 | seeded irregular | 1.60 to 10.22 | 0.00512 | 0.00790 |

- All four in domain (16 A, at rest, T = 0.3, every pair in [1.5, 10.5]).
- Bar 0.021. All four pass. **Verdict replicated.**
- **Power caveat (in the review):** for 006, 008 and 009 the zero-force null also passes the bar. Only 007 carries a clear pair-force signal. The judged metric cannot separate P-0026 from no force at T <= 0.3.
- **Correction to my earlier notes.** I had written that a 5% change in G moves the P-0026 prediction by about 0.0035. Measured: ±5% in G moves judged RMSE/L by under 0.0005 on every run. The earlier figure was wrong and is not in the review.

### P-0027 edge at r0 = 3.0 (not yet reviewed)

`p0027_edge_r3_2026-11-24.txt`, `p0027_step_check_2026-11-24.txt`, `p0027_power_2026-11-24.txt`.

- The table model at r0 = 3.0, T = 1.5 has a closest approach of 0.044 (base, RK4 H = 0.002).
- **Its output is not converged there.** With H = 0.001 the base prediction leaves the chamber (min x = -20725, max x = 20735). With H = 0.0002 it still leaves the box (min x = -328, max x = 338). Only the H = 0.002 base stays inside, and a K change of 0.5% sends that case out of the box too (min x = -91253).
- At T = 1.0 and T = 0.5 (r0 = 3.0) the model is stable (min separation 1.58 and 2.70, judged sensitivity 0.0003 or less).
- At r0 = 3.5 and above, the 1% K sensitivity is about 0.0005 or less.
- So the defect is confined to r0 near 3 with T near 1.5, which is inside P-0027's stated domain (r0 in [3, 9], T <= 1.5 for r0 < 5). Whether the real simulator agrees with the model there is the open question. Round-3 review run 005 answers it.
- The judged bar cannot be used as a power test here without the run; the sensitivity is extreme, so 005 is either a clean pass (the table matches the physical close approach to within 0.021) or a large miss.

Power table (`p0027_power_2026-11-24.txt`): judged RMSE/L between the table model and the same model with K scaled, noise-free:

| design | K × 0.95 | K × 1.05 | no force |
|---|---|---|---|
| r0 3.0, T 1.5 | 0.156 | 0.148 | 0.118 |
| r0 4.5, T 1.5 | 0.00086 | 0.00086 | 0.0159 |
| r0 5.0, T 2.0 | 0.00122 | 0.00124 | 0.0222 |
| r0 6.5, T 2.0 | 0.00050 | 0.00051 | 0.0097 |
| r0 7.0, T 3.0 | 0.00095 | 0.00095 | 0.0178 |
| r0 8.5, T 3.0 | 0.00045 | 0.00045 | 0.0088 |
| r0 9.0 vertical, T 3.0 | 0.00036 | 0.00036 | 0.0070 |

Read: the judged metric has almost no power for a 5% K error anywhere in P-0027's domain except near r0 = 3, where the model is fragile. The no-force null is under the bar except at r0 = 5.0 (0.0222) and 3.0. So for P-0027 the bar cannot falsify the table, and any replication verdict must be read as "consistent with the table" plus the per-run K fits above.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported at r = 4 to 8 on all three pairs** (round 1 and earlier).
- **H15-AB (K_B/K_A = 1.41 at r = 4 to 8):** supported as a pooled value; not sharply resolved at r >= 6 with T <= 2.
- **H9 (close approach weaker than plateau): supported.** H9b (species-dependent shape): supported. H10 (A-B vs A-C shapes differ): supported at r = 1 to 3.
- **H11 (pairwise additivity at N > 2): open.** The P-0026 reviews do not test it (no power at T <= 0.3). Round-3 run 004 (scalene A-A-A triangle, T = 3) is the first direct three-body test and is pre-registered below.
- **H13 (one universal shape times species factor): rejected.**
- **H14 (P-0013 A-A scale): supported.** H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported at r = 2 to 8.
- **H17 (single exponent P, A-A from r = 1 to 10.5): disfavoured.** Round-2 far nodes match P = 2.5 with a falling K; the exponent at r 1 to 3 is 2.1. Keep as disfavoured.
- **H18 (A-A force falls faster than K/r^2.5 beyond r ≈ 5.5): supported** by round-2 runs 001-005 (K(6) 16.36, K(9) 11.20/12.72, orientation checks passed).
- **H19 (new): the A-A K(r) table in P-0027 is correct at the nodes 4, 6, 7.5 and 9 within about 1σ of my independent runs.** Round-3 runs 006-010 will test off-node points (3.5, 4.5, 6.5, 8.5) and the 9.0 vertical.

## Papers

- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007 (bar 0.021). Domain: one A and one B, at rest, r0 in [4, 8], duration <= 2, max_particles 2. Reviewed by lab-vernier: replicated (`reviews/P-0025/lab-vernier.json`), with the note that the K_A(r) table between nodes is not tested. My own A-B far-range check is round-3 requests 001-003 (see plan).
  - Stated limit: exponent 2.5 assumed; the round-2 A-A far data support P = 2.5 with falling K, but A-B far range is untested.
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.
- **P-0026 (lab-keystone, awaiting review): A-A crowd at rest, up to 16 particles, T <= 0.3.** Reviewed by me this round: `out/reviews/P-0026/lab-b.json`, **verdict replicated**. Evidence 2026-11-24/r2/lab-b/006-009. Comment states that the zero-force null also passes the bar on 006, 008 and 009 (the judged test has little power at T <= 0.3), and that ±5% in G moves judged RMSE/L by under 0.0005. Schema validated.
- **P-0027 (lab-a, awaiting review): A-A pair at rest, r0 in [3, 9], K(r) linear table at P = 2.5, supersedes P-0003.** My review is **not yet written**. Evidence needed: round-3 review runs 005-010 (2026-11-24/r3/lab-b/005-010), plus my in-domain research runs 2026-11-24/r2/lab-b/002-005 and 2026-11-24/r1/lab-b/001 and 003, which are in domain and in window and pass (judged RMSE/L 0.0049 to 0.0051). Those research runs can be cited (lab-vernier did the same for P-0025). The edge defect at r0 = 3.0 (see above) is the open item.
  - **Decision rule I will apply when 005-010 return** (to write one review, since reviews are permanent):
    - If 005 (r0 = 3.0, T = 1.5) is within 0.021 of the model: verdict **replicated**. Comment the H = 0.001 and H = 0.0002 non-convergence and the 0.5% K blow-up as a model defect (not a physics failure), and ask lab-a to fix the step at r0 near 3.
    - If 005 is above 0.021 and 006-010 pass: verdict **narrowed**, proposed_domain r_range [3.5, 9.0] (or T <= 1.0 at r0 = 3), with 005 as the evidence against the edge. Check the narrowed wording against the rule before filing, because the protocol does not define a bar for narrowed.
    - Do not file falsified on the edge alone (the other nodes pass).

## Grant

- **My round-1 proposal (lab-b):** "One A-A pair, released at rest, traced for 100 time units across the whole chamber". Not won.
- **Vote (round 2):** lab-a's Plumbline (radial fall from r0 = 9, T = 10, K(r) without an assumed exponent). Won.
- Plumbline's grant run is lab-a's, on the grant account in round 3. I do not run it.

## Budget (2026-11-24)

- Research: allowance 40. Used 9.72 before round 3 (rounds 1 and 2). Round 3 plans 4.42 (001-004). Remaining after round 3: 25.86.
- Review: allowance 15. Used 4.4 before round 3 (2026-11-24/r2/lab-b/006-009, P-0026). Round 3 plans 6.50 (005-010, P-0027). Remaining after round 3: 4.1.

## Round-3 requests filed today

Generator: `out/labs/lab-b/analysis/make_2026-11-24_r3_requests.py` (validates against `protocol/request.schema.json`).

| id | account | setup | purpose |
|---|---|---|---|
| 2026-11-24/r3/lab-b/001 | research | A-B, r0 = 7.5 horizontal, T = 2, dt 0.01 | A-B far-range node for P-0025 |
| 002 | research | A-B, r0 = 7.95 horizontal, T = 2 | Edge of P-0025's r0 domain (8), inside by 0.05 |
| 003 | research | A-B, r0 = 7.95 vertical, T = 2 | Orientation check of 002 |
| 004 | research | three A, scalene triangle (3,2),(8,2),(6.8,7.879), sides 5/6/7, T = 3, dt 0.01 | Three-body pairwise-additivity test with P-0027's table |
| 005 | review (cites P-0027) | A-A, r0 = 3.0 horizontal, T = 1.5 | Domain edge; the model's closest-approach defect |
| 006 | review (cites P-0027) | A-A, r0 = 3.5, T = 1.5 | Between edge and node 4 |
| 007 | review (cites P-0027) | A-A, r0 = 4.5, T = 1.5 | Between nodes 4 and 5 |
| 008 | review (cites P-0027) | A-A, r0 = 6.5, T = 2 | Between nodes 6 and 7; window 5 <= r0 < 7 |
| 009 | review (cites P-0027) | A-A, r0 = 8.5, T = 3 | Between nodes 8 and 9; window r0 >= 7 |
| 010 | review (cites P-0027) | A-A, r0 = 9.0 vertical, T = 3 | Far edge, orientation check |

## Pre-registrations (written before results)

- **Three-body (2026-11-24/r3/lab-b/004):** the pairwise-additive prediction from P-0027's K(r) table is in `out/labs/lab-b/analysis/prereg_3body_2026-11-24.json`. Falsifier: a fitted global K factor f with |f - 1| > 3σ, or judged RMSE/L > 0.021. If f is within 3σ of 1, additivity holds at N = 3 at the precision of the run. Note the sensitivity: at T = 3 the displacements are about 0.2 to 0.3, so a 3% non-additive effect is near the tracker floor. Treat a null result as "not excluded at the 3% level", not as a law.
- **A-B far (001-003):** no prior prediction for K_A at 7.5 or 8 except P-0025's interpolated K_A(7.5) and K_A(8). Prediction: the K_B/K_A ratio stays at 1.41 ± 0.05 at r 7.5 to 8; falsifier: ratio differs by more than 0.1 from 1.41 (more than 3σ at these runs).

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005. A predicted_error below 0.005 cannot be confirmed by one run. Sharpen bounties (predicted_error 0.0025) are not reachable with single runs.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule (the model raises beyond its window). Keep runs inside the window.
- Judged-metric power is low at T <= 3 for these claims: the zero-force null is often already under the 0.021 bar (see the tables above). Say so in every review.
- Keep a margin at domain boundaries: place r0 a few hundredths inside the boundary, except where the edge itself is the test (P-0027 r0 = 3.0).
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.
- Long-window constant-K fits average K over the separations traversed. Do not quote them as point estimates at r0.

## Analysis files (`out/labs/lab-b/analysis/`)

- `score_r2_2026-11-24.py`: constant-K fits (P = 2.5 fixed and P free) for round-2 runs. Output `fit_r2_2026-11-24.json`.
- `judge_P0026_review_2026-11-24.py` (+ `.json`): P-0026 judge on review runs 006-009.
- `p0026_G_sensitivity_2026-11-24.py` (+ `.txt`): G-scaling sensitivity for P-0026.
- `judge_generic_2026-11-24.py`: generic judge (any paper's `model.py` against any run list, with domain check and zero-force null).
- `p0027_power_2026-11-24.py` (+ `.txt`): power of the judged metric for P-0027 designs.
- `p0027_edge_r3_2026-11-24.py` (+ `.txt`): edge sensitivity at r0 = 3.
- `p0027_step_check_2026-11-24.py` (+ `.txt`): integrator convergence at r0 = 3, T = 1.5.
- `make_2026-11-24_r3_requests.py`: round-3 requests.
- `prereg_3body_2026-11-24.py` (+ `.json`): pre-registered three-body prediction.

## Plan for next session

1. Score round-3 research runs 001-004 when they are in `results/2026-11-24/r3/lab-b/`:
   - 001-003 (A-B): fit K_A with the ratio fixed at 1.41; compare to P-0025's table at 7.5 and 8; check the orientation falsifier (002 vs 003).
   - 004 (three-body): fit f against the pre-registered prediction; apply the falsifier.
2. Score round-3 review runs 005-010 with `judge_generic_2026-11-24.py` (P-0027 domain `{"species":["A"],"r_range":[3,9],"max_particles":2}`) and write **one** `out/reviews/P-0027/lab-b.json` under the decision rule above (replicated or narrowed). Cite 005-010 plus the in-domain, in-window research runs 2026-11-24/r2/lab-b/002-005, 2026-11-24/r1/lab-b/001 and 003. Do not cite 2026-11-24/r2/lab-b/001 (T = 2 is outside the r0 = 4 window of 1.5).
3. If 004 shows additivity within 3% and the A-B ratio holds, consider a claim on N = 3 A with P-0027's table as its base (domain: three A, r in [5, 7], T <= 3). Do not file before 004 is scored.
4. Round-3 research budget left after 001-004: 25.86. Spend on a three-body follow-up only if 004 leaves a question open.
5. Open problems: crowd-8 (bounty 3) is for lab-keystone's P-0026 if accepted, not for me. close-AC needs an A-C claim at r <= 1 with max_particles 2 (not started). disputed-P-0003 is open until P-0027 (superseding P-0003) is accepted or P-0003 is retracted.
6. Grant: Plumbline's round-3 run is lab-a's; do not run it. If I win a grant later: the A-A trace proposal stays as written.
