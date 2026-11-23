# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then replicate and review other labs' claims at their edges with precise numbers.

Last updated: 2026-11-23, round 1.

## Standing rule I now apply to every claim and review

A review can only test a claim if the zero-force null (all K = 0) on the cited runs sits **above** 3 times predicted_error. The tracker noise floor is 0.005 RMSE/L, so predicted_error below about 0.005 is not reachable and the bar is 0.015 or more. Short runs (T <= 2, displacements of about 0.1) give nulls near 0.009 to 0.011 and wrong-K errors near 0.001 to 0.003. Both sit under any honest bar. **Discriminating evidence needs long runs or large displacements, or a close approach where K is sensitive.** I now check both numbers before filing a paper or a review.

## Cost model (confirmed)

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Every result so far matches. Budget is rarely binding; design is.

## Corrections to my own earlier work (kept)

1. The round-1 far-field table was labelled by starting separation, not by the separation inside the window. H14 (steepening from that table) was withdrawn. It is revisited below as H22 with window labels.
2. Window fits (labelled by observed mean separation) replace trajectory averages.
3. Short windows are unidentified when the null is less than 2 times the fit RMSE (see sensitivity column below).
4. Lone-particle runs pass the domain test vacuously. 2026-11-19 r1 001, 002, 005, 006; r2 002, 004; r3 003 are not pair evidence.
5. Null errors must exceed the bar (see standing rule).
6. Exponent and coupling are not separately identified from one short window.
7. Close pass breaks runs. 2026-11-21 r3 001 (A-B, separation 6, T = 6) passes through contact (r 1.46). Excluded.
8. Singular r^-2.5 models can blow up near contact (P-0014). Check minimum separation first.

## Papers (mine, numbers as the gate assigned them)

- **P-0011** tracker noise for a lone particle (published).
- **P-0015** close-range B-C at separation 1.0.
- **P-0016** close-range A-C at separation 1.0.
- **P-0021** A-B pair at separation 7, at rest, constant K_A(B) = 7.75, K_B(A) = 10.97 at P = 2.5, T <= 6. Domain r 6.9 to 7.1, predicted_error 0.007. Evidence 2026-11-21 r3/003, r1/010. **At risk**: round-3 r3/005 (start 6.9, T = 2) gave K = 7.21, not 7.75. The decisive test is round-1 request 006 (below).
- **P-0023** (this was filed as "separation 9" and renumbered from the P-0022 I had expected). A-B pair at separation 9, at rest, constant K_A(B) = 6.16, K_B(A) = 8.70 at P = 2.5, T <= 10, domain r 8.9 to 9.1, predicted_error 0.006. Evidence 2026-11-22 r2/001, r2/002. Out-of-sample 0.0051 and 0.0052 RMSE/L.
- **P-0022** is **Icarus's** (lab-b), not mine: A-B at separation 2, T <= 0.8, K_A(B) = 7.59, K_B(A) = 10.59, domain r 1.95 to 2.05, predicted_error 0.008. I am not the author.

No paper filed this round (see plateau check below).

## Round 3 results (2026-11-22 r3 001-008), analysed this round

Free fit of K_A(B), K_B(A) at P = 2.5 over t in [0, 2], all A-B at rest (`analysis/fit_r3_2026-11-22.py`). "null/fit" is the zero-force RMSE/L divided by the fit RMSE/L, a sensitivity measure.

| run | start (designed) | placement | mean obs r | min obs r | K_A(B) | K_B(A) | R | fit RMSE/L | null/fit |
|---|---|---|---|---|---|---|---|---|---|
| 001 | 5.5 | centred | 5.30 | 4.82 | 8.55 | 12.13 | 1.42 | 0.00489 | 2.2 |
| 002 | 5.8 | centred | 5.63 | 5.16 | 8.27 | 11.71 | 1.415 | 0.00498 | 1.9 |
| 003 | 6.0 | centred | 5.85 | 5.43 | 8.43 | 11.59 | 1.374 | 0.00487 | 1.8 |
| 004 | 6.5 | centred | 6.38 | 6.01 | 7.54 | 11.42 | 1.516 | 0.00498 | 1.5 |
| 005 | 7.0 | centred | 6.91 | 6.52 | 7.21 | 10.51 | 1.458 | 0.00525 | 1.3 |
| 006 | 6.0 | y = 2 | 5.85 | 5.38 | 8.38 | 11.73 | 1.399 | 0.00497 | 1.8 |
| 007 | 6.0 | vertical | 5.85 | 5.43 | 8.18 | 11.48 | 1.403 | 0.00493 | 1.8 |
| 008 | 4.5 | centred | 4.13 | 3.21 | 9.23 | 12.98 | 1.406 | 0.00488 | 3.8 |

Results against the pre-registered rules (written before the data):

- **Reproducibility (003 within 3% of 8.15): missed by 0.3 points** (8.43 is 3.4% above 8.15). The same-start replicates 003, 006, 007 give 8.43, 8.38, 8.18: mean 8.33, spread 1.5%. The earlier 8.15 (r1 003 window) is 2% below that mean and is within the spread of the replicates. Precision at start 6.0 is about 1.5% per run, better than predicted.
- **H19 (K about 6.3 above the step, at rest)**: the prediction "K(004) or K(005) near 6.3" fails. K(004) = 7.54 and K(005) = 7.21 are both 15 to 20% above 6.3 and 9 to 13% below 8.3. Neither falsification clause fires, because no run is within 3% of 8.3 at r > 6.5 and K(001) = 8.55 is not within 3% of 6.3. **H19 as a sharp step to 6.3 is not supported.** Runs 004 and 005 are weakly constrained (null/fit 1.5 and 1.3) but the 8.3 to 7.2 difference is about 4 sigma by the design study below.
- **H20 (window K depends only on r, not start state)**: not falsified by its written rule (004 and 005 are not within 3% of 8.3). But at-rest windows at r 6.4 to 6.9 (7.2 to 7.5) sit above the later-time moving windows at the same r (6.2 to 6.7, from 2026-11-22 r1/005, r2/001-002). That is a state-dependence hint, not a test. Round-1 requests 007 and 008 test it directly.
- **H21 (position and orientation)**: 006 (y = 2) gives 8.38 and 007 (vertical) gives 8.18, against 8.43 for 003. Within 3% of each other: **H21 not falsified** at this precision.

### Global picture of windowed K_A(B) at P = 2.5 (all A-B runs, labelled by observed r)

| mean obs r | K_A(B) | source |
|---|---|---|
| 4.13 | 9.23 | r3 008 (wide window, r 3.2 to 4.65) |
| 4.80 to 4.90 | 8.37 to 8.41 | r1 001 to 004 |
| 5.30 | 8.55 | r3 001 |
| 5.63 | 8.27 | r3 002 |
| 5.85 | 8.33 (mean of three) | r3 003, 006, 007 |
| 6.38 | 7.54 | r3 004 |
| 6.91 | 7.21 | r3 005 |
| 6.2 to 6.8 (moving) | 6.2 to 6.7 | r1 005; r2 001, 002 (later windows) |
| 7.4 to 7.6 | 5.9 to 6.4 | r1 005, r2 001, 002 |
| 8.2 | 5.9 to 6.0 | r1 006, 007; r2 001, 002 |
| 8.7 to 8.9 | 5.8 to 6.1 | r1 006, 007; r2 001, 002 |
| 9 (full T = 10) | 6.16 | P-0023 |

Reading: **K_eff falls smoothly with r**, from about 9.2 at r 4.1 to about 6.0 at r 8.5 to 9. A log-log fit over these points gives slope about -0.5, i.e. an apparent exponent near 3.0 with P fixed at 2.5. This is **H22 (new, hypothesis)**: the apparent exponent is about 3, with a smooth decline and no step. Caveats: the r 4.1 point is a wide window; the at-rest versus moving difference (H20) could bias the slope; and this is a fit label, not a local exponent. It is not a claim yet.

**Step versus smooth decline**: the new at-rest points (6.38 and 6.91) do not show a step at 6. They show a decline through the 6 to 7 range. My earlier "step" (H19) came from mixing at-rest and moving windows. Withdraw the step language. Keep H22 as the working hypothesis.

## Round-1 plausibility checks (this session, analysis/)

1. **P-0022 (Icarus, A-B separation 2, T <= 0.8, bar 0.024)** — `analysis/review_edges_2026-11-23.py`:
   - zero-force null RMSE/L vs a "true" K of 7.7/11.6 = **0.0235**, just under the bar of 0.024. A no-force model would pass the bar, so a review would not test the claim. **Not filed.**
   - paper-model vs the same truth = 0.0025. A 10% error in K_B(A) is far below the bar. The bar cannot falsify P-0022's K_B(A) even if it is off.
   - Near-contact sensitivity (`analysis/edge_p0022_2026-11-23.py`): with K_A(B) = 7.59 fixed, the end separation at T = 0.8 is 0.696 (K_B(A) = 9.0), 0.450 (10.59, the paper's value, reproduced), 0.368 (11.0), 0.211 (11.6), 0.030 (12.0). Slope about 0.2 to 0.26 per unit K_B(A). **So the end separation is a sharp probe of K_B(A) near contact, even though the review bar cannot use it.** My own r2/004 (separation 2, T = 0.5, centred) gave K_B(A) = 11.65, 10% above 10.59 (noisy short window, not conclusive). Round-1 requests 001 to 005 test it.
2. **Constant-K plateau claim (start 5.4 to 6.1, at rest, T <= 2)** — `analysis/claim_plateau_2026-11-23.py`:
   - constant-K predictor (8.33 / 11.66) residuals on r3 001, 002, 003, 006, 007: **0.0049 to 0.0050 RMSE/L**, at the noise floor. The model fits.
   - but a wrong K of 7.5, 6.66 or 6.3 (10%, 20%, 24% low) moves RMSE/L by only **0.0012, 0.0023, 0.0028**. With predicted_error 0.0055 the falsification bar is 0.0165. **The claim could never be falsified, and its zero-force null (about 0.010) also sits under the bar.** Not published. This is the reason no paper is filed this round.
3. **P-0021 close-pass check (own claim, start 7.0 at rest, T = 6, model K 7.75/10.97)**: minimum separation 3.77, final 3.77. No close pass. Safe to run.
4. **Design study (`analysis/design_round1_2026-11-23.py`)**: single-run precision for K_A(B) at fixed K = 8.3 and noise 0.05 per coordinate. At T = 2: start 5.85 gives 2.2%, start 6.5 gives 2.9%, start 6.9 gives 3.3%. At T = 4: 0.3% to 0.5% (but the constant-K assumption is then wrong by the H22 drift, so these figures are an upper bound on what the data can say). T = 6 from 6.0 and 4.5 is so sensitive that the pair passes close to contact, and I did not use it.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05)**: supported. P-0011.
- **H2 (species-independent noise at N = 1)**: supported (2.4% spread).
- **H3 (no clipping near a wall)**: supported.
- **H4 (no sample-timing offset)**: supported (about 0.005 time units).
- **H5 (stationarity over T = 100)**: mean supported; x-spread variation not reproduced.
- **H6 (P-0003 domain)**: separation 3 fails for P-0003 (r1/007, error 0.181). Separations 4 and 5 pass.
- **H7 (P-0006 shared-law factor at separation 9 for A-C)**: supported within 3% in one fit.
- **H8 (P-0008 coefficients flat over separations 3 to 5)**: supported for A-B at 4 and B-C at 3, 5. Not for A-A at 3 and 4.
- **H9 (P-0010 far-field G(r0), C-factor 0.9475)**: replicated at all three pairs and A-A at 6. C-C at 7 is 5.6% above. A-B has the step-like feature that H22 now describes as smooth decline. Check P-0010's range before relying on it.
- **H10 (A-A coefficient at separation 4 is 17.70)**: supported by the diagonal replicate.
- **H11 (close-range B-C)**: supported. P-0015.
- **H12 (A-B and B-B not constant-K over the first 0.3 time units at r = 1)**: open. Round-1 requests 001 to 005 (separation 2, T = 0.8) cover this at the P-0022 edge.
- **H13 (pairwise superposition)**: untested for more than two bodies.
- **H14 (far-field steepening)**: withdrawn in its old form (correction 1). Replaced by H22.
- **H17 (K_B(A)/K_A(B) = 1.41 at all separations)**: supported. Round-3 R values 1.37 to 1.52 (noisy at short windows); long windows 1.38 to 1.44.
- **H18 (m_A/m_B = 1.41 with momentum conservation)**: inference from H17, not tested directly.
- **H15 (P-0004-c2 magnitude)**: K_C(A) about -20.7 from three repeats, published -21.38. Flagged.
- **H16 (P-0014 A-A contact failure)**: integrator blows up after close approach at t about 1.2 for A-A at r0 = 3. Filed as P-0014 falsification.
- **H19 (step near r = 6 at rest, K 8.3 to 6.3)**: **not supported as stated** (round 3, 004 and 005 give 7.5 and 7.2). Replaced by H22.
- **H20 (window K depends only on current r, not start state, time or speed)**: open. Round-1 requests 007, 008 (moving starts at r 6.5) and 009 (vertical at-rest control) test it.
- **H21 (position and orientation invariance for the A-B law)**: not falsified at 3% (round 3, 006, 007 vs 003).
- **H22 (new)**: K_eff(r) at fixed P = 2.5 falls smoothly from about 9.2 (r 4) to about 6.0 (r 8.5); apparent exponent about 3. Falsified if the moving-start runs (007, 008) at r 6.5 agree with the at-rest value 7.5 for a smooth r-only curve, or if the two runs disagree at a level above their 3% precision (then H20 holds and the r-only curve is wrong).

## Round-1 requests (2026-11-23, research account, tracker only, 9 runs, est. 9.64 credits of 40)

Files: `out/requests/2026-11-23/r1/lab-vernier/001-009.json`.

| request | design | purpose | prediction |
|---|---|---|---|
| 001 | A-B, sep 2.0 horizontal, at rest, T = 0.8 | P-0022 domain edge | P-0022 end separation 0.45. K_B(A) read from the endpoint and fit. |
| 002 | same, vertical | orientation control of 001 | agrees with 001 within 3% on K_B(A) |
| 003 | same, diagonal | orientation control of 001 | agrees with 001 within 3% on K_B(A) |
| 004 | sep 1.95 horizontal, T = 0.8 | P-0022 lower domain edge | same law as 001 |
| 005 | sep 2.05 horizontal, T = 0.8 | P-0022 upper domain edge | same law as 001 |
| 006 | sep 7.0 at rest horizontal, T = 6 | **P-0021 check** | P-0021 predicts min r 3.77 and its K. Falsifies P-0021 at its own bar (residual > 0.021 RMSE/L). Other outcomes: K drifts (H22). |
| 007 | sep 6.5 outward relative speed 0.3, T = 2 | H20 state test | If H20 (r-only) holds, K matches r3 004 (7.5) within 3%. If the speed matters, K differs by more than 3%. |
| 008 | sep 6.5 inward relative speed 0.3, T = 2 | H20 state test | same as 007 |
| 009 | sep 6.5 at rest, vertical, T = 2 | H19 replicate, orientation | K = 7.5 within 3% of r3 004 |

Decision rules (written before results):
- **P-0022 (001 to 005):** K_B(A) from each run in [10.06, 11.12] (within 5% of 10.59) supports the paper. K_B(A) outside that band with the three orientations agreeing within 3% falsifies the K_B(A) constant near contact. Report it in the notebook either way. The review bar cannot use the result (see above), so any falsification is a note, not a scoreboard claim.
- **P-0021 (006):** residual RMSE/L of P-0021's model over the run. Above 0.021 falsifies its constant-K claim over T = 6 (3 times 0.007). Below 0.021 keeps it.
- **H20 (007, 008, 009):** falsified if |K(007) - 7.5| or |K(008) - 7.5| exceed 3% of 7.5 (0.23) at the same start, or K(009) differs from 004 by more than 3%.
- **H22:** a smooth r-only curve through the at-rest points is consistent with 009; a difference between 007 and 008 with the same r0 would show speed dependence, which weakens H22 as an r-only law.

## Reviews this round: none filed

- P-0012, P-0013, P-0017, P-0018, P-0019, P-0020 (other labs, short-run claims): zero-force nulls sit below 3 times predicted_error (earlier estimates: 0.0014 to 0.017 vs bars 0.024 to 0.03). Not filed.
- P-0022 (Icarus): null 0.0235 vs bar 0.024. Not filed (see above).
- P-0023 (mine) and P-0021 (mine): not reviewed by others yet.
- Review credits (15) lapse unused. I would rather spend them on a claim whose null exceeds its bar.

## Grant

- Round 2 vote: lab-keystone (local A-A exponent test). Keystone won tonight's grant. **That grant is for Keystone.** I have no grant credits.
- Round-1 proposal **filed today** (`out/grants/2026-11-23/proposals/lab-vernier.json`): "A-B pair at separation 2, at rest, to T = 0.8: K_B(A) to 1% at the P-0022 domain edge" (the endpoint slope makes this a few-percent test, see pitch). It is a 2-body pair-law test, not a multi-body one.

## Open problems: assessment

- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025)**: not reachable with this tracker (noise floor 0.005). Do not file.
- **close-AB (bounty 2), close-AC (bounty 2)**: need r_range starting at 1 or less. Blocked by H12. Round-1 requests 001 to 005 are at separation 2, not 1. A run at separation 1.0 would be the next step after H12 at 2 is settled.
- **crowd-8 (bounty 3)**: multi-body. Not attempted (H13 untested; the cross-pair species laws are not all known).
- **contested-P-0014, disputed-P-0003, -P-0006, -P-0007**: not addressed this round.

## Budgets, 2026-11-23

- **Research**: 40 allowed today. Planned round 1: 9.64 (001 to 009). Remaining after filing: about 30.4.
- **Review**: 15 allowed today. 0 used. None filed.
- **Grant**: none for this lab. Proposal filed for 2026-11-23.
- Ledger check (2026-11-22): research used 22.86 of 40 (round 3 at 8.64, estimated). Results of round 3 in the checkout show actual cost 1.08 per run, total 8.64. Consistent.

## Plan for next round (when 2026-11-23 r1 results arrive)

1. Read `results/2026-11-23/r1/lab-vernier/001-009`. Run `analysis/fit_r3_2026-11-22.py` pattern with the new dates (copy and change the run list and the window). Use `analysis/fit_tools.py` (copied into `out/labs/lab-vernier/analysis/`).
2. Apply decision rules in order: P-0021 (006) and P-0022 (001 to 005), then H20 (007 to 009), then H22.
3. If H20 holds (r-only) and 006 is consistent with P-0021: consider a narrow paper on the at-rest/moving K(r) curve **only if its zero-force null exceeds 3 times predicted_error** on the cited runs. If it fails, note it and skip.
4. If H20 fails (speed or state matters): write H23 (state-dependent K) and design a speed scan at fixed r.
5. If the 006 residual exceeds 0.021: P-0021 is falsified on its own domain. Publish a withdrawal or narrowed claim. Its evidence from 2026-11-21 is at r 6.9 to 7.1, so the narrowed domain is T <= 2.
6. Do not file a review unless the null exceeds the bar. Check the bar before every review file.

## Not read

`gate/`, `tools/`, `exam_papers.json`, predictor or score files. I did not read them and will not.
