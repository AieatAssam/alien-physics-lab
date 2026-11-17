# LAB-C notebook

## Round 3 — 2026-11-17

### Ledger and corrections (read first)
- **Research budget:** 40 allowed, 18.0 used before round 3, **22.0 remaining** at the start of round 3. (The round-2 note "36.2 remaining" was wrong.) Round-3 requests 001–010 cost 10.23 in total, leaving 11.77 if all are accepted.
- **Review budget:** 15 allowed, 0 used. Round-3 requests 011–012 (review account, cite P-0001) cost 4.40.
- **Correction: lab-c has not published anything.** The round-2 notebook said "P-0001 published by lab-c". That is wrong. `papers/P-0001/` belongs to lab-b (free flight of a lone A particle). There is no lab-c paper in `papers/` or `out/papers/`. The old `check_p1_model.py` pointed at a non-existent `out/papers/P-0001`; it is superseded by `analysis/check_P0001_model.py`, which checks lab-b's paper.

### Calibrated facts
- **Cost constant k = 0.02.** Confirmed by 007: cost 3.0 = 1 + 0.02 × 1 × 100. Cost does not depend on sample_dt.
- **Tracker noise sd ≈ 0.05 per coordinate.** 007 residuals against the free-flight model: x 0.051, y 0.049 over 2001 samples.
- **Dynamics are deterministic given initial conditions (P2 supported).** r1/003 and r2/004 have identical ICs (A-A, (3,4) v(1,0) and (7,6) v(−1,0)) at dt 0.1 and dt 0.005. Over 101 common times the rms position difference is 0.098 (particle 0) and 0.108 (particle 1). Pure measurement noise gives about 0.10 for a difference of two noisy readings, so the spread is all noise. The notebook's prediction (< 0.15) holds.
- **Sampling dt does not change the dynamics** (same result as above).

### Round-2 results (all nine `ok`; `census` returned no events in any run)
**Single particle**
- **007 (C, speed 1 in +x, duration 100, dt 0.05).** Matches the unfolded free-flight model at noise level: rms 0.051 (x) and 0.049 (y). Eight time segments show mean residuals ≤ 0.008. No drift. The particle stays on y = 5, so y-walls are not touched. About ten x-wall bounces (one every 8 time units). No decay events in 100 time units.

**Pairs at rest (A-A), all on the line y ≈ 5 (y rms deviation 0.05 = noise)**
- Point symmetry x0 + x1 = 10 holds for 001, 005 and 006 (mean ≈ 0, sd 0.07 ≈ √2 × 0.05).
- **006 (r = 6.0):** attractive and smooth. Separation falls 6.0 → 5.2 (t=2) → 1.2 (t=5). Relative acceleration ≈ 0.4 at r ≈ 6.
- **001 (r = 3.0):** separation 3.0 → 2.67 (t=0.5) → 0.58 (t≈1.2). The particles cross, then the separation grows to 8.6 at t=2.0, while each moves at a mean speed of about 5 over t ∈ [1, 2] (x0 goes 4.19 → 9.28). Both reach the walls by t≈2.1.
- **005 (r = 1.5):** separation 1.44 → 0.42 (t=0.4), cross, then 8.0 at t=2.0 and wall contact by t≈2.5.
- **Interpretation.** A pair started at rest gains kinetic energy of order 25 in total within 2 time units and separates to 8–9. For a conservative pair potential U(r) that is attractive at r = 3 (U increasing in r there), we would need U(8.6) < U(3), which requires a non-monotone potential (a barrier between r ≈ 3 and 8.6). The alternative is a non-conservative or velocity-dependent interaction. This argument uses only separations and speed magnitudes, so it does not depend on whether tracker ids survive close approach.
- **Caveat:** the initial-acceleration fits over short windows (≤ 0.4 time units) are noise-dominated and are not used. Round 3 uses longer windows matched to separation.

**Moving pairs (same ICs as r1/003)**

| Run | Species | min sep (t) | sep at t=10 | mean \|p0+p1−(10,10)\| |
|---|---|---|---|---|
| 004 | A-A | 0.25 (1.44) | 7.89 | 0.09 |
| 003 | B-B | 0.81 (1.96) | 8.66 | 0.09 |
| 009 | C-C | 0.34 (1.59) | 6.57 | 0.09 |
| 002 | A-B | 0.52 (1.71) | 6.65 | 1.5 |
| 008 | A-C | 2.73 (9.61) | 3.05 | 4.1 |

- For A-A, B-B, C-C the centre of mass stays at (5,5) within noise. For A-B and A-C it drifts.
- **The drift is not yet explained.** Candidate causes: unequal masses, non-reciprocal forces, or wall impulses. Walls are hit in several moving runs (002 x=10.04, 003 y=10.05, 004 x=10.09, 008 y=10.11, 009 x=10.17). Wall impulses cannot be excluded as the cause of the A-B and A-C drift, so **do not infer unequal masses from it.**
- **A-C never closes** (min sep 2.7). The other pairs close to 0.3–0.8. Either the A-C force is weaker or it has the opposite sign. The at-rest test (round 3) will tell which.
- Trajectory differences between species at identical ICs are large (rms 1.7–5.7). Species matter for moving pairs, which contradicts H2 for pairs.

### Hypotheses (status after round 2)
- **H1 single particle, ballistic with specular walls:** supported for A (r1/001 and lab-b r1/001), B (r1/002), C (r2/007 over 100 units). Only x-walls tested; y-walls and corners untested (review requests 011 and 012 pending).
- **H2 single-particle motion independent of species:** supported for free flight (A, B, C at speed 1 all give unit straight lines).
- **H3 no interaction at separation ≥ 2:** falsified (r1/003 and r2/001, 005, 006).
- **H4 species decay:** no census event in any run so far, including the single C particle over 100 units and all pair runs over 10 units. Not tested for decay in long pair runs.
- **H5 (new): pair force is a central, conservative function of separation only.** Contradicted for at-rest A-A by the energy gain above. Two replacements: H5a, the force has a non-monotone (barrier) component; H5b, the force is velocity-dependent or non-conservative.
- **H6 (new): pair dynamics are species-independent.** Falsified for moving pairs at identical ICs (trajectory differences of 1.7–5.7 rms), though the wall-hit confound on the centre-of-mass drift is unresolved.

### Round-3 requests (research account, 10.23 credits)
All at dt set so that duration/dt = 2000 samples; both instruments on.

Force curve, A-A at rest along x (initial acceleration from a quadratic fit over the whole window):
- **001** r = 2.0 at (4,5),(6,5), T = 0.4
- **002** r = 1.0 at (4.5,5),(5.5,5), T = 0.2 (window short so the particles have not crossed)
- **003** r = 4.0 at (3,5),(7,5), T = 0.8
- **004** r = 8.0 at (1,5),(9,5), T = 2.0 (long-range tail)
- **005** r = 2.0 along y at (5,4),(5,6), T = 0.4 (isotropy check vs 001)

Species at rest, r = 2.0 along x, T = 0.4 (at (4,5),(6,5)):
- **006** A-B, **007** A-C, **008** B-B, **009** B-C, **010** C-C

**Predictions (falsifiable):**
- **P5a (no barrier):** if the force is a monotone attraction, a(r=4) attracts with magnitude 0.5–1.5 and a(r=8) attracts with magnitude 0.05–0.3. **P5b (barrier):** a(r=4) is repulsive or near zero, with a sign change between r = 4 and 6. If 003 shows attraction of ≥ 1 at r = 4, a monotone conservative potential survives and the energy argument needs rechecking (non-conservative or velocity-dependent force).
- **P-iso:** 005 (along y) matches 001 (along x) within 10%. Otherwise the force is anisotropic and the 1D picture is wrong.
- **P-species:** if the force is species-independent, the magnitude at r = 2 matches 001 within 10% for all pairs. A-C is expected to differ (weaker), per 008.
- **P-reciprocity:** for A-B, a_A and a_B are equal and opposite if the masses are equal. Unequal magnitudes indicate unequal masses or a non-reciprocal force. Resolves the centre-of-mass drift if reciprocity holds.

### Review of P-0001 (lab-b, lone species-A free flight)
- **Filed:** `out/reviews/P-0001/lab-c.json`, verdict **replicated** (narrow case only), evidence r1/lab-c/001 and r1/lab-b/001.
- **Checks:** `analysis/check_P0001_model.py` gives RMSE 0.075 (lab-b 001) and 0.078 (lab-c 001). Both match noise. Predicted error 0.01 (side-normalised, 0.1 absolute) holds with room.
- **Problems raised in the review:** the falsification threshold is written in two scales (0.03 "chamber units" vs 0.3 absolute); the "does not establish" section cites runs not in the evidence list.
- **Edges still untested for P-0001:** y-walls, corners, speed > 1, duration > 10.
- **Round-3 review requests:** 011 (speed 3.36, duration 100, y-wall hits) and 012 (exact diagonal, corner hits at t=8 and t=18). Prediction: both at noise level (RMSE ≲ 0.1), so the claim survives. If residuals grow with time, the speed or wall model is wrong. **Update the review file once 011 and 012 return.**

### Open questions and risks
- The energy argument is the most important open question. The simplest test is 003 and 004 (force at r = 4 and 8).
- Velocity dependence is not yet tested. At-rest runs isolate position dependence; moving runs mix position and velocity. A test: same separation, different relative velocity.
- Pairs have been run only to t = 10. Decay and pair-with-wall effects over longer runs are unknown.
- Wall impulses confound the centre-of-mass test for asymmetric pairs.

### Plan for round 4 (or the next session today)
1. Fit a(r) for A-A from 001–005 and 006 (round 2). Decide P5a vs P5b.
2. If a barrier exists, locate the sign change with 1–2 further A-A at-rest runs (r = 3, 5), kept within budget.
3. Species matrix from 006–010. Decide species dependence and reciprocity.
4. Update the P-0001 review with 011 and 012.
5. Keep about 11.8 research credits unless round-3 data show a sharp discriminating test. Unused credits do not roll over.
6. **Publish only when a predict(setup) model reproduces the at-rest runs at noise level.** The first candidate is a pair claim with domain species A-A, max_particles 2, separation range as tested (1–8). Do not publish the energy observation before 001/005 are confirmed against a model.

### Analysis files (out/labs/lab-c/analysis/)
- `round2_analysis.py`: round-2 summaries (007 free flight; at-rest pairs 001/005/006; moving pairs 002/003/004/008/009; trajectory comparisons).
- `round2_accel_replicate.py`: determinism check (r1/003 vs r2/004) and the early-window acceleration fits (noise-dominated; not used).
- `check_P0001_model.py`: P-0001 `model.py` against lab-b r1/001 and lab-c r1/001.
- `make_round3_requests.py`: generates round-3 requests under out/requests/2026-11-17/r3/lab-c/ and checks the schema constraints by hand (jsonschema is not installed).

### Publications
- **lab-c: none.** The round-2 entry claiming P-0001 was wrong (see Ledger).
- **Review filed:** P-0001 (lab-b), verdict replicated (narrow), updated when 011/012 return.
