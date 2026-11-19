# LAB-B notebook

Persona: bold theorist. Rule I hold myself to: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-19, round 1. P-0006 published. Reviews of P-0004 written. P-0005 review pending today's results. Requests for today written (see Round 1 plan).

## Season facts (measured)

- Season 1, species A, B, C (`protocol/season.json`). Chamber [0, 10]^2.
- **Cost k = 0.020**: cost = 1 + 0.02·N·T. Confirmed on all round-2 and round-3 results.
- Cost independent of sample_dt. 2000 samples per run at dt = T/2000 is fine.
- **Tracker noise sd ≈ 0.05 per coordinate.** Residual rms 0.049–0.051 in every fit within its valid window.
- **Census: no decay, appear or vanish events** in any run so far (0 events in round 2 and round 3).

## Round-3 results (2026-11-18), refit

Fits: `out/labs/lab-b/analysis/pair_fit_integrated.py`, outputs in `out/labs/lab-b/analysis/fit2_r3_*.txt`. Windows set by minimum separation from the samples. The first-pass fits (`fit_r3_*.txt`) used windows too short for r=2, 4, 5 and are superseded.

Per-particle coefficients K_i(j) (acceleration = K/r^2.5; positive = attraction):

| pair | r=2 (t≤0.6) | r=3 | r=4 (t≤2) | r=5 (t≤2) |
|---|---|---|---|---|
| K_B(B) | 5.49 (r3/001) | 6.33 (r2/011) | 6.48 (r3/007) | — |
| K_C(C) | 12.02 (r3/002) | 13.20 (r2/012) | 13.13 (r3/008) | — |
| K_A(B) | 7.89 (r3/003) | 8.95 (r2/013, r3/015) | 9.16 (r3/009) | 8.94 (r3/012) |
| K_B(A) | 11.05 | 12.58 | 12.92 | 12.58 |
| K_A(C) | −8.03 (r3/004) | −8.97 (r2/014, r3/016) | −9.06 (r3/010) | −8.72 (r3/013) |
| K_C(A) | −19.30 | −21.40 | −21.67 | −20.97 |
| K_B(C) | −5.69 (r3/005) | −6.41 (r2/015) | −6.42 (r3/011) | −6.34 (r3/014) |
| K_C(B) | −9.58 | −10.66 | −10.91 | −10.45 |
| K_A(A) | 15.6 (r2/017, single run, t≤0.5) | 17.67 (r2/010) | not mine (r2/018 unfitted) | — |

Residual rms 0.049–0.051 for every fit. Two independent runs at r=3 for A-B and A-C agree within 1%.

Findings:
- **Constancy for r=3–5:** K for A-B, A-C, B-C is constant within about 3%. So P=2.5 holds at r≥3 for these pairs. (Previous notebook's claim "P=2.5 fails below r≈3" is confirmed only for r<3.)
- **Below r=3 the coefficients fall** for A-B and A-C (7.9 at r=2 vs 9.0 at r=3). A-A rises from 13.8 (r=1.5) to 17.7 (r=3). These go in opposite directions, so there is no single short-range power law. Not claimed.
- **Mass ratios** (Newton's third law, m_i K_i(j) = m_j K_j(i)): m_B/m_A = 0.71 at r=2, 3; m_C/m_A = 0.42 at r=2–5; m_C/m_B = 0.59–0.61 at r=2–5 (expected 0.58 from the other two; 3% off). Same ratios at every separation, so this is a stable number, not a fit artefact.
- **Rank-one (H10):** A-B holds (1.02 at r=2, 1.01 at r=3). A-C and B-C fail at both (0.83 and 0.82). The violation replicates across two separations and is consistent with sep 1.5 (0.79, 0.67). Each ratio's uncertainty I estimate at about 5% (window spread), so the 17% deviation is about 3σ. **Published as P-0006-c2.**

## Three-body additivity (H11): PASSES

- Request 2026-11-18/r3/lab-b/006 (equilateral A,B,C, side 3, at rest), pre-registered prediction from sep-3 table.
- Integrated pairwise sum (`threebody_integrated_r3.py`) vs tracker: rms 0.049–0.051 per coordinate for all three particles, t≤1.0. Mean residuals ≤0.002.
- The earlier polynomial acceleration fits were ill-conditioned (quartic term); the integrated comparison is the valid test.
- Limits: one geometry, all distances 3, one run. **Published as P-0006-c3.**

## Post-collision divergence (H9, section from round 2)

- Trajectories from the same state reproduce at noise level until the first approach to r≈0.3; after that they split by 0.2–0.3 rms within 0.5 time units.
- Duration is not the cause of the round-2 T=10 outlier; the old run had a different sample_dt.
- **Controlled test queued today** (research 003–005): identical A-B state at sep 1, T=2. 003 and 004 are identical requests (reproducibility), 005 has sample_dt 0.01 (grid dependence). Claim is not published until these return.

## Papers

- **P-0001** (lab-b, accepted). Lone species-A free flight, specular walls.
- **P-0002** (lab-b, accepted; lab-a replicated narrowly). Lone species-C free flight, 40 time units.
- **P-0003** (lab-a). AA attraction K/r^2.5 at sep 3–6. My review: narrowed (species A, r in [0.5, 6], max 2). The predictor blows up after close approach (r<0.5), so the domain must stop there.
- **P-0004** (lab-a). AB and AC at sep 5. **My review: replicated** (`out/reviews/P-0004/lab-b.json`). Replicates at 5 (within 2.3%), holds at 3, and the B-C prediction passes (7.5% and −2.3%, tolerance 20%). Proposed domain species A,B,C, r in [3,5], max 2.
- **P-0005** (lab-a, supersedes P-0004). Claims c1–c5 at sep 5. Reviews of c1, c2, c5 are supported by my round-3 r3/012–014 (within 0.6–3.9%). c3 (B-B 6.12) and c4 (C-C 12.36) are pending today's review requests (001, 002). **Review file not yet written.**
- **P-0006** (lab-b, mine, published today). Claims: c1 constancy r=3–5 (3%), c2 rank-one A-B holds / A-C, B-C fail at r=2,3, c3 triangle additivity (one run). Predictor `out/papers/P-0006/model.py` reproduces 006 at noise.

## Round 1 plan (2026-11-19)

Requests in `out/requests/2026-11-19/r1/lab-b/` (validated against the schema; generator `out/labs/lab-b/analysis/make_round1_2026-11-19.py`):

| id | account | setup | cost | purpose |
|---|---|---|---|---|
| 001 | review (cites P-0005) | B-B, sep 5, T=2 | 1.08 | replicate c3 (6.12, within 10%) |
| 002 | review (cites P-0005) | C-C, sep 5, T=2 | 1.08 | replicate c4 (12.36, within 5%) |
| 003 | research | A-B, sep 1, T=2, dt 0.001 | 1.08 | post-collision reproducibility |
| 004 | research | same as 003 | 1.08 | reproducibility replicate |
| 005 | research | same as 003, dt 0.01 | 1.08 | sample-grid dependence |
| 006 | research | A,B,C triangle, sides A-B 3, B-C 4, A-C 5, T=1 | 1.06 | additivity, mixed distances (config 1) |
| 007 | research | A,B,C triangle, sides A-B 4, B-C 3, A-C 5, T=1 | 1.06 | additivity, mixed distances (config 2) |

Research total 5.36 of 40. Review 2.16 of 15.

**Pre-registration for 006 and 007 (written before results).** Predict each particle's initial trajectory by the pairwise sum with coefficients taken at each pair's own separation: K(3) for A-B side-3, K(4) for B-C side-4 and K(5) for A-C side-5 from the table above. Falsified if any particle's residual from the pairwise integration exceeds 0.05 per coordinate over t≤1.0 (noise-level mean residual ≤0.01). Predicted initial accelerations (P-0006 `model.py` table, computed 2026-11-19 before results):
- Config 1 (006): A (0.483, −0.128), B (−0.814, −0.200), C (0.229, 0.639).
- Config 2 (007): A (0.154, −0.096), B (−0.397, −0.410), C (0.306, 0.914).
Check the integrated trajectories with `compare_model.py out/papers/P-0006/model.py <request> <result> 1.0`.

**Grant proposal** (`out/grants/2026-11-19/proposals/lab-b.json`): four-body rectangle A(2,2), B(5,2), C(5,6), A(2,6), at rest, T=1, sample_dt 0.0005. Sides 3 and 4, diagonals 5. Pairwise prediction from the same table; falsified if any particle deviates by more than 0.05 per coordinate over t≤1.0.

## Reviews written by me

- `out/reviews/P-0003/lab-b.json`: narrowed, species A, r in [0.5, 6], max 2 (round 2).
- `out/reviews/P-0004/lab-b.json`: replicated, species A,B,C, r in [3,5], max 2 (round 3 evidence 012–016).
- P-0005: pending today's results from r1/001–002.

## Ledger

- Research 2026-11-17: allowance 40, used 17.70.
- Research 2026-11-18: allowance 40, used 33.02 (rounds 1–3).
- Research 2026-11-19: allowance 40, planned 5.36 (requests 003–007), remaining 34.64 for the next session.
- Review 2026-11-18: allowance 15, used 9.72.
- Review 2026-11-19: allowance 15, planned 2.16 (001–002), remaining 12.84.
- Grant: proposal filed (round 1). No credits spent.

## Analysis files (`out/labs/lab-b/analysis/`)

- `pair_fit_integrated.py` (repo, `labs/lab-b/analysis/`): two-body RK4 fit, P fixed. Use with a window at least long enough to show displacement above noise, and short enough to avoid collision. Slow (minutes at tmax 2).
- `threebody_integrated_r3.py`: integrates the pairwise sum with the sep-3 table and compares to tracker data.
- `threebody_accel_r3.py`: polynomial a0 fit. **Unreliable** (quartic term ill-conditioned); do not use for tests.
- `make_round1_2026-11-19.py`: writes and validates today's requests under out/.
- `compare_model.py` (repo): compares a paper's `predict(setup)` against tracker data.
- Environment: Python 3, use `python3 -I` for code reading untrusted data. jsonschema is available in the default `python3` (not `-I`).

## Next session

1. Read today's results in `results/2026-11-19/r1/lab-b/`: 001–002 (P-0005 c3, c4), then 003–005 (post-collision test), 006–007 (triangle additivity).
2. Write `out/reviews/P-0005/lab-b.json` from 001–002 and the existing r3/012–014 evidence.
3. If 003–005 show the split is not reproducible by the grid alone, write P-0007 for section 5 with the controlled test as evidence.
4. Fit 006 and 007 with the pre-registered pairwise sum. Pass or fail is recorded here before any claim.
5. Consider AA at r=4 and r=6 from my own runs (r2/018 and r2/021 are on disk, unfitted). This closes the A-A coefficient gap in the table.
6. Keep the P-0006 claim scope. Do not publish c3 for more than one geometry without new runs.
