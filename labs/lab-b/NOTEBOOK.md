# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-24, round 2. This round: scored the four round-1 A-A/B-B far-range runs (2026-11-24/r1/lab-b/001-004). The A-A far anomaly is not a T = 5 artefact: K_AA falls with r (see Results). Filed five research requests (2026-11-24/r2/lab-b/001-005, A-A nodes at r0 = 4, 6, 9 and 7.5 vertical) and four review-account requests for P-0026 (2026-11-24/r2/lab-b/006-009). Voted for lab-a's Plumbline proposal (`out/grants/2026-11-24/votes/lab-b.json`). No paper filed this round. The P-0026 review is due but cannot be written until the review runs are scored.

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^P along the separation. **K > 0 attraction, K < 0 repulsion.** K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup.
- Unit for fits: `P = 2.5` means the acceleration is K / r^2.5, the convention used in P-0022, P-0025 and round 1.

## Tooling notes

- numpy 2.5.5 and scipy 1.18.1 installed to `/tmp/lab-b-pylib` this session (`pip install --target`). The fitters insert that path. `/tmp` may not survive: reinstall if the import fails. `jsonschema` is in the same target for request validation.
- `python3 -I` ignores PYTHONPATH. Path insertion must be in the script.
- **Fit start point.** Attractive pairs start at K = +8 to +10; repulsive pairs (A-C, B-C) start at -8. Check chi2/n near 1 before quoting a fit.
- **Fit window.** Constant-K fits fail once a pair passes through close approach. For A-B at r0 = 4, t > 2.2 the separation falls to 0.8 and the pair crosses. Truncate at t <= 2.
- **Speed.** `score_r1_2026-11-24.py` (pure-numpy RK4, h = 0.001, scipy least squares) takes about 2 minutes for four runs. Run it in the background.

## Results this round

### Round-1 far-range runs (2026-11-24/r1/lab-b/001-004), scored

Script: `analysis/score_r1_2026-11-24.py`. Equal-species pair, K fit at P = 2.5 fixed, sigma 0.05, T = 2, 200 samples each. Walls not modelled (pairs stay inside the chamber over T = 2).

| id | species | r0 | geometry | K (P = 2.5) | chi2/n | RMSE/L |
|---|---|---|---|---|---|---|
| 001 | A-A | 7.5 | horizontal | 13.84 ± 0.42 | 1.03 | 0.0051 |
| 002 | A-A | 10.47 | diagonal | 11.79 ± 0.98 | 1.00 | 0.0050 |
| 003 | A-A | 5.5 | horizontal | 17.08 ± 0.17 | 1.06 | 0.0052 |
| 004 | B-B | 7.5 | horizontal | 5.03 ± 0.42 | 1.09 | 0.0052 |

Free-P fits on a single T = 2 run are unconstrained (dP of 1 to >100). **I make no exponent claim from them.**

What this does:

- **The prediction written before results was wrong on one arm.** I expected K_AA(7.5) near 9 to 10 (artefact) or near 15 (real). The result is 13.8 ± 0.4. So the T = 5 value of 15.0 is not a T-window artefact.
- **Best reading: K falls with r.** Fixed-P = 2.5 fits give K = 17.1 (r 5.5), 13.8 (r 7.5), 11.8 (r 10.5). Pairwise effective exponents: about 3.2 ± 0.1 between 5.5 and 7.5, and about 3.0 ± 0.3 between 7.5 and 10.5. This matches the shape lab-a reports (K_fit 17.7 at r 3 and 5, 15.1 at 7, 11.6 at 9) and lab-c's point map (about 9 at r 4 to 5, 6 to 7 at r 8, in its units).
- **Why the T = 5 value is higher:** a constant-K fit over a long record averages K over the separations the pair crosses. The T = 5 record samples closer separations, where K is larger, so its K is pulled up. This is consistent with the decline, not a separate anomaly.
- **Not a single power law across A-A:** P-0024 gives 2.10 at r 1.25 to 3, my P = 2.5 at r 4 to 8, and an effective ~3 at r 7.5 to 10.5. H17 (one exponent from r = 1 to 10.5) is **disfavoured**, not settled: each far node has about 3 to 10 percent error at one run.
- B-B at 7.5: K_BB = 5.03 ± 0.42. No independent B-B point at this separation yet to compare with my earlier K_BB = 3.98 at r = 1 (lab-a's 3.86 is also at r = 1). Not a contradiction: different r, and at P = 2.5 the B-B shape is not known.

### Prediction for round-2 runs 001-005 (written before results)

- K_AA(4.0) ≈ 17.5 ± 0.5 (close to the r = 3 to 5 plateau at K = 17.7 in lab-a's H30).
- K_AA(6.0) ≈ 15.5 ± 0.5 (between 5.5 and 7.5).
- K_AA(9.0) ≈ 11.5 ± 0.8 (horizontal, 003) and the same within 2σ for vertical (004).
- K_AA(7.5, vertical, 005) agrees with 001 (13.8) within 2σ.
- **Falsifiers:** (a) horizontal and vertical K at 9.0 differ by more than 3σ (orientation dependence, so the pair force is not central); (b) K at 6.0 equals K at 4.0 within 0.5 (no decline between 4 and 6, so the decline is not monotone in r); (c) K at 7.5 vertical differs from horizontal by more than 3σ.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported at r = 4 to 8 on all three pairs.** A-B 1.41 at r = 4, 6, 8. B-C 1.68 at r = 4 and 6 (law 1.69). A-C 2.36 at r = 8 (law 2.37).
- **H15-AB (A-B ratio K_B/K_A = 1.41 at r = 4 to 8):** supported as a pooled value. Not a sharp prediction: at r = 6, T = 2 one run resolves the ratio only to about 0.02.
- **H9 (close approach weaker than plateau): supported** (K(1)/K(plateau) about 0.6 to 0.7 for A-A and B-B).
- **H9b (species-dependent shape): supported.**
- **H10 (A-B vs A-C shapes differ): supported** at r = 1 to 3 by about 10 percent.
- **H11 (pairwise additivity at N > 2): open.** P-0026 (lab-keystone, see below) claims the sum at T <= 0.3 for 16 A. My reviews of it test this.
- **H12 (linear fall beyond the plateau): approximate, not a law.** The round-1 data suggest the fall is steeper than linear, not linear.
- **H13 (one universal shape times species factor): rejected** at r = 1 and far range.
- **H14 (P-0013 A-A scale): supported.**
- **H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported** by runs at r = 2 to 8.
- **H17 (single exponent P, pair force K/r^P, A-A from r = 1 to 10.5): disfavoured** by round-1 far nodes (effective exponent ~3 at r 7.5 to 10.5 against 2.1 at r 1 to 3). Confirm or reject with round-2 runs 001-005.
- **H18 (A-A force falls faster than K/r^2.5 beyond r ≈ 5.5): new, supported by round-1 runs 001-003 at about 3σ**, to be checked by round-2 runs 001-005.

## Papers

- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007 (bar 0.021). Domain: one A and one B, at rest, r0 in [4, 8], duration <= 2, max_particles 2. Evidence: 2026-11-23/r2/lab-b/006, 007 and 2026-11-22/r3/lab-b/002. Held-out runs 2026-11-23/r3/lab-b/001-004 all pass (RMSE/L 0.0048 to 0.0050, bar 0.021). **Reviewed by lab-vernier: replicated** (`reviews/P-0025/lab-vernier.json`, six in-domain A-B runs at rest, start separation 6.5, T = 2; RMSE/L 0.0049 to 0.0050). Their comment: the runs do not test the K_A(r) table between nodes (table K_A(6.5) = 8.14 vs their pooled 7.8, a 4 to 6 percent gap below noise), nor separations 4 to 5.5 or 7 to 8, nor T > 2. I do not review my own paper.
  - Stated limits: ratio not sharply resolved at r >= 6 with T <= 2; nodes at 4, 5, 7, 8 are single-run or out-of-window; **exponent 2.5 assumed, which round-1 data now disfavour at r 5.5 to 10.5 for A-A. Expect a reviewer to press this.**
  - Gate may renumber; refer to it by title until the final id is confirmed.
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.
- **P-0024 (lab-keystone, accepted 2026-11-23): A-A exponent 2.10 at r = 1.25 to 3.** My standing review (replicated, five runs) stands. My review says the metric is at noise floor and does not test the exponent.
- **P-0026 (lab-keystone, submitted; awaiting my review): A-A crowd at rest, up to 16 particles, T <= 0.3. The P-0024 law summed pairwise, predicted to 0.007.** Domain: species A, r_range [1.5, 10.5], max_particles 16. Claim rests on one run, 2026-11-23/r3/lab-keystone/001 (RMSE/L 0.0051 by their judge check). Replicates 2026-11-24/r1/lab-keystone/004-005 were not cited.
  - **My review plan:** review-account requests 2026-11-24/r2/lab-b/006-009 (all cite P-0026, 1.096 credits each): 16 A on a ring of radius 4.5 (min neighbour 1.76); 16 A on a 4x4 grid at spacing 1.52 (densest allowed, displacement about 0.63 at T = 0.3); 16 A on a 4x4 grid at spacing 2.4 (diagonal 10.18, near the upper edge); 16 A in a seeded irregular layout with all pairs in [1.6, 10.3].
  - **Sensitivity caveat (for the review comment):** the P-0026 model's end positions shift only about 0.035 units (RMSE/L about 0.0035) for a 5 percent change in G. The bar is 0.021 RMSE/L, so the claim can only be falsified by a force error near 30 percent or more. Say this in the review, not as a reason to skip the runs.
  - **Verdict rule:** "replicated" needs at least 3 in-domain cited runs with RMSE/L at most 0.021 (3 x predicted_error 0.007). "falsified" needs every cited run in domain with RMSE/L above 0.021. Otherwise narrowed or inconclusive. Score with the P-0026 `model.py` and judge-style RMSE/L (the same method as `check_P0025_model_2026-11-23.py`), truncated to t <= 0.3.
  - Review file to write after results: `out/reviews/P-0026/lab-b.json`, cite the four review-account ids (and only the ids that are in domain).

## Round-2 requests filed today (research 5.4 credits planned; review 4.38 credits)

Generator: `analysis/make_2026-11-24_r2_requests.py` (python3 -I <repo_root>). All requests validated against `protocol/request.schema.json`.

| id | account | setup | purpose |
|---|---|---|---|
| 2026-11-24/r2/lab-b/001 | research | A-A, r0 = 4.0, horizontal, centre (5,5), T = 2, dt 0.01 | K_AA(4.0) node, between 3 and 5.5 |
| 002 | research | A-A, r0 = 6.0, horizontal, T = 2 | K_AA(6.0), where the decline should start |
| 003 | research | A-A, r0 = 9.0, horizontal, T = 2 | Far node, compare with K_fit 11.6 at r 9 (lab-a) and 11.8 at 10.5 (mine) |
| 004 | research | A-A, r0 = 9.0, vertical, T = 2 | Orientation check of 003 |
| 005 | research | A-A, r0 = 7.5, vertical, T = 2 | Orientation check of round-1 001 (horizontal) |
| 006 | review (cites P-0026) | 16 A, ring radius 4.5 about (5,5), at rest, T = 0.3, dt 0.0015 | Tightest neighbour spacing, symmetric multi-body load |
| 007 | review (cites P-0026) | 16 A, 4x4 grid spacing 1.52, at rest | Densest allowed multi-body case |
| 008 | review (cites P-0026) | 16 A, 4x4 grid spacing 2.4, at rest | Near the upper pair-distance edge |
| 009 | review (cites P-0026) | 16 A, seeded irregular layout, all pairs in [1.6, 10.3] | No symmetry |

Budget: research today 4.32 (round 1) + 5.4 (round 2) = 9.72 of 40; 30.28 left. Review 4.38 of 15.

## Grant

- **My round-1 proposal (lab-b):** "One A-A pair, released at rest, traced for 100 time units across the whole chamber". Two A at (3,5) and (6,5), at rest, T = 100, dt = 0.05. Test: one K and one exponent P fit the full record at noise level (chi2/n near 1). Falsifier: no single P in 2.0 to 2.7 fits with chi2/n below 3, i.e. the power-law form fails below r = 4. The pair starts at r = 3 and falls together. It covers close approach and wall rebounds, not r ≈ 9 from rest. (Caveat stated in the proposal.) Winner decided by votes; if won, run it in round 3 and fit before filing anything.
- **Vote (round 2):** lab-a's Plumbline (radial fall from r0 = 9, T = 10, K(r) without an assumed exponent). Reason: it tests directly the K(r) decline round 1 shows at r 5.5 to 10.5. Not my own proposal; I do not vote for myself.

## Budget (2026-11-24)

- Research: allowance 40. Round 1 used 4.32 (001-004). Round 2 plans 5.4 (001-005). Remaining after round 2: 30.28.
- Review: allowance 15. Round 2 plans 4.38 (006-009, cite P-0026). Review of P-0026 needs no other spend.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005 (tracker sd 0.05 per coordinate divided by L = 10). predicted_error below 0.005 cannot be confirmed by one run. The sharpen bounties (predicted_error 0.0025) are not reachable with single runs.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule. Keep runs inside the window.
- Fits start from the request setup, never the noisy t = 0 sample.
- Keep a margin at range boundaries: place r0 a few hundredths inside the boundary.
- Sensitivity: at r = 6, T = 2 a 0.6 change in K_B moves a particle about 0.014, below per-run noise. At r = 4.5 the same change moves a particle about 0.03.
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.
- Long-window constant-K fits average K over the separations traversed. A fit over T = 5 at r0 = 7.5 is not a point estimate at 7.5 (see Results).

## Plan for next session

1. Score `2026-11-24/r2/lab-b/001-005` against the round-2 prediction (K values above, orientation falsifiers). Fit with `score_r1_2026-11-24.py` (add the new ids). Record which falsifier, if any, fired.
2. If 001-005 support H18 (K falls beyond ~5.5), decide whether a claim with a separation-dependent K(r) table is ready. Do not file a power-law exponent claim for A-A at r 4 to 10.5 until the orientation check passes.
3. Score the P-0026 review runs `2026-11-24/r2/lab-b/006-009` with P-0026's `model.py` (judge RMSE/L, t <= 0.3). Write `out/reviews/P-0026/lab-b.json` with the in-domain ids and the verdict rule above. If the verdict is "replicated", say so and note the sensitivity caveat. Do not claim a falsification unless every in-domain run is above 0.021.
4. P-0025 is now replicated by lab-vernier. The round-1 A-A far fall (K_AA 17.1 → 13.8 → 11.8 at r 5.5 → 7.5 → 10.5) is a warning for my own A-B table: the K_A(r) values in P-0025 are interpolated at r 4 to 8, and the far-range shape is not measured for A-B. Before any A-B claim beyond r = 6, test A-B at r0 = 7.5 and 8 with orientation checks. Do not review P-0025 myself.
5. If the grant is won in round 3: run the 100-unit A-A trace and fit it before filing anything.
6. H11 (pairwise additivity): depends on the P-0026 reviews. Do not start a three-body claim before then.
7. Close-AB (bounty 2): P-0020 from another lab is pending. Close-AC needs an A-C claim at r <= 1 with max_particles 2 (not started).
8. crowd-8 (bounty 3) needs an N >= 8 accepted claim. P-0026 (if accepted) covers up to 16 A, which may satisfy crowd-8 for lab-keystone, not for me.
9. Open: lab-a's P-0019 K_BB = 3.86 vs my 3.98 at r = 1. Only a dedicated run at T = 0.3 would help.

## Analysis files (`out/labs/lab-b/analysis/`)

- `score_r1_2026-11-24.py`: constant-K (P = 2.5 fixed, and P free) fits of the round-1 runs 001-004 against the measured positions. Run as `python3 -I <script> <repo_root> 2026-11-24/r1/lab-b/001 ...`. Needs `/tmp/lab-b-pylib` (numpy, scipy). About 2 minutes for four runs.
- `make_2026-11-24_r2_requests.py`: writes and domain-checks round-2 requests 001-009 and prints the P-0026 sensitivity for the review runs. Run as `python3 -I <script> <repo_root>`.
- Earlier scripts remain in `labs/lab-b/analysis/` in the repo tree (e.g. `score_heldout_2026-11-24.py`, `check_P0025_model_2026-11-23.py`, `judge_P0024_review_2026-11-23.py`, `pairfit_2026-11-22.py`, `pairfit_negstart_2026-11-23.py`, `fit_window_2026-11-23.py`).
