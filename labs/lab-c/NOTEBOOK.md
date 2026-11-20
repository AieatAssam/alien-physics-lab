# LAB-C notebook (Nullius)

Last updated: 2026-11-20, round 3. Earlier rounds condensed under "History".

## Status at a glance
- Accepted papers: 0. No paper of mine is submitted. Unsupported reviews on the scoreboard: 2 (2026-11-18, my `replicated` verdicts on P-0001 and P-0002). Before any `replicated` verdict I now check the judge's bar against the runs I cite.
- Reviews (final this round): **P-0009 (lab-a) `replicated`** and **P-0010 (lab-keystone) `narrowed`**, both finalising my round-2 interim reviews. Standing reviews from earlier rounds: P-0007 narrowed, P-0008 replicated, P-0011 replicated, P-0005 replicated.
- Round 2 results are in (001-007). The short-range result is now the main line of work: at r0 = 1.5 to 2.5, all pairs I have run move more slowly than the P-0008 law (K/r^2.5, P-0005 coefficients) predicts. The best-fit coupling scale is 0.75 to 0.92, and single runs fit at noise. Not yet replicated.
- A-A coefficient in P-0010: my round-2 claim (A-A 2-4% low at r0 6-9) is withdrawn. Two new long runs give s = 0.974 at r0 6 (pre-approach) and 0.995 at r0 8. Sign was also wrong in the review text (see Corrections).
- New domain failure: P-0010's A-A pair at r0 6 at rest collides by t about 4.1 and the model blows up (2026-11-20/r2/lab-c/002). P-0010's domain has no closest-approach limit.
- Round 3 requests filed: 17 research, about 17.8 of the 29.84 research credits left today. Review account: none filed (no paper awaiting my review); 4.89 review credits unused today.

## Judging rules (carried forward)
- Judged error (tools/editor.py): sqrt(mean over particle-samples of |dpos|^2) / 10. Noise floor with tracker noise 0.05 per coordinate: sqrt(2) x 0.05 / 10 = **0.0071**.
- Replicate bar: 3 x predicted_error on cited in-domain runs that the paper's model.py scores. A run the model refuses (ValueError) does not count.
- Judged domain checks species, particle count, and initial pairwise separations. It does not check velocity, duration (except where a model raises), or closest approach.
- The judged metric cannot resolve a few-percent coupling error at this noise, and it cannot falsify a short-range claim whose pe is 0.01 (bar 0.03). For coupling claims I use a per-run scale fit (chi-square at sigma 0.05 per coordinate), with a time-block jackknife, not Delta-chi2 = 1 (which underestimates the error; see Corrections).
- Pre-registered falsifiers on single samples are miscalibrated: a separation has noise 0.071. Use window means against the noise, and check the window does not contain a model artefact (see H16 and Corrections).

## Round 2 results (2026-11-20/r2/lab-c/001-007)

### A. Short-range pairs at rest, pre-registered on the P-0008 law (004-007)
Predictions: `out/labs/lab-c/analysis/pred_2026-11-20_r2_shortrange.json`, regenerated from the pre-registration script (the repo copy was missing). Endpoints match the stated predictions (6.25, 2.23, 0.49, 1.74).

Pre-registered falsifiers, as written in each request:
| run | pair, r0, T | valid window | late-window mean residual (measured minus predicted) | falsifier | status |
|---|---|---|---|---|---|
| 004 | AA, 1.5, 0.4 | pred >= 0.5 | -0.89 (window contaminated by post-contact artefact) | fires if > +0.1 | did not fire; test invalid as designed |
| 005 | AC, 1.5, 0.4 | all | -0.093 +/- 0.008 (block SE) | fires if < -0.1 | did not fire (just short) |
| 006 | CC, 1.5, 0.4 | all | +0.104 +/- 0.019 | fires if > +0.1 | fires marginally (0.3 sigma above threshold) |
| 007 | AA, 2.5, 1.0 | pred > 1.7 | -2.64 (window contaminated by post-contact artefact) | fires if > +0.1 | did not fire; test invalid as designed |

**The 004 and 007 windows are invalid.** The P-0008 integrator's singular 1/r^2.5 force collides in the prediction (004 at t about 0.35, 007 at t about 0.87) and then rebounds to 6.25 and 4.7 at the ends of the runs. The pre-registered gate (pred >= 0.5) does not exclude the rebound. That is my design error.

Time series (measured minus predicted; noise 0.07 per sample):
- 004 (AA, r0 1.5): agrees to t about 0.2; from t 0.24 to 0.34 the measured separation is 0.1 to 0.4 larger than predicted. The prediction collides at t about 0.35; the measured pair is still at 0.33-0.8 at t 0.36-0.40 and does not collide before T.
- 007 (AA, r0 2.5): agrees to t about 0.6. From t 0.65 to 0.85 measured is 0.1 to 0.4 larger. The measured pair reaches contact near t 0.93 (minimum 0.015), later than the predicted contact near 0.87.
- 005 (AC, repulsive): measured is slightly below predicted from t about 0.2 (about -0.1 at t 0.36-0.40).
- 006 (CC): measured is slightly above predicted near the end, concentrated in t 0.36-0.40 where the prediction is near contact (0.5-0.8).

### B. Coupling-scale fit on short-range runs (`out/labs/lab-c/analysis/scale_fit_short_range.py`, post-hoc window)
Model: P-0008 law with every coefficient times s. Window: samples before each scale's own predicted separation drops below 0.6 (rebound-independent). chi2/n is per separation sample, sigma 0.071. Full output: `scale_fit_short_range_2026-11-20.txt`.

| run | pair, r0, T | best s | jackknife SE (5 time-blocks) | chi2/n at best s | chi2/n at s = 1 |
|---|---|---|---|---|---|
| 004 | AA, 1.5, 0.4 | 0.753 | 0.006 | 1.05 | 3.19 |
| 005 | AC, 1.5, 0.4 | 0.811 | 0.007 | 0.98 | 1.65 |
| 006 | CC, 1.5, 0.4 | 0.874 | 0.006 | 0.96 | 1.56 |
| 007 | AA, 2.5, 1.0 | 0.924 | 0.004 | 0.98 | 2.13 |

Reading: at each best s, chi2/n is at the noise floor (about 1), while s = 1 is clearly rejected. The per-run jackknife errors are too small for model systematics; I quote s to about +/- 0.02 for now. The deficit is weaker at 2.5 than at 1.5 for AA. A single scale per run cannot separate a coupling offset from a change in shape (softening, or a different exponent). A pure exponent change (r/5)^q fits the two AA points badly (q = 0.12 from 2.5 predicts 0.87 at 1.5, not 0.75), so this is not a simple exponent shift.

**H16 status: supported in direction, not established.** Four runs, each a single run per pair, species-dependent scale (AA 0.75 at 1.5, AC 0.81, CC 0.87; AA 0.92 at 2.5). Replicates and the shape series in round 3 are needed.

### C. Long A-A runs and the P-0010 coefficient (002, 003; `out/labs/lab-c/analysis/review_runs_2026-11-20.py`)
- **003 (A-A, r0 8, at rest, T=6; minimum separation 4.53):** judged 0.00728 (noise). Full-run coupling scale s = **0.995** (chi2/N 1.06; scan grid 0.90-1.10). This does not reproduce my earlier A-A value at 8 (0.949-0.959 from two runs; about 2-3 sigma apart).
- **002 (A-A, r0 6, at rest, T=6; minimum separation 0.04, collision near t about 4.0-4.1):** the model's error exceeds 0.2 first at t = 4.12 (judged 281). Pre-approach window (t <= 3.96, separation above 1.5): s = **0.974** (chi2/N 1.03 at best).
- P-0010 has no closest-approach limit in its claim, so 002 is inside its stated domain and the model fails there.

### D. Three-body replicate (001: B, C, C equilateral, side 5, at rest, T=2; P-0009 c1)
- Judged 0.00714 (bar 0.03). Per-coordinate rms 0.0505 (bar 0.07). Zero-force null on the same run: 0.140. No census events. This supports P-0009 c1 at noise, one run.

## Round 1 close-range results (2026-11-20/r1/lab-c/001-006, r0 = 1.0, T = 0.2; unchanged from round 2)
- AA never collapses within T=0.2 (min 0.42); P-0008 predicts collision at t about 0.175. AB, AC, BC: measured separations larger than predicted from t about 0.10 for attractive pairs, smaller than predicted for repulsive pairs. BB shows no deviation (about 0). CC: larger than predicted from t about 0.10.
- Pre-registered 0.1 per-sample falsifier was miscalibrated; window-mean reading used.

## Reviews this round (out/reviews/)
- **P-0009 (lab-a): `replicated` (final).** Evidence: 2026-11-20/r2/lab-c/001 (three-body) and 2026-11-19/r1/lab-c/023, 024, 025 (two-body at side 5). All four are inside the claim's stated domain and score 0.0070-0.0071 against the bar of 0.03. Comment says that only one of the four is three-body.
- **P-0010 (lab-keystone): `narrowed` (final).** Evidence adds 002 and 003. Proposed domain: species B and C only, r 6-9, max 2 (conservative; AB and AC also within about 5%). Comment records the closest-approach failure and the corrected A-A values.

## Requests filed this round (out/requests/2026-11-20/r3/lab-c/001-017)
All research account, two particles at rest unless noted. Cost = 1 + 0.02 x particles x T. Pre-registered expected s ranges are in each request's purpose.

| id | pair | r0 | T | dt | expected s | what it tests |
|---|---|---|---|---|---|---|
| 001 | AA | 1.0 | 0.3 | 0.0002 | 0.55-0.80 | trend continues at r 1.0 (falsifier: s >= 0.90) |
| 002 | AA | 2.0 | 0.6 | 0.0004 | 0.80-0.90 | interpolation between 1.5 and 2.5 |
| 003 | AA | 3.0 | 2.0 | 0.001 | 0.97-1.03 | P-0008 domain edge (2.95). **Discriminating:** a monotone rise to 5 would give about 0.94 here; falsifier s < 0.95 |
| 004 | AA | 3.5 | 1.5 | 0.00075 | 0.97-1.03 | inside P-0008 domain |
| 005 | AA | 4.0 | 2.0 | 0.001 | 0.98-1.03 | inside P-0008 domain |
| 006 | AA | 1.5 | 0.4 | 0.0002 | 0.70-0.80 | replicate of 2026-11-20/r2/lab-c/004 |
| 007 | AB | 1.5 | 0.4 | 0.0002 | 0.75-0.95 | does AB show the deficit? |
| 008 | AC | 1.5 | 0.4 | 0.0002 | 0.76-0.86 | replicate of r2/005 |
| 009 | AC | 2.5 | 1.0 | 0.0005 | 0.85-0.97 | repulsive pair at 2.5 |
| 010 | BB | 1.5 | 0.4 | 0.0002 | 0.97-1.03 | species test (round 1 BB showed none) |
| 011 | BC | 1.5 | 0.4 | 0.0002 | 0.75-0.95 | repulsive B-C at 1.5 |
| 012 | CC | 2.5 | 1.0 | 0.0005 | 0.90-1.00 | CC at 2.5 |
| 013 | BB | 2.5 | 1.0 | 0.0005 | 0.97-1.03 | BB at 2.5 |
| 014 | CC | 1.5 | 0.4 | 0.0002 | 0.82-0.92 | replicate of r2/006 |
| 015 | AC | 3.0 | 2.0 | 0.001 | 0.97-1.03 | P-0008 domain edge for AC (falsifier s < 0.94) |
| 016 | CC | 3.0 | 2.0 | 0.001 | 0.97-1.03 | P-0008 domain edge for CC (falsifier s < 0.94) |
| 017 | AA | 7.0 | 3.0 | 0.0015 | 0.96-1.02 (vs P-0010) | P-0010 range, before approach |

Estimated cost 17.75 of 29.84 research credits left today. Unused credits do not roll over.

## Hypotheses (status)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; T to 100).
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r >= 2: falsified (pairs interact at r = 3-9).
- **H5** monotone attractive A-A static force, r = 1-9: supported as monotone; fixed-P form not adequate (H11).
- **H6** pair force species-independent as accelerations: falsified; reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F proportional to q_i q_j / r^2: not tested cleanly; C-C fails the coupling product at r=5 by 15-19% in P-0005's c4, but P-0009's pair check (C-C 1.01 +/- 0.01 at r=5) agrees with P-0005. These two statements conflict; not resolved.
- **H8** velocity-dependent pair force: partially tested; 2026-11-19/r3/lab-c/004 vs 003 matches at noise. Not quantified at 5%.
- **H9** isotropy at r=2 (round 1): supported.
- **H10** mass ratio 1 : 0.73 : 0.40, equal-and-opposite forces. Cycle identity holds at r=5 to 1.7%.
- **H11 (reframed)** effective pair coupling depends on separation, with a maximum near r = 4-5. Relative to P-0008's A-A coefficient of 18, the scales are: 0.75 (r 1.5), 0.92 (r 2.5), 1.00 (r 5, anchor), about 0.93 (r 6), about 0.77 (r 8), about 0.66 (r 9). The 6-9 values use P-0010's radial factor G(r) and so are not independent of it. Round-3 runs 001-005 and 017 test the shape. Not established.
- **H12** post-contact outcomes for two A at rest are not reproducible (2026-11-19/r1/lab-c/021 and 022 are identical requests; samples differ). Not decided.
- **H13** pairwise additivity at r=5 for three bodies (ABC triangle, side 5): supported at tracker noise.
- **H14** coupling-product law K_X(Y) = u_X v_Y: holds for A-pairs at r=5 to about 2%; C-C conflicts (see H7).
- **H15** triangle additivity at side 3 (A-B-C): supported at noise. Closed.
- **H16 (main question, open)** short-range pair law, r below about 3. Round 2: all four runs fit s < 1 (AA 0.75 at 1.5 and 0.92 at 2.5; AC 0.81 and CC 0.87 at 1.5). Round 1 r0 = 1 runs agree in sign for attractive and repulsive pairs. Open: is the deficit a scale or a shape change; is it species-dependent (round 3 010 says BB shows none in round 1); where does it end (round 3 003, 015, 016 test P-0008's domain edge at 3). Species: round-1 BB showed no deviation; request 010 (BB at 1.5) tests it. Replicates 006, 008, 014 test reproducibility.
- **H18 (retracted in part)** P-0010 A-A coefficient 2-4% high at r0 6-9. Now: s = 0.974 at 6 (pre-approach), 0.995 at 8 (full run). At 8 the earlier value does not replicate. At 6 the paper is about 3% too strong. Status: weak; round 3 017 at r0 7 is the next test.
- **H19** P-0005 pair coefficients at separation 5 hold to 1-2% for BB, BC, CC on 2-body runs (P-0009 pair part). Three-body part (P-0009 c1) now supported at noise by 001.
- **H20** tracker noise per coordinate 0.0507 (lone particles, pooled); P-0011 c1 is about 2 sigma above 0.050.
- **H21 (new)** P-0010's closest-approach failure: A-A at r0 6 at rest collides by t about 4.1; the model's error passes 0.2 at t = 4.12. Supported by one run (002). Other pair types at r0 6-9 with T up to 6 have not been checked for close approach.

## Corrections and retractions (cumulative)
- **This round:** my round-2 review of P-0010 said "A-A is 2-4% low". The sign was wrong: a scale below 1 means the paper's coefficient is too large. The final review corrects this.
- **This round:** my round-2 A-A value at r0 8 (0.949-0.959) does not replicate: 003 gives 0.995. I no longer claim an A-A deficit at 8.
- **This round:** the pre-registered falsifiers for 004 and 007 were contaminated by the P-0008 integrator's post-contact rebound (the pred >= 0.5 gate does not exclude it). They are not valid tests. Replaced by the pre-collision scale fit above (post-hoc window, stated as post-hoc).
- **This round:** the pre-registered prediction JSON the requests cite was missing from the repository. Regenerated from the same script into `out/labs/lab-c/analysis/`; endpoints match the notebook's previous values.
- **This round:** Delta-chi2 = 1 errors from the scale scan (for example +/- 0.003 on 004) are far too small, because successive samples carry correlated model error. Use the jackknife SE and quote s to about +/- 0.02.
- **This round:** the round-2 summary said the P-0010 A-A coefficient is "outside its own 3% tolerance". The claim text states no explicit tolerance; I should not have written that.
- **Earlier this round (round 2):** the judged noise floor is 0.0071 (Euclidean RMSE / 10), not 0.005. The P-0008 falsifier windows and the round-1 0.1 per-sample falsifier were miscalibrated (replaced by window means).
- **Round 3 of 2026-11-19:** the 0.15 per-sample falsifier for H15 was miscalibrated. My error, not the physics.
- **Earlier:** energy-excess paragraph retracted (post-contact separation not reproducible). H8 'falsified' downgraded to not decided. P-0004 'replicated' withdrawn to inconclusive. P-0005 'inconclusive' replaced by 'replicated' with scope.

## Plan for next session
1. Read 2026-11-20/r3/lab-c/001-017 when they return. Score each with the scale fit (`scale_fit_short_range.py`, adapting the run list) and compare with the expected ranges above. Check the replicates (006, 008, 014 against 004, 005, 006) before anything else.
2. **Publication decision, pending the replicates.** If 014 (CC at 1.5) and 006 agree with s about 0.87 within 0.03, file a narrow claim: C-C pair at rest, r0 in [1.45, 1.55], T <= 0.4, coefficient P-0005 times 0.87. Set predicted_error from the replicate scatter, not 0.01. Say in the paper that the judged metric cannot discriminate at this noise. Do not publish any close-* bounty claim (r0 <= 1) yet: the power law fails there and I have no model that predicts r0 = 1.
3. Shape test: if 003 (AA, 3.0) gives s in [0.97, 1.03] and 009 (AC, 2.5) and 012 (CC, 2.5) agree with 2.5 values above, the deficit is confined to r below about 2.5, and H16 becomes a short-range cutoff question. If 003 gives s below 0.95, P-0008 is wrong inside its own domain at r 3 and I should say so in a review when a P-0008-based paper is next under review.
4. P-0010: no further A-A tests needed beyond 017 (r0 7). Watch for a closest-approach limit in any follow-up paper; flag any paper whose domain includes pairs approaching under about 1.5.
5. The grant (Plumbline, lab-a, close-CC at r 2) will produce data; compare with 006 and 014 when it returns.

## Analysis files (out/labs/lab-c/analysis/)
- `pred_2026-11-20_r2_shortrange.json`: pre-registered short-range predictions (regenerated).
- `analyze_r2_short_range.py`: round-2 pre-registered window test (shows the contamination for 004 and 007).
- `scale_fit_short_range.py` and `scale_fit_short_range_2026-11-20.txt`: coupling-scale fit for 004-007 (pre-collision window, floor-based cut, time-block jackknife).
- `review_runs_2026-11-20.py` and `.txt`: 001 (P-0009 bar and null), 002 and 003 (P-0010 judged error, approach time, scale fit).
- `inventory_r3_2026-11-20.txt`: scored inventory of all lab-c runs (from the repository's inventory script).
- `make_2026-11-20_r3_requests.py`: generates the 17 round-3 requests (in `out/requests/2026-11-20/r3/lab-c/`).
- Reviews: `out/reviews/P-0009/lab-c.json`, `out/reviews/P-0010/lab-c.json`.
- Older analysis (rounds 1-2): `labs/lab-c/analysis/` in the repository, including `coupling_scale_scan.py`, `close_range_check_2026-11-20.py`, `r2_pair_check.py`, `lone_noise_check_2026-11-20.py`, `inventory_2026-11-20.py`.

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed. P-0004 review (later withdrawn to inconclusive).
- Round 3 (2026-11-17/18): P-0005 review (later revised to `replicated`).
- Round 1 of 2026-11-19: 25 requests: species matrix at r=3, 6, 8, A-A r=9, triangle at side 5, replicates for H12, three review runs on P-0005.
- Round 2 of 2026-11-19: 11 requests (A-A r=9 T=6; side-3 triangle; P-0006 review runs). Analysed in round 3 of 2026-11-19.
- Round 3 of 2026-11-19: 4 requests (side-3 replicate; A-A at 4 with and without velocity; P-0007 review run). Analysed in round 1 of 2026-11-20.
- Round 1 of 2026-11-20: 6 research (close-range pairs at r = 1.0), 6 review (P-0008 and P-0007 replicates), grant proposal (16 bodies, T=0.4). Analysed in round 2.
- Round 2 of 2026-11-20: 7 requests (3 review: P-0009 BCC side 5, P-0010 A-A at 6 and 8; 4 research: short-range AA, AC, CC at 1.5 and AA at 2.5). Vote for lab-a (Plumbline, close-CC). Analysed in round 3 (this file).
