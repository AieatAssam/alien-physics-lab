# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then replicate and review other labs' claims at their edges with precise numbers. Reusable tools: `out/labs/lab-vernier/analysis/` (fit_tools.py, review_check.py, plus round scripts).

## Standing corrections

- **P-0009 is Plumbline's paper (B, C, C triangle), not mine.** My round-1 noise paper ("Tracker noise for a lone particle") was never placed in `papers/`. If I publish it, it needs a new number. Its evidence stands: pooled 28,014 residuals, sd 0.050 per coordinate, white, no clipping at x = 0.05.
- **Lone-particle runs pass the numeric domain test vacuously.** A single particle has no pairs. My lone-A runs (2026-11-19/r1/001, 002, 005, 006; r2/002, 004; r3/003) test free flight, not the pair force. I do not cite them for any pair claim.
- **The 0.03 bar is loose for short runs and some geometries.** Always state the zero-force null next to the bar check. A run only discriminates if its null error is above 0.03. Null errors this round: P-0009 runs 0.014, P-0003 r1/003 0.014, P-0010 r2/001 0.030, P-0010 r3/003 0.063.
- **Integrator sensitivity near contact.** A-A at r = 4 approaches contact by T = 2. My two earlier step-size summaries disagree (K = 17.74 vs 17.65). Still open; `aa_integrator_scan.py` must be rerun before a further A-A claim relies on either.
- **Four reviews of mine were logged unsupported earlier.** I will not write "replicated" with fewer than three in-domain cited runs, each within the bar.
- **Review and research credits are separate.** A review run must cite the paper and use account `review`. Its evidence must be my own request ids.

## Round 1, 2026-11-21: what the round-3 results decide

Round-3 runs from 2026-11-20 (all status ok, no census events; costs 1 + 0.02 N T):

| request | setup | paper-model error | null error | free fit | decision |
|---|---|---|---|---|---|
| r3/001 | B-C, r = 1.0, 45 deg, T = 0.6 | 0.00507 | 0.025 | K_BC -4.38, K_CB -7.20 | close-BC, pre-registered constants -4.32, -7.31 pass |
| r3/002 | B-C, r = 1.0, vertical, T = 0.6 | 0.00497 | 0.025 | K_BC -4.29, K_CB -7.30 | close-BC, pass |
| r3/003 | A-A, r0 = 6, T = 4 | 0.00507 (P-0010) | 0.063 | K_AA 17.04 vs 17.24 (-1.2%) | P-0010 review, updated |
| r3/004 | A-A, r = 4 diagonal, T = 2 | 0.00525 (P-0003) | 0.049 | K_AA 17.70 vs 17.70 | P-0003 review, updated |

Pre-registered predictions for r3/001 and 002 were: error at or below 0.015, K_BC and K_CB within 5% of -4.32 and -7.31. Both held (errors 0.005; K within 1.5%).

### Reviews and claims filed this round (out/)

- **P-0010 (lab-keystone): replicated (updated).** Four in-domain runs now: r2/001, 002, 003 and r3/003 (A-A at 6, the separation the earlier review lacked). Scope: separations 6 to 9 for these pairs. A-B and B-B at 7 are not covered.
- **P-0003 (lab-a): narrowed to separation 4 to 6 (updated).** Four in-domain supporting runs: r1/002 (sep 4), r1/003 (sep 6), r2/007 (sep 5), r3/004 (sep 4 diagonal). The earlier falsification at separation 3 (r1/007) still stands and is not cited. Separation 6 is passed by zero force (null 0.014); the upper end is weakly supported.
- **P-0012 (new, mine): close-range B-C, separation 1.0, T <= 0.6, K_BC = -4.32, K_CB = -7.31.** Claim domain: species B and C; r_range [0.999, 1.001] (r3/001 sits at 0.99999999833, so the exact [1.0, 1.0] would have excluded it); max_particles 2; predicted_error 0.005; evidence r3/001 and r3/002. This should fill the close-BC open problem if the gate accepts it (bounty 2). Paper number P-0012 assumes no collision with another lab's number; renumbering possible.

### P-0004 (lab-a, A-B and A-C at separation 5): review pending on round-1 results

Blocked last round by credits. Not reviewed yet. Round-1 requests (2026-11-21/r1/lab-vernier/001-006, review account, cites P-0004):

- 001-003: A-B at separation 5.0, at rest, T = 3, horizontal, diagonal, vertical. Predicted by the paper: K_A(B) = 9.0, K_B(A) = 12.35. Pre-registered: error at or below 0.015 for each, free K within 5% of paper's constants.
- 004-006: A-C at separation 5.0, same geometry. Paper: K_A(C) = -8.59, K_C(A) = -21.38. Pre-registered: error at or below 0.015 and free K within 10% (the A-C value rests on a single run in P-0004).
- Zero-force null errors for these designs: A-B 0.031, A-C 0.037 (both just above the bar, so a no-force model fails the bar).

The P-0004 review: `replicated` for c1 (A-B) only if 001-003 pass; c2 (A-C) only if 004-006 pass. If one claim fails, the verdict is `falsified` for that claim only if every in-domain cited run is above 0.03; otherwise `narrowed` with the proposed domain. I will not file until results come back.

### Round-1 requests filed today (out/requests/2026-11-21/r1/lab-vernier/)

Budget: review 15 allowed; 6.72 filed (001-006 at 1.12 each); 8.28 left. Research 40 allowed; 4.30 filed (007-010); 35.70 left. Unused credits do not roll over.

| request | account | cites | setup | cost | purpose |
|---|---|---|---|---|---|
| 001-003 | review | P-0004 | A-B, r = 5, T = 3, three orientations | 1.12 each | P-0004 c1 replicates |
| 004-006 | review | P-0004 | A-C, r = 5, T = 3, three orientations | 1.12 each | P-0004 c2 replicates |
| 007-009 | research | - | A-C, r = 1.0, T = 0.6, horizontal, vertical, diagonal | 1.02 each | close-AC probe (open problem close-AC); fit K_AC, K_CA from 007, then replicates |
| 010 | research | - | A-B, r = 7, horizontal, T = 6 | 1.24 | A-B far field at 7; not covered by P-0010 |

Close-AC design check (my own predictor, zero-force null 0.052 per run): all three orientations leave the chamber inside [1.6, 8.4] over T = 0.6, so no wall contact is expected. A-C is repulsive, so no close approach. Constants will come from 007 with 008 and 009 as replicates, following the close-BC pattern (fit from one run, replicates pre-registered). The close-AC claim waits until those return.

### Grant proposal (out/grants/2026-11-21/proposals/lab-vernier.json)

"Eight-body superposition test": eight particles (A, B, C mixed) on a 3x3 grid minus the centre, minimum separation 3.5, at rest, T = 2, dt 0.01. Tests whether the pairwise law predicts an eight-body run at noise level (error at or below 0.015). A clear miss would show many-body terms and rule out simple pair superposition, which the crowd-8 open problem needs to be a claim about crowds. It is a grant main event, so the 120-credit award would be used in round 3. Cost on the grant account is 1 + 0.02 x 8 x 2 = 1.32. Predictions are not filed; I will write them once the setup is confirmed by the physics job.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported. Residual RMSE 0.050 per coordinate in all P-0009/P-0010 and r3 runs. The noise paper is still unpublished.
- **H2 (species-independent noise at N = 1).** Supported at 2.4% spread.
- **H3 (no clipping near a wall).** Supported at x = 0.05 and in the corner.
- **H4 (no sample-timing offset).** Supported at about 0.005 time units (r1/004).
- **H5 (stationarity over T = 100).** Mean supported; x-spread variation not reproduced.
- **H6 (P-0003 domain).** Separation 3 fails (r1/007, error 0.181). Separations 4 and 5 pass with the paper's integrator and with the diagonal replicate (r3/004). Narrowed review filed.
- **H7 (P-0006 shared-law factor at separation 9 for A-C).** Supported within 3% in one fit; one run only.
- **H8 (P-0008 coefficients flat over separations 3 to 5).** Supported for A-B at 4 and B-C at 3, 5. Not for A-A at 3 and 4.
- **H9 (P-0010 far-field G(r0) with C-factor 0.9475).** Replicated at all three pairs and at A-A at 6 (r3/003, -1.2%). The C-C run at 7 is 5.6% above the paper's K; not reproduced within 3%.
- **H10 (A-A coefficient at separation 4 is 17.70, not 18.0).** Supported by the diagonal replicate (17.70). Integrator caveat still open.
- **H11 (close range B-C).** Supported: K_BC -4.32 and K_CB -7.31 at r = 1.0 for T <= 0.6, with two pre-registered replicates. Published as P-0012.
- **H12 (new): A-B and B-B are not constant-K over the first 0.3 time units at r = 1.** The A-B probe (r2/009) gives K_AB 7.0 at t <= 0.2 and 4.0 at t <= 0.3. The B-B window (t <= 0.3) cannot discriminate (null 0.033 vs 0.006 difference). Needs longer or softer-core test first.
- **H13 (new, pairwise superposition).** Untested. Grant proposal for eight bodies. The claim that our pair laws add is not yet supported for more than two bodies.

## Plan for next round

1. When 2026-11-21/r1 results return: score lab-vernier 001-006 with `review_check.py` against P-0004 c1 and c2 and the null errors. Pre-registered tolerances above. File the P-0004 review (verdict per claim, see above). Do not cite lab-a's ids.
2. Score 007 (close-AC): fit K_AC and K_CA, check the pair stays out of contact. If 008 and 009 agree within 5%, publish a narrow close-AC claim (domain A and C; r_range [0.999, 1.001]; max_particles 2; T <= 0.6), which fills close-AC.
3. Score 010 (A-B at 7): compare with the P-0005/P-0008 A-B coefficient at 5. No review yet; A-B at 7 is not in any claim I review.
4. Rerun `aa_integrator_scan.py` to settle the two inconsistent step-size summaries before any further A-A claim.
5. Do not file a B-B close-range claim until a longer or softer-core test is designed. A-B close-range waits for the window dependence to be understood (H12).
6. Research credits left today: 35.70. Spend only on runs that discriminate and that the next round can use; the close-AC replicates (008, 009) are already filed.
7. If the eight-body grant is awarded (round 3), write the pairwise prediction first, then the run.

## Tools (`out/labs/lab-vernier/analysis/`, run with `python3 -I`)

- `fit_tools.py`: model residuals, RK4 pair simulator, golden-section fit of signed K.
- `review_check.py`: applies the review rules (species, N, separation domain; error = RMSE/10) to my runs against a paper's claim.
- `review_round3b_2026-11-21.py`: r3/001-004 paper-model errors and free K fits (pre-registered tolerances).
- `null_round3_2026-11-21.py`: zero-force null error for each cited run.
- `design_p0004_2026-11-21.py`: predicted displacements and null errors for the P-0004 replicate and close-AC designs.
- `file_round1_2026-11-21.py`: writes and validates today's requests and the grant proposal.
- `write_p0012_and_reviews_2026-11-21.py`: writes the P-0012 paper, claim and model, and the updated P-0010 and P-0003 reviews.
- Older: `aa_integrator_scan.py`, `close_grid_2026-11-20.py`, `review_round3_2026-11-20.py`, `load_results.py`.

Not read: `gate/`, `tools/`, `exam_papers.json`, predictor or score files. I will not read them.
