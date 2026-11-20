# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Budget ledger

### 2026-11-17, 2026-11-18, 2026-11-19 (closed)
- 17: research used 23.30 of 40; review used 6.00.
- 18: research used 30.38 of 40; review used 6.20 (review of P-0002).
- 19: research used 13.12 of 40 (rounds 1-3); grant account: award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Votes: lab-keystone.

### 2026-11-20 (this date)
- **Round 1** (earlier session): research `001-004` (4.07); review `005-009` on P-0008 (5.34); grant proposal filed (C-C at separation 2.0, T = 0.5, cost 1.02).
- **Round 2** (earlier session): research `2026-11-20/r2/lab-a/001` (C-C at separation 3.0, T = 1), cost 1.04. Result confirms budget_remaining 34.89 before it. Vote: lab-keystone (`grants/2026-11-20/votes/lab-a.json`).
- **Round 3** (this session), requests in `out/requests/2026-11-20/r3/lab-a/`:
  - Research (4.07 of 34.89 left): `002` replicate of `r2/001` (C-C, separation 3, T = 1), 1.04; `003`, `004` A-A at separation 1.0, T = 0.15, 1.006 each; `005` replicate of `r1/004` (B-B, separation 2, T = 0.5), 1.02.
  - Grant (1.02 of 120): `001` = the filed proposal, unchanged (C-C at separation 2.0, T = 0.5, 1000 samples, pre-registered prediction 1.370).
  - Review (8.56 of 9.66 left, `cites_paper` set): `006-009` on P-0010 (keystone), `010-012` on P-0011 (vernier).
- Totals after round 3, if all run: research 9.18 of 40 (30.82 unused, lost at close); review 13.90 of 15 (1.10 left); grant 1.02 of 120 (118.98 unused, lost at close).
- Note on the grant: the filed design costs 1.02 of the 120 award. I kept the proposal unchanged because other labs voted on it. The rest of the award goes unused. This is a choice to flag, not an oversight.

## Established

### Cost constant (H3): supported at N = 1, 2, 3, 4, 16
- k = 0.02. Every result matches `1 + 0.02 N T`. Confirmed again by `r2/001`: N = 2, T = 1 gives cost 1.04.

### Tracker noise: about 0.05 per coordinate
- Review runs 005-009 (P-0008 review) against its model: per-coordinate RMSE 0.0481-0.0511.
- Earlier: residual rms 0.047-0.053 on runs that fit their model.

### Pairwise additivity for three and four particles (H12): supported at separations 3-5, T = 1, at noise level
- P-0007 (N = 3, side 5), P-0009 (B-C-C, side 5, two runs), lab-b's P-0008 (N = 3 and 4, separations 3-5, reviewed by me as replicated; see Reviews).
- Caveat: the C-C pair at separation 3 is 5.6% stronger than the separation-5 value (see C-C below). P-0008's flatness claim for C-C is not established at the 5% level.

### Pair coefficients at separation 5, at rest, T = 2 (P-0005, replicated)
Acceleration on particle i = K_i / r^2.5 toward the partner for K > 0 (negative = repulsion). Chamber and time units.

| pair | particle | run means | runs | status |
|---|---|---|---|---|
| A-A | A | 18.0 | P-0003 (2026-11-17 r3/005-006) | established at sep 5; see close-range below |
| A-B | A (on B) | 8.99 | 8.82 / 9.16 | replicated |
| A-B | B (on A) | 12.34 | 12.39 / 12.28 | replicated |
| A-C | A (on C) | -8.77 | -8.60 / -8.94 | replicated, repulsion |
| A-C | C (on A) | -21.25 | -21.38 / -21.12 | replicated, repulsion |
| B-B | B | 6.12 | 5.60, 6.28 (r1); 5.85, 6.75 (r2) | 4 values, spread about 9%; not pooled |
| C-C | C | 12.36 | 12.34, 12.70 (r1); 12.31, 12.08 (r2) | 4 values, spread about 5% |
| B-C | B (on C) | -6.10 | -5.93 / -6.27 | pre-registered prediction passed |
| B-C | C (on B) | -10.59 | -10.65 / -10.53 | pre-registered prediction passed |

Published as P-0005 (separation 5 only). Unchanged.

### Close range (H14): constant-K power law fails at separation 1.5-2 for A-A (round 2 finding)
Runs (all: two particles at rest, centred at (5,5), tracker + census, 0 census events):

| run | pair | r0 | T | pre-reg K | rms per coord vs pre-reg | separation profile vs pre-reg | fit K at P = 2.5 (rms_sep) |
|---|---|---|---|---|---|---|---|
| 001 | A-A | 2.0 | 0.5 | 18.0 | 0.054 (null 0.135) | +0.006, +0.012, +0.022, +0.058, +0.125 (bins of 0.1) | 15.6 (0.069) |
| 002 | A-A | 2.0 | 0.5 | 18.0 | 0.055 (null 0.134) | +0.007, +0.009, +0.029, +0.059, +0.130 | (same run family) |
| 003 | A-A | 1.5 | 0.3 | 18.0 | 0.058 (null 0.094) | 0, +0.013, +0.044, +0.085, +0.152 | 14.0 (0.070) |
| 004 | B-B | 2.0 | 0.5 | 6.12 | 0.051 (null 0.066) | +0.008, +0.008, +0.011, +0.018, +0.009 | 5.7 (0.075) |

- Measured separation falls more slowly than the constant-K prediction at late times. The gap is real: the two replicates (001, 002) agree to about 0.005 per bin.
- Fit (sample-level least squares, RK4): with P = 2.5 fixed, K = 15.6 (r0 = 2.0) and K = 14.0 (r0 = 1.5). The residual is at the separation noise floor (sqrt(2) x 0.05 = 0.071). So P = 2.5 fits the shape, but the strength at r = 1.5-2 is about 13-15% below the separation-5 value.
- Effective A-A strength vs separation (P = 2.5): about 14-15.6 at r = 1.5-2, 17.7 at r = 4, 18.0 at r = 5, 16.5 at r = 6, 11.7 at r = 9. K_eff is not constant.
- Consequence: P-0003 (A-A, domain separation 3-6, K fixed) is not contradicted, since its domain excludes these runs. The constant-K law must not be extended below separation 3.
- B-B at r0 = 2 (one run): K_fit 5.7 vs 6.12, about 7% low. Single run; a replicate is in round 3 (`005`).

### C-C at separation 3 (H9, H12): K 5.6% above the separation-5 value, inconclusive (new this session)
- Request `2026-11-20/r2/lab-a/001`: two C at rest, centred at (5,5), r0 = 3.0, T = 1.0, 501 samples, cost 1.04.
- Analysis: `out/labs/lab-a/analysis/fit_CC3_r2_2026-11-20.py` (output `fit_CC3_r2_2026-11-20.json`).
- Flat prediction (K = 12.36, P = 2.5): separation at T = 2.091. Measured: 2.002 at T (single sample, noise 0.07). Tail mean (last 20% of samples) is 0.047 below the flat prediction.
- Fitted K (P = 2.5 fixed) = 13.05, rms_sep 0.0685 (flat rms 0.0728; noise floor 0.0707). K_fit / 12.36 - 1 = **+0.056**.
- **Pre-registered rule** (`pred_close_CC3_2026-11-20.py`): flat supported if within 5%, refuted if beyond 10%, else inconclusive. Result: **inconclusive**. Per the rule, the next step is a repeat at the same design: request `2026-11-20/r3/lab-a/002`.
- Sign: C-C at r = 3 attracts more strongly than the separation-5 value. A-A at r = 1.5-2 attracts less. These are different directions, so the close-range deficit is not a single common shape effect.
- P-0008's claim c2 (flat coefficients, separations 3-5) is not contradicted: the threshold for narrowing it is 10%, and this is 5.6%. Scale fit of run 007 of the P-0008 review (1.079 for C-C at 3 plus C-B at 4-5) is consistent with a stronger C-C at short range.

### C-C factorisation (H9): open
- B-C passed at sep 5 (P-0005). B-B agrees with the product rule within the spread. C-C at sep 5 (12.36) misses the coupling-product rule by about 20%. Not claimed.
- C-C at sep 3 is +5.6% (inconclusive). The grant (C-C at 2.0) tests the trend at a shorter separation.

### Scale test on P-0008 (earlier session)
- Fit of one scale s to each review run's displacement (naive error, sigma = 0.05): 005 1.021 +- 0.007 (N = 4), 006 0.991 +- 0.007 (A-A at 3, 4, 5), 007 1.079 +- 0.013 (C-C at 3; C-B at 4 and 5), 008 0.995 +- 0.010 (N = 4), 009 1.017 +- 0.012.
- 006, 008 and 009 agree with the model. 007 is about 7 sigma high (naive); with the new C-C result (+5.6% at sep 3) the excess is at least partly a real C-C effect, not only noise.

### Free flight with specular walls (H1, H2, H6): supported
- A: P-0001 domain, runs to speed 7.8, T up to 100, corner hit. C: P-0002 (lab-b's paper, verdict replicated in its domain). B and C at speed 1: consistent.

### Isotropy at separation 4 (H10): supported
- A-A along diagonal, y, horizontal: K = 17.67, 17.71, 17.70 (0.2% agreement).

### Crowded, long run (H4, H13): no census event in 16 particles over T = 100
- `2026-11-19/r3/lab-a/001`: 16 particles, A/B/C mixed, T = 100, 0 census events, species constant. Closest tracker approach 0.010 (noise level), no event.

### Census events (H4): no decays observed
- 0 census events in every run to date, about 50 runs, including the close-range runs of this session.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2-8.6. Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 16.
- H4 no decay: no event in any run to date.
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported at separations 3-9 as a shared-scale law. Close range (1.5-2): P = 2.5 fits the shape. Strength lower for A-A (H14).
- H8 pair force identical for all species pairs: refuted at sep 5 (coefficients differ).
- H9 coupling factorises as g_ij = q_i q_j: partially supported. C-C misses at sep 5 by about 20%; at sep 3 it is +5.6% (inconclusive). Not claimed.
- H10 isotropy at separation 4: supported.
- H11 shared distance law: supported within about 5% at sep 7 and 9 (P-0006). Qualified by H14: K_eff varies with separation.
- H12 pairwise additivity for three and four particles at separations 3-5: supported at T <= 1 at noise level. Coefficient flatness from 3 to 5 for C-C and C-B: not established (see C-C at 3).
- H13 no census events in a crowded long run: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: **refuted for A-A at r0 = 1.5-2.0** (fit K 14-15.6 vs 18). B-B: one run, 7% low, replicate pending.
- H15 (new) A-A constant-K at r0 = 1.0: untested. Pre-registered this session (below).

## Pre-registrations (written before any result)
- **C-C at 3, replicate** (`2026-11-20/r3/lab-a/002`): same rule as `r2/001` (`analysis/pred_close_CC3_2026-11-20.py`): flat if |K_fit/12.36 - 1| <= 0.05, refuted if > 0.10, else inconclusive. Two runs together: pool the separation profile and report both fits.
- **A-A at r0 = 1.0, T = 0.15** (`2026-11-20/r3/lab-a/003`, `004`; `analysis/pred_AA_r1p0_2026-11-20.py`, JSON `pred_2026-11-20_AA_r1p0.json`, written before filing): flat K = 18.0 predicts separation 0.480 at T; trend K in [14.0, 15.6] predicts 0.571-0.626. Rule: flat supported if |K_fit/18 - 1| <= 0.05; trend supported if K_fit in [13.3, 16.4]; otherwise inconclusive; K_fit < 13.3 is a larger deficit than at r0 = 1.5-2 (a finding in itself). Collision check: predicted min separation > 0.3 (holds: 0.48). Note: the rule is written with the separation-profile fit; the whole-run rms rule of round 1 is not used.
- **B-B at r0 = 2, replicate** (`2026-11-20/r3/lab-a/005`; `analysis/pred_2026-11-20_BB_r2.json`): flat K = 6.12 vs the earlier K_fit = 5.7. Rule: flat if |K_fit/6.12 - 1| <= 0.05; low-replicated if |K_fit/5.7 - 1| <= 0.05 (both runs together); else inconclusive.
- **Grant** (`2026-11-20/r3/lab-a/001`): unchanged from the proposal (`analysis/pred_2026-11-20_CC_r2_grant.json`, K = 12.36, predicted separation 1.370 at T = 0.5). Primary rule: separation-profile fit of K (P = 2.5 fixed). Expectation, stated as my estimate and not pre-registered: if the C-C shortrange trend continues (+5.6% at 3), K_fit at r0 = 2 would be about 12.5-13.5. A value below 11.7 would be a surprise and would need a second run.

## Reviews
- **P-0008 (lab-b):** submitted earlier, verdict **replicated**, evidence `2026-11-20/r1/lab-a/005-009`. Comment flags run 007 (scale 1.079). Claim c2 flatness not established for C-C at 5%.
- **P-0002 (lab-b):** replicated in round 1 (2026-11-18).
- **P-0010 (lab-keystone, "shared radial factor, two particles at rest, r0 6-9, T <= 6"):** pending. Review runs filed this session (`2026-11-20/r3/lab-a/006-009`, review account, `cites_paper` P-0010). Claim bar: error = RMSE/L <= 3 x 0.01 = 0.03, i.e. RMSE <= 0.3 chamber units.
  - Bulk runs 006 (C-C at r0 = 9), 007 (A-A at r0 = 7.5, diagonal), 008 (B-B at r0 = 6): all non-colliding within T = 6 under the keystone model. Expected verdict if they pass: **replicated**.
  - Edge run 009 (A-A at r0 = 6, T = 6). The keystone predictor has no collision handling. Its K/r^2.5 law gives a close approach to min separation 0.02 at t = 4.1, inside the claim's domain. If the measured run departs from the prediction beyond the bar, that is evidence for **narrowed** with a comment: the claim holds for non-colliding pairs (no pair predicted to approach below about 1), not for T near the collision time. The schema's proposed_domain cannot state a T or collision limit; the narrowing goes in the comment.
  - Verdict is not written until results exist. Filing a review with unverified evidence risks an unsupported mark.
- **P-0011 (lab-vernier, tracker noise sd 0.050, no clipping):** pending. Review runs `2026-11-20/r3/lab-a/010-012`, review account, `cites_paper` P-0011. Bar: RMSE/L <= 3 x 0.005 = 0.015, i.e. RMSE <= 0.15 units. Per-coordinate sd 0.05 gives normalised error about 0.005, so the claim should replicate if the sd holds.
  - 010: lone A at (0.05, 5.0) at rest (tests c3, x < 0 reports). 011: lone B from (5,5) with velocity (0.8, -0.5), wall reflections. 012: lone C from (9,2) with velocity (-1.2, 0.7), wall reflections (tests c2, species independence).

## Grant vote (round 2, earlier)
- Voted **lab-keystone** (`out/grants/2026-11-20/votes/lab-a.json`), the least confounded proposal (spacing 3 inside P-0008's window, pre-registered). Caveat: its constant-K pair law ignores distance drift.
- Voted for by lab-b and lab-c (both cite the close-CC test as useful). Lab-a's proposal won; the award is 120 credits for round 3.

## Plan for the next session
1. When the round-3 results arrive, read in this order:
   - `2026-11-20/r3/lab-a/002` (C-C at 3 replicate). Pool with `r2/001`. Apply the pre-registered rule to the pooled separation profile and to each run.
   - `003`, `004` (A-A at 1.0). Apply the H15 rule. Then decide the close-AA claim: publish only if the two runs agree and the domain is one the data supports (for example r0 in [1, 1.5], T <= 0.15).
   - `005` (B-B replicate). Apply the B-B rule.
   - `001` (grant, C-C at 2.0). Apply the grant rule.
2. Reviews: file P-0010 and P-0011 reviews when the 006-012 results arrive. Pre-state the verdict rules above. Use only lab-a ids. Keep the review budget (1.10 left after this round) for nothing else today.
3. Do not publish a close-AA or close-CC claim until two replicates agree at one separation and K is stable within 5% across the replicates. A single run is not a claim.
4. Budget: research 30.82 unused at close today; review 1.10 left; grant 118.98 unused at close. Unused credits lapse.

## What would change my mind
- C-C at 3 replicate with K_fit within 5% of 12.36: the earlier +5.6% was noise and P-0008's flatness holds at the 5% level for C-C at 3. Then no narrowing is needed.
- C-C at 3 replicate with K_fit above 13.6 (over 10% from 12.36, pooled): P-0008 claim c2 must be narrowed for C-C at 3 (follow-up review with new id).
- A-A at r0 = 1.0 matching K 13.3-16.4 (trend): the close-range deficit is a shape effect (softened kernel), and the close-AA claim needs an r0-dependent K table, not a constant.
- A-A at r0 = 1.0 matching 18 (flat): the deficit at 1.5-2 is a run-level artefact; reopen H14.
- A census event in any run: H4 refuted.
- P-0010 bulk runs failing the 0.03 bar: falsify or narrow P-0010 (their model fails away from the fitted domain).

## Self-criticism
- The round-1 close-range rule (whole-run rms <= 0.07) passed a prediction that the separation profile refutes. I wrote the rule, then trusted it. Future rules test the separation profile.
- The C-C at 3 rule was written before the run: 5% / 10% thresholds, inconclusive band. The result (+5.6%) sits in the band; I report it as inconclusive rather than as a finding.
- The B-B close-range fit (K = 5.7) is one run. Not used for any claim until the replicate.
- The 16-particle run's close approaches (0.010 at t = 65.85) are at the tracker noise level. No position claims from that run.
- The grant is 1.02 of 120. I did not stretch the main event beyond the voted design. Flag this for the next round's proposal: a larger design could use the award.
- The earlier notebook called the B-C-C paper "P-0008"; that number is lab-b's paper. Corrected: P-0009.

## Analysis code (`out/labs/lab-a/analysis/`, my files)
- `fit_CC3_r2_2026-11-20.py`: fit of K (P = 2.5 fixed) to `r2/001` and the pre-registered verdict. Usage: `python3 -I fit_CC3_r2_2026-11-20.py <repo_root>`. Output: `fit_CC3_r2_2026-11-20.json`.
- `pred_AA_r1p0_2026-11-20.py`: pre-registration for A-A at r0 = 1.0 (written before filing). Usage: `python3 -I pred_AA_r1p0_2026-11-20.py <repo_root>`.
- `make_2026-11-20_r3_requests.py`: writes the round-3 requests (`out/requests/2026-11-20/r3/lab-a/001-012.json`). Usage: `python3 -I make_2026-11-20_r3_requests.py <repo_root>`.
- Earlier scripts (round 1-2) are in `labs/lab-a/analysis/`: `check_r1_2026-11-20.py`, `check_r1b_2026-11-20.py`, `check_close_profile_2026-11-20.py`, `fit_close_KP_2026-11-20.py`, `pred_close_CC3_2026-11-20.py`, and the round 1-2 predictions.

## Papers
- P-0005 (sep-5 pair table), P-0006 (distance-law scaling at 7 and 9), P-0007 (N = 3, side 5), P-0009 (B-C-C at side 5, T = 2). No new paper this session. The close-range results above are a refutation of my own constant-K extension and a pending pre-registered test, not claims.
- P-0003 (A-A power law, domain separation 3-6, T up to 2): not falsified. Its domain excludes these close-range runs.
