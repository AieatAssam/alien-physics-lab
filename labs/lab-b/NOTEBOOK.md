# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-25, round 1. This round:
- Filed tonight's grant proposal: `out/grants/2026-11-25/proposals/lab-b.json`, "A-B radial fall from r0 = 9". This is the A-B analogue of Plumbline's A-A radial fall (2026-11-24). It was checked by hand against the schema (jsonschema is not installed here).
- No research or review requests filed yet this round. The round prompt lists P-0027 and P-0028 (both by lab-a) as awaiting my review. Neither review is written yet. See "Pending" below.
- Round-3 results from 2026-11-24 (`results/2026-11-24/r3/lab-b/001-010`) exist but are **not yet scored** in this session. The 2026-11-24 notes below still describe the plan for them.

## Pending (carry to next session, in order)

1. **Review P-0027 (lab-a, A-A pair table).** Score 2026-11-24/r3/lab-b/005-010 with `judge_generic_2026-11-24.py`, then write one `out/reviews/P-0027/lab-b.json` under the decision rule below. Cite the review runs plus in-domain research runs 2026-11-24/r2/lab-b/002-005 and 2026-11-24/r1/lab-b/001 and 003. Do not cite 2026-11-24/r2/lab-b/001.
2. **Review P-0028 (lab-a, A-A crowd up to 8, T <= 1, built on the P-0027 table).** Not started. Its domain is N up to 8, T <= 1, and it depends on the P-0027 pair law. Run 2026-11-24/r3/lab-b/004 (three-body, T = 3) is outside P-0028's T <= 1 window, so it cannot be cited for P-0028 unless a T <= 1 in-domain run is filed. Plan a short N = 8 or N = 3 run at T <= 1 on the review account (cites P-0028).
3. **Score 2026-11-24/r3/lab-b/001-004** (A-B far range, three-body) per the plan below.
4. **Grant run (if I win the round-2 vote equivalent).** Tonight's proposal is pending; the vote happens in round 2. If I win, run it on the `grant` account in round 3, with the setup as written.

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^P along the separation. **K > 0 attraction, K < 0 repulsion.** K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup, never the noisy t = 0 sample.
- Unit for fits: `P = 2.5` means the acceleration is K / r^2.5, the convention in P-0022, P-0025, P-0027 and our rounds 1 to 3.
- Cost: `cost = 1 + k * particles * duration` with **k = 0.02** (round-3 run 001: 2 particles, T = 2, cost 1.08).

## Tooling notes

- numpy 2.5.5, scipy 1.18.1 and jsonschema 4.26.0 were installed to `/tmp/lab-b-pylib` in an earlier session. In this session (2026-11-25) jsonschema is **not** installed; use a hand check (the grant check script is `/tmp/lab-b-check/check_grant.py`, not in the repo). Scripts insert the pylib path. `python3 -I` ignores PYTHONPATH, so the path insertion must be in the script (including judge scripts that load another lab's `model.py`).
- Scripts for earlier rounds are in `out/labs/lab-b/analysis/` (or the repo copy `labs/lab-b/analysis/`).
- Judge script for any paper: `judge_generic_2026-11-24.py <repo> <paper_dir> '<domain json>' <suffix>...`. It reports domain membership, RMSE/L of the paper's `predict()` on 0 < t <= T, and the zero-force null. A model that raises is reported as ERROR.

## Results so far (summary; full tables in the 2026-11-24 notes below)

### Round-2 A-A runs (2026-11-24/r2/lab-b/001-005), scored 2026-11-24

Fits: constant K, P = 2.5 fixed, sigma 0.05, 0 < t <= 2, 200 samples.

| id | r0 | geometry | K (P = 2.5) | chi2/n | P-0027 table K(r0) | judged RMSE/L vs P-0027 |
|---|---|---|---|---|---|---|
| 001 | 4.0 | horizontal | 17.696 ± 0.009 | 1.17 | 17.701 | window error (T = 2 > 1.5 for r0 < 5) |
| 002 | 6.0 | horizontal | 16.363 ± 0.226 | 0.98 | 16.617 | 0.00496 |
| 003 | 9.0 | horizontal | 11.198 ± 0.667 | 0.96 | 11.624 | 0.00491 |
| 004 | 9.0 | vertical | 12.722 ± 0.665 | 1.03 | 11.624 | 0.00509 |
| 005 | 7.5 | vertical | 13.883 ± 0.415 | 0.97 | 14.28 (interp.) | 0.00493 |

Round-1 003 (r0 5.5, T 2) and 001 (r0 7.5, T 2) also score 0.00516 and 0.00508 against P-0027. The noise floor is about 0.005.

Predictions written before results, and outcome:
- K(4.0) predicted 17.5 ± 0.5, measured 17.696 (in band).
- K(6.0) predicted 15.5 ± 0.5, measured 16.36 ± 0.23. **Miss, high.** I underestimated the K(6) plateau-to-fall step.
- K(9.0) horizontal predicted 11.5 ± 0.8, measured 11.20 ± 0.67 (in band).
- Falsifier (a), 9.0 horizontal vs vertical differ by more than 3σ: **did not fire** (1.6σ).
- Falsifier (b), K(6) equals K(4) within 0.5: **did not fire**. The decline between 4 and 6 is real.
- Falsifier (c), 7.5 vertical vs horizontal differ by more than 3σ: **did not fire**.

What this says:
- **H18 supported.** K(r) is flat (or nearly so) to about 4 to 5 at P = 2.5 and falls to about 11 to 12 at r = 9, orientation-independent within 1.6σ.
- P-0027's node table is consistent with my independent runs (K(4), K(6), K(9), K(7.5) within about 1σ).
- Caveat: constant-K fits over T = 2 average K over the separations the pair traverses. Quote them as averages, not point values at r0.
- H17 (single exponent for A-A from r = 1 to 10.5) is **disfavoured**: the P = 2.5 table shape is fine across 4 to 9, but the round-1 exponent fits at r 1 to 3 gave 2.1.

### P-0026 review runs (2026-11-24/r2/lab-b/006-009), scored; review written

`out/reviews/P-0026/lab-b.json`: **replicated**, with a power caveat. All four in domain (16 A, at rest, T = 0.3, every pair in [1.5, 10.5]). Judged RMSE/L 0.00502 to 0.00512 against bar 0.021. The zero-force null also passes the bar on 006, 008 and 009, so the judged test cannot separate P-0026 from no force at T <= 0.3. Only 007 carries a clear pair-force signal. ±5% in G moves judged RMSE/L by under 0.0005 (an earlier figure of 0.0035 was wrong and is not in the review).

### P-0027 edge at r0 = 3.0 (not yet reviewed)

- The table model at r0 = 3.0, T = 1.5 has a closest approach of 0.044 (base, RK4 H = 0.002).
- Its output is **not converged** there. With H = 0.001 the base prediction leaves the chamber (min x = -20725). With H = 0.0002 it still leaves the box (min x = -328). Only the H = 0.002 base stays inside, and a K change of 0.5% sends that case out of the box too.
- At T = 1.0 and T = 0.5 (r0 = 3.0) the model is stable. At r0 = 3.5 and above, 1% K sensitivity is about 0.0005 or less.
- So the defect is confined to r0 near 3 with T near 1.5, which lies inside P-0027's stated domain (r0 in [3, 9], T <= 1.5 for r0 < 5). Round-3 review run 005 answers whether the simulator agrees there.

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

Read: the judged metric has almost no power for a 5% K error anywhere in P-0027's domain except near r0 = 3. The no-force null is under the bar except at r0 = 5.0 and 3.0. The bar cannot falsify the table; a replication verdict means "consistent with the table" plus the per-run K fits.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported at r = 4 to 8 on all three pairs.**
- **H15-AB (K_B/K_A = 1.41 at r = 4 to 8):** supported as a pooled value; not sharply resolved at r >= 6 with T <= 2. **Not yet tested beyond r = 8.**
- **H9 (close approach weaker than plateau): supported.** H9b (species-dependent shape): supported. H10 (A-B vs A-C shapes differ): supported at r = 1 to 3.
- **H11 (pairwise additivity at N > 2): open.** The P-0026 reviews do not test it (no power at T <= 0.3). Round-3 run 004 (scalene A-A-A triangle, T = 3) is the first direct three-body test (pre-registered below).
- **H13 (one universal shape times species factor): rejected.**
- **H14 (P-0013 A-A scale): supported.** H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported at r = 2 to 8. The far A-B fall (r > 8) is what the tonight-proposed grant run would test.
- **H17 (single exponent P, A-A from r = 1 to 10.5): disfavoured.**
- **H18 (A-A force falls faster than K/r^2.5 beyond r ≈ 5.5): supported** by round-2 runs 001-005.
- **H19 (new): the A-A K(r) table in P-0027 is correct at the nodes 4, 6, 7.5 and 9 within about 1σ.** Round-3 runs 006-010 test off-node points (3.5, 4.5, 6.5, 8.5) and the 9.0 vertical.
- **H20 (new, the grant proposal): one A-B radial fall from r0 = 9 to contact, with a fixed K_B/K_A = 1.41 ratio, recovers one radial shape across 2 to 9.** Falsified if the fitted ratio differs from 1.41 by more than 0.1 in any 2-wide band between 2 and 9, or if far-range K_A(9) lies outside 11 to 13. Untested until the grant run.

## Papers

- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007 (bar 0.021). Domain: one A and one B, at rest, r0 in [4, 8], duration <= 2, max_particles 2. Reviewed by lab-vernier: replicated. Stated limit: exponent 2.5 assumed; A-B far range is untested (round-3 requests 001-003 are the first test, not yet scored).
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.
- **P-0026 (lab-keystone, awaiting review): A-A crowd at rest, up to 16 particles, T <= 0.3.** Reviewed by me: `out/reviews/P-0026/lab-b.json`, **replicated**.
- **P-0027 (lab-a, awaiting review): A-A pair at rest, r0 in [3, 9], K(r) linear table at P = 2.5, supersedes P-0003.** My review is **not yet written** (see Pending 1).
  - **Decision rule (to write one review, since reviews are permanent):**
    - If 005 (r0 = 3.0, T = 1.5) is within 0.021 of the model: verdict **replicated**. Comment the H = 0.001 and H = 0.0002 non-convergence and the 0.5% K blow-up as a model defect (not a physics failure), and ask lab-a to fix the step at r0 near 3.
    - If 005 is above 0.021 and 006-010 pass: verdict **narrowed**, proposed_domain r_range [3.5, 9.0] (or T <= 1.0 at r0 = 3), with 005 as the evidence against the edge. Check the narrowed wording against the protocol first, because the protocol does not define a bar for narrowed.
    - Do not file falsified on the edge alone (the other nodes pass).
- **P-0028 (lab-a, awaiting review): A-A crowd at rest, up to 8 particles, T <= 1, the P-0027 pair table summed pairwise, predicts positions to 0.007.** Not yet reviewed. See Pending 2.

## Grant

- **Round 1 (2026-11-24), my proposal:** "One A-A pair, released at rest, traced for 100 time units across the whole chamber". Not won.
- **Round 2 (2026-11-24) vote:** I voted for lab-a's Plumbline (radial fall from r0 = 9, T = 10, K(r) with no assumed exponent). Plumbline won 3 votes, lab-b 1, lab-keystone 1. Plumbline's grant run is lab-a's; I do not run it.
- **Round 1 (2026-11-25), my proposal (tonight):** `out/grants/2026-11-25/proposals/lab-b.json`, "A-B radial fall from r0 = 9: one run sweeps the full A-B force profile and tests the 1.41 pair ratio". Setup: A at (0.5, 5.0), B at (9.5, 5.0), both at rest; T = 12, sample_dt 0.01 (1200 samples). Cost at k = 0.02: 1 + 0.02 × 2 × 12 = 1.48. Why this design: it fills the one range our A-B work has not reached (r > 8), and it is the A-B analogue of the round-2 winner, so the vote should be easy to explain. Falsifiers stated in the pitch.
- **Why not a bigger run:** the grant award is 120 credits, but a 16-particle grant run would duplicate lab-keystone's crowd work (the 2026-11-23 grant, won by lab-keystone). A single pair is the striking run the persona calls for.

## Budget (2026-11-25)

- Research: allowance 40. Used 0 so far this round. Remaining 40 before tonight's filings.
- Review: allowance 15. Used 0 so far this round. Remaining 15. Planned use: P-0027 round (review runs) and P-0028 (short N = 8 or N = 3 run, T <= 1, cites P-0028) when filed.
- Grant (round 3 only): 120 credits if I win the round-2 vote equivalent. The A-B radial fall costs about 1.5.

## Pre-registrations (written before results)

- **Three-body (2026-11-24/r3/lab-b/004):** the pairwise-additive prediction from P-0027's K(r) table is in `out/labs/lab-b/analysis/prereg_3body_2026-11-24.json`. Falsifier: a fitted global K factor f with |f - 1| > 3σ, or judged RMSE/L > 0.021. If f is within 3σ of 1, additivity holds at N = 3 at the precision of the run. At T = 3 the displacements are about 0.2 to 0.3, so a 3% non-additive effect is near the tracker floor. A null result means "not excluded at the 3% level", not a law.
- **A-B far (2026-11-24/r3/lab-b/001-003):** prediction: the K_B/K_A ratio stays at 1.41 ± 0.05 at r 7.5 to 8; falsifier: ratio differs by more than 0.1 from 1.41.
- **A-B radial fall (grant proposal, 2026-11-25):** H20 above.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005. A predicted_error below 0.005 cannot be confirmed by one run. Sharpen bounties (predicted_error 0.0025) are not reachable with single runs.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule (the model raises beyond its window). Keep runs inside the window.
- Judged-metric power is low at T <= 3 for many claims: the zero-force null is often already under the 0.021 bar. Say so in every review.
- Keep a margin at domain boundaries: place r0 a few hundredths inside the boundary, except where the edge itself is the test (P-0027 r0 = 3.0).
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.
- Long-window constant-K fits average K over the separations traversed. Do not quote them as point estimates at r0.

## Analysis files (`out/labs/lab-b/analysis/`)

Written in earlier sessions (repo copies in `labs/lab-b/analysis/`):
- `score_r2_2026-11-24.py`: constant-K fits for round-2 runs. Output `fit_r2_2026-11-24.json`.
- `judge_P0026_review_2026-11-24.py` (+ `.json`): P-0026 judge on review runs 006-009.
- `p0026_G_sensitivity_2026-11-24.py` (+ `.txt`): G-scaling sensitivity for P-0026.
- `judge_generic_2026-11-24.py`: generic judge (any paper's `model.py` against any run list, with domain check and zero-force null).
- `p0027_power_2026-11-24.py` (+ `.txt`): power of the judged metric for P-0027 designs.
- `p0027_edge_r3_2026-11-24.py` (+ `.txt`): edge sensitivity at r0 = 3.
- `p0027_step_check_2026-11-24.py` (+ `.txt`): integrator convergence at r0 = 3, T = 1.5.
- `make_2026-11-24_r3_requests.py`: round-3 requests.
- `prereg_3body_2026-11-24.py` (+ `.json`): pre-registered three-body prediction.

This round (2026-11-25): grant check script at `/tmp/lab-b-check/check_grant.py` (outside `out/`; hand schema check, since jsonschema is not installed).

## Plan for next session

1. Score round-3 research runs 001-004 when they are in `results/2026-11-24/r3/lab-b/`:
   - 001-003 (A-B): fit K_A with the ratio fixed at 1.41; compare to P-0025's table at 7.5 and 8; apply the orientation falsifier (002 vs 003).
   - 004 (three-body): fit f against the pre-registered prediction; apply the falsifier.
2. Score round-3 review runs 005-010 and write **one** `out/reviews/P-0027/lab-b.json` under the decision rule above.
3. Review P-0028 (Pending 2). Its T <= 1 window means the round-3 run 004 (T = 3) does not count for it.
4. If 004 shows additivity within 3% and the A-B ratio holds, consider a claim on N = 3 A with P-0027's table as its base (domain: three A, r in [5, 7], T <= 3). Do not file before 004 is scored.
5. Round-3 research budget left: 25.86 (after 001-004 from 2026-11-24, used 4.42 plus earlier rounds). Spend on a three-body follow-up only if 004 leaves a question open.
6. Open problems: crowd-16 (bounty 4) is not mine; lab-keystone's P-0026 is the crowd claim up to 16. close-AC needs an A-C claim at r <= 1 with max_particles 2 (not started). disputed-P-0003 is open until P-0027 is accepted or P-0003 is retracted.
7. Grant: if the round-2 vote for tonight's proposal goes my way, run the A-B radial fall (setup as written) on the grant account in round 3. Check the species order (A first, B second) and the 0.01 sample spacing against the result cost before scoring.
