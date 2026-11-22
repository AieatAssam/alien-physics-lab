# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Budget ledger

### Closed days
- 2026-11-17: research used 23.30 of 40; review 6.00.
- 2026-11-18: research used 30.38 of 40; review 6.20 (review of P-0002).
- 2026-11-19: research used 13.12 of 40; grant award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Voted lab-keystone.
- 2026-11-20: research used 9.19 of 40; review 13.90 of 15 (P-0008; P-0010 and P-0011); grant 1.02 of 120 (`r3/001`, C-C at r0 2). Voted lab-keystone.
- 2026-11-21: research used 31.37 of 40 (rounds 1-3); review 12.42 of 15 (P-0013, P-0014, P-0015, P-0016 filings); grant 1.09 of 120 (`r3/001`, the 9-A main event). Unused grant credit (118.91) and unused research (8.6) lapse at day end. Voted lab-vernier.

### 2026-11-22 (round 1, today)
- Research: 8.06 filed (`r1/001-008`, close-AB replicates, 1.008 each). Research left after filing: 31.94. Unused research lapses at day end.
- Review: 3.02 filed (`r1/009-011`, B-B runs for P-0017, 1.006 each). Review left after filing: 11.98.
- Review verdicts filed without new spend: P-0016 (from `2026-11-21/r3/lab-a/016-018`), P-0018 (from `2026-11-21/r1/lab-a/003, 004` and `r3/005, 006`).
- Grant proposal filed: `out/grants/2026-11-22/proposals/lab-a.json` (9-body mixed-species Latin square, 1.09). Proposal only; no grant credit spent today.

## Established (accepted-level claims, or runs I trust)

Pair coefficients at separation 5 (P-0005, accepted). Convention in this notebook: K_XY = acceleration coefficient of species X toward species Y, P = 2.5. The table in P-0005 reads "A on B = 8.99, B on A = 12.34"; I have not verified its convention against the per-particle fits below, and the A-B ratio comparison depends on it (see close-AB).

| pair | K values | runs | status |
|---|---|---|---|
| A-A | 18.0 | P-0003 (domain sep 3 to 6) | established at sep 3 to 6; not valid at sep 1 |
| A-B | 8.99 and 12.34 (see convention note) | replicated | close-range fit pending (below) |
| A-C | -8.77 and -21.25, repulsion | replicated | |
| B-B | 6.12 | 4 values, spread about 9% | |
| C-C | 12.36 | 4 values, spread about 5% | |
| B-C | -6.10 and -10.59 | pre-registered prediction passed | |

Other established results:
- Free flight with specular walls (P-0001, P-0002): A, B, C at speeds up to 8.6, T up to 100, corner hits. Supported.
- Isotropy at separation 4 (A-A along diagonal, y, horizontal): K = 17.67, 17.71, 17.70. Supported at sep 4 (not at sep 1).
- Pairwise additivity for three and four particles at separations 3 to 5 (T <= 1): at noise level.
- **N = 9 same-species additivity (round-3 grant `2026-11-21/r3/lab-a/001, 002`, 9 A on 3x3, spacing 3.5, T 0.5): the P-0003 pairwise-sum model gives RMSE/L = 0.0071 in both repeats, inside the pre-registered support threshold of 0.01.** Supported for one species at N = 9. Mixed species not tested yet (proposed today).
- Shared distance law at separations 7 and 9 (P-0006): within about 5%, qualified by the close-range results.
- No census event (decay or appearance) in about 70 runs, including 16 particles at T = 100.
- Cost law cost = 1 + 0.02 N T: supported at N = 1, 2, 3, 4, 9, 16. N = 9 confirmed by the grant costs (1.09 for 9 particles at T 0.5).
- Noise: tracker noise on separation sd about 0.07 (about 0.05 per coordinate). Single-particle free-flight runs give error/L 0.0068 to 0.0073 against any exact model. **0.007 is the noise floor of the judged metric.** Any claimed error below about 0.007 cannot be confirmed by a single run.

## Close range

### B-B at r0 = 1.0: orientation control passes (round 1, 2026-11-22 analysis)
Symmetric fits (P = 2.5 fixed, relative RK4, `analysis/analyse_2026-11-22.py`), T = 0.3:

| run | orientation | K_fit |
|---|---|---|
| 2026-11-21/r1/lab-a/001 | horizontal | 3.822 |
| 2026-11-21/r1/lab-a/002 | horizontal | 3.838 |
| 2026-11-21/r3/lab-a/003 | diagonal | 3.884 |
| 2026-11-21/r3/lab-a/004 | diagonal | 3.884 |

Horizontal mean 3.83, diagonal mean 3.88, a 1.4% difference (pre-registered tolerance 5%). Pooled K = 3.857 (sd 0.03). **Published as P-0019 (close-BB), K = 3.86.** Its claim differs from P-0017 (lab-b, K = 3.98) by about 3%, roughly 4 sigma on my scatter. The judged metric cannot separate them (both about 0.007 error at T <= 0.3). I have said so in the paper and ask lab-b to check.

### C-C at r0 = 1.0: orientation control fails the pre-registered rule (narrowly)
| run | orientation | T | K_fit |
|---|---|---|---|
| 2026-11-21/r1/lab-a/003 | horizontal | 0.15 | 9.438 |
| 2026-11-21/r1/lab-a/004 | horizontal | 0.15 | 9.569 |
| 2026-11-21/r3/lab-a/005 | diagonal | 0.15 | 8.930 |
| 2026-11-21/r3/lab-a/006 | diagonal | 0.15 | 9.043 |

Horizontal mean 9.50, diagonal mean 8.99: 5.4% lower. The pre-registered window was 9.03 to 9.98, so the diagonal mean misses by 0.4%. **Rule not met; close-CC held.** Diagonal runs are lower for A-A (round 2, about 5%) and C-C (now 5%); B-B shows no such effect. Two open readings: a real orientation effect for A and C, or a position effect of the (5,5) diagonal layout. Next test: C-C at (5,5) with a vertical pair (not run; not needed to publish anything today).

### A-B at r0 = 1.0: round-3 fits fail the rule (power limit)
Per-particle fits (K_AB on A, K_BA on B; `analysis/fit_AB_2026-11-22.py`), T = 0.15:

| run | layout | K_AB (on A) | K_BA (on B) |
|---|---|---|---|
| 2026-11-21/r3/lab-a/012 | horizontal, A left | 5.84 | 7.30 |
| 2026-11-21/r3/lab-a/013 | horizontal, B left | 5.56 | 7.62 |
| 2026-11-21/r3/lab-a/014 | diagonal, A left | 6.30 | 7.96 |
| 2026-11-21/r3/lab-a/015 | diagonal, A left | 4.80 | 8.30 |

K_AB scatters by about 10% and K_BA by about 6% across four runs. The pre-registered rule (both K's within 5% per pair of runs and means within 5%) fails. The per-run precision at T = 0.15 is too low: the per-particle displacement signal is about 0.07 (0.5 K t^2) against tracker noise 0.05 per coordinate. **Not publishable. Close-AB held.** Remedy: longer T (signal grows as T^2; information scales about T^2.5). T = 0.2 is a crude choice: the relative separation shrinks by about 0.5 (K_AB + K_BA) t^2 = 0.28, from 1.0 to about 0.72 (hand estimate, not an RK4 run), so no collision is expected. Check the minimum separation in the results before fitting. Round 1 `001-008` run this (pre-registered in `analysis/pred_2026-11-22_r1.json`).

Convention check still open: the ratio K_AB/K_BA from these runs (0.73 to 0.80 horizontal and diagonal except run 015) is compatible with 0.728 (the P-0005 table, read as "A on B" over "B on A") under one reading, and not under the reverse. The pre-registered rule compares K's per particle, not the ratio, so the convention does not change today's decision. It will matter when writing the claim.

### A-A at r0 = 1.0: orientation and position (round-2 control, 2026-11-21)
K fits: one coefficient K, P = 2.5 fixed, initial separation from the request setup. Per-run sd of K about 0.33 (3%).

| run | orientation, centre | r0 | T | K_fit |
|---|---|---|---|---|
| 2026-11-21/r2/lab-a/001 | horizontal, (3,3) | 1.0 | 0.15 | 10.87 (+-0.33) |
| 2026-11-21/r2/lab-a/002 | diagonal, (5,5) | 1.0 | 0.15 | 10.65 (+-0.32) |
| 2026-11-21/r2/lab-a/003 | diagonal, (3,3) | 1.0 | 0.15 | 10.64 (+-0.33) |
| 2026-11-21/r2/lab-a/004 | horizontal, (5,5) | 1.25 | 0.15 | 12.60 (+-0.64) |
| 2026-11-21/r1/lab-a/009 | diagonal, (3,3) | 1.0 | 0.15 | 10.35 (+-0.3) |
| 2026-11-20/r3/lab-a/003, 004 | horizontal, (5,5) | 1.0 | 0.15 | 11.52, 11.05 |
| 2026-11-21/r1/lab-a/005-008 | horizontal, (5,5) | 1.25, 0.85 | 0.12-0.15 | 11.55, 13.25, 10.55, 10.00 |

**Round-3 six-vs-six control (analysed 2026-11-22, `analysis/aa_six_2026-11-22.py`):** horizontal (12 runs incl. 2026-11-20/r3/003-004 and 2026-11-21/r3/007, 008, 019, 020): K values 11.51, 11.04, 10.78, 11.13, 11.13, 11.00, mean 11.10 (sd 0.24). Diagonal (2026-11-21/r2/002 and r3/009, 010, 011, 021, 022): 10.65, 10.67, 10.32, 11.26, 11.33, 11.31, mean 10.92 (sd 0.43). Difference diagonal minus horizontal -0.18, SE 0.20, **-0.9 SE: inside the pre-registered 2 SE band, so no orientation effect at (5,5).** The round-2 diagonal deficit was a fluctuation. Pooled 12-run K = 11.01 (about 0.07 SE). P-0012's K = 11.3 is the mean of the two horizontal 2026-11-20 runs and sits about 2.5% above this pool: inside its predicted_error at T <= 0.15 (about 0.0003 in RMSE/L from a 2.5% K offset), but I record it as a known offset, not a retraction.

- A-A K at r0 0.85 to 2.0: K_eff about 10.3 (0.85), 10.3 to 11.5 (1.0), 12.4 (1.25), 14.0 (1.5), 15.6 (2.0). Not constant below sep 3.
- P-0003 (A-A, domain sep 3 to 6) is not contradicted: its domain excludes these runs.

## Reviews

### Filed 2026-11-22 (round 1)
- **P-0016 (lab-vernier, A-C at r0 1.000, T <= 0.6): replicated.** Evidence `2026-11-21/r3/lab-a/016, 017, 018`. Errors/L 0.0072, 0.0071, 0.0072 against bar 0.018. `out/reviews/P-0016/lab-a.json`.
- **P-0018 (lab-b, C-C at r0 1.000, at rest, T <= 0.15, K = 9.31): replicated.** Evidence `2026-11-21/r1/lab-a/003, 004` and `r3/005, 006`. Errors/L 0.0069 to 0.0072 against bar 0.024. Our pooled C-C K at T 0.15 is 9.25, consistent with 9.31. Written in `out/reviews/P-0018/lab-a.json`.

### Pending
- **P-0017 (lab-b, B-B at r0 1.000, K = 3.98, T <= 0.15): verdict next round.** Needs `2026-11-22/r1/lab-a/009-011` (review account, T 0.15, B-B horizontal/vertical/diagonal). Our existing B-B runs are at T = 0.3, outside the claim's stated T, so I did not cite them. The verdict will be replicated if at least three of the new runs have error <= 0.024, which the noise floor makes very likely; the comment must say the metric cannot separate K = 3.98 from 3.86.

### Standing reviews
- P-0013 (lab-c): replicated. P-0014 (keystone): narrowed (T <= 1 for close approach). P-0015 (vernier): replicated. P-0010 (keystone): narrowed. P-0011 (vernier): replicated. P-0002: 2026-11-18.

## Papers
- **P-0019 (mine, close-BB, filed 2026-11-22)**: B-B at r0 1.0 at rest, K = 3.86, T <= 0.3, predicted_error 0.008. Evidence `2026-11-21/r1/lab-a/001, 002` and `r3/003, 004`. Model error 0.0069 to 0.0072 on its evidence. Cites P-0017.
- **P-0012 (mine, close-AA, filed 2026-11-20)**: K = 11.3 at r0 1.0, horizontal orientation. The diagonal K (10.35 to 10.65) is 5% to 8% lower, inside P-0012's predicted_error at T <= 0.15. Stands; the orientation point is recorded here, not as a retraction. Round-3 six-vs-six A-A orientation test will say whether the scope needs to change.
- Gate numbering: P-0019 may be renumbered if another lab takes the same number this round; refer to it by title until the final id is visible.

## Round-1 requests (filed today)

All under `out/requests/2026-11-22/r1/lab-a/`, validated against `protocol/request.schema.json` with jsonschema.

| id | account | purpose | cost |
|---|---|---|---|
| 001 | research | close-AB, horizontal, A left, r0 1.0, T 0.2 | 1.008 |
| 002 | research | close-AB, horizontal, B left | 1.008 |
| 003 | research | close-AB, horizontal, A left (repeat) | 1.008 |
| 004 | research | close-AB, horizontal, B left (repeat) | 1.008 |
| 005 | research | close-AB, diagonal, centre (5,5), A left | 1.008 |
| 006 | research | close-AB, diagonal, B left | 1.008 |
| 007 | research | close-AB, diagonal, A left (repeat) | 1.008 |
| 008 | research | close-AB, diagonal, B left (repeat) | 1.008 |
| 009 | review (cites P-0017) | B-B horizontal, r0 1.0, T 0.15 | 1.006 |
| 010 | review (cites P-0017) | B-B vertical, r0 1.0, T 0.15 | 1.006 |
| 011 | review (cites P-0017) | B-B diagonal, r0 1.0, T 0.15 | 1.006 |

Pre-registration: `analysis/pred_2026-11-22_r1.json`, written before any round-1 result.

## Grant

- Round-3 event (`2026-11-21/r3/lab-a/001, 002`, 9 A, 3x3, spacing 3.5, T 0.5): RMSE/L 0.0071 both repeats against the P-0003 pairwise-sum model. Support for one-species additivity at N = 9.
- Proposal filed today (round 1): 9 bodies in a 3x3 Latin square (A, B, C in every row and column), spacing 3.5, at rest, T 0.5, sample_dt 0.0025, cost 1.09. Question: does pairwise additivity hold across species? I will fix the prediction before the result. The pair couplings at separation 5 are the only ones I trust for this geometry; the sign convention (see above) must be settled first.
- Grant credits: 120 award per night, usable in round 3 of the date. A single 9-particle T 0.5 event uses about 1 credit; the rest lapses. The main event is one experiment per night, so I cannot spend the award usefully without an equally larger design (a 16-particle T 100 run costs 33). I have not enlarged the proposal: a larger run would be a different, unregistered experiment.

## Analysis code (`out/labs/lab-a/analysis/`, my files)

- `analyse_2026-11-22.py`: P-0016 / P-0017 / P-0018 scoring against the judged bar, and symmetric K fits. Usage: `python3 -I analyse_2026-11-22.py <repo_root>`.
- `fit_AB_2026-11-22.py`: per-particle K_AB and K_BA grid fit, P = 2.5 fixed. Usage: `python3 -I fit_AB_2026-11-22.py <repo_root> [rids...]`.
- `grant_2026-11-22.py`: round-3 grant score against P-0003 (and P-0005, which failed on a two-particle domain check; not used).
- `make_2026-11-22_r1_requests.py`: writes `r1/001-011`.
- `pred_2026-11-22_r1.json`: pre-registration for round 1.
- Earlier scripts (round 1 to round 3) are in `labs/lab-a/analysis/` in the repo, and `out/labs/lab-a/analysis/` for my round-3 scripts (`pred_2026-11-21_r3.json`, `fit_r2_2026-11-21.py`, `score_reviews_2026-11-21.py`).

## Errors caught

- **r0 from the first measured sample.** Earlier fits took r0 from the noisy first sample (noise about 0.07), shifting K by 10 to 20%. Fixed: r0 comes from the request setup.
- **Sample minimum read as collision.** Minimum separation over a noisy profile is biased low. Not used as a collision distance.
- **Grid bug in one fit (round 1).** The first B-B fit's K grid started at 4.0, pinning the result at the edge. Refit on 3.0 to 4.5 gives 3.82 and 3.84.
- **Model-vs-model divergence (P-0014).** P-0014's model output diverges for A-A at r0 2.5, T = 2 (error 4.10). I have not checked whether the measured pair comes close within T = 2. Stated as such in the review.
- **Convention mismatch in the notebook table.** The table in P-0005 and the notebook's own K_AB label disagree on which species is the acting one. Fixed for the per-particle fits (K_AB is the acceleration of A toward B); the ratio comparison is marked as convention-dependent.
- **Under-powered A-B design (round 3).** I sized round 3 by the number of cells, not the power needed. Round 3's four runs at T 0.15 cannot reach 5% per-particle precision, as the fits above show. Round 1 `001-008` lengthen T to 0.2 and double the runs.
- **Round-3 orientation design too small (round 2).** Two runs per cell cannot resolve a few-percent effect at 3% scatter. Round 3 used six per arm for A-A.

## What would change my mind

- **Close-AB (round 2, from `2026-11-22/r1/lab-a/001-008`)**: publish if the pre-registered rule passes (8-run SE <= 3%, horizontal and diagonal means within 5%, no run beyond 10% of the mean). If it fails at T 0.2, report the per-run scatter as the power limit and hold.
- **Close-CC**: publishable only if a new vertical or diagonal control agrees within 5% with horizontal. Right now the diagonal is 5.4% lower.
- **P-0017 review**: replicated if at least three of `009-011` have error <= 0.024. Anything else: falsified only if all three are above 0.024, which I do not expect at the noise floor.
- **A-A six-vs-six**: analysed. No orientation effect (-0.9 SE). P-0012's scope needs no orientation note; its K (11.3) is 2.5% above the 12-run pool (11.0), which I record.
- **Grant `2026-11-21/r3/lab-a/001-002`** already supports one-species additivity at N = 9 (RMSE/L 0.0071). Mixed-species grant tests the species matrix; a result above 0.02 would falsify the species-independent coupling at N = 9.

## Self-criticism

- **Close-BB published on T = 0.3 runs.** The claim states T <= 0.3, which is the T of the runs. The judged metric cannot test K at this T better than about 5%, so the publication is a precise fit, not a falsifiable bound. I say so in the paper.
- **The B-B K disagrees with lab-b's P-0017 at about 4 sigma, and I have not checked my fit against theirs.** The most likely source is a fit method difference (P fixed, fit window, initial separation). I ask lab-b to re-fit my four runs rather than assume the disagreement is in my favour.
- **Review verdicts at the noise floor.** Both P-0016 and P-0018 are "replicated" by the bar, but the bar (3 x predicted_error, 0.018 to 0.024) is set well above what a single run can distinguish from the claimed K. The comments state this.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2 to 8.6. Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 9, 16.
- H4 no decay: no event in any run to date (about 70 runs).
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported at separations 3 to 9 as a shared-scale law. Close range: P = 2.5 fits the shape for B-B and A-A at r0 1.0 to 2.0; P not tested at r0 = 1.0 alone.
- H8 pair force identical for all species pairs: refuted at sep 5.
- H9 coupling factorises as g_ij = q_i q_j: partially supported. Not claimed.
- H10 isotropy: supported at separation 4 and, for A-A at r0 1.0 at (5,5), by the round-3 six-vs-six control (-0.9 SE). **B-B: supported (1.4% difference). C-C: 5.4% difference, not significant by the pre-registered rule.**
- H11 shared distance law: supported within about 5% at sep 7 and 9 (P-0006).
- H12 pairwise additivity for 3 and 4 particles at separations 3 to 5: supported at T <= 1. **N = 9 same species at spacing 3.5, T 0.5: supported (RMSE/L 0.0071 both repeats).** N = 9 mixed species: proposed grant.
- H13 no census events in crowded long runs: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: refuted for A-A at r0 0.85 to 2.0.
- H15 A-A constant-K at r0 = 1.0: refuted (K about 10.5 to 11.5, not 18).
- H16 B-B and C-C ratio to A-A constant at close range: B-B/A-A at r0 1.0 = 0.34 (supported). C-C/A-A = 0.84 (horizontal orientation).
- H17 A-A K at r0 1.0 is orientation-independent at (5,5): supported (-0.9 SE, six-vs-six). Position dependence (3,3) vs (5,5): one horizontal (3,3) run only (10.87), not separated.
- H18 P-0014's T = 2 predictions: resolved in part. Fails at T = 2 for A-A at r0 2.5 (error 4.10) and C-C at r0 3.5 (0.066). Passes for A-C at r0 2.5 (0.0071). T <= 1 holds for the pairs measured.
- H19 P-0013's S_AA = 0.753 is supported by the judged metric. S_AC and S_CC are not separated from 1 by the metric.
- H20 close-range A-B: per-particle K ratio at r0 1.0 equals the separation-5 ratio: open. Round-3 fits at T 0.15 are too imprecise to test; round 1 `001-008` at T 0.2.
- H21 (new) B-B at r0 1.0: K = 3.86 (lab-a), 3.98 (lab-b, P-0017). Disagreement at about 4 sigma on my scatter; open pending lab-b re-fit.
- H22 (new) C-C diagonal orientation: 5.4% below horizontal at (5,5). Open.

## Papers (summary)
- P-0003 (A-A power law, domain sep 3 to 6, T up to 2): not falsified.
- P-0005, P-0006, P-0007, P-0009: accepted or other labs' papers as recorded in the scoreboard.
- P-0012 (mine, close-AA at r0 1.0, K = 11.3, horizontal): stands; diagonal orientation recorded.
- P-0019 (mine, close-BB at r0 1.0, K = 3.86, T <= 0.3): filed today.

## Plan for the next round
1. Read `results/2026-11-22/r1/lab-a/001-011`.
2. Close-AB: apply the pre-registered rule to `001-008` (8-run SE, horizontal vs diagonal means, 10% outlier bar). Publish close-AB (domain species [A,B], r0 [0.999, 1.001], max 2, T <= 0.2) only if it passes. If it passes, the close-AB bounty is ours.
3. P-0017 review: file replicated if at least three of `009-011` have error <= 0.024; comment on the K disagreement and the metric's limit.
4. Done early (2026-11-22): A-A six-vs-six, no orientation effect. Nothing to carry over.
5. Round-3 A-B (`012-015`): report as held (power limit), not as a claim.
6. Round-3 grant (`001-002`): record as supported (RMSE/L 0.0071) in the public notebook.
7. If the grant proposal wins the round-2 vote, fix the mixed-species prediction before the round-3 result and file it with the grant credit.
8. Consider a sharper C-C orientation control (vertical pair) only if the close-CC claim becomes a priority.
