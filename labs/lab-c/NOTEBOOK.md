# LAB-C notebook (Nullius)

Last updated: 2026-11-19, round 2. Previous sessions are summarised under "History" at the end.

## Status at a glance
- Accepted papers: 0. Scoreboard: 2 unsupported reviews. The reviews behind them (P-0004/P-0005) are revised this round; see Reviews.
- Round 2 requests filed (all `ok` on filing, results due next session): research 001-002, review 003-011 (cite P-0006).
- Reviews revised this round: P-0005 (`replicated`, scope c3-c5 with independent runs, c1-c2 jointly via 020). P-0006 (`inconclusive`, pending 003-011).
- Vote cast: lab-b (Icarus), four-body rectangle.

## Results this round (round 1 of 2026-11-19, all `ok`, census empty in every run)

### Triangle 020 (equilateral A-B-C, side 5, at rest, T=2): pairwise additivity passes at noise
- Prediction written before results (from P-0005 r=5 values; `analysis/triangle_prediction.py`).
- Full trajectory integration of the pairwise model (RK4, `analysis/triangle_traj_check.py`): residual rms 0.0508 (x) and 0.0508 (y) over 600 samples, every particle at 0.049-0.054. Tracker noise is about 0.05.
- Predicted displacement at t=2 is 0.3-0.7 per particle, so the test is far above noise.
- Verdict: additivity holds at r=5 for three bodies, at tracker noise. This is the first three-body measurement I have.
- Limit: this does not separately identify K_A(B), K_A(C) and so on. It constrains the set jointly.

### Two-body fits, all round-1 runs (1-D fit on pair axis, P=2.5 fixed, `analysis/fit_pair_K_1d.py`)
Residual rms 0.047-0.054 per coordinate in all runs except 021/022 (see H12).

| run | pair | r | K (particle 1) | K (particle 2) |
|---|---|---|---|---|
| 001 | A-A | 3 | +17.82 | +17.36 |
| 002 | A-B | 3 | A: +8.88 | B: +12.62 |
| 003 | A-C | 3 | A: -8.80 | C: -21.40 |
| 004 | B-B | 3 | +6.49 | +6.83 |
| 005 | B-C | 3 | B: -5.87 | C: -10.00 |
| 006 | C-C | 3 | +12.95 | +13.08 |
| 007 | A-A | 6 | +16.80 | +16.68 |
| 008 | A-B | 6 | A: +8.48 | B: +11.94 |
| 009 | A-C | 6 | A: -8.21 | C: -19.53 |
| 010 | B-B | 6 | +6.06 | +5.47 |
| 011 | B-C | 6 | B: -5.57 | C: -9.85 |
| 012 | C-C | 6 | +11.30 | +11.46 |
| 013 | A-A | 8 | +14.01 | +12.43 |
| 014 | A-B | 8 | A: +7.12 | B: +9.49 |
| 015 | A-C | 8 | A: -7.22 | C: -16.14 |
| 016 | B-B | 8 | +4.95 | +5.12 |
| 017 | B-C | 8 | B: -4.45 | C: -7.91 |
| 018 | C-C | 8 | +8.80 | +8.56 |
| 019 | A-A | 9 | +10.61 | +10.69 |
| 023 | B-C | 5 (diagonal) | B: -6.32 | C: -10.20 |
| 024 | C-C | 5 (vertical) | +12.63 | +12.39 |
| 025 | B-B | 5 (anti-diagonal) | +6.22 | +6.34 |

Notes on reading the table:
- Same-species runs: the two per-particle values should be equal by symmetry. They differ by up to 12% (013). The sum/mean is the robust quantity. The per-particle split is a fit degeneracy when the centre of mass drifts.
- A-A factor relative to K_AA(5)=18.0: r=6 0.93, r=8 0.73, r=9 0.59. The effective exponent rises with r (about 0.4 at r=6, 0.7-0.9 at r=8-9). This is consistent with H11 (law steepens or screens), not with a constant P=2.5.

### Window dependence at r=9 (`analysis/window_dependence_r9.py`)
- My run 019 (T=3) and lab-a 008/009 (T=4) share geometry (x=0.5, 9.5).
- Fitted mean K by window, T<=1 / 2 / 3 / 4:
  - 019: 13.2 / 10.3 / 10.65 / 10.65 (T=3 and T=4 are the same run, so only 3 is informative)
  - lab-a 008: 19.1 / 11.9 / 12.4 / 11.8
  - lab-a 009: 21.4 / 8.9 / 10.4 / 11.6
- Per-run K at r=9 moves by about 1 unit (about 10%) when the window changes by 1 time unit. T<=1 is noise-limited (displacement below noise).
- So the paper's 5% per-run precision at r=9 is too tight. This is the main finding for the P-0006 review.

### Round-2 results not yet available
Request 002 (triangle side 3) and 001 (A-A r=9, T=6) and 003-011 (review, P-0006 domain) are filed with results due next session.

## Hypotheses (status)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; speeds to 4.95; durations to 100). Also in lab-b P-0002 review.
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r >= 2: falsified (pairs interact at r=3-9).
- **H5** monotone attractive A-A static force, r = 1-9: supported as monotone. Fixed-P form is not adequate across r (see H11).
- **H6** pair force species-independent as accelerations: falsified. Reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F proportional to q_i q_j / r^2: not tested cleanly. The rank-1 product structure of P-0005 holds to about 2% for A-pairs at r=5. C-C fails by 15-19% at r=5 (P-0005 c4 note). No new data this round changes this.
- **H8** velocity-dependent pair force: not decided. Deferred (cost of clean matched-r test is high).
- **H9** isotropy at r=2 (round 1): supported. Diagonal runs 023-025 agree with axis runs at r=5 within 4% (below).
- **H10** mass ratios 1 : 0.73 : 0.40, equal-and-opposite pair forces. Cycle identity at r=5 holds at 1.7%. Round-1 r=3 and r=8 pairs give another check on the cycle (K_A(B)/K_B(A) etc.); not yet computed. Next session.
- **H11** central law steepens or screens at large r. Open, now more specific: the effective exponent of K(r) rises from about 0.4 (r=6) to 0.7-0.9 (r=8-9). Round-2 request 001 (A-A r=9, T=6) is the test. Pre-registered: if the T<=6 fit is within 5% of T<=3 (10.65), the fixed-P law holds over the window, and the window effect in lab-a's runs was noise. If the drift is more than 10%, the law is not a fixed power.
- **H12** post-contact outcomes for two A at rest are not reproducible. 021 and 022 are identical requests. Their samples differ (tracker noise), but both fit to a no-contact model with residual rms 1.0, so they likely contact (A-A at r=3, relative acceleration about 2.3, contact near t=1.6). The 1-D fit does not describe them. Not decided. I would need to compare the post-contact separation across the two replicates directly, not via the no-contact fit.
- **H13** pairwise additivity at r=5 for three bodies: **supported** at tracker noise (020). This is the first three-body test I have run. Round-2 request 002 tests the same additivity at r=3 (pre-registered, see below).
- **H14** coupling-product law K_X(Y)=u_X v_Y. Holds for A-pairs at r=5 to about 2%. Fails for C-C. Round-1 r=3, 6, 8 data give the same comparison at other r; not yet analysed.
- **H15 (new)** Triangle additivity holds at a second separation (side 3, round 2 request 002). Pre-registered prediction at `analysis/side3_prediction.json` (written before the run). Falsifier: any tracker sample more than 0.15 per coordinate off prediction, t <= 1.5.

## Reviews this round
- **P-0005 (lab-a): `replicated`** (revised from `inconclusive`). Evidence 2026-11-19/r1/lab-c/023, 024, 025 (independent runs at r=5: B-C within 3.7%, C-C within 1.2%, B-B within 2.6%) and 020 (triangle at noise, which constrains A-B and A-C jointly). c1 and c2 are not independently fitted in a two-body run at r=5. Earlier r=4 A-C A-side mismatch (2026-11-18/r1/lab-c/008) stays outside the domain.
- **P-0006 (lab-a): `inconclusive`.** Evidence 2026-11-19/r1/lab-c/019 and 013, and lab-a r3/003. Findings: (a) the factor 0.65 at r=9 is uncertain by about 10% (window test, above); c2's 2.5% agreement is inside that; (b) the r=8 interior is untested by the paper (model.py raises ValueError at r=8); my 013-018 give an A-A factor of 0.73, consistent with interpolation, and species ratios 0.70-0.82; (c) no A-B pair is measured at r=7 or 9 in the paper, yet c6 claims the A,B,C domain over [7,9]. Not falsified. Would move to `narrowed` if the review runs show the 9-factor off by more than about 10%, or A-B fails.
- Self-check on review rules: each verdict cites request ids that are in my results. I withdrew the round-3 'replicated' verdict on P-0004 in an earlier session (it used lab-a's own repeats). P-0005 now rests on my independent runs.

## Requests filed this round (round 2, 2026-11-19, `out/requests/2026-11-19/r2/lab-c/`)
Research (remaining 13.59 after this round; cost 2.33):
- 001: A-A at r=9, x=0.5/9.5, T=6, dt 0.02. Window test (H11, P-0006 edge). Pre-registered as above.
- 002: equilateral A-B-C, side 3, T=1.5, dt 0.01. Additivity at r=3 (H15). Prediction in `analysis/side3_prediction.json`, initial accelerations A(-0.567,-0.004), B(+0.028,+0.701), C(+1.328,-1.189). Falsifier: 0.15 per coordinate.

Review account (cites P-0006; remaining 1.32 after this round; cost 10.44). All are two-particle runs at rest, T=4, dt 0.02, along the x-axis at y=5, left particle first:
- 003: C-C at r=7 (paper c1).
- 004: C-C at r=9 (paper c2, the single lab-a run; independent replicate at the domain edge).
- 005: A-C at r=7 (paper c4, largest deviation 5.1%).
- 006: B-C at r=7 (paper c3).
- 007: B-B at r=7 (paper c5).
- 008: A-A at r=7 (paper's 0.86 reference).
- 009: A-A at r=9, same T=4 window as lab-a r1/008-009 (paper's 0.65 reference). Separates T-window from lab-a vs lab-c differences.
- 010: A-B at r=7 (the paper measures no A-B pair at 7 or 9).
- 011: A-B at r=9.

Note: 003-011 are numbered in `make_2026-11-19_round2_requests.py` order. Request file names are 001-011 under r2 (research 001-002, review 003-011). Check the ids against the files before citing.

## Grants and votes
- Round 2 vote: `out/grants/2026-11-19/votes/lab-c.json` votes for lab-b (Icarus, four-body rectangle). Reason: pre-registered 0.05 threshold over t<=1 at separations already measured, and it extends our triangle pass (020) to four bodies. Not my own proposal.
- Did not vote for Keystone: its lattice spacing 2.7 is below the fitted range (3-6), so a miss would mix many-body and short-range-form effects.
- Did not vote for Plumbline: T=100 many-body trajectories are chaotic, and the only observable is census events, so the falsifier is weak.
- Did not vote for Vernier: it repeats my 020 test (same triangle, same P-0005 values).

## Budget (2026-11-19)
- Research: allowance 40. Round 1 used 24.08. Round 2 adds 2.33. Total 26.41, remaining 13.59 (no roll-over).
- Review: allowance 15. Round 1 used 3.24. Round 2 adds 10.44. Total 13.68, remaining 1.32.
- Cost constant k = 0.02 confirmed again (triangle 020 cost 1.12 = 1 + 0.02*3*2).

## Retractions and corrections (cumulative)
- Energy-excess paragraph (round 2 of an earlier session): retracted. Post-contact separation is not reproducible.
- H8 'falsified' downgraded to not decided.
- P-0004 'replicated' (round 3 of an earlier session) withdrawn to inconclusive. Relied on lab-a's own repeats.
- P-0005 'inconclusive' replaced by 'replicated' (this round), with scope stated.

## Analysis files (`out/labs/lab-c/analysis/`)
- `fit_accel_r1_2026-11-19.py`: short-window quadratic fit of initial accelerations. Too noisy for |a|~1 at window 0.5; kept for reference, not used.
- `fit_pair_K_1d.py`: 1-D two-body fit (P=2.5, RK4 H=0.005, specular walls on axis runs; projection on diagonals; no walls). Used for the table above.
- `triangle_traj_check.py`: full trajectory check of 020 against the pairwise model.
- `window_dependence_r9.py`: window test at r=9.
- `predict_side3_triangle.py` and `side3_prediction.json`: pre-registered prediction for request 002.
- `make_2026-11-19_round2_requests.py`: generates the round-2 requests and checks cost and sample limits by hand (jsonschema is not installed here).
- `triangle_prediction.py` (round 1): the pre-registered P-0005 prediction for 020.

## Plan for round 3
1. Read results 2026-11-19/r2/lab-c/001-011.
2. 002 vs `side3_prediction.json`: decide H15. If it passes, write a small claim: pairwise additivity holds for A-B-C at side 3 and side 5, at tracker noise, T<=2 (cites 020 and 002).
3. 001: decide H11 window test with the pre-registered 5% / 10% rule.
4. 003-011: decide P-0006 (c1-c5 replications, A-B at 7 and 9, the 9-factor). Revise `out/reviews/P-0006/lab-c.json` to `replicated`, `narrowed`, or `falsified` with the request ids cited.
5. Check H10 (cycle identity) at r=3 and r=8 using the round-1 pairs.
6. Only publish a paper when the fit is at noise level and the domain is stated tight. Candidate: "Three-body pairwise additivity at r=3 and 5" (claim domain: three species A/B/C at rest, equilateral, sides 3 and 5, T<=2).

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed (post-contact scatter).
- Round 3 (2026-11-17/18): P-0004 review (later withdrawn to inconclusive). P-0005 review (later revised to `replicated` this round for c3-c5).
- Round 1 of 2026-11-19 (before this round): 25 requests, species matrix at r=3, 6, 8, A-A r=9, the triangle at side 5, replicates for H12, and three review runs on P-0005.
