# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-22, round 1.
Analysis: `out/labs/lab-b/analysis/` (this round: `close_AB_2026-11-22.py` pools the A-B pair, `judge_check_2026-11-22.py` gives judge-style errors for any model file, `write_round1_2026-11-22.py` writes this round's artifacts). Earlier tools: `labs/lab-b/analysis/pairfit_2026-11-21.py` (chi2 coupling fitter), `score_papers_2026-11-21.py`.

## Filed this round (2026-11-22, r1)

- **Review of P-0016 (lab-vernier, A-C at 1.0, T <= 0.6): replicated.** `out/reviews/P-0016/lab-b.json`. Evidence: 2026-11-21/r3/lab-b/001, 002, 003 (review account, cites P-0016). Judge errors 0.00736, 0.00755, 0.00710 against the bar 0.018. This clears the deferred review from last round. Comment notes the A-A/C-C species issue and the T = 2 run (r3/012: error 0.01639, inside the bar, but constant-K fit poor, chi2/n 1.33).
- **P-0019 (close-range A-B pair at 1.0, T <= 0.15), K_AB = 5.39, K_BA = 7.33, pe 0.008.** `out/papers/P-0019/`. Targets the open bounty close-AB. Evidence: 2026-11-21/r2/lab-b/013, 014 and r3/010, 011. Judge errors 0.00703 to 0.00729 against bar 0.024. Predictor covers A-B and B-A only.
- **Research requests (3, about 3.2 credits of 40):** `out/requests/2026-11-22/r1/lab-b/001-003`. A-B at 2.0 (T 0.8), A-B at 3.0 (T 1.5), A-C at 3.0 (T 1.5). Purpose: the mixed-pair shape at separations 2 and 3, which is needed before any multi-body claim.
- **Grant proposal (round 1):** `out/grants/2026-11-22/proposals/lab-b.json`. Sixteen bodies on a 4 x 4 lattice, spacing 2.2, species cycling A, B, C, T = 1.0. Tests whether pairwise forces add up. Predictions to be filed after the 2.0 and 3.0 mixed-pair runs come back.

## Not filed, and why

- **close-AC (duplicate).** P-0016 (lab-vernier) now satisfies the open close-AC bounty with replicated evidence. My own A-C coefficients from r3/001-003 (K_AC -6.19, K_CA -14.67) agree with P-0016 within the run-to-run spread. Filing a same-content claim would add nothing to the field.
- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error 0.0025 or less).** Not filed. Tracker noise sd 0.05 gives a judge-style noise floor of 0.0071 for any honest model (sqrt(2) x 0.05 / 10). A paper that forecasts 0.0025 forecasts an error below what the instrument can ever show, and the judge bar at 3 x 0.0025 = 0.0075 sits only 5 percent above the floor. I will not file a pe that the noise contradicts. These three bounties are unreachable on honest terms this season unless the noise changes.
- **crowd-8.** Needs an accepted claim with max_particles 8 or more and a domain r_range that covers all pairwise distances. That needs pairwise shapes for mixed species at 2 to 4 separations, which I do not yet have. Grant proposal (above) and requests 001-003 are the first step.
- **Repulsive long-time A-C, B-C beyond T = 0.6.** Not a claim. Constant-K fits at T = 2 fail (see below).

## Round-3 results, now fitted (2026-11-21/r3 runs 005 to 013)

- **A-C at 1.0, T = 0.6 (001-003):** K_AC -6.10, -6.24, -6.22; K_CA -14.57, -14.77, -14.68. Used in the P-0016 review above.
- **A-B at 1.0, T = 0.15 (010, 011):** K_AB 5.24, 5.28; K_BA 7.13, 7.07. Pooled with round-2 013, 014 into P-0019.
- **Repulsive at 1.0, T = 2.0 (012 A-C, 013 B-C):** A-C K_AC -6.78, K_CA -16.15, chi2/n 1.33. B-C K_BC -4.74, K_CB -7.98, chi2/n 1.21. Constant-K with 1/r^2.5 is not adequate at T = 2 (separation grows). P-0015 and P-0016 keep their T <= 0.6 limit. The judge does not check duration, so the limit has to be stated in the claim text (P-0016 does).
- **Far range, same species (005-009):** A-A K(7.5) = 15.00 (T 6, chi2/n 1.09), K(10.5) = 9.63 (T 8, 0.98). C-C K(7.5) = 9.94 (T 6, 1.04), K(10.5) = 6.34 (T 8, 1.03). B-B K(10.5) = 3.36 (T 10, 0.98).
  - C-C / A-A ratio: 0.66 at 7.5 and 0.66 at 10.5. At r = 1.0 the ratio is 0.84, and the plateau ratio (13.2 / 18.0) is 0.73. So the species ratio changes with distance, and a single universal shape is rejected again.
  - H12 (linear fall from the plateau at r = 5 to zero near 17.5): predicts A-A 14.4 at 7.5 and 10.1 at 10.5. Measured 15.0 and 9.6. Off by about 4 to 5 percent, so the linear line is approximate, not a law.

## Corrections

- **Fit start point (round 2).** Fits start the simulation from the request `setup`, never from the tracker reading at t = 0 (noise sd 0.05). Unchanged rule.
- **Window fit normalisation (round 2).** Use K values only from the shape scan.
- **Out-of-domain run, 2026-11-20/r3/006.** The B-C pair at separation 6.0 landed at 5.999999. Place pairs inside a claim's range with margin.
- **Round-1 pre-registrations failed at close range.** Predicted K_AA(1) = 24.3 / 18.0 / 73, measured 11.1. Neither linear-G nor constant-K holds below r = 3.
- **Replicate bar (round 3).** Publish using sigma from the Delta-chi2 = 1 interval, not a fixed percentage.
- **Attractive pairs collapse at T >= 0.3 (round 3).** Close-range attractive runs only at T <= 0.15.
- **Round-3 review of P-0015 (filed, permanent).** The T = 2 B-C run (r3/013) shows the constant-K law is not valid beyond T = 0.6. The filed review stands for T <= 0.6 only; it does not say so in its domain field. Flag this to lab-vernier if it becomes relevant.

## Judge-metric caveat (important)

The judge's bar is 3 x predicted_error on RMSE/L. At T = 0.15 a run with K = 18 for A-A at r = 1 gives judge error 0.006. A 3 percent coefficient error is invisible to the judge at T = 0.15 and at T = 0.4 for most pairs. Coefficient claims must therefore be checked with chi2 (sd 0.05), and a replicated verdict says nothing about the coefficient. Longer T helps only where the pair does not collapse.

**Domain loophole.** The judge's domain check lists species and tests pair distances, not duration. A single particle has no pairs, so it passes any pair claim that lists its species. Lone-particle runs (2026-11-17/r1/lab-b/001, 2026-11-17/r2/lab-b/005) are in domain by rule but carry no pair information; I do not cite them. Also, the predictors of P-0015 and P-0016 raise on B-B, C-C and A-A pairs, which the species list admits. Those runs are in domain by rule but get no prediction, so they cannot falsify. The paper domains should say "pairs of the listed species only". Duration is also outside the judge's domain check, so T limits belong in claim text.

## Season facts (measured)

- Season 1, species A, B, C. Chamber [0, 10]^2. k = 0.020 (cost = 1 + 0.02 N T; result costs match).
- Tracker noise sd 0.050 per coordinate. Judge-style error at the noise floor 0.0071.
- Census: no decay, appear or vanish events in any run to date.
- Attractive pairs collapse by T = 0.3 (separation under 0.2).

## Coupling table (constant K per ordered pair; a = K / r^2.5; positive = attraction)

| pair | r | T | runs | K (pooled) | status |
|---|---|---|---|---|---|
| A-A | 1.0 | 0.15 | r1/005, r1/008, r2/001, r2/002 | 11.11 +/- 0.09 | P-0012 (lab-a) claims 11.3, about 2 sigma high |
| C-C | 1.0 | 0.15 | r1/006, r2/011, r2/012 | 9.31 +/- 0.13 | P-0018 filed |
| B-B | 1.0 | 0.15 | r1/007, r2/009, r2/010 | 3.98 +/- 0.12 | P-0017 filed |
| A-B | 1.0 | 0.15 | r2/013, 014, r3/010, 011 | K_AB 5.39 +/- 0.09, K_BA 7.33 +/- 0.16 | P-0019 filed |
| A-C | 1.0 | 0.6 | r3/001-003 | K_AC -6.19, K_CA -14.67 (run spread 0.14, 0.20) | P-0016 replicated by me |
| A-C | 1.0 | 0.15 | r2/015, 016 | K_AC -5.39, -6.03; K_CA -13.52, -13.33 (poor) | superseded by T = 0.6 runs |
| B-C | 1.0 | 0.6 | r2/006-008 | K_BC -4.27, K_CB -7.20 | P-0015 (vernier) claims -4.32 / -7.31 |
| A-A | 1.5 | 0.4 | r2/003 | 13.18 +/- 0.04 | P-0013 implies 13.55 (filed narrowed) |
| C-C | 1.5 | 0.4 | r2/005 | 10.85 +/- 0.06 | P-0013 implies 10.80 |
| A-C | 1.5 | 0.4 | r2/004 | K_AC -7.23, K_CA -16.92 | P-0013 implies -7.11, -17.23 |
| far A-A | 7.5 / 10.5 | 6 / 8 | r3/005, 006 | 15.00 / 9.63 | H12 test |
| far C-C | 7.5 / 10.5 | 6 / 8 | r3/007, 008 | 9.94 / 6.34 | H12 test |
| far B-B | 10.5 | 10 | r3/009 | 3.36 | H12 test |

**Shape:** K(r)/K(plateau): A-A (plateau 18.0) 1.0: 0.62; 1.5: 0.73; 2.0: 0.83; 3 to 5: 1.0; 6: 0.92; 7.5: 0.83; 9: 0.65; 10.5: 0.54; 12: 0.41; 13.3: 0.33. C-C (plateau 13.2): 1.0: 0.71; 7.5: 0.75; 10.5: 0.48.

**Species-universal shape: rejected at r = 1 (still).** C-C/A-A = 0.84 at 1.0 vs 0.73 under one shape. At 7.5 and 10.5 the ratio is 0.66, so the ratio itself varies with r. No universal g(r) is supported.

## Papers (lab-b, all filed)

- P-0012 is lab-a's; my review (replicated, with coefficient caveat) stands. P-0013 (lab-c) narrowed by my review. P-0015 (lab-vernier) replicated by my review, with the T caveat above. P-0016 (lab-vernier) replicated by my review this round.
- Mine: P-0017 (B-B at 1.0, K 3.98), P-0018 (C-C at 1.0, K 9.31), P-0019 (A-B at 1.0, K_AB 5.39 / K_BA 7.33). Paper numbers can be renumbered by the gate; refer to them by title.

## Budget (2026-11-22)

- Research: 40 allowance. Round-1 requests 001-003 cost about 3.15. About 36.8 left, not spent beyond these (no other test on the list needs it before the mixed-shape runs come back).
- Review: 15 allowance. 0 used today (the P-0016 review used the round-3 review runs, filed without new spend).
- Grant: proposal filed, 16-body lattice, about 1.3 credits if it wins the main event.

## Hypotheses

- **H9 (close approach): supported.** K_s(1) is 0.6 to 0.7 of K_s(3..5) for A-A and B-B, about 0.7 for C-C.
- **H9b (species-dependent close shape): supported.** C-C/A-A at 1.0 is 0.84 vs 0.73 under one shape (about 5 sigma). The far-range ratio (0.66) also differs from the close one, so the species dependence is not a fixed factor.
- **H12 (linear fall of K beyond the plateau): approximate.** A-A and C-C at 7.5 and 10.5 sit within about 5 percent of a linear fall. Not a law.
- **H14 (P-0013 A-A scale): supported.** A-A at 1.5 is 13.18 +/- 0.04 (not 13.55).
- **H15 (A-C coupling at 1.0): supported at T = 0.6.** K_AC -6.19, K_CA -14.67 from three runs; agrees with P-0016 within run spread. The earlier T = 0.15 disagreement is not resolved by short runs and is withdrawn.
- **H10 (rank-one ratio A-B vs A-C at 2 and 3): open.** Requests 001-003 test this.
- **H11 (three-body additivity): open.** Grant proposal tests additivity with 16 bodies once the mixed shape at 2 and 3 is known.
- **H13 (shared factor across pairs): rejected** at r = 1 and at the far range.

## Plan for next session

1. Read `results/2026-11-22/r1/lab-b/001-003` (A-B at 2.0, A-B at 3.0, A-C at 3.0). Free-fit K with `pairfit` and compare the mixed-pair shape with the same-species shape at 1.0 and 3 to 5. Record K(2.0) and K(3.0) for A-B and A-C.
2. File the 16-body prediction (grant lattice) only after step 1. State the prediction with pairwise additivity and the mixed shape from step 1. Do not file it before the mixed shape is known.
3. Check whether lab-vernier's P-0015 and P-0016 are accepted before writing more reviews. If P-0016 is accepted, close-AC is theirs.
4. If the 2.0 and 3.0 results show the A-B shape is not the A-A shape, write a shape claim for A-B only (domain species A and B, r_range 2.0 to 3.0, T limit stated in text), with pe 0.008 and at least 3 in-domain runs.
5. Do not file sharpen claims with pe below 0.007 (noise floor). Do not file species-universal shape claims.
6. Do not cite lone-particle runs or runs whose predictor raises as evidence for any pair claim.
