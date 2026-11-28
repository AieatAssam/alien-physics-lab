# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-28, round 3.

## This round (2026-11-28, round 3)

- **Reviews filed (both to `out/reviews/`, validated by hand against the schema):**
  - **P-0037 (lab-keystone, A-A pair, r0 3.5 to 9): replicated** (consistent, not precise). Evidence `2026-11-28/r2/lab-b/004, 005, 006`. Judged RMSE/L 0.00490, 0.00502, 0.00497 against bar 0.021. Nulls 0.010, 0.009, 0.031, so power is modest. predict() did not raise on any of the three.
  - **P-0036 (lab-a, mixed pairs A-B, A-C, B-C at r0 3 to 5, T 2): narrowed to r0 in [4, 5].** Not "replicated" on the stated domain, and not "falsified". Eleven clean in-domain runs at r0 4.0 to 5.0 (RMSE/L 0.00489 to 0.00513). Two A-B runs at r0 = 3.0 with T = 2 (`2026-11-28/r2/lab-b/001`, RMSE/L 4.04; `2026-11-18/r3/lab-b/015`, 8.12) reach a measured separation of about 0.03 to 0.04 at t about 1.6. So the pair goes through contact. The claim excludes contact, but the judge's domain check sees only initial distances, so these count as in domain. The model then diverges (1/r^2.5 with no contact treatment). Repulsive A-C and B-C at r0 3.0 and 3.5 are clean (0.00498 to 0.00503). The judged metric cannot see the mass-ratio tension (0.72 vs 0.7085), which is mentioned in the comment as a side note.
  - Evidence for P-0036 cites my earlier runs as well as the round-2 review runs: 2026-11-18/r2/lab-b/014, 2026-11-18/r3/lab-b/009 to 016, 2026-11-22/r2/lab-b/006, 007, 009, 2026-11-22/r3/lab-b/003, 2026-11-23/r3/lab-b/001, 2026-11-25/r2/lab-b/005, 006 (lower judge scores, not cited). Those are in the review file's evidence list. Scores are reproducible with `analysis/review_scores_2026-11-28.sh`.
- **Grant (2026-11-28, "Sixteen A at rest on a jittered grid"): NOT filed. Blocked.** Reason is the pre-registered rule from round 1: pin the pair law before the run. It cannot be pinned consistently:
  - A-A P = 2.5 law is unmeasured for separations 2.75 to 3.0. The linear fill between P-0037's 2.5 and 3.0 nodes (from P-0034) is an interpolation, not a measurement.
  - Pairs at about 2.23 (the proposal's nearest pair) need P-0035, which has exponent 2.099 and G = 23.63, and is validated only for T <= 0.6. A single pair-sum cannot use two exponents.
  - At T = 2 many pairs reach contact (see the P-0036 finding above), where no law is validated.
  - Any 16-body layout in a 10 x 10 chamber has minimum spacing about 3.0 or less, so the gap is unavoidable. The earlier design note ("16 bodies with min spacing 3.5") is not feasible.
  - The 120-credit award for 2026-11-28 is therefore unspent. It is the user's call whether to allow a substitute design. Any substitute must be written and pre-registered before filing.
- **Budget (2026-11-28):** research allowance 40, used 5.2 in round 2 (`2026-11-28/r2/lab-b/007, 008`), so 34.8 left and not spent this round (no pre-registered design ready). Review allowance 15, used 6.55 (round 2), so 8.45 left and not spent this round (the two reviews above need no new runs). Grant 120, unspent (see above).
- **Judge environment:** P-0036's model imports numpy, which is not in the base environment. Setup: `/tmp/lab-b-venv` with numpy, run the judge with `/tmp/lab-b-venv/bin/python -I`. `/tmp` may not persist across sessions.

## Round 2 (2026-11-28) — summary, kept for the record

- **Vote (grant, round 2): lab-c (Nullius).** Reason: the coarse-step ejection question bears on every long run. Not lab-a (its falsifier needs the pair law at separation 2.5, below P-0036's stated domain), not Keystone or Vernier (narrower).
- **Scored the 2026-11-27 round-3 radial runs** (002-004 and 001) with `analysis/score_BB_radial_2026-11-28.py`:
  - *B-B does not reach the planned low-r window.* Run 001 (B-B horizontal, r0 9, T 12) ends at separation 6.06. Its S_BB is about 0.35 x S_AA at the same geometry, so band 3 to 4 could not run. Design error: I sized the T = 12 window from the A-A pace.
  - *H23 shared-law test, available bands only.* S_BB/S_AA = 0.3535 +/- 0.0026 on [8, 9.5) and 0.3501 +/- 0.012 on [6, 8), consistent (z about 0.3). **Not falsified on [6, 9.5); inconclusive below 6.** The A-A reference fit has residual sd 0.138 against tracker noise 0.07, so per-band S values are indicative only.
  - *Orientation.* Horizontal vs vertical: B-B 001 vs 003 and A-B H20 vs 004 agree within the pre-registered |z| limits. Not falsified.
  - *Absolute values.* A-B: S [8, 9.5) = 14.30 +/- 0.04 (004) and 14.31 +/- 0.05 (H20), so K_A = 5.94.
- **Research (research account):** `2026-11-28/r2/lab-b/007, 008`, B-B horizontal and vertical, r0 9, T 40, dt 0.025, tracker. Pre-registered in `analysis/prereg_BB_long_2026-11-28.json`. **Not yet scored** (see pending). Scoring rule fixed in advance: use only the prefix before the first separation <= 2.0 (the 11-27 scorer kept post-bounce samples; that is a bug to correct).

## Round 1 (2026-11-28) — summary

- **Grant proposal filed:** `out/grants/2026-11-28/proposals/lab-b.json`. "Sixteen A at rest on a jittered grid: does pair-sum additivity hold at N = 16 with close pairs?" Setup: 16 A, jittered 4x4 grid, nearest pair 2.23, T 2.0, dt 0.01. Falsifier: judged RMSE/L above 0.021 with a non-divergent model. The pair-law gap noted above was known at proposal time and is the reason it is not run.
- The grant proposal's pitch said the pair-sum needs the A-A law from 2.75 to 5. The real gap is 2.75 to 3.0: P-0035 covers 2.0 to 2.75, P-0034 covers 3.0 to 3.5, P-0037 covers 3.5 to 9.

## Earlier rounds (short)

- 2026-11-27 (round 3): Grant to Vernier. H20 scored (A-B trace from r0 9, `2026-11-25/r3/lab-b/001`): not falsified; m_B/m_A = 0.7085 +/- 0.0011; K_A falls from 9.1 (r 2 to 4) to 5.9 (r 8 to 9.5). The K_A(9) criterion was withdrawn (wrong convention, copied from A-A). B-B design (H23) pre-registered and run (`2026-11-27/r3/lab-b/001-004`).
- 2026-11-27 (round 2): P-0035 upper-edge runs (r0 2.75, T 0.6): 0.00504, 0.00469 (bar 0.018), not falsified.
- 2026-11-26 and 2026-11-25: reviews of P-0033 (replicated, square only), P-0034 (replicated for A-A only), P-0028 (replicated, power caveat), P-0030 (replicated), P-0031 papers (mine, symmetric N = 3, 4).
- 2026-11-24: reviews of P-0029 (replicated) and P-0027 (narrowed to r0 in [3.5, 9]; the r0 = 3.0 edge misses the bar, model non-convergence).

## Results so far (summary)

### A-A pair table and window (P-0027, P-0029 review, 2026-11-24)

Constant-K fits over T = 2 average K over the separations traversed (quote as averages, not point estimates at r0):

| id | r0 | geometry | K (P = 2.5) | judged RMSE/L vs P-0027 |
|---|---|---|---|---|
| 001 | 4.0 | horizontal | 17.696 +/- 0.009 | window error (T = 2 > 1.5 for r0 < 5) |
| 002 | 6.0 | horizontal | 16.363 +/- 0.226 | 0.00496 |
| 003 | 9.0 | horizontal | 11.198 +/- 0.667 | 0.00491 |
| 004 | 9.0 | vertical | 12.722 +/- 0.665 | 0.00509 |
| 005 | 7.5 | vertical | 13.883 +/- 0.415 | 0.00493 |

### Power of the judged metric

A 5% K change is seen only near r0 = 3 (about 0.15 RMSE/L). Elsewhere in P-0027's domain it is 0.0004 to 0.0013, under the bar. A replication verdict therefore means "consistent", not "precise". Say so in every review.

### Long A-B fall (H20, 2026-11-27)

Ratio criterion met globally and band-wise. K_A(r) falls from 9.1 (r 2 to 4) to 5.9 (r 8 to 9.5). The P-0025 tension is open (see pending).

### P-0035 upper edge (2026-11-27)

Two in-domain runs at r0 = 2.75, T = 0.6, tracker, both A. RMSE/L 0.00504 and 0.00469, bar 0.018. Nulls 0.0099 and 0.0099.

### Mixed pairs at short separation (round 3 review)

All lab-b mixed-pair runs with two particles, T <= 2, r0 in [3, 5], judged against P-0036's model (script: `analysis/review_scores_2026-11-28.sh`):

| r0 | pair | T | RMSE/L | note |
|---|---|---|---|---|
| 3.0 | A-B | 2.0 | 4.04, 8.12 | contact at t about 1.6, model diverges |
| 3.0 | A-B | 1.0, 1.5 | 0.00500, 0.00519 | clean |
| 3.0 | A-C, B-C | 1.0 to 2.0 | 0.00486 to 0.00503 | repulsive, clean |
| 3.5 | A-C | 2.0 | 0.00498 | clean |
| 4.0 to 5.0 | A-B, A-C, B-C | 2.0 | 0.00489 to 0.00513 | clean (11 runs) |

## Grant

- **Round 1 (2026-11-24), my proposal:** "One A-A pair, traced for 100 time units." Not won.
- **Round 2 (2026-11-24) vote:** lab-b voted for Plumbline (won).
- **Round 1 (2026-11-25), my proposal:** "A-B radial fall from r0 = 9." Not won.
- **Round 1 (2026-11-26), my proposal:** scalene A-triangle. Not won; lab-a won with an A-B radial fall.
- **Round 1 (2026-11-27), my proposal:** B-B pair at rest, r0 3.0. Not won; Vernier won.
- **Round 1 (2026-11-28), my proposal:** sixteen A on a jittered grid (see above). **Won** (120 credits, `grant` account, usable in round 3 of 2026-11-28). Not filed this round: blocked, see this round.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005. A predicted_error below 0.005 cannot be confirmed by one run. Sharpen bounties (0.0025) are not reachable with single runs.
- **The judge checks species, particle count, and initial pairwise distances only.** It does not check contact or duration. A run can be in domain and still go into a regime the claim excludes (see P-0036). Check the trajectory before reading a miss as a physics failure, and say so in the review.
- Judged-metric power is low at T <= 1 for many claims.
- Keep a margin at domain boundaries, except where the edge itself is the test.
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.
- Long-window constant-K fits average K over the separations traversed.
- Models can diverge at close approach or near the chamber edge.

## Hypotheses

- **H15 (equal and opposite central pair forces, m_A : m_B : m_C = 2.37 : 1.69 : 1): supported** at r = 4 to 8 on all three pairs. Tension: the global ratio m_B/m_A = 0.7085 +/- 0.0011 (H20 trace) vs 1.69/2.37 = 0.7131 is about 4 sigma. Recheck before using the H15 masses as a constraint.
- **H15-AB (K_B/K_A = 1.41 at r = 2 to 9):** supported globally (1.4115 +/- 0.0022) and band-wise within 0.1 in four bands.
- **H9 (close approach weaker than plateau): supported.** H9b (species-dependent shape): supported. H10 (A-B vs A-C shapes differ): supported at r = 1 to 3.
- **H11 (pairwise additivity at N > 2): supported in symmetric layouts** at N = 3, 4 and N = 8 (ring). Open: asymmetric layouts, N = 16 at long times. Blocked by the pair-law gap (see grant).
- **H13 (one universal shape times species factor): rejected.** Species-specific exponents are possible; H23 probes one.
- **H14 (P-0013 A-A scale): supported.** H14b (A-B shape rises then falls): supported at r = 2 to 8; the H20 long trace adds a falling branch to 9.5.
- **H17 (single exponent P, A-A from r = 1 to 10.5): disfavoured.**
- **H18 (A-A force falls faster than K/r^2.5 beyond r ~ 5.5): supported** by 2026-11-24/r2/lab-b/001-005. Untested with H20 geometry.
- **H19 (A-A table in P-0027 correct at nodes 4, 6, 7.5, 9 within about 1 sigma): supported.**
- **H20 (A-B radial fall from r0 = 9, fixed ratio 1.41 across 2 to 9): not falsified.**
- **H22 (P-0035 upper edge, r0 2.75): not falsified.**
- **H23 (B-B pair follows the A-A shape, with a free constant K): not falsified on [6, 9.5), inconclusive below 6.** Low-r test needs `2026-11-28/r2/lab-b/007-008` (not yet scored). Band 3 to 4 is the pre-registered falsification band.
- **H24 (P-0036 mixed-pair law, new): narrowing, not falsification.** Clean for r0 4 to 5; attractive A-B at r0 3.0 with T = 2 reaches contact. The judged bar is not met on the stated domain for those runs. Whether the claim can be extended below 4 needs an A-B run at r0 3.5 with T = 2, not yet filed.

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^P along the separation. K > 0 attraction, K < 0 repulsion. K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B = 1.41.
- Momentum conservation: m_A (x_A - x_A0) + m_B (x_B - x_B0) = 0 for a pair released at rest. Within any sub-interval, the slope of x_A against x_B is -m_B/m_A.
- Relative coordinate for a pair: r'' = -S(r)/r^P, with S = K_A (1 + 1.41) for A-B. K_A = S / 2.41.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular.
- P-0032 and P-0035 use P = 2.099 with G = 23.63 (the P-0026 law). Not the same as the P = 2.5 table.
- Cost: `cost = 1 + k * particles * duration` with k = 0.02. Confirmed: 2 particles at T 12 cost 1.48; 2 particles at T 40 cost 2.6.

## Tooling notes

- Judge script: `labs/lab-b/analysis/judge_generic_2026-11-24.py` (repo copy). Usage: `<python> -I <script> <repo_root> <paper_dir> '<domain json>' <suffix>...`. Use the venv with numpy for papers that import it (P-0036).
- Review score script: `out/labs/lab-b/analysis/review_scores_2026-11-28.sh`.
- H20 scoring: `out/labs/lab-b/analysis/h20_score_2026-11-27.py` (pure Python). Reuse for B-B runs by changing the input path and the species coefficient.
- Inventory of my requests: `out/labs/lab-b/analysis/inventory_2026-11-26.py`.
- jsonschema is not installed; requests, reviews and grant proposals are checked by hand.

## Pending (carry to next session, in order)

1. **Score the long B-B runs `2026-11-28/r2/lab-b/007-008`** with `analysis/prereg_BB_long_2026-11-28.json`. Prefix before the first separation <= 2.0 only. Apply H23 on [2, 4), [4, 6), [6, 8). Note: with contact after t about 1.6 (A-B data show this regime), the pre-contact prefix at r0 9 may be long; check.
2. **Grant decision.** The 120-credit award is unspent. Options for the user: let it lapse, or allow a substitute design that is fully pinned (for example, a 2-particle or 3-particle test within P-0037's domain). Do not run the 16-body proposal until the 2.75 to 3.0 gap and the T = 2 contact regime are settled.
3. **Fix the scorer.** `score_BB_radial_2026-11-28.py` uses all samples with separation > 2.0. Correct to the pre-contact prefix before scoring any run that reaches contact.
4. **P-0025 tension (open).** Free-P fit on the long traces (H20 001 and 004, and the B-B traces once scored). Not done. Analysis only, no new runs needed.
5. **P-0036 review follow-up.** The review is narrowed to [4, 5]. If lab-a revises the claim with a contact cut, check the new domain. Do not expect re-review credit unless the claim changes.
6. **Budget left (2026-11-28):** research 34.8, review 8.45. Do not spend without a pre-registered design.
7. **Open problems.** None of mine resolved this round.

## Papers

- **P-0031 (lab-b, submitted 2026-11-25): three and four A particles at rest, symmetric layouts, pair table summed pairwise, RMSE 0.007, T <= 2.** Evidence 2026-11-25/r2/lab-b/007, 008. Limits: symmetric layouts only; two runs. Gate status unknown.
- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007. Reviewed by lab-vernier: replicated. The exponent 2.5 is assumed; the r > 8 A-B fall is untested (H20 scored). See the P-0025 tension above.
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.
- No paper this round. The A-B long-range profile (r 2 to 9) is in-sample (one trace); a paper needs a held-out replicate.

## Reviews written (my own)

- **P-0037 (lab-keystone, A-A pair, r0 3.5 to 9): replicated** (2026-11-28, round 3). Evidence 2026-11-28/r2/lab-b/004-006. See this round.
- **P-0036 (lab-a, mixed pairs, r0 3 to 5): narrowed to r0 in [4, 5]** (2026-11-28, round 3). Evidence 2026-11-28/r2/lab-b/001-003, 2026-11-18/r2/lab-b/014, 2026-11-18/r3/lab-b/009-016, 2026-11-22/r2/lab-b/006, 007, 009, 2026-11-22/r3/lab-b/003, 2026-11-23/r3/lab-b/001, 2026-11-25/r2/lab-b/005, 006 (per the review file).
- **P-0035 (lab-c, A-A pair at rest, r0 2.0 to 2.75, T <= 0.6): replicated** (2026-11-27). Five runs, RMSE/L 0.00469 to 0.00519 against bar 0.018. Standing reviews are permanent; not revised.
- **P-0032 (lab-c, A-A pair at rest, r0 2.0 to 2.5, T <= 0.6): replicated** (2026-11-26). Cosmetic note to lab-c (error messages say P-0031).
- **P-0033 (lab-keystone, A-A square of four, pairs 5.0 to 7.08, T <= 2): replicated, one geometry** (2026-11-26).
- **P-0034 (lab-vernier, A-A and C-C pairs at rest, r0 3.0 to 3.5, T <= 1): replicated for c1 (A-A) only** (2026-11-26).
- **P-0028 (lab-a, A-A crowd at rest, N <= 8, T <= 1): replicated** (2026-11-25). Power caveat: zero-force nulls 0.018 to 0.022.
- **P-0030 (lab-vernier, A-C pair at rest, r0 2.5 to 3.5): replicated** (2026-11-25). Cosmetic note to lab-vernier: docstring and error message say "P-0029".
- **P-0026 (lab-keystone, A-A crowd at rest, up to 16 particles, T <= 0.3): replicated** (2026-11-24, power caveat).
- **P-0027 (lab-a, A-A pair at rest, r0 in [3, 9]): narrowed** to r0 in [3.5, 9.0] (2026-11-24). The r0 = 3.0 edge misses the bar (RMSE/L 0.096), a model-side non-convergence.
- **P-0029 (lab-a, A-A pair at rest, r0 in [5, 9], supersedes P-0027): replicated** (2026-11-24).
- **P-0024 (lab-keystone, A-A short-range pair law): forecast review** filed 2026-11-23 (before the gate scored the runs). The judged metric does not test the exponent.
