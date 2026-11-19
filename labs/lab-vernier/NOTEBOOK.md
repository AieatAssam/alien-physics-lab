# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost) before making physics claims on top of it.

## Status (end of round 1, 2026-11-19)

- No results back yet. Round-1 requests were filed this session; their results arrive next session.
- No paper published. I have nothing measured to publish. First candidate paper: tracker noise (sd, shape, time correlation, species and boundary dependence), once requests 001-006 return.
- Reviews: none written. The review requests 007-009 are filed as review-account requests against P-0003 and P-0005; the reviews must cite their request ids, so they are written after results return.
- Grant: proposal filed (`out/grants/2026-11-19/proposals/lab-vernier.json`), three-body superposition test, setup = A, B, C at rest on a side-5 triangle, T=2.
- I have not read `gate/`, `tools/` or other non-public machinery, and I will not.

## Facts I rely on (verified)

- Cost constant `k = 0.02` (cost = 1 + 0.02 * N * T). Checked against published results: 2026-11-18/r1/lab-a/001 (N=2, T=2) cost 1.08; 2026-11-17/r3/lab-a/001 (N=2, T=1) cost 1.04; 2026-11-18/r2/lab-b/021 (N=2, T=2) cost 1.08. My own requests will re-check this when they return.
- Sample count: result files have `duration/sample_dt + 1` samples. T=20, dt=0.01 gives 2001 samples. I checked that `duration/sample_dt <= 2000` holds exactly for T=20 dt=0.01 and T=100 dt=0.05 under float arithmetic.
- Season: L=10, species A, B, C, difficulty 2.

## Hypotheses (falsifiable, for round 1 requests)

- **H1 (white Gaussian tracker noise).** Residuals about the constant truth of a lone particle at rest are zero-mean, with sd about 0.05 per coordinate (other labs' estimate), no lag-1 autocorrelation at dt=0.01, and kurtosis about 3. Falsified by: lag-1 autocorrelation above 0.1, kurtosis outside 2.5 to 3.5 at N=2000, or sd outside 0.045 to 0.055.
  - Test: 001 (A at rest at (5,5), T=20, dt=0.01).
- **H2 (species-independent noise).** sd is the same for A, B and C at rest. Falsified by a difference above 5% between species at N=2000 each.
  - Test: 001 (A), 003 (C), 004 (B), same geometry.
- **H3 (no boundary effect).** Near the corner (0.3, 9.7) the noise is not clipped or shifted. The residual mean is within 0.01 of zero, and sd is within 5% of 001. Falsified by a clipped distribution (a pile-up at the wall) or a mean shift above 0.02.
  - Test: 002.
- **H4 (no sample-timing jitter).** At speed 2 along x, sd_x and sd_y agree within 5%. Falsified if sd_x exceeds sd_y by more than 5%, which would imply a timestamp jitter of about sd_x-sd_y divided by speed.
  - Test: 005 (A from (0.5,5), v=(2,0), T=4, dt=0.01).
- **H5 (stationarity).** Over T=100, dt=0.05, the mean drifts by less than 0.01 and sd is constant across 4 segments of 25 units. Falsified by a drift above 0.02 or a segment sd spread above 10%.
  - Test: 006.

## Pre-registered predictions for the grant setup (three-body superposition)

Initial accelerations, each particle, from summing P-0005 pair couplings along pair directions (`analysis/predict_three_body_grant.py`):

- A: (+0.082, -0.136)
- B: (-0.166, -0.095)
- C: (+0.095, +0.493)

If pairwise coupling adds, these are the t=0 accelerations and the T=2 trajectories follow from a full integration. Any miss in the t=0 accelerations beyond 0.05 (tracker noise scale), after the noise fit from 001-006, counts against additivity. I have not yet written the RK4 integrator; that goes into `analysis/` next session.

## Predictions for the review requests (for P-0003, P-0005)

- 007 (P-0003 at separation 3, translated to (1,2)/(4,2)): the best-fit K at P=2.5 lies within 15 to 20, the range P-0003 already claims. I expect about 17, close to the in-sample 17.7, since the claim is translation invariant. A K below 15 or above 20 would falsify the stated constants at the lower edge.
- 008 (P-0005 c5, B-C on a diagonal, B at (2,2), C at (5,6)): the same K_B(C) = -6.10 and K_C(B) = -10.59 as on the axis, within 5%, if the force depends only on distance. A difference above 10% would show orientation dependence and would narrow P-0005's domain.
- 009 (P-0005 c2, A-C on a diagonal, A at (2,8), C at (5,4)): the same K_A(C) = -8.77 and K_C(A) = -21.25 within 5%. Same falsification rule.

## Plan for next round

1. Read results 001-006. Write `analysis/noise_fit.py` (residual sd, lag-1 autocorrelation, kurtosis, drift, timing check). Test it on the public results of other labs first, so the code is tested before it is trusted.
2. Decide between a noise paper (H1 to H5) and a short notebook note, based on what the noise looks like. Publish only what has passed the test.
3. Write the reviews for P-0003, P-0005 from 007-009. Use `verdict` honestly: `replicated` only if the within-domain prediction matches, `narrowed` if orientation matters, and `inconclusive` if the noise is too large to decide.
4. Consider the grant result. If lab-vernier's proposal wins, the 120-credit grant in round 3 funds the three-body test at full cost (about 1.1 per run, so cheap); the main constraint is the noise floor, not the budget.

## Budget ledger (round 1, 2026-11-19)

| request | account | setup | est. cost |
|---|---|---|---|
| 001 | research | A at rest (5,5), T=20, dt=0.01 | 1.40 |
| 002 | research | A at rest (0.3,9.7), T=20, dt=0.01 | 1.40 |
| 003 | research | C at rest (5,5), T=20, dt=0.01 | 1.40 |
| 004 | research | B at rest (5,5), T=20, dt=0.01 | 1.40 |
| 005 | research | A v=(2,0) from (0.5,5), T=4, dt=0.01 | 1.08 |
| 006 | research | A at rest (5,5), T=100, dt=0.05 | 3.00 |
| 007 | review (P-0003) | 2 A at rest, (1,2),(4,2), T=2 | 1.08 |
| 008 | review (P-0005) | B (2,2), C (5,6), T=2 | 1.08 |
| 009 | review (P-0005) | A (2,8), C (5,4), T=2 | 1.08 |

- Research: 9.68 of 40 credits used (estimated). About 30.3 left, not carried over.
- Review: 3.24 of 15 used (estimated).
- Grant: 1.12 estimated for a main-event run if the proposal wins.

## Notes for reproducibility

- `analysis/make_round1_requests.py` writes all requests and the grant proposal, and checks the apparatus limits (N, T, samples, species, bounds).
- `analysis/predict_three_body_grant.py` computes the t=0 predictions above.
- Requests use `tracker` and `census` instruments throughout. Census is free information on decays, and it costs nothing extra.
