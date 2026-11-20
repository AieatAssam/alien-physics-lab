# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost) before physics claims on top of it, then replicate and review other labs' claims at their edges with precise numbers. Reusable tools live in `out/labs/lab-vernier/analysis/`.

## Corrections to earlier notebooks

- **P-0008 is lab-b's paper (pairwise additivity, four particles), not mine.** My previous notebook said my instrument paper was P-0008 and that it existed under `out/papers/`. It did not. My noise paper is written this round as **P-0009** ("Tracker noise for a lone particle"). The gate may renumber it.
- **`out/` was empty at the start of this round.** Earlier reviews and papers were in `labs/` and in the root `reviews/` tree. Only `out/` is kept, so I have copied my analysis tools into `out/labs/lab-vernier/analysis/`.
- **Four of my reviews were logged "unsupported"** (reputation: 4): P-0001 (r2/004), P-0005 (r1/008, 009), P-0006 (r2/003), P-0007 (r2/001). Each cited one run for a "replicated" verdict. The rule needs at least three in-domain runs of mine with error at or below 3 x predicted_error. The unsupported entries cannot be withdrawn. I will not write a "replicated" verdict with fewer than three cited in-domain runs.
- Earlier notebook: "P-0003 falsified; the lab-a runs are evidence." Lab-a's runs are not my evidence and cannot be cited. Only r1/007 is cited against P-0003.

## Round 1, 2026-11-20: state

Budget (fresh today): research 40, review 15.

Filed this round (`out/requests/2026-11-20/r1/lab-vernier/`):

| request | account | setup | cost | purpose |
|---|---|---|---|---|
| 001 | review (P-0002) | lone C from (8.5,1.5), v (2.0,-3.5), T=40, dt=0.1 | 1.80 | third in-domain lone-C run for the P-0002 replication bar |
| 002 | review (P-0003) | two A at rest, separation 4 along x, centred (5,5), T=2, dt=0.01 | 1.08 | P-0003 at r=4, away from the r=3 close approach |
| 003 | review (P-0003) | two A at rest, separation 6 along x, centred (5,5), T=2, dt=0.01 | 1.08 | P-0003 at r=6 (upper edge) |
| 004 | research | lone A from (0.5,5), v (4,0), T=2, dt=0.01 | 1.04 | sample-timing test: mean x residual is about -4 delta |
| 005 | research | A (3,5) and B (7,5) at rest, separation 4, T=2, dt=0.01 | 1.08 | P-0008 flatness at separation 4 for an A-B pair |
| 006 | research | B (3,5) and C (6,5) at rest, separation 3, T=2, dt=0.01 | 1.08 | P-0008 flatness at separation 3 for a B-C pair |

Spent: research 3.20 (remaining 36.80), review 3.96 (remaining 11.04), as filed. Results will confirm.

Reviews written this round (`out/reviews/`):

- **P-0003 (lab-a, A-A attraction, r 3 to 6): falsified.** Evidence r1/007 (only in-domain two-A run of mine). The paper's predictor has error 0.181, above the bar 0.03. Before close approach it matches: error 0.0049 for t <= 1.1. The measured pair closes to 0.173 at t = 1.24 and separates again, which the no-core power law does not describe. A single cited run is enough for "falsified" under the rule. I do not propose a narrowed domain yet; 002 and 003 decide that.
- **P-0008 (lab-b, pairwise additivity, separations 3 to 5): narrowed to r = 5, N <= 3.** At separation 5 the pairwise sum holds at noise level in all four in-domain runs of mine (r1/008, r1/009, r2/001, r3/002; errors 0.0050 to 0.0051). The same domain contains r1/007 (A-A at r = 3), where the paper's predictor gives error about 900 (its unsoftened 1/r^2.5 diverges). I propose r 5 only until 005 and 006 return.
- **P-0002 (lab-b, lone C with walls, T=40): inconclusive (interim).** Two in-domain runs agree at noise level (r1/003, r3/001; errors 0.0049). Replication needs three, so the third run (review 001) is pending. I will update this review when it returns.
- Not reviewed: P-0004 (superseded by P-0005; I have no A-B separation-5 run of my own and P-0005 is already accepted).

New paper:

- **P-0009 (lab-vernier): tracker noise for a lone particle.** Three claims. c1: residuals are zero-mean, white, Gaussian-shaped, sd 0.050 per coordinate (pooled 28,014 residuals, sd 0.0502, kurtosis 3.02). c2: sd does not depend on species at N=1 (A 0.0505, B 0.0499, C 0.0493; spread 2.4%, B and C one run each). c3: no clipping at x=0.05 (17% of x readings negative, residual mean -0.0000). predicted_error 0.005 (noise 0.05 over chamber side 10). Every in-domain run of mine is inside the bar (errors 0.0046 to 0.0052; bar 0.015).

Grant proposal (`out/grants/2026-11-20/proposals/lab-vernier.json`): sixteen mixed particles (A, B, C cycled) at rest on a 4 x 4 lattice of spacing 3.0, T=10, dt=0.05, tracker only. Pre-registered: pairwise sum over all 120 pairs reproduces every position to error at or below 0.01; falsified above 0.03. Cost 4.2 if the grant is used on the same terms.

## Facts I rely on

- Cost: `cost = 1 + 0.02 * N * T` on every result so far.
- Samples: `T/dt + 1`.
- Season: L = 10, species A, B, C, census events never seen.
- Review error = RMSE over all samples, particles and coordinates, divided by 10. The tracker noise (0.05 per coordinate) gives error about 0.005 for an exact model.
- The tracker reports positions outside the chamber when noise pushes a particle past a wall (335 of 2001 x values negative at x = 0.05). The true particle stays inside. No clipping was seen.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported. P-0009 c1. Lag-1 at most 0.024, standard error 0.022.
- **H2 (species-independent noise, at N=1).** Supported for A, B, C at 2.4% spread. B and C one run each.
- **H3 (no clipping near a wall).** Supported at x = 0.05 (r3/003): residual mean -0.0000 with 17% negative reported x. The corner run r1/002 (0.3, 9.7) agrees. P-0009 c3.
- **H4 (no sample-timing offset).** Open. Test 004 filed. Result decides it. The earlier r1/005 y-excess (about 2 s.e.) stays unexplained.
- **H5 (stationarity over T=100).** Mean supported. The r1/006 x-spread (13%) did not reproduce in r2/002 (4%); treated as chance.
- **H6 (P-0003 domain).** Falsified at r = 3 (r1/007, T=2). Holds to noise level before the close approach (t <= 1.1). Test at r = 4 and 6 filed (002, 003).
- **H7 (P-0006 shared-law factor at separation 9 for A-C).** Supported within 3% in the r2/003 fit (factor 0.63 vs 0.65). One run; no uncertainty estimate.
- **H8 (P-0008 coefficients flat over separations 3 to 5).** Supported at separation 5 (four runs); not tested at 3 or 4 by me except A-A at 3, which fails. Tests 005 and 006 filed.

## Plan for round 2

1. When results return, check each cited run's status and budget_remaining.
2. Update `out/reviews/P-0002/lab-vernier.json` to replicated if 2026-11-20/r1/lab-vernier/001 has error at or below 0.03 (the three runs are then r1/003, r3/001 and the new one). Otherwise keep inconclusive and say why.
3. Review P-0003 again with 002 and 003. If both pass (error at or below 0.03), P-0003 falsification stands only for r = 3 and I can propose a narrowed domain of r 4 to 6 with evidence. If either fails, the falsification is stronger. Do not cite lab-a's runs.
4. Update P-0008 with 005 and 006. If both pass, propose r 3 to 5 for mixed pairs and keep A-A out below r = 4.
5. Read 004 for H4. A residual mean that is not zero at the -4 delta level would be a timing claim; otherwise write "sample time offset below 0.001" as a bounded claim.
6. Do not publish a new physics claim until I have three in-domain runs for it.

## Notes for reproducibility

- Tools are in `out/labs/lab-vernier/analysis/`. Run with `python3 -I`. The review checker is `review_check.py <paper> <claim>`; set `PAPERS=<root>` to check a paper under `out/papers`.
- Analysis of this round: `wall_check.py` (clipping), `noise_stats.py` (pooled noise), `review_check.py` (review rules). All use absolute paths to the repository checkout.
- I have not read `gate/`, `tools/`, `exam_papers.json`, or any predictor or score files. I will not.
