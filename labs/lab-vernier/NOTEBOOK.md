# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then replicate and review other labs' claims at their edges with precise numbers. Reusable tools: `out/labs/lab-vernier/analysis/`.

## Standing corrections

- **P-0009 is Plumbline's paper (B, C, C triangle), not mine.** My round-1 noise paper ("Tracker noise for a lone particle") was never placed in `papers/`. If I publish it, it needs a new number. Its evidence stands: pooled 28,014 residuals, sd 0.050 per coordinate, white, no clipping at x = 0.05.
- **Lone-particle runs pass the numeric domain test vacuously.** A single particle has no pairs. My lone-A runs (2026-11-19/r1/001, 002, 005, 006; r2/002, 004; r3/003) pass the P-0003 numeric test at error about 0.005 but test free flight, not the pair force. I do not cite them for any pair claim. This is a reviewing trap for everyone.
- **The 0.03 bar is loose for short runs and for some geometries.** The zero-force null error (RMSE/10 for a model with all K = 0) is below 0.03 for many of the runs I cite: all three P-0009 runs (0.014), P-0003 r1/003 at separation 6 (0.014), P-0010 r2/003 (0.017). So "passes the bar" does not, by itself, exclude no interaction. Reviews now state the null error next to each bar check. For the close-range runs, the discriminating test is the null error against the bar (below).
- **Correction to my round-2 reasoning on P-0003.** I wrote that "falsified" was too strong because r = 4 and 6 passed. The rule says "falsified" stands when every cited run is in domain and above 3x predicted_error. The claim as written (separation 3 to 6) is falsified by r1/007 alone, so that falsification stands. The narrowing is a separate, proposed domain, and the file now says so.
- **Integrator sensitivity near contact.** A-A at r = 4 approaches contact by T = 2. My two earlier summaries of the step-size scan disagree: one says K = 17.74 gives rms 0.053 at step 0.002 and 0.74 at step 0.0005; the other says the best K at a 4x finer step is 17.65 with rms 0.053. Both cannot be right as stated. Rerun `aa_integrator_scan.py` before relying on either. Review verdicts use the paper's own predict(), which is what the gate uses.
- Four reviews of mine were logged unsupported earlier (reputation: 4). I will not write "replicated" with fewer than three in-domain cited runs, each within the bar.

## Round 3, 2026-11-20: what the round-2 results decide

Round-2 runs (all status ok, no census events, costs 1 + 0.02 N T):

| request | setup | account | error (paper's predict) | null error | free fit | decides |
|---|---|---|---|---|---|---|
| r2/001 | A-A, r0 = 9, T = 6 | review, P-0010 | 0.00503 | 0.030 | K_AA 11.98 vs 12.28 (-2.4%) | P-0010 |
| r2/002 | C-C, r0 = 7, T = 6 | review, P-0010 | 0.00641 | 0.056 | K_CC 10.71 vs 10.14 (+5.6%) | P-0010 |
| r2/003 | B-C, r0 = 8, T = 6 | review, P-0010 | 0.00496 | 0.017 | K_BC -4.60 vs -4.47 (+2.8%); K_CB -7.80 vs -7.77 (+0.5%) | P-0010 |
| r2/004 | B, C, C triangle, side 5, T = 2 | review, P-0009 | 0.00502 | 0.014 | not fitted | P-0009 |
| r2/005 | C, B, C triangle, rotated | review, P-0009 | 0.00495 | 0.014 | not fitted | P-0009 |
| r2/006 | C, C, B triangle, rotated 45 deg | review, P-0009 | 0.00493 | 0.014 | not fitted | P-0009 |
| r2/007 | A-A, r = 5, T = 2 | review, P-0003 | 0.00493 | 0.023 | not fitted | P-0003 (narrowing) |
| r2/008 | B-B, r0 = 1.0, T = 0.6 | research | n/a | 0.033 | K_BB 3.78 (t <= 0.3, rms 0.051) | close-BB probe |
| r2/009 | A-B, r0 = 1.0, T = 0.6 | research | n/a | 0.029 | not settled (see below) | close-AB probe |
| r2/010 | B-C, r0 = 1.0, T = 0.6 | research | n/a | 0.025 | K_BC -4.32, K_CB -7.31 (full window, rms 0.049) | close-BC probe |

Errors and null errors are RMSE/10 per the editor metric. Free fits use P = 2.5 fixed.

### Reviews filed this round (out/reviews/)

- **P-0010 (lab-keystone, far-field G(r0), r0 6 to 9): replicated.** Three in-domain runs (r2/001, 002, 003), all at error at or below 0.03. The C-C run at r0 = 7 is 5.6% above the paper's K, outside the 3% tolerance I set myself. Only r2/002 discriminates strongly against no interaction (null 0.056). The predicted_error of 0.01 is loose for T = 6 runs of this kind. Pairs at separation 6 are not covered by my runs; the A-A run at 6 is pending (r3/003).
- **P-0009 (lab-a, B, C, C triangle side 5): replicated.** Three in-domain runs (r2/004, 005, 006), all at error about 0.005. The bar is passed by the null (0.014), so the discriminating evidence is residual RMSE 0.050 per coordinate against the null's 0.14. The review says that.
- **P-0003 (lab-a, A-A, separation 3 to 6): narrowed to separation 4 to 6 (proposed).** Falsified as written by r1/007 at separation 3 (error 0.181); this stands and is stated in the review. Three in-domain runs support 4 to 6 (r1/002 at 4, r1/003 at 6, r2/007 at 5). Separation 6 passes with no force at all (null 0.014), so the upper end is weakly supported. The separation-4 pass rests on the paper's integrator (see corrections). The review's evidence is only the three supporting runs.
- **P-0004 (lab-a, A-B and A-C at 5): no review filed.** Three in-domain runs of mine are needed for the bar and each run costs at least 1.0 credit, so three runs cannot fit in the 2.88 review credit left today. I did not file an inconclusive review, because a review that misses its bar is logged unsupported.
- **P-0005, P-0006, P-0007, P-0008, P-0001, P-0002, P-0011:** no new reviews this round. P-0002 and P-0008 reviews from earlier rounds stand.

### Close-range probes (r = 1.0): findings

- **B-C (r2/010): clean.** A repulsive pair with no close approach over T = 0.6 (separation 1.0 to 2.3). A single free fit with P = 2.5 gives K_BC = -4.32 and K_CB = -7.31 at noise (rms 0.049 against zero-force 0.248). The separation-5 values are -6.10 and -10.59, so the ratio is about 0.70 for both. The probe's null error (0.025) is well above the 0.015 bar I plan to use, so it is discriminating.
- **B-B (r2/008): fits at noise only for t <= 0.3** (K = 3.78 to 4.0 over windows 0.2 to 0.3). The pair approaches contact at about t = 0.35 and passes through. Over T = 0.3 the model and the zero-force null differ by only 0.006 in error units, which is below the tracker-noise floor (about 0.005). So a T = 0.3 B-B run cannot discriminate with the bar at 0.015. Three such runs were considered and dropped. A B-B close-range claim needs a longer or softer-core test first.
- **A-B (r2/009): not settled.** The best K_AB depends on the window: 7.0 at t <= 0.2 and 4.0 at t <= 0.3, with K_BA = 7.5 in both (rms about 0.05). A constant-K pair law is not stable over the first 0.3 time units. No A-B close-range claim.
- **Reading across the probes:** near separation 1, B-C and B-B coefficients are about 0.6 to 0.7 times the separation-5 values. That is a single radial law only if the exponent is not 2.5 (an effective exponent near 2.3 fits the B-C ratio). This is one run per pair and I do not claim it.

## Round-3 requests filed today (`out/requests/2026-11-20/r3/lab-vernier/`)

Budget: research 40 allowed; 6.26 used before filing; 2.05 filed now; 31.69 left. Review 15 allowed; 12.12 used before filing; 2.24 filed now; 0.64 left. Unused credits do not roll over.

| request | account | cites | setup | cost | purpose |
|---|---|---|---|---|---|
| 001 | research | - | B-C, r = 1.0, 45 degrees, T = 0.6, dt 0.003 | 1.02 | close-BC replicate 1 (pre-registered) |
| 002 | research | - | B-C, r = 1.0, vertical, T = 0.6, dt 0.003 | 1.02 | close-BC replicate 2, orientation check |
| 003 | review | P-0010 | A-A, r0 = 6, T = 4, dt 0.01 | 1.16 | fills the missing A-A at 6 for P-0010 |
| 004 | review | P-0003 | A-A, r = 4, diagonal, T = 2, dt 0.01 | 1.08 | diagonal replicate of r1/002 for narrowed P-0003 |

### Pre-registered predictions

- **r3/001, r3/002 (B-C at r = 1, T = 0.6):** with K_BC = -4.32 and K_CB = -7.31 (P = 2.5 fixed, constant over the run), each run's error should be at or below 0.015. The zero-force null is 0.024 (above the bar), so these runs can fail. A miss on K_BC or K_CB by more than 5% (about 0.2 in K) would reject the constants. Predicted claim: `predicted_error` 0.005, domain B and C, `r_range` [1.0, 1.0], `max_particles` 2, T <= 0.6.
- **r3/003 (A-A at r0 = 6, T = 4):** P-0010 predicts K_AA = 18.0 x G(6) = 18.0 x 0.958 = 17.24 (no C factor for A-A). Error should be at or below 0.03 (bar). The zero-force null is about 0.03 here, so a pass alone is weak evidence; I will read the free fit as well and expect K within 3% of 17.24.
- **r3/004 (A-A at r = 4, diagonal):** error at or below 0.03 for P-0003 (K = 17.7) on the diagonal. Same integrator caveat as r1/002; a failure would point at orientation dependence or at the integrator.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported (noise paper, not published). Residual RMSE 0.050 per coordinate in P-0009 and P-0010 runs at the noise floor.
- **H2 (species-independent noise at N = 1).** Supported at 2.4% spread (A, B, C).
- **H3 (no clipping near a wall).** Supported at x = 0.05 and in the corner.
- **H4 (no sample-timing offset).** Supported at about 0.005 time units (r1/004).
- **H5 (stationarity over T = 100).** Mean supported; x-spread variation not reproduced.
- **H6 (P-0003 domain).** Separation 3 fails (r1/007, error 0.181). Separations 4, 5 and 6 pass with the paper's integrator. Narrowed review filed (proposed 4 to 6, weakly supported at 6).
- **H7 (P-0006 shared-law factor at separation 9 for A-C).** Supported within 3% in one fit; one run only.
- **H8 (P-0008 coefficients flat over separations 3 to 5).** Supported for A-B at 4 and B-C at 3 (r1/005, 006) and at 5. Not for A-A at 3 and 4.
- **H9 (new, P-0010): the far-field radial factor G(r0) with C-factor 0.9475.** Replicated at three pairs (P-0010 review). The C-C run at 7 is 5.6% above the paper's K, which is the one point that does not match the 3% tolerance. The A-A at 6 run (r3/003) is the next test.
- **H10 (new): A-A coefficient at separation 4 is 17.70, not 18.0.** Supported by the best-fit scan, with the integrator caveat above.
- **H11 (new, close range): B-C at separation 1.0 is about 0.7 times the separation-5 coefficients, with the r^-2.5 form holding over T = 0.6.** One run at noise (r2/010). Replicates are filed (r3/001, 002). No claim published until they return.

## Plan for next round

1. When round-3 results return, run `review_round3_2026-11-20.py` and `null_bar_2026-11-20.py` on r3/001 to 004. Compute the free K fits and the null errors, and check the pre-registered tolerances above.
2. If r3/001 and r3/002 both have error at or below 0.015 with the pre-registered constants, publish a narrow close-range B-C claim (domain B, C; r_range [1.0, 1.0]; max_particles 2; T <= 0.6; predicted_error 0.005). This fills close-BC. Cite r2/010 as the fit source and r3/001 and 002 as the evidence.
3. Update the P-0010 review with r3/003 (A-A at 6). If it passes the bar and is outside the null, the replicated verdict covers all three remaining pairs.
4. Update the P-0003 review with r3/004. If it passes, the narrowed domain has four supporting runs.
5. Rerun `aa_integrator_scan.py` to resolve the inconsistent step-size summaries before any further A-A claim.
6. Do not file a B-B close-range claim until a longer or softer-core test is designed; the T = 0.3 window cannot discriminate. A-B waits until the window dependence is understood.
7. Spend the research credits left today (31.69 after this filing) on close-range and far-field runs that discriminate; unused credits do not roll over, so the remainder should go to runs that the next round can use.

## Tools (`out/labs/lab-vernier/analysis/`, run with `python3 -I`)

- `fit_tools.py`: model residuals, RK4 pair simulator, golden-section fit of signed K (copied from my earlier analysis folder).
- `review_check.py`: applies the review rules (species, N, separation domain; error = RMSE/10) to my runs against a paper's claim.
- `review_round3_2026-11-20.py`: paper-model errors and free K fits for r2/001 to 010.
- `close_grid_2026-11-20.py`: grid fits for the close-range probes, to check optimizer stability.
- `null_bar_2026-11-20.py`: zero-force null error for each cited run against the bar.
- `file_round3_2026-11-20.py`: writes and validates round-3 requests and reviews.
- `load_results.py`: loader for result files.

Not read: `gate/`, `tools/`, `exam_papers.json`, predictor or score files. I will not read them.
