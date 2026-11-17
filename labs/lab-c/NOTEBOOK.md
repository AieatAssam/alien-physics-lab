# LAB-C notebook

## Round 1 — 2026-11-17

### State of knowledge
- Nothing measured yet. Season 1 uses species A, B, C (`protocol/season.json`), L = 10.0, difficulty 2.
- Unknown: cost coefficient `k`, tracker noise scale, whether particles interact, whether any species decays (census events), wall behaviour (elastic reflection assumed, not verified).

### Hypotheses (round 1 targets)
- H1: a lone particle moves ballistically (constant velocity) between wall bounces. Falsified if position residuals from a line/reflected-line fit exceed the noise floor estimated from the fit itself.
- H2: species does not change free motion (A and B with identical initial conditions give the same tracker trajectory within noise). Falsified by a systematic difference between 001 and 002 beyond noise.
- H3: two same-species particles do not interact at separation >= ~2 (request 003). Falsified by deflection from the ballistic prediction well beyond noise.
- H4 (no data yet): species C or others may decay; decays appear as census events. Not probed this round.

### Requests submitted (research account, 40-credit allowance)
- 001: single A, pos [2,5], vel [1,0], duration 10, dt 0.1, tracker+census. Tests H1, gives k and noise.
- 002: single B, same ICs. Tests H2.
- 003: A pair, pos [3,4] vel [1,0] and pos [7,6] vel [-1,0], duration 10, dt 0.1. Tests H3.
- Expected costs if k ~ 1: 11, 11, 21 (total 43, so 003 may be rejected in file order). If k <= 0.9 all three fit. Rejected requests cost nothing, so this is acceptable.
- Not requested: C-species probes and long-duration decay probes. Deferred until k is known.

### Plan for next round
1. Read k from result costs; recompute budget. If k is small, add a C-species single and a long (duration ~50–100) single run for decay/census events.
2. Estimate tracker noise sigma from the residuals of 001 after fitting a ballistic (with wall reflection) model. Put the noise estimate in `analysis/`.
3. Only publish a claim once the noise floor is known and at least one run discriminates H1 from an alternative (e.g. constant acceleration or drag). Scope the domain to what was measured: species, speed range, pair separation, duration.
4. Do not claim anything about speeds or separations outside those tested.

### Self-criticism
- 001 and 002 are the same geometry; if the particle motion is identical for A and B, that is weak evidence for a species-independent free motion only. It says nothing about species-dependent interaction.
- Speed 1.0 is one value. A ballistic law can hide a speed-dependent force that is zero at this speed.
