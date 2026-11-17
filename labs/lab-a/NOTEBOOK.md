# LAB-A notebook

## Season 1 context
- Chamber [0,10]^2. Species in use: A, B, C (`protocol/season.json`). L = 10.0, difficulty 2.
- Budget: research 40 credits/day. No review credits used so far. No papers exist yet, so no reviews are due.
- Unknowns: cost constant k (inferred, see below), tracker noise sigma (estimated), whether particles interact, whether species decay (census events), wall behaviour, whether free motion depends on species.

## Established so far

### Cost constant k (round 1, requests 2026-11-17/r1/lab-a/001 and 002)
- Both runs: 1 particle, duration 5.0, cost 1.1 each.
- Under the stated form cost = 1 + k * particles * duration: k = 0.02.
- Caveat: one (particles, duration) pair only. The pair test in round 2 (2 particles, 5 s, expected cost 1.2) and the 12 s wall runs (expected 1.24) give independent checks of the linear form. Budget ledger agrees: research_used 2.2 after two runs of 1.1.

### Tracker noise (round 1, analysis in `out/labs/lab-a/analysis/fit_r1.py`)
- Free straight-line fit of species-A particle, v = (1, 0), 101 samples over [0, 5].
- Run 001: x = 2.0035 + 0.9983 t, y = 4.9954 + 0.0040 t. Residual sd x = 0.052, y = 0.045.
- Run 002: x = 2.0048 + 0.9994 t, y = 5.0018 - 0.0024 t. Residual sd x = 0.050, y = 0.046.
- Residual lag-1 autocorrelation within +/-0.1 in all four series: no visible structure, consistent with independent noise.
- Run-to-run difference: mean dx = -0.004, dy = +0.009; per-measurement sd from differences /sqrt2: x = 0.050, y = 0.047. Consistent with pure measurement noise, with no run-to-run systematic difference detected.
- Working estimate: tracker noise sd about 0.05 per coordinate, similar in x and y. Based on 2 runs x 101 samples in one geometry, so the uncertainty on the sd is roughly 0.004 in the sampling sense. It does not cover noise that varies with position, speed or species.
- Fitted intercepts agree with the requested start (2, 5) to within about 0.01, so the noise appears zero-mean.
- Fitted velocity = (1, 0) within 0.003 in both runs. Free motion over t <= 5 is straight-line within that tolerance.

### Trajectory range in round 1
- Particle never came closer than 2.0 to x = 2 or reached x = 7.02. No wall was reached, so no wall behaviour is known.

## Hypotheses (status)
- H1 (ballistic free flight): supported only for t <= 5, x in [2, 7], speed 1, species A, one particle. Not yet tested to the walls. Round 2 tests the walls.
- H2 (species does not change free motion): untested. Round 1 used only species A.
- H3 (cost = 1 + k N T): consistent so far with one point. Round 2 gives 3 more cost points.
- H4 (no decay): untested. Needs a long single-particle census run (planned for a later round, cost about 3 credits for 100 s).
- H5 (no pairwise interaction at separation about 0.5): untested. Round 2 pair test.
- H6 (wall reflection is elastic): untested. Round 2 walls. Competing: wall stop, wrap-around, speed change on impact.

## Round 2 (2026-11-17) requests, research account
All under `out/requests/2026-11-17/r2/lab-a/`. Expected cost in brackets. Total expected about 7.1 credits.
- 001 (1.24): single A, [2,5], v (1,0), T = 12. Hits x = 10 at t = 8.
  - Elastic reflection: x(12) = 6.0.
  - Wall stop: x(12) = 10.0.
  - Wrap-around: x(12) = 4.0.
- 002 (1.24): exact repeat of 001.
- 003 (1.08): single A, [5,2], v (0,-1), T = 4. Hits y = 0 at t = 2.
  - Elastic reflection: y(4) = 2.0.
  - Wall stop: y(4) = 0.0.
  - Wrap-around: y(4) = 8.0.
- 004 (1.20): pair. Moving A from [2,5] v (1,0), stationary A at [6,5.5]. Closest approach 0.5 at t = 4. The moving particle's y should stay at 5.0 (baseline), and the stationary one should stay at (6, 5.5).
- 005 (1.20): exact repeat of 004.
- 006 (1.10): control. Stationary A alone at [6,5.5]. Used to check drift without a partner.

## Plan and decision rules
1. Wall result (001/002/003). If both repeats agree on one of the three wall models, the reflection/stop/wrap outcome is recorded. Only then is a free-flight claim worth publishing, because a claim with species and count only (the claim domain has no duration or speed field) would be scored against wall-touching exam setups.
2. Pair result (004/005 against 006 and the round 1 baseline). If the stationary A is displaced more than about 0.1 from (6, 5.5) in a repeat-consistent way, or the moving particle's y deviates from 5.0 by more than about 0.1 near t = 4, I call it interaction. If not, I narrow the claim to "no interaction detected at separation >= 0.5 for species A, 2 particles".
3. No paper this round. Publishing a claim that the scorer can't restrict to the tested time range would be overreach. I will publish P-0001 in the next session, after the wall results are read.
4. Next round candidates, to decide after results: species B and C single-particle free motion at the round 1 ICs (cost 1.1 each), a 100 s single-A census run for decay (cost about 3.0), and a same-species pair at larger separation for the distance dependence of any interaction.

## What would change my mind
- If the wall runs give a speed change after impact, then the model is not simple specular reflection and the claim must name it.
- If 004 and 005 disagree with each other beyond noise, I treat pair effects as unresolved, not as evidence either way.
- If the control 006 drifts, the baseline for the pair run is no longer the single-particle fit.

## Self-criticism
- Everything so far is one speed (1.0), one direction (+x), one species (A), and one start point. A law that is zero here can hide speed, direction or species dependence.
- The noise estimate comes from a single geometry and was checked only in x and y over t <= 5. It should not be quoted as a global noise level.
- k = 0.02 rests on one cost measurement under an assumed linear form. I will call it "consistent with" until more cost points agree.
- Budget is 37.8 credits remaining before round 2. After round 2 about 30.7 credits remain for the decay and species tests.
