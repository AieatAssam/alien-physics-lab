# LAB-B notebook

Persona: bold theorist. Rule I hold myself to: a striking law only after a discriminating run supports it, and stated with its domain.

Last updated: 2026-11-18, round 1 (requests written, results pending).

## Season facts (measured)

- Season 1, species in use: A, B, C (`protocol/season.json`). Chamber [0, 10]^2.
- **Cost constant k = 0.020.** Cost is `1 + k·N·T` and does **not** depend on `sample_dt`. Confirmed on every result so far (r2: 1.40, 1.06, 1.80; r3: 1.12 for N=2, T=3; 1.04 for N=2, T=1; 1.40 for N=2, T=10).
- **Consequence:** sample_dt is free. The only limit is 2000 samples, so `sample_dt = duration/2000` is always allowed and gives the most data per credit. Round 2 used dt 0.05 at T=10 (200 samples) when dt 0.005 (2000 samples) would have cost the same. Use the finest dt the sample cap allows from now on.
- Tracker noise: **sd about 0.05 per coordinate** (r1/001: 0.053/0.052; r2/005: 0.052/0.050).
- Census: no decay or appear events in any run so far (r1 001–002, r2 001–006, r3 001–006).
- Masses, relative to m_A = 1, from centre-of-mass conservation before wall contact (`analysis/r2_checks.py`). Rough:
  - A-A: 0.98, so equal masses.
  - A-B: 0.55, 0.74, 0.70. I take m_B ≈ 0.7 m_A, spread ±0.1.
  - A-C: 0.40. So m_C ≈ 0.4 m_A.

## Pair sign pattern (main result so far)

All six unordered species pairs have now been measured at rest with a requested separation of 1–2 (and A-B also at 4):

| Pair | Run(s) | Sign at short range | Evidence |
|---|---|---|---|
| A-A | r2/001 | attract | first r<0.5 at t=0.65 |
| A-B | r1/002, r2/002–004, r3/006 | attract | first r<0.5 at t=0.25–0.30 (sep 1); t=0.84 (sep 2, offset); t=2.55 (sep 4) |
| B-B | r3/001 | attract | first r<0.5 at t=1.08 (sep 2) |
| C-C | r3/002 | **attract** | first r<0.5 at t=0.72 (sep 2) |
| A-C | r2/006, r3/004, r3/005 | **repel** | separation grows monotonically; sep 1, 2, 4 |
| B-C | r3/003 | **repel** | separation grows monotonically to 7.95 at t=3 (sep 2) |

**Round 3 falsified my "C repels everything" rule (H7 as stated).** r3/002 (C-C) attracts. So the repulsion is not set by C alone.

The six signs fit a charge-product rule: F_ij ∝ q_i q_j, with q_A = q_B = +1 and q_C = −1. Like-charged pairs (AA, AB, BB) attract. Unlike pairs with C (AC, BC) repel. CC attracts, since q_C² > 0. **This fits every observed sign. It is not yet tested for magnitudes or for additivity.** Same-species signs are automatic under this rule, so only the cross-species signs are informative. They are all now consistent with it. Only three species exist in this season, so a fourth sign assignment cannot be tested here.

Rough initial relative accelerations at the requested separation (fit `r(t) − d0 = ½·a·t²` over t ≤ 0.3 and t ≤ 0.6, `analysis/r3_summary.py`). These are noisy: at sep 2 the displacement over t ≤ 0.3 is only about 0.07, the size of the noise.

| Pair, sep | a (t≤0.3) | a (t≤0.6) | Sign |
|---|---|---|---|
| A-A, 2 (r2/001) | −5.5 | −7.1 | attract |
| B-B, 2 (r3/001) | −1.6 | −2.0 | attract |
| C-C, 2 (r3/002) | −4.6 | −5.1 | attract |
| B-C, 2 (r3/003) | +1.5 | +2.6 | repel |
| A-C, 4 (r3/005) | +1.1 | +0.8 | repel |
| A-C, 2 (r2/006) | +4.6 | +4.0 | repel |
| A-C, 1 (r3/004) | +16.8 | +12.7 | repel |
| A-B, 1 (r2/003) | −16.7 | −4.6 | attract |
| A-B, 1 (r3/006) | −16.7 | −6.6 | attract |

- **H6, A-C repulsion falls off steeply with separation (supported, rough).** The initial acceleration goes +16.8 (sep 1), +4.6 (sep 2), +1.1 (sep 4). Each doubling of separation cuts it by roughly 4, close to r^-2. Uncertainty is large (±50%). The sep-1 window is affected by the fast separation, so I will fit it properly with a full model before stating an exponent.
- BB attraction looks weaker than AA and CC at the same separation (−1.6 vs −5.5 and −4.6). Under equal charge magnitudes that would require a mass or charge difference. Not yet claimed; a longer, dense run is needed (see plan).

## Results so far

### Round 1 (r1)

- **001 (ok), one A particle, free flight.** Nominal v = (1.0, 0.5), duration 10, dt 0.1. Best-fit velocity (0.9995, 0.4985). Reflected-line model fits with one x-wall bounce, no drift. Basis for **P-0001**.
- **002 (ok), A at (4,5) and B at (6,5), both at rest, dt 0.1.** The pair accelerates toward each other. Separation first drops below 0.5 at t≈0.9. Confirmed attraction, not inert.

### Round 2 (r2), all status ok, all 0 census events

- **001, A-A at rest, 2.0 apart, dt 0.05.** A-A attracts. First r<0.5 at t=0.65. The pair passes through its partner (min r≈0.10 at t≈0.75) and oscillates, then separates to the walls.
- **002, A-B at rest, 4.0 apart, dt 0.05.** First r<0.5 at t=2.55. Far-field approach. The single-run power-law fit is consistent with n between 0.5 and 1.5 at noise level.
- **003, A-B at rest, 1.0 apart, dt 0.05, T 10.** First r<0.5 at t=0.30, then repeated passes with min r≈0.08–0.2. Bound oscillation through the centre for t≤5, then wall bounces. A simple power law does not fit this run (see close-approach section).
- **004, A-B at rest, offset (2.0, 0.5), dt 0.02, T 1.5.** Central-force test. Pre-contact separation angle: mean 14.19°, sd 2.18° (n=30), expected 14.04°, so the line direction holds within about ±0.4°. After the pass the angle is 13.71° mod 180, also consistent. Central force supported for A-B (H3).
- **005, single C, speed 3.6, duration 40, dt 0.1.** Reflected-line fit: velocity (3.0000, 2.0000), exactly nominal. Residual sd 0.052 (x), 0.050 (y). Free flight holds for C at high speed and long duration (H5). Basis for **P-0002**.
- **006, A-C at rest, 2.0 apart, dt 0.05.** A and C repel. Separation grows from 2.10 to 3.67 by t=1.0 and to 7.6 by t=2.2 (then wall contact). The round-2 persona note "every species pair attracts" is falsified.

### Round 3 (r3), requested 2026-11-17, all status ok, all 0 census events

Costs match `1 + 0.02·N·T` in every case. Budget remaining after the round: 22.30.

- **001, B-B at rest, 2.0 apart, dt 0.02, T 3.** Attracts. First r<0.5 at t=1.08, min r=0.03 at t=2.92. My prediction was attraction with first contact near t≈0.6–0.9. It came later than predicted, but the sign was correct. **Partly confirmed.**
- **002, C-C at rest, 2.0 apart, dt 0.02, T 3.** **Attracts**, first r<0.5 at t=0.72, min r=0.20 at t=0.74. My prediction was repulsion. **Falsified.**
- **003, B-C at rest, 2.0 apart, dt 0.02, T 3.** Repels. Separation grows monotonically to 7.95 at t=3. Prediction was repulsion. **Confirmed.**
- **004, A-C at rest, 1.0 apart, dt 0.02, T 3.** Repels at short range. Separation grows from about 0.95 to 7.2 by t=1.5. Prediction was repulsion (no sign change at r=1). **Confirmed.**
- **005, A-C at rest, 4.0 apart, dt 0.02, T 3.** Repels, slowly. Initial acceleration about +1.1 (t≤0.3), much smaller than at sep 2 (+4.6). Prediction was "smaller than sep 2". **Confirmed.**
- **006, A-B at rest, 1.0 apart, dt 0.01, T 1 (exact repeat of r2/003's initial state).**
  - Early times agree with r2/003. Initial acceleration −16.7 in both, and first r<0.5 at t=0.25 (r3/006) vs 0.30 (r2/003).
  - **After the first close pass they disagree.** Coordinate difference rms over common times t≤1.0 is 0.25 in x and 0.07 in y. The y component agrees with noise. The x component does not. Expected from noise alone is about 0.07 in each.
  - Conclusion: either the simulator is not deterministic for identical setups, or the dynamics depend on sample_dt, or the close-pass dynamics are chaotic and amplify small differences. **This is the top open question.** The round 1 requests test it.

## Hypotheses (status after round 3)

- **H1, free flight of a lone particle (A):** supported by r1/001. Published as **P-0001**. Lab-a has a partial replication (see Papers).
- **H5, free flight of a lone particle (C), high speed, long run:** supported by r2/005. Published as **P-0002**.
- **H2, pair interaction is species-pair specific, with signs:** supported. All six pairs measured. Sign pattern fits a charge-product rule with q_C opposite to q_A, q_B. Magnitudes not tested.
- **H7 (sign follows C alone):** **falsified** by r3/002 (C-C attracts). Replaced by the charge-product sign rule above.
- **H3, central pair force:** supported for A-B (r2/004). Not yet tested for A-C, B-C, or A-A.
- **H4, distance dependence of attraction (A-B):** qualitatively supported. Time to r<0.5 from rest: 0.25–0.30 at sep 1, 0.84 at sep 2 (offset), 2.55 at sep 4.
- **H6, A-C repulsion decays with separation:** supported (rough). Initial accelerations +16.8, +4.6, +1.1 at sep 1, 2, 4. Roughly r^-2, ±50%.
- **H8, short-range (r<1) pair dynamics follow a central power law:** not supported as measured; see close-approach section.
- **H9 (new), the simulator is deterministic at fixed dt and sample_dt-independent:** untested. Directly tested by round 1 requests 001–003. Currently in doubt because of r3/006.

## Close-approach problem (open, now sharper)

- Joint fit of the A-B runs (002, 003, 004 and r1/002) and the A-A run (001) with one power law F = k·r^(-n), free masses, and exact requested initial states gives rms 0.28–0.34 (noise 0.05). Not usable.
- Per-run: far-field runs fit at noise level (r2/002, r2/004). Close-approach runs do not (r2/003 rms ~0.16 at best, r1/002 ~0.10).
- Softening does not help. The grid picks ε = 0.
- **New (round 3):** r3/006 and r2/003 start from the same state and agree before the first close pass but disagree after it. This means either a non-deterministic simulator, a dependence on sample_dt, or chaotic amplification at close passes. Each has different consequences:
  - *Non-deterministic:* close-pass samples are not reliable truths. Claims restricted to far field and the sign pattern remain valid. The noise model would need a second component.
  - *sample_dt dependence:* the simulator takes steps tied to output sampling. Then finer sampling is closer to the true dynamics, and I should use the finest dt always (free, see Season facts).
  - *Chaotic amplification:* a tiny difference grows during close passes. Then any close-pass prediction has a finite horizon, and the claim domain must exclude it.
- Do not publish a pair law until the round 1 determinism and dt tests are in.

## Round 1 plan (2026-11-18, r1), submitted

Written to `out/requests/2026-11-18/r1/lab-b/`. All are research account, N=2, T=1, same initial state as r3/006 (A at (4.5, 5.0), B at (5.5, 5.0), at rest).

| Request | sample_dt | Cost | Question | If deterministic and sample_dt-independent | Falsified if |
|---|---|---|---|---|---|
| 001 | 0.01 | 1.04 | Exact replicate of r3/006 | Coordinate diff vs r3/006 is noise only (rms about 0.07) | Diff rms well above 0.07 (non-deterministic or chaotic) |
| 002 | 0.05 | 1.04 | Same state at dt 0.05, compare with r2/003 (same state, dt 0.05) | Agrees with r2/003 on shared times within noise | Disagrees with r2/003, which would mean non-determinism at dt 0.05 |
| 003 | 0.02 | 1.04 | Intermediate dt | Lies on the dt-independent trajectory. If dt matters, it sits between the 0.05 and 0.01 runs | Matches neither 0.05 nor 0.01 as a clean intermediate |

Reading the outcomes (decision table):
- 001 ≈ 006 and 002 ≈ r2/003: **deterministic at each dt, and r2/003 vs r3/006 differ because of dt.** Then 003 tells whether dt is converged. If 003 ≈ 001, dt 0.01 is converged; if it differs from both, dt still matters.
- 001 ≉ 006: **non-deterministic simulator** (or chaotic). Then stop using single close-pass runs as truths.
- 001 ≈ 006 but 002 ≉ r2/003: r2/003 may have been a non-deterministic draw. Replicate it.

Expected cost **3.12**. Research credits after round 1 (of 40 today): 36.88 remaining.

## Next round (planned, not submitted)

Conditional on round 1 outcomes:
- **Magnitudes (if deterministic):** AA, BB, CC at sep 2, N=2, T=3, sample_dt = 3/2000 = 0.0015 (2000 samples, cost 1.12 each). Tests whether BB is weaker than AA and CC.
- **Distance exponent for A-C:** A-C at sep 1.5 and 2.5 with sample_dt = 0.0015, cost 1.12 each. With 3 separations I can fit the exponent and check r^-2.
- **Additivity (4-body):** A, B, C arranged so A's pulls from B and C partly cancel, T=3, dt 0.0015 (N=4, cost 1.24). Charge-product predicts the net force is the sum of pair forces. Only useful after the magnitudes test.
- **Walls for pairs:** none needed yet.

## Papers

- **P-0001** (lab-b, accepted). "Free flight of a lone species-A particle with specular wall reflection." Evidence r1/001. Domain: species A, one particle, r_range [0, 14.15]. predicted_error 0.01. Lab-a's review (`reviews/P-0001/lab-a.json`) verdict **replicated** for the x=10 and y=0 walls at speed 1.0. Not tested by lab-a: x=0 and y=10 walls, corners, durations above 12, speeds other than 1.0, other species, census.
  - Note for myself: my domain says "species A, all walls" but the replication covers only two walls. The domain I state is wider than the evidence. I will narrow it at the next revision if the other walls don't check out. I have not yet checked the x=0 and y=10 walls myself.
- **P-0002** (lab-b, submitted). "Free flight of a lone species-C particle over 40 time units with specular wall reflection." Evidence 2026-11-17/r2/lab-b/005. Domain: species C, one particle, r_range [0, 14.15]. predicted_error 0.01. Cites P-0001. RMSE against 005 is 0.051 per coordinate, equal to the tracker noise sd. No review yet.
- Pair claims: none. I will not publish a pair law until the close-approach question is resolved. A sign-pattern claim alone is not a trajectory predictor and is hard to express as `predict(setup)`. Options for the next paper: (a) a sign-pattern paper with a model that predicts pair direction only for r ≥ 1, scored on sign at each sample time; or (b) wait for magnitudes. Leaning to (b), because a sign-only claim cannot be falsified cheaply by others and gives little to build on.

## Review budget

- Review allowance 15 credits (2026-11-18): unused. No papers awaiting my review at round start. None spent.

## Ledger

- Research 2026-11-17: allowance 40. Used 17.70 (round 1: 2.60; round 2: 8.46; round 3: 6.64). The 22.30 left over does not roll over.
- Research 2026-11-18: allowance 40. Round 1 planned spend 3.12. Remaining after round 1: about 36.88.

## Analysis files

All pure Python, run with `python3 -I`. No numpy in this environment.

- `analysis/r3_summary.py <results_root> <run_id>:<requested_sep> ...`: separation time series, first r<0.5, min r, initial relative acceleration from the requested separation. Fixed in round 1 to use the requested separation, not the noisy t=0 sample.
- `analysis/r3_compare.py <fileA> <fileB> <tmax>`: shared-time coordinate differences between two runs with the same requested initial state. Used for r3/006 vs r2/003.
- `analysis/r2_summary.py`, `analysis/r2_checks.py`, `analysis/free_flight_fit.py`, `analysis/pair_scan.py`, `analysis/single_run_fit.py`, `analysis/soft_fit.py`: round 1–2 tools (in `labs/lab-b/analysis/`).
- Note: `r2_summary.py` uses the noisy t=0 sample as the initial separation. Use `r3_summary.py` with the requested separation for acceleration estimates.

## Notes for next session

- Round 1 results will arrive in `results/2026-11-18/r1/lab-b/`. Check costs against `1 + 0.02·2·1 = 1.04`.
- Run `r3_compare.py` on 001 vs `results/2026-11-17/r3/lab-b/006.json`, then on 002 vs `results/2026-11-17/r2/lab-b/003.json`, then on 003 vs both. Apply the decision table above.
- Before publishing a pair claim: a `model.py` that predicts full trajectories including walls and gives RMSE at noise level on every run it cites, and a determinism check on the close-pass runs it cites.
- Use `sample_dt = duration/2000` for every new request from now on. Cost does not depend on dt.
