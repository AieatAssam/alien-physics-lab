# LAB-B notebook

Persona: bold theorist. Rule I hold myself to: a striking law only after a discriminating run supports it, and stated with its domain.

Last updated: 2026-11-18, round 3 (round-3 requests written, results pending; P-0003 review written).

## Season facts (measured)

- Season 1, species in use: A, B, C (`protocol/season.json`). Chamber [0, 10]^2.
- **Cost constant k = 0.020.** Confirmed on all 21 round-2 results (N=2 at T=1, 2, 5, 10; `1 + 0.02·N·T` exact).
- Cost is independent of `sample_dt`. Requests with `duration/sample_dt = 2000` (`dt = T/2000`, exact in float for T=1, 2) return 2001 samples including t=0.
- **Tracker noise: sd about 0.05 per coordinate.** Confirmed again: rms residuals of 0.049–0.052 across every fit that is inside its valid window.
- **Census: no decay, appear or vanish events** in any run so far (round 2: 21 of 21 with 0 events).

## Main results so far

### 1. Pair coefficients (per-particle, P = 2.5 fixed, pre-collision windows)

Fit: `out/labs/lab-b/analysis/pair_fit_integrated.py`. Model: particle i accelerates toward partner j with magnitude K_i(j)/r^2.5. Fits K_0, K_1 to tracker positions for t ≤ tmax. Raw output: `out/labs/lab-b/analysis/fits_r2_2026-11-18.txt`.

| Pair | sep 1.5 (t≤0.3) K_i(j) | sep 3 (t≤1.0) K_i(j) | Source |
|---|---|---|---|
| A on A | 13.80 (13.55, 14.05) | 17.67 (17.75, 17.59) | r2/004, r2/010 |
| B on B | 4.83 (4.86, 4.80) | 6.33 (6.34, 6.33) | r2/005, r2/011 |
| C on C | 11.19 (11.42, 10.95) | 13.20 (13.19, 13.22) | r2/006, r2/012 |
| A on B | 6.92 | 8.97 | r2/007, r2/013 |
| B on A | 9.69 | 12.55 | r2/007, r2/013 |
| A on C | −7.14 | −8.98 | r2/008, r2/014 |
| C on A | −17.03 | −21.45 | r2/008, r2/014 |
| B on C | −4.42 | −6.41 | r2/009, r2/015 |
| C on B | −8.20 | −10.66 | r2/009, r2/015 |

- All fits have residual rms 0.049–0.051 per coordinate (noise level).
- **Window stability (sep 1.5, AA, r2/004):** K = 12.95/14.89 (t≤0.2), 13.55/14.05 (t≤0.3), 13.19/13.36 (t≤0.4). Uncertainty about 4% on AA. AB is less stable: K_A(B) = 6.14, 6.92, 6.95 for the same windows, so about ±10%.
- **Cubic early-window fits** (`early_accel_fit.py`, round 2 ancestor tool) are **not reliable** for sep 1.5 pairs: the jerk term is degenerate with acceleration, and the two particles in a like-species pair get different accelerations (AA: 3.95 vs 5.17). Use `pair_fit_integrated.py` instead. Older numbers in previous notebooks from cubic fits are superseded.

### 2. Masses from Newton's third law (m_i K_i(j) = m_j K_j(i))

| Ratio | sep 1.5 | sep 3 | Note |
|---|---|---|---|
| m_B/m_A | 0.714 | 0.715 | consistent across separations |
| m_C/m_A | 0.419 | 0.419 | consistent across separations |
| m_C/m_B | 0.539 | 0.601 | from BC pair; 0.587 expected from the AB and AC ratios. Sep 1.5 BC is 9% off, sep 3 is 2.5% off |

So m_A : m_B : m_C ≈ 1 : 0.715 : 0.42. Agrees with the old rough values (0.7, 0.4). Equal-species pairs (A-A, B-B, C-C) give equal per-particle coefficients, as Newton's third law requires for equal masses.

### 3. Rank-one test (H10, masses cancel)

Hypothesis (charge-product form with a single pair function): F_ij = m_i K_i(j) and F_ij² = F_ii F_jj imply **K_i(j)·K_j(i) = K_i(i)·K_j(j)** (masses cancel).

| Pair | ratio at sep 1.5 | ratio at sep 3 | Verdict |
|---|---|---|---|
| A-B | 1.01 | 1.005 | **holds at both separations** |
| A-C | 0.79 | 0.83 | **fails by 17–21%** at both separations |
| B-C | 0.67 | 0.82 | **fails by 18–33%** at both separations |

- Error estimate: about 4% per coefficient, so about 8% on a four-coefficient ratio. Under that estimate the violations are about 2–4σ (A-C 2.1σ and 2.6σ; B-C 2.3σ at sep 3 and 4σ at sep 1.5). The violations are consistent across two separations, which argues against a noise artefact but does not rule one out. The 8% is my estimate, not a measured one; the sep-2 replicate is the real test.
- **Current reading:** the simple product rule (A and B behave as a single charge pair; C is a different coupling) is not supported for pairs involving C. The AB pair is consistent with it. The sign pattern from round 2 is unchanged (AA, AB, BB, CC attract; AC, BC repel).
- Not a published claim yet. A replicate at separation 2 (round 3) is needed first.

### 4. Radial dependence of the AA coefficient (challenges the power law below r=3)

| r | K_AA | Source |
|---|---|---|
| 1.0 | 10.7 (t≤0.2 only; collision by 0.3) | r2/016 |
| 1.5 | 13.8 | r2/004 |
| 2.0 | 15.4 (t≤0.3); 15.6 (t≤0.5) | r2/017 |
| 3.0 | 17.7 | r2/010 |
| 4.0 | not yet fitted (see review of P-0003, r2/018) | |
| 6.0 | not yet fitted (r2/021 matches P-0003 at noise level) | |

- K rises from 13.8 (r=1.5) to 17.7 (r=3). Effective exponent between 1.5 and 2 is about 2.1, and between 2 and 3 about 2.2. So **P = 2.5 is not right below r≈3**. P-0003 fits K=17.7 over 3–6; my data say the coefficient is still changing below 3. This is the P-0003 "power law vs screened form" caveat showing up at short range. Not a claim yet, but it bears on P-0003's domain edge and on P-0004.

### 5. Duration and near-collision: the T=10 outlier is not a duration effect

The round-2 duration test (`out/labs/lab-b/analysis/compare_runs.py`, rms per coordinate in windows):

| Pair of runs (same initial state, A at (4.5,5), B at (5.5,5), at rest) | 0–0.25 | 0.25–0.6 | 0.6–1.0 |
|---|---|---|---|
| T1 family (r1/001–003) pairwise | 0.06–0.09 | 0.05–0.08 | 0.06–0.07 |
| T10 new (r2/001, T=10, dt .005) vs T1 family | 0.06–0.07 | 0.08 | 0.07 |
| T10 old (11-17 r2/003, T=10, dt .05) vs T1 family | 0.07 | 0.16–0.18 | 0.29–0.33 |
| T10 new vs T10 old | 0.05 | 0.17 | 0.30 |
| T5 (r2/002, dt .0025) vs T1 family | 0.07 | 0.24 | 0.28 |
| T2 (r2/003, dt .001) vs T1 family | 0.07 | 0.29 | 0.57 |

- **Duration is not supported as the cause.** The new T=10 run matches the T=1 family through t≈1. The old T=10 run does not. Same duration and state, different dt, different trajectory. So T is not the cause; the outcome after a close pass is not a function of T alone.
- **The divergence starts at the first near-collision.** Separation for A-B at sep 1 falls to 0.01–0.1 at t≈0.3–0.5 in every run (`analysis` output, separation table). Runs stay together through the first pass and separate afterwards at 0.2–0.3 rms within 0.5 time units. This is sensitivity to tiny differences in a singular encounter (the force diverges as r→0), not measurement noise.
- **Claim candidate (not yet published):** trajectories are reproducible at noise level up to the first approach to r≈0.3; after that, runs from the same state disagree at 0.2–0.3 rms within 0.5 time units. Evidence: r1/001–003, r2/001–003, r2/003 (11-17). Needs one more controlled test (same state and T, dt = 0.001 vs 0.01) before publication; the round-3 sep-2 runs will not show it because they stay apart.
- Implication for other labs' fits: **anything fitted after a close approach (r < 0.3) is not reproducible**, including P-0003's closest-approach runs (to r≈0.14 at t=2) and my round-2 r2/003 power-law fits. Withdrawn from my own analysis.

### 6. Review of P-0003 (lab-a, "A-A attraction, K/r^2.5, separation 3–6")

Written: `out/reviews/P-0003/lab-b.json`, verdict **narrowed**, proposed domain species A, r_range [0.5, 6.0], max_particles 2. Evidence: 2026-11-18/r2/lab-b/004, 010 (research), 018–021 (review).

- Predictor: `papers/P-0003/model.py` run on each setup (`out/labs/lab-b/analysis/compare_model.py`).
- Position/orientation: rms 0.051–0.052 per coordinate before first approach to r=0.5 for 018 (sep 4, along x at y=1), 019 (sep 4, diagonal), 020 (sep 3, vertical near the right wall). 021 (sep 6, along x at y=2): rms 0.051 over the full T=2, no drift.
- Constant at sep 3: K0=17.75, K1=17.59 (r2/010). Replicates K=17.7.
- Narrowing: after the pair first reaches r<0.5 (t=1.97 for 018, 019; t=1.20 for 020), the predictor departs by rms 0.70 (018), 1.01 (019), and blows up (about 800) in 020. The observed pair in 020 passes within 0.017 at t=1.25, and the observed trajectory stays smooth, so the fault is in the predictor (fixed-step RK4 on a singular force) and possibly in the law, and I cannot separate them.
- This means P-0003's claim "fits at noise level for durations 1–2" fails for any run in which the pair closes within that time. The proposed domain stops at separation 0.5 for this reason.
- Also see section 4 (K rises below r≈3).

### 7. Round-2 review requests (cites P-0003): spend and status

- 018–021 (review account): cost 4.32. Done (above). Review credits remaining after round 2: 10.68.

## Hypotheses (status after round 3 planning)

- **H1, free flight of a lone A particle:** supported (r1/001). Published as P-0001 (accepted).
- **H5, free flight of a lone C particle, long run:** supported (r2/005). Published as P-0002 (lab-a review: replicated, narrow scope).
- **H2, pair interaction is species-pair specific with signs:** supported. Signs: AA, AB, BB, CC attract; AC, BC repel. All six sign pattern holds at sep 1.5 and 3.
- **H3, central pair force:** supported for A-B (r2/004 family). Still not tested for C pairs off-axis.
- **H4, distance dependence:** supported qualitatively for every pair, but **the power law P=2.5 fails below r≈3** (section 4). The effective P between 1.5 and 3 is about 2.1–2.2.
- **H6, A-C repulsion falls off with separation:** supported at sep 1.5, 3 (K_A(C) −7.1, −9.0), and at 5 in P-0004 (−8.6). The shape is not yet resolved.
- **H7 (C repels everything):** falsified (CC attracts, r3/002 of 11-17).
- **H8 (short-range r<1 pair dynamics central power law):** not supported. Close approaches are not reproducible (section 5).
- **H9, simulator reproducibility and sample_dt-independence:** sample_dt-independence supported at T=1 (dt 0.005–0.05). Duration is **not** the cause of the T=10 outlier (section 5). Post-near-collision non-reproducibility is the working explanation.
- **H10, rank-one product rule (K_i(j) K_j(i) = K_i(i) K_j(j)):** supported for A-B at sep 1.5 and 3 (1.01, 1.005). **Violated for A-C and B-C** at both separations (0.67–0.83). Needs replicate at sep 2 (round 3).
- **H11 (new), pairwise additivity:** untested. Pre-registered prediction for the equilateral three-body run below.

## Pre-registered prediction: three-body additivity (request 2026-11-18/r3/lab-b/006)

Equilateral triangle, side 3, at rest: A (4,4), B (7,4), C (5.5, 6.598). Prediction = sum over partners of K_i(j)/3^2.5 along unit vectors, using the sep-3 coefficients above (`out/labs/lab-b/analysis/predict_threebody_r3.py`, run before results):

| Particle | predicted initial acceleration |
|---|---|
| A | (+0.287, −0.499), \|a\| = 0.576 |
| B | (−0.600, −0.356), \|a\| = 0.697 |
| C | (+0.346, +1.784), \|a\| = 1.817 |

- **Falsified if** the fitted initial acceleration (pre-collision fit, t≤0.6 window, as for the pair fits) differs from the prediction by more than 0.05 in any component, or by more than 10% in magnitude. Additivity is a bold claim: if it holds it lets the lab-a predictor (pairwise sum) extend to N>2.
- **Caveat:** K_i(j) at sep 3 is used at distance 3 for all three pairs, so this tests additivity at fixed distance only. Equilateral symmetry means the three pairs cannot be distinguished by distance; that is intended, but it means the prediction does not test distance-dependence within a triangle.

## Round 3 plan (2026-11-18, r3), submitted

Files: `out/requests/2026-11-18/r3/lab-b/001–016.json`. Research total 11.66 of 18.64. Review total 5.40 of 10.68. All validate against `protocol/request.schema.json` (checked with jsonschema). Sample count 2000 per run (dt = T/2000).

| Request | Account | Setup | Cost | Question | Prediction / falsification |
|---|---|---|---|---|---|
| 001–005 | research | sep 2 pairs at rest on the x-axis, T=1: BB, CC, AB, AC, BC | 5.20 | Rank-one ratio at a third separation. C-pair violation replicated at 2? | AB ratio within 0.94–1.06. AC, BC ratio off by more than 10% (replicate). Falsified if AC and BC ratios are within 10% of 1 at sep 2 |
| 006 | research | equilateral A,B,C side 3, T=1 | 1.06 | Pairwise additivity | Table above. Falsified if off by >0.05 per component |
| 007–011 | research | sep 4 pairs on the x-axis, T=2: BB, CC, AB, AC, BC | 5.40 | Coefficients at sep 4 (P-0003 and P-0004 domain edge) | Same rank-one pattern as at sep 3; K_AB and K_AC at sep 4 near the sep-3/5 values (about 9 and 8.6–9.0) if the coefficient is constant for r ≥ 3 |
| 012 | review (cites P-0004) | A-B at sep 5, (2.5,5)/(7.5,5), T=2 | 1.08 | Replicate P-0004 c1: K_A(B)=9.0, K_B(A)=12.3 | Replicated if within 10% of P-0004 values |
| 013 | review (cites P-0004) | A-C at sep 5, T=2 | 1.08 | Replicate P-0004 c2: K_A(C)=−8.6, K_C(A)=−21.4 | Replicated if within 10% |
| 014 | review (cites P-0004) | B-C at sep 5, T=2 | 1.08 | P-0004's own prediction: K_B(C)=−5.9, K_C(B)=−10.7 | Miss by >20% rejects the factorisation |
| 015 | review (cites P-0004) | A-B at sep 3, (2.0,5)/(5.0,5), T=2 | 1.08 | Domain edge: does the sep-5 coefficient hold at 3? My sep-3 AB is K_A(B)=8.97, K_B(A)=12.55 | Narrowed if sep-3 values differ from sep 5 by >10% |
| 016 | review (cites P-0004) | A-C at sep 3, (2.0,5)/(5.0,5), T=2 | 1.08 | Domain edge for repulsion; my sep-3 AC: K_A(C)=−8.98, K_C(A)=−21.45 | As 015 |

Budget after the planned round: research 18.64 − 11.66 = 6.98 unspent (kept for follow-ups after results). Review 10.68 − 5.40 = 5.28 unspent.

Predictions are written in the request purposes too. Analysis after results:
1. `pair_fit_integrated.py` for 001–005, 007–011 (tmax 0.3 for sep 2, tmax 0.6 for sep 4 — check min separation first), and 012–016 (tmax 1.0 for sep 5, 3).
2. Rank-one ratio per separation, mass ratios.
3. Three-body fit for 006 vs `predict_threebody_r3.py` table.
4. Review of P-0004 with verdicts per claim, written only from 012–016. Expected outcomes from my data: c1 (AB) and c2 (AC) replicate at sep 3 already (K_AB, K_AC within 4%), so the review's likely verdict is **narrowed** to separations 3–5 unless sep-5 runs disagree. The B-C prediction (K_B(C)=−5.9) is at risk: my sep-3 value is −6.41, a 9% gap, and the factorisation has already failed for A-C and B-C (section 3). Expect a miss unless the sep-5 result differs.

## Papers

- **P-0001** (lab-b, accepted). Lone species-A free flight, specular walls. Replicated by lab-a for x=10 and y=0 walls at speed 1.0. Domain as stated covers all walls; lab-a tested two of them. Will narrow if others fail.
- **P-0002** (lab-b, submitted). Lone species-C free flight, 40 time units, walls. Replicated by lab-a on a narrow scope (speed 1.0 to 8.6, duration up to 100 per lab-a's review, corner hits).
- **No new paper this round.** Candidate claims ready but not yet publishable:
  - Pair coefficient table (section 1) with mass ratios (section 2): solid for sep 1.5 and 3; publish after round-3 sep-2 data.
  - Rank-one result (section 3): A-B holds; C pairs violate. Publish after sep-2 replicate (a violation at 3 separations would be a falsifiable claim others can break).
  - Post-near-collision non-reproducibility (section 5): needs the controlled dt test first.
  - AA coefficient rising below r=3 (section 4): needs sep 4 and 6 fits (r2/018, r2/021, and round-3 007).

## Reviews written by me

- `out/reviews/P-0003/lab-b.json`: **narrowed**, domain species A, r_range [0.5, 6.0], max_particles 2. Evidence 018–021, 010, 004.
- P-0004 (lab-a, A-B and A-C at sep 5): review requests 2026-11-18/r3/lab-b/012–016 queued. Review file to be written after results.

## Ledger

- Research 2026-11-17: allowance 40. Used 17.70.
- Research 2026-11-18: allowance 40. Round 1 used 3.12. Round 2 used 18.24. Remaining 18.64 before round 3. Round 3 planned 11.66 (requests 001–011). Remaining after round 3 plan: 6.98.
- Review 2026-11-18: allowance 15. Round 2 used 4.32 (018–021, P-0003). Remaining 10.68. Round 3 planned 5.40 (012–016, P-0004). Remaining after: 5.28.

## Analysis files (`out/labs/lab-b/analysis/`)

- `compare_runs.py <root> label=path ...`: windowed rms comparison of tracker trajectories on shared sample times. Used for the duration and divergence tables (section 5).
- `pair_fit_integrated.py <request> <result> <tmax> [P]`: two-body integrated fit of K_0, K_1 for an at-rest pair, RK4, pure Python. Primary magnitude tool. Residual rms about 0.05 when the window is valid. Slow (about 10 s for 600 samples, 2 min for 2000); run in background for long windows.
- `compare_model.py <model.py> <request> <result> [tmax]`: compares a paper's `predict(setup)` against tracker data, per particle, rms and mean residual.
- `fits_r2_2026-11-18.txt`: saved outputs of the pair fits and the window-sensitivity check.
- `make_round3_requests.py <repo_root>`: writes and budget-checks round-3 requests.
- `predict_threebody_r3.py`: pre-registered three-body additivity prediction.
- Older tools in `labs/lab-b/analysis/` (repo, not mine to edit): `early_accel_fit.py` (cubic early-window fit; **unreliable at sep 1.5**, see section 1), `determinism_windows_r1.py`, `r3_summary.py`, `r2_checks.py`.
- Environment: pure Python 3 with `python3 -I`; `jsonschema` installed for validation (repo tests use it). No numpy.

## Next session

1. Read round-3 results in `results/2026-11-18/r3/lab-b/`. Start with 001–005 (sep-2 rank-one) and 006 (three-body prediction). Those two decide whether the C-pair violation and additivity are claims.
2. Fit 007–011 (sep 4) and 012–016 (P-0004 review); write `out/reviews/P-0004/lab-b.json` per claim.
3. Fit r2/018 and r2/021 (AA at 4 and 6) with `pair_fit_integrated.py` at tmax 1.5 to finish the K(r) profile (section 4).
4. If the sep-2 rank-one violation for C pairs replicates, write P-0005 (pair coefficients at sep 2, 1.5, 3, 4, plus the rank-one result with its failure stated), with predictor and claim JSON. Claim domain: 2 particles at rest, r in [1.5, 4], T ≤ 1.
5. Controlled post-collision test (same state, dt 0.001 vs 0.01, T=2) before publishing claim section 5.
6. Budget: 6.98 research and 5.28 review credits will be spent after the round-3 plan; re-check the ledger before adding requests.
