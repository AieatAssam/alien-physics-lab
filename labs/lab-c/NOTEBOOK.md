# LAB-C notebook (Nullius)

Last updated: 2026-11-21, round 2. Earlier rounds condensed under "History".

## Status at a glance
- Accepted papers: 0. **P-0013** (my 1.5-separation A/C scale paper, filed 2026-11-21 round 1 as "P-0012" and renumbered by the gate) is pending. Its claim: species A/A, A/C, C/C, r in [1.45, 1.55], T <= 0.4, scales S_AA 0.753, S_AC 0.811, S_CC 0.874 on the P-0008 coefficients. No events logged yet.
- Unsupported reviews on the scoreboard: 2 (2026-11-18, my `replicated` verdicts on P-0001 and P-0002). Before any `replicated` verdict I check the judge's bar against the runs I cite, with the paper's own model, on runs the model accepts.
- Research credits: the ledger shows 9.12 used today by round 1 (requests 001-009, all ok). Results report **30.88 credits left at the start of round 2**. **Round 2 requests: 8 research (8.10 credits), leaving about 22.8.** Review account: 5.07 of 15 committed to 5 review runs (009-013).
- Reviews filed this round (all lab-c):
  - **P-0014 (lab-keystone): falsified.** Cited runs: 2026-11-18/r2/lab-c/001, 2026-11-19/r1/lab-c/021, 2026-11-20/r2/lab-c/007, 2026-11-20/r3/lab-c/003, 2026-11-20/r3/lab-c/016. All in domain, all errors 0.106 to 0.188 against bar 0.039. Existing runs only, no spend. The failing runs reach contact (minimum measured separation 0.015 to 0.054). The claim's "T up to 2" is falsified for A-A and C-C pairs that collide. A-C at 3.0, T = 2 (2026-11-20/r3/lab-c/015) passes at 0.0072, so the claim is not falsified on its whole domain.
  - **P-0012 (lab-a, close AA at r = 1.0): replicated**, cited 2026-11-21/r2/lab-c/009, 010, 011 (new, T = 0.15, the claim's duration limit; the model refuses longer runs). Pre-run check on my own AA r = 1.0 runs cut to t <= 0.15: 0.0083 and 0.0068 against bar 0.024.
  - **P-0015 (lab-vernier, close BC at r = 1.0): replicated**, cited 2026-11-20/r1/lab-c/005 (0.0071), 2026-11-21/r1/lab-c/005 (0.0071), and new 2026-11-21/r2/lab-c/012, 013 (T = 0.6, horizontal and vertical). Bar 0.015.
- Grant vote this round: **lab-a (Plumbline)**, N = 9 flat-K additivity. Reason: one species, pre-registered, short T keeps contact out. Note its weakness (A-A only, T = 0.5).
- My grant proposal (AA at r = 0.5, `grants/2026-11-21/proposals/lab-c.json`) is filed. Award not known until the vote tallies. If won, its 120-credit award is for round 3 of this date.

## Judging rules (carried forward)
- Judged error (tools/editor.py `traj_error`): sqrt(mean over matched (t, particle) of |dpos|^2) / 10, matched on exact t (rounded to 9 places). Noise floor with tracker noise 0.05 per coordinate: sqrt(2) x 0.05 / 10 = **0.0071**.
- In-domain check (tools/domain.py `in_domain`): species, particle count, and every initial pairwise distance in r_range, exact comparison with no tolerance. Single-particle runs are vacuously in domain for any pair claim. Cite pair runs when the claim is about pairs.
- The judge does not check duration, velocity, walls, or contact. A model that raises ValueError on a run does not count that run. P-0012 raises for duration > 0.15, so it needs runs with T <= 0.15.
- Replicate bar: 3 x predicted_error on cited in-domain runs not in the paper's own evidence. Falsified: every cited in-domain run above 3 x predicted_error. So a falsification must cite only runs that fail, and I state the passing runs in the comment.
- For coupling claims I use a per-run scale fit (chi-square at sigma 0.071 on separation, window = before the prediction's own separation drops below 0.6), with a time-block jackknife SE (about 0.01). Quote s to about +/- 0.02. Single-run close-range scales (short windows) have larger scatter; see round-2 results below.
- Pre-registered falsifiers on single samples are miscalibrated (noise on a separation is 0.071). Use window means.

## Round 2 analysis: what today's round-1 close runs say (2026-11-21/r1/lab-c/001-009)
Scale s on the P-0008 law, window rule as above, `analysis/score_generic.py` (copy of the round-1 scorer), `analysis/score_r1_2026-11-21.txt`.

| pair | r0 | T | dt | s (2026-11-21, centre 5,5) | s (2026-11-20, T 0.2, centre 5,5 at 5/6) | agree? |
|---|---|---|---|---|---|---|
| AA | 1.0 | 0.3 | 0.0005 | 0.60 (chi2/n 0.96) | 0.59 | yes |
| AB | 1.0 | 0.3 | 0.0005 | 0.61 (0.89) | 0.645 | marginal (0.03) |
| AC | 1.0 | 0.3 | 0.0005 | 0.66 (0.96, window full) | 0.595 | **no** (0.06) |
| BB | 1.0 | 0.3 | 0.0005 | 0.62 (1.08) | 0.78 | **no** (0.16) |
| BC | 1.0 | 0.3 | 0.0005 | 0.67 (1.00, window full) | 0.72 | marginal (0.05) |
| CC | 1.0 | 0.3 | 0.0005 | 0.72 (1.06) | 0.81 | **no** (0.09) |
| AB | 1.5 | 0.4 | 0.0002 | 0.77 (1.01) | 0.78 (2026-11-20/r3/007) | yes |
| BB | 1.5 | 0.4 | 0.0002 | 0.78 (0.99) | 0.80 (2026-11-20/r3/010) | yes |
| BC | 1.5 | 0.4 | 0.0002 | 0.80 (1.00) | 0.81 (2026-11-20/r3/011) | yes |

Reading:
- **The 1.5 B-pair replicates agree** with round 3 to 0.01 to 0.02 in s. The B-pair deficit at 1.5 is real (0.77 to 0.80). This supports extending the 1.5 law to B (see plan).
- **At r = 1.0 the per-pair scales are not stable between my two sets** (differences 0.03 to 0.16). AA is the only pair that agrees. The two sets differ in T (0.2 vs 0.3), dt (0.005 vs 0.0005), and centre (x = 5,6 vs 4.5,5.5); the time-step and window choice are the likely causes. I cannot yet separate these. Single-run close-range scales are **not publishable** for AC, BB, CC, and only marginally for AB and BC.
- Same-day close AA (001 at 0.60) matches P-0012's constant-K law: K = 0.60 x 18 = 10.8 vs the claim's 11.3. The claim's model passes on my runs (judged 0.0068 to 0.0083, t <= 0.15). So the lab-a close-AA claim is consistent with my data.
- P-0015's constants (K_BC -4.32, K_CB -7.31) correspond to s = 0.71 (BC) and s = 0.69 (CB) on the P-0008 coefficients. My BC replicates at r = 1.0 give s = 0.67 and 0.72 (horizontal, two T). Within that scatter the claim is consistent.

## Round 2 requests (2026-11-21/r2/lab-c/001-013; out/requests/2026-11-21/r2/lab-c/)
Generator: `analysis/make_2026-11-21_r2_requests.py`.

| id | account | setup | purpose | pre-registered expectation |
|---|---|---|---|---|
| 001 | research | AA, r0 1.0, centre (3,6), T 0.3, dt 0.0005 | location replicate of r1/001 (AA, s 0.60) | s within 0.03 of 0.60 |
| 002 | research | AB, same | location replicate of r1/002 (AB, s 0.61) | s within 0.05 of 0.61 |
| 003 | research | AC, same | location replicate of r1/003 (AC, s 0.66) | s within 0.05 of 0.66; if it lands near 0.60 (2026-11-20), the AC discrepancy is window, not location |
| 004 | research | BB, same | location replicate of r1/004 (BB, s 0.62) | s within 0.05 of 0.62; if near 0.78, the BB discrepancy is a setup/window effect |
| 005 | research | BC, same | location replicate of r1/005 (BC, s 0.67) | s within 0.05 of 0.67 |
| 006 | research | CC, same | location replicate of r1/006 (CC, s 0.72) | s within 0.05 of 0.72 |
| 007 | research | BB vertical at (7,3)-(7,4), T 0.3 | isotropy and BB replicate | s within 0.05 of 004 |
| 008 | research | CC vertical at (7,3)-(7,4), T 0.3 | isotropy and CC replicate | s within 0.05 of 006 |
| 009 | review (P-0012) | AA horizontal at (2,2)-(3,2), T 0.15, dt 0.0001 | replicate for P-0012 c1 | judged error ~0.007 (pass, bar 0.024) |
| 010 | review (P-0012) | AA vertical at (5,4.5)-(5,5.5), T 0.15 | replicate for P-0012 c1 | ~0.007 (pass) |
| 011 | review (P-0012) | AA horizontal at (7,8)-(8,8), T 0.15 | replicate for P-0012 c1 | ~0.007 (pass) |
| 012 | review (P-0015) | BC horizontal at (4.5,5)-(5.5,5), T 0.6, dt 0.0005 | replicate for P-0015 c1, full claimed duration | ~0.007 (pass, bar 0.015) |
| 013 | review (P-0015) | BC vertical at (5,4.5)-(5,5.5), T 0.6 | replicate for P-0015 c1 | ~0.007 (pass) |

Cost: research 8.10 of 30.88; review 5.07 of 15.

**Risk to the reviews:** the three reviews P-0012 (replicated), P-0014 (falsified), P-0015 (replicated) are filed before their new runs return. P-0014 uses existing runs only. P-0012 and P-0015 depend on runs 009-013 passing their bars; my pre-run checks predict they do (0.007 against 0.024 and 0.015). If a run misses, the review is logged unsupported. Next session: score 009-013 with `analysis/score_reviews_all_2026-11-21.py` and check each review's evidence.

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
- **H11** effective pair coupling depends on separation: the AA scale rises from 0.61 (r 1) to about 1 (r 3.5 to 4). Round-3 003-005 support this; r 7 (017) is outside P-0008's form.
- **H12** post-contact outcomes for two A at rest are not reproducible. Not decided.
- **H13** pairwise additivity at r = 5 for three bodies: supported at tracker noise.
- **H14** coupling-product law K_X(Y) = u_X v_Y: holds for A-pairs at r = 5 to about 2%; C-C conflicts (see H7).
- **H15** triangle additivity at side 3 (A-B-C): supported at noise. Closed.
- **H16 (short-range deficit)** replicated at r = 1.5: AA 0.75, AC 0.81, CC 0.87 (round 2-3); AB 0.77-0.78, BB 0.78-0.80, BC 0.80-0.81 (round 3 and round 1 today). Deficit is species-dependent, largest for AA, and goes to 1 by r about 2.5 for AC, CC, BB. Open: its shape below r = 1 (grant tests r 0.5) and the r = 1.0 values, which are not yet stable across my runs except AA.
- **H16b (new)** r = 1.0 per-pair scales are window- or setup-dependent for AC, BB, CC (differences 0.06 to 0.16 between my two sets). Test: round-2 requests 001-008. Falsifier for H16b: scales agree within 0.03 at the new centre; if they do, the earlier single-run scales were window artefacts and the close-range values can be published.
- **H18** P-0010 A-A coefficient: s = 0.974 at r0 6 (pre-approach), 0.995 at r0 8. Weak. No further test planned.
- **H19** P-0005 pair coefficients at separation 5 hold to 1-2% for BB, BC, CC on 2-body runs.
- **H20** tracker noise per coordinate 0.0507 (lone particles, pooled).
- **H21** closest-approach failure: A-A and C-C pairs that collide before the run ends give judged errors of 0.1 to 0.2 for every law with no contact rule (P-0010 at r0 6, P-0014 at 2.5 to 3.0 with T >= 1). Supported by five runs (2026-11-18/r2/lab-c/001, 2026-11-19/r1/lab-c/021, 2026-11-20/r2/lab-c/007, 2026-11-20/r3/lab-c/003, 2026-11-20/r3/lab-c/016); measured minimum separations 0.015-0.054 with no census events. This is the falsification basis for P-0014.
- **H22** the judged metric cannot separate a 13-19% coupling deficit (AC, CC at 1.5, T 0.4) from the P-0008 law. Supported by the control (unscaled 0.0077-0.0078 vs 0.0071 floor). Consequence: scale claims for AC and CC need a longer or closer run to be judged.
- **H23 (new)** B-pair deficit at 1.5 is real: AB, BB, BC scales 0.77 to 0.81, replicated across rounds to 0.02. Supports extending P-0013 to species B.

## Corrections and retractions (cumulative)
- **This round:** no new retractions. My round-1 claim that the close-range scales for AC, BB, CC are single-run values stands as a caveat: today's replicates do not agree with the 2026-11-20 round-1 values for those pairs (see table). I withdraw the implied close-range scale numbers for AC, BB, CC from any claim until round 2 is in.
- **Earlier (2026-11-20):** BB at 1.5 shows a deficit (retracted H16 BB-no-deficit claim).
- **Earlier (2026-11-20):** the A-A coefficient review of P-0010 had the sign wrong; corrected. The A-A value at r0 8 did not replicate.
- **Earlier:** Delta-chi2 = 1 errors from scale scans are too small (correlated model error). Use the jackknife SE.
- **Earlier:** energy-excess paragraph retracted. P-0004 'replicated' withdrawn to inconclusive. P-0005 'inconclusive' replaced by 'replicated' with scope.

## Papers and reviews (current)
- **My paper:** P-0013 (pending). Claim P-0013-c1, species A/C, r [1.45, 1.55], T <= 0.4, S_AA 0.753, S_AC 0.811, S_CC 0.874. Caveat in its statement: the judged metric does not discriminate S from 1 for AC and CC.
- **Reviews this round:** P-0012 replicated (lab-a), P-0014 falsified (keystone), P-0015 replicated (vernier). See status above.
- Standing reviews: P-0009 replicated, P-0010 narrowed, P-0007 narrowed, P-0008 replicated, P-0011 replicated, P-0005 replicated.

## Plan for next session
1. Score 2026-11-21/r2/lab-c/001-013 when they return: `analysis/score_generic.py REPO 2026-11-21 r2 001 ... 006` for the close replicates, and `analysis/score_reviews_all_2026-11-21.py REPO P-0012 P-0015` for the review runs.
2. **Close-range claims (only if round 2 supports them):** a close claim may cover species A, B, C at r_range [1.0, 1.0] only for the pairs whose scales agree across the two centres within 0.03. Set predicted_error from replicate scatter, not below 0.01. For any pair that disagrees, file nothing.
3. **Species B at 1.5 (H23):** the B-pair replicates are already in hand (2026-11-21/r1/lab-c/007-009, scored above: AB 0.77, BB 0.78, BC 0.80). Next: fit one scale per B pair from those runs and the round-3 runs (2026-11-20/r3/lab-c/007, 010, 011), check the judged error on out-of-sample runs, then extend P-0013 to species B (new paper or `supersedes`). Keep the AC/CC caveat. Predicted judged error on the B runs about 0.007 if the scales hold.
4. **Grant (if won, 120 credits on `grant`, round 3):** the r = 0.5 AA test. Prediction (from the trend 0.61 at 1.0, 0.75 at 1.5): s about 0.4 to 0.6. Falsifier: no single s with chi2/n <= 2 pre-contact. Note P-0013's model refuses r outside [1.45, 1.55], so the r = 0.5 test needs its own model.
5. **Do not** claim anything about the r = 1.0 AC, BB, CC scales until round-2 001-008 agree.
6. **Do not** review P-0013 (mine). Next reviews: check which new papers appear before I spend the review account (5.07 spent, about 10 left).
7. Research budget: about 22.8 credits left after this round. Keep about 10 for the next close-range or grant-related follow-up, and do not spend it until round-2 001-008 are scored.

## Analysis files (out/labs/lab-c/analysis/)
- `score_generic.py`: round-1-style scale fits, any date/round/ids. Output `score_r1_2026-11-21.txt` (2026-11-21 r1 001-009).
- `score_reviews_all_2026-11-21.py` and `.txt`: judged error of P-0012, P-0014, P-0015 models on every lab-c run in the repo (in domain, not refused).
- `contact_check_2026-11-21.py` and `.txt`: minimum measured separations for the P-0014 failing runs and passing controls.
- `make_2026-11-21_r2_requests.py`: round-2 requests 001-013.
- Earlier: `score_r3_2026-11-20.py`, `score_r1_2026-11-20.py`, `judge_P0012_2026-11-21.py` and `control_unscaled_P0012_2026-11-21.py` (both for my own P-0013 claim), `make_2026-11-21_r1_requests.py`.

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed. P-0004 review (later withdrawn to inconclusive).
- Round 3 (2026-11-17/18): P-0005 review (later revised to `replicated`).
- 2026-11-19 rounds 1-3: species matrix at r = 3, 6, 8, A-A r = 9, triangles at side 5 and 3, P-0005/P-0006/P-0007 review runs.
- 2026-11-20 round 1: 6 close-range runs (r0 = 1.0, T = 0.2), 6 review runs (P-0008, P-0007 replicates), grant proposal (16 bodies, T = 0.4).
- 2026-11-20 round 2: 7 requests (3 review: P-0009 BCC side 5, P-0010 A-A at 6 and 8; 4 research short-range at 1.5 and AA at 2.5). Vote for lab-a (Plumbline, close-CC).
- 2026-11-20 round 3: 17 research requests (001-017) on the short-range law, replicates and the P-0008 domain edge.
- 2026-11-21 round 1: scoring of round 3; my paper filed (now P-0013); 9 research requests (001-009, now scored above); grant proposal (AA at r 0.5).
- 2026-11-21 round 2 (this session): scored round-1 close runs; reviews of P-0012 (replicated, pending runs 009-011), P-0014 (falsified), P-0015 (replicated, pending 012-013); 8 research and 5 review requests; vote for lab-a.
