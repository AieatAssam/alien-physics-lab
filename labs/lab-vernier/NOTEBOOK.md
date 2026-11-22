# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then replicate and review other labs' claims at their edges with precise numbers.

## Reusable tools (`out/labs/lab-vernier/analysis/`)

- `fit_tools.py`: pair-law simulator (RK4, specular walls) and free-coupling fits at a fixed exponent P. Copied from the checked-in analysis folder so this folder is self-contained.
- `fit_r1_2026-11-22.py`: free K_A(B), K_B(A) at fixed P for all eight round-1 runs (2026-11-22/r1/lab-vernier/001-008), with observed minimum separation. `python3 -I ... [P]`.
- `file_round2_2026-11-22.py`: round-2 request and vote writer (checks the schema fields by hand; jsonschema is not installed here).
- Earlier scripts (`fit_h14_2026-11-22.py`, `pfree_h14_2026-11-22.py`, `oos_sep7_2026-11-22.py`, `design_h14b_2026-11-22.py`, `file_round1_2026-11-22.py`, and others) remain in the checked-in `labs/lab-vernier/analysis/` folder. They read `labs/` for `fit_tools.py`.

## Papers

- **P-0011** tracker noise for a lone particle (published).
- **P-0015** close-range B-C at separation 1.0.
- **P-0016** close-range A-C at separation 1.0.
- **P-0021** A-B pair at separation 7, at rest: effective K_A(B) = 7.75, K_B(A) = 10.97 at P = 2.5, T <= 6. **Renumbered.** My notebook called it P-0019 until the round-1 listing showed P-0019 belongs to lab-a. Refer to it as P-0021 from now on.

## Standing corrections

- **Lone-particle runs pass the numeric domain test vacuously.** My lone-A runs (2026-11-19/r1/001, 002, 005, 006; r2/002, 004; r3/003) test free flight, not the pair force. Do not cite them for any pair claim.
- **Null errors must be stated, and the null must be above the bar.** A run only discriminates if its zero-force null error exceeds 3 x predicted_error. Filed nulls:
  - P-0013 (A/C, separation 1.5, T <= 0.4): null 0.011 to 0.017 against a bar of 0.03. Not discriminating.
  - P-0012 (A-A, r = 1.0, T <= 0.15): null about 0.004 against a bar of 0.024. Not discriminating.
  - P-0017 (B-B, r = 1.0, T <= 0.15) and P-0018 (C-C, r = 1.0, T <= 0.15): null about 0.0014 against a bar of 0.024. Not discriminating.
  - P-0019 (lab-a, B-B, r = 1.0, T <= 0.3, predicted error 0.008): null about 0.017 against a bar of 0.024. Not discriminating (estimate: 0.5 x 3.86 x 0.3^2 per particle, RMS over particles and coordinates, / L).
  - P-0020 (lab-b, A-B, r = 1.0, T <= 0.15, predicted error 0.008): null about 0.007 against a bar of 0.024. Not discriminating.
  - Earlier nulls: A-B at 5, 0.032; A-C at 5, 0.036-0.037; A-C at 1.0, 0.040.
- **Fit exponent and coupling are not separately identified over a short window.** The RMSE over P = 2.1 to 3.0 is flat (0.0050 at each P for runs 002, 003, 010). What is identified is the ratio of fitted K at two separations: d ln K_fit / d ln r = P_fit - P_true. Read exponents only from the separation dependence, never from one run.
- **Close pass can break a run.** 2026-11-21/r3/001 (A-B, separation 6, T = 6) falls to separation 1.46 at t = 5.5 and the particles pass through each other. Its fit RMSE is 0.057 against a 0.005 floor. Excluded from all H14 conclusions. Use T <= 4 for separation 6.
- **Integrator sensitivity near contact.** A-A at r = 4 approaches contact by T = 2. My two earlier step-size summaries disagree (K = 17.74 vs 17.65). Still open; `aa_integrator_scan.py` must be rerun before a further A-A claim relies on either.
- **Four reviews of mine were logged unsupported earlier.** I write "replicated" only with at least three in-domain cited runs, each within the bar, and only when the null test above passes.
- **Review and research credits are separate.** A review run must cite the paper and use account `review`. Its evidence must be my own request ids.
- **Model-blow-up check.** Paper models with singular forces (r^-2.5) can blow up at close approach (P-0014). Check measured minimum separation before blaming the physics.

## Round 1 results, analysed this session (2026-11-22)

Requests 2026-11-22/r1/lab-vernier/001-008, all `ok`, cost 9.36 in total. Free K at fixed P = 2.5, full window, from `fit_r1_2026-11-22.py`:

| run | separation, orientation | T | K_A(B) | K_B(A) | R = K_B(A)/K_A(B) | fit RMSE/L | null RMSE/L | min. separation observed |
|---|---|---|---|---|---|---|---|---|
| 008 | 4, horizontal | 2 | 9.15 | 12.85 | 1.405 | 0.0052 | 0.026 | 2.38 |
| 001 | 5, horizontal | 3 | 9.01 | 12.66 | 1.405 | 0.0051 | 0.033 | 2.85 |
| 002 | 5, vertical | 3 | 8.86 | 12.55 | 1.417 | 0.0052 | 0.032 | 2.91 |
| 003 | 6, horizontal | 4 | 8.37 | 11.78 | 1.408 | 0.0049 | 0.033 | 3.77 |
| 004 | 6, vertical | 4 | 8.41 | 12.05 | 1.432 | 0.0048 | 0.034 | 3.80 |
| 005 | 8, horizontal | 6 | 6.67 | 9.62 | 1.442 | 0.0051 | 0.028 | 6.15 |
| 006 | 9, horizontal | 6 | 6.03 | 8.26 | 1.371 | 0.0051 | 0.018 | 7.79 |
| 007 | 9, vertical | 6 | 5.96 | 8.27 | 1.387 | 0.0049 | 0.018 | 7.82 |

Every run is in domain: no close approach (observed minimum separations 2.4 to 7.8). Every fit is at the tracker noise floor (0.005 per coordinate in L units). Every null sits at least 3.5 times the fit RMSE.

Earlier round-3 and round-1 separation-7 and 8 values (fit at P = 2.5, from the 2026-11-21 runs): K_A(B) = 7.75 at 7 (runs 003 and 010, averaged; 7.74 and 7.77), K_A(B) = 6.88 at 8 (run 002, diagonal). Run 005 (today, horizontal, 8) gives 6.67. The separation-8 mean is 6.78.

### What the table says about the far field

**K_A(B) at fixed P = 2.5 falls monotonically across separations 4 to 9:** 9.15, 8.94, 8.39, 7.75, 6.78, 6.00. Each step is well above the 1% precision, so the decline is real.

The local effective exponent follows from d ln K_fit / d ln r = P_fit - P_true, with P_fit = 2.5:

| interval (mid-r) | slope d ln K / d ln r | P_true (local) |
|---|---|---|
| 4 to 5 (4.5) | -0.10 | 2.60 +/- 0.15 |
| 5 to 6 (5.5) | -0.35 | 2.85 +/- 0.15 |
| 6 to 7 (6.5) | -0.51 | 3.01 +/- 0.15 |
| 7 to 8 (7.5) | -1.00 | 3.50 +/- 0.15 |
| 8 to 9 (8.5) | -1.04 | 3.54 +/- 0.15 |

The error of about 0.15 per interval is from the 1% K precision over the interval width. Overall, 4 to 9 gives P_true = 3.02.

**Conclusion (H14 revised):** the A-B far field is **not** a single power law with P = 2.5 across r = 4 to 9. The local exponent rises from about 2.6 at r = 4.5 to about 3.5 at r = 8.5. That is steepening, not a constant exponent. The pre-registered H14 prediction (K at 6 and 8 within 3% of 9.0) is already falsified (round-1 result: K(8) = 6.78, 25% low; K(6) = 8.39, 7% low).

Candidate form, not tested: a screened power law F = K r^(-p) exp(-r/lambda) gives a linear local exponent P_true(r) = p + r/lambda. The slope above, about 0.22 per unit r, suggests lambda about 4.4 and p about 1.6. This is one possibility among several (for example a cutoff, or the wall images), and it is not a claim. The infall requests below test the continuous shape.

### H17: K_B(A)/K_A(B) ratio

- Pre-registered: R = 1.41 +/- 0.02 at all separations 4 to 9. Falsifier: R outside 1.41 +/- 0.04 at any separation, or a monotone trend of 3% or more over 4 to 9.
- Result by separation: 4: 1.405. 5: 1.40 and 1.42. 6: 1.41 and 1.43. 8: 1.44. 9: 1.37 and 1.39.
- **Status:** not falsified. R stays within 1.41 +/- 0.04 everywhere. But the separation-9 pair (mean 1.38) sits 2% below 1.41, at the edge of the band, and the trend is not monotone (up at 8, down at 9). Treat as **supported with a marginal point at 9**. The scatter in R (about 1.5%) is about the same size as the 2% K precision, so R is consistent with a constant 1.41 but not sharply so.
- R is independent of P: at P = 2.1 and 3.0 it stayed at 1.40 to 1.41 for separations 7 and 8 (earlier analysis).

### H18: centre-of-mass drift

Earlier: with m_A/m_B = 1.41, the CM drift was 0.001 per time unit; with equal masses 0.02 to 0.045. Round-1 runs were not separately tested for CM drift in this session. Inference, not measurement of masses.

### H14b shape prediction (pre-registered 2026-11-22)

Predicted: K_A(B) at separation 8 falls 5 to 15% below 7.75. Result: 6.67 (14% below) at separation 8, horizontal, run 005. Also monotone across 5, 7, 8, 9 (8.94, 7.75, 6.67, 6.00). **Supported at the upper edge of the range.** It is consistent with the local exponent rising through the range, as above.

## Round 2 (2026-11-22): votes and filings

### Vote

`out/grants/2026-11-22/votes/lab-vernier.json`: **vote for lab-keystone** (the local A-A exponent test at r = 0.5 to 2.25). Reason: it is the cheapest proposal (1.03 credits), and its pre-registered alternatives differ by about 3.5 sigma by my noise estimate (5.66 for P = 2.5 against 3.7 for P = 1.9). It tests the exponent behind every close-range claim, and my far-field table now says the effective exponent drifts. Caveat: its cross-pair forces assume P.

Why not the others:
- **lab-a (9-body Latin square, T = 0.5):** the displacements are about 0.03 at T = 0.5, and the null RMSE sits below the support bar, so a no-force model would pass. Not discriminating.
- **lab-b (16-body lattice, T = 1.0):** the strongest signal and a clear falsifier. But its pair laws at 2.2 to 4.4 are untested, and the far-field exponent is clearly not 2.5 at 4 to 9, so a miss could come from the pair laws rather than from additivity. Its own plan to run the 2.0 and 3.0 mixed-pair runs first is the right fix. I would vote for it after those results.
- **lab-c (octagon, T = 5):** eight bodies at adjacent separation 2.68 will collapse on the centre within T of about 2 to 3 (the same behaviour I saw for three and four bodies). Contact makes the pairwise prediction singular, so the falsifier is not well defined.
- My own proposal (infall) is not eligible.

### Requests (research account, tracker only, est. 4.86 credits of 40)

| request | setup | T | dt | est. cost | min. separation (K = 9 / 6, P = 2.5) |
|---|---|---|---|---|---|
| 2026-11-22/r2/lab-vernier/001 | A-B infall from 9, horizontal (A x=0.5, B x=9.5, y=5) | 10 | 0.01 | 1.40 | 2.52 / 5.42 |
| 002 | same, vertical (A y=0.5, B y=9.5, x=5) | 10 | 0.01 | 1.40 | 2.52 / 5.42 |
| 003 | A-B separation 3, horizontal, centred | 1 | 0.005 | 1.04 | 2.22 / 2.50 |
| 004 | A-B separation 2, horizontal, centred | 0.5 | 0.0025 | 1.02 | 1.46 / 1.66 |

Pre-registration (written before any round-2 result):
- **001, 002 (infall, windows at fixed P = 2.5):** K_A(B) per window must follow the round-1 table within 4%: K(4) = 9.1, K(5) = 8.9, K(6) = 8.4, K(7) = 7.75, K(8) = 6.8, K(9) = 6.0. R = K_B(A)/K_A(B) = 1.41 +/- 0.02 in every window. **Falsified** if the windows are flat (within 3% of one value), or if R leaves 1.41 +/- 0.04.
- **003, 004 (short range):** K(3)/K(4) = 1.00 if the local exponent is 2.5 at r = 2 to 4. It is 0.86 for a local exponent 1.9 (the Keystone alternative). A steepening that continues inward predicts 0.93 to 0.97.

Note: the "min. separation" column is a P = 2.5 simulation with constant K. The infall's real K falls with r (see above), so the true minimum should be somewhat larger. No contact expected in any case.

Budget after filing: research 9.36 (round 1) + 4.86 (round 2) = 14.22 of 40, so about 25.8 credits remain today. Review 0 of 15 used.

### Reviews filed this round: none, with reasons

- **P-0012, P-0013, P-0017, P-0018, P-0019, P-0020:** every zero-force null sits below the bar (see Standing corrections). No in-domain run can discriminate, so a replicate would be a non-test. Not filed.
- Unused review credits (15) lapse. I would rather spend them on a claim whose null exceeds its bar.

### Grant

My proposal (infall, T = 10, round 1) is not voted on by me. If it wins, the 120 credits are for round 3. The round-2 infall requests (001, 002) cover the same measurement on research credits, so a round-3 grant event should go to something that round 2 does not cover.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported. Published as P-0011.
- **H2 (species-independent noise at N = 1).** Supported at 2.4% spread.
- **H3 (no clipping near a wall).** Supported at x = 0.05 and in the corner.
- **H4 (no sample-timing offset).** Supported at about 0.005 time units.
- **H5 (stationarity over T = 100).** Mean supported; x-spread variation not reproduced.
- **H6 (P-0003 domain).** Separation 3 fails for P-0003 (r1/007, error 0.181). Separations 4 and 5 pass. Narrowed review filed in round 1.
- **H7 (P-0006 shared-law factor at separation 9 for A-C).** Supported within 3% in one fit; one run only.
- **H8 (P-0008 coefficients flat over separations 3 to 5).** Supported for A-B at 4 and B-C at 3, 5. Not for A-A at 3 and 4.
- **H9 (P-0010 far-field G(r0) with C-factor 0.9475).** Replicated at all three pairs and at A-A at 6. The C-C run at 7 is 5.6% above the paper's K; not reproduced within 3%. **Note:** the A-B far field (H14) now shows the exponent is not constant over 4 to 9. Re-examine P-0010's separation range before any further far-field claim relies on P = 2.5.
- **H10 (A-A coefficient at separation 4 is 17.70, not 18.0).** Supported by the diagonal replicate. Integrator caveat still open.
- **H11 (close range B-C).** Supported: K_BC -4.32 and K_CB -7.31 at r = 1.0 for T <= 0.6. Published as P-0015.
- **H12 (A-B and B-B are not constant-K over the first 0.3 time units at r = 1).** The A-B probe gives K_AB 7.0 at t <= 0.2 and 4.0 at t <= 0.3. Still open.
- **H13 (pairwise superposition).** Untested for more than two bodies. Multi-body designs collapse in the 10-unit chamber with these couplings.
- **H14 (A-B far-field power law at P = 2.5 over r = 4 to 9).** **Falsified** (round 1, 2026-11-22). K_A(B) falls from 9.15 to 6.00 across 4 to 9. Local exponent rises from 2.6 to 3.5. Continuous shape being tested by requests 001 and 002.
- **H14c (new): steepening is a smooth, continuous change of local exponent with r.** Open. Test: infall windows (001, 002) and short-range points at 3 and 2 (003, 004).
- **H15 (P-0004-c2 magnitude).** K_C(A) about -20.7 from three repeats, against the published -21.38. Published error passes the bar, so I filed `replicated` but flagged the magnitude.
- **H16 (P-0014 A-A contact failure).** The P-0014 model's integrator blows up after close approach at t about 1.2 for A-A at r0 = 3. Filed as the P-0014 falsification.
- **H17 (ratio K_B(A)/K_A(B) = 1.41 +/- 0.02 at separations 4 to 9).** Supported at 4 to 8 (1.40 to 1.44). Marginal at 9 (1.38, at the edge of the band). Not monotone.
- **H18 (masses m_A/m_B = 1.41 with momentum conservation).** Inference from H17. Not tested directly this session.

## Plan for next round

1. Round 3: read `results/2026-11-22/r2/lab-vernier/001-004`. Refit with `fit_r1_2026-11-22.py` after adding the new runs to a copy of the RUNS list.
   - Check the 001 and 002 windows against the pre-registered table (within 4%) and R within 1.41 +/- 0.04. Read the local exponent from the windows, not from one run.
   - Check 003 and 004 for K(3)/K(4): 1.00 (P = 2.5 locally), 0.86 (1.9), or 0.93 to 0.97 (steepening inward).
2. If the windows confirm the steepening, file a narrowed claim: "K_A(B) at P = 2.5 falls from 9.1 (r = 4) to 6.0 (r = 9); the local exponent rises from 2.6 to 3.5." Make no statement about the functional form. Domain: A-B, r 4 to 9, T <= 4 for separation 6 and T <= 6 for separation 8 or 9, max_particles 2.
3. If the windows are flat, the table is a fitting artifact (for example, the wall reflections at sep 8 and 9). Check the wall images in `fit_tools.simulate` before anything else.
4. Do not file close-AB or close-BB until H12 is settled.
5. Reviews: none pending that discriminate. Only file a review where the zero-force null exceeds 3 x predicted_error.
6. Rerun `aa_integrator_scan.py` before any further A-A claim.
7. Sharpen-* open problems need predicted_error at or below 0.0025. The tracker noise is about 0.005 per coordinate in L units, so 0.0025 is below the noise. Do not file a sharper claim without a noise-floor argument.
8. If round-2 lab-b (16-body) results appear with its 2.0 and 3.0 mixed-pair runs, be ready to review whether pair laws at 2.2 to 4.4 are consistent with the steepening found here.

## Budgets, 2026-11-22

- **Research:** 40 allowed. Used 9.36 (round 1) and 4.86 (round 2, requests 001-004). About 25.8 remaining.
- **Review:** 15 allowed. 0 used. Declined (see above).
- **Grant:** round-1 proposal filed (infall). Vote cast for lab-keystone in round 2.

## Not read

`gate/`, `tools/`, `exam_papers.json`, predictor or score files. I will not read them.
