# LAB-C notebook

## Round 2 — 2026-11-17

### Calibrated facts (from round 1, results/2026-11-17/r1/lab-c/)
- **Cost constant k = 0.02.** From the costs: 001 and 002 cost 1.2 each (1 + k·1·10), 003 cost 1.4 (1 + k·2·10). Cost does not depend on sample_dt, so fine sampling is free (only the 2000-sample cap binds).
- **Tracker noise ≈ 0.05 per coordinate.** Residual sd against the ballistic model: 001 x 0.053 / y 0.057; 002 x 0.048 / y 0.048. Means within 0.003 of zero.
- Research budget: 40 allowed, 3.8 spent in round 1, **36.2 remaining today**. Unused credits do not roll over.

### Results and status of hypotheses
- **H1 (single particle is ballistic with specular wall reflection): supported, narrow.** 001 (species A) and 002 (species B) both fit a unit-speed straight-line path with one reflection at x=10 (t≈8), RMSE 0.078 and 0.067 length units (0.008, 0.007 of side). Only +x speed 1, one x-wall bounce, duration 10 were tested. y-wall reflection is untested. Published as P-0001 (claim c1, predicted_error 0.02).
- **H2 (species does not change single-particle motion): supported for A vs B only.** 001 and 002 agree within noise. C untested. Pair species dependence not yet tested (round 2 002, 003, 008, 009).
- **H3 (no interaction at separation ≥ ~2): FALSIFIED by 003 (request 2026-11-17/r1/lab-c/003).** Two A particles at speed 1 (initial separation 4.5, approaching at relative speed 2) deviate strongly from free motion. Their separation falls to ≈0.5 at t≈1.4, then grows back to ≈10 by t≈8 and is still decreasing at t=10. Particle paths are far from ballistic (e.g. at t=2 particle 0 is at (4.07, 5.92) where free motion gives (5, 4)).
- **H4 (species C or others decay): not probed.** No census events in any round-1 run (duration 10 only).

### What 003 shows (analysis/round1_003_pair_series.py)
- **Point symmetry:** p0(t) + p1(t) = (10, 10) to within noise at every sampled time. The centre of mass stays at (5, 5), so total momentum is near zero and the pair dynamics respect this symmetry. Consistent with a pair-only interaction (no external field).
- **Rough time-reversal symmetry about closest approach:** separation is approximately mirrored about t≈1.4 (2.19 at t=1.0 vs 1.75 at t=1.8; 3.2 at t=0.6 vs 3.1 at t=2.2). Not exact, and the noise is large, so this only weakly suggests a conservative central pair force.
- **Speed rises on approach and falls on separation.** Finite-difference speeds reach ≈3–4 near closest approach (from 1.0) and fall to ≈0.5–1 afterwards. Qualitatively what an attractive pair potential would do. Finite-difference speeds are noisy (≈0.3–0.4), so energy conservation is **not** established; the sign of the force is **not** yet determined.
- **Leading guess (low confidence): the A-A force is attractive, with range of at least 2–4.** The range is not determined: at-rest runs (001, 005, 006) will pin it. Nothing in the data yet distinguishes attraction from a velocity-dependent or dissipative law.

### Round 2 requests (research account, 9 requests, est. total 14.2 credits; budget remaining after ≈22.0)
All use dt 0.005 (2000 samples) unless noted. The `tracker` and `census` instruments are on.
- **001** A-A at rest, sep 3.0 along x (3.5, 6.5), y=5. Sign test with no velocity. If the force is attractive, both accelerate toward each other symmetrically about x=5; if repulsive, they move apart; if there is no force, they stay at rest.
- **002** A-B, same ICs as 003. Species dependence.
- **003** B-B, same ICs as 003. Species dependence.
- **004** A-A, same ICs as 003, replicate. Tests determinism vs fresh noise, and resolves the close approach that dt 0.1 undersamples.
- **005** A-A at rest, sep 1.5. Short-range force law. Compare with 001.
- **006** A-A at rest, sep 6.0 (x = 2, 8). Long-range tail. Compare with 001 and 005.
- **007** C single, same ICs as round-1 001, duration 100, dt 0.05. Species C free motion, many wall bounces, decay (census) check. Cost 3.0.
- **008** A-C, same ICs as 003. Species dependence for C.
- **009** C-C, same ICs as 003. Species dependence for C.

### Predictions I am testing (falsifiable)
- P1: 001 shows symmetric approach (x-positions mirror about 5 at all t) and a sign determined by the sign of the acceleration. A repulsive or no-force outcome would falsify "attractive" as the leading guess.
- P2: 004 reproduces 003 within noise (RMSE < 0.15 length units, about 2× the noise-only RMSE of ≈0.07). If 004 differs by more than that, the dynamics are not deterministic given ICs, which would change how I interpret single runs.
- P3: 001 and 005 accelerations: |a(1.5)| > |a(3.0)| if the force is short-range and attractive; 006 should show near-zero acceleration if the range is ≲6.
- P4: 002 and 003 are both species-independent if the force is the same for A-A, A-B, and B-B. Any difference beyond noise supports species-dependent pairwise forces (as H2 in the round-1 plan would predict).
- P5: 007 shows no census events over duration 100. A decay of C would appear as a census event.

### Open questions and risks
- Is the pair force velocity-dependent? Rest (001, 005, 006) vs moving (003, 004) runs will show this only if the force law at equal separation matches.
- Does the force depend on species pair? 002, 003, 008, 009 vs 003/004 test this.
- Energy and momentum conservation: point symmetry holds, but I have not checked energy with precise velocities. Need the fine-sampled runs for that.
- Wall reflection in y is untested. Walls might act on pair forces too; do not assume.
- Single-particle domain (P-0001) is deliberately narrow. Do not broaden it until 007 and the wall/speed checks come back.

### Plan for round 3 (after round 2 results)
1. Fit the pair force as a function of separation from 001/005/006 (at rest) and check the sign and range. Compare against 003/004 (moving) to test velocity dependence.
2. Species dependence: compare 002, 008, 009 with 003/004 at matched ICs.
3. If the A-A law is pairwise and central, design a three-particle test (A-A-A, cost ≈ 1.6 at duration 10) to probe non-additivity. Only after the pair law is pinned.
4. Write a pair-interaction paper only once a predict(setup) model reproduces 003/004 and at least one at-rest run. A falsifiable pair claim with a stated domain (species, separation range, max_particles 2) is the target for round 3 or later.
5. Use the remaining daily budget (≈22 credits) only if round 2 leaves a clear discriminating test. Unused credits do not roll over.

### Analysis files (out/labs/lab-c/analysis/)
- `round1_free_flight_check.py`: residuals of 001/002 vs ballistic model with wall reflection.
- `round1_003_pair_series.py`: separation, speed, centre of mass, and momentum for 003.
- `check_p1_model.py`: checks the P-0001 claim schema and model RMSE against 001/002 (editor metric: RMSE / side).
- `make_round2_requests.py`: generates the round-2 request files.

### Publications
- **P-0001** (out/papers/P-0001/): single particle (species A/B) ballistic with specular wall reflection; domain max_particles 1, species A/B, speed 1.0 tested, x-wall only tested. predicted_error 0.02. Evidence: 2026-11-17/r1/lab-c/001, 002.
