# LAB-A notebook

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted.

## Budget ledger

### 2026-11-17 (closed)
- Research allowance 40, used 23.3. Review used 6.0.

### 2026-11-18
- Research allowance 40. Used so far per ledger: 22.26 (round 1: 14.54; round 2: 7.72, results all in, all ok).
- Round 3 requests written this session (7 x 1.16 = 8.12, see below). Planned total 30.38. Unused after plan: 9.62.
- Review allowance 15, used 6.2 (round 1 review of P-0002, r1/014-016). Unused 8.8. No review requests this round; no paper awaiting my review.
- Cost constant re-checked on round 2: all 7 results equal `1 + 0.02 N T` (1.08 for N=2, T=2; 1.16 for N=2, T=4).

## Established

### Cost constant (H3): supported at N = 1, 2, 16
- k = 0.02. Round 1 (16 results) and round 2 (7 results) all match `1 + 0.02 N T`.

### Tracker noise: about 0.05 per coordinate
- Residual rms 0.047-0.053 on every pair and lone run that fits its model, across rounds 1-2.

### No decays or census changes observed
- 0 census events in every run to date: round 1 (16 runs), round 2 (7 runs), round 3 lone A (T = 100). Supports "no decay seen" for the runs made. Not a general claim.

### Pair coefficients at separation 5, at rest, T = 2 (replicated)
Acceleration on particle i = K_i / r^2.5 toward the partner for K > 0 (negative = repulsion). Chamber and time units. Per-particle signed fits, P = 2.5 fixed, two-parameter grid with refinement, RK4 step 0.005.

| pair | particle | run means | runs (r1 / r2) | status |
|---|---|---|---|---|
| A-A | A | 18.0 | P-0003 (2026-11-17 r3/005-006) | established (P-0003) |
| A-B | A (on B) | 8.99 | 8.82 / 9.16 | replicated |
| A-B | B (on A) | 12.34 | 12.39 / 12.28 | replicated |
| A-C | A (on C) | -8.77 | -8.60 / -8.94 | replicated, repulsion |
| A-C | C (on A) | -21.25 | -21.38 / -21.12 | replicated, repulsion |
| B-B | B | 6.12 | 5.60, 6.28 (r1); 5.85, 6.75 (r2) | 4 values, spread about 9% |
| C-C | C | 12.36 | 12.34, 12.70 (r1); 12.31, 12.08 (r2) | 4 values, spread about 5% |
| B-C | B (on C) | -6.10 | -5.93 / -6.27 (r2/001-002) | pre-registered prediction passed |
| B-C | C (on B) | -10.59 | -10.65 / -10.53 (r2/001-002) | pre-registered prediction passed |

- Published as P-0005 (`out/papers/P-0005/`, supersedes P-0004). Predictor `model.py` fits all 10 sep-5 runs at noise level (rms 0.047-0.052, in-sample).

### Factorisation test (H9): split result
Coupling product g_ij = K_i(j) m_i, with m_B = 0.73 and m_C = 0.40 inferred (not measured) from the A-B and A-C runs. Prediction g_BC = g_AB g_AC / g_AA = -4.3.
- **B-C: passed.** Predicted K_B(C) = -5.9, K_C(B) = -10.7. Measured -6.10 and -10.59 (3.6% and 1.5% off; 5% tolerance set in advance). Caveat: B-C constants in `model.py` are fitted to these same runs, so the test is the comparison, not a residual.
- **B-B: agrees, retrospectively.** Product predicts K_B(B) = 6.16, measured 6.12. The product was written before the B-B repeat, so this is a check, not a pre-registered test.
- **C-C: does not fit.** Product predicts K_C(C) = g_AC^2 / (g_AA m_C) = 10.3 (10.0-10.3 depending on which A-C run gives m_C). Measured 12.36, which is 19-26% high. This is at or past my 20% threshold. My earlier note compared g_CC (5.0 measured) with 4.1, which is the same mismatch in coupling units. Both are about 20%.
- Interpretation: the product works for B-C and B-B, but not for C-C. Either C-C has its own term, or the mass estimate for C is off. The mass estimate comes from one pair of runs. Not decided.

### Distance law: A-A far field (H7), separation 3-9
Effective K at P = 2.5, shared-K fits to A-A pairs at rest:
- r = 4: 17.7; r = 5: 18.0 (repeat agrees); r = 6: 16.5; r = 7: 15.5 (r2/006 15.62, r2/007 15.34); r = 8: 13.6; r = 9: 11.7.
- Smooth monotone decline. Effective exponent rises with separation. A constant K with P = 2.5 holds near 4-5 and fails beyond 6, as found before.
- Power law and screened inverse square (K exp(-r/8)/r^2) were equal on r1/006-009. Round 2 adds sep 7 (15.5), which lies between sep 6 and sep 8 as a smooth curve should. It does not separate the two forms.
- P-0003 (domain 3-6, K = 17.74) is not affected by the drop; its domain stays as written.

### Free flight with specular walls (H1, H2, H6): supported
- A: P-0001 domain, runs to speed 7.8, T up to 100, corner hit.
- C: P-0002 (lab-b's paper, reviewed by me): speeds 0.22-8.6, durations to 100, corner hit. Residuals 0.048-0.052, no drift.
- B and C at speed 1 (12 units): consistent with the same reflected-line predictor.

### Isotropy at separation 4 (H10): supported
- A-A along the diagonal (r1/010): K = 17.67; along y (r1/011): 17.71; horizontal (r3/003-004): 17.70. Agreement 0.2%.
- Caveat: fits near closest approach are sensitive to the integrator. Weighted lower than the far-field result.

### P-0003 status
- Predictor reproduces its runs at noise level. Not falsified within its domain (sep 3-6, T up to 2).
- Numerical note: separation 3-4 trajectories are sensitive to K and step. My integrator is converged at step 0.005 to 0.0002 for K = 17.67; K = 17.74 is unstable at step 0.001 on the diagonal. Others checking P-0003 near sep 3-4 need a step test.

## Papers and reviews
- P-0003 (lab-a, A-A, sep 3-6): published, domain unchanged.
- P-0004 (lab-a, species coupling at sep 5): superseded by P-0005.
- P-0005 (lab-a, pair coefficients at sep 5 for A, B, C; B-C prediction passed; C-C mismatch stated): written this session, `out/papers/P-0005/`. Claims c1-c5, evidence 2026-11-18/r1 and r2 runs. Validates against `protocol/claim.schema.json`.
- Reviews: P-0001 (lab-a and lab-c), P-0002 (lab-b's paper; my review by lab-a, verdict replicated).

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2-8.6. Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 16.
- H4 no decay: no event in any run to date. Supported for the runs made.
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5, K = 17.7 (A-A) over 3-6: supported inside 3-6. Constant-K P = 2.5 rejected beyond 6. Sep 7 gives K = 15.5, smooth. Form (power vs screened) not discriminated.
- H8 pair force identical for all species pairs: refuted at sep 5 (A-B, A-C, B-B, C-C, B-C all differ from A-A).
- H9 coupling factorises as g_ij = q_i q_j with masses m_B = 0.73, m_C = 0.40: partially supported. B-C passed a pre-registered test; B-B agrees; C-C misses by about 20%. Not claimed for C-C.
- H10 isotropy at separation 4: supported.
- H11 (new): the distance law (r-dependence) is the same for all species pairs, so the ratio K(7)/K(5) is species-independent. Untested so far. Test: round 3 (below).

## Round 3 (2026-11-18): requests written, results pending
Output: `out/requests/2026-11-18/r3/lab-a/001-007.json`. Generator: `out/labs/lab-a/analysis/make_2026-11-18_r3_distance_requests.py`. Validated against `protocol/request.schema.json`. All research account, all 2 particles, T = 4, sample_dt 0.04, cost 1.16 each, total 8.12.

| id | pair | sep | pre-registered prediction if the distance law is shared |
|---|---|---|---|
| 001, 002 | C-C | 7 | K_C(C) about 10.6 (sep-5 mean 12.36 x 0.86) |
| 003 | C-C | 9 | K_C(C) about 8.0 (x 0.65) |
| 004, 007 | B-C | 7 | K_B(C) about -5.2, K_C(B) about -9.1 |
| 005 | A-C | 7 | K_A(C) about -7.5, K_C(A) about -18.3 |
| 006 | B-B | 7 | K_B(B) about 5.3 |

The ratios 0.86 (sep 7) and 0.65 (sep 9) come from A-A (sep 7 mean 15.48, sep 5 18.0; sep 9 11.7).

## Decision rules for next session
1. Check r3 results. Fit with `out/labs/lab-a/analysis/round2_2026-11-18.py` pattern (signed, per-particle, P = 2.5 fixed). Adapt the file to r3 paths; it is pure python with no numpy.
2. Distance law (H11): if C-C and B-C at sep 7 and 9 match the same-law predictions within about 10% (using the ratio 0.86 and 0.65), the distance law is shared, and the C-C sep-5 excess is a coefficient issue, not a law issue. If C-C deviates from the A-A ratio at sep 7 or 9, the C-C distance law differs from A-A, and the factorisation is rejected for C-C. Narrow P-0005 and say so.
3. A-C (005) and B-C (004, 007): same rule. B-C repeat pair must agree with each other within 5%.
4. Do not claim anything at separation 3-4 for mixed pairs without a converged integrator.
5. Keep P-0005's c5 claim. It is a pre-registered test that passed. Do not extend the B-C result to other separations until r3 is in.

## What would change my mind
- If C-C at sep 7 is 0.86 x 12.36 (about 10.6): the distance law is shared. Then the C-C excess at sep 5 is a coefficient problem, and P-0005 c4 stands as a measured value with the factorisation rejected for C-C.
- If C-C at sep 7 is far from 10.6 (say more than 15%): the C-C distance law differs from A-A. The factorisation is rejected for C-C, and P-0005 must say the C-C coefficient is valid at sep 5 only.
- If the B-C repeat (r3/007) does not match r3/004 within 5%: the B-C result is noise-limited, and c5 is weakened.
- If any round-3 run has a census event: H4 is refuted, and decays need a dedicated test.

## Self-criticism
- My earlier fits allowed only positive K, which hid the A-C repulsion for a round. Signed fits are now standard.
- My earlier notebook compared the C-C coupling (g, 5.0 measured) with a prediction (4.1) and called it a mismatch, but also called the K-unit prediction 4.1, which was wrong: the K-unit prediction is 10.3. Both give about 20%. Corrected here.
- P-0005 c5 uses B-C constants fitted to the same two runs, so its residual rms is in-sample. The pre-registered comparison is the valid test; I state that in the paper.
- The masses (m_B, m_C) are inferred from Newton's third law and one A-B, one A-C run. They are not measured. Any claim that depends on them is weaker than its numbers.
- B-B and C-C per-particle values scatter by 5-9% across four values. I now treat the run spread as the error, not the single-run noise.
- Separation 3-4 fits are sensitive to the integrator. Not used for any new claim.

## Analysis code
All in `out/labs/lab-a/analysis/` (my files). Pure python, no numpy.
- `round2_2026-11-18.py`: signed per-particle pair fits for all sep-5 runs (r1 and r2), shared-K far-field fits, and a dt convergence check. Usage: `python3 -I round2_2026-11-18.py <repo_root>`. About 25 s.
- `make_2026-11-18_r3_distance_requests.py`: writes `out/requests/2026-11-18/r3/lab-a/001-007.json`. Re-run safe (identical output).
- `check_p0005.py`: residual check of `out/papers/P-0005/model.py` on the ten sep-5 runs. Usage: `python3 -I check_p0005.py <repo_root>`.
- `round1_2026-11-18.py`, `round1_species_signed.py`: round-1 cost check and round-1 fits (copied from the repo's `labs/lab-a/analysis/`).
- Older lab scripts copied from `labs/lab-a/analysis/` (`make_round1_requests.py`, `make_round2_requests.py`, `fit_r1.py`, `pair_*.py`, `compare_model_r3.py`, and others). `make_round3_requests.py` is the earlier 2026-11-17 round-3 generator: do not run it for 2026-11-18, it writes to the 2026-11-17 directory.
- Validator: `jsonschema` installed with `pip install jsonschema` (needed for the repo tests too).
