# LAB-A notebook

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted.

## Budget ledger

### 2026-11-17 (closed)
- Research allowance 40. Used 23.3 in total across rounds 1-3 (ledger). Round 3 matched the plan: 14.04 research (001-011, 013) and 6.00 review (012-014). Unused credits do not roll over.

### 2026-11-18 (round 1, this session)
- Research allowance 40. Planned: 14.54 (requests 001-013). Unused after plan: 25.46.
- Review allowance 15, spendable only on requests citing a paper I review. Planned: 6.20 (014-016, cite P-0002). Unused after plan: 8.80.
- Request costs checked against `cost = 1 + 0.02 * N * T` (all 16 requests, see table below). Requests validated against `protocol/request.schema.json` by hand (jsonschema not installed in this environment; constraint check only, not a full schema validation).

## Established

### Cost constant k = 0.02
- Four (N, T) combinations so far, all matching `1 + 0.02 N T`: (1,5) 1.10, (2,5) 1.20, (1,4) 1.08, (1,12) 1.24. Result costs match the ledger exactly.
- Not yet checked at N = 16. Round-1 request 013 (16 particles, T = 1, predicted cost 1.32) does this.

### Tracker noise sd about 0.05 per coordinate (zero mean)
- Round 1: residual sd 0.045-0.052 on straight-line series.
- Round 2: wall-fit residual rms 0.046-0.055. Pair repeat difference sd 0.063-0.072 (pure noise predicts 0.071).
- Round 3: residual rms vs P-0001 and P-0002 predictors 0.047-0.057 across lone-particle runs (001-014). vs P-0003 predictor 0.047-0.059 across at-rest pairs.
- Noise is assumed independent of position, speed and species. The lone-particle checks cover species A, B and C; the pair checks cover species A only.

### Lone-particle free flight with specular walls (H1, H2, H6): supported
- Species A, speed 1.0: x = 10 and y = 0 walls, elastic reflection, speed preserved (r2/001-003). Wall-stop and wrap-around rejected.
- Species A, speed up to 7.8, duration 100, corner hit: all consistent with the P-0001 predictor at noise level (r3/011-014). Corner reflection at (10,10) at t = 2/3 included.
- Species B and C (speed 1.0, 12 time units, x = 10 wall at t = 8): consistent with the same reflected-line predictor (r3/009, r3/010). Species independence of free motion holds for this case.
- Species C at speed 1.0, 12 units: consistent with P-0002's predictor (r3/010). Speed 3.6 and duration 40 are lab-b's run; my own edge tests for P-0002 are queued (2026-11-18/r1/lab-a/014-016).

### Lone-particle decay (H4): no event in one run
- Lone A, speed 0.8, 100 time units, census every 0.1: 0 census events (r3/011). This supports only "no decay of a lone A over 100 time units in this one run". Not a general claim.

### Pair attraction between two species-A particles at rest (H5 refuted; H7 supported, narrow)
- Round 2 (r2/004-006): a moving A and a stationary A attract (H5 that they do not interact is refuted). The force law was not fit from that run.
- Round 3 at-rest series (r3/001-008): two A at rest, separation 3, 4, 5, 6, repeated at each separation, T = 1 or 2.
  - Fit of K / r^P (two-body integration, both particles, both coordinates): best P = 2.50, K = 17.74, rms 0.051 per coordinate. P in 2.25 to 2.75 gives rms 0.054-0.055; P = 2.0 or 3.0 give rms 0.062-0.064 (clearly worse). Noise is 0.05, so P = 2.5 is the best fit and the residual is at noise level.
  - Per-run best K at P = 2.5: 17.2, 17.7 (sep 3), 17.7, 17.8 (sep 4), 18.2, 17.9 (sep 5), 16.3, 16.8 (sep 6). Repeats agree at each separation. The sep-6 runs sit about 7% lower.
  - Closest approach in the sep-4 runs (003-004) is about 0.14 at t = 2. The fit still holds there, but no claim is made below that separation.
  - Screened form K exp(-r/lambda)/r^2 fits the same data slightly better: lambda = 8 gives SSE 7.26 vs 7.49 for the power law. So the exponent and screening length are not separated by these data. Far-field runs (round-1 006-009) will discriminate: the two forms differ by about 15% at separation 8.5-9.
  - No census events in any pair run (002-008) over 2 time units.
- Written up as P-0003 (`out/papers/P-0003/`): claim domain species A, two particles, separation 3-6, at rest, duration up to 2. predicted_error 0.01 (normalized, 2x the observed rms). Constants are fit to these same runs; the prediction test is round 1.

### Note on my own earlier estimates (fixed)
- My quadratic fit to the at-rest runs printed 2 x the x^2 coefficient (the basis is 0.5 t^2, so the coefficient is the acceleration). It also gives a time-averaged value, not the initial acceleration, because the force grows as the pair closes. Both points are why the two-body fit is used instead. Nothing published depends on the quadratic numbers.

## Hypotheses (status)
- H1 (lone-A ballistic free flight): supported. Now extended to speed 7.8 and 100 time units (r3/011-014).
- H2 (species does not change free motion): supported for B and C at speed 1, 12 units, x=10 wall (r3/009-010). Not tested at other speeds for B or C; lab-b's P-0002 covers C at speed 3.6, duration 40.
- H3 (cost = 1 + k N T): supported at four (N, T) pairs; N = 16 check queued (round 1 request 013).
- H4 (no decay): one run, lone A, 100 time units, census: 0 events (r3/011). Not yet tested with pairs or other species.
- H5 (no pairwise interaction at separation about 0.5): refuted (round 2).
- H6 (wall reflection is elastic): supported for lone A at speed 1 on the x=10 and y=0 walls, and for lone A at speeds 4.2 and 7.8, including a corner hit (r3/012-014). Extended to species B and C at speed 1 (r3/009-010).
- H7 (pair attraction is central, depends on distance, power-law-like at separations 3-6, species A only): supported at noise level for P = 2.5, K = 17.74 (P-0003). The form is not confirmed (screened inverse square fits equally well). Far-field, species and isotropy tests are queued (round 1).
- H8 (new): the pair force is isotropic (direction-independent) and the same for B-B, C-C, A-B and A-C pairs. Round 1 requests 001-005 (species) and 010-011 (isotropy) test this.

## Reviews
- P-0001 (lab-b, lone A free flight): `out/reviews/P-0001/lab-a.json`. Verdict replicated for the claim as written (species A, one particle), with evidence r2/001-003 and r3/011-014. Corners, speeds up to 7.8 and durations up to 100 are now covered. x=0 and y=10 walls on their own are still not separately tested.
- P-0002 (lab-b, lone C, speed 3.6, 40 units): `out/reviews/P-0002/lab-a.json`. Partial, narrow verdict: replicated at speed 1.0, 12 units (r3/010) only. The claim's own scope (speed 3.6, 40 units, corners, long slow run) is queued as review requests 014-016. I will update this review when those results arrive. If any of them disagrees with the predictor by more than 0.03 normalized, I will call it falsified or narrowed per the results.

## Round 1 (2026-11-18): requests written, results pending
Output: `out/requests/2026-11-18/r1/lab-a/001-016.json`. Generator: `out/labs/lab-a/analysis/make_round1_requests.py`.

| id | setup | T | cost | purpose |
|---|---|---|---|---|
| 001, 002 | A-B at rest, sep 5 | 2 | 1.08 each | species dependence of pair force (repeat) |
| 003 | B-B at rest, sep 5 | 2 | 1.08 | species dependence |
| 004 | C-C at rest, sep 5 | 2 | 1.08 | species dependence |
| 005 | A-C at rest, sep 5 | 2 | 1.08 | mixed species |
| 006, 007 | A-A at rest, sep 8 | 4 | 1.16 each | far field; power law vs screened form |
| 008, 009 | A-A at rest, sep 9 | 4 | 1.16 each | far field (repeat) |
| 010 | A-A at rest, sep 4, 45 degrees | 2 | 1.08 | isotropy |
| 011 | A-A at rest, sep 4, along y | 2 | 1.08 | isotropy |
| 012 | A-A at rest, sep 2 | 0.5 | 1.02 | near-field low end of domain |
| 013 | 16 species-A at rest, 4x4 grid, spacing 2 | 1 | 1.32 | cost constant at N = 16 |
| 014 | review: lone C, speed 8.6 (7,-5) from (3,6) | 40 | 1.80 | P-0002 at high speed (cites P-0002) |
| 015 | review: lone C, corner hit (8,8) v (3,3) | 20 | 1.40 | P-0002 corner (cites P-0002) |
| 016 | review: lone C, speed 0.22 from (5,5) | 100 | 3.00 | P-0002 drift over long run (cites P-0002) |

Expected research total 14.54, review 6.20.

## Decision rules for next session
1. Read round-1 results 001-013 as they arrive. Check repeats first (001 vs 002, 006 vs 007, 008 vs 009). If a repeat pair disagrees beyond noise, treat that measurement as unresolved and say so.
2. Species (001-005): fit each species pair with the same two-body fit. If A-B, B-B, C-C, A-C agree with A-A at the same separation, state species-independence of the pair force for separations 3-6 (new paper). If not, name the species dependence and its size.
3. Far field (006-009): compare the power law (K = 17.74, P = 2.5) with the screened form (lambda = 8, K = 15). Whichever fits the 8-9 separation data better, the other is ruled out if the difference exceeds 3 times the noise on the fitted displacement. If neither fits, say so and refit P-0003's domain to match.
4. Isotropy (010-011): compare with the horizontal sep-4 runs (r3/003-004). Same K within noise → central, isotropic. A discrepancy → the force depends on direction; then P-0003's "central" claim is narrowed.
5. Near field (012): compare to the power-law prediction at separation 2 (about 3.1 per particle at rest). Use it to decide whether P-0003's domain can extend below 3.
6. N = 16 (013): compute the cost from the result and check it is 1.32. Mismatch → revise k.
7. P-0002 edge tests (014-016): compare each against P-0002's `model.py` with `out/labs/lab-a/analysis/compare_model_r3.py`. Residual rms within 0.03 normalized (0.3 chamber units) → replicated for that test. Outside → falsified or narrowed, and write it up.
8. P-0003 update: a prediction test passes if 006-009 and 010-011 are inside the noise band of the P-0003 predictor (rms per coordinate about 0.05 for T up to 4 and sep 8-9). If they are not, retract the constants or narrow the domain before anything else is published.

## What would change my mind
- If the far-field runs (006-009) fall well off the power-law prediction (more than 15%), the force is not a power law over 3-9 and P-0003 must be narrowed or replaced.
- If the isotropy runs (010-011) disagree with the horizontal runs, the force is not central. Then P-0003's central form is wrong.
- If the species runs show a census event, a species change under interaction is possible and every pair claim needs a census check.
- If any P-0002 edge test (014-016) departs from the predictor by more than 3 times predicted_error, my partial review changes to falsified or narrowed.
- If the 16-particle cost is not 1.32, k = 0.02 does not hold at N = 16 and all cost-based budgeting needs revision.

## Self-criticism
- P-0003 is fit to the same 8 runs that set K and P. The residual test is in-sample. The prediction test is round 1 (006-011). I have said so in the paper, but the claim's predicted_error (0.01 normalized) should be read as a consistency level, not as a forecast.
- The power law (P = 2.5) is an effective description. The screened inverse-square form fits as well on current data, and I say that in the paper. I have no evidence yet that P = 2.5 is a physical exponent.
- Per-run best K at separation 6 is about 7% lower than at separation 4. Noise alone may explain it, but the two sep-6 runs agree, so it could be real. It is the first thing the far-field and screened-form tests should address.
- Round 2's moving-pair run (r2/004-005) reached separation about 0.8. P-0003 does not claim anything there. I have not checked whether the same law explains that run.
- The noise estimate (0.05) is from A-species lone runs and at-rest pairs. Species B and C noise is only checked through the lone-particle residuals (r3/009-010), which agree.
- My P-0001 and P-0002 reviews are limited to the tested scope. The P-0002 review is partial on purpose; the verdict will be updated when the edge-test results arrive.
- The ledger's research total for 11-17 is consistent with the round-3 plan, but I did not re-derive the full ledger across rounds 1-3 from result costs. Treat the 23.3 used figure as the ledger's, not my own check.

## Analysis code
All in `out/labs/lab-a/analysis/`. Pure python, no numpy (numpy is not installed here).
- `pair_rest_r3.py`: per-run quadratic fits; reports window-averaged acceleration (not the initial acceleration).
- `pair_central_fit_r3.py`: two-body integration, grid over P, K.
- `pair_central_refine_r3.py`: golden-section K for each P, with rms.
- `pair_form_compare_r3.py`: power law vs screened inverse square.
- `compare_model_r3.py`: residuals of any paper's `model.py` against result samples, with census events.
- `make_round1_requests.py`: writes `out/requests/2026-11-18/r1/lab-a/`.
- Earlier: `fit_r1.py`, `fit_r2.py`, `pair_fit_r2.py`, `pair_accel_r2.py`, `make_round3_requests.py`.
