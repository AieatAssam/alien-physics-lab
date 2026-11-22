# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then replicate and review other labs' claims at their edges with precise numbers.

Reusable tools in `out/labs/lab-vernier/analysis/`:
- `fit_tools.py`: pair-law simulator (RK4, specular walls) and free-coupling fits at a fixed exponent P.
- `fit_h14_2026-11-22.py`: free K_A(B), K_B(A) at P = 2.5 for the H14 far-field runs.
- `pfree_h14_2026-11-22.py`: scan over P (2.0 to 3.5) for the same runs; `traj` mode prints separation vs time.
- `oos_sep7_2026-11-22.py`: out-of-sample check of the separation-7 fit, and centre-of-mass drift for mass ratios 1.0 and 1.41.
- `design_h14b_2026-11-22.py`: minimum-separation check for candidate designs (run before filing anything).
- `file_round1_2026-11-22.py`: today's request and grant writer (validated against the schemas).
- Older: `file_round3_2026-11-21.py`, `diag_p0014_run007_2026-11-21.py`, and others.

## Current papers

- **P-0011** tracker noise for a lone particle (published).
- **P-0015** close-range B-C at separation 1.0.
- **P-0016** close-range A-C at separation 1.0.
- **P-0019** A-B pair at separation 7, at rest: effective K_A(B) = 7.75 and K_B(A) = 10.97 at P = 2.5, T <= 6 (filed 2026-11-22). Refer by title if the number moves.

## Standing corrections

- **Lone-particle runs pass the numeric domain test vacuously.** My lone-A runs (2026-11-19/r1/001, 002, 005, 006; r2/002, 004; r3/003) test free flight, not the pair force. Do not cite them for any pair claim.
- **Null errors must be stated, and the null must be above the bar.** A run only discriminates if its zero-force null error exceeds 3 x predicted_error. Filed nulls:
  - P-0013 (A/C, separation 1.5, T <= 0.4): null 0.011 to 0.017 against a bar of 0.03. Not discriminating.
  - P-0012 (A-A, r = 1.0, T <= 0.15): null about 0.004 against a bar of 0.024. Not discriminating.
  - **P-0017 (B-B, r = 1.0, T <= 0.15) and P-0018 (C-C, r = 1.0, T <= 0.15): null about 0.0014 (estimated: 0.5 x 3.98 x 0.15^2 displacement, RMS over samples and coordinates, / L) against a bar of 0.024.** Not discriminating; a no-force model passes.
  - Earlier nulls: A-B at 5, 0.032; A-C at 5, 0.036-0.037; A-C at 1.0, 0.040.
- **Fit exponent and coupling are not separately identified over a short window.** The RMSE over P = 2.1 to 3.0 is flat (0.0050 at each P for runs 002, 003, 010). What is identified is the ratio of fitted K at two separations: d ln K_fit / d ln r = P_fit - P_true. Read exponents only from the separation dependence, never from one run.
- **Close pass can break a run.** 2026-11-21/r3/001 (A-B, separation 6, T = 6) falls to separation 1.46 at t = 5.5 and the particles pass through each other (A ends at x = 6.97, B at 1.00). Its fit RMSE is 0.057 against a 0.005 floor. Excluded from all H14 conclusions. Use T <= 4 for separation 6.
- **Integrator sensitivity near contact.** A-A at r = 4 approaches contact by T = 2. My two earlier step-size summaries disagree (K = 17.74 vs 17.65). Still open; `aa_integrator_scan.py` must be rerun before a further A-A claim relies on either.
- **Four reviews of mine were logged unsupported earlier.** I write "replicated" only with at least three in-domain cited runs, each within the bar, and only when the null test above passes.
- **Review and research credits are separate.** A review run must cite the paper and use account `review`. Its evidence must be my own request ids.
- **Model-blow-up check.** Paper models with singular forces (r^-2.5) can blow up at close approach (P-0014, see Round 3 of 2026-11-21). Check measured minimum separation before blaming the physics.

## Round 1, 2026-11-22: results from the 2026-11-21 round-3 H14 runs

Runs 2026-11-21/r3/lab-vernier/001-003 are back (cost 1.24 each). Plus the earlier round-1 run 010 (same separation 7).

Free K at fixed P = 2.5, full window (`fit_h14_2026-11-22.py`):

| run | separation, orientation | K_A(B) | K_B(A) | fit RMSE/L | null RMSE/L | status |
|---|---|---|---|---|---|---|
| 001 | 6, horizontal, T=6 | 9.94 | 7.09 | 0.057 | 0.129 | excluded: close pass to 1.46 |
| 002 | 8, diagonal | 6.88 | 9.65 | 0.0049 | 0.029 | in domain |
| 003 | 7, vertical | 7.74 | 10.95 | 0.0050 | 0.048 | in domain |
| 010 (r1) | 7, horizontal | 7.77 | 10.99 | 0.0052 | 0.049 | in domain |

### H14 pre-registered result: falsified at the stated falsifier

- **Prediction (pre-registered 2026-11-21):** free K_A(B) at r = 6 and 8 within 3% of 9.0.
  **Result:** r = 8 gives 6.88 (24% low). r = 6 is excluded. **Prediction fails.**
- **Falsifier (pre-registered):** a monotone trend of 5% or more across r = 5, 7, 8 rejects P = 2.5 for A-B.
  **Result:** 9.0 (r = 5, notebook value from earlier fits), 7.75 (r = 7), 6.88 (r = 8). Monotone, 14% and 24% down. **Falsifier met for K_A(B).** The r = 5 reference is the weakest link: it was not refit this session. Its K_B(A) was not recorded.
- **Scope of the falsification:** a single power law with P = 2.5 is rejected for A-B across r = 5 to 8. It is not a claim about the true exponent (see next point).

### What the far field looks like, from the K ratios

- At fixed P_fit, K_fit(r) scales as r^(P_fit - P_true). From the 7 to 8 pair (runs 003 and 002): slope -0.89 (K_A(B)) and -0.94 (K_B(A)) at P_fit = 2.5. That gives P_true = 3.39 and 3.44.
- Same pair at P_fit = 3.0: slope -0.27, P_true = 3.27. At P_fit = 2.1 (K_A(B)): P_true = 3.29. The three estimates agree, so the exponent from the 7 to 8 pair is about 3.3 to 3.4, with an error of about +-0.2 from the 1 to 2% K precision.
- From r = 5 to r = 7 (using the notebook's 9.0 at r = 5): P_true = 2.95.
- **These two estimates differ by about 0.4, about 2 sigma.** A single power law is not clearly supported. Possible explanations: the law steepens with separation (not a power law), or the r = 5 reference is biased. Round-1 runs 001-008 test this directly.

### Ratio K_B(A)/K_A(B) and centre of mass: a new, P-independent result

- Ratio R = K_B(A)/K_A(B): 1.402 (run 002, r = 8), 1.415 (run 003, r = 7), 1.415 (run 010, r = 7). At P = 2.1 and P = 3.0 the ratio stays 1.40 to 1.41. **R is independent of P and of separation in this sample.**
- Centre of mass (`oos_sep7_2026-11-22.py`): with masses m_A/m_B = 1.41, the drift is 0.0008 and 0.0009 per time unit (runs 002, 003, 010). With equal masses it is 0.017 to 0.045. So the ratio R = 1.41 is consistent with momentum conservation with m_A/m_B = 1.41. This is an inference, not a measurement of masses.
- Out-of-sample, separation 7 (fit on one orientation, test on the other): RMSE/L 0.0050 (010 to 003) and 0.0052 (003 to 010). This is at the tracker noise floor (0.05 per coordinate, /10 = 0.005).

## Round 1 filings, 2026-11-22

### Pre-registration (written before any 2026-11-22 result)

- **Ratio test (H17):** R = K_B(A)/K_A(B) = 1.41 +/- 0.02 at every separation 4 to 9. Falsifier: R outside 1.41 +/- 0.04 at any separation, or a monotone trend in R of 3% or more over 4 to 9.
- **Shape test (H14b):** K_A(B) at P = 2.5 falls from the separation-7 value (7.75) by 5 to 15% at separation 8 (run 005). A monotone trend across 5, 7, 8, 9 is expected; its size is what the exponent estimate predicts.
- **Null discriminating:** zero-force displacements for separations 5 to 9 at T = 3 to 6 are at least 0.4 per particle, so each run discriminates against a no-force model (nulls at least 10 x the noise floor).

### Research requests (account `research`, est. cost 9.36 of 40 credits)

| request | setup | T | dt | cost |
|---|---|---|---|---|
| 2026-11-22/r1/lab-vernier/001 | A-B separation 5, horizontal, centred | 3 | 0.02 | 1.12 |
| 002 | A-B separation 5, vertical, centred | 3 | 0.02 | 1.12 |
| 003 | A-B separation 6, horizontal, A at x=2 | 4 | 0.02 | 1.16 |
| 004 | A-B separation 6, vertical, centred | 4 | 0.02 | 1.16 |
| 005 | A-B separation 8, horizontal, A at x=1 | 6 | 0.02 | 1.24 |
| 006 | A-B separation 9, horizontal, A at x=0.5 | 6 | 0.02 | 1.24 |
| 007 | A-B separation 9, vertical, A at y=0.5 | 6 | 0.02 | 1.24 |
| 008 | A-B separation 4, horizontal, centred | 2 | 0.02 | 1.08 |

All request files validate against `protocol/request.schema.json`. Design minimum separations (K = 9, P = 2.5): 3.3, 3.3, 4.1, 4.1, 6.0, 7.6, 7.6, 2.7. No contact.

### Grant proposal (round 1)

`out/grants/2026-11-22/proposals/lab-vernier.json`: "Single-pair infall from separation 9: far-field shape of the pair law in one run." A-B pair from rest at separation 9, T = 10, dt = 0.01. Covers r = 9 down to about 4.2 without contact (simulated). It samples the force over a continuous range in one run and tests the H14 shape claim and the H17 ratio.

I checked the three-body and four-body alternatives first. Both collapse to contact within T = 4 (minimum separations 0.09 and 0.27). They are not filed.

### Publication

- **P-0019 (lab-vernier): A-B pair at separation 7, at rest: effective K_A(B) = 7.75, K_B(A) = 10.97 at P = 2.5, T <= 6.** Domain: species A and B, r_range [6.9, 7.1], max_particles 2. Predicted error 0.007 (out-of-sample 0.0050 to 0.0052; bar 0.021). Evidence: 2026-11-21/r3/lab-vernier/003 and 2026-11-21/r1/lab-vernier/010. The claim explicitly disclaims any exponent and any other separation. Minimum separation over T = 6 is 3.77, so the pair does not reach contact in the domain.

### Reviews filed this round: none, with reasons

- **P-0012 (lab-a):** null about 0.004 against a bar of 0.024. Not discriminating. Not filed.
- **P-0013 (lab-c):** null 0.011 to 0.017 against a bar of 0.03 (within domain separation 1.45 to 1.55). Not discriminating. Not filed.
- **P-0017 (lab-b, B-B) and P-0018 (lab-b, C-C), both at r = 1.0, T <= 0.15:** null about 0.0014 against a bar of 0.024. A no-force model passes by a factor of about 17. Not filed. A "replicated" verdict here would be meaningless, and I will not file one.
- I have no in-domain run to falsify any of them. Claims with a bar of 3 x 0.008 at T <= 0.15 cannot be falsified by any physical K error at that duration.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported. Published as P-0011.
- **H2 (species-independent noise at N = 1).** Supported at 2.4% spread.
- **H3 (no clipping near a wall).** Supported at x = 0.05 and in the corner.
- **H4 (no sample-timing offset).** Supported at about 0.005 time units.
- **H5 (stationarity over T = 100).** Mean supported; x-spread variation not reproduced.
- **H6 (P-0003 domain).** Separation 3 fails for P-0003 (r1/007, error 0.181). Separations 4 and 5 pass. Narrowed review filed in round 1.
- **H7 (P-0006 shared-law factor at separation 9 for A-C).** Supported within 3% in one fit; one run only.
- **H8 (P-0008 coefficients flat over separations 3 to 5).** Supported for A-B at 4 and B-C at 3, 5. Not for A-A at 3 and 4.
- **H9 (P-0010 far-field G(r0) with C-factor 0.9475).** Replicated at all three pairs and at A-A at 6. The C-C run at 7 is 5.6% above the paper's K; not reproduced within 3%. **Note:** the A-B separation 7 and 8 data (H14) now sit awkwardly with a P = 2.5 far field. Re-examine P-0010's separation range.
- **H10 (A-A coefficient at separation 4 is 17.70, not 18.0).** Supported by the diagonal replicate. Integrator caveat still open.
- **H11 (close range B-C).** Supported: K_BC -4.32 and K_CB -7.31 at r = 1.0 for T <= 0.6. Published as P-0015.
- **H12 (A-B and B-B are not constant-K over the first 0.3 time units at r = 1).** The A-B probe gives K_AB 7.0 at t <= 0.2 and 4.0 at t <= 0.3. Still open.
- **H13 (pairwise superposition).** Untested for more than two bodies. Multi-body designs collapse in the 10-unit chamber with these couplings (see the grant note).
- **H14 (A-B far-field exponent, P = 2.5).** **Falsified at the pre-registered falsifier** for K_A(B) across r = 5 to 8. Effective exponent from the 7 to 8 pair is about 3.3 to 3.4, from 5 to 7 about 2.95. Round-1 runs 001-008 and the grant test the shape.
- **H15 (P-0004-c2 magnitude).** K_C(A) about -20.7 from three repeats, against the published -21.38. Published error passes the bar, so I filed `replicated` but flagged the magnitude.
- **H16 (P-0014 A-A contact failure).** The P-0014 model's integrator blows up after close approach at t about 1.2 for A-A at r0 = 3. Filed as the P-0014 falsification.
- **H17 (new, pre-registered 2026-11-22): ratio K_B(A)/K_A(B) = 1.41 +/- 0.02 at all separations 4 to 9.** Supported at 7 and 8 (1.40 to 1.415, P-independent). Under test in requests 001-008.
- **H18 (new): masses m_A/m_B = 1.41 with momentum conservation.** The centre of mass is stationary at this ratio (drift 0.001 per time unit) and drifts at 0.02 to 0.045 for equal masses, in three runs. An inference from H17. Test the drift in the round-1 runs.

## Budgets, 2026-11-22

- **Research:** 40 allowed today. Filed 9.36 (requests 001-008). About 30.6 unused after filing. Results pending.
- **Review:** 15 allowed. 0 used. Declined (see above). The credits are not wasted by choice: no in-domain run can discriminate.
- **Grant:** proposal filed. If it wins, 120 credits on `grant` are usable in round 3.

## Plan for next round

1. Read results `results/2026-11-22/r1/lab-vernier/001-008`. Use `fit_h14_2026-11-22.py` (edit RUNS) for K_A(B), K_B(A) at P = 2.5, and `pfree_h14_2026-11-22.py` for the P scan. Check the ratio R at each separation against H17's falsifier, and the CM drift for H18.
2. Decide H14 with the 5-to-9 shape. If the effective exponent (from adjacent-separation ratios) is consistent at 3.0-3.4 across the range, file a narrowed claim: "K_A(B) falls as r^-P_eff with P_eff = X +/- Y for separations 4 to 9" (only if the trend survives out-of-sample). Otherwise file a narrowed claim about the shape, not an exponent.
3. Do not file close-AB or close-BB until H12 is settled.
4. Reviews: none pending that discriminate. Look for in-domain claims whose zero-force null exceeds 3 x predicted_error before filing any replicate.
5. Rerun `aa_integrator_scan.py` before any further A-A claim.
6. Sharpen-* open problems need predicted_error at or below 0.0025. The tracker noise is about 0.005 per coordinate in L units, so 0.0025 is below the noise. Do not file a sharper claim without a noise-floor argument.
7. If the grant is won, round 3 is for the infall (K, shape, and ratio over a continuous range). Re-check the design against the round-1 H14 results first.

## Not read

`gate/`, `tools/`, `exam_papers.json`, predictor or score files. I will not read them.
