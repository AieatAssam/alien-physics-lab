# LAB-C notebook (Nullius)

Last updated: 2026-11-21, round 1. Earlier rounds condensed under "History".

## Status at a glance
- Accepted papers: 0. **P-0012 (my first paper, this round) is filed** as a narrow claim: pair law at separation 1.5 for A-A, A-C and C-C at rest, T <= 0.4 (out/papers/P-0012/). Its id may be renumbered by the gate.
- Unsupported reviews on the scoreboard: 2 (2026-11-18, my `replicated` verdicts on P-0001 and P-0002). Before any `replicated` verdict I check the judge's bar against the runs I cite.
- Reviews: none awaiting. Standing reviews: P-0009 replicated, P-0010 narrowed, P-0007 narrowed, P-0008 replicated, P-0011 replicated, P-0005 replicated.
- Round-3 results of 2026-11-20 (001-017) are scored (below). Replicates agree with round 2 to 0.005 in scale.
- **Key finding this round:** the judged metric (RMSE / 10) does not discriminate the P-0008 coupling from the fitted scale for AC and CC at T = 0.4. The unscaled P-0008 model scores 0.0077-0.0078 on those runs, against a noise floor of 0.0071. Only AA is resolved by the judge (unscaled 0.068). Any claim about AC or CC scales must say so.
- Research credits used today: about 9.1 of 40 (round 1 requests, see below). Review account: unused (15 available).

## Judging rules (carried forward)
- Judged error (tools/editor.py `traj_error`): sqrt(mean over matched (t, particle) of |dpos|^2) / 10, matched on exact t (rounded to 9 places). Noise floor with tracker noise 0.05 per coordinate: sqrt(2) x 0.05 / 10 = **0.0071**.
- Replicate bar: 3 x predicted_error on cited in-domain runs. A run the model refuses (ValueError) does not count.
- Judged domain checks species, particle count, and initial pairwise separations only. It does not check velocity, duration, wall distance or closest approach. So any restriction I want must be enforced by my model raising ValueError (P-0012 does this for velocity, duration and wall distance).
- For coupling claims I use a per-run scale fit (chi-square at sigma 0.071 on separation, window = before the prediction's own separation drops below 0.6), with a time-block jackknife SE (about 0.01). Quote s to about +/- 0.02.
- Pre-registered falsifiers on single samples are miscalibrated (noise on a separation is 0.071). Use window means.

## Round 3 results of 2026-11-20 (001-017), scored with `score_r3_2026-11-20.py`
Scale s on the P-0008 law (all coefficients times s), best fit, chi2/n at best s:

| id | pair | r0 | T | best s | chi2/n (best) | chi2/n (s=1) | expected (pre-reg) | note |
|---|---|---|---|---|---|---|---|---|
| 001 | AA | 1.0 | 0.3 | 0.61 | 0.97 | 1.96 | 0.55-0.80 | pre-contact window only 0.14 at s=1 |
| 002 | AA | 2.0 | 0.6 | 0.85 | 1.02 | 3.07 | 0.80-0.90 | in range |
| 003 | AA | 3.0 | 2.0 | 0.96 | 1.10 | 1.54 | 0.97-1.03 | falsifier s < 0.95 did not fire (0.96) |
| 004 | AA | 3.5 | 1.5 | 1.00 | 1.04 | 1.04 | 0.97-1.03 | consistent with 1 |
| 005 | AA | 4.0 | 2.0 | 1.01 | 1.14 | 1.14 | 0.98-1.03 | consistent with 1 |
| 006 | AA | 1.5 | 0.4 | 0.75 | 1.01 | 3.20 | 0.70-0.80 | replicate of r2/004 (0.753): agrees to 0.004 |
| 007 | AB | 1.5 | 0.4 | 0.78 | 0.96 | 2.41 | 0.75-0.95 | AB deficit present |
| 008 | AC | 1.5 | 0.4 | 0.81 | 0.97 | 1.69 | 0.76-0.86 | replicate of r2/005 (0.811): agrees to 0.005 |
| 009 | AC | 2.5 | 1.0 | 0.98 | 0.95 | 0.98 | 0.85-0.97 | no deficit at 2.5 |
| 010 | BB | 1.5 | 0.4 | 0.80 | 0.99 | 1.27 | 0.97-1.03 | **BB does show a deficit at 1.5** (expected none) |
| 011 | BC | 1.5 | 0.4 | 0.81 | 0.98 | 1.22 | 0.75-0.95 | in range |
| 012 | CC | 2.5 | 1.0 | 1.01 | 1.00 | 1.04 | 0.90-1.00 | no deficit at 2.5 |
| 013 | BB | 2.5 | 1.0 | 0.99 | 1.01 | 1.02 | 0.97-1.03 | no deficit at 2.5 |
| 014 | CC | 1.5 | 0.4 | 0.87 | 0.97 | 1.62 | 0.82-0.92 | replicate of r2/006 (0.874): agrees to 0.005 |
| 015 | AC | 3.0 | 2.0 | 1.02 | 1.03 | 1.12 | 0.97-1.03 | consistent with 1 |
| 016 | CC | 3.0 | 2.0 | 1.04 | 1.00 | 1.68 | 0.97-1.03 | consistent with 1 (slightly high) |
| 017 | AA | 7.0 | 3.0 | 0.84 | 1.03 | 2.92 | 0.96-1.02 (vs P-0010) | outside P-0008 domain; the P-0008 radial form is not P-0010's G(r), so not comparable to P-0010 |

Reading:
- **Replicates reproduce** (006, 008, 014 vs round-2 004, 005, 006), within 0.005 in s.
- **AA scale rises with r:** 0.61 (r 1.0), 0.75 (1.5), 0.85 (2.0), 0.92 (2.5), 0.96 (3.0), 1.00 (3.5), 1.01 (4.0). A smooth trend, not a step.
- **Other pairs at 2.5-3.0 are at 1 within about 0.05** (AC, CC, BB). The 1.5 deficit for AB, BB, BC, AC, CC is 0.78-0.87.
- So the short-range deficit is species-dependent at 1.5 (AA lowest, CC highest), and at 2.5 only AA still deviates. The earlier H16 hypothesis that BB shows no deficit is **retracted**: BB at 1.5 gives 0.80.

## Round 1 close-range results of 2026-11-20 (001-006, r0 = 1.0, T = 0.2), `score_r1_2026-11-20.py`
Single runs, 41 samples. Best s: AA 0.60, AB 0.65, AC 0.60, BB 0.78, BC 0.72, CC 0.81. chi2/n at best s 0.82-1.12; at s = 1 1.3-2.5. Ordering matches the 1.5 pattern (AA lowest, CC highest). These are **single runs** and have not been replicated. The windows are short (29-41 samples).

## Publication (P-0012, `out/papers/P-0012/`)
- Claim P-0012-c1: species A, C; r_range [1.45, 1.55]; max_particles 2; predicted_error 0.01. Model: P-0008 coefficients times fixed per-pair scales (AA 0.753, AC 0.811, CC 0.874), fitted on round-2 runs only, so the round-3 replicates (006, 008, 014) are out of sample.
- Judged error of the model on all six runs: 0.00704 to 0.00717 (noise floor 0.0071; bar 0.03).
- **Control (unscaled P-0008):** AA 0.068 (fails), AC 0.0078 and CC 0.0077 (pass). The paper says so.
- The model refuses: species other than A/C, separations outside [1.45, 1.55], particles with velocity, particles within 2 of a wall, duration above 0.4.
- Not claimed: B species, other separations, longer times, closest approach. Close-* bounties need r_range starting at 1.0 or less, so P-0012 does not win one.

## Round 1 requests of 2026-11-21 (out/requests/2026-11-21/r1/lab-c/001-009), research account, tracker only
| id | pair | r0 | T | dt | prior s | what it tests |
|---|---|---|---|---|---|---|
| 001 | AA | 1.0 | 0.3 | 0.0005 | 0.61 | close-AA replicate |
| 002 | AB | 1.0 | 0.3 | 0.0005 | 0.65 | close-AB replicate |
| 003 | AC | 1.0 | 0.3 | 0.0005 | 0.60 | close-AC replicate |
| 004 | BB | 1.0 | 0.3 | 0.0005 | 0.78 | close-BB replicate |
| 005 | BC | 1.0 | 0.3 | 0.0005 | 0.72 | close-BC replicate |
| 006 | CC | 1.0 | 0.3 | 0.0005 | 0.81 | close-CC replicate |
| 007 | AB | 1.5 | 0.4 | 0.0002 | 0.78 | AB 1.5 replicate of r3/007 |
| 008 | BB | 1.5 | 0.4 | 0.0002 | 0.80 | BB 1.5 replicate of r3/010 |
| 009 | BC | 1.5 | 0.4 | 0.0002 | 0.81 | BC 1.5 replicate of r3/011 |

Estimated cost about 9.1 credits (cost = 1 + 0.02 x particles x T). The grant proposal (`out/grants/2026-11-21/proposals/lab-c.json`) asks for one A-A pair at r0 = 0.5, T = 0.2, dt = 0.0001: a test of whether the scale law still holds below r = 1.

## Hypotheses (status)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; T to 100).
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r >= 2: falsified (pairs interact at r = 3-9).
- **H5** monotone attractive A-A static force, r = 1-9: supported as monotone.
- **H6** pair force species-independent as accelerations: falsified; reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F proportional to q_i q_j / r^2: not tested cleanly; C-C conflicts with the P-0005 coupling product at r = 5 (see H14).
- **H8** velocity-dependent pair force: partially tested; not decided.
- **H9** isotropy at r = 2 (round 1): supported.
- **H10** mass ratio 1 : 0.73 : 0.40, equal-and-opposite forces. Cycle identity holds at r = 5 to 1.7%.
- **H11** effective pair coupling depends on separation, with the P-0008 AA scale rising from 0.61 (r 1) to about 1 (r 3.5 to 4). Round-3 003-005 support this; r 7 (017) is outside P-0008's form and not comparable.
- **H12** post-contact outcomes for two A at rest are not reproducible. Not decided.
- **H13** pairwise additivity at r = 5 for three bodies: supported at tracker noise.
- **H14** coupling-product law K_X(Y) = u_X v_Y: holds for A-pairs at r = 5 to about 2%; C-C conflicts (see H7).
- **H15** triangle additivity at side 3 (A-B-C): supported at noise. Closed.
- **H16 (main, open)** short-range pair deficit. Now: replicated for AA, AC, CC at 1.5 (scales 0.75, 0.81, 0.87); single run each for AB (0.78), BB (0.80), BC (0.81); single runs at r 1.0 for all pairs (0.60-0.81). The deficit is species-dependent (AA largest) and disappears by r about 2.5 for AC, CC, BB. **Open:** scale or shape (the grant tests r 0.5); replicates of AB, BB, BC at 1.5 and all pairs at 1.0 (requests 001-009).
- **H18** P-0010 A-A coefficient: s = 0.974 at r0 6 (pre-approach), 0.995 at r0 8. Weak. No further test planned.
- **H19** P-0005 pair coefficients at separation 5 hold to 1-2% for BB, BC, CC on 2-body runs.
- **H20** tracker noise per coordinate 0.0507 (lone particles, pooled).
- **H21** P-0010 closest-approach failure: A-A at r0 6 at rest collides by t about 4.1 and the model's error passes 0.2 at t = 4.12 (run 2026-11-20/r2/lab-c/002). Supported by one run.
- **H22 (new)** the judged metric cannot separate a 13-19% coupling deficit (AC, CC at 1.5, T 0.4) from the P-0008 law. Supported by the control (unscaled 0.0077-0.0078 vs 0.0071 floor). Consequence: scale claims for these pairs need a longer or closer run to be judged.

## Corrections and retractions (cumulative)
- **This round:** the round-2 claim that BB shows no short-range deficit (H16, round 1 r0 1.0 result) is contradicted by round-3 010 (BB at 1.5, s = 0.80). Also round-1 BB at 1.0 gave 0.78, not 1.0. Retracted.
- **This round:** my round-2 summary said the deficit "is not yet replicated." It now is for AA, AC, CC at 1.5.
- **This round:** the 2026-11-20 round-2 "species-dependent" wording is now supported by replicates for three pairs.
- **Earlier (2026-11-20):** the A-A coefficient review of P-0010 had the sign wrong; corrected in the final review. The A-A value at r0 8 (0.949-0.959) did not replicate (003 gives 0.995). The round-2 pre-registered falsifiers for 004 and 007 were contaminated by the P-0008 integrator's post-contact rebound.
- **Earlier:** Delta-chi2 = 1 errors from scale scans are too small (correlated model error). Use the jackknife SE.
- **Earlier:** energy-excess paragraph retracted. P-0004 'replicated' withdrawn to inconclusive. P-0005 'inconclusive' replaced by 'replicated' with scope.

## Plan for next session
1. Read 2026-11-21/r1/lab-c/001-009 when they return. Score with `score_r3_2026-11-20.py` adapted to these ids (or a new script). Pre-registered falsifiers: each request's purpose.
2. If the close replicates (001-006) agree with round 1 within the falsifier bands, file **close-* claims** with r_range starting at 1.0 (for example [1.0, 1.1]). One claim with species A, B, C could cover every close-* bounty (`covers()` checks species membership), but only if each pair has a passing replicate. Set predicted_error from replicate scatter (not below 0.01). Check the judged bar on the replicates before publishing.
3. The 1.5 B-pair replicates (007-009): if they agree, extend P-0012 to species B (new claim or a v2 with `supersedes`), keep the AC/CC caveat, and set domain species to A, B, C.
4. Grant (if won, 120 credits on `grant`, usable in round 3): the r 0.5 test. Compare with the trend (s about 0.5 to 0.6 from 1.0 to 1.5). Falsifier: no single s with chi2/n <= 2 pre-contact.
5. Before publishing any AC or CC scale claim, check the judged metric: a model's error must be above 0.0071 + margin on some domain run, or the claim is not testable through the judge. Consider a longer T or closer pair (close-range runs, where the scale change is largest).
6. Do not review anything until the review account has a paper. Keep research use under 40 credits per day.

## Analysis files (out/labs/lab-c/analysis/)
- `score_r3_2026-11-20.py` and `.txt`: scale fits for all 17 round-3 runs.
- `score_r1_2026-11-20.py` and `.txt`: scale fits for round-1 close runs (r0 = 1.0).
- `judge_P0012_2026-11-21.py` and `.txt`: judged error of P-0012's model on the six 1.5 runs.
- `control_unscaled_P0012_2026-11-21.py` and `.txt`: same runs with unscaled P-0008 coefficients (the control).
- `make_2026-11-21_r1_requests.py`: generates round-1 requests 001-009 and the grant proposal.
- Earlier: `scale_fit_short_range.py`, `review_runs_2026-11-20.py`, `analyze_r2_short_range.py`, `pred_2026-11-20_r2_shortrange.json` (round 2; in `labs/lab-c/analysis/` in the repo).
- Paper: `out/papers/P-0012/{paper.md, claim.json, model.py}`.

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed. P-0004 review (later withdrawn to inconclusive).
- Round 3 (2026-11-17/18): P-0005 review (later revised to `replicated`).
- 2026-11-19 rounds 1-3: species matrix at r = 3, 6, 8, A-A r = 9, triangles at side 5 and 3, P-0005/P-0006/P-0007 review runs.
- 2026-11-20 round 1: 6 close-range runs (r0 = 1.0, T = 0.2), 6 review runs (P-0008, P-0007 replicates), grant proposal (16 bodies, T = 0.4).
- 2026-11-20 round 2: 7 requests (3 review: P-0009 BCC side 5, P-0010 A-A at 6 and 8; 4 research short-range at 1.5 and AA at 2.5). Vote for lab-a (Plumbline, close-CC).
- 2026-11-20 round 3: 17 research requests (001-017) on the short-range law, replicates and the P-0008 domain edge. Scored this session.
- 2026-11-21 round 1 (this session): scoring of round 3; P-0012 filed; 9 research requests; grant proposal (AA at r 0.5).
