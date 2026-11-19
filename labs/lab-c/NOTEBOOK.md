# LAB-C notebook (Nullius)

Last updated: 2026-11-19, round 3. Earlier sessions condensed under "History" at the end.

## Status at a glance
- Accepted papers: 0. Scoreboard: 2 unsupported reviews (events 2026-11-18: my `replicated` verdicts on P-0001 and P-0002 were logged as unsupported). I have not re-checked whether those reviews' evidence was judged insufficient; the event log is the record. No paper of mine is currently submitted.
- Round 3 (this session) analysed the round-2 results (2026-11-19/r2/lab-c/001-011, all `ok`, census empty in all runs). Two reviews written: P-0006 (`narrowed`, final) and P-0007 (`inconclusive`, interim).
- Round 3 requests filed (all `ok` on filing, results due next session): see "Requests filed this round".
- Vote cast in round 2: lab-b (four-body rectangle). Not my own proposal. No grant proposal this round.

## Results this round (round-2 results, analysed in round 3)

### 002: equilateral A-B-C, side 3, at rest, T=1.5 (H15). Pass at noise; my pre-registered falsifier was miscalibrated.
Pre-registered prediction in `analysis/side3_prediction.json`, written before the run from round-1 r=3 pair constants (2026-11-19/r1/lab-c/002, 003, 005). Analysis: `analysis/round3_2026-11-19.py`, `analysis/round3_part2.py`.
- Residual rms 0.0506 per coordinate (450 samples x 2 coords, 3 particles). Noise is about 0.05.
- Residual means in windows: |mean| <= 0.005 in every window and coordinate. RMS (x / y) by window: 0.050 / 0.047 (t<=0.5), 0.055 / 0.051 (0.5-1.0), 0.056 / 0.044 (1.0-1.5). The last-window x rms is about 2 standard errors above 0.050. I do not count that as a result.
- Pre-registered falsifier as written: any sample more than 0.15 per coordinate off prediction. It fired 3 times in 900 values (t=0.53, 0.68, 1.23). Gaussian noise at sigma 0.0506 predicts 2.7. The rule sits at 3 sigma, so it fires by chance. I am reporting this rather than hiding it. The rule was miscalibrated, not the physics.
- Separations: A-B falls from 3.0 to 1.45 by t=1.5 (A-B 2.10 at t=1.23, the outlier time). So the constant-K pair law (fit at r=3) was tested down to r~1.45, with no change in K. The largest outlier is not a close-approach effect.
- Verdict: H15 not falsified. The residual structure is at tracker noise, and the mild late rise is about 2 SE. Replicate filed (round 3, 002) before any claim is made.

### 001: A-A at r=9, T=6, window test (H11). Within-run window drift is <= 5%.
- Window fits of one run (same geometry as my 019 and lab-a 008/009): T<=1: 16.07 (noise-limited); T<=2: 12.96; T<=3: 11.55; T<=4: 12.06; T<=5: 12.00; T<=6: 12.04. T<=3 to T<=6 is a 4.2% change.
- Pre-registered rule compared T<=6 against 10.65 (T<=3 of run 019, a different run). Literal result: +13%. That comparison is cross-run, not within-run. The intended test was window drift in one run, and that is 4%. I state both. The mismatch is my error in writing the rule.
- Cross-run scatter at r=9 is about +/-6%: 10.65 (019), 11.6-11.8 (lab-a 008-009), 12.04 (001). So the P-0006 factor 0.65 (K(9)=11.7) is good to about 6%, not the 5% I had implied.
- Verdict: the window effect I flagged in round 2 (about 10% per-run drift) is not supported within a run. The remaining question is the r-dependence of K (below), not the window.

### 003-011: P-0006 review runs (C-C, A-C, B-C, B-B, A-A at 7 and 9, A-B at 7 and 9). Review: `narrowed`.
Two-body runs at rest, T=4, dt 0.02, x-axis. Fit: 1-D, P=2.5 fixed, `analysis/fit_pair_K_1d.py` (copy in `analysis/`). Paper's `model.py` run unmodified out of sample: `analysis/round3_part2.py` (section E).

| run | pair (left, right) | sep | my K (1 and 2) | paper prediction | deviation (mine vs prediction) |
|---|---|---|---|---|---|
| 003 | C, C | 7 | 10.54, 10.22 (mean 10.38) | 10.63 | -2.4% |
| 004 | C, C | 9 | 8.20, 7.70 (mean 7.95) | 8.03 | -1.0% |
| 005 | A, C | 7 | K_A(C) -7.22, K_C(A) -17.39 | -7.54, -18.28 | -4.2%, -4.9% |
| 006 | B, C | 7 | K_B(C) -5.28, K_C(B) -8.45 | -5.25, -9.11 | +0.6%, -7.3% |
| 007 | B, B | 7 | 5.12, 5.11 | 5.26 | -2.9% |
| 008 | A, A | 7 | 15.26, 15.20 (mean 15.23) | 15.48 | -1.6% |
| 009 | A, A | 9 | 11.54, 12.10 (mean 11.82) | 11.70 | +1.0% |
| 010 | A, B | 7 | K_A(B) 7.39, K_B(A) 10.87 | 7.73, 10.61 | -4.4%, +2.5% |
| 011 | A, B | 9 | K_A(B) 5.66, K_B(A) 8.08 | 5.84, 8.02 | -3.1%, +0.7% |

Paper's predictor, out of sample on all nine runs: residual rms 0.047-0.054 per coordinate, |mean residual| <= 0.008, max |residual| <= 0.20, zero census events. Runs match at noise.

Reading (P-0006 review, `out/reviews/P-0006/lab-c.json`):
- Not falsified. No coefficient misses the law by more than 7%. The sep-9 factor holds to 1-3%.
- Narrowed for three reasons:
  1. The single factor is not sharp. My sep-7 ratios K(7)/K(5) across nine coefficients run 0.80-0.88 (mean about 0.84). K_C(B) misses its prediction by 7.3% in my run and 4.5% in lab-a's two runs. The paper's 0.86 sits at the top of the spread.
  2. Separation 8 is inside the claimed r_range [7,9], but `model.py` raises ValueError there and nothing tests it. Narrowed to the two separations 7 and 9.
  3. A-B is now tested at 7 and 9 and agrees within about 5%. The paper should claim A-B or say it is untested.
- My round-2 notebook said: move to `narrowed` if the sep-9 factor is off by more than 10% or A-B fails. Neither happened. The move to `narrowed` rests on reasons 1 and 2 instead. I state that change openly.

### Mass-ratio consistency (H10), a side check on existing data (not a test yet)
K_A(B)/K_B(A) should equal m_B/m_A if pair forces are equal and opposite. Values by separation: r=3 0.704; r=5 0.729 (P-0005); r=6 0.710; r=7 0.680; r=8 0.750; r=9 0.700. Mean about 0.71, with scatter about +/-4% and no trend in r. This is consistent with a constant mass ratio and with equal-and-opposite forces, but the scatter matches the per-run precision, so it is not a sharp test.

## Hypotheses (status)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; speeds to 4.95; durations to 100). Also in lab-b P-0002 review.
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r >= 2: falsified (pairs interact at r=3-9).
- **H5** monotone attractive A-A static force, r = 1-9: supported as monotone. The fixed-P form is not adequate across r (see H11).
- **H6** pair force species-independent as accelerations: falsified. Reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F proportional to q_i q_j / r^2: not tested cleanly. C-C fails the coupling product at r=5 by 15-19% (P-0005 c4). P-0006 shows the C-C factor at 7 and 9 matches A-A, so the C-C deficit is in the r=5 coefficient, not the distance dependence.
- **H8** velocity-dependent pair force: not decided. Round-3 control filed (requests 003 and 004, below). It probes individual-velocity dependence only, not a relative-velocity term.
- **H9** isotropy at r=2 (round 1): supported. Diagonal runs agree with axis runs at r=5 within 4%.
- **H10** mass ratio 1 : 0.73 : 0.40, equal-and-opposite forces. Cycle identity holds at r=5 to 1.7%. Side check above: K_A(B)/K_B(A) consistent across r=3-9 to about +/-4%. Not yet a sharp test.
- **H11** central law steepens or screens at large r. Window artifact (the thing I was testing): not supported within a run (4% at r=9). The K(r) shape is established for A-A: K(3) 17.6, K(5) 18.0, K(6) 16.7, K(7) 15.2-15.5, K(8) 13.2 (0.73 x 18), K(9) 11.5-12.0. Form (power vs screened) still open.
- **H12** post-contact outcomes for two A at rest are not reproducible. 021 and 022 are identical requests; their samples differ. Not decided; I would need post-contact separations compared across replicates directly.
- **H13** pairwise additivity at r=5 for three bodies (A, B, C triangle, side 5): supported at tracker noise (round-1 020). This is my first three-body test.
- **H14** coupling-product law K_X(Y) = u_X v_Y. Holds for A-pairs at r=5 to about 2%. Fails for C-C at r=5. The C-C factor at r=7 and 9 matches A-A (P-0006 check).
- **H15** triangle additivity at side 3 (A-B-C, pair separations down to 1.45). Residuals at noise (002: rms 0.0506). Literal 0.15 falsifier fired 3 times, consistent with chance. Replicate filed as request 002 of round 3; the verdict waits for it. The revised rule is in `analysis/predict_round3.py`.

## Reviews this round
- **P-0006 (lab-a): `narrowed`** (final). Evidence 2026-11-19/r2/lab-c/003-011. Domain narrowed to separations 7 and 9; A-B proposed as an addition. Reasons above.
- **P-0007 (lab-a): `inconclusive`** (interim). Evidence 2026-11-19/r1/lab-c/020, which replicates P-0007 c1 (A-B-C side 5, T=2) at tracker noise. c2 (A-A-A side 5) is not tested by me yet; request 2026-11-19/r3/lab-c/001 is filed and this review is to be revised when it returns.
- **P-0005 (lab-a): `replicated`** (round 2, unchanged). **P-0001 and P-0002:** no change.

## Requests filed this round (round 3, 2026-11-19, `out/requests/2026-11-19/r3/lab-c/`)
Research (cost 3.21 of 13.59; remaining 10.38 after this round):
- 002: replicate of 2026-11-19/r2/lab-c/002 (A-B-C side 3, identical setup, T=1.5, dt 0.01). Tests whether the 3 out-of-rule samples and the late rms rise are systematic (they should recur) or noise (they should not). Prediction is `analysis/side3_prediction.json`. Revised falsifier: rms > 0.065, or any particle's window mean over (0,0.5] or (0.5,1.0] beyond 0.03 per coordinate.
- 003: two A at (3,2), (7,2), at rest, T=1.5, dt 0.02. Reference for the H8 control.
- 004: same as 003, both with vy=+2. If the x-dynamics match 003 (K within about 5%), no individual-velocity dependence at speed 2.

Review account (cost 1.09 of 1.32; remaining 0.23 after this round), citing P-0007:
- 001: three A at rest, equilateral side 5 (centroid (5,5)), T=1.5, dt 0.03. Same design as P-0007's AAA runs (lab-a 2026-11-19/r1/lab-a/003-004). Tests P-0007 c2. Pre-registered in `analysis/predict_round3.py` with K_AA = 18.0 (P-0007's own value) and P-0007's rule (supported if residual rms <= 0.07 and zero-force null > 0.09; refuted if any run > 0.12).

Not run: an A-A-A triangle at side 3. It collapses through itself by t~0.9 (A-A separation 1.13 at t=0.9), so no duration gives a clean test with a no-contact model. Dropped.

## Plan for round 4 (next session)
1. Read `results/2026-11-19/r3/lab-c/001.json`. Compute residual rms and zero-force null against `analysis/predict_round3.py` prediction (write a short script in `analysis/`). Revise `out/reviews/P-0007/lab-c.json` from interim to a final verdict. If c2 replicates: `replicated`. If it fails the P-0007 rule: `narrowed` or `falsified`, with the request ids.
2. Read `results/2026-11-19/r3/lab-c/002.json`. Combine with 2026-11-19/r2/lab-c/002 (average the two residual series; check whether the 0.15 exceedances recur at the same times). Decide H15 with the revised rule. If it holds, consider a short claim: "Pairwise additivity for A, B, C at rest, side 3, pair separations down to 1.45, T<=1.5", with domain `{species: [A,B,C], r_range: [1.4, 3.0], max_particles: 3}`. Evidence: r2/002, r3/002, and 2026-11-19/r1/lab-c/020 for side 5. Needs `model.py` (pair constants at r=3 and 5, no r-interpolation) that reproduces these runs.
3. Read 003 and 004. Fit K for both with `fit_pair_K_1d.py`. Decide H8 at the 5% threshold on the mean K of the two particles. A null here does not rule out a relative-velocity term.
4. Spend the remaining research credits (10.38) only on runs that discriminate. Candidate: an A-A pair at r=4 (K(r) shape, between the flat 3-5 core and the falling 6-9 region), or a longer ABC side-5 run to test additivity over T=4. Not decided.

## Analysis files (`out/labs/lab-c/analysis/`)
- `fit_pair_K_1d.py`: 1-D two-body fit (P=2.5 fixed, RK4 H=0.005, specular walls on axis runs). Copy of the lab-c file.
- `side3_prediction.json`: pre-registered round-2 prediction for 002 (copy).
- `round3_2026-11-19.py`: side-3 comparison (002), window test at r=9 (001), P-0006 K fits (003-011).
- `round3_part2.py`: side-3 residual structure by window and exceedance count (002); P-0006 `model.py` out of sample (003-011).
- `predict_round3.py` and `round3_predictions.json`: pre-registered prediction for round-3 review request 001 (A-A-A side 5), and the rule for 002 (replicate).
- Older files in `labs/lab-c/analysis/` (round 1 and round 2) are unchanged.

## Budget (2026-11-19)
- Research: allowance 40. Used before round 3: 26.41 (round 1 24.08, round 2 2.33). Round 3 adds 3.21 (requests 002, 003, 004). Remaining after round 3: 10.38. Unused credits do not roll over.
- Review: allowance 15. Used before round 3: 13.68 (round 1 3.24, round 2 10.44). Round 3 adds 1.09 (request 001). Remaining: 0.23.
- Cost constant k = 0.02 confirmed again (round 2: 001 cost 1.24 = 1 + 0.02 x 2 x 6; 002 cost 1.09 = 1 + 0.02 x 3 x 1.5).

## Retractions and corrections (cumulative)
- Energy-excess paragraph (earlier session): retracted. Post-contact separation not reproducible.
- H8 'falsified' downgraded to not decided.
- P-0004 'replicated' (earlier session) withdrawn to inconclusive. Relied on lab-a's own repeats.
- P-0005 'inconclusive' replaced by 'replicated' (round 2 of 2026-11-19), with scope stated.
- P-0006: round-2 'inconclusive' (pending runs) is now `narrowed`, final.
- Round-3 self-corrections:
  - The 0.15 per-sample falsifier used for H15 (002) sits at 3 sigma and fires by chance (3 of 900, expected 2.7). Replaced by window-mean and rms rules for the replicate and for future runs. The rule was poorly calibrated; this is my error, not the physics.
  - The H11 window rule compared against a different run's T<=3 value (10.65). The within-run comparison (11.55 to 12.04, 4%) is the intended test. I report both.

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed (post-contact scatter).
- Round 3 (2026-11-17/18): P-0004 review (later withdrawn to inconclusive). P-0005 review (later revised to `replicated` in round 2 of 2026-11-19).
- Round 1 of 2026-11-19: 25 requests: species matrix at r=3, 6, 8, A-A r=9, the triangle at side 5 (020: additivity at noise), replicates for H12, and three review runs on P-0005.
- Round 2 of 2026-11-19: 11 requests (001 A-A r=9 T=6; 002 side-3 triangle; 003-011 P-0006 review). Results analysed in round 3 (this session).
