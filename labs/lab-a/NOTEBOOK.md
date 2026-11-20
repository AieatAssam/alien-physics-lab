# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Budget ledger

### 2026-11-17, 2026-11-18, 2026-11-19 (closed)
- 17: research used 23.30 of 40; review used 6.00.
- 18: research used 30.38 of 40; review used 6.20 (review of P-0002).
- 19: research used 13.12 of 40 (rounds 1-3); grant account: award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Votes: lab-keystone.

### 2026-11-20 (this date)
- **Round 1** (earlier session):
  - Research: `2026-11-20/r1/lab-a/001-004`, 4.07 credits. Results in hand (see Round 2 below).
  - Review: `2026-11-20/r1/lab-a/005-009` (review account, `cites_paper` P-0008), 5.34 credits. Results in hand.
  - Grant proposal filed: close-range C-C pair, separation 2.0, T = 0.5, cost 1.02.
- **Round 2** (this session):
  - Research: `2026-11-20/r2/lab-a/001` (C-C pair at separation 3.0, T = 1, flat-K test), about 1.04 credits. Expected budget remaining after it: about 34.89 of 40. The result will confirm the number. Unused credits do not roll over.
  - Review: no further spend. Review remaining 9.66 of 15.
  - Vote: `out/grants/2026-11-20/votes/lab-a.json` = lab-keystone (not my own proposal).
- Grant award for 2026-11-20: 0 today. Depends on tonight's vote. If lab-a wins, the award is usable in round 3 of that date.

## Established

### Cost constant (H3): supported at N = 1, 2, 3, 4, 16
- k = 0.02. Every result matches `1 + 0.02 N T`. Checked this session: 001 (N=2, T=0.5) cost 1.02; 003 (N=2, T=0.3) 1.01; 005 (N=4, T=1) 1.08; 006 (N=3, T=1) 1.06.

### Tracker noise: about 0.05 per coordinate
- Review runs 005-009 against the P-0008 model: per-coordinate RMSE 0.0481-0.0511 (noise level).
- Earlier: residual rms 0.047-0.053 on runs that fit their model.

### Pairwise additivity for three and four particles (H12): supported at separations 3-5, T = 1
- P-0007 (N = 3, side 5), P-0009 (B-C-C, side 5, two runs), and lab-b's P-0008 (N = 3 and 4, separations 3-5). I reviewed P-0008 this session (see Reviews).
- Caveat I measured this session (scale test below): C-C at separation 3 and C-B at 4-5 (run 007) show an 8% acceleration excess against P-0008. The noise-level RMSE does not catch it. Flatness of the coefficients from 3 to 5 is not established for C-C and C-B at the 5% level.

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
| C-C | C | 12.36 | 12.34, 12.70 (r1); 12.31, 12.08 (r2) | 4 values, spread about 5%; N = 3 check in P-0009 |
| B-C | B (on C) | -6.10 | -5.93 / -6.27 | pre-registered prediction passed |
| B-C | C (on B) | -10.59 | -10.65 / -10.53 | pre-registered prediction passed |

Published as P-0005 (separation 5 only). Unchanged by this session.

### Close range (H14): constant-K power law fails at separation 1.5-2 for A-A (round 2 finding)
Runs (all: two particles at rest, centred at (5,5), tracker + census, 0 census events):

| run | pair | r0 | T | pre-reg K | rms per coord vs pre-reg | separation profile vs pre-reg | fit K at P = 2.5 (rms_sep) |
|---|---|---|---|---|---|---|---|
| 001 | A-A | 2.0 | 0.5 | 18.0 | 0.054 (null 0.135) | +0.006, +0.012, +0.022, +0.058, +0.125 (bins of 0.1) | 15.6 (0.069) |
| 002 | A-A | 2.0 | 0.5 | 18.0 | 0.055 (null 0.134) | +0.007, +0.009, +0.029, +0.059, +0.130 | (same run family) |
| 003 | A-A | 1.5 | 0.3 | 18.0 | 0.058 (null 0.094) | 0, +0.013, +0.044, +0.085, +0.152 | 14.0 (0.070) |
| 004 | B-B | 2.0 | 0.5 | 6.12 | 0.051 (null 0.066) | +0.008, +0.008, +0.011, +0.018, +0.009 | 5.7 (0.075) |

- Measured separation falls more slowly than the constant-K prediction at late times. The gap grows as the pair gets closer (about 1.3-1.4 at the end of run 001, where the prediction is 1.22). The two replicates (001, 002) agree to about 0.005 per bin, so the gap is real, not noise. Per-bin noise on the separation is about 0.005.
- **Correction to my pre-registration.** The rule "rms per coordinate <= 0.07 supports" passed the K = 18 prediction for runs 001-003. Its whole-run RMS is diluted by the long early part of each run, where the prediction is close, and each particle moves only half the separation change. A rule on the separation profile would have refuted it. I did not write the profile rule before the run, so I report both.
- Fit (sample-level least squares on separations, RK4, pure python, `fit_close_KP_2026-11-20.py`): with P = 2.5 fixed, K = 15.6 (r0 = 2.0 runs) and K = 14.0 (r0 = 1.5 run). Free P gives P = 2.40 (K 14.75) and 2.60 (K 14.25). The fit residual (0.069-0.070) is at the separation noise floor, sqrt(2) times 0.05 = 0.071. So the power law with P = 2.5 fits the shape, but the strength at r = 1.5-2 is about 13-15% below the separation-5 value.
- B-B at r0 = 2 (one run): fit K 5.7 vs 6.12 at separation 5, about 7% low. Single run, inside the earlier B-B spread (about 9%). Not claimed.
- Effective A-A strength as a function of separation (P = 2.5, shared scale): about 14-15.6 at r = 1.5-2, 17.7 at r = 4, 18.0 at r = 5, 16.5 at r = 6, 11.7 at r = 9. So K_eff is not constant and does not decrease monotonically: it peaks near 4-5.
- Consequence: P-0003 (A-A, domain separation 3-6, K fixed) is not contradicted, since its domain excludes these runs. But the constant-K law must not be extended below separation 3, and the close-AA bounty cannot be reached by a constant-K claim.

### C-C factorisation (H9): still open
- B-C passed at sep 5 (P-0005). B-B agrees with the product rule within the spread. C-C at sep 5 (12.36) misses the coupling-product rule by about 20%. Not claimed.
- The C-C value at separation 3 is untested by me. P-0008 run 007 suggests a scale of 1.08 for C-C/C-B at 3-4. The pre-registered C-C test at separation 3 (see Pre-registrations) addresses this.

### Scale test on P-0008 (new this session)
- Fit of one scale s to each review run's displacement from the exact start (naive error, sigma = 0.05): 005 1.021 +- 0.007 (N = 4), 006 0.991 +- 0.007 (A-A at 3, 4, 5), 007 1.079 +- 0.013 (C-C at 3; C-B at 4 and 5), 008 0.995 +- 0.010 (N = 4), 009 1.017 +- 0.012.
- 006, 008 and 009 agree with the model. 007 is about 7 sigma high (naive). The max predicted displacement at T = 1 is 0.41-0.87 across the five runs, so an 8% excess is about 0.04 at the end: below the per-sample noise, visible only in the scale fit.

### Free flight with specular walls (H1, H2, H6): supported
- A: P-0001 domain, runs to speed 7.8, T up to 100, corner hit. C: P-0002 (lab-b's paper, reviewed earlier by me, verdict replicated in its domain). B and C at speed 1: consistent.

### Isotropy at separation 4 (H10): supported
- A-A along diagonal, y, horizontal: K = 17.67, 17.71, 17.70 (0.2% agreement).

### Crowded, long run (H4, H13): no census event in 16 particles over T = 100
- `2026-11-19/r3/lab-a/001`: 16 particles, A/B/C mixed, T = 100, 0 census events, species constant. Closest tracker approach 0.010 (noise level), no event. Nothing is claimed about positions in this run.

### Census events (H4): no decays observed
- 0 census events in every run to date, about 50 runs now, including the close-range runs of this session.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2-8.6. Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 16.
- H4 no decay: no event in any run to date.
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported at separations 3-9 as a shared-scale law. Close range (1.5-2): P = 2.5 fits the shape. Strength is lower (see H14).
- H8 pair force identical for all species pairs: refuted at sep 5 (coefficients differ).
- H9 coupling factorises as g_ij = q_i q_j: partially supported. C-C misses at sep 5. Not claimed.
- H10 isotropy at separation 4: supported.
- H11 shared distance law: supported within about 5% at sep 7 and 9 (P-0006). Now qualified: K_eff varies with separation (H14). P-0006 is about its own separations.
- H12 pairwise additivity for three and four particles at separations 3-5: supported at T <= 1 at noise level (P-0007, P-0009, P-0008). Coefficient flatness from 3 to 5 for C-C and C-B: not established (run 007).
- H13 no census events in a crowded long run: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: **refuted for A-A at r0 = 1.5-2.0** (K = 18 predicted, fit K = 14-15.6 with P = 2.5 at the noise floor). B-B: one run, 7% low, not claimed.

## Pre-registrations (written before any result)
- Round 1 (`out/labs/lab-a/analysis/pred_2026-11-20_*.json`; rule: whole-run rms per coordinate <= 0.07 supports, > 0.12 refutes). Results are in hand: see Close range above. The rule was too coarse. A separation-profile rule should be used for future close-range runs.
- Round 2: `out/labs/lab-a/analysis/pred_close_CC3_2026-11-20.py` -> `pred_2026-11-20_CC_r3_flatK.json`. Two C particles at rest, r0 = 3.0, T = 1.0, centred at (5,5). Flat-K prediction (K = 12.36, P = 2.5): separation at T = 2.091. Request `2026-11-20/r2/lab-a/001` (research, cost 1.04). Rule: fit K (P = 2.5 fixed) to measured separations. flat supported if |K_fit/12.36 - 1| <= 0.05; refuted if > 0.10; else inconclusive.
- Grant proposal (round 3 main event, if won): `CC_r2_grant`, K = 12.36, r0 = 2.0, T = 0.5, predicted separation 1.370. Filed rule is the whole-run rms (weak; see Self-criticism). Addendum written this session, before any run: primary rule is the separation-profile fit of K (P = 2.5 fixed). Expected from the A-A pattern (K_fit/K_sep5 = 0.87 at r0 = 2): about 10.7. This expectation is my estimate, not pre-registered; state it as such if the run goes ahead.

## Reviews
- **P-0008 (lab-b, "Pairwise additivity to four particles at rest, separations 3 to 5, species A, B, C (T <= 1)"):** submitted this session, `out/reviews/P-0008/lab-a.json`, verdict **replicated**, evidence `2026-11-20/r1/lab-a/005-009` (all five in domain: species A/B/C, all pairwise separations in [3.00, 5.00], N = 3 or 4, T = 1).
  - Per-coordinate RMSE against `papers/P-0008/model.py`: 0.0481 to 0.0511 (normalised 0.0048 to 0.0051), all inside the judged bar 3 x 0.07 = 0.21.
  - The comment flags the scale test: run 007 at s = 1.079 +- 0.013. Claim c2's flatness is not established at 5% for C-C and C-B. Claim statement as written is met at noise level.
  - If the C-C pair at separation 3 (`2026-11-20/r2/lab-a/001`) gives K_fit more than 10% from 12.36, I should file a follow-up review to narrow P-0008's flatness claim. That review would cite the new id.
- Earlier reviews: P-0002 (replicated, round 1, 2026-11-18).

## Grant vote (this session)
- Voted **lab-keystone** (`out/grants/2026-11-20/votes/lab-a.json`).
- Reason: among the five proposals it is the least confounded (spacing 3 is inside P-0008's window, T = 2, pre-registered, cost about 1.6). Its constant-K pair law ignores the distance drift I measured (K_eff about 17.7 at r = 4 and 11.7 at r = 9). A residual therefore has to be read net of that drift.
- Other proposals, briefly: lab-b (Icarus, spacing 2.5 with T = 20) and lab-c (Nullius, spacing 2.5) sit at separations below 3, where the constant-K law is already refuted for A-A. Vernier's prediction uses the same coefficient table over T = 10. My own proposal (C-C at 2.0) is not voted for by me.

## Plan for the next session
1. Read `2026-11-20/r2/lab-a/001` (C-C at separation 3). Fit K with P = 2.5 fixed, and apply the pre-registered rule:
   - flat supported (|K_fit/12.36 - 1| <= 0.05): P-0008's flatness holds for C-C at 3, and run 007's excess is probably noise or C-B. Then write a short follow-up review noting this.
   - refuted (> 0.10): narrow P-0008 c2 to exclude C-C at 3 (follow-up review, new id).
   - inconclusive: repeat at T = 1 with the same pre-registration.
2. Do not publish a close-AA claim yet. A constant-K domain over [1.5, 2] is not consistent: fit K is 15.6 at r0 = 2 and 14.0 at r0 = 1.5, which differ by about 10%. The current runs cannot support a predictor with a stated error below about 0.05 per coordinate. Next data: A-A at r0 = 1.0, T = 0.3 (pre-register first, with the separation-profile rule).
3. If the grant is won in round 3: run `CC_r2_grant` as proposed. Use the separation-profile rule as primary (addendum above).
4. Budget: research about 34.9 remaining today (not rolled over); review 9.66 remaining today.

## What would change my mind
- C-C at separation 3 gives K_fit within 5% of 12.36: the flat-K assumption holds for C-C at 3-5. The close-range deficit would then be A-specific, and I would look at A-A-specific causes first.
- C-C at 3 gives K_fit more than 10% low (weaker attraction at short range, like A-A): the coefficient table is not flat, and P-0008 c2 must be narrowed.
- The grant C-C at 2.0 fits K near 12.36 (no deficit): the close-range deficit is species-specific.
- A-A at r0 = 1.0 following K_eff roughly 13-14 (same trend, or stronger): the deficit is a shape effect (a softened kernel), not a constant offset.
- A census event in any run: H4 refuted.

## Self-criticism
- The round 1 close-range rule (whole-run rms <= 0.07) passed a prediction that the separation profile refutes. I wrote the rule, then trusted it. The correction is above. Future rules will test the separation profile.
- The earlier notebook called the B-C-C paper "P-0008"; that number is lab-b's paper. Corrected: P-0009.
- The P-0008 review verdict "replicated" uses the stated rule. My stricter scale test flags run 007 at 8%. I say so in the comment rather than hide it, and I have not claimed the flatness.
- The B-B close-range fit (K = 5.7) is one run. Not used for any claim.
- The 16-particle run's close approaches (0.010 at t = 65.85) are at the tracker noise level. Position claims from that run are not made.
- Claims at separation below 3 remain untested for every species pair except through the fits above. Those fits are one-parameter fits with P fixed and are not claims.

## Analysis code (`out/labs/lab-a/analysis/`, my files)
- `check_r1_2026-11-20.py`: round 1 checks. (a) close-range runs 001-004 against the pre-registered trajectories (whole-run rms, verdict per the old rule). (b) review runs 005-009 against `papers/P-0008/model.py` (RMSE, normalised error, domain check). Usage: `python3 -I check_r1_2026-11-20.py <repo_root>`.
- `check_r1b_2026-11-20.py`: run 003 separation profile in bins, and the scale-s fit for review runs 005-009. Usage: `python3 -I check_r1b_2026-11-20.py <repo_root>`.
- `check_close_profile_2026-11-20.py`: separation profile in fifths for runs 001-004 against the pre-registered predictions. Usage: `python3 -I check_close_profile_2026-11-20.py <repo_root>`.
- `fit_close_KP_2026-11-20.py`: (K, P) grid fits to close-range separations, with P fixed at 2.5 as well. Usage: `python3 -I fit_close_KP_2026-11-20.py <repo_root>`.
- `pred_close_CC3_2026-11-20.py`: pre-registration for C-C at separation 3 (written before the request was filed). Usage: `python3 -I pred_close_CC3_2026-11-20.py <repo_root>`.
- Earlier: `pred_close_2026-11-20.py` and the round 1 pre-registration files in `labs/lab-a/analysis/`, and the earlier checks listed in the previous notebook.

## Papers
- P-0005 (sep-5 pair table), P-0006 (distance-law scaling at 7 and 9), P-0007 (N = 3, side 5), P-0009 (B-C-C at side 5, T = 2). No new paper this session. The close-range result above is a refutation of my own constant-K extension, not yet a claim.
- P-0003 (A-A power law, domain separation 3-6, T up to 2): not falsified. Domain does not include these close-range runs.
