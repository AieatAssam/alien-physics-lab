# LAB-C notebook (Nullius)

Last updated: 2026-11-20, round 1. Earlier sessions condensed under "History" at the end.

## Status at a glance
- Accepted papers: 0. Scoreboard: 2 unsupported reviews (2026-11-18: my `replicated` verdicts on P-0001 and P-0002). The unsupported-review cause is not in my notes; the event log is the record. No paper of mine is currently submitted.
- This session: inventoried all my in-domain runs against P-0008 (lab-b's paper, the only one awaiting my review). Found that every in-domain run at rest with pairs kept above about 1.5 apart matches P-0008's law at tracker noise. Failures are all close-approach or long-duration runs.
- Interim reviews written: P-0008 (`inconclusive`), P-0007 (`inconclusive`, revised from round-3 interim after its round-3 replicate passed P-0007's own rule).
- Requests filed this round: 6 research (close-range pairs, bounty-relevant), 6 review-account (P-0008 c1/c2 interior tests, P-0007 c2 interior replicates). Grant proposal filed (16-body lattice).
- H15 is now supported at tracker noise (see Hypotheses). The 0.15 per-sample falsifier that fired three times was miscalibrated (my error).

## Judging rules I now apply (my own reading, to keep my thresholds honest)
- Judged error = RMSE / 10 (chamber side). Replication bar = 3 x predicted_error. For P-0008 and P-0007 that is 0.21 normalized = 2.1 absolute. Noise is 0.05 absolute (0.005 judged). A bar 40 times the noise cannot separate a correct law from one that misses by a unit. I raise this in the reviews.
- I write all my own thresholds in absolute units (position rms per coordinate), and convert to judged units only when comparing to the judge's bars.
- The judged domain checks species, particle count and initial pairwise separations only. It does NOT check duration, velocity, or closest approach. Papers whose statements say "T <= 1, at rest" can be judged on runs at T=10 or on runs that collide. I cite runs honestly against the statement scope and say so in the comment.
- Endpoint runs (initial separation exactly 3.0 or 5.0) are at the boundary of a closed range. Floating-point distances can land just outside. I do not rely on them as judged evidence; I cite interior runs and mention endpoint runs in comments only.

## Results this round

### Inventory of my in-domain runs against P-0008 (`analysis/p0008_inventory.py`, output `analysis/p0008_inventory_2026-11-20.txt`)
31 ok runs of mine fall inside P-0008's judged domain (species A/B/C, 2 to 4 bodies, all initial separations in [3,5]). Scored with P-0008's model.py unmodified:

| class | runs | judged error (rms/10) | reading |
|---|---|---|---|
| 2-body, separation 4.0, at rest or moving, T 0.8 to 1.5 | 2026-11-17/r3/003; 2026-11-18/r1/004, 005, 007, 008; 2026-11-19/r3/003, 004 | 0.0050 to 0.0050 (all) | at noise. 2026-11-19/r3/004 has vy=2 and matches too |
| 2-body, separation 3.0 or 5.0 (endpoints), T 1.0 to 2.0 | 2026-11-19/r1/001-006, 023-025 | 0.0049 to 0.0051 | at noise, including BB, CC, BC, AC |
| 3-body, endpoints 3.0 (ABC, T=1.5) | 2026-11-19/r2/lab-c/002, r3/002 | 0.0497, 0.0508 | at noise (rms per coordinate) |
| 3-body, endpoint 5.0 (ABC T=2; AAA T=1.5) | 2026-11-19/r1/lab-c/020, r3/lab-c/001 | 0.0507, 0.0486 | at noise |
| 2-body, separation 3.0, at rest, T=2 (contact at t about 1.25) | 2026-11-18/r2/001; 2026-11-19/r1/021, 022 | 0.13 | misses by 1.3 absolute; minimum measured separation 0.01 to 0.05 |
| 2-body, T=10, moving or at contact | 2026-11-17/r1/003 (AA at 4.47, moving; minimum not checked), r2/002 (AB at 4.47, moving), r2/003 (BB, moving), r2/004 (AA, moving), r2/009 (CC, moving), r2/001 (AA at 3.0, at rest) | 0.27 to 0.49 (r2/001: 4443) | r2/002, 003, 004, 009 and r2/001 approach below 1 (minima 0.02 to 0.81) |
| 2-body AC, T=10 | 2026-11-17/r2/lab-c/008 | 0.0085 | matches; minimum separation 2.73 |

Contact diagnosis (`analysis/p0008_failures.py`): every failure has a measured minimum pair separation at or below 0.8. The one run that stayed above 1.4 (2026-11-19/r1/lab-c/001, A-A at 3, minimum 1.43 at t=0.99) matches at noise in its first window and drifts to rms 0.069 in the second window, as the pair approaches 1.4. That is the first hint of a deviation near r of 1.4. It is not established.

Note on the scoring: the judge's replication bar (0.21 judged) is easy for any run that does not collide. A collision run with error 1.3 absolute still counts as "in bar" by the judge's rule. So the bar is not evidence of the law at contact.

### P-0007 c2 rule on 2026-11-19/r3/lab-c/001 (`analysis/p0007_c2_check.py`)
Three A at rest, equilateral, side 5.0, T=1.5, 51 samples.
- Residual rms per particle (vs P-0008 law, A-A = 18.0): 0.0529, 0.0504, 0.0417 per coordinate. Overall 0.0486. Rule: <= 0.07. Pass.
- Zero-force null rms per particle: 0.216, 0.222, 0.219. Rule: > 0.09. Pass.
- Rule supported. The side-5 endpoint is the only 3-body A run I have at this geometry. Two interior replicates are filed (below).

### H15 side-3 triangle (A-B-C, equilateral, side 3.0, T=1.5)
- 2026-11-19/r2/lab-c/002: residual rms 0.0497 (P-0008 law). Round-2 pre-registered prediction (from analysis/side3_prediction.json) was written before the run.
- 2026-11-19/r3/lab-c/002: replicate, residual rms 0.0508.
- The 0.15 per-sample falsifier fired 3 times in 900 values (t=0.53, 0.68, 1.23). At sigma 0.0506 that is expected by chance (about 2.7). My rule was miscalibrated; the physics is not.
- Verdict: H15 supported at tracker noise for A-B-C at side 3.0 down to pair separations near 1.45 (round-2 002 late window).

## Hypotheses (status)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; speeds to 4.95; durations to 100). Also in lab-b P-0002 review.
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r >= 2: falsified (pairs interact at r=3-9).
- **H5** monotone attractive A-A static force, r = 1-9: supported as monotone. Fixed-P form not adequate across r (see H11).
- **H6** pair force species-independent as accelerations: falsified. Reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F proportional to q_i q_j / r^2: not tested cleanly. C-C fails the coupling product at r=5 by 15-19% (P-0005 c4). P-0006 shows C-C at 7 and 9 matches A-A, so the C-C deficit is in the r=5 coefficient, not the distance dependence.
- **H8** velocity-dependent pair force: partially tested. 2026-11-19/r3/lab-c/004 (A-A at 4, vy=2 each) matches the velocity-independent pair law at noise (rms 0.050), as does the at-rest twin 003 (rms 0.050). Sensitivity is not yet quantified: I have not checked how much a 5% K change would move these runs. A null here does not rule out a relative-velocity term.
- **H9** isotropy at r=2 (round 1): supported. Diagonal runs agree with axis runs at r=5 within 4%.
- **H10** mass ratio 1 : 0.73 : 0.40, equal-and-opposite forces. Cycle identity holds at r=5 to 1.7%. K_A(B)/K_B(A) consistent across r=3-9 to about +/-4%. Not yet a sharp test.
- **H11** central law steepens or screens at large r. Window artifact not supported within a run (4% at r=9). K(r) for A-A: K(3) 17.6, K(5) 18.0, K(6) 16.7, K(7) 15.2-15.5, K(8) 13.2, K(9) 11.5-12.0. Form (power vs screened) still open.
- **H12** post-contact outcomes for two A at rest are not reproducible. 021 and 022 are identical requests; their samples differ. Contact at t about 1.25 (2026-11-19/r1/lab-c/021, 022). Not decided.
- **H13** pairwise additivity at r=5 for three bodies (ABC triangle, side 5): supported at tracker noise (round-1 020, and P-0008 law gives 0.0507).
- **H14** coupling-product law K_X(Y) = u_X v_Y. Holds for A-pairs at r=5 to about 2%. Fails for C-C at r=5. The C-C factor at r=7 and 9 matches A-A.
- **H15** triangle additivity at side 3 (A-B-C): supported at noise (see above). Closed.
- **H16 (new, open)** close-range law (r = 1 to 3). P-0008's law is only tested at r >= 2.95 and at its endpoints. Contact runs fail. Whether K/r^2.5 holds below about 1.5 is open. Round-1 research 001-006 (below) tests all six pair types at r=1.0.
- **H17 (new, open)** many-body additivity beyond 4 bodies. Untested by me. Grant proposal (16-body lattice, T=0.4) is the test.

## Reviews this round
- **P-0008 (lab-b, four-body rectangle and three-body triangles): `inconclusive`, interim.** Evidence: seven in-domain 2-body runs at separation 4.0 (2026-11-17/r3/lab-c/003; 2026-11-18/r1/lab-c/004, 005, 007, 008; 2026-11-19/r3/lab-c/003, 004), all at noise. The 3-body claim (c2) rests on endpoint runs I have not cited. The 4-body claim (c1) is untested by me. Comment also covers: the judged domain omits duration, velocity and closest approach; contact breaks the law; predicted_error 0.07 is 14x the noise floor. Final verdict pending review-account runs 007-010.
- **P-0007 (lab-a): `inconclusive`, interim (replaces round-3 interim).** Evidence: 2026-11-19/r3/lab-c/001 (passes P-0007 c2 rule) and 2026-11-19/r1/lab-c/020 (c1 replicate at noise). The replicated bar needs three in-domain c2 runs; I have one at the endpoint. Pending review-account runs 011 and 012 (interior sides 4.5 and 4.0).
- **P-0006 (lab-a): `narrowed`** (final, round 3). Unchanged. **P-0005 (lab-a): `replicated`** (round 2, unchanged). **P-0001 and P-0002:** no change.

## Requests filed this round (`out/requests/2026-11-20/r1/lab-c/`, results due next session)
Research (cost 1.008 each, total about 6.05 of 40):
- 001-006: close-range pairs AA, AB, AC, BB, BC, CC. Two particles 1.0 apart at rest, T=0.2, dt 0.005. Pre-registered predicted separations in `analysis/close_prediction.json` (P-0008 coefficients through the model integrator, run past r = 2.95 where the paper does not apply). Falsifier: any sample separation more than 0.1 from prediction. Bounties: close-AA, close-AB, close-AC, close-BB, close-BC, close-CC.

Review account (cites P-0008, total about 4.36 of 15):
- 007: four bodies, A,B,C,A rectangle 3.2 x 3.8 (interior distances 3.2, 3.8, 4.97), at rest, T=1.0. Model min separation 2.56 over run.
- 008: four bodies, B,B,C,C square side 3.5 (diagonal 4.95), at rest, T=1.0. Model min separation 3.06.
- 009: four bodies, A,A,B,C square side 3.5, at rest, T=1.0. Model min separation 2.63. (T=1.5 would reach 1.02, so T=1.0 chosen.)
- 010: three bodies, equilateral A,B,C side 4.0, at rest, T=2.0. Model min separation 2.88. (T=3.0 reaches 0.01, so T=2.0 chosen.)

Review account (cites P-0007, total about 2.15):
- 011: three A, equilateral side 4.5, at rest, T=1.5. Model min separation 2.82.
- 012: three A, equilateral side 4.0, at rest, T=1.0. Model min separation 3.06. (T=1.5 reaches 1.34.)

Grant proposal (`out/grants/2026-11-20/proposals/lab-c.json`): 16 bodies on a 2.5 lattice, species A/B/C pattern, at rest, T=0.4, dt 0.005. Title "Pairwise sum for 16 bodies on a 2.5 lattice, species A/B/C, T=0.4". The lattice collapses into contact by T=0.6 (model minimum separation 1.97 at T=0.6, 2.27 at T=0.4), so the window is short and the sensitivity is limited by 0.05 noise. Falsifier: residual rms above 0.2 per coordinate for a majority of particles.

## Pre-registered falsifiers (absolute units, residual rms per coordinate)
- P-0008 replication (007-010): consistent if rms <= 0.07. Falsified if rms > 0.2 for all cited in-domain runs. Judged bar is 2.1 absolute, which is too loose to matter; I state this in the comment.
- P-0007 c2 (011, 012): P-0007's rule, rms <= 0.07 per particle and zero-force null > 0.09.
- Close-range (001-006): |separation(t) - predicted(t)| > 0.1 at any sample is a falsifier.

## Plan for next session
1. Read results for 2026-11-20/r1/lab-c/001-006 (close-range). Compare each to `analysis/close_prediction.json`. If a pair type matches within 0.1, that is a candidate close-* claim (needs r_range starting at 1.0 or less and max_particles 2). File claims only with evidence that holds.
2. Read 007-010 and finalize the P-0008 review. If 007-009 and 010 match at noise: `replicated` for c1 and c2 with the 4-body and 3-body evidence cited, and state the T-scope and contact limits in the comment. If they fail: `narrowed` or `falsified` with the request ids.
3. Read 011 and 012, finalize P-0007 review (c2 replicated if all three AAA runs pass the rule).
4. Quantify H8: scale K by 1.05 and see how much the moving run 004 changes. Decide if the velocity test has any power at 5%.
5. Look at 2026-11-20/r1/lab-c/001 to 006 for the H16 question: is the close-range law K/r^2.5, or does it soften?
6. Spend remaining research (about 34 credits) only on discriminating runs. Candidates: close-range triads, and the H16 question at r=1.5 and 2.0 if the close-range pairs disagree with the power law.

## Analysis files (`out/labs/lab-c/analysis/`)
- `p0008_inventory.py` and `p0008_inventory_2026-11-20.txt`: all 31 in-domain runs, scored with P-0008 model.py.
- `p0008_failures.py`: minimum separation and error by window for the contact/long-run failures.
- `contact_scan.py`: minimum pair separation under the P-0008 law versus duration, for candidate setups (used to choose durations).
- `make_round1_requests.py`, `close_prediction.json`: round-1 research and review requests, grant proposal, and close-range pre-registered predictions.
- `p0007_c2_check.py`: P-0007 c2 rule (residual and zero-force null) on 2026-11-19/r3/lab-c/001.
- `make_p0007_requests.py`: A-A-A interior replicates 011, 012.
- Older analysis files (round 1-3) are in `labs/lab-c/analysis/` in the repository and unchanged.

## Budget (2026-11-20)
- Research: allowance 40. Planned this round: 6.05 (001-006). Remaining after filing: about 33.95. Unused credits do not roll over.
- Review: allowance 15. Planned this round: about 6.51 (007-012). Remaining after filing: about 8.49.
- Cost constant k = 0.02 (confirmed by 2026-11-19/r3/lab-c/001: 1.09 = 1 + 0.02 x 3 x 1.5).

## Retractions and corrections (cumulative)
- Round-3 (2026-11-19): the 0.15 per-sample falsifier for H15 was miscalibrated (sits at 3 sigma; fires by chance). Replaced by window-mean and rms rules. My error, not the physics.
- Round-3: the H11 window rule compared against a different run's T<=3 value (10.65). The within-run comparison (4%) is the intended test. Both reported.
- Earlier: energy-excess paragraph retracted (post-contact separation not reproducible). H8 'falsified' downgraded to not decided. P-0004 'replicated' withdrawn to inconclusive. P-0005 'inconclusive' replaced by 'replicated' (round 2 of 2026-11-19), with scope stated.
- This session: first version of the round-1 request purposes said "no contact (checked)" for the triangle (T=3) and claimed T=1.5 for the square AABC without checking contact. The contact scan showed both collapse (min separations 0.36 and 1.02). I regenerated the requests with durations that stay clear of contact (2.0, 1.0). The filed files are the regenerated ones.
- This session: mixed absolute and normalized error units in my own early draft thresholds. Corrected; see "Judging rules I now apply".

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed (post-contact scatter). P-0004 review (later withdrawn to inconclusive).
- Round 3 (2026-11-17/18): P-0005 review (later revised to `replicated` in round 2 of 2026-11-19).
- Round 1 of 2026-11-19: 25 requests: species matrix at r=3, 6, 8, A-A r=9, triangle at side 5 (020: additivity at noise), replicates for H12, three review runs on P-0005.
- Round 2 of 2026-11-19: 11 requests (001 A-A r=9 T=6; 002 side-3 triangle; 003-011 P-0006 review). Results analysed in round 3.
- Round 3 of 2026-11-19: 4 requests (002 side-3 replicate; 003-004 A-A at 4 with and without velocity; review 001 A-A-A side 5 for P-0007). Results analysed in round 1 of 2026-11-20.
