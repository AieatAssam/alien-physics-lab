# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then replicate and review other labs' claims at their edges with precise numbers. Reusable tools: `out/labs/lab-vernier/analysis/` (`fit_tools.py` for pair-law fits and residuals; `fit_round1_2026-11-21.py` for round-1 free-constant fits; older round scripts there and in `labs/lab-vernier/analysis/`).

## Standing corrections

- **My papers, by current number.** P-0011: tracker noise for a lone particle (published, lab-vernier). P-0015: close-range B-C at separation 1.0 (my former P-0012 draft, renumbered by the gate because Plumbline took P-0012). P-0016: close-range A-C at separation 1.0 (filed this round). Refer to papers by title if numbers move again.
- **Lone-particle runs pass the numeric domain test vacuously.** A single particle has no pairs. My lone-A runs (2026-11-19/r1/001, 002, 005, 006; r2/002, 004; r3/003) test free flight, not the pair force. I do not cite them for any pair claim.
- **Null errors must be stated.** A run only discriminates if its zero-force null error is above the bar. Measured nulls from the zero-force model at the initial positions (this round): A-B at 5 0.032; A-C at 5 0.036-0.037; A-C at 1.0 0.040. My earlier design-time estimate of 0.052 for the close-AC probe was wrong; the measured value is 0.040. Still above the 0.015 bar.
- **Integrator sensitivity near contact.** A-A at r = 4 approaches contact by T = 2. My two earlier step-size summaries disagree (K = 17.74 vs 17.65). Still open; `aa_integrator_scan.py` must be rerun before a further A-A claim relies on either.
- **Four reviews of mine were logged unsupported earlier.** I write "replicated" only with at least three in-domain cited runs, each within the bar.
- **Review and research credits are separate.** A review run must cite the paper and use account `review`. Its evidence must be my own request ids.
- **Round-1 note on my earlier plan.** The notebook said my round-1 noise paper was never placed. It was: P-0011.

## Round 2, 2026-11-21: results and decisions

Round-1 runs (2026-11-21/r1/lab-vernier, all status ok, no census events, costs 1.12 / 1.02 / 1.24 as filed).

| request | setup | paper-model error | null | free fit (P = 2.5, full window) | decision |
|---|---|---|---|---|---|
| 001 | A-B, r = 5, horizontal, T = 3 | 0.00512 | 0.032 | K_A(B) 8.90, K_B(A) 12.61 | P-0004-c1 replicate |
| 002 | A-B, r = 5, diagonal, T = 3 | 0.00508 | 0.032 | 8.97, 12.55 | P-0004-c1 replicate |
| 003 | A-B, r = 5, vertical, T = 3 | 0.00488 | 0.032 | 8.91, 12.56 | P-0004-c1 replicate |
| 004 | A-C, r = 5, horizontal, T = 3 | 0.00521 | 0.037 | K_A(C) -8.85, K_C(A) -20.77 | P-0004-c2 replicate |
| 005 | A-C, r = 5, diagonal, T = 3 | 0.00516 | 0.036 | -8.86, -20.66 | P-0004-c2 replicate |
| 006 | A-C, r = 5, vertical, T = 3 | 0.00510 | 0.036 | -8.65, -20.60 | P-0004-c2 replicate |
| 007 | A-C, r = 1.0, horizontal, T = 0.6 | 0.00512 | 0.040 | K_AC -6.25, K_CA -14.78 | close-AC fit run |
| 008 | A-C, r = 1.0, vertical, T = 0.6 | 0.00503 | 0.040 | -6.27, -14.81 | close-AC replicate (within 0.4%) |
| 009 | A-C, r = 1.0, diagonal, T = 0.6 | 0.00542 | 0.040 | -6.25, -14.79 | close-AC replicate (within 0.4%) |
| 010 | A-B, r = 7, horizontal, T = 6 | 0.00974 | not computed | K_A(B) 7.76, K_B(A) 10.99 | far-field probe, see H14 |

### Reviews and claims filed this round (out/)

- **P-0004 (lab-a), verdict `replicated` (both claims).** c1 (A-B at 5): runs 001-003 pass the bar (0.0049-0.0051 against 0.03), and free K values are within 3% of 9.0 and 12.35. c2 (A-C at 5, previously single-run): runs 004-006 pass, and free K_A(C) is within 3.2% of -8.59. K_C(A) fits at -20.6 to -20.8, which is about 3% above the paper's -21.38. The paper-model error still passes the bar, so the verdict stands, and the review comment says the magnitude should read as about -20.7.
- **P-0016 (new, mine): close-range A-C at separation 1.0, T <= 0.6.** K_AC -6.25, K_CA -14.78. Domain: species A, C; r_range [0.999, 1.001]; max_particles 2; predicted_error 0.006. Evidence 007, 008, 009; 008 and 009 are the pre-registered replicates (free K within 0.4%). This is intended to fill close-AC (bounty 2). Paper number may move.

### Grant vote (out/grants/2026-11-21/votes/lab-vernier.json)

Voted for lab-a (Plumbline), the nine-particle grid test. Reason: pre-registered RMSE thresholds (0.01 supports, 0.02 refutes), uses only a pair law already measured, about 1.1 credits. Not voted for my own proposal.

### Credits

- Research: 40 allowed; 4.30 filed round 1 (007-010) plus 15.2 and 8.3 earlier days. Round-2 research spend today so far: 4.30 (007-010 from round 1). 35.70 unused, nothing filed this round.
- Review: 15 allowed; 6.72 filed round 1 (001-006). 8.28 unused, nothing filed this round.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported. Residual RMSE 0.050 per coordinate in all P-0009/P-0010 and r3 runs. Published as P-0011.
- **H2 (species-independent noise at N = 1).** Supported at 2.4% spread.
- **H3 (no clipping near a wall).** Supported at x = 0.05 and in the corner.
- **H4 (no sample-timing offset).** Supported at about 0.005 time units (r1/004).
- **H5 (stationarity over T = 100).** Mean supported; x-spread variation not reproduced.
- **H6 (P-0003 domain).** Separation 3 fails (r1/007, error 0.181). Separations 4 and 5 pass with the paper's integrator and with the diagonal replicate (r3/004). Narrowed review filed (round 1).
- **H7 (P-0006 shared-law factor at separation 9 for A-C).** Supported within 3% in one fit; one run only.
- **H8 (P-0008 coefficients flat over separations 3 to 5).** Supported for A-B at 4 and B-C at 3, 5. Not for A-A at 3 and 4.
- **H9 (P-0010 far-field G(r0) with C-factor 0.9475).** Replicated at all three pairs and at A-A at 6. The C-C run at 7 is 5.6% above the paper's K; not reproduced within 3%.
- **H10 (A-A coefficient at separation 4 is 17.70, not 18.0).** Supported by the diagonal replicate. Integrator caveat still open.
- **H11 (close range B-C).** Supported: K_BC -4.32 and K_CB -7.31 at r = 1.0 for T <= 0.6. Published as P-0015.
- **H12 (A-B and B-B are not constant-K over the first 0.3 time units at r = 1).** The A-B probe (r2/009) gives K_AB 7.0 at t <= 0.2 and 4.0 at t <= 0.3. Still open: needs a longer or softer-core test.
- **H13 (pairwise superposition).** Untested for more than two bodies. Proposed as an eight-body grant; not awarded this round by my vote.
- **H14 (new, A-B exponent or shape at separation 7).** Single run 2026-11-21/r1/lab-vernier/010. With P = 2.5 fixed, the free K at r = 7 is 7.76 (A on B) and 10.99 (B on A), about 14% and 11% below the separation-5 values (9.0, 12.35). Either the A-B exponent is not 2.5 or the law is not a single power law. The P-0004 and P-0005 paper models are fitted at separation 5 only and make no claim at 7, so no review is affected. Needs a second far run at 7 (or a run at 6 and 8) to fit the exponent before I say anything about it.
- **H15 (new, P-0004-c2 magnitude).** K_C(A) about -20.7 from three repeats, against the published -21.38. The published value's error passes the bar, so I filed `replicated` but flagged the magnitude.

## Plan for next round

1. Round 3: if the eight-body grant is awarded to me, write the pairwise prediction first, then run. Otherwise do not run eight-body tests on research credits without a pre-registered prediction.
2. Watch for P-0015 and P-0016 results from the gate. Once P-0016 is accepted, close-AC is filled.
3. Close-AB, close-BB, close-CC: H12 and H14 must be settled first (window dependence and the exponent). Do not file a close-range AB or BB claim before then.
4. Review of P-0014 (Keystone, A or C at separation 2.5 to 3.5) and P-0013 (Nullius, A/A, A/C, C/C at 1.5) is still open. The review account has 8.28 credits. Only file if the runs are in domain and pre-registered; a miss costs reputation.
5. Rerun `aa_integrator_scan.py` to settle the two inconsistent step-size summaries before any further A-A claim.
6. Sharpen-* open problems need predicted_error at or below 0.0025 for species A, B, C. My current claims sit at 0.005 to 0.006. Do not file a sharper claim without a noise-floor argument: the tracker noise is 0.005 per coordinate in L units, so 0.0025 is below the noise.

## Tools (`out/labs/lab-vernier/analysis/`, run with `python3 -I`)

- `fit_tools.py`: model residuals, RK4 pair simulator, golden-section fit of signed K.
- `fit_round1_2026-11-21.py`: free-constant fits for 001-010 at P = 2.5, full window.
- Earlier (in `labs/lab-vernier/analysis/`): `review_check.py` applies the review rules (species, N, separation domain; error = RMSE/10) to my runs against a paper's claim, `null_round3_2026-11-21.py`, `design_p0004_2026-11-21.py`, `file_round1_2026-11-21.py`, `write_p0012_and_reviews_2026-11-21.py`.

Not read: `gate/`, `tools/`, `exam_papers.json`, predictor or score files. I will not read them.
