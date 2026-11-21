# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Budget ledger

### Closed days
- 2026-11-17: research used 23.30 of 40; review 6.00.
- 2026-11-18: research used 30.38 of 40; review 6.20 (review of P-0002).
- 2026-11-19: research used 13.12 of 40; grant award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100, no census events). Voted lab-keystone.
- 2026-11-20: research used 9.19 of 40 (rounds 1 to 3, incl. `r3/002` to `005`); review 13.90 of 15 (`r1/005-009` on P-0008; `r3/006-012` on P-0010 and P-0011); grant 1.02 of 120 (`r3/001`, C-C at r0 2). Voted lab-keystone.

### 2026-11-21 (this session, round 1)
- Research: nine requests `r1/001-009` (out/requests/2026-11-21/r1/lab-a/). Estimated cost 9.06 of 40 (k = 0.02, cost = 1 + k N T; to be confirmed from result costs). Remaining 30.9 unused unless round 2 or 3 spends it.
- Review: no new review runs. Both reviews filed today use existing 2026-11-20 results. Review allowance for today (15) is unused.
- Grant: proposal filed (`out/grants/2026-11-21/proposals/lab-a.json`, 9 A particles, 3x3 grid at spacing 3.5). Estimated cost about 1.09 of the 120 award when run.

## Established (accepted-level claims, or runs I trust)

Pair coefficients at separation 5 (P-0005, accepted; K_XY = acceleration coefficient of species X toward Y, P = 2.5):

| pair | K (species in first slot, on the second) | runs | status |
|---|---|---|---|
| A-A | 18.0 | P-0003 (domain sep 3 to 6) | established at sep 3 to 6; not valid at sep 1 (see below) |
| A-B | 8.99 (A on B), 12.34 (B on A) | replicated | |
| A-C | -8.77 (A on C), -21.25 (C on A) | replicated, repulsion | |
| B-B | 6.12 | 4 values, spread about 9% | |
| C-C | 12.36 | 4 values, spread about 5% | |
| B-C | -6.10 (B on C), -10.59 (C on B) | pre-registered prediction passed | |

Other established results:
- Free flight with specular walls (P-0001, P-0002): A, B, C at speeds up to 8.6, T up to 100, corner hits. Supported.
- Isotropy at separation 4 (A-A along diagonal, y, horizontal): K = 17.67, 17.71, 17.70. Supported.
- Pairwise additivity for three and four particles at separations 3 to 5 (T <= 1): at noise level.
- Shared distance law at separations 7 and 9 (P-0006): within about 5%, qualified by the close-range results below.
- No census event (decay or appearance) in about 50 runs, including 16 particles at T = 100.
- Cost law cost = 1 + 0.02 N T: supported at N = 1, 2, 3, 4, 16.

## Close range (new this session)

### A-A is not constant-K below separation 2 (H14: refuted at r0 1.5 to 2.0; K falls further at r0 = 1.0)
Fits: one coefficient K, P = 2.5 fixed, least squares on the measured separation at every sample. Initial separation taken from the request setup, not from the noisy first sample.

| run | pair | r0 | T | K_fit | K_fit / K_flat - 1 | rms_sep (noise floor 0.071) |
|---|---|---|---|---|---|---|
| 2026-11-20/r1/lab-a/001 | A-A | 2.0 | 0.5 | 15.6 | -0.13 (vs 18.0) | 0.069 |
| 2026-11-20/r1/lab-a/002 | A-A | 2.0 | 0.5 | consistent with 001 (0.005 per bin) | | |
| 2026-11-20/r1/lab-a/003 | A-A | 1.5 | 0.3 | 14.0 | -0.22 | 0.070 |
| 2026-11-20/r3/lab-a/003 | A-A | 1.0 | 0.15 | 11.52 | -0.36 | 0.072 |
| 2026-11-20/r3/lab-a/004 | A-A | 1.0 | 0.15 | 11.05 | -0.39 | 0.070 |

- The two replicates at r0 = 1.0 agree to 4%. Both separation profiles sit at the noise floor.
- K_eff(r0) for A-A, P = 2.5 fixed: about 11.3 at r0 = 1.0, 14.0 at 1.5, 15.6 at 2.0, 17.7 at 4, 18.0 at 5, 16.5 at 6, 11.7 at 9 (earlier fits). It is not constant below separation 3.
- The power-law shape is not tested at r0 = 1.0: the separation changes only by about 0.3 in T = 0.15, so P and K are not separately determined.
- P-0003 (A-A, domain separation 3 to 6, K = 18.0) is not contradicted: its domain excludes these runs.

### Noise extremes, not collisions
Minimum separation over a noisy profile is biased low. Runs 2026-11-20/r3/003 and 004 have sample minima of 0.58, but the model's own minimum separation over T = 0.15 is 0.71. Do not read a sample minimum as a collision distance.

### B-B at r0 = 2 (replicated, about 9% below the separation-5 value)
| run | K_fit | K_fit / 6.12 - 1 |
|---|---|---|
| 2026-11-20/r1/lab-a/004 (earlier) | 5.70 | -0.07 |
| 2026-11-20/r3/lab-a/005 (replicate) | 5.42 | -0.11 |

- Pre-registered rule (flat if within 5% of 6.12; low-replicated if within 5% of 5.70): the replicate sits 4.9% below 5.70. Result: low-replicated, at the edge of the band. B-B at r0 = 2 is about 9% below the separation-5 value (pooled ~5.56). No claim published (replicate only at the edge of the rule).

### C-C: deviation from 12.36 across separations 2 to 5 (not monotonic, not established as flat at 5%)
| run | r0 | K_fit | K_fit / 12.36 - 1 |
|---|---|---|---|
| 2026-11-20/r2/lab-a/001 | 3 | 13.05 | +0.056 |
| 2026-11-20/r3/lab-a/002 (replicate) | 3 | 13.13 | +0.062 |
| 2026-11-20/r3/lab-a/001 (grant) | 2 | 12.01 | -0.028 |

- Two runs at r0 = 3 agree within 1% and sit 6% above 12.36. Not noise, but below the 10% refutation threshold of the pre-registered rule. Result: inconclusive (between the 5% and 10% bounds).
- The grant at r0 = 2 gives 12.0, not the 12.5 to 13.5 I expected if the r0 = 3 trend continued. Not below 11.7 either, so not a surprise. Single run.
- C-C K over separations 2 to 5 spans 12.0 to 13.1, about 9%. Flat at the 5% level is not established. P-0008 c2 (flat C-C coefficients at 3 to 5) is not refuted (threshold for narrowing 10%) but its 5% flatness is not confirmed at separation 3.

### Scale test on P-0008 (earlier session, unchanged)
Fit of one scale s to each review run: 005 1.021, 006 0.991, 007 1.079 (C-C at 3; C-B at 4 and 5), 008 0.995, 009 1.017. Run 007 is consistent with the C-C short-range excess above.

## Reviews filed today

- **P-0010** (lab-keystone, shared radial factor for r0 6 to 9, T <= 6): verdict **narrowed**, evidence `2026-11-20/r3/lab-a/006-009`, proposed_domain = the paper's own (schema cannot state a T or collision limit; narrowing stated in the comment).
  - Bulk runs replicate: 006 (C-C, r0 9) error/L 0.0071; 007 (A-A, r0 7.5) 0.0077; 008 (B-B, r0 6) 0.0072. Bar 3 x 0.01 = 0.03.
  - Run 009 (A-A, r0 6, T 6) fails: error/L 0.195. Measured minimum separation 0.028 at t = 4.26; the point-force predictor has no collision and passes the particles through each other.
  - Verdict chosen: narrowed, not replicated. Three in-domain passes would satisfy the replicated rule, but run 009 is inside the claim's stated domain and fails it by a factor of about 6 over the bar. The claim as written does not hold across its domain.
- **P-0011** (lab-vernier, tracker noise sd 0.050, no clipping): verdict **replicated**, evidence `2026-11-20/r3/lab-a/010-012` (one run per species, all error/L 0.0071 to 0.0072 vs bar 0.015).

## Paper filed today

- **P-0012** (out/papers/P-0012/, pending gate numbering): close-range A-A pair at rest, r0 = 1.0 exactly, T <= 0.15, K = 11.3, P = 2.5, predicted error 0.008. Domain: species [A], r_range [1.0, 1.0], max_particles 2. Evidence `2026-11-20/r3/lab-a/003` and `004`. Predictor error on both runs 0.0071 and 0.0071 (noise floor). Cites P-0003.
  - Rationale: the notebook's rule to publish close-AA once two replicates agree within 5% and K is stable. Both conditions hold at r0 = 1.0. The domain is one separation, because K changes with r0.
  - Bounty fit: close-AA asks for an A-containing claim with max_particles >= 2 and r_range starting at 1 or less. This claim qualifies if accepted.
  - Not claimed: any other separation; P (shape); mixed species.

## Round-1 pre-registrations (written before any round-1 result)

Requests `out/requests/2026-11-21/r1/lab-a/001-009` (script `analysis/make_2026-11-21_r1_requests.py`):

| request | run | r0 | T | pre-registered K | rule |
|---|---|---|---|---|---|
| 001, 002 | B-B | 1.0 | 0.3 | 4.0 (ratio to K_AA(1.0) = 11.3 is 0.35, from B-B/A-A at 2 and 5) | within 10% of 4.0 supports constant ratio; outside is a finding |
| 003, 004 | C-C | 1.0 | 0.15 | band [8.0, 9.6] (ratio to K_AA(1.0) of 0.71 to 0.85, from C-C/A-A at 2, 3, 5) | inside the band supports the ratio trend; outside is a finding |
| 005, 006 | A-A | 1.25 | 0.15 | 12.5 (linear between K(1.0) = 11.3 and K(1.5) = 14.0) | within 5% supports the interpolation |
| 007, 008 | A-A | 0.85 | 0.12 | band [9.5, 11.5] (extrapolated) | inside the band supports the trend; below 9.5 is a larger deficit (finding); flat 18 refuted if K_fit < 13.3 |
| 009 | A-A, diagonal, centred (3,3) | 1.0 | 0.15 | 11.3 | within 5% supports isotropy at close range |

- Expected sign: all K below their separation-5 values (C-C near 12.36 at r0 = 2 to 3 is the exception that the 003, 004 band tests).
- Collision risk: at r0 = 0.85 and T = 0.12 the model's minimum separation is about 0.4. The run is shortened to keep clear of collision.

## Grant (round 1, filed today)

- `out/grants/2026-11-21/proposals/lab-a.json`: nine A particles on a 3x3 grid, spacing 3.5 (positions 1.5, 5.0, 8.5), at rest, T = 0.5, dt 0.005 (100 samples), tracker and census.
- Pre-registered prediction: pairwise sum of the flat A-A law (K = 18.0, P = 2.5), computed by `analysis/make_2026-11-21_grant.py` into `analysis/pred_grant_2026-11-21.json`. Model minimum pair separation over T = 0.5 is 3.30.
- Rule: RMSE/L of the pairwise-sum model at most 0.01 supports additivity at N = 9 (noise floor 0.007); above 0.02 refutes the flat law at 3.5 to 7 or pairwise additivity.
- Rationale: this tests the flat law and additivity at N = 9 in a regime where every pair is at or above 3.5, which is where our data is cleanest. It also bears on crowd-8, since N = 9 covers an 8-particle subset.
- Cost: 1 + 0.02 x 9 x 0.5 = 1.09, a small fraction of the 120 award. The award is not required to be spent.

## Analysis code (`out/labs/lab-a/analysis/`, my files)

- `eval_2026-11-21.py`: (1) evaluates the review runs `2026-11-20/r3/lab-a/006-012` against P-0010 and P-0011 model.py, editor metric. (2) Separation-profile K fit for the close-range and grant runs. Usage: `python3 -I eval_2026-11-21.py <repo_root>`. Writes `fits_2026-11-21.json`.
- `check_P0012_2026-11-21.py`: predictor error on runs 003 and 004 for P-0012. Usage: `python3 -I check_P0012_2026-11-21.py <repo_root>`.
- `make_2026-11-21_r1_requests.py`: writes the round-1 requests 001-009.
- `make_2026-11-21_grant.py`: writes the grant pre-registration prediction.
- Earlier scripts from 2026-11-17 to 2026-11-20 are in `labs/lab-a/analysis/`.

## Errors caught this session

- **r0 from the first measured sample.** My first version of the separation fit took the initial separation from the noisy first sample (about 0.07 noise), which shifted K by 10 to 20% (C-C at 3 showed K 10.9 instead of 13.05). Fixed: the fit now uses the setup separation. Lesson: the true initial state comes from the request, never from a measurement.
- **Sample minimum read as collision.** The 0.58 minimum in the close-range runs is a noise extreme. Use the model's minimum, not the sample minimum, for any collision check.

## Pending results and plan for the next session

1. When the round-1 results (`results/2026-11-21/r1/lab-a/001-009`) arrive, apply the pre-registered rules in the table above. Check each run's cost against the estimate.
2. Grant: when the award is confirmed, the main-event run is in round 3. Apply the grant rule.
3. P-0012 (close-AA): wait for the gate's paper number and any reviews. Do not add a second claim on the same runs.
4. Close-BB and close-CC: publish only after two replicates agree within 5%, as for close-AA. The round-1 requests 001-004 are that test.
5. Close-AB, close-AC, close-BC: mixed pairs need per-particle K fits (K_ij and K_ji separately). Not attempted yet. Do not claim until a per-particle fit is in hand.
6. Reviews: none pending for lab-a today. Keep the review allowance (15) for runs that cite a paper the lab is reviewing.

## What would change my mind

- Round-1 A-A at r0 = 1.25 with K within 5% of 12.5: the close-range K is a smooth function of r0 and the close-AA claim can be widened to a table.
- Round-1 A-A at r0 = 0.85 with K below 9.5: the deficit grows steeply below 1.0. The close-AA domain stays at one separation.
- Round-1 B-B and C-C at r0 = 1.0 each near their predicted K: the close-range ratio is roughly constant across species, and the close-AB, close-AC and close-BC claims can use one ratio plus a per-pair measurement.
- Grant with RMSE/L at most 0.01: the flat A-A law and pairwise additivity hold at N = 9 with separations 3.5 to 7. That supports a crowd claim (crowd-8), at the cost of a larger model.
- Grant above 0.02: the flat law or additivity fails at 3.5 to 7, and P-0003's domain (3 to 6) is suspect.
- A census event in any run: H4 refuted.

## Self-criticism

- The round-1 close-range rule (whole-run rms) previously passed a prediction the separation profile refuted. Future rules test the separation profile, with the true r0.
- The C-C deviation at r0 = 3 (+6%) is reproducible, but I report it as inconclusive, not as a finding, because it sits between the bounds.
- The grant at r0 = 2 (C-C) gave K = 12.0, against an expected 12.5 to 13.5. I have one run, and I did not repeat it. It stays a single data point.
- Run 009 of P-0010 is my test that the claim fails in its stated domain. I chose narrowed over replicated because the claim covers that case. Replicated would have been defensible under the letter of the rule, but not under its purpose.
- The B-B r0 = 2 rule is at its edge (4.9% against 5%). I report low-replicated with that caveat, not a claim.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2 to 8.6. Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 16.
- H4 no decay: no event in any run to date (about 50 runs).
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported at separations 3 to 9 as a shared-scale law. Close range (1.0 to 2): P = 2.5 fits the shape but the strength is lower for A-A (H14). P not tested at r0 = 1.0 alone.
- H8 pair force identical for all species pairs: refuted at sep 5 (coefficients differ).
- H9 coupling factorises as g_ij = q_i q_j: partially supported. C-C misses at sep 5 by about 20%; at sep 3 it is +6% (two runs, inconclusive). Not claimed.
- H10 isotropy at separation 4: supported. Isotropy at r0 = 1.0 (request 009): pending.
- H11 shared distance law: supported within about 5% at sep 7 and 9 (P-0006). Qualified by H14.
- H12 pairwise additivity for three and four particles at separations 3 to 5: supported at T <= 1 at noise level. N = 9 at spacing 3.5: pending grant.
- H13 no census events in a crowded long run: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: refuted for A-A at r0 = 1.0 to 2.0 (K 11.3 to 15.6 vs 18). Close-AA claim P-0012 restricted to r0 = 1.0.
- H15 A-A constant-K at r0 = 1.0: refuted (K = 11.3, not 18). Replicated at 4%.
- H16 (new) B-B and C-C ratio to A-A constant at close range: pending round-1 requests 001-004.

## Papers
- P-0005 (sep-5 pair table, accepted), P-0006 (distance-law scaling at 7 and 9), P-0007 (N = 3, side 5), P-0009 (B-C-C at side 5, T = 2): accepted or other labs' papers as recorded in the scoreboard.
- P-0003 (A-A power law, domain separation 3 to 6, T up to 2): not falsified. Its domain excludes the close-range runs.
- P-0012 (filed today, pending): close-range A-A at r0 = 1.0, K = 11.3.
