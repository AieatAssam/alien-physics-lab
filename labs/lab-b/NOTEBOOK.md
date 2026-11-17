# LAB-B notebook

Persona: bold theorist. Rule I am holding myself to: a striking law only after a discriminating run supports it, and stated with its domain.

## Season facts (measured)

- Season 1, species in use: A, B, C (`protocol/season.json`). Chamber [0, 10]^2.
- Cost constant **k = 0.020**, from two results: 001 cost 1.2 = 1 + k·1·10, and 002 cost 1.4 = 1 + k·2·10.
- Tracker noise: about **0.05 sd per coordinate** (from 001 residuals, n = 101 samples, 4 segments consistent).
- Census: no decay or appear events in either run.

## Results so far

### 001 (round 1, ok): one A particle, free flight
- Start (2.0, 2.0), nominal v = (1.0, 0.5), duration 10, dt 0.1.
- Best-fit velocity (0.9995, 0.4985). Reflected-line model fits with x-wall bounce at t≈8, no drift.
- Residuals: x sd 0.053, y sd 0.052, max |r| 0.15. Nominal-model RMSE 0.075 absolute (0.0075 normalized).
- Analysis: `out/labs/lab-b/analysis/round1_fits.py`.

### 002 (round 1, ok): A at (4,5) and B at (6,5), both at rest
- **H2 (no interaction) is rejected.** The pair accelerates toward each other from rest. Positions move about 0.2 units in the first 0.4 time units, well above noise.
- The pair crosses itself repeatedly, near t≈0.9, 3.8, 7.0, and 9.0 (separation minima 0.04 to 0.5). Within the time resolution I could check, there is no visible deflection at the crossing, so the particles seem to pass through each other rather than scatter. This is the most striking thing I have.
- Walls confound the rest of the run: B reaches x≈0.2 at t≈2.0, and A reaches x≈9.8 near t≈2.8. So I cannot read a clean turning point or energy budget from this run.
- Momentum-balance scan over t ≤ 1.6 (before any wall contact): m_B/m_A ≈ 0.71, rms 0.066, which is at the noise level. **Indicative only.**
- I do not yet have a force law. Dependence on distance, central direction, and species are all untested.

## Hypotheses (status after round 1)

- **H1, free flight (lone particle):** supported for species A, one trajectory, speed 1.1, duration 10, one wall reflection. Published narrowly as **P-0001**. Untested at other species, speeds, durations, corners.
- **H2, species-pair-specific interaction:** REVISED. The A-B pair does interact strongly. Open question is whether the interaction is species-specific or general. Tested next by 001 (A-A) and 006 (A-C).
- **H3, central pair force:** a pair at rest feels a force along the line joining them. Test: 004 (offset start, separation direction should stay at 14.04°).
- **H4, distance dependence:** the first close approach time from rest should lengthen with separation for an attractive central force. Tests: 002 (sep 4) and 003 (sep 1) against 002 of round 1 (sep 2).
- **H5, free flight holds for species C at high speed and long duration:** tested by 005 (C, speed 3.6, duration 40, many bounces). A drag or speed-dependent term would show here.

Persona note: a candidate general law, to be stated only if round 2 supports it: *in this season, every species pair attracts with a central force that does not scatter particles at short range (pass-through), and a lone particle moves freely.* I will not publish that as a law until H2, H3 and H4 have data.

## Round 2 plan (2026-11-17, r2)

Requests submitted (research account, all validated against `protocol/request.schema.json`, all `dt` chosen to resolve close approaches):

| Request | Setup | Duration, dt | Expected cost | Discriminates |
|---|---|---|---|---|
| 001 | A-A at rest, 2.0 apart | 10, 0.05 | 1.40 | Is the attraction species-pair specific? If AA attracts with the same timing as AB, it is general; if inert, specific. |
| 002 | A-B at rest, 4.0 apart | 10, 0.05 | 1.40 | Distance dependence: later first approach means a weaker or shorter-range force. |
| 003 | A-B at rest, 1.0 apart | 10, 0.05 | 1.40 | Distance dependence at short range; does the pass-through persist? |
| 004 | A-B at rest, offset (2.0, 0.5) | 1.5, 0.02 | 1.06 | Central test: separation direction should stay at 14.04°. Deviation means non-central. |
| 005 | C at (1,1), v = (3.0, 2.0) alone | 40, 0.1 | 1.80 | Free-flight edge: a fit to the reflected-line model within noise supports H5; drift means drag or self-force. |
| 006 | A-C at rest, 2.0 apart | 10, 0.05 | 1.40 | Does C interact with A, and like B? |

Total expected cost **8.46**. Credits left today after round 2 are about **28.9** (ledger 37.4 before; the ledger's 2.6 is round 1 spend).

Falsification criteria I committed to before running:
- 001 inert while 002 attracts → H2 holds as species-pair specific; the general-law persona note is dead.
- 002 first approach no later than 002 (round 1) at sep 2 → force does not weaken with distance over this range; the distance-law hypothesis is dead.
- 004 separation direction drifts more than 1° from 14.04° over the first 1.5 time units → H3 (central) is rejected.
- 005 residuals deviate from the reflected-line model by more than 0.15 absolute (3× noise) or show a trend → P-0001's scope cannot be extended to C at speed, and I should narrow the claim.

## Papers

- **P-0001** (lab-b): "Free flight of a lone species-A particle with specular wall reflection." Files in `out/papers/P-0001/`: `paper.md`, `claim.json`, `model.py`. Claim validates against `protocol/claim.schema.json`; `model.py` passes the gate import check and reproduces 001 at RMSE 0.0750 absolute.
  - `predicted_error` = 0.01 (normalized). The scorer's margin is 3×, so a falsification needs RMSE above 0.03 normalized (0.3 absolute).
  - Id collision risk: P-0001 is the first free number as far as this checkout shows. If another lab submits P-0001 in the same batch, the gate will reject one of us.
- No pair paper yet. I will publish the A-B pair claim only after round 2 gives a distance scan and a central-direction test.

## Review budget

- Review allowance 15 credits: unused. No papers awaiting my review at round start. None spent.

## Ledger

- Research 2026-11-17: allowance 40, used 2.6 (round 1: 1.2 + 1.4), remaining 37.4 before round 2.
- Round 2 submitted: 8.46 expected. Hold about 28.9 for a round 3 today.
- Notes for next session:
  - When results come back, check `cost` against 1 + 0.02·N·T to confirm k.
  - Check the samples at t = 0.05 steps for 001, 002, 003, 006 before fitting, since close approaches happen between samples at dt 0.1.
  - `round1_fits.py` is pure Python, no numpy in this environment. Run it with `python3 -I`.
