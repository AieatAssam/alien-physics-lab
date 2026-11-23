# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then replicate and review other labs' claims at their edges with precise numbers.

Last updated: 2026-11-23, round 2.

## Standing rules I apply to every claim and review

1. **Falsification needs a null above the bar.** A review can falsify a claim only if the zero-force null (all K = 0) on the cited runs sits above 3 times predicted_error. The tracker noise floor is about 0.005 RMSE/L, so predicted_error below about 0.005 is not reachable.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within 3 times predicted_error on at least 3 in-domain runs. A null above the bar is not needed for that. Say which verdict I am making and check the bar for that verdict.
3. **Check domain on the request positions, not on observed positions.** Start separation at exactly the r_range edge is risky: P-0022's model rejects a start separation of 1.950 (strict float guard). Cite runs at the centre of the band.
4. **Single-run precision.** Free fits of K over T <= 2 at separation 6.5 have scatter about 0.3 on K_A(B) (about 4 percent) and 0.3 on K_B(A) (2.5 to 3 percent). Monte Carlo at tracker noise 0.05 per coordinate, `analysis/mc_h20_2026-11-23.py`. Any state or orientation test at a 3 percent threshold needs pooled replicates.

## Cost model (confirmed)

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Every result so far matches (round-1 costs 1.03, 1.08, 1.24).

## Corrections to my own earlier work (kept)

1. The round-1 far-field table was labelled by starting separation, not by the separation inside the window (H14 withdrawn; see H22).
2. Window fits (labelled by observed mean separation) replace trajectory averages.
3. Short windows are unidentified when the null is less than 2 times the fit RMSE.
4. Lone-particle runs pass the domain test vacuously. 2026-11-19 r1 001, 002, 005, 006; r2 002, 004; r3 003 are not pair evidence.
5. Null errors must exceed the bar for falsification (rule 1).
6. Exponent and coupling are not separately identified from one short window.
7. Close pass breaks runs. 2026-11-21 r3 001 (A-B, separation 6, T = 6) passes through contact (r 1.46). Excluded.
8. Singular r^-2.5 models can blow up near contact (P-0014). Check minimum separation first.
9. (new) The round-3 "step" H19 was withdrawn in round 2 (see H22).

## Papers (mine, numbers as the gate assigned them)

- **P-0011** tracker noise for a lone particle (published).
- **P-0015** close-range B-C at separation 1.0.
- **P-0016** close-range A-C at separation 1.0.
- **P-0021** A-B pair at separation 7, at rest, constant K_A(B) = 7.75, K_B(A) = 10.97 at P = 2.5, T <= 6. Domain r 6.9 to 7.1, predicted_error 0.007. **Round-1 check (r1/006, T = 6, start 7.0, min separation 3.58, end 3.77): P-0021 model residual 0.0051 RMSE/L, well below the 0.021 falsification bar. P-0021 kept.** The earlier "at risk" note (r3/005 gave K = 7.21) is still open for H22: the constant-K claim is over T <= 6 from 7.0 and fits here.
- **P-0023** A-B pair at separation 9, at rest, constant K_A(B) = 6.16, K_B(A) = 8.70 at P = 2.5, T <= 10, domain r 8.9 to 9.1, predicted_error 0.006. Evidence 2026-11-22 r2/001, r2/002.
- **P-0022** is **Icarus's** (lab-b), not mine: A-B at separation 2, T <= 0.8, K_A(B) = 7.59, K_B(A) = 10.59, domain r 1.95 to 2.05, predicted_error 0.008, bar 0.024.

## Round-1 results (2026-11-23 r1 001-009), analysed this round

Script: `analysis/fit_r1_2026-11-23.py`. Free fits, P = 2.5, tracker only.

**Near-contact edge of P-0022 (001 to 005, T <= 0.8):**

| run | design | sep start | sep end | K_A(B) free | K_B(A) free | K_B(A), K_A(B) fixed 7.59 | fit RMSE/L | null RMSE/L |
|---|---|---|---|---|---|---|---|---|
| 001 | sep 2.0 horizontal | 1.968 | 0.362 | 7.75 | 10.58 | 10.64 | 0.00516 | 0.0220 |
| 002 | sep 2.0 vertical | 1.975 | 0.462 | 7.57 | 10.65 | 10.64 | 0.00481 | 0.0218 |
| 003 | sep 2.0 diagonal | 1.970 | 0.430 | 7.54 | 10.63 | 10.61 | 0.00489 | 0.0217 |
| 004 | sep 1.95 horizontal | 2.052 | 0.243 | 7.75 | 10.11 | 10.24 | 0.00524 | 0.0240 |
| 005 | sep 2.05 horizontal | 2.141 | 0.591 | 7.87 | 10.81 | 10.90 | 0.00519 | 0.0206 |

- Mean K_B(A) over 001 to 005 (free): 10.56 (scatter about 2.5 percent). Paper value 10.59 is within 0.3 percent of the mean. Individual runs 10.11 to 10.81 (-4.5 to +2 percent).
- The P-0022 model residual on 001 to 003 is 0.0048 to 0.0052 RMSE/L. The model rejects 004 at its exact start separation 1.950 (see rule 3). 005 not yet run through the model.
- Null RMSE/L 0.021 to 0.024 is at or just under the P-0022 falsification bar 0.024. P-0022 cannot be falsified by null-level data. It can be replicated.
- End separation is a sharp probe of K_B(A): 0.36 to 0.59 across the band. Consistent with the earlier estimate of slope 0.2 to 0.26 per unit K_B(A).

**H20 state test (007 to 009, sep about 6.5, T <= 2, free fits over t in [0, 2]):**

| run | arm | K_A(B) | K_B(A) | fit RMSE/L | null RMSE/L |
|---|---|---|---|---|---|
| 007 | outward, relative speed 0.3 | 7.83 | 11.02 | 0.00493 | 0.0073 |
| 008 | inward, relative speed 0.3 | 7.85 | 11.83 | 0.00491 | 0.0081 |
| 009 | at rest, vertical | 7.45 | 10.65 | 0.00498 | 0.0074 |

For comparison, r3/004 (at rest, horizontal, start 6.5, T = 2): K_A(B) 7.54, K_B(A) 11.42 (from round 3).

- **Monte Carlo of single-run scatter** (`analysis/mc_h20_2026-11-23.py`, truth K_A(B) 7.6, K_B(A) 11.2, noise 0.05, 12 reps each): K_A(B) sd 0.27 to 0.32 (about 4 percent); K_B(A) sd 0.27 to 0.38 (about 2.5 to 3.4 percent).
- **The pre-registered rule (3 percent of 7.5 = 0.23) cannot decide H20.** The single-run scatter (about 0.3) is larger than the rule's threshold. Runs 007 and 008 are at 7.83 and 7.85, which the rule would call "falsified", but a 1-sigma scatter gives the same result for a state-independent law. **I withdraw the 3 percent rule as a decision criterion. H20 is undecided.**
- Descriptive only: the two moving arms average K_A(B) 7.84, the at-rest arm (009 and r3/004) averages 7.50. Difference +0.34, about 1.4 sigma with these samples. Not significant. Round 2 adds replicates (below).

**P-0021 check (006, T = 6):** residual 0.0051 RMSE/L against P-0021's own model (bar 0.021). Keep. Minimum separation 3.58, so no close pass. This also means that the P-0021 domain (start 6.9 to 7.1, T <= 6) is supported by one run; r3/005 (start 7.0, T = 2, K = 7.21) and the plateau-shaped K(r) below remain the open question.

## Global picture of windowed K_A(B) at P = 2.5 (labelled by observed r)

| mean obs r | K_A(B) | source |
|---|---|---|
| 4.13 | 9.23 | r3 008 (wide window, r 3.2 to 4.65) |
| 4.80 to 4.90 | 8.37 to 8.41 | r1 001 to 004 (2026-11-22) |
| 5.30 | 8.55 | r3 001 |
| 5.63 | 8.27 | r3 002 |
| 5.85 | 8.33 (mean of three) | r3 003, 006, 007 |
| 6.38 | 7.54 | r3 004 |
| 6.57 (moving) | 7.83, 7.85 | r1 007, 008 (2026-11-23) |
| 6.57 (at rest, vertical) | 7.45 | r1 009 |
| 6.91 | 7.21 | r3 005 |
| 6.2 to 6.8 (moving) | 6.2 to 6.7 | 2026-11-22 r1/005, r2/001-002 |
| 7.4 to 7.6 | 5.9 to 6.4 | same |
| 8.2 to 8.9 | 5.8 to 6.1 | same, P-0023 at 9 gives 6.16 |

Reading: K_eff falls with r, about 9.2 at r 4 to about 6.0 at r 8.5 to 9. Log-log slope about -0.5 (apparent exponent about 3 at P = 2.5). The at-rest versus moving difference (H20) could bias the slope. Not a claim yet.

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
- **H13** (pairwise superposition): untested for more than two bodies. Keystone's grant proposal would test it.
- **H14** (far-field steepening): withdrawn. Replaced by H22.
- **H15** (P-0004-c2 magnitude): K_C(A) about -20.7 from three repeats, published -21.38. Flagged.
- **H16** (P-0014 A-A contact failure): integrator blows up after close approach. Filed as P-0014 falsification.
- **H17** (K_B(A)/K_A(B) = 1.41 at all separations): supported. Round-3 R values 1.37 to 1.52 at short windows, 1.38 to 1.44 at long windows.
- **H18** (m_A/m_B = 1.41 with momentum conservation): inference from H17, not tested directly.
- **H19** (K 8.3 to 6.3 step near r = 6, at rest): **withdrawn**. Round 3 (7.54, 7.21) and round 1 (7.45 vertical) give a smooth decline, not a step.
- **H20** (window K depends only on current r, not on state): **undecided**. Round 1 gives moving arms at 7.84, at rest 7.45 to 7.54 (about 1.4 sigma, not significant). Round 2 adds pooled replicates (see below).
- **H21** (position and orientation invariance for the A-B law): not falsified at 3 percent (round 3 006, 007 vs 003). Round 1 r1/002, 003, 009 agree with r1/001 within the single-run scatter.
- **H22** (K_eff(r) at P = 2.5 falls smoothly from about 9.2 at r 4 to about 6.0 at r 8.5): open working hypothesis.
- **H23** (new, placeholder): if H20 holds, K_eff is an r-only curve; if not, a speed-dependent law. Test only with pooled replicates.

## Round 2 (2026-11-23, this session)

Requests in `out/requests/2026-11-23/r2/lab-vernier/` (scripts `analysis/file_round2_2026-11-23.py`):

| request | account | design | purpose | cost |
|---|---|---|---|---|
| 001 to 004 | review, cites P-0022 | A-B, separation 2.0 (horizontal centred at 5, vertical, diagonal, horizontal offset at y 6), at rest, T = 0.8 | replication of P-0022 with four in-domain runs | 4 x 1.032 = 4.13 of 15 review credits |
| 005 to 008 | research | at rest, horizontal, separation 6.5, T = 2 | H20 at-rest replicates | 4 x 1.08 |
| 009 to 012 | research | outward, relative speed 0.3, separation 6.5, T = 2 | H20 outward replicates | 4 x 1.08 |
| 013 to 016 | research | inward, relative speed 0.3, separation 6.5, T = 2 | H20 inward replicates | 4 x 1.08 |

**Review filed**: `out/reviews/P-0022/lab-vernier.json`, verdict **replicated**, evidence r2/001 to r2/004 (review account). Pre-registered expectations: paper-model error on each of the four runs about 0.005 RMSE/L, against the 0.024 bar (3 x 0.008). Replicated stands if at least 3 of 4 are at or below 0.024. Failing that, the review is logged unsupported. Limits stated in the comment: domain 1.95 to 2.05, T <= 0.8, not a falsification test.

**Predictions for round 2 (written before results):**
- P-0022 runs 001 to 004 each give paper-model error of 0.005 or less (replicated).
- H20: pooled at-rest (005 to 008 and 009, plus r3/004 if its start matches) versus pooled moving (007, 008 and 009 to 016). Per-arm SE on K_A(B) of about 0.3 over sqrt(n). With 6 at-rest and 10 moving runs, SE on the difference is about 0.13. A state-independent law predicts a difference within 2 SE of zero. A difference above 3 SE (about 0.4 on K_A(B)) would be evidence for state dependence. Written before the data.

## Grant

- **Round 2 vote: lab-keystone** (`out/grants/2026-11-23/votes/lab-vernier.json`). Reason: it is the only proposal that tests N > 2 additivity directly (H13, which crowd-8 depends on). Cheap (cost about 1.1), residual threshold set at the tracker floor. Power is limited at T = 0.3.
- Other proposals considered: Plumbline (N = 9, T = 50, cost about 10 per run, chaos at long T makes a pairwise-sum test hard to falsify cleanly). Icarus (3 particles, T = 2.5, a sharp centre-of-mass test of equal-and-opposite forces, cheap and clean; I rank it second). My own (A-B at separation 2, K_B(A) to 1 percent): the round-1 data already show the endpoint precision (K_B(A) = 10.56 mean across five runs), so the grant is largely done in practice.
- Proposal for 2026-11-23 is on file (`out/grants/2026-11-23/proposals/lab-vernier.json`). I have no grant credits tonight.

## Open problems: assessment

- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025)**: not reachable with this tracker (noise floor 0.005). Do not file.
- **close-AB (bounty 2), close-AC (bounty 2)**: need r_range starting at 1 or less. Blocked by H12.
- **crowd-8 (bounty 3)**: multi-body. Not attempted (H13 untested).
- **contested-P-0014, disputed-P-0003, -P-0006, -P-0007**: not addressed.

## Reviews: other papers (checked, none filed this round)

- P-0012, P-0013, P-0017, P-0018, P-0019, P-0020: zero-force nulls sit below 3 times predicted_error on my earlier estimates (bars 0.024 to 0.03). Falsification not possible with my data. Not filed.
- P-0024 (Keystone, A-A exponent 2.10): not checked this round.
- P-0021 and P-0023 (mine): not reviewed by others yet.

## Budgets, 2026-11-23

- **Research**: 40 allowed. Used before this session: 9.63 (round 1, nine runs). Round 2 plan: 12 runs at 1.08 = 12.96. Remaining after filing: about 17.4.
- **Review**: 15 allowed. Round 2 plan: four runs at 1.032 = 4.13 (P-0022 replication). Remaining: about 10.9.
- **Grant**: none for this lab.

## Plan for next round (when 2026-11-23 r2 results arrive)

1. Check results `results/2026-11-23/r2/lab-vernier/001-016`. Confirm costs and the status of each run.
2. Review P-0022: compute paper-model RMSE/L on 001 to 004 with `fit_tools.model_residuals`. If at least 3 are at or below 0.024, the replicated verdict stands. If not, the review is logged unsupported, and I should record it as an error.
3. H20: free fits over t in [0, 2] on 005 to 016. Pool each arm. Compare with the SE from the MC. Report the difference in SE units. Do not use the 3 percent rule.
4. If H20 is undecided, file more replicates only if the pooled difference is above 1 SE. Otherwise move on to a different question (the r-dependence H22 at fixed state).
5. Do not file a review unless the null exceeds the bar.

## Not read

`gate/`, `tools/`, `exam_papers.json`, predictor or score files. I did not read them and will not.
