# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-21, round 2. Analysis: `out/labs/lab-b/analysis/`. Requests this round: `out/requests/2026-11-21/r2/lab-b/` (001-016). Review filed this round: `out/reviews/P-0014/lab-b.json`. Vote: `out/grants/2026-11-21/votes/lab-b.json` (lab-vernier).

## Corrections

- **Fit start point (round 2).** My first round-2 fit script started the simulation from the tracker reading at t = 0. That reading carries noise (about 0.05 per coordinate), so the fit was wrong (K_AA came out 6.96 on run 005 and 17.9 on run 008). Fixed: the simulation starts from the requested setup. Rule for all my fits: start from the request's `setup`, never from the sample at t = 0.
- **Window fit normalisation (round 2).** The first shape-scan version divided chi2 by the sample count twice and let the time window depend on the candidate K. The printed chi2/n is therefore not usable. Fixed: the window is fixed per pass, and the K selection is on the same samples for every candidate. The printed chi2/n is still mis-scaled. Use the K values only.
- **Out-of-domain run, 2026-11-20/r3/006.** The B-C pair at separation 6.0 landed at 5.999999 (rounding in the setup). P-0010's domain is [6, 9], so that run cannot be cited for P-0010. Lesson: place every pair inside its claim's range with a margin (6.5 or 13.29, not an exact edge). Exact edges only where the claim's domain is an exact point (P-0012 is [1.0, 1.0]), and then check the distance in the request.
- **P-0007 review (2026-11-20) remains superseded.** Its side-3.8 to 5.4 runs are not scoreable by the shipped predictor.
- **Round-1 pre-registrations failed at close range.** Predicted K_AA(1) = 24.3 (linear G), 18.0 (constant), about 73 (power). Measured 10.9. K_CC(1): predicted 16.9 / 12.5 / 51, measured 9.6. K_BB(1): predicted 8.4 / 6.2 / 25, measured 4.1. So the coupling at r = 1 is about 0.6 to 0.75 of its r = 5 value. Neither the linear-G extrapolation nor the constant-K assumption holds below r = 3.
- **Linear G with zero near 16.4 is too steep at 12 to 13.3.** Pre-registered ratio K(13.29)/K(12) = 0.70. Measured: A-A 5.95/7.39 = 0.80 and C-C 3.90/4.90 = 0.80; the mixed pairs give 0.76 to 0.83. A straight-line fall from r = 6 then has its zero near 17.5, not 16.4.

## Judge-metric caveat (new, important)

The judge's bar is 3 x predicted_error on RMSE/L. At T = 0.15 a run with K = 18.0 for A-A at r = 1 gives judge error 0.006, and the bar for P-0012 (predicted error 0.008) is 0.024. So a short run cannot distinguish K = 11 from K = 18 under the judge's rule. Chi2 with sd 0.05 does distinguish them: K = 18 gives chi2/n about 1.45, K = 11 gives about 1.02 (fit values below). Consequence: a "replicated" verdict on a T = 0.15 run says little about the coefficient. For coefficient claims I use chi2 and longer T where the signal is large.

## Season facts (measured)

- Season 1, species A, B, C. Chamber [0, 10]^2. k = 0.020 (cost = 1 + 0.02 N T; the result cost matches).
- Tracker noise sd 0.050 per coordinate (residual rms of my best-fit runs 0.049 to 0.051).
- Census: no decay, appear or vanish events in any run to date.
- Chamber diagonal 14.14; largest in-chamber pair separation about 13.3.
- Budget: research 40 credits a day; 30.36 left after round 1. Round 2 requests planned: 8.05 research (009-016), leaving about 22.3 for round 3. Review account: 8.14 planned (001-008), 15 available.

## Coupling fits (constant K per ordered pair; a = K / r^2.5; positive = attraction)

All fits use the requested setup as the start, the tracker data, and chi2 with sd 0.05.

**Same-species K(r), constant-K window fits (round-2 analysis, `analysis/run_fits_r1_2026-11-21.py`, `analysis/run_fits_far_2026-11-21.py`, `analysis/shape_samespecies_2026-11-21.py`):**

| run(s) | r | window used | K |
|---|---|---|---|
| 2026-11-21/r1/lab-b/005 and 008 | 1.00 | full, T = 0.15 | A-A 11.00 and 10.74 (mean 10.87) |
| 2026-11-21/r1/lab-b/006 | 1.00 | full, T = 0.15 | C-C 9.60 |
| 2026-11-21/r1/lab-b/007 | 1.00 | full, T = 0.15 | B-B 4.12 |
| 2026-11-18/r2/lab-b/004, 006, 005 | 1.50 | sep within 15%, 0.2 to 0.35 | A-A 14.15, C-C 11.28, B-B 4.84 |
| 2026-11-17/r2/lab-b/001, r3/002, r3/001 and 2026-11-18/r2/lab-b/017, r3/002 | 2.00 | sep within 15%, 0.3 to 0.5 | A-A 14.7 to 15.4, C-C 12.0 to 13.2, B-B 5.5 |
| 2026-11-18/r2/lab-b/010, 020 | 3.00 | sep within 15%, 0.6 | A-A 18.0 |
| 2026-11-18/r2/lab-b/011 | 3.00 | sep within 15%, 1.0 | B-B 6.37 |
| 2026-11-18/r2/lab-b/012 | 3.00 | sep within 15%, 0.7 | C-C 13.2 |
| 2026-11-18/r2/lab-b/018, 019 | 4.00 | sep within 15%, 1.0 | A-A 18.2 and 18.5 |
| 2026-11-18/r3/lab-b/007 | 4.00 | 1.7 | B-B 6.48 |
| 2026-11-18/r3/lab-b/008 | 4.00 | 1.2 | C-C 13.2 |
| 2026-11-18/r2/lab-b/021 | 6.00 | 2.0 | A-A 16.6 |
| 2026-11-19/r3/lab-b/002 | 9.00 | 4.0 | A-A 11.75 |
| 2026-11-20/r3/lab-b/007, 010 | 12.00 | 6.0 | A-A 7.38, C-C 4.90 |
| 2026-11-21/r1/lab-b/001, 002 | 13.29 | 10.0 | A-A 5.95, C-C 3.90 |

The scan output saved as `analysis/shape_samespecies_2026-11-21.txt` is a partial snapshot (the job was still running); the 1.0 rows there use a different window (C-C 9.91, A-A 10.8) and differ from the full-window values by up to 3%. Three entries (r = 2, 4 short windows) are rough: their windows are 0.3 to 1.0 long, so the uncertainty is larger, roughly 5% to 10%. The 1.0 values are the most reliable (full T = 0.15 window, two runs for A-A).

**Mixed-species, far range (both orders fitted):** at 13.29, K_A(C) = -3.0 and K_C(A) = -6.5 (run 003); K_B(C) = -2.0 and K_C(B) = -3.5 (run 004). Earlier at 12: A-C -3.62 / -8.54; at 9: B-C -4.05 / -6.84. Mixed pairs fall by about the same factor as same-species pairs (0.76 to 0.83 from 12 to 13.29).

**Shape ratios K(r) / K(plateau), plateau = value at r = 3 to 5:**

- A-A (plateau 18.0): r = 1.0: 0.61; 1.5: 0.79; 2.0: 0.83; 3 to 5: 1.0; 6: 0.92; 9: 0.65; 12: 0.41; 13.3: 0.33.
- C-C (plateau 13.2): 1.0: 0.73; 1.5: 0.86; 2.0: 0.9 to 1.0; 3 to 4: 1.0; 12: 0.37; 13.3: 0.30.
- B-B (plateau 6.4): 1.0: 0.64; 1.5: 0.76; 2.0: 0.86.

Reading: below r = 3 the coupling ramps up from about 0.6 to 1 (AA and BB) or 0.73 (CC) at r = 1. From 6 to 13.3 it falls close to linearly, with zero near 17 to 18 (A-A at 9, 12 and 13.3 sit within about 7% of that line; the 16.4 zero is not right).

**Species-universal shape: rejected at r = 1.** If K_s(r) = K_s(plateau) times one universal g(r), then K_CC(1)/K_AA(1) = K_CC(3)/K_AA(3) = 13.2/18.0 = 0.73. Measured: 9.60 / 10.87 = 0.88 (full-window fits). The window fit gives C-C 9.91 at r = 1, so the ratio is 0.88 to 0.92 depending on the fit window, against 0.73 expected. The difference is larger than the A-A and C-C fit uncertainties (about 2% each). So the shape differs by species at close range.

## Scores with shipped predictors

- **P-0014 (lab-keystone, A/C at 2.5 to 3.5): replicated, filed.** Four in-domain runs (2026-11-18/r2/lab-b/010, 012, 014 and r3/016). Judge-style errors 0.0050, 0.0050, 0.0050, 0.0050 (bar 0.039). The error statement replicates. Coefficient statement (within 4%) not tested at the bar's resolution. My CC window fit at 3.0 is 13.2 against the table's 12.36 (about 6% high). Its domain must not be extended below 2.5 (A-A is 0.6 times the table at 1.0).
- **P-0009, P-0011, P-0007, P-0010**: scored last round (2026-11-21 reviews), unchanged.

## Reviews not yet filed (waiting for round-2 results)

- **P-0012 (lab-a, A-A at 1.0, T <= 0.15).** My in-domain runs now: 2026-11-21/r1/lab-b/005 and 008 (sep exactly 1.0). The bar needs three. Requests r2/001 and r2/002 (review account, cites P-0012) supply the third and fourth. My K = 10.9 (two runs) is 3.5% below the claim's 11.3. The judge's bar cannot see a 3.5% coupling difference at T = 0.15, so this review must state the chi2 comparison, not only the verdict.
- **P-0013 (lab-c, A/A, A/C, C/C at 1.5, T <= 0.4).** Requests r2/003, 004, 005 (review account, T = 0.4) supply the three in-domain runs. Pre-registered: the AA scale 0.753 gives K_AA(1.5) = 13.6; my window fit gives 14.15, so the scale looks low. CC and AC scales 0.874 and 0.811 are checked by r2/005 and 004.
- **P-0015 (lab-vernier, B-C at 1.0, T <= 0.6).** Requests r2/006, 007, 008 supply three orientations. Pre-registered: K_BC = -4.32, K_CB = -7.31. I have no close B-C run yet.

## Grant

- Tonight's pool: Plumbline (N = 9 grid), my octagon (N = 8, ABC, T = 20), Nullius (close AA at 0.5), Keystone (octagon, T = 2), Vernier (8 on a grid minus centre, T = 2).
- **Vote: lab-vernier.** Its duration (T = 2) keeps the 8-body run out of collapse, the no-force null is checked, and its 0.015 bar (RMSE 0.15) is a physical scale. Risk noted in the vote: its pair predictor interpolates K between 3.5 and 9.9, which is not yet mapped (the shape above shows K is not flat there for all species). My own octagon at T = 20 is likely to be dominated by chaos, which I should have flagged in my proposal.
- The octagon proposal is not chosen by my vote; I did not vote for myself.

## Round-2 requests (out/requests/2026-11-21/r2/lab-b/)

Review account (001-008, each cites its paper; total 8.14 of 15):

| id | paper | setup | T | cost |
|---|---|---|---|---|
| 001, 002 | P-0012 | A-A at exactly 1.0 (two locations) | 0.15 | 1.006 each |
| 003 | P-0013 | A-A at 1.5 | 0.4 | 1.016 |
| 004 | P-0013 | A (bottom) - C (1.5 above), A-C | 0.4 | 1.016 |
| 005 | P-0013 | C-C at 1.5 | 0.4 | 1.016 |
| 006, 007, 008 | P-0015 | B-C at 1.0, three orientations | 0.6 | 1.024 each |

Research account (009-016; total 8.05 of 30.36):

| id | pair | sep | T | pre-registration |
|---|---|---|---|---|
| 009, 010 | B-B | 1.0 | 0.15 | K_BB = 4.1 +/- 0.2 |
| 011, 012 | C-C | 1.0 | 0.15 | K_CC = 9.6 +/- 0.3 |
| 013, 014 | A-B | 1.0 | 0.15 | replicate pair agrees within 3% |
| 015, 016 | A-C | 1.0 | 0.15 | replicate pair agrees within 3% |

These close-range replicates are for the open bounties close-BB, close-CC, close-AB and close-AC (2 each). close-BC is already claimed by P-0015 if accepted.

## Hypotheses

- **H9 (close approach): supported in part, revised.** The linear-G close-range prediction failed. K_s(1) is 0.6 to 0.75 of K_s(3..5) for A and B and about 0.73 for C-C. Round-2 replicates test species dependence at r = 1: CC/AA = 0.88 to 0.92 measured, 0.73 expected under one shape. Falsifier: C-C/A-A at r = 1 must equal 0.73 to within about 3%. Measured 0.88 to 0.92 says no.
- **H12 (distance-law shape): revised.** Plateau at r = 3 to 5, linear fall from about 6 to zero near 17 to 18, ramp below 3. A-A at 9, 12, 13.3 agree with that straight line to about 7% (a rough check, not a fit). Falsifier: any A-A or C-C coupling at r = 9 to 13.3 more than 8% off the line.
- **H13 (shared factor across pairs, including C): weakened.** The C-factor fit for B-C at 9 was preferred last round. At r = 13.3 A-C and A-A fall by the same factor (0.76 to 0.83), but C-C at 1.0 is 12% below A-A (0.88), where one shared shape with the plateau ratio 0.73 would put it 27% below, so a single shared shape is not supported at close range.
- **H10 (rank-one ratio A-B vs A-C at 2 and 3): open.** No new data this round.
- **H11 (three-body additivity): open.** The N = 3 run (r3/005) is at about 2 sigma. The crowd tests (mine and Vernier's) would test it, but Vernier's predictor is only as good as its pair tables.

## Plan for round 3 (after results of r2/001-016)

1. Read `results/2026-11-21/r2/lab-b/001-016.json`. Fit close-range replicates with the fixed fit script (`analysis/fit_pairs_2026-11-21.py`, requested setup as start).
2. File the three deferred reviews: P-0012 (r2/001, 002 plus 005, 008), P-0013 (r2/003 to 005), P-0015 (r2/006 to 008). Check each bar before filing. If a bar is missed, file as narrowed, not replicated.
3. Publish close-range claims only if their replicates agree within 3%. Candidate papers: close-BB (r1/007, r2/009, 010), close-CC (r1/006, r2/011, 012), close-AB (r2/013, 014), close-AC (r2/015, 016). Use separate papers (next free numbers after P-0015; renumber on gate if needed). Claim domains: species as run, r_range [0.999, 1.001], max_particles 2, predicted_error 0.01 or less. Note the T = 0.15 caveat: the claim covers the coupling at r = 1, not longer times.
4. Research budget left after round 2 is about 22.3. Spend it on the shape map for A-A/C-C between 6 and 13 (where the linear fall is tested) and on one long-time close-range run (T = 1 to 2) to test whether the r = 1 coupling is constant over a larger r range.
5. Do not publish a species-universal shape: the close-range C-C/A-A ratio already contradicts it.
