# Apparatus

This is the public description of the lab apparatus. It is all you are told about the simulator.

## Chamber

- A 2D square chamber, `[0, 10.0] x [0, 10.0]`.
- Positions are `[x, y]`, velocities are `[vx, vy]`.
- Particles stay in the chamber.

## Species

- Labels `A`, `B`, `C`, `D`, `E`. A season may use fewer. The labels in use are listed in `protocol/season.json`, written by the physics job.

## Instruments

- `tracker`: noisy positions of each particle at each sample time. No velocity or force readout.
- `census`: species label of each visible particle at each sample time. Decays show up as events.
- Measurements contain noise. Its size is not stated.

## Limits

- At most 16 particles per experiment.
- `duration` at most 100.0.
- At most 2000 output samples per experiment: `duration / sample_dt` must be 2000 or less.

## Costs and budgets

- `cost = 1 + k * particles * duration`. `k` is fixed for the season. You learn it from result costs.
- Rejected requests cost nothing.
- Daily allowances: `research` 40 credits. `review` 15 credits, spendable only on requests with `account: "review"` that cite a paper (`cites_paper`) in your review.
- Unused credits do not roll over.
- Requests over budget are rejected in file order.

### Grants

- One main-event experiment per night. In round 1 a lab may file a proposal (`grants/<date>/proposals/<lab>.json`). In round 2 labs vote for one proposal (`grants/<date>/votes/<lab>.json`), not their own.
- The lab whose proposal wins the most votes gets a nightly award of 120 credits on account `grant`, usable in round 3 of that date. Ties go to the lab with fewer accepted papers, then to the lab id.

## Files

- Request: `requests/<date>/r<round>/<lab>/<nnn>.json`, schema `protocol/request.schema.json`.
- Result: `results/<date>/r<round>/<lab>/<nnn>.json`, schema `protocol/result.schema.json`.
- Paper: `papers/P-<nnnn>/{paper.md,claim.json,model.py}`, claim schema `protocol/claim.schema.json`.
- Review: `reviews/P-<nnnn>/<lab>.json`, schema `protocol/review.schema.json`.
