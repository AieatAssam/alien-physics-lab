# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-21, round 3.
Analysis: `out/labs/lab-b/analysis/` (`pairfit_2026-11-21.py` is the chi2 coupling fitter, `score_papers_2026-11-21.py` scores my runs with the shipped predictors, judge-style).
Requests this round: `out/requests/2026-11-21/r3/lab-b/` (001-013).
Reviews filed this round: `out/reviews/P-0012/lab-b.json` (replicated), `out/reviews/P-0013/lab-b.json` (narrowed), `out/reviews/P-0015/lab-b.json` (replicated). P-0016 review deferred (see below).
Paper filed this round: `P-0017` (close-range B-B, K = 3.98) and `P-0018` (close-range C-C, K = 9.31). Paper numbers may be renumbered by the gate; refer to them by title.
Vote in round 2: lab-vernier (proposal not mine; I did not vote for myself).

## Corrections

- **Fit start point (round 2).** Fits that start the simulation from the tracker reading at t = 0 are wrong (the reading carries noise, sd 0.05 per coordinate). Rule for all fits: start from the request `setup`.
- **Window fit normalisation (round 2).** The first shape-scan printed chi2/n is mis-scaled. Use the K values only.
- **Out-of-domain run, 2026-11-20/r3/006.** The B-C pair at separation 6.0 landed at 5.999999; not citable for P-0010. Place pairs inside a claim's range with a margin, or at an exact edge only when the claim's range is an exact point and the request distance has been checked.
- **Round-1 pre-registrations failed at close range.** Predicted K_AA(1) = 24.3 / 18.0 / 73, measured 11.1 now. Neither linear-G nor constant-K holds below r = 3.
- **My 3% replicate bar was too strict (round 3).** I wrote "publish only if replicates agree within 3%". With per-run K errors of 2% (A-A, C-C) and 5% (B-B), the observed spreads are consistent with the fit errors. Publishing decision now uses sigma from the Delta-chi2 = 1 interval, not a fixed percentage.
- **Attractive pairs collapse at T >= 0.3 (round 3).** In the model with K near 4 to 11, the separation falls to 0.06 to 0.14 by T = 0.3 (A-A, A-B, C-C), so close-range attractive runs are only valid at T <= 0.15. Repulsive pairs (A-C, B-C) do not collapse at any T used here.

## Judge-metric caveat (important)

The judge's bar is 3 x predicted_error on RMSE/L. At T = 0.15 a run with K = 18 for A-A at r = 1 gives judge error 0.006. A 3% coefficient error is invisible to the judge at T = 0.15 and at T = 0.4 for most pairs. Coefficient claims must therefore be checked with chi2 (sd 0.05), and a replicated verdict says nothing about the coefficient. Longer T helps only where the pair does not collapse: P-0013's A-A at T = 0.4 gives sigma 0.04 on K (about 0.3%), which is enough to show a 3% error.

**Domain loophole (new).** The judge's domain check lists species and tests pair distances. A single particle has no pairs, so it passes any pair claim that lists its species. Lone-particle runs (2026-11-17/r1/lab-b/001 A, 2026-11-17/r2/lab-b/005 C) therefore count as in-domain for P-0016 and P-0015 and reproduce at the noise floor. They carry no pair information, so I do not cite them. Also, the predictors of P-0015 and P-0016 raise on B-B, C-C and A-A pairs, which the species list allows. Such runs are in-domain by rule but get no prediction, so they cannot falsify. Both papers should state the pair restriction in their domain.

## Season facts (measured)

- Season 1, species A, B, C. Chamber [0, 10]^2. k = 0.020 (cost = 1 + 0.02 N T; result costs match).
- Tracker noise sd 0.050 per coordinate; residual rms of best fits 0.049 to 0.051. Judge-style error at the noise floor is 0.0071.
- Census: no decay, appear or vanish events in any run to date.
- Chamber diagonal 14.14; largest in-chamber separation about 13.3.

## Coupling fits (constant K per ordered pair; a = K / r^2.5; positive = attraction)

Method: `pairfit_2026-11-21.py`, RK4 step 0.002, start from the request setup, chi2 with sd 0.05. sigma from delta chi2_total = 1.

| pair | r | T | runs (lab-b) | per-run K | pooled | note |
|---|---|---|---|---|---|---|
| A-A | 1.0 | 0.15 | r1/005, r1/008, r2/001, r2/002 | 11.00, 10.75, 11.28, 11.43 (sigma 0.18 each) | **11.11 +/- 0.09** | P-0012 claims 11.3 (2 sigma high) |
| C-C | 1.0 | 0.15 | r1/006, r2/011, r2/012 | 9.59, 9.05, 9.30 (sigma 0.19) | **9.31 +/- 0.13** | P-0018 |
| B-B | 1.0 | 0.15 | r1/007, r2/009, r2/010 | 4.13, 3.86, 3.97 (sigma 0.21) | **3.98 +/- 0.12** | P-0017 |
| A-B | 1.0 | 0.15 | r2/013, r2/014 | K_AB 5.64, 5.39; K_BA 7.77, 7.35 | K_AB ~5.5, K_BA ~7.6, spread 3 to 6% | not yet published; third and fourth runs requested (r3/010, 011) |
| A-C | 1.0 | 0.15 | r2/015, r2/016 | K_AC -5.39, -6.03; K_CA -13.52, -13.33 | not resolved at T = 0.15 | P-0016 claims -6.25 / -14.78; K_CA low by about 3 sigma (rough) |
| B-C | 1.0 | 0.6 | r2/006, 007, 008 | K_BC -4.28, -4.26, -4.27 (sigma 0.03); K_CB -7.20, -7.23, -7.17 (sigma 0.03) | K_BC -4.27, K_CB -7.20 | P-0015 claims -4.32 / -7.31: K_CB 3 sigma high (1.5%) |
| A-A | 1.5 | 0.4 | r2/003 | 13.18 (sigma 0.04) | 13.18 | P-0013 implies 13.55 (2.8%, 8 sigma high) |
| A-C | 1.5 | 0.4 | r2/004 | K_AC -7.23 (sigma 0.14), K_CA -16.92 (sigma 0.15) | | P-0013 implies -7.11 / -17.23 (within 2 sigma) |
| C-C | 1.5 | 0.4 | r2/005 | 10.85 (sigma 0.06) | 10.85 | P-0013 implies 10.80 (consistent) |
| A-C | 1.0 | T = 3 | 2026-11-17/r3/lab-b/004 | K_AC -6.93, K_CA -16.48, chi2/n 1.42 | | model fails at T = 3 (sep grows); constant-K not adequate there |

Earlier same-species values (round 2, window fits, less precise): A-A 14.15 at 1.5, 14.7 to 15.4 at 2.0, 18.0 at 3.0 and 4.0 (plateau); C-C 11.28 at 1.5, 13.2 at 3 and 4; B-B 4.84 at 1.5, 6.37 at 3.0, 6.48 at 4.0; A-A 16.6 at 6.0, 11.75 at 9.0, 7.38 at 12.0, 5.95 at 13.3; C-C 4.90 at 12.0, 3.90 at 13.3.

**Shape ratios K(r) / K(plateau), plateau = value at r = 3 to 5:**

- A-A (plateau 18.0): r = 1.0: 0.62; 1.5: 0.73 (13.18/18.0); 2.0: 0.83; 3 to 5: 1.0; 6: 0.92; 9: 0.65; 12: 0.41; 13.3: 0.33.
- C-C (plateau 13.2): 1.0: 0.71 (9.31/13.2); 1.5: 0.82; 3 to 4: 1.0; 12: 0.37; 13.3: 0.30.
- B-B (plateau 6.4): 1.0: 0.62; 1.5: 0.76; 2.0: 0.86.

**Species-universal shape: still rejected at r = 1.** One universal g(r) would give K_CC(1)/K_AA(1) = 13.2/18.0 = 0.73. Measured 9.31/11.11 = 0.84 +/- 0.02. Rejected at about 5 sigma. Note the plateau-based K_AA(3..5)=18.0 and K_CC=13.2 come from round-2 window fits, so this rejection has the window-fit uncertainty (a few percent); the excess is larger than that.

## Scores with shipped predictors (reviews)

- **P-0012 (lab-a, A-A at 1.0): replicated, filed.** Four in-domain runs (r1/005, r1/008, r2/001, r2/002), judge error 0.0069 to 0.0071 against bar 0.024. Coefficient: 11.11 +/- 0.09 vs 11.3, about 2 sigma high. The coefficient caveat is in the comment.
- **P-0013 (lab-c, A/A, A/C, C/C at 1.5, T <= 0.4): narrowed, filed.** Three in-domain runs (r2/003, 004, 005), judge error 0.0070 to 0.0071 against bar 0.030. A-A scale 0.753 gives K 13.55, but the T = 0.4 fit gives 13.18 +/- 0.04, 2.8% high (8 sigma). C-C and A-C agree within 2 sigma. Verdict narrowed because the A-A scale fails.
- **P-0015 (lab-vernier, B-C at 1.0, T <= 0.6): replicated, filed.** Three in-domain runs at T = 0.6 (r2/006, 007, 008), judge error 0.0071 to 0.0071 against bar 0.015. K_BC -4.27 (claim -4.32, 1.3 sigma); K_CB -7.20 (claim -7.31, 3 sigma, 1.5%). Comment states the domain issue.
- **P-0014 (lab-keystone, A/C at 2.5 to 3.5): replicated, filed in round 2.** Unchanged.
- **P-0016 (lab-vernier, A-C at 1.0, T <= 0.6): review DEFERRED.** Only two in-domain runs at 1.0 pass the bar (r2/015 0.00692, r2/016 0.00716; judge bar 0.018). Replicated needs three, so I cannot file it yet. A third run in-domain at 1.0 (2026-11-17/r3/lab-b/004, T = 3) fails the bar at 0.0278, so the claim is valid at short T but not at T = 3. Round-3 requests r3/001 to 003 are three A-C runs at T = 0.6 (the claim's limit), in three orientations. File the review next session, once those results are in. Plan: replicated if all three are under 0.018 and K agrees; narrowed (T <= 0.15 or a shorter limit) if they fail. Also note the domain issue (A-A and C-C pairs listed in the species).

## Papers (this round)

- **P-0017, close-range B-B pair at separation 1.0, K = 3.98, T <= 0.15.** Evidence r1/007, r2/009, r2/010. Predictor covers only B-B. Own-run judge errors 0.0070 to 0.0072 (bar 0.024). Targets the open bounty close-BB.
- **P-0018, close-range C-C pair at separation 1.0, K = 9.31, T <= 0.15.** Evidence r1/006, r2/011, r2/012. Same structure. Targets close-CC.
- **Not published: close-AB** (K_AB and K_BA differ by 3 to 6% between replicates; the replicates are not yet enough). Two more runs requested (r3/010, 011); publish next round if the pooled coefficients hold.
- **Not published: close-AC.** P-0016 (Vernier) covers A-C at 1.0 and its constants are in doubt. My own A-C coefficients at 1.0 are -5.7 and -13.4 (pooled, T = 0.15), which disagrees with P-0016's -6.25 / -14.78. I will publish an A-C claim only after the T = 0.6 runs (r3/001-003) resolve which is right.
- **Not published: crowd-8.** No validated pairwise shape at the separations an 8-body run needs (3 to 6 apart). Needs the shape map first.

## Budget (2026-11-21)

- Research: 40 allowance, 17.72 used before round 3 (round-1 9.67, round-2 8.05). Round-3 requests 005-013 cost 10.69. Leftover about 11.6, not spent (no test on my list needs it).
- Review: 15 allowance, 8.14 used in round 2. Round-3 requests 001-004 (cites P-0016 x3, P-0013 x1) cost 4.09. Leftover about 2.8.

## Round-3 requests (out/requests/2026-11-21/r3/lab-b/)

| id | account | cites | setup | T | purpose |
|---|---|---|---|---|---|
| 001 | review | P-0016 | A-C at 1.0, horizontal | 0.6 | test K_AC, K_CA at the claim's stated limit |
| 002 | review | P-0016 | A-C at 1.0, vertical | 0.6 | orientation check |
| 003 | review | P-0016 | A-C at 1.0, 45 degrees | 0.6 | third orientation |
| 004 | review | P-0013 | A-A at 1.5, vertical | 0.4 | replicate of the A-A scale check (S_AA) |
| 005 | research | none | A-A at 7.5, horizontal | 6 | shape map 6 to 9 |
| 006 | research | none | A-A at 10.5, diagonal | 8 | far range |
| 007 | research | none | C-C at 7.5 | 6 | paired with 005 for the A-A / C-C ratio |
| 008 | research | none | C-C at 10.5 | 8 | paired with 006 |
| 009 | research | none | B-B at 10.5 | 10 | completes the far-range ratio set |
| 010 | research | none | A-B at 1.0, vertical | 0.15 | third A-B run for close-AB |
| 011 | research | none | A-B at 1.0, 45 degrees | 0.15 | fourth A-B run |
| 012 | research | none | A-C at 1.0, horizontal | 2.0 | repulsive shape beyond T = 0.6 |
| 013 | research | none | B-C at 1.0, horizontal | 2.0 | the same for B-C |

Far-range runs (005 to 009) use separation 7.5 horizontal or 10.5 diagonal, with the end points at (1.25, 1.25) and (8.75, 8.598) so the pair stays in the chamber.

## Hypotheses

- **H9 (close approach): supported.** K_s(1) is 0.6 to 0.7 of K_s(3..5) for A-A and B-B, about 0.7 for C-C. Falsifier not yet hit.
- **H9b (species-dependent close shape): supported.** C-C/A-A at 1.0 = 0.84 vs 0.73 under one universal shape (about 5 sigma).
- **H12 (distance-law shape):** plateau at r = 3 to 5, linear fall from about 6 to zero near 17 to 18 for A-A. Round-3 runs 005 to 009 test it at 7.5, 10.5, 13.3 (already measured). Falsifier: any A-A or C-C coupling at r = 7.5 to 10.5 more than 8% off the line.
- **H14 (P-0013 A-A scale): supported.** The A-A coupling at 1.5 is 13.18 +/- 0.04, not 13.55. Replicate r3/004 next session.
- **H15 (P-0016 coupling): open.** The 1.0-separation A-C coupling from my runs disagrees with P-0016 at roughly 2 to 3 sigma on K_CA. The T = 0.6 runs (r3/001 to 003) decide it.
- **H13 (shared factor across pairs): weakened further.** Shared shape across species is rejected at r = 1.
- **H10 (rank-one ratio A-B vs A-C at 2 and 3): open.**
- **H11 (three-body additivity): open.** The N = 3 run (r3/005 from the round-1/2 series) sits at about 2 sigma. Crowd tests need the shape map first.

## Plan for next session

1. Read `results/2026-11-21/r3/lab-b/001-013` once the sim commits them. Fit the T = 0.6 A-C runs (001-003) with `pairfit_2026-11-21.py` and score them with `score_papers_2026-11-21.py` against P-0016. File the P-0016 review: replicated if three in-domain runs are under 0.018 and the fitted K agrees; otherwise narrowed. Cite only A-C pairs at 1.0.
2. Check the A-A replicate (r3/004) for P-0013. If it confirms 13.2 +/- 0.05, the narrowed verdict stands.
3. Publish close-AB (P-0019 or next free number) only if the pooled K_AB, K_BA from r2/013, 014 and r3/010, 011 hold within their sigma. Domain: species [A, B], r_range [0.999, 1.001], max_particles 2. Evidence: the four runs.
4. Publish close-AC after the T = 0.6 result. If my K_AC/K_CA hold, the claim contradicts P-0016 on the coupling; publish it with its own sigma and cite the T = 0.6 runs.
5. Fit the far-range runs (005 to 009): A-A and C-C K at 7.5 and 10.5, and the ratio C-C/A-A at each. Test H12.
6. Repulsive long runs (012, 013): compare the 1/r^2.5 model against the separation as it grows from 1 to about 5. If the model fails by T = 2, say so and bound P-0015 and P-0016 to T <= 0.6 in my reviews.
7. Do not publish a species-universal shape (rejected at r = 1 in the round-2 data).
8. Do not cite lone-particle runs or runs whose predictor raises as evidence for any pair claim.
