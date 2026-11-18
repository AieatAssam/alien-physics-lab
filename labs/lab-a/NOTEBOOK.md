# LAB-A notebook

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted.

## Budget ledger

### 2026-11-17 (closed)
- Research allowance 40, used 23.3 (ledger, rounds 1-3). Review used 6.0 (ledger).

### 2026-11-18
- Research allowance 40. Round 1 (r1, requests 001-013): 14.54 used, results all in (16 ok). Round 2 (r2, requests 001-007): 7.72 planned, not yet run. Planned total 22.26; unused after plan 17.74.
- Review allowance 15. Round 1 review (r1/014-016, cites P-0002): 6.20 used. Unused 8.80. No review requests this round.
- Every cost in the 16 round-1 results equals `1 + 0.02 N T` (checked, see below). Cost budget was checked against the ledger, and the ledger matches the result costs.

## Established

### Cost constant (H3): supported at N = 1, 2, 16
- k = 0.02. All 16 round-1 results match `1 + 0.02 N T`, including r1/013 (N = 16, T = 1, cost 1.32).

### Tracker noise: about 0.05 per coordinate
- Round 1 residual rms 0.047-0.053 on every pair and lone run that fits its model (r1/001, 002, 005, 010-012, 014-016). Unchanged from earlier rounds.

### No decays or census changes observed
- Round 1: 0 census events in all 16 runs (pairs to T = 4, lone C to T = 100, 16-particle run to T = 1). Round 3 lone A (T = 100) also none. This supports "no decay seen", for the runs made. It is not a general claim.

### Free flight with specular walls (H1, H2, H6): supported
- Species A: P-0001 domain, r2/001-003 and r3/011-014 (speeds to 7.8, T up to 100, corner hit).
- Species C: P-0002 scope (speed 3.6, 40 units) and wider edge tests (round 1 review, r1/014-016): speed 8.6 over 40 units, corner hit from (8,8) at v (3,3) over 20 units, and speed 0.22 over 100 units. Residual rms 0.048-0.052, means below 0.004, no drift, no events.
- Species B and C free motion (speed 1, 12 units): consistent with the same reflected-line predictor (r3/009-010).

### Pair force at separation 5, species-dependent (H8 refuted)
Per-particle coefficients K in acceleration = K / r^2.5 (time and chamber units), fit with P = 2.5 at r = 5, T = 2, pairs at rest. Positive means attraction.

| pair | particle | K | runs | rms |
|---|---|---|---|---|
| A-A | A (on A) | 18.0 | r3/005, 006 (repeat agrees: 18.18, 17.87) | 0.050 |
| A-B | A (on B) | 9.0 | r1/001, 002 (8.81, 9.16) | 0.052 |
| A-B | B (on A) | 12.35 | r1/001, 002 (12.41, 12.28) | 0.052 |
| A-C | A (on C) | -8.6 | r1/005 (single run) | 0.048 |
| A-C | C (on A) | -21.4 | r1/005 (single run) | 0.048 |
| B-B | B (on B) | 5.9 | r1/003 (single run) | 0.050 |
| C-C | C (on C) | 12.5 | r1/004 (single run) | 0.050 |

- A-B repeat agrees to 4%. The A-C pair repels: A moves 0.29 away and C moves 0.76 away over t = 2, against noise 0.05 per coordinate. B-B and C-C each come from one run (repeats queued as r2/003-004).
- The raw data show the A-C sign clearly, but my earlier fit that allowed only positive K missed it (the A-C fit sat at the grid edge). Signed fits are the correct analysis.
- Interpretation (inference, not measurement): if the pair force obeys Newton's third law, m_B/m_A = 8.99/12.35 = 0.73 and m_C/m_A = 8.59/21.38 = 0.40. These are masses inferred from forces, not measured masses. The A-A, A-B, B-B, A-C, and C-C coefficients are consistent with a factorised coupling g_ij = q_i q_j with q_A^2 = 18.0, q_A q_B = 9.0, q_A q_C = -8.6 (in units of m_A). That predicts q_B^2 = 4.5 (B-B measured 4.3) and q_C^2 = 4.1 (C-C measured 5.0). The C-C disagreement is 20%, and a single run. This is the open question.
- Prediction (r2/001-002): B-C pair at rest should repel, K_B(C) = -5.9 and K_C(B) = -10.7 (from g_BC = g_AB g_AC / g_AA = -4.29). A miss of more than about 20% rejects the factorisation.

### Far-field: the constant-K power law fails beyond separation 6 (P-0003 extrapolation)
Per-separation effective K at P = 2.5 (A-A, at rest):
- r = 4: 17.7 (r3/003-004, repeat agrees)
- r = 5: 18.0 (r3/005-006)
- r = 6: 16.5 (r3/007-008; per-run 16.3, 16.8)
- r = 8: 13.6 (r1/006-007; per-run 13.64, 13.60)
- r = 9: 11.7 (r1/008-009; per-run 11.76, 11.64)

The effective exponent rises with separation: local P_eff about 2.4 at r = 4.5, 3.0 at r = 5.5, 3.8 at r = 8.5. So a constant K with P = 2.5 holds near 4-5 and fails further out. The P-0003 predictor (K = 17.74, P = 2.5) gives residual rms 0.081-0.087 against the sep 8-9 runs, which is outside its noise band. That is outside P-0003's stated domain (3-6), so P-0003 is not falsified, but its power-law form does not extend.
- Power law (P = 2.5, shared K) and screened inverse square (K exp(-r/8)/r^2) fit r1/006-009 equally well (rms 0.047-0.053, same as noise). The far-field data do not separate the two forms.

### Isotropy at separation 4 (H10): supported
- A-A along the 45-degree diagonal (r1/010): K = 17.67. Along y (r1/011): K = 17.71. Horizontal (r3/003-004): 17.70, 17.70. All four agree to 0.2%.
- Caveat: separation-4 runs approach to about 0.3 by t = 2. The fit is sensitive there (see the integrator note). The agreement is good, but I weight it lower than the far-field result.

### Near field (separation 2, T = 0.5): not a usable test
- r1/012: K = 15.2, rms 0.047. T = 0.5 gives a small displacement, so K is poorly constrained. Not claimed.

### Lone-particle free motion and P-0002: replicated
- P-0002 review updated (`out/reviews/P-0002/lab-a.json`): replicated within its domain, and at speeds 0.22-8.6, durations to 100, corner hit (r1/014-016).

### P-0003 status
- Predictor reproduces its own evidence runs (r3/001-008) at noise level (rms 0.046-0.059, no events).
- Not falsified within its domain (separation 3-6, T up to 2). Its constant-K, P = 2.5 form is not valid beyond about 6 (far-field, above).
- Numerical note: near closest approach (separation 3-4, T = 2), the predicted trajectory is sensitive to K and to the integrator step. In my own integrator, K = 17.74 gives an unstable trajectory at step 0.001 (separation 4, diagonal), while K = 17.67 is converged across steps 0.005 to 0.0002. P-0003's own step (H = 0.002) gives noise-level fits on its runs. Other labs checking P-0003 at separation 3-4 should use a converged integrator and a step test.

## Papers and reviews
- P-0003 (lab-a, A-A pair, separation 3-6): published, unchanged. Domain stays as written.
- P-0004 (lab-a, species-dependent pair coupling at separation 5): `out/papers/P-0004/`. c1 (A-B) replicated in two runs. c2 (A-C repulsion) single run; the sign is firm, magnitudes await the repeat. Model reproduces r1/001, 002, 005 at noise level (in-sample).
- Reviews: P-0001 (lab-a, lab-c, earlier), P-0002 (lab-a, updated to replicated).

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C; speeds 0.2-8.6; durations to 100).
- H2 species does not change free motion: supported for B and C at speed 1, and for C at speeds 0.2-8.6 (P-0002 tests). Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 16.
- H4 no decay: no event in any round-1 run and in round 3 lone-A run. Supported for the runs made, not general.
- H5 no pairwise interaction: refuted (round 2).
- H6 wall reflection is elastic: supported (lone A, B, C).
- H7 pair attraction, central, P = 2.5, K = 17.7 for A-A over 3-6, T up to 2: supported inside 3-6. Constant-K P = 2.5 rejected beyond 6. Form not discriminated (power vs screened).
- H8 pair force is the same for all species pairs: REFUTED at separation 5. A-B, A-C differ from A-A (A on B 9.0 vs A on A 18.0; A-C repels). B-B and C-C are single runs (repeats queued).
- H9 (new, from P-0004 inference): coupling factorises as g_ij = q_i q_j with masses m_B = 0.73, m_C = 0.40 (m_A = 1). Test: r2/001-002 (B-C, predicted K_B(C) = -5.9, K_C(B) = -10.7). C-C mismatch of 20% is the first warning.
- H10 isotropy at separation 4: supported (K 17.67-17.71 across three directions).

## Round 2 (2026-11-18): requests written, results pending
Output: `out/requests/2026-11-18/r2/lab-a/001-007.json`. Generator: `out/labs/lab-a/analysis/make_round2_requests.py`.

| id | setup | T | cost | purpose |
|---|---|---|---|---|
| 001, 002 | B-C pair at rest, separation 5 | 2 | 1.08 each | prediction test of factorisation: B and C repel, K_B(C) ~ -5.9, K_C(B) ~ -10.7 |
| 003 | B-B pair at rest, separation 5 (repeat of r1/003) | 2 | 1.08 | confirm K_BB = 5.9 |
| 004 | C-C pair at rest, separation 5 (repeat of r1/004) | 2 | 1.08 | confirm K_CC = 12.5 (factorisation predicts 4.1) |
| 005 | A-C pair at rest, separation 5 (repeat of r1/005) | 2 | 1.08 | confirm repulsion magnitudes |
| 006, 007 | A-A pair at rest, separation 7, T=4 | 4 | 1.16 each | effective force between 6 (16.5) and 8 (13.6) |

Expected research total 7.72. Remaining unused after plan: 17.74.

## Decision rules for next session
1. Check r2 results when they arrive. Use `out/labs/lab-a/analysis/round1_2026-11-18.py` pattern for fits; use signed K (negative is repulsion) and per-particle coefficients for mixed species.
2. B-C (001-002): repeat must agree within 5% of predicted K_B(C) = -5.9 and K_C(B) = -10.7. Pass: factorisation holds for B-C. Miss by more than 20%: factorisation rejected, and P-0004 says so.
3. B-B (003) and C-C (004): if the repeats match r1 within 5% (5.9, 12.5), publish B-B and C-C coefficients as part of P-0004 (new claim). If C-C moves toward 4.1, the factorisation survives and my 5.0 was noise; if it stays at 5.0, factorisation fails for C-C.
4. A-C repeat (005): if magnitudes match (-8.6, -21.4) within 5%, P-0004 c2 is promoted to replicated. Otherwise narrow c2 to the sign only.
5. Far field (006-007): K_eff(7) between 13.6 and 16.5 means the drop is smooth. Compare the two forms with the per-run fit. If the sep-7 value does not fit a smooth curve through 6, 8, 9, the P=2.5 law is wrong in a way neither form captures.
6. Do not publish a separation-3 or separation-4 prediction without a converged integrator (step test). The fits there are sensitive.

## What would change my mind
- If the B-C prediction misses by more than 20%: the coupling is not a product of per-species factors. Then P-0004 is narrowed to the measured pairs only.
- If the repeat of A-C does not repel: c2 is wrong (single-run artefact), and I retract the sign.
- If far-field separation 7 falls on the P-0003 power-law curve (K about 17.7 times something smaller), the drop is not monotone and H7's domain has to shrink further.

## Self-criticism
- My earlier analysis fit only positive K, which hid the A-C repulsion for a whole round. Signed fits are now standard.
- The separation-4 and separation-3 fits are numerically sensitive near closest approach. The isotropy agreement and P-0003's separation 3-4 fits rest on that. I have not run a full step-convergence study for each run, only for run 010.
- The mass and charge reading is inference from Newton's third law, not a measurement. The C-C value already disagrees with it. I should not treat the factorisation as established until r2/001-004 are in.
- P-0004 c2 is a single run. I published it with the sign-only caveat in the paper; if the repeat fails, I will say so in a revision.
- The per-separation K values for 6 and 8-9 come from fits with a shared K over two runs each (r3 007-008; r1 006-009) at P = 2.5. The drift is real at noise level, but the local-exponent numbers are rough.

## Analysis code
All in `out/labs/lab-a/analysis/` (my own files). Pure python, no numpy (not installed).
- `round1_2026-11-18.py`: round-1 cost check; species, far-field, isotropy, near-field fits with a shared K; P-0003 residuals. Usage: `python3 -I round1_2026-11-18.py <repo_root>`.
- `make_round2_requests.py`: writes `out/requests/2026-11-18/r2/lab-a/001-007.json`.
- `round1_species_signed.py`: signed per-particle fits for A-B and A-C (runs 001, 002, 005) and P-0002 edge-test residuals (r1/014-016). Run output matches the notebook table.
- Older scripts in the repo under `labs/lab-a/analysis/` (fit_r1, fit_r2, pair_central_fit_r3, compare_model_r3, etc.) are unchanged. `compare_model_r3.py` is the residual tool used for P-0002 and P-0004 checks.
