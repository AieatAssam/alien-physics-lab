# LAB-B notebook

## 2026-11-17, round 1

### State
- Season 1, species in use: A, B, C (from `protocol/season.json`). Chamber 10 x 10. Cost constant `k` unknown.
- No results yet. No papers yet.

### Working hypotheses (all unverified, stated to be falsified)
- H1 (free flight): an isolated particle moves in a straight line at constant velocity between wall bounces, with specular reflection at the walls. Predicts x(t) = x0 + vx*t and y(t) = y0 + vy*t with reflection, noise-only deviations.
- H2 (species-dependent pair force): a central pair force exists only between some species pairs. Pair A-B at 2.0 separation at rest should show a separation change beyond noise if the force is nonzero; if it stays at 2.0 within noise, the pair is inert at this separation.

### Plan for round 1 (budget: 40 research credits)
- 001: one species-A particle, duration 10, sample_dt 0.1, tracker+census. Tests H1 and measures noise scale from residuals against the straight-line fit. Cost = 1 + k*10, so this also reveals k.
- 002: A and B at rest 2.0 apart, duration 10. Tests H2 for the A-B pair.
- Next round, depending on results: vary separation to map the force law, and test A-A and B-B. Add C.

### Domain and risk
- Claims will be scoped to the chamber and to the sampled durations. I do not yet claim any force law.
- Persona note: I would like one striking general law, but I will not state one until a result supports it.

### Ledger
- Round 1 requests submitted: 001 (A free flight), 002 (A-B pair). Expected cost is 1 + k*10 each for one and two particles; the pair costs 1 + 2k*10. Total expected cost is 2 + 30k, which is within 40 credits if k <= 1.27. If the pair request is rejected for budget, I will resubmit it next round.
