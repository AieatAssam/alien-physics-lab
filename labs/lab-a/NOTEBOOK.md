# LAB-A notebook

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted.

## Budget ledger (2026-11-17)
- Research allowance 40. Used 9.26 at start of round 3 (ledger). Round 2 results left 30.74 remaining.
- Round 3 requests planned: 14.04 research. If all accepted and run, 16.70 remains for the next day.
- Review allowance 15. Planned round 3 use: 6.00 (requests `r3/lab-a/012-014`, cite P-0001). Remaining after: 9.00.

## Established

### Cost constant k = 0.02 (confirmed across four (particles, duration) combinations)
- Formula `cost = 1 + k * N * T`, k = 0.02, matches every result so far:
  - N=1, T=5: 1.10 (r1/001, r1/002, r2/006)
  - N=2, T=5: 1.20 (r2/004, r2/005)
  - N=1, T=4: 1.08 (r2/003)
  - N=1, T=12: 1.24 (r2/001, r2/002)
- Budget ledger matches result costs exactly.

### Tracker noise sd about 0.05 per coordinate (zero mean)
- Round 1: residual sd 0.045-0.052 across four straight-line series (r1/001, r1/002).
- Round 2 wall fits: residual rms 0.046-0.055 across the elastic-model fits (r2/001, 002, 003).
- Pair repeats (r2/004 minus r2/005): difference sd 0.063-0.072 per coordinate. Pure noise predicts 0.05*sqrt2 = 0.071, so the repeats agree within noise.
- Noise is assumed independent of position, speed and species. Only tested for species A, speed 1, short runs.

### Walls (lone species-A, speed 1.0): elastic reflection, speed preserved
- x = 10 wall, start (2,5) v (1,0) (r2/001, r2/002; 12 s, bounce at t=8):
  - Elastic model rms 0.048 and 0.055. Wall-stop model rms 1.34 and 1.34. Wrap-around rms 3.73 and 3.74.
  - Post-impact x-velocity -0.988 and -0.999 (elastic predicts -1). Pre-impact +0.9998 and +1.0002.
  - Endpoint x(12) = 6.07 and 6.07, elastic predicts 6.0. (Note: the endpoint alone does not reject wall-stop; the full trajectory does.)
- y = 0 wall, start (5,2) v (0,-1) (r2/003; 4 s, bounce at t=2):
  - Elastic model rms 0.046. Wall-stop rms 0.83. Wrap-around rms 5.64.
  - Post-impact y-velocity +0.986 (elastic predicts +1), intercept -1.96 (elastic -2).
- Conclusion: for a lone species-A particle at speed 1, reflection is specular and speed is preserved, at both walls tested. Corners, x=0, y=10, speeds other than 1, and durations above 12 untested by me. P-0001 (lab-b) makes the same claim for lone A; see review below.

### Pair interaction exists (H5 REFUTED). Two species-A particles attract at separation about 3
- Pair run r2/004 and repeat r2/005: moving A from (2,5) v (1,0), stationary A at (6,5.5). Control r2/006 (stationary A alone) shows no drift (dx 0.015, dy -0.005, sd 0.05).
- Repeat agreement: summary statistics agree within 0.05.
- The stationary partner moves toward the moving particle from the start. The moving particle is pulled forward early:
  - Its x-deviation from the free line 2+t: +0.04 at t=0.5 (separation about 3.4), +0.19 at t=0.75 (separation about 2.9), +0.5 at t=1.0 (separation 2.2).
  - Closest encounter near separation 0.8 around t=1.5, followed by strong scattering. Both particles end up far from their free-line positions (moving particle y reaches 9.7 by t=5).
- No census events. No species change in 5 s.
- Free-motion model (no interaction) misses by rms 0.10-0.16; with a central attractive force the fit residual drops to 0.035 (about the noise of a pooled two-run mean). The interaction is real and repeatable.
- What I did NOT establish: the force law. A central power-law fit (K/r^p, optional softening) is ill-conditioned on this data. Fits over t<=0.9, 1.0, 1.1 give p=2.7, 3.2, 3.4 with K ranging 23 to 100. I will not publish a force law from it.

### Design error in my round-2 pair test (own it)
- I planned "closest approach 0.5 at t=4" as if the stationary partner were inert until the moving particle arrived. That was wrong: the partner is attracted from separation about 3.5, so the encounter happened near t=1.5 at x about 5, not at t=4. The pair run is therefore an interaction-dominated run, not the clean "no interaction at 0.5" baseline I intended. The H5 test is decided by the result above, not by the planned geometry.

## Hypotheses (status)
- H1 (lone-A ballistic free flight, species A, speed 1, short runs): supported (r1/001, 002; r2/001, 002).
- H2 (species does not change free motion): untested for B and C. Requests r3/009, r3/010 (lone B and C, same initial condition as r2/001) will decide.
- H3 (cost = 1 + k N T): supported. Four (N,T) combinations, k=0.02.
- H4 (no decay): untested. Request r3/011 (lone A, 100 s, census) is the first long test.
- H5 (no pairwise interaction at separation about 0.5): REFUTED. Attraction onset at separation about 3.5 for two species-A particles, scattering at separation about 0.8.
- H6 (wall reflection is elastic): supported for lone A at speed 1 on the x=10 and y=0 walls. Wall-stop and wrap-around rejected.
- H7 (new): pair attraction is central, depends on distance, and holds only for like species. Untested. Round 3 at-rest pairs (r3/001-008) map it.

## Round 3 (2026-11-17): requests submitted, results pending
All under `out/requests/2026-11-17/r3/lab-a/`. Expected cost in brackets.

Research:
- 001, 002 (1.04 each): at-rest pair of A at (2,5) and (5,5), separation 3.0, T=1.0. Short duration to stay short of contact. Repeat.
- 003, 004 (1.08 each): at-rest pair, separation 4.0, T=2.0. Repeat.
- 005, 006 (1.08 each): at-rest pair, separation 5.0, T=2.0. Repeat.
- 007, 008 (1.08 each): at-rest pair, separation 6.0, T=2.0. Repeat.
  - Predicted displacement per particle over T if a central attraction K/r^p with the round-2 fit (K=23, p=2.7) holds: about 0.5 for separation 4 at T=2, about 0.3 for separation 5. These are above the 0.05 noise over 100 samples.
  - Decision rule: the displacement-vs-separation curve gives a force-vs-distance estimate. If the four separations give a monotone curve with repeats agreeing, I will fit it and publish a narrow pair claim.
- 009, 010 (1.24 each): lone species-B and species-C particle, same initial condition as r2/001 (x-wall at t=8). Decides H2 across species.
- 011 (3.00): lone species-A, 100 s, census. Decides H4 (decay). Also long free flight with multiple reflections.

Review (account review, cites_paper P-0001, lab-b's lone-particle wall claim; domain max_particles 1, species A):
- 012 (3.00): 100 s lone A from (1,8) v (3.6,-2.1), many reflections. Tests P-0001 for duration and speed. Note: the claim states the model; I compare to its `model.py` predictor.
- 013 (1.40): exact corner hit: A from (8,8) v (3,3), corner at t=2/3. Tests reflection at corners.
- 014 (1.60): high speed about 7.8, A from (5,5) v (6,5), 30 s. Tests P-0001 above speed 3.6.

Analysis code: `out/labs/lab-a/analysis/` (fit_r2.py, pair_accel_r2.py, pair_fit_r2.py, make_round3_requests.py).

## Review of P-0001 (lab-b): replicated, partial
- `out/reviews/P-0001/lab-a.json`: verdict replicated, evidence r2/001-003.
- Scope: x=10 and y=0 walls for lone A at speed 1.0. I did not endorse the corner or high-speed parts. Round 3 requests 012-014 will test those and I will update or amend the review then.
- Noted for lab-b: their pair probe (A-B) shows strong interaction; that matches the A-A attraction above. Their claim's max_particles=1 keeps it clear of the pair physics.

## Plan and decision rules
1. Next session, read r3/001-008 (pair series). Compute displacement per particle over T for each separation, repeats first. If repeats disagree beyond noise (sd about 0.07 on pooled difference), treat that separation as unresolved.
2. Publish a pair claim only with a narrow domain: species A, 2 particles, separation range supported by data, time range supported by data. The predictor must not extrapolate past contact. Target paper P-0002 (P-0001 is taken). Draft after r3/001-008 are read.
3. If r3/009-010 show B or C free flight matches A, claim species-independence of free motion for speed 1 at the round-1 start. If not, name the species dependence.
4. If r3/011 (100 s census) shows any decay event, record its time and species transition before publishing anything about decay. No event in 100 s at 1000 samples (dt 0.1) would support "no decay for lone A over 100 s at speed about 1" only.
5. Review 012-014 against P-0001's `model.py` predictor: compute residual rms, compare to 3*predicted_error (0.03 chamber units). Verdict replicated, narrowed, or falsified accordingly.
6. Budget after round 3 (if all run): 16.70 research, 9.00 review.

## What would change my mind
- If the at-rest pair displacements are not monotone in separation, the force is not a simple central function of distance. I would then stop describing a force and report only the observations.
- If r3/011 shows census events, the apparent no-decay evidence from short runs is not enough for any claim.
- If r3/009 or 010 deviate from the A-wall result (x-wall at t=8, same initial condition), species matters for walls, and H2 and H6 must be stated per species.
- If repeats (r3/001 vs 002, etc.) disagree beyond noise, the effect size is not reproducible and I treat that measurement as inconclusive.

## Self-criticism
- The pair data are from one geometry (both particles on the line y about 5, moving partner at speed 1 along +x). Attraction direction and strength could depend on the velocity direction of the moving particle. The at-rest series is designed to remove that.
- I chose an interaction test whose geometry I did not check against the free-motion prediction. The planned H5 test could not have decided the question as designed. Future geometry: at-rest pairs first, then moving.
- The k=0.02 cost value rests on four distinct (N, T) pairs. Good, but still no check at N=16.
- The noise estimate covers species A at speed 1 only. It is not a global noise level.
- My review of P-0001 is partial and uses walls only. I did not test corners or speeds. Do not read the verdict as covering the full claim.
