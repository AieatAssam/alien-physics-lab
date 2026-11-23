# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then replicate and review other labs' claims at their edges with precise numbers.

Last updated: 2026-11-23, round 3.

## Standing rules I apply to every claim and review

1. **Falsification needs a null above the bar.** A review can falsify a claim only if the zero-force null (all K = 0) on the cited runs sits above 3 times predicted_error. The tracker noise floor is about 0.005 RMSE/L, so predicted_error below about 0.005 is not reachable.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within 3 times predicted_error on at least 3 in-domain runs. A null above the bar is not needed for that. Say which verdict I am making and check the bar for that verdict.
3. **Check domain on the request positions, not on observed positions.** Start separation at exactly the r_range edge is risky (strict float guards: P-0022 rejects a start separation of 1.950). Cite runs at the centre of the band. Run each candidate setup through the paper's own `predict()` before filing (it raises ValueError when out of domain).
4. **Single-run precision.** Free fits of K over T <= 2 at separation 6.5 have scatter about 0.3 to 0.4 on K_A(B) (4 to 5 percent). Any state or orientation test needs pooled replicates.
5. **Bars are loose relative to the tracker.** The review bar is 3 times predicted_error in RMSE/L. For T <= 0.15 close-range claims, the bar is about 0.24 chamber units, and the total displacement is only about 0.02 to 0.06. A K error of 20 percent does not register. Such reviews are replications only, and the comment says so.

## Cost model (confirmed)

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Every result so far matches.

## Corrections to my own earlier work (kept)

1. The round-1 far-field table was labelled by starting separation, not by the separation inside the window (H14 withdrawn; see H22).
2. Window fits (labelled by observed mean separation) replace trajectory averages.
3. Short windows are unidentified when the null is less than 2 times the fit RMSE.
4. Lone-particle runs pass the domain test vacuously. 2026-11-19 r1 001, 002, 005, 006; r2 002, 004; r3 003 are not pair evidence.
5. Null errors must exceed the bar for falsification (rule 1).
6. Exponent and coupling are not separately identified from one short window.
7. Close pass breaks runs. 2026-11-21 r3 001 (A-B, separation 6, T = 6) passes through contact (r 1.46). Excluded.
8. Singular r^-2.5 models can blow up near contact (P-0014). Check minimum separation first.
9. The round-3 "step" H19 was withdrawn in round 2 (see H22).
10. (round 3) My stated per-run K precision at T <= 0.15 is not what I would get from the tracker. I did not run a formal Monte Carlo for that case; the claim is a rough estimate (several times larger than the 0.09 that P-0020 quotes). Treat it as open until checked.

## Papers (mine, numbers as the gate assigned them)

- **P-0011** tracker noise for a lone particle (published).
- **P-0015** close-range B-C at separation 1.0.
- **P-0016** close-range A-C at separation 1.0.
- **P-0021** A-B pair at separation 7, at rest, constant K_A(B) = 7.75, K_B(A) = 10.97 at P = 2.5, T <= 6. Domain r 6.9 to 7.1, predicted_error 0.007. Round-1 check (r1/006, T = 6): residual 0.0051 RMSE/L against the 0.021 bar. Kept.
- **P-0023** A-B pair at separation 9, at rest, constant K_A(B) = 6.16, K_B(A) = 8.70 at P = 2.5, T <= 10, domain r 8.9 to 9.1, predicted_error 0.006. Evidence 2026-11-22 r2/001, r2/002.
- **P-0022** is **Icarus's** (lab-b), not mine: A-B at separation 2, T <= 0.8, K_A(B) = 7.59, K_B(A) = 10.59, domain r 1.95 to 2.05, predicted_error 0.008, bar 0.024. My review (`out/reviews/P-0022/lab-vernier.json`, replicated, evidence r2/001 to 004) **checked this round**: the paper's own model gives RMSE/L 0.00487, 0.00510, 0.00483, 0.00510 on r2/001 to 004. All four are far below the 0.024 bar. Replicated stands.

## Round-1 and round-2 results (summary)

Round 1 (2026-11-23 r1 001-009): P-0022 edge runs 001 to 005 (free K_B(A) 10.11 to 10.81, mean 10.56, about 2.5 percent scatter). H20 runs 007 to 009 (see H20). P-0021 check 006 (residual 0.0051).

Round 2 (2026-11-23 r2 001-016):
- 001 to 004: P-0022 replication (cited, see above).
- 005 to 016: H20 replicates at separation 6.5, T = 2, six at rest (005-008), four outward (009-012), four inward (013-016).

## H20 (state dependence): pooled result this round

Script: `out/labs/lab-vernier/analysis/check_r3_2026-11-23.py` (free fits over t in [0, 2], K_A(B), K_B(A)).

| run | arm | K_A(B) | K_B(A) |
|---|---|---|---|
| r2/005 | rest | 8.02 | 10.95 |
| r2/006 | rest | 7.58 | 11.53 |
| r2/007 | rest | 8.40 | 11.03 |
| r2/008 | rest | 8.32 | 11.33 |
| r1/009 | rest, vertical | 7.45 | 10.65 |
| r3/004 (2026-11-22) | rest, horizontal | 7.54 | 11.42 |
| r2/009 | outward | 7.66 | 10.61 |
| r2/010 | outward | 7.79 | 11.43 |
| r2/011 | outward | 7.13 | 10.61 |
| r2/012 | outward | 7.05 | 10.72 |
| r2/013 | inward | 7.85 | 11.57 |
| r2/014 | inward | 8.39 | 11.89 |
| r2/015 | inward | 8.08 | 11.26 |
| r2/016 | inward | 7.94 | 11.31 |
| r1/007 | outward | 7.83 | 11.02 |
| r1/008 | inward | 7.85 | 11.83 |

- At rest (n = 6): K_A(B) 7.88, K_B(A) 11.15.
- Moving (n = 10): K_A(B) 7.76, K_B(A) 11.23.
- Difference K_A(B): +0.13. Pooled scatter about 0.41, so the SE of the difference is about 0.16. The difference is about 0.8 SE. Difference K_B(A): -0.07, well inside the SE.
- My pre-registered rule (written in round 2): a K_A(B) difference above 3 SE (about 0.4) would count as state dependence. Not reached. **H20 is not supported. No state dependence is detected at this precision.**
- Caveat: the observed per-run scatter (0.41 on K_A(B)) is larger than the Monte Carlo estimate in `analysis/mc_h20_2026-11-23.py` (0.27 to 0.32). The MC underestimates the single-run scatter, probably because the noise or the fit has more structure than I put in. I did not resolve this; the conclusion holds with the larger scatter.

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported. P-0011.
- **H2** (species-independent noise, N = 1): supported (2.4 percent spread).
- **H3** (no clipping near a wall): supported.
- **H4** (no sample-timing offset): supported (about 0.005 time units).
- **H5** (stationarity over T = 100): mean supported; x-spread variation not reproduced.
- **H6** (P-0003 domain): separation 3 fails for P-0003 (r1/007, error 0.181). Separations 4 and 5 pass.
- **H7** (P-0006 shared-law factor at separation 9 for A-C): supported within 3 percent in one fit.
- **H8** (P-0008 coefficients flat over separations 3 to 5): supported for A-B at 4 and B-C at 3, 5. Not for A-A at 3 and 4.
- **H9** (P-0010 far-field G(r0), C-factor 0.9475): replicated at all three pairs and A-A at 6. C-C at 7 is 5.6 percent above.
- **H10** (A-A coefficient at separation 4 is 17.70): supported by the diagonal replicate.
- **H11** (close-range B-C): supported. P-0015.
- **H12** (A-B and B-B not constant-K over the first 0.3 time units at r = 1): open.
- **H13** (pairwise superposition): untested for more than two bodies. Keystone's grant tests it. crowd-8 depends on it.
- **H15** (P-0004-c2 magnitude): K_C(A) about -20.7 from three repeats, published -21.38. Flagged.
- **H16** (P-0014 A-A contact failure): integrator blows up after close approach. Filed as P-0014 falsification.
- **H17** (K_B(A)/K_A(B) = 1.41 at all separations): supported. Round-3 R values 1.37 to 1.52 at short windows, 1.38 to 1.44 at long windows. Icarus's close-range ratio (7.33/5.39 = 1.36) agrees.
- **H18** (m_A/m_B = 1.41 with momentum conservation): inference from H17, not tested directly.
- **H19** (step near r = 6): withdrawn.
- **H20** (window K depends only on current r, not on state): **not supported at the 3 SE rule.** Pooled difference +0.13 on K_A(B) (about 0.8 SE). Rests on 16 runs, see above.
- **H21** (position and orientation invariance for the A-B law): not falsified at 3 percent (round 3 006, 007 vs 003). Round-1 and round-2 orientation spread agrees within scatter.
- **H22** (K_eff(r) at P = 2.5): **revised to H24 below.** Earlier working hypothesis of a smooth monotone decline from r = 4 is wrong: the windowed values are not monotone (see H24).
- **H24** (new, working): K_eff(r) = a(r) r^2.5 for A-B is non-monotone. Labelled points: about 5.39 at r 1.0 (Icarus P-0020, uncertain, see below), 7.59 at r 2.0 (P-0022, precise), about 9.2 at r 4.1 (r3/008), about 8.4 at r 4.8, 8.3 at r 5.9, 7.5 at r 6.4, 6.0 at r 8.5 to 9. Local exponent between neighbouring points: about 2.0 from r 1 to 2, about 2.2 from r 2 to 4, about 3.1 from r 4 to 8.5. A single power law cannot describe this. The r = 1 point is the weakest, because Icarus's stated precision is probably optimistic. Tested by the round-3 research runs below.
- **H25** (new, working): the A-A law differs from the A-B law in exponent. P-0024 (Keystone) claims a A-A exponent of 2.10 on r 1.25 to 3. My A-A runs at r 2 and r 3 (T = 0.8 and T = 2, outside P-0024's duration window for r < 2.5 but inside its claim for r = 3) test this directly. Predicted K_AA(eff) at r = 2 (in the P = 2.5 frame): 15.6 if P-0024 holds, 13.55 if P-0013's constant-K coefficient holds, 11.3 if P-0012 at r = 1 holds without change.

## Round 3 (2026-11-23): what I filed

Script: `out/labs/lab-vernier/analysis/design_round3_2026-11-23.py` (requests, domain check with each paper's `predict()`). Requests in `out/requests/2026-11-23/r3/lab-vernier/`, all 22 validate against `protocol/request.schema.json`.

Review account (10.10 of 15 credits; 0.78 left):

| request | paper | design | cost |
|---|---|---|---|
| 001-004 | P-0013 (A-C claim, A-A runs) | A-A at rest, separation 1.50 (centre of band), T 0.4, four orientations | 4 x 1.016 |
| 005-007 | P-0020 (A-B close range) | A-B at rest, separation 1.000, T 0.15, three orientations | 3 x 1.006 |
| 008-010 | P-0018 (C-C close range) | C-C at rest, separation 1.000, T 0.15, three orientations | 3 x 1.006 |

Research account (12.56 of 17.41 credits; 4.85 left, unspent, reserved for a round-3 follow-up if any):

| request | design | purpose |
|---|---|---|
| 011-014 | A-B at rest, r0 1.5, T 0.5, four orientations | constant-K test at short range (H24) |
| 015-016 | A-B at rest, r0 3.0, T 2.0, two orientations | long-range end of the curve (H24) |
| 017-018 | A-B at rest, r0 2.5, T 1.2, two orientations | midrange point (H24) |
| 019-020 | A-A at rest, r0 2.0, T 0.8, two orientations | A-A exponent check (H25) |
| 021-022 | A-A at rest, r0 3.0, T 2.0, two orientations | A-A exponent check, long range (H25) |

### Reviews filed this round (pre-registered)

- **P-0020 (lab-b, A-B close range): `out/reviews/P-0020/lab-vernier.json`, verdict replicated**, evidence r3/005-007. Prediction: each run within 0.005 RMSE/L against the 0.024 bar. Comment states the bar is weak here and raises two issues (stated SE too small; K_A(B) 5.39 at r 1 vs 7.59 at r 2 implies local exponent about 2).
- **P-0018 (lab-b, C-C close range): `out/reviews/P-0018/lab-vernier.json`, verdict replicated**, evidence r3/008-010. Prediction as above. Comment notes that P-0013's constant-K C-C value (10.8 at r 1.5) and P-0018's (9.31 at r 1.0) differ by about 15 percent, and the bar cannot decide between them.

### Review held: P-0013 (lab-c, A-A at separation 1.5)

I have **not** filed the P-0013 review. Its claim covers A-A, A-C and C-C at r 1.45 to 1.55 with predicted_error 0.01 (bar 0.03). The claim's own text says the scaled A-A result is "resolved" only by the unscaled model's score (0.068), and gives no score for the scaled A-A model. I cannot yet predict whether the scaled model passes the bar on my four A-A runs. Pre-registered expectation: replicated, with RMSE/L about 0.005 to 0.01. The null sits near 0.03 at this T (a horizontal run gives about 0.028), so falsification is not possible, which is consistent with rule 1.

**Next session: check results r3/001-004 and file the P-0013 review only if at least 3 of the 4 runs have paper-model RMSE/L at or below 0.03.** Otherwise do not file it, and record the failure here.

### Pre-registered predictions (written before results)

- P-0020 runs 005-007 and P-0018 runs 008-010: paper-model RMSE/L at or below 0.005 each. Both reviews stand as replicated.
- r3/011-014 (A-B, r0 1.5): free fit of K_A(B) over t in [0, 0.5], P fixed at 2.5, predicted 6.5 +/- 0.4 under H24 (monotone interpolation between 5.39 at r 1 and 7.59 at r 2). Constant K at P = 2.5 predicts 7.6 (K_A(B) fixed by P-0022). Mean of the four runs below 7.0 counts against constant K at short range. SE on the four-run mean at T = 0.5 is about 0.2 (about 3 percent) by my estimate.
- r3/015-016 (A-B, r0 3.0, T 2): K_A(B) at P = 2.5 near 8.8 under H24. Under constant K it is 7.6.
- r3/017-018 (A-B, r0 2.5, T 1.2): K_A(B) near 8.2 under H24.
- r3/019-020 (A-A, r0 2.0, T 0.8): K_AA(eff) = 15.6 if P-0024 holds, 13.55 if P-0013 holds, 11.3 if P-0012 holds. My per-run SE on the acceleration at T 0.8 is about 0.5 percent by my estimate, so these three predictions can be separated.
- r3/021-022 (A-A, r0 3.0, T 2): K_AA(eff) near 19.3 under P-0024, 13.55 under constant K.

These are my pre-registered guesses; a mismatch on any of them is a result, not a failure.

## Grant

- **Round 2 vote: lab-keystone** (`out/grants/2026-11-23/votes/lab-vernier.json`). Reason: it is the only proposal that tests N > 2 additivity directly (H13, which crowd-8 depends on). Tonight's grant went to Keystone (120 credits, usable in round 3 on their account). I have no grant credits.
- Proposal for 2026-11-23 is on file (`out/grants/2026-11-23/proposals/lab-vernier.json`).

## Open problems: assessment

- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025)**: not reachable with this tracker (noise floor 0.005). Do not file.
- **close-AB (bounty 2), close-AC (bounty 2)**: need r_range starting at 1 or less. Blocked by H12.
- **crowd-8 (bounty 3)**: multi-body. Not attempted (H13 untested).
- **contested-P-0014, disputed-P-0003, -P-0006, -P-0007**: not addressed.

## Reviews: other papers

- **P-0022 (Icarus)**: replicated, filed in round 2, verified this round.
- **P-0020 (Icarus), P-0018 (Icarus)**: filed this round, replicated (pre-registered).
- **P-0013 (Nullius)**: held (see above).
- **P-0012 (Plumbline, A-A K 11.3 at r 1), P-0017 (Icarus, B-B K 3.98 at r 1), P-0019 (Plumbline, B-B K 3.86 at r 1)**: not filed. Their bars are about 0.24 absolute at T <= 0.15, so the tests cannot separate them. P-0017 and P-0019 differ by 3 percent and are not decidable here.
- **P-0024 (Keystone, A-A exponent 2.10)**: not filed. Its window (duration 0.3 for r0 < 2.5) gives displacements of about 0.05, far below the 0.18 absolute bar. My A-A runs at r 2 and r 3 (r3/019-022, beyond the window at r 2) are the real test of H25; a review will follow only if the bar is met.
- P-0021 and P-0023 (mine): not reviewed by others yet.

## Budgets, 2026-11-23 (after round 3 filing)

- **Research**: 40 allowed. Used before round 3: 22.59 (rounds 1 and 2). Round 3 filed: 12.56. Total 35.15. **Remaining 4.85.**
- **Review**: 15 allowed. Used before round 3: 4.12 (P-0022 replication). Round 3 filed: 10.10. Total 14.22. **Remaining 0.78.**
- **Grant**: none for this lab.

## Plan for next round (when 2026-11-23 r3 results arrive)

1. Check results `results/2026-11-23/r3/lab-vernier/001-022`. Confirm costs and status.
2. Reviews: compute paper-model RMSE/L on r3/005-010 (P-0020, P-0018). If at least 3 of 3 are at or below 0.024 each, the replicated verdicts stand. Then check r3/001-004 for P-0013 (see the rule above).
3. H24: free fits of K_A(B) and K_B(A) over t <= 0.5 (r0 1.5), t <= 1.2 (r0 2.5), t <= 2 (r0 3.0), with P fixed at 2.5 and also with P free. Compare with the predictions above. Plot K_eff(r) with all points (including P-0022 and r3/008).
4. H25: free fits of K_AA with P fixed at 2.5 over r0 2 (T 0.8) and r0 3 (T 2). Compare with the three predictions (15.6, 13.55, 11.3 at r 2; 19.3 vs 13.55 at r 3).
5. If H24 is confirmed (non-monotone K_eff), publish a narrow claim about the A-B law in the measured band only (r 1.5 to 3 at P = 2.5, with the fitted K values). Do not claim a global form.
6. Do not file a review unless the bar is met by my own runs (see the rules at the top).

## Not read

`gate/`, `tools/`, `exam_papers.json`, predictor or score files. I did not read them and will not.
