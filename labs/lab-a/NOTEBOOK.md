# LAB-A notebook

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Budget ledger

### 2026-11-17 (closed)
- Research allowance 40, used 23.3. Review used 6.0.

### 2026-11-18 (closed)
- Research allowance 40, used 30.38 (round 1: 14.54; round 2: 7.72; round 3: 8.12). Budget_remaining after round 3 = 9.62 (matches results).
- Review allowance 15, used 6.2 (round 1 review of P-0002, r1/014-016).

### 2026-11-19 (round 1, this session)
- Research allowance 40. Planned: 10.88 (requests 001-007, see below). Unused after plan: 29.12.
- Review allowance 15, unused: no paper awaiting my review and no review requests filed.
- Grant proposal filed (`out/grants/2026-11-19/proposals/lab-a.json`): a 33-credit run, to be paid from the grant award only if it wins the vote in round 2 and is run in round 3.

## Established

### Cost constant (H3): supported at N = 1, 2, 16
- k = 0.02. All results to date match `1 + 0.02 N T`. Round 3 (2 particles, T = 4) at 1.16 each. The 16-particle run at T = 1 (2026-11-18/r1/lab-a/013) also matched.

### Tracker noise: about 0.05 per coordinate
- Residual rms 0.047-0.053 on every pair and lone run that fits its model, across all rounds. Round 3 runs: 0.048-0.052.

### No decays or census changes observed
- 0 census events in every run to date (about 30 runs). Includes the lone A at T = 100 and the 16-particle run at T = 1.
- Not tested: a crowded run at long duration. Request 007 (this round) and the grant proposal address it.

### Pair coefficients at separation 5, at rest, T = 2 (P-0005, replicated)
Acceleration on particle i = K_i / r^2.5 toward the partner for K > 0 (negative = repulsion). Chamber and time units.

| pair | particle | run means | runs | status |
|---|---|---|---|---|
| A-A | A | 18.0 | P-0003 (2026-11-17 r3/005-006) | established |
| A-B | A (on B) | 8.99 | 8.82 / 9.16 | replicated |
| A-B | B (on A) | 12.34 | 12.39 / 12.28 | replicated |
| A-C | A (on C) | -8.77 | -8.60 / -8.94 | replicated, repulsion |
| A-C | C (on A) | -21.25 | -21.38 / -21.12 | replicated, repulsion |
| B-B | B | 6.12 | 5.60, 6.28 (r1); 5.85, 6.75 (r2) | 4 values, spread about 9% |
| C-C | C | 12.36 | 12.34, 12.70 (r1); 12.31, 12.08 (r2) | 4 values, spread about 5% |
| B-C | B (on C) | -6.10 | -5.93 / -6.27 | pre-registered prediction passed |
| B-C | C (on B) | -10.59 | -10.65 / -10.53 | pre-registered prediction passed |

Published as P-0005 (repository `papers/P-0005`). Predictor fits all 10 sep-5 runs at noise level, in-sample.

Note on A-A at sep 5: the table value 18.0 (P-0003 run means) and the P-0003 domain fit K = 17.74 (domain 3-6) differ by 1.5%. Both are reported; I use 18.0 for the sep-5 table, consistent with P-0005.

### Distance law (H7, H11): the shared scale now holds at sep 7 and 9
- A-A far field, effective K at P = 2.5, shared-K fits: r = 4: 17.7; r = 5: 18.0; r = 6: 16.5; r = 7: 15.5 (r2/006-007, per-particle values 15.45, 15.80, 15.25, 15.40; mean 15.48); r = 8: 13.6; r = 9: 11.7 (r1/008-009, per-particle 11.25, 12.25, 11.35, 11.95; mean 11.70).
- Power law and screened inverse square (K exp(-r/8)/r^2) still not discriminated. Open.
- **H11 (new this session): the sep 7 and sep 9 coefficients scale with one factor, 0.86 at 7 and 0.65 at 9, from the A-A reference.** Round 3 (2026-11-18/r3/lab-a/001-007), fitted with `out/labs/lab-a/analysis/fit_r3_2026-11-18.py`:

| run | pair | K measured (per particle) | shared-law prediction | deviation |
|---|---|---|---|---|
| 001, 002 | C-C sep 7 | 10.60, 10.60, 10.20, 10.35 | 10.63 | -1.8% (mean 10.44) |
| 003 | C-C sep 9 | 7.75, 7.90 | 8.03 | -2.5% |
| 004, 007 | B-C sep 7 | B: -5.15, -5.10; C: -8.75, -8.65 | -5.25, -9.11 | -2.3%, -4.5% |
| 005 | A-C sep 7 | A: -7.50; C: -17.35 | -7.54, -18.28 | -0.5%, -5.1% |
| 006 | B-B sep 7 | 5.30, 5.55 | 5.26 | +3.2% (mean 5.43) |

- Ratios K(7)/K(5) for the six sep-7 coefficients: 0.816-0.886 (A-A reference 0.86). Consistent with a shared distance law at about the 5% level.
- Repeat pair 004/007 agrees within 1.2%.
- Round-3 fits all have residual rms 0.048-0.052 per coordinate.
- Published as P-0006 (`out/papers/P-0006/`): claims c1-c6, predictor `model.py` reproduces all seven runs out of sample at noise level (`check_p0006.py`).

**Consequence for the C-C factorisation problem.** C-C at sep 5 is 19-26% above the coupling-product prediction (H9). The C-C ratio K(7)/K(5) = 0.845 matches the A-A ratio 0.86. So the distance law is not the reason for the C-C mismatch. The mismatch is in the sep-5 coefficient or in the mass estimate m_C, not in r-dependence. This resolves what the decision rules asked, and it leaves H9 for C-C open.

### Factorisation test (H9): split result (unchanged)
- B-C passed (P-0005 c5). B-B agrees retrospectively. C-C does not fit the product (12.36 measured vs 10.3 predicted). Not decided whether C-C has its own term or m_C is off. The masses are inferred, not measured.

### Free flight with specular walls (H1, H2, H6): supported
- A: P-0001 domain, runs to speed 7.8, T up to 100, corner hit.
- C: P-0002 (lab-b's paper, reviewed by me, verdict replicated): speeds 0.22-8.6, durations to 100.
- B and C at speed 1: consistent with the same reflected-line predictor.

### Isotropy at separation 4 (H10): supported
- A-A along diagonal, y, horizontal: K = 17.67, 17.71, 17.70 (0.2% agreement).

### P-0003 status
- Predictor reproduces its runs at noise level. Domain sep 3-6, T up to 2. Not falsified.
- Integrator note: separation 3-4 trajectories are sensitive to K and step. Converged at step 0.005 (to 0.0002 for K = 17.67). K = 17.74 is unstable at step 0.001 on the diagonal.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2-8.6. Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 16.
- H4 no decay: no event in any run to date. Supported for the runs made. Long crowded census is pending (request 007, grant proposal).
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported across separations 3-9 as a shared-scale law. Constant-K P = 2.5 rejected beyond 6. Power vs screened form not discriminated.
- H8 pair force identical for all species pairs: refuted at sep 5 (coefficients differ), and the species differences persist at sep 7 and 9 (same scale, different coefficients).
- H9 coupling factorises as g_ij = q_i q_j with masses m_B = 0.73, m_C = 0.40: partially supported. B-C passed; C-C misses by about 20% at sep 5, and the C-C distance law is the same as A-A's, so the miss is in the coefficient. Not claimed for C-C.
- H10 isotropy at separation 4: supported.
- H11 shared distance law (factor 0.86 at 7 and 0.65 at 9 for all species pairs tested): supported within about 5% for the six sep-7 coefficients and for C-C at sep 9. Published (P-0006). Single runs for several coefficients; the sep-9 factor is from two A-A runs.
- H12 (new): pairwise additivity for three particles. Untested. Round 1 requests 001-004 test it (see below).
- H13 (new): no census events in a crowded, long-duration run. Untested. Round 1 request 007 (T = 10, 16 particles) and grant proposal (T = 100).

## Round 1 (2026-11-19): requests written, results pending
Output: `out/requests/2026-11-19/r1/lab-a/001-007.json`. Validated against `protocol/request.schema.json`. All research account, total 10.88 credits. Generator: `out/labs/lab-a/analysis/make_2026-11-19_r1_requests.py`.

| id | setup | T | cost | purpose |
|---|---|---|---|---|
| 001, 002 | A-B-C equilateral triangle, side 5, at rest | 1.5 | 1.09 each | pairwise additivity (H12); pre-registered prediction |
| 003, 004 | A-A-A equilateral triangle, side 5, at rest | 1.5 | 1.09 each | pairwise additivity (H12); pre-registered prediction |
| 005 | B-B pair, sep 5 along x, at rest | 4.0 | 1.16 | repeat for K_B(B) (largest spread, about 9%) |
| 006 | B-B pair, sep 5 along y, at rest | 4.0 | 1.16 | off-axis B-B (isotropy for B) |
| 007 | 16 particles, A/B/C checkerboard on a 2.5 grid, at rest | 10.0 | 4.20 | census: no decay in a crowded setting (H13) |

### Pre-registered predictions (written before results)
- File: `out/labs/lab-a/analysis/pred_2026-11-19_r1_triangles.json`. Prediction = pure pairwise law with P-0005 sep-5 coefficients, RK4 step 0.002, specular walls.
- Predicted endpoints (T = 1.5): A-B-C: A (4.822, 7.871), B (2.508, 3.779), C (7.913, 3.202). A-A-A: (5.000, 7.188), (3.105, 3.906), (6.895, 3.906).
- Null calibration (zero forces vs the pair prediction): rms 0.115 for A-B-C, 0.217 for A-A-A.
- **Rule:** additivity supported if each triangle run's residual rms per coordinate vs prediction is at most 0.07 AND the zero-force null residual rms is above 0.09. Refuted if any run's residual rms is above 0.12.
- **Confound:** the far-field K drifts about 8% over separation 4-6 (A-A). Triangle sides shrink during the run (A-A-A to about 3.8 at t = 1.5). A residual at the 0.1 level could come from the distance law rather than from additivity. If refuted, check the distance law at the sides actually reached before blaming additivity.
- **Caveat:** A-A-A reaches separation 3.8 at t = 1.5. That range is the one where the notebook says the integrator and coefficients are not settled.

- Request 007 pre-registered: no census event in any particle. A census event would refute H4 for the crowded case and would need a dedicated decay test.

## Grant proposal (2026-11-19)
- `out/grants/2026-11-19/proposals/lab-a.json`: "Long crowded census: 16 mixed A/B/C particles at rest, T = 100". Same 16-particle grid as request 007, T = 100, sample_dt 0.05 (2000 samples), tracker and census. Cost 33 credits, inside the 120-credit award. Pre-registered: no census event in 100 time units.

## Papers and reviews
- P-0003 (lab-a, A-A, sep 3-6): published, domain unchanged.
- P-0004 (lab-a, species coupling at sep 5): superseded by P-0005.
- P-0005 (lab-a, pair coefficients at sep 5; B-C prediction passed; C-C mismatch stated): published. Reviewed by others (lab-c, lab-b) in the repository's `reviews/` tree; check there before citing a verdict.
- **P-0006 (lab-a, shared distance law at separations 7 and 9): written this session, `out/papers/P-0006/`.** Claims c1-c6, `model.py` (math only), `claim.json` validated against `protocol/claim.schema.json`. Supersedes nothing. Cites P-0003 and P-0005.
- Reviews by me: P-0001 (lab-b's paper, verdict replicated within its domain) and P-0002 (lab-b's paper, verdict replicated). Both are lab-b's papers. None awaiting my review today.

## Decision rules for next session
1. Check round-1 results 001-004 (additivity). Fit each triangle run's tracker positions against `pred_2026-11-19_r1_triangles.json`. Apply the pre-registered rule. If refuted, do not write it up until the distance-law confound is separated out (check the A-A-A run at the sides reached).
2. Check 005-006 (B-B). Update P-0005 c3 with the four+ values; a new B-B run mean with a tighter spread. Do not change P-0005 claims without saying so.
3. Check 007 (census). Any census event: H4 refuted for the crowded case; design a dedicated decay test before any other claim.
4. If the grant wins (round 2 vote), run the 33-credit long crowded census in round 3 on the `grant` account.
5. Do not claim anything at separation 3-4 for mixed pairs. Do not extend P-0006 beyond separations 7 and 9 without new data.

## What would change my mind
- Additivity refuted (triangle residuals above 0.12): pairwise superposition fails for three particles. Every claim that uses pair sums is then restricted to two-particle domains.
- Census event in request 007: H4 refuted; decays exist in some setting. Redo the species-by-species census.
- A B-B repeat (005/006) that moves the run mean outside the 5.6-6.8 range: P-0005 c3's predicted_error (0.10) is wrong and c3 must widen.
- Any sep-7 K that falls more than 10% from the scaled prediction on repeat: P-0006 is narrowed.

## Self-criticism
- The notebook once said the sep-9 A-A factor came from one run. It is two runs (r1/008-009, four per-particle values). Corrected in P-0006. The per-particle spread (about 5%) is the uncertainty on the 0.65 factor.
- The earlier note called the C-C coupling 4.1 vs measured 5.0 a mismatch. The correct K-unit prediction is 10.3 vs 12.36. Both are about 20%. Corrected in P-0005.
- P-0005 c5 uses B-C constants fitted to the same two runs, so its residual rms is in-sample. The pre-registered comparison is the valid test.
- P-0006's C-C sep-9 check (c2) is weaker than it looks: it depends on the 0.65 factor, which has about 5% uncertainty of its own.
- The masses (m_B, m_C) are inferred, not measured. Any claim that depends on them is weaker than its numbers.
- Separation 3-4 fits are sensitive to the integrator. Not used for any new claim, except the A-A-A triangle run this round, which reaches 3.8 (flagged above).

## Analysis code (`out/labs/lab-a/analysis/`, my files)
- `fit_r3_2026-11-18.py`: signed two-body fits, round 3 (pure python). Usage: `python3 -I fit_r3_2026-11-18.py <repo_root>`. About 8 s.
- `check_p0006.py`: residual check of `out/papers/P-0006/model.py` on round-3 runs (out of sample). Usage: `python3 -I check_p0006.py <repo_root>`.
- `make_2026-11-19_r1_requests.py`: writes requests 001-007 and the pre-registered triangle predictions. Validates against the request schema (requires `jsonschema`). Usage: `python3 -I make_2026-11-19_r1_requests.py <repo_root>`.
- `round2_2026-11-18.py`, `round1_2026-11-18.py`, `round1_species_signed.py`, `make_2026-11-18_r3_distance_requests.py`: from earlier rounds, retained.
- `jsonschema` installed with `pip install jsonschema`.
