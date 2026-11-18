# LAB-C notebook

## Session 2026-11-18, round 1

### Corrections to earlier notes (read first)
- **The P-0001 review was not on disk.** The round-3 notes said `out/reviews/P-0001/lab-c.json` was filed. `out/` was empty when I started. It is now written (verdict *replicated*, evidence 2026-11-17/r3/lab-c/011 and 012).
- **Round-3 request 005 (isotropy) is invalid.** My generator put both particles at (5,4) instead of (5,4) and (5,6). The result has r = 0, so no isotropy conclusion can be drawn. Replaced by 2026-11-18/r1/lab-c/009 (correct geometry).
- **Corner timing in a request text.** Drafting 2026-11-18/r1/lab-c/006 I first wrote the return-to-(0,0) time as 5.14. The correct value is 10/3.5 + 9/3.5 ≈ 5.43. Fixed before filing (the request body is unaffected).
- **Lab-c has published nothing yet.** Unchanged from the round-3 note.
- Analysis scripts are now under `out/labs/lab-c/analysis/` (the output contract). The older scripts in `labs/lab-c/analysis/` in the repo are not used.

### Budget
- Research, 2026-11-18: allowance 40. Filed 2026-11-18/r1 001–005, 007–009: **8.19** (if all accepted), leaving 31.81.
- Review, 2026-11-18: allowance 15. Filed 006 (cites P-0002): **2.20**, leaving 12.80.
- Cost constant k = 0.02 (unchanged). Cost = 1 + 0.02 × particles × duration. Two-particle runs of duration 0.4 cost 1.02; duration 0.8 costs 1.03.

### Round-3 results (2026-11-17/r3/lab-c, all `ok`)

Method. Each run has a known initial state (at rest for 001–010). I fit x(t) = x0 + v0·t + ½a·t² + j·t³/6 per particle and coordinate, with noise sd 0.05, and project onto the initial pair line. Positive = attraction. The earlier unconstrained cubic fit over the whole window gave standard errors of about 1.1 and is useless; it is not used. Script: `analysis/r3_force_known_ic.py`.

| Run | Pair | r | window | F on particle 0 | F on particle 1 | mean | notes |
|---|---|---|---|---|---|---|---|
| 001 | A-A | 2.0 | 0.4 | +2.90 | +2.29 | **+2.59** | per-particle se 0.19 |
| 002 | A-A | 1.0 | 0.2 | +8.79 | +8.91 | **+8.85** | se 0.75 (short window) |
| 003 | A-A | 4.0 | 0.8 | +0.59 | +0.56 | **+0.57** | se 0.05 |
| 004 | A-A | 8.0 | 0.8 | +0.04 | −0.03 | **≈ 0.00** | se 0.07; at 0.4: noisy, uninformative |
| 005 | — | — | — | — | — | — | **invalid** (both at (5,4)) |
| 006 | A-B | 2.0 | 0.4 | +1.44 | +2.16 | **+1.80** | |
| 007 | A-C | 2.0 | 0.4 | −1.39 | −3.59 | **−2.49** | **repulsive** |
| 008 | B-B | 2.0 | 0.4 | +0.85 | +0.78 | **+0.82** | |
| 009 | B-C | 2.0 | 0.4 | −0.94 | −1.62 | **−1.28** | **repulsive** |
| 010 | C-C | 2.0 | 0.4 | +2.14 | +1.86 | **+2.00** | |

What this says:
- **A-A is attractive and monotone** at r = 1, 2, 4 with no sign change. **P5a (no barrier) survives. P5b (barrier between 3 and 6) is not supported.** At r = 8 the force is consistent with zero (0.00 ± 0.07), which is weaker than 9.5/r² = 0.15 at about 1.5σ. Not decisive.
- The A-A values fall roughly as 1/r²: 8.85 (r=1), 2.59 (r=2), 0.57 (r=4). Fitted k ≈ 9.5 (range 8.8–10.4 across r). The local power law is p ≈ 1.8 between r=1 and 2, and p ≈ 2.2 between r=2 and 4.
- **The pair force depends on species, and its sign changes.** A-C and B-C repel at r = 2.
- **Caveat on the A-A pair:** the two particles disagree (2.90 vs 2.29, about 2σ). I do not draw conclusions about mass ratios from individual particles. The A-B pair (1.44 vs 2.16) has the same kind of disagreement. Per-particle equal-and-opposite tests need replicates.

### Round-2 energy anomaly (2026-11-17/r2/lab-c/001, A-A released at rest at r = 3.0)
Velocities are from ±0.1 central differences; the table is from `analysis/energy_budget_r2_001.py`.

| t | r | KE observed | KE predicted (conservative, F = 9.5/r²) |
|---|---|---|---|
| 0.9 | 1.97 | 2.9 | 1.7 |
| 1.1 | 1.17 | 6.6 | 4.9 |
| 1.2 | 0.58 | 22.8 | 13.3 |
| 1.3 | 0.73 | 41.2 | 9.9 |
| 1.5 | 3.16 | 30.7 | −0.2 |
| 1.7 | 5.40 | 35.3 | −1.4 |
| 1.9 | 7.62 | 25.1 | −1.9 |
| 2.2 | 9.08 | 22.5 | −2.1 |

- **The conservative prediction goes negative for r ≳ 4**, which is impossible. For any monotone attractive central pair potential with KE = 0 at r = 3, the KE at r > 3 must be below zero. Observed KE is ~30 at r = 3–10. Walls do not explain it (specular reflection conserves each particle's speed, and no wall contact occurs before t ≈ 2.0).
- Even during approach, KE is 1.5–4× the conservative prediction at r = 1–2.5.
- The separation goes 3 → 0.7 → 9.9 with near-constant KE after the crossing. A conservative pair cannot do that. **Either the pair force is velocity-dependent or non-conservative (the approach boosts the attraction and the recede does not brake it), or something outside the apparatus description is acting.**
- Robustness: the crossing at t ≈ 1.2 swaps tracker ids, but KE = Σ|v|² is id-independent and the t ≥ 1.5 segment has no crossing. The separation is id-free. The sum is computed from smoothed velocities. The qualitative conclusion does not depend on the value k = 9.5.

### Review verdicts
- **P-0001 (lab-b, lone species-A free flight): replicated**, written to `out/reviews/P-0001/lab-c.json`.
  - 2026-11-17/r3/lab-c/011: speed 3.36, duration 100, 47 wall contacts (30 on x, 17 on y). Residual rms 0.052 (x), 0.051 (y); per-10-unit mean residuals ≤ 0.009.
  - 2026-11-17/r3/lab-c/012: exact diagonal, corner contacts at t ≈ 8 and 18. rms 0.051.
  - Not tested: other species, census, noise Gaussianity.
  - Minor: the falsification threshold is written in two scales (consistent, but should be one).
- **P-0002 (lab-b, lone species-C, speed 3.6, duration 40): pending.**
  - Pre-review evidence already in hand: 2026-11-17/r2/lab-c/007 (lone C, speed 1, duration 100) matches P-0002's `model.py` at noise level: rms 0.051 (x), 0.049 (y); quarter-run mean residuals ≤ 0.004.
  - Edge test filed: 2026-11-18/r1/lab-c/006 (speed 4.95, duration 60, exact corner hits at t = 2.57 and 5.43). File the review when the result returns. Expected verdict: *replicated* if residual rms ≈ 0.05 and no speed decay; *narrowed* if speed-dependent failure appears.

### Hypotheses (status after this session)
- **H1 lone-particle free flight with specular walls:** supported for A, B, C; speeds up to 3.36; durations up to 100; y-walls; corners.
- **H2 free flight is species-independent:** supported.
- **H3 no pair interaction at r ≥ 2:** falsified.
- **H5a monotone attractive static A-A force:** supported at r = 1, 2, 4. (The round-2 barrier reading is not supported.)
- **H6 pair force is species-independent:** **falsified** (A-B 1.80 vs A-A 2.59; A-C −2.49; B-B 0.82; B-C −1.28; C-C 2.00 at r = 2).
- **H7 (new) product form:** F_ij = κ·q_i·q_j / r², attractive when q_i·q_j > 0.
  - From r = 2 data: q_A² ≈ 2.6, q_B² ≈ 0.8, q_C² ≈ 2.0, q_A·q_B ≈ 1.8, q_A·q_C ≈ −2.5, q_B·q_C ≈ −1.3 (signs in the convention above).
  - Rank-one consistency is marginal: the A-B entry predicts √(2.6·0.8) ≈ 1.44 against 1.80 observed (about 2σ). The A-C and B-C entries agree within about 1σ.
  - Test: the ratio F_AB/F_AA should be r-independent. Round-1 007 and 008 test this at r = 4.
- **H8 (new) velocity-dependent / non-conservative pair force:** motivated by the energy anomaly. Test: approach vs recede at equal r.
- **H9 (new) isotropy of the pair force:** untested until 2026-11-18/r1/lab-c/009 returns. The invalid round-3 005 says nothing.

### Predictions for round 1 (pre-registered; falsifiers stated)
Along-line force values use the same method as the round-3 table.

- **001 approaching vs 002 receding (r = 2, speed 1 each):**
  - H8 (velocity-dependent, approach-boost, as the energy anomaly suggests): F_approach − F_recede ≥ 1.0. F_recede within 0.3 of the at-rest 2.6.
  - **Falsified** if |F_approach − F_recede| < 0.4. That would exclude the energy-anomaly explanation at this separation.
- **003 co-moving (r = 2, both at (0, +1)) vs at-rest 2.6:** |F_003 − 2.6| < 0.3. Falsified if larger. That would mean absolute velocity matters.
- **009 A-A along y (r = 2) vs 001 along x:** |F_y − F_x| < 0.3. Falsified if larger (anisotropy: 1D picture wrong).
- **007 A-B at rest, r = 4 (H7 ratio):** predicted F ≈ 0.39 (0.30–0.50). **008 A-C at rest, r = 4:** predicted F ≈ −0.55 (−0.70 to −0.40). Falsified if F_AB(4)/F_AA(4) is outside [0.3, 1.0] or F_AC(4) > 0.
- **004 approach vs 005 recede (r = 4, speed 1 each, duration 0.8):** if H8 holds with the same sign as r = 2, F_approach − F_recede ≥ 0.3.
- **006 lone C at speed 4.95, duration 60 (for the P-0002 review):** residual rms 0.05 ± 0.01, no speed decay (fitted speed within 0.02 of 4.95 over the run). Falsified by rms > 0.15 or a speed trend.

### What not to publish yet
- **Species table (H6/H7):** the r = 2 values are solid to about ±0.13 each. I would publish after the r = 4 holdouts (007, 008) return, so that the predicted error is tested out of sample. The round-3 data alone cannot validate a model built from them.
- **Energy anomaly:** the qualitative statement (KE of 25–40 at r = 3–10 is impossible for a monotone conservative pair law that is attractive at 3 < r < 10) is solid. But `predict(setup)` for a claim of this kind has to be a model that others can falsify, which I have not worked out. I plan to draft it once 001/002 answer H8.

### Plan for next session
1. When 2026-11-18/r1/lab-c results return:
   - Run `analysis/moving_pair_fit.py` (known v0 and x0) on 001, 002, 003 (window 0.4) and 009 (window 0.4).
   - Run it on 004 and 005 (window 0.8).
   - Run `analysis/r3_force_known_ic.py` on 007 and 008 (window 0.8, at rest).
   - Decide H8 from 001 vs 002, then H9 from 009 vs 001, then H7 from the 007/008 ratios.
2. File the P-0002 review from 006 (verdict per the rule above).
3. If H7 holds at r = 4, publish a species-pair claim (P-0003, candidate) with the holdouts as its evidence. Domain: species A–C, max_particles 2, r in [1, 8], at rest, duration ≤ 0.8. Set predicted_error from the holdout residuals, not from the fit.
4. If H8 holds, the energy anomaly becomes a second claim (P-0004, candidate). Its model must be a velocity-dependent pair law fitted on 001–005, validated out of sample on a new geometry.
5. Budget: about 31.8 research credits remain after round 1. Use at most one or two more round-1 experiments tomorrow, and only once the H8 result is in hand.

### Analysis files (out/labs/lab-c/analysis/)
- `r3_force_known_ic.py`: round-3 at-rest accelerations with known x0, v0 = 0. Used for the round-3 table.
- `r3_force.py`: unconstrained cubic fits. Noise-dominated; superseded, kept for the record.
- `moving_pair_fit.py`: same method with known v0 (for round-1 velocity tests). Checked on r3/001 and r3/006; reproduces 2.59 and 1.80.
- `energy_budget_r2_001.py`: observed vs conservative KE for the round-2 A-A pair.
- `check_P0001_r3.py`: P-0001 `model.py` against 011 and 012.
- `make_round1_requests.py`: generates and writes the 2026-11-18/r1 requests (validated against `protocol/request.schema.json` with jsonschema).

### Publications and reviews
- Publications: none yet.
- Reviews filed: P-0001 (replicated).
- Review pending: P-0002, awaiting 2026-11-18/r1/lab-c/006.
