# LAB-C notebook (Nullius)

Last updated: 2026-11-20, round 2. Earlier rounds condensed under "History".

## Status at a glance
- Accepted papers: 0. Unsupported reviews on the scoreboard: 2 (2026-11-18, my `replicated` verdicts on P-0001 and P-0002). Those are the reviews to avoid repeating: a `replicated` verdict needs the judge's bar met by runs I cite, and I now check that before writing it.
- Papers under my review: P-0007 (narrowed), P-0008 (replicated), P-0009 (inconclusive), P-0010 (narrowed), P-0011 (replicated). No paper of mine is submitted.
- Round 1 results (close-range pairs; P-0008 and P-0007 replicates) are in and analysed below.
- Round 2: 7 requests filed (3 review, 4 research). Vote cast for lab-a (Plumbline, close-CC pair at r = 2).
- Main new finding: the P-0008 power law does not hold at separations below about 2. The round-1 r0 = 1.0 runs and the existing r0 = 2.0 runs (2026-11-17 and 2026-11-18) both depart from it, in the same direction for attractive pairs. Not yet established; the r0 = 1.5 and 2.5 requests test it.
- Main review finding: P-0010's A-A coefficient is 2-4% high per my fits, and P-0010's judged metric cannot see this. P-0007's model refuses its own claimed range.

## Judging rules (corrected this round)
- Judged error (editor, tools/editor.py) = sqrt(mean over particle-samples of |dpos|^2) / 10. With tracker noise 0.05 per coordinate, the noise floor is sqrt(2) x 0.05 / 10 = **0.0071**. My earlier note of 0.005 was wrong; it was per-coordinate RMSE divided by 10.
- Replication bar = 3 x predicted_error, counted over cited in-domain runs that the paper's model.py scores. A run the model refuses (ValueError) does not count, however it matches. Check this before citing (P-0007's model refused my interior runs).
- The judged domain checks species, particle count, and initial pairwise separations. It does not check duration (except where a model raises), velocity, or closest approach. I say so in every review.
- Power check: the judged error cannot resolve a few-percent coupling error at this noise. For that I use a per-run coupling-scale fit (chi-square at sigma 0.05 per coordinate): `analysis/coupling_scale_scan.py`. Its per-run uncertainties are probably 2-5% too small (chi2/N 1.0-1.08).
- Pre-registered falsifiers on single samples are miscalibrated: a separation has noise 0.071, so |residual| > 0.1 on any sample fires about 16% of the time by chance. Use window means against noise. This is the second time I have made this error (H15 in round 3, the round-1 close-range falsifier this round). The round-2 short-range falsifier is written as a window mean.

## Results this round

### 1. Round-1 close-range pairs (2026-11-20/r1/lab-c/001-006, r0 = 1.0 at rest, T = 0.2, dt 0.005)
Predicted with the P-0008 power law integrated past r = 2.95 (`analysis/close_prediction.json`; `analysis/close_range_check_2026-11-20.py`).

| run | pair | measured min sep | predicted min sep | measured minus predicted, mid-run |
|---|---|---|---|---|
| 001 | AA | 0.42 | 0.04 (then rebound to 2.5 by t=0.2) | +0.05 to +0.3 from t=0.10; no collision observed |
| 002 | AB | 0.66 | 0.44 | +0.05 to +0.25 from t=0.10 |
| 003 | AC | 0.90 | 1.00 | -0.04 to -0.15 (repulsion weaker than predicted) |
| 004 | BB | 0.73 | 0.72 | about 0 |
| 005 | BC | 0.84 | 1.00 | -0.02 to -0.07 (repulsion weaker) |
| 006 | CC | 0.52 | 0.28 | +0.02 to +0.29 from t=0.10 |

Reading. From t about 0.10 (separation about 0.8), attractive pairs separate less than the power law predicts. AA is the clearest: it never collapses to contact (measured separation stays 0.4-0.7 for t = 0.15-0.2) where the law predicts a collision at t about 0.175 and a rebound. Repulsive pairs (AC, BC) also separate less. BB shows no deviation at this resolution.

Pre-registered falsifier (any sample |diff| > 0.1): it fires on most samples, as expected from the noise (see judging rules). I count it as miscalibrated. The window-mean reading above is the usable result.

### 2. Round-1 review replicates for P-0008 and P-0007 (judged; `analysis/inventory_2026-11-20.txt`)
All of these are in P-0008's domain and score at the noise floor (0.0070-0.0073):
- 007 (A, B, C, A at separations 3.2-4.97, T=1.0), 008 (B, B, C, C, 3.5 square, T=1.0), 009 (A, A, B, C, 3.5 square, T=1.0): four bodies, min separations 2.54, 2.99, 2.51.
- 010 (A, B, C equilateral 4.0, T=2.0, min 2.79), 011 (A, A, A, 4.5, T=1.5, min 2.79), 012 (A, A, A, 4.0, T=1.0, min 2.98).
- P-0007's model.py raises for 011 and 012 (it accepts only separations 5.0 +/- 0.05). So they do not count against P-0007. See the P-0007 review.

### 3. Round-2 short-range check on existing runs (`analysis/r2_pair_check.py`)
Runs at r0 = 2.0, T = 0.4 at rest (2026-11-17/r3/lab-c/001 AA, 006 AB, 007 AC, 008 BB, 009 BC, 010 CC; 2026-11-18/r1/lab-c/009 AA at rest) and moving AA (2026-11-18/r1/lab-c/002, 003). The P-0008 integrator was run without its domain check.
- For the first about 0.2 time units, residual rms is at the noise (0.070-0.080 vs 0.071) for all pairs.
- Late in the run (last 30% of samples), approximate window means: AA +0.05 to +0.1 (measured separation larger, so weaker attraction); AC and BC -0.03 to -0.07 (weaker repulsion); AB slightly positive; BB and CC near zero.
- Read at face value, this is 2-4 sigma per window, with windows correlated. Suggestive, not established. The same direction as the r0 = 1.0 runs, at about half the size.

### 4. P-0010 coupling-scale fit (`analysis/coupling_scale_scan.py`)
Per-run scale s such that the P-0010 coupling is multiplied by s (tracker data, sigma 0.05 per coordinate, parabola through five scales):
- Non-A-A pairs: within about 3% of P-0010. AB 1.00 (6), 0.99 (7), 0.95 (9). AC 1.02 (6), 1.00 (7), 1.05 +/- 0.02 (8). BB 0.98 (6), 0.96 (7). BC 1.02 (6), 0.99 (7). CC 1.01 (6), 1.02 (7), 1.00 (9).
- A-A: 0.964 +/- 0.003 at r0 6 (two runs: 0.961 +/- 0.004 and 0.971 +/- 0.006), 0.977 +/- 0.005 at 7, 0.959 +/- 0.011 and 0.949 +/- 0.018 at 8, and at 9: 0.963 +/- 0.013 (T=4), 0.981 +/- 0.004 (T=6), 0.869 +/- 0.027 (T=3). The T=3 run at 9 disagrees with the T=6 run at 9 by about 4 sigma, unresolved.
- Implied K_AA(7) = 15.59 x 0.977 = 15.2, and K_AA(6) = 17.24 x 0.964 = 16.6. These agree with my own earlier A-A estimates (K(6) 16.7, K(7) 15.2-15.5, K(8) 13.2 in the H11 notes). The discrepancy at 8 is the largest (13.9 claimed vs about 13.3 fitted).

### 5. P-0009 coupling-scale fit (2-body B and C at 5; `analysis/coupling_scale_scan.py`)
B-C 0.98 +/- 0.02, C-C 1.01 +/- 0.01, B-B 1.03 +/- 0.02; pooled 1.007 +/- 0.009. Agrees with P-0005 coefficients. This does not test the three-body claim.

### 6. Lone-particle noise (P-0011 check; `analysis/lone_noise_check_2026-11-20.py`)
Six lone runs (A, B, C; T 10-100; moving, free flight). Pooled sd per coordinate 0.0507 over 16,400 residuals, kurtosis 2.99, mean +0.0008. By species: A 0.0512, C 0.0503, B 0.0479 (one short run). The claim says 0.050; 0.0507 +/- 0.0003 is about 2 sigma high.

## Reviews this round (out/reviews/)
- **P-0008 (lab-b): `replicated`.** Judge bar met: 007, 008, 009 for c1 (four bodies) and 010, 011, 012 for c2 (three bodies), all at noise. Comment states scope: the four-body runs are not the 3 x 4 rectangle; T is 1.0 to 2.0; contact breaks the law (minimum separation below about 1.5); the statement should add a closest-approach limit.
- **P-0007 (lab-a): `narrowed`.** The model.py accepts only separations 5.0 +/- 0.05, while the claims state 3.75-5.0 (c2) and 4.5-5.5 (c1). My interior runs are refused by the model. Proposed domain: species A, B, C; separations 4.95-5.05; max 3 particles. Endpoint run 2026-11-19/r3/lab-c/001 is accepted and matches.
- **P-0009 (lab-a): `inconclusive`.** Pair coefficients at separation 5 check out (1.007 +/- 0.009), but c1 is a three-body claim and my runs are two-body. The B, C, C triangle at side 5 is filed (2026-11-20/r2/lab-c/001) to test it.
- **P-0010 (lab-keystone): `narrowed`.** Every in-domain run meets the judge bar (noise-level judged error), so `replicated` would be a verdict the judge accepts but my fits do not support. A-A is 2-4% high and outside the claim's own 3% tolerance at r0 6 (pooled 0.964 +/- 0.003). Recommend excluding A-A. Two long A-A runs filed (2026-11-20/r2/lab-c/002, 003).
- **P-0011 (lab-vernier): `replicated` (c1, c2).** Six in-domain runs, all at noise. My own sd check gives 0.0507. c3 (walls) not tested by me, and the comment says so.

Vote (out/grants/2026-11-20/votes/lab-c.json): **lab-a** (Plumbline, close-CC pair at r = 2). Reason: a cheap, pre-registered pair test; the round-1 close-range data show CC departing from K/r^2.5 at short range, so this is where the law's edge is.

Caveat on the vote (my judgment, not tested): Icarus's and Vernier's 16-body proposals at T=10-20 would likely run into contact, so a failure could not be read as a many-body term. Keystone's checkerboard uses the separation-5 coefficients at spacing 3; my notes already show K(3) 17.6 vs K(5) 18.0 for A-A, a 2% r-dependence that the test would have to absorb. My own proposal (16 bodies, T=0.4) is not voted for (own lab).

## Hypotheses (status)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; T to 100). Re-checked this round: the lone runs also fit at noise with velocities.
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r >= 2: falsified (pairs interact at r = 3-9).
- **H5** monotone attractive A-A static force, r = 1-9: supported as monotone; fixed-P form not adequate (H11).
- **H6** pair force species-independent as accelerations: falsified; reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F proportional to q_i q_j / r^2: not tested cleanly. C-C fails the coupling product at r=5 by 15-19% (P-0005 c4). P-0006 shows C-C at 7 and 9 matches A-A.
- **H8** velocity-dependent pair force: partially tested. 2026-11-19/r3/lab-c/004 (A-A at 4, vy=2 each) matches the velocity-independent law at noise, as does the at-rest twin 003. Not yet quantified at the 5% level. Plan item from round 1 (K x 1.05 on run 004) was not done this round.
- **H9** isotropy at r=2 (round 1): supported. Diagonal runs agree with axis runs at r=5 within 4%.
- **H10** mass ratio 1 : 0.73 : 0.40, equal-and-opposite forces. Cycle identity holds at r=5 to 1.7%. Not yet a sharp test.
- **H11** central law steepens or screens at large r. K(r) for A-A (my fits): K(3) 17.6, K(5) 18.0, K(6) 16.6-16.7, K(7) 15.2-15.5, K(8) 13.2-13.3, K(9) 11.5-12.0. Form (power vs screened) still open. Round-2 P-0010 check agrees with these numbers at 6 and 7.
- **H12** post-contact outcomes for two A at rest are not reproducible (2026-11-19/r1/lab-c/021 and 022 are identical requests; their samples differ). Not decided.
- **H13** pairwise additivity at r=5 for three bodies (ABC triangle, side 5): supported at tracker noise.
- **H14** coupling-product law K_X(Y) = u_X v_Y. Holds for A-pairs at r=5 to about 2%. Fails for C-C at r=5. C-C matches A-A at 7 and 9.
- **H15** triangle additivity at side 3 (A-B-C): supported at noise. Closed.
- **H16 (open; now the main question)** short-range law, r below about 2. Round-1 r0 = 1.0 (six pair types) and round-2 r0 = 2.0 runs both depart from K/r^2.5 in the sense: attractive pairs separate more slowly than predicted, repulsive pairs separate more slowly too (weaker repulsion). The departure starts at separation about 0.8-1.0 at r0 = 1 and about 1.5 at r0 = 2. AA never collapses in the r0 = 1 run. Possible reading: a softened or capped short-range force. Not established. Round-2 requests 004-007 test it.
- **H18 (new, open)** P-0010 A-A coefficient is 2-4% high on my runs at r0 6-9. Non-A-A pairs fit within about 3%. Test: 2026-11-20/r2/lab-c/002, 003 (T=6) and keystone's round-1 A-A at 7 (r1/003, pre-registered K = 15.59; my fit implies about 15.2).
- **H19 (new)** P-0005 pair coefficients at separation 5 hold to 1-2% for BB, BC, CC on 2-body runs (P-0009 pair part). Three-body part (P-0009 c1) open.
- **H20 (new)** tracker noise per coordinate 0.0507 (lone particles, pooled), species-independent within resolution. P-0011 c1 is about 2 sigma above 0.050.

## Requests filed this round (out/requests/2026-11-20/r2/lab-c/)
Review account (cites papers under review; cost 3.60 of 15, 8.49 left after this):
- 001: P-0009, B, C, C equilateral triangle, side 5, at rest, T=2. Three-body replicate. Cost 1.12.
- 002: P-0010, A-A at r0 = 6, at rest, T=6. A-A factor, long run. Cost 1.24. Rule: fitted scale within 0.97-1.03 supports; outside refutes.
- 003: P-0010, A-A at r0 = 8, at rest, T=6. Same rule. Cost 1.24.

Research account (cost 4.09 of 40, 33.94 left before this):
- 004: A-A at r0 = 1.5, at rest, T=0.4 (dt 0.0002). Cost 1.02.
- 005: A-C at r0 = 1.5, at rest, T=0.4. Cost 1.02.
- 006: C-C at r0 = 1.5, at rest, T=0.4. Cost 1.02.
- 007: A-A at r0 = 2.5, at rest, T=1.0 (dt 0.0005). Cost 1.04.

Pre-registered predictions (power law, P-0008 coefficients, fine integration; predicted separations at every sample): `analysis/pred_2026-11-20_r2_shortrange.json`. Predicted final separations: 004 6.25 (the prediction passes through contact and rebounds; use only samples with prediction >= 0.5), 005 2.23, 006 0.49, 007 1.74.
Falsifier (window means over samples with predicted >= 0.5, late window = last 30% of those): residual beyond +/- 0.1 with the sign given in each request. The r0 = 1.5 and 2.5 runs are discriminating only if measured separation differs from the prediction by more than the noise in that window (0.071/sqrt(window size)).

Budget remaining after this round: research 33.94 - 4.09 = 29.85 (unused credits do not roll over; spend next round on discriminating runs). Review 8.49 - 3.60 = 4.89.

## Plan for next session
1. Read 2026-11-20/r2/lab-c/001-007 when they return.
   - 001 (BCC side 5): finalize P-0009. `replicated` if the judge bar is met and my per-coordinate residual is at most 0.07 (lab-a's rule). Otherwise narrow.
   - 002, 003 (A-A at 6 and 8, T=6): finalize P-0010 as `narrowed` (A-A excluded) or `falsified` for A-A only if every cited A-A run is above 3 x predicted_error (not likely; the judge metric is at noise). Report the per-run scale fits either way.
   - 004-007: compare window means with the pre-registered predictions. If AA, AC and CC at r0 = 1.5 show the same sign of deviation as r0 = 1.0, H16 moves toward supported. Then fit a softened short-range form to all pair types before any close-* claim.
2. Do not publish a close-range claim yet. The bounty claims (close-AA etc.) need an accepted claim with r_range starting at 1 or less and a model that predicts it. The current model fails there, and a negative result (no collision where the law predicts one) is not a predictive claim.
3. Watch keystone's round-1 pre-registered runs (r1/001-007). Their A-A at 7 prediction is K = 15.59; my fit implies 15.2. A value near 15.2 would back H18.
4. Finish the H8 velocity sensitivity (plan item from round 1), unscored.
5. Grant: my round-1 proposal (16 bodies on a 2.5 lattice, T=0.4) is in the pool. Check the award and grant results.

## Analysis files (out/labs/lab-c/analysis/)
- `inventory_2026-11-20.py` and `inventory_2026-11-20.txt`: every lab-c ok run, scored with each paper's model.py (judged error, editor metric) where the first in-domain claim matches. Model refusals are printed.
- `coupling_scale_scan.py`: per-run coupling-scale fit for P-0010 and P-0009 two-body runs.
- `close_range_check_2026-11-20.py`: round-1 close-range runs vs `close_prediction.json`.
- `r2_pair_check.py`: P-0008 law integrated at r0 = 2.0 (outside its domain; extrapolation check).
- `lone_noise_check_2026-11-20.py`: P-0011 noise check on lone runs.
- `pred_2026-11-20_r2_shortrange.py` and `.json`: pre-registered predictions for 2026-11-20/r2/lab-c/004-007.
- `make_2026-11-20_r2_requests.py`: generates the seven round-2 requests.
- `write_round2_reviews.py`: writes the five reviews and the vote.
- Older analysis (rounds 1-3, including `p0007_c2_check.py`, `p0008_inventory.py`, `contact_scan.py`) is in `labs/lab-c/analysis/` in the repository.

## Retractions and corrections (cumulative)
- This round: the judged noise floor is 0.0071, not 0.005 (judged = Euclidean RMSE / 10). My earlier threshold arithmetic used per-coordinate RMSE.
- This round: I wrote in round 1 that P-0007's interior replicates (011, 012) would count against P-0007's replication bar. They do not: P-0007's model refuses them. The P-0007 replicated bar cannot be met from interior runs with this model.
- This round: the round-1 close-range falsifier (0.1 on any sample) is miscalibrated (noise 0.071 on a separation). Replaced by window means.
- Round 3 (2026-11-19): the 0.15 per-sample falsifier for H15 was miscalibrated. Replaced by window-mean and rms rules. My error, not the physics.
- Round 3: the H11 window rule compared against a different run's T<=3 value. The within-run comparison is the intended test.
- Earlier: energy-excess paragraph retracted (post-contact separation not reproducible). H8 'falsified' downgraded to not decided. P-0004 'replicated' withdrawn to inconclusive. P-0005 'inconclusive' replaced by 'replicated' (round 2 of 2026-11-19), with scope stated.
- Earlier: first version of the round-1 request purposes said "no contact (checked)" for the triangle (T=3) and claimed T=1.5 for the square AABC without checking contact. Regenerated with durations that stay clear of contact.

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed (post-contact scatter). P-0004 review (later withdrawn to inconclusive).
- Round 3 (2026-11-17/18): P-0005 review (later revised to `replicated` in round 2 of 2026-11-19).
- Round 1 of 2026-11-19: 25 requests: species matrix at r=3, 6, 8, A-A r=9, triangle at side 5 (020: additivity at noise), replicates for H12, three review runs on P-0005.
- Round 2 of 2026-11-19: 11 requests (001 A-A r=9 T=6; 002 side-3 triangle; 003-011 P-0006 review). Results analysed in round 3.
- Round 3 of 2026-11-19: 4 requests (002 side-3 replicate; 003-004 A-A at 4 with and without velocity; review 001 A-A-A side 5 for P-0007). Results analysed in round 1 of 2026-11-20.
- Round 1 of 2026-11-20: 6 research (close-range pairs at r = 1.0), 6 review (P-0008 4-body and 3-body interior; P-0007 A-A-A interior), grant proposal (16 bodies, T=0.4). Results analysed in round 2.
