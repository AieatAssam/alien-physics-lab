# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Judge notes that govern my claims

- The domain check covers species, particle count and initial pair separations. Duration is not in the domain, so a run at a different T can count as in-domain. I still cite runs inside the claim's own duration window, so reviews stay clean.
- Edge runs: a run placed exactly on a domain edge can fail the paper's own check by float rounding (seen with `1.95` read as `1.94999...`, and with diagonal layouts that round to 6 decimals). Place review-account edge runs 0.01 inside the edge. In my own models I accept a 1e-3 tolerance at the edge.
- **The judged metric is coarse.** Noise floor: tracker noise 0.05 per coordinate gives a correct model RMSE/L of about 0.005 (observed 0.0049 to 0.0053 on correct models). **A 6% error in K at separation 6, over T = 2, is still at that floor.** P-0003's constant K = 17.7 is 6% high at r = 6 and scores 0.0051 on the judge. So the judge cannot test K to better than several percent at these durations. My decisions on K rest on per-run K fits (chi2 at sigma 0.05, reduced chi2 about 1), not on the judged error.
- **Do not state predicted_error below about 0.005.** The sharpen-A/B/C bounties ask for 0.0025 or less, below the floor a correct model reaches, so I will not claim them.
- Review evidence is judged on my own request ids only. Runs that test a paper use `account: review` with `cites_paper`.
- Cost is `1 + 0.02 * N * T`.
- Environment: numpy and jsonschema are not preinstalled in the sandbox. Install with `python3 -m pip install numpy jsonschema`. Scripts run with `python3 -I`.

## Budget ledger

### Closed days
- 2026-11-17: research 23.30 of 40; review 6.00.
- 2026-11-18: research 30.38 of 40; review 6.20 (P-0002 review).
- 2026-11-19: research 13.12 of 40; grant 120 awarded, 33.00 spent on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Voted lab-keystone.
- 2026-11-20: research 9.19 of 40; review 13.90 of 15; grant 1.02 of 120. Voted lab-keystone.
- 2026-11-21: research 31.37 of 40; review 12.42 of 15; grant 1.09 of 120. Voted lab-vernier.
- 2026-11-22: research 32.32 of 40; review 6.75 of 15.
- 2026-11-23: research 37.78 of 40 (round 1 20.34, round 2 0, round 3 17.44); review 13.80 of 15. Keystone won the grant; my proposal lost.

### 2026-11-24 (today)
- Round 1: research 13.12 of 40 (`r1/009-020`); review 8.64 of 15 (`r1/001-008`, P-0025). Grant proposal filed (radial fall, r0 = 9). Results now in and scored (below).
- Round 2: research planned 9.90 (`r2/001-009`); review planned 3.29 (`r2/010-012`, P-0026).
- Totals if round 2 runs as filed: research 23.02 of 40 (16.98 left for round 3); review 11.93 of 15 (3.07 left). Grant: no award today. Vote filed for lab-b.

## Results in hand (2026-11-24, round 1, scored today)

Scored with `out/labs/lab-a/analysis/score_round1_2026-11-24.py` (output `score_round1_2026-11-24.json`) and `check_P0027_2026-11-24.py`.

### P-0025 (lab-b, A-B table, r0 4 to 8): REPLICATED on the stated bound
- Runs `r1/001-008` (review account, all in domain, all 1991 samples): judged RMSE/L 0.00497 to 0.00506. Bar 3 x 0.007 = 0.021. All eight pass.
- Edge: r0 4.01 horizontal and diagonal pass at the floor. The clamped K table below r = 4 does not show at T = 2.
- Not tested: the K_B/K_A = 1.41 ratio. The judge cannot resolve it at T <= 2 (see judge notes).
- Review filed: `out/reviews/P-0025/lab-a.json`, verdict replicated, comment scoped to the 0.007 bound.

### A-A K(r) table (P = 2.5, per-run fits, reduced chi2 0.98 to 1.10)

| r | run ids | K per run | mean K | replicate spread |
|---|---|---|---|---|
| 3 | H30 `2026-11-23/r3/lab-a/001-004` | 17.666 (horiz), 17.700 (diag) | 17.683 | 0.4% |
| 4 | `2026-11-24/r1/lab-a/011-012` | 17.701, 17.701 | 17.701 | 0.0% |
| 5 | H30 `r3/005-008` | (see H30 table) | 17.834 | 0.4% |
| 5.99 | `r1/009-010` (P-0003 edge) | 16.538, 16.670 | 16.60 | 0.8% |
| 6 | `r1/017-018` | 16.592, 16.642 | 16.617 | 0.3% |
| 7 | H30 `r3/009-012` | 15.120, 15.121 | 15.121 | 0.4% |
| 8 | `r1/013-016` | 13.541, 13.437, 13.441, 13.311 | 13.432 | 1.7% |
| 9 | H30 `r3/013-016` | 11.694, 11.553 (orient) | 11.624 | 1.8% |

Findings:
- **H30 (constant K = 17.7, P = 2.5 over 3 to 9): refuted (2026-11-24).** Holds at 3 and 5, fails at 7 (-14.6%) and 9 (-34.3%). Stays refuted.
- **K is flat on [3, 5] and falls from 5 to 9** (17.83 to 11.62). K(r)/K(3): 1.001 (4), 1.009 (5), 0.940 (6), 0.855 (7), 0.760 (8), 0.657 (9).
- **Pre-registered interpolation rule passed** (`analysis/prereg_2026-11-24_r1.json`). Linear interpolation of the 3/5/7/9 nodes predicts the withheld nodes 4, 6, 8 at -0.3%, +0.9% and +0.5%. Rule: within 3%, and replicate spread below 3%. The linear table over [3, 9] is therefore allowed. Basis for P-0027.
- Shape: not a single power law (local exponent of K changes from about 2.1 near r 1 to 2.5 on [3, 5] to about 3.4 on [6, 9]; the 1 to 3 value is from P-0024). The screened and cutoff forms are not compared yet. Not claimed.
- **P-0003 (constant K = 17.7, domain 3 to 6) is biased at 6 by -6.1%.** Pre-registered trigger: narrow P-0003 if sep 6 is off by more than 3%. Triggered. P-0027 supersedes it with the table over [3, 9].

### Crowd-8 ring (3x3 grid minus centre, spacing 3.1, T = 0.5): at the floor, not discriminating
- `r1/019`: judged RMSE/L 0.00498 with table pairwise model and 0.00498 with constant K. `r1/020`: 0.00501 and 0.00501.
- The ring at T = 0.5 cannot separate the table from constant K (predicted difference 0.008 max). Crowd-8 is **open**: no claim filed.

### P-0003 edge (own paper, not a review)
- `r1/009-010` at r0 5.99 (T = 2): K fits 16.54 and 16.67 and the P-0003 model's judged RMSE/L 0.0051 at the floor. The judge does not see the 6% bias (see judge notes).

## Papers

### P-0027 (filed 2026-11-24, round 2): A-A pair at rest, separation 3 to 9, K(r) table at P = 2.5. Supersedes P-0003.
- Claim: K(r) piecewise linear through 17.683 (3), 17.701 (4), 17.834 (5), 16.617 (6), 15.121 (7), 13.432 (8), 11.624 (9). Judged error 0.007. Duration windows: T <= 1.5 for r0 < 5, T <= 2 for 5 <= r0 < 7, T <= 3 for r0 >= 7 (the windows keep closest approach away from contact; at r0 = 3, T = 2 predicted min sep is 0.005, and at r0 = 4, T = 2, 0.022).
- Evidence: 24 runs (H30 `r3/001-016`; `r1/009-010`, `013-018`). `r1/011-012` (r0 4, T = 2) are outside the r0 < 5 window and not cited.
- Model check: judged RMSE/L 0.0049 to 0.0051 on all 24 cited runs.
- Paper number: P-0027 is the next free number after P-0026 at filing. The gate may renumber; refer to it by title in the notebook until the final id is visible.

## Reviews

### Filed
- 2026-11-24: P-0025 replicated (`out/reviews/P-0025/lab-a.json`, evidence `2026-11-24/r1/lab-a/001-008`).
- 2026-11-23: P-0022 replicated (`r1/001-004`); P-0023 replicated (`r1/005-008`); P-0024 replicated, scoped (exponent not tested).
- 2026-11-22: P-0021 replicated (`r2/013-015`); P-0017 replicated (`r1/009-011`); P-0020 replicated (`r3/012-015`); P-0016 and P-0018 replicated.
- Standing: P-0013 replicated; P-0014 narrowed (T <= 1 for close approach); P-0015 replicated; P-0010 narrowed; P-0011 replicated; P-0002 replicated.

### Pending
- **P-0026 (lab-keystone, A crowd of 16, T <= 0.3, r 1.5 to 10.5).** Three review-account runs filed: `2026-11-24/r2/lab-a/010` (4x4 grid, spacing 1.52, minimum pair at the 1.5 lower edge), `011` (ring radius 4.9, adjacent chord 1.92), `012` (seeded irregular layout, minimum 1.60, maximum 9.07). All three pass the paper's `predict()` domain check (checked). Verdict rule: replicated if at least 3 in-domain runs have judged error at most 0.021. Expected at the floor; the grid run is the edge test. **Write the review once results arrive.** Do not write it before.

## Requests filed round 2 (pre-registered; `analysis/make_2026-11-24_r2_requests.py`)

| id | account | purpose | N | T | cost | predicted K (table) |
|---|---|---|---|---|---|---|
| r2/001 | research | A-A sep 3.5, horizontal | 2 | 1.0 | 1.04 | 17.692 (interp 3 and 4) |
| r2/002 | research | A-A sep 4.5, diagonal | 2 | 1.5 | 1.06 | 17.768 |
| r2/003 | research | A-A sep 5.5, diagonal | 2 | 2.0 | 1.08 | 17.226 |
| r2/004 | research | A-A sep 6.5, horizontal | 2 | 2.0 | 1.08 | 15.869 |
| r2/005 | research | A-A sep 6.5, diagonal (replicate) | 2 | 2.0 | 1.08 | 15.869 |
| r2/006 | research | A-A sep 7.5, diagonal | 2 | 3.0 | 1.12 | 14.277 |
| r2/007 | research | A-A sep 8.5, horizontal | 2 | 3.0 | 1.12 | 12.528 |
| r2/008 | research | crowd-8 ring, spacing 3.1 | 8 | 1.0 | 1.16 | table pairwise |
| r2/009 | research | crowd-8 ring, replicate | 8 | 1.0 | 1.16 | table pairwise |
| r2/010 | review (P-0026) | 16 A grid, spacing 1.52 | 16 | 0.3 | 1.10 | - |
| r2/011 | review (P-0026) | 16 A ring r 4.9 | 16 | 0.3 | 1.10 | - |
| r2/012 | review (P-0026) | 16 A seeded irregular | 16 | 0.3 | 1.10 | - |

**Pre-registered decision rules (written before results):**
1. **Off-node K (r2/001-007).** Per run, fit K at P = 2.5 (`score_round1_2026-11-24.py` fitter). Pass a node if |K_fit - K_pred| / K_pred <= 2% and replicate spread (where two runs exist) below 3%. A node that misses by more than 4% means the linear table is not valid there. If any node fails, narrow P-0027 to the nodes that pass, in the next paper.
2. **Crowd-8 ring at T = 1.0 (r2/008-009).** Table pairwise model predicted max position difference from the constant-K 17.7 model: 0.032 (RMS 0.026). Min pair stays above 2.3, so no collapse. Pass the table pairwise model if chi2/dof <= 1.5 at sigma 0.05. Prefer the table over constant K if chi2 (constant) - chi2 (table) > 9 per run. If both have chi2/dof > 3, the pairwise sum fails at N = 8 and no crowd-8 claim is made.
3. **P-0026 review (r2/010-012).** Replicated if >= 3 in-domain runs have judged error <= 0.021. Narrowed if the grid run (min pair 1.52) fails while the others pass. Falsified only if all three fail above 0.021.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2 to 8.6. B at high speed not tested.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 8, 9, 16.
- H4 no decay: no census event in about 70 runs.
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central: supported. A-A: K(r) table on [3, 9] (P-0027).
- H8 pair force identical for all species pairs: refuted at sep 5.
- H9 coupling factorises as g_ij = q_i q_j: partially supported. Not claimed.
- H10 isotropy: supported at sep 4, 5, 8 (horiz vs diag within about 1.5%). A-B horizontal-diagonal -1.98% pooled, not significant. C-C horizontal-diagonal 5.4%: open.
- H11 shared distance law: C-based pairs at 7 and 9 within about 5% (P-0006). **A-A at 7 and 9 refuted for constant K (H30).**
- H12 pairwise additivity for 3 and 4 particles at separations 3 to 5 (T <= 1): supported. N = 9 at T = 10: not evaluable (cluster collapses within 2 time units).
- H13 no census events in crowded long runs: supported (16 particles, T = 100).
- H14 constant-K power law at close range: refuted for A-A at r0 0.85 to 2.0.
- H15 A-A constant K at r0 = 1.0: refuted (K about 10.5 to 11.5, not 18).
- H16 B-B and C-C ratio to A-A at close range: B-B/A-A at r0 1.0 = 0.34; C-C/A-A = 0.84 (horizontal).
- H17 A-A K at r0 1.0 orientation-independent at (5,5): supported.
- H18 P-0014's T = 2 predictions fail for A-A at r0 2.5 (error 4.10) and C-C at r0 3.5. T <= 1 holds for pairs measured.
- H19 P-0013's S_AA = 0.753 supported. S_AC and S_CC not separated from 1.
- H20 close-range A-B: K_BA passes; K_AB fails clause (iii) on run 005. Open.
- H21 B-B at r0 1.0: K = 3.86 (lab-a), 3.98 (lab-b, P-0017). About 4 sigma apart; open pending lab-b refit.
- H22 C-C diagonal orientation 5.4% below horizontal at (5,5). Open.
- H23 A-B diagonal orientation: resolved as fluctuation.
- H24 P-0020 K_BA: my fit about 7.8 vs paper 7.33 (6%). Open.
- H25 P-0021 constant K over T = 6 (A-B at sep 7 falling to about 3.8): supported.
- H26 close-range A-B K_BA pooled 7.80: open as a claim only if K_AB is resolved.
- H27 A-C close range: K_AC -5.75, K_CA -13.6; diagonal control fails clause (iii). Held.
- H28 N = 9 same species, long time: not evaluable.
- H29 A-A K at sep 7 and 9 vs 17.7: confirmed (K 15.1 and 11.6).
- H30 A-A single P = 2.5 power law with K = 17.7 over sep 3 to 9: **refuted (2026-11-24).**
- H31 P-0024 exponent 2.10 over 1.25 to 3 vs P = 2.5: **untested.** Short runs cannot separate P from K (2026-11-23 null).
- H32 A-A K(r) shape over sep 3 to 9: **table measured and claimed as effective K at P = 2.5 (P-0027). Functional form open.**
- H33 crowd-8 pairwise law with table K at N = 8: **open.** Ring at T = 0.5 at floor, not discriminating. Discriminating test filed at T = 1.0 (r2/008-009).
- H34 P-0025 (lab-b) A-B table at r0 4 to 8: **replicated on the stated 0.007 bound (review 2026-11-24).** K_B/K_A = 1.41 untested.
- H35 (new) A-A K flat on [3, 5] (17.68 to 17.83): supported, replicate spread below 1%.
- H36 (new) P-0003's constant K = 17.7 is 6% high at separation 6 (measured 16.62): supported, per-run K fits.
- H37 (new) Judged metric cannot resolve K to better than several percent at T <= 2: supported by H36 (P-0003 at 5.99 scores at the floor).

## Plan for the next round
1. Score `2026-11-24/r2/lab-a/001-012` when results arrive. Use the pre-registered rules above.
2. Write the P-0026 review (`out/reviews/P-0026/lab-a.json`) from `r2/010-012` only if the rule is met. Do not file before the results.
3. If r2/001-007 pass, consider a P-0027 successor only if it adds information (for example, a crowd-8 claim or the screened-form comparison). Do not re-publish the same table.
4. Crowd-8: file a claim (max_particles 8, r in [3, 9], T <= 1.0) only if `r2/008-009` pass the table rule. Otherwise hold.
5. Keep the sharpen bounties out of reach by design: no predicted_error below 0.005.
6. Research budget left after round 2: about 17 credits. Use it on the crowd and off-node follow-ups, not on repeating settled H30 results.

## Errors caught
- **r0 from the first measured sample.** Fixed: r0 comes from the request setup.
- **Sample minimum read as collision.** Not used as a collision distance.
- **Grid bug in one B-B fit.** Refit on 3.0 to 4.5.
- **Edge runs fail the paper's own domain check.** Fixed by moving runs 0.01 inside; in my model, 1e-3 tolerance at the edge (diagonal layouts round to 6 decimals).
- **Weak crowd test (T = 0.5 ring).** Insensitive to K. Replaced by T = 1.0 design (`r2/008-009`).
- **Uniform-K integrator divergence (N = 9, T = 10).** Recorded as not evaluable.
- **Pre-registered clause missed by one run (close-AC run 014).** Recorded as a fail; held.
- **Exponent sensitivity overestimated (2026-11-23).** The short run cannot separate P from K. Recorded as null.
- **Circular secondary in the H30 scorer (2026-11-24).** Not reported.
- **Sharpen bounty trap.** Not pursued; predicted_error below 0.005 would be claiming below the noise floor.
- **P-0003 bias at separation 6 went unnoticed until today.** My own P-0003 had K = 17.7 over 3 to 6. The per-run fit at 6 gives 16.62. I should have fitted each separation of my own claim. Superseded by P-0027.

## Self-criticism
- **The judged metric hides K errors of several percent at these durations.** Today's P-0003 result is the example. I have been reading "replicated" as "K confirmed". For K, the evidence is the per-run fit. The judge verdict only tests the error bound.
- **Replicate verdicts sit at the noise floor.** P-0022, P-0023, P-0024 and now P-0025 are replicated only in the sense that the stated error bound holds. None of them constrains the constants or the exponent beyond what is stated.
- **H30 was pre-registered, refuted, and I did not publish it as a paper on the day.** The result stays in the notebook until the table was complete. The table was completed today (round 1 nodes 4, 6, 8) and P-0027 is filed. This is the delay I accepted.
- **Close-AB held on run 005.** Not excluded post hoc.
- **B-B K still disagrees with P-0017 at about 4 sigma.** Asked lab-b to refit. Not resolved.

## What would change my mind
- **A-A K(r):** if the off-node runs (r2/001-007) miss a node by more than 4%, the linear table is wrong there and P-0027 must narrow to the passing nodes.
- **Crowd-8:** if the table pairwise model fails at chi2/dof above 3 on the ring at T = 1, the pairwise sum is wrong at N = 8 and the crowd claim is dead.
- **P-0026 (lab-keystone):** if the grid run at minimum pair 1.52 fails while the others pass, the crowd claim is narrowed to minimum pair above 1.6.
- **Exponent (H31):** only a wide-r design can separate P from K. The grant proposal was the design (r0 = 9 radial fall); it did not win today.
