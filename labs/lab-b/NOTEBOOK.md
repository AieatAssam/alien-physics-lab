# LAB-B notebook

Persona: bold theorist. Rule I hold myself to: a striking law only after a discriminating run supports it, and stated with its domain.

## Season facts (measured)

- Season 1, species in use: A, B, C (`protocol/season.json`). Chamber [0, 10]^2.
- Cost constant **k = 0.020**. Confirmed by three costs in round 2: 001 cost 1.40 = 1 + k·2·10; 004 cost 1.06 = 1 + k·2·1.5; 005 cost 1.80 = 1 + k·1·40.
- Tracker noise: **sd about 0.05 per coordinate**. Round 1 gave 0.053/0.052 (101 samples). Round 2 005 gave 0.052/0.050 (401 samples). Consistent.
- Census: no decay or appear events in any run so far (r1 001-002, r2 001-006).
- Masses, relative to m_A = 1, from centre-of-mass conservation before wall contact (`analysis/r2_checks.py`). These are rough, because the window is short and the estimates vary by run:
  - A-A: 0.98 (r2/001), so equal masses.
  - A-B: 0.55 (r2/002), 0.74 (r2/003), 0.70 (r1/002). I take m_B ≈ 0.7 m_A with spread ±0.1.
  - A-C: 0.40 (r2/006). So m_C ≈ 0.4 m_A.

## Results so far

### Round 1 (r1)

- **001 (ok), one A particle, free flight.** Nominal v = (1.0, 0.5), duration 10, dt 0.1. Best-fit velocity (0.9995, 0.4985). Reflected-line model fits with one x-wall bounce, no drift. Basis for **P-0001**.
- **002 (ok), A at (4,5) and B at (6,5), both at rest, dt 0.1.** The pair accelerates toward each other. The separation first drops below 0.5 at t≈0.9. Confirmed attraction, not inert.

### Round 2 (r2), all status ok, all 0 census events

- **001, A-A at rest, 2.0 apart, dt 0.05.** A-A attracts. First r<0.5 at t=0.65 (A-B at the same separation: t≈0.9). So the attraction is not specific to A-B. The pair passes through its partner (min r≈0.10 at t≈0.75) and oscillates, then separates to the walls.
- **002, A-B at rest, 4.0 apart, dt 0.05.** First r<0.5 at t=2.55. The approach is far slower than at separation 2. Best single-run power-law fit to near 0.05 noise (n between 0.5 and 1.5 all fit).
- **003, A-B at rest, 1.0 apart, dt 0.05.** First r<0.5 at t=0.30, then repeated passes with min r≈0.08–0.2. Bound oscillation through the centre for t≤5, then wall bounces. A simple power law does not fit this run (rms 0.16–0.37 vs noise 0.05). See the close-approach section.
- **004, A-B at rest, offset (2.0, 0.5), dt 0.02, T 1.5.** Central-force test. Pre-contact separation angle over t∈(0, 0.6]: mean 14.19°, sd 2.18° (n=30), expected 14.04°, so the line direction holds within about ±0.4°. After the pass (t∈[1,1.5]) the angle is 13.71° mod 180, also consistent. **Central force supported (H3).**
- **005, single C, speed 3.6, duration 40, dt 0.1.** Reflected-line fit: velocity (3.0000, 2.0000), exactly nominal. Residual sd 0.052 (x), 0.050 (y). Max |r| 0.175. Segment means within 0.005 of zero over four 10-unit segments with many bounces. **Free flight holds for C at high speed and long duration (H5 supported).** Basis for **P-0002**.
  - Note on my round-2 criterion: "residual above 0.15 absolute" was meant as a systematic deviation. A single sample at 0.175 is about 3.5 sd among 802 coordinates, so it is what noise gives, not a deviation.
- **006, A-C at rest, 2.0 apart, dt 0.05.** **A and C repel.** Separation grows from 2.10 to 3.67 by t=1.0 and to 7.6 by t=2.2 (then wall contact). This is the first sign-reversed pair. The round-2 persona note ("every species pair attracts") is **falsified**.

## Hypotheses (status after round 2)

- **H1, free flight of a lone particle (A):** supported by r1/001. Published as **P-0001**. Untested at speeds above 1.1 for A.
- **H5, free flight of a lone particle (C), high speed, long run:** supported by r2/005. Published as **P-0002**.
- **H2, pair interaction is species-pair specific:** Now **strongly supported**, with signs. Known: A-A attracts (001), A-B attracts (r1/002, r2/002–004), A-C repels (006). Untested: B-B, B-C, C-C.
- **H3, central pair force:** supported by r2/004 (angle within about ±0.4° of 14.04°, pre and post pass). Only tested for A-B. Open for A-C and A-A.
- **H4, distance dependence of attraction (A-B):** supported qualitatively. Time to r<0.5 from rest: 0.30 at sep 1, about 0.9 at sep 2 (r1/002 and offset 004), 2.55 at sep 4. The far field (sep 4, offset) fits a power law with n between 0.5 and 1.5 within noise. For A-C, the distance dependence is still open.
- **H6 (new): the A-C repulsion decays with separation.** Test: r3/005 (sep 4) vs r2/006 (sep 2).
- **H7 (new): the sign pattern follows the C species.** Test: r3/001–003 (BB, CC, BC).
- **H8 (new): short-range (r<1) pair dynamics are a central power law.** NOT supported as measured. See the close-approach section.

## Close-approach problem (open)

- Joint fit of the three A-B runs (002, 003, 004 and r1/002) and the A-A run (001) with one power law F = k·r^(-n), free masses, and exact requested initial states gives rms 0.28–0.34 (noise 0.05). Not usable.
- Per-run: far-field runs fit at noise level (r2/002 rms 0.05, r2/004 rms 0.05–0.07). Close-approach runs do not: r2/003 rms 0.16 at best, r1/002 rms 0.10 at best (n = 1).
- Softening (F = k·r/(r²+ε²)^((n+1)/2), ε ∈ {0, 0.2, 0.4, 0.7}) does not help. The grid picks ε = 0.
- Candidate explanations, not yet separated:
  1. The simulator's integration step is coarse, so close passes are not resolved. Requests 003 and 006 (dt 0.01 over T 1) are designed to test this.
  2. The force has a shape other than a power law or a softened power law at short range.
  3. The pair force is not purely central at short range, or it depends on velocity. 004 shows no deflection at the 1.0-2.0 scale, but a test at short range has not been done.
- Do not publish a pair law until this is resolved. The far-field law alone is not a usable predictor, since exam setups will contain close approaches.

## Round 3 plan (2026-11-17, r3)

Requests written and checked against the schema constraints (required fields, id pattern, species, lengths, duration/dt limit). Each is a 2-particle run at rest. Costs use k = 0.020.

| Request | Setup | T, dt | Cost | Question | Prediction if my picture holds | Falsified if |
|---|---|---|---|---|---|---|
| 001 | B-B at (4,5),(6,5) | 3, 0.02 | 1.12 | Does B-B attract (as A-A)? | Attraction, first r<0.5 near t≈0.6–0.9 | B-B inert or repulsive |
| 002 | C-C at (4,5),(6,5) | 3, 0.02 | 1.12 | Is C the repulsive partner? | **Repulsion** (C repels everything) | C-C attracts |
| 003 | B-C at (4,5),(6,5) | 3, 0.02 | 1.12 | Does the sign follow C? | **Repulsion**, like A-C | B-C attracts |
| 004 | A-C at (4.5,5),(5.5,5) | 3, 0.02 | 1.12 | Does A-C repel at short range too? | Repulsion, separation grows monotonically over t≤1 | A-C attracts at r=1 (sign change) |
| 005 | A-C at (3,5),(7,5) | 3, 0.02 | 1.12 | Distance dependence of repulsion | Early acceleration of separation **smaller** than in r2/006 (sep 2) | Acceleration at sep 4 ≥ at sep 2 |
| 006 | A-B at (4.5,5),(5.5,5) | 1, 0.01 | 1.04 | Close-approach resolution; determinism replicate of r2/003 | Trajectory agrees with r2/003 within noise at shared times; dt 0.01 shows the turnaround is resolved | Disagreement beyond noise (non-deterministic sim) or residual stays at 0.15 with a fine grid (law is not a central power law) |

Expected total cost **6.64**. Research credits after this round: 28.94 − 6.64 ≈ **22.3**.

Claims I will make from round 3 only if the data support them:
- If 002 and 003 both repel: "the repulsive partner is C" is a candidate general rule. Then state the domain as species pairs with C, plus AA and AB attraction, and nothing for B-B unless 001 is clean.
- If 002 attracts while 003 and 006-A-C repel: the sign is not set by C alone; I will not publish a general rule.

Round 4 candidates (not submitted; only if round 3 is clean): a 4-body additivity test (A, B, C arranged so that A's forces from B and C partly cancel; T 3, cost 1.24); a longer A-C run at sep 2 for the walls and the mass ratio.

## Papers

- **P-0001** (lab-b, published round 1): "Free flight of a lone species-A particle with specular wall reflection." Evidence r1/001. Domain: species A, one particle, r_range [0, 14.15]. predicted_error 0.01. Model reproduces 001 at RMSE 0.075 absolute.
- **P-0002** (lab-b, written this round, not yet submitted to the gate): "Free flight of a lone species-C particle over 40 time units with specular wall reflection." Evidence 2026-11-17/r2/lab-b/005. Domain: species C, one particle, r_range [0, 14.15]. predicted_error 0.01. `cites` P-0001. `model.py` is the reflected-line law. Check: RMSE against 005 is 0.051 absolute per coordinate (0.0051 normalized), which equals the tracker noise sd. Files in `out/papers/P-0002/` (paper.md, claim.json, model.py).
  - Id collision risk: P-0002 is the next free number in this checkout (only P-0001 is present). If another lab submits P-0002 in the same batch, the gate will reject one of us.
- Pair claims: none yet. I will not publish a pair law until the close-approach problem is resolved or narrowed to a domain that avoids it (for example, r ≥ 2 only, which fits at noise level for A-B).

## Review budget

- Review allowance 15 credits: unused. No papers awaiting my review at round start. None spent.

## Ledger

- Research 2026-11-17: allowance 40. Used before round 3: 11.06 (round 1: 2.6; round 2: 8.46). Remaining at start of round 3: 28.94.
- Round 3 submitted: 6.64 expected (requests 001–006). Remaining after round 3 expected: about 22.3.

## Notes for next session

- Round 3 results will arrive in `results/2026-11-17/r3/lab-b/`. Check each `cost` against 1 + 0.02·N·T.
- Check that r3/006 agrees with r2/003 at shared times, within noise. Disagreement beyond noise means the simulator is not deterministic for identical setups, which changes how I treat all repeats.
- Analysis scripts are in `out/labs/lab-b/analysis/` and all are pure Python. Run them with `python3 -I`. There is no numpy in this environment.
  - `r2_summary.py <dir> <ids...>`: separation time series and local minima for pair runs.
  - `r2_checks.py`: central-angle test (004), COM mass ratios, first-approach times.
  - `free_flight_fit.py <result> x0 y0 vx vy`: reflected-line fit and segment drift.
  - `pair_scan.py`, `single_run_fit.py`, `soft_fit.py`: power-law and softened force fits, from the exact requested initial state. Note that a fit's rms of 0.05 is noise; 0.1 and up means the law is missing something.
- Superseded: an earlier joint fit (pair_fit.py) started from the noisy t=0 sample and got rms 0.69. Deleted. Do not reuse.
- Before publishing a pair claim: a `model.py` that predicts full trajectories, including walls, and gives RMSE at noise level on every run it cites.
