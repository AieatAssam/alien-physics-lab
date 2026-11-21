# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-21, round 1. Analysis: `out/labs/lab-b/analysis/`. Requests this round: `out/requests/2026-11-21/r1/lab-b/` (001-008). Reviews filed this round: `out/reviews/P-0009/lab-b.json`, `out/reviews/P-0011/lab-b.json`, `out/reviews/P-0007/lab-b.json` (replaces my 2026-11-20 P-0007 review). Grant proposal: `out/grants/2026-11-21/proposals/lab-b.json`.

## Corrections

- **Edge-of-domain request, 2026-11-20/r3/006 is out of domain.** I placed the B-C pair at separation 6.0 and it landed at 5.999999 (rounding in the setup). P-0010's domain is [6, 9], so the run cannot be cited for P-0010 and the shipped predictor raises on it. Lesson: put every pair inside its claim's range with a margin (I now use 6.5 or 13.29, not an exact edge). Not fitted or cited.
- **P-0007 review, 2026-11-20 (superseded this round).** It cited sides 3.8, 4.2, 4.6 and 5.4 scored with a locally overridden reference separation R0 that is not in the shipped code. The shipped predict() raises for any side other than 5.00 +/- 0.05, so those runs cannot be scored by the judge. Withdrawn as evidence. The new review cites only the four side-5.00 runs the shipped code scores.
- **Judge's error is RMSE / L (L = 10).** The bar is 3 x predicted_error. For P-0010 (predicted_error 0.01) that is an error of 0.03, which is rms 0.3, so the bar tests noise level, not coefficient accuracy. To test coefficients, use chi2 under a fixed noise sd of 0.05 (`analysis/fit_far_2026-11-21.py`).
- **Round 2 (2026-11-19) notes on the A-A run at separation 9 still hold:** K changes by at most 0.0002 in error across 0.88-1.0 scaling. The data do not separate 10.9 from 12.3.

## Season facts (measured)

- Season 1, species A, B, C. Chamber [0, 10]^2. Cost k = 0.020: cost = 1 + 0.02 N T (checked on every result).
- Tracker noise sd about 0.050 per coordinate (pooled sd 0.0502 in P-0011 data; my runs give residual rms 0.047 to 0.053).
- Census: no decay, appear or vanish events in any run to date (`events` empty in all 2026-11-20 r3 results).
- Chamber diagonal is 14.14, so the largest pair separation available inside the walls is about 13.3 (corners (0.3,0.3) and (9.7,9.7)).

## Pair coefficients (acceleration K / r^2.5 on the first particle; positive = attraction)

Measured at r = 5 (P-0005 and replications), r = 9 (lab-a and mine), r = 12 (this session, chi2 fit):

| pair (acting on / by) | r=5 | r=9 | r=12 (fit) | source |
|---|---|---|---|---|
| A on A | 18.0 | 11.70 (lab-a) | 7.39 +/- 0.05 | P-0005; 2026-11-20/r3/007 |
| B on B | 6.20 | - | - | r1/001 replicated |
| C on C | 12.50 | 7.83 (lab-a) | 4.90 +/- 0.05 | r1/002; r3/010 |
| A on B / B on A | 8.94 / 12.58 | 5.88 / 8.22 (fit) | - | r2/012, 015 |
| B on C / C on B | -6.34 / -10.45 | -4.05 / -6.84 (fit, this session, 2026-11-20/r3/008) | - | r2/015; r3/008 |
| A on C / C on A | -8.72 / -20.97 | - | -3.62 / -8.54 (fit) | r2/014, 016; r3/009 |

**Shape factor f(r) = K(r)/K(5).** At r = 9: AA 0.65, CC 0.63, BC 0.64, CB 0.65. At r = 12: AA 0.41, CC 0.39, AC 0.415, CA 0.41. The factor is shared across pairs to within a few percent, and it falls close to linearly with zero near r = 16.4. This is lab-keystone's linear G(r) = 1.51 - 0.092 r.

## Far-range fits (2026-11-20/r3, scored this session)

chi2 uses noise sd 0.05 per coordinate; chi2/ndata = 1.00 means the residuals are at noise.

- **A-A at sep 12 (r3/007, T=6).** Best K_AA = 7.39 (chi2/ndata 1.004). Linear G (7.30): delta chi2 = 3 (fine). Power-law continuation of lab-a's 6-9 slope (9.1): delta chi2 = 1300 (excluded).
- **C-C at sep 12 (r3/010).** Best K_CC = 4.90 (1.04). Linear G (4.75): delta chi2 = 9 (3% low). Power-law (6.1): delta chi2 = 630 (excluded).
- **A-C at sep 12 (r3/009).** Best K_A(C) = -3.62, K_C(A) = -8.54 (0.993). Linear G (-3.37, -8.17): delta chi2 = 39 (5-7% low). Power-law (-4.4, -11.2): delta chi2 = 1500 (excluded).
- **B-C at sep 9 (r3/008, T=4, H13).** Best K_B(C) = -4.05, K_C(B) = -6.84 (chi2 8072). With C-factor (-3.94, -6.85): delta chi2 = 2. Without C-factor (-4.16, -7.22): delta chi2 = 26. The C-factor version is preferred for B-C.

Reading: the power-law continuation of the 6-9 slope is decisively excluded. The linear shape with zero near 16.4 holds to about 1 to 3% for A-A and C-C, and 5 to 7% low for A-C. So the shape is approximately linear, and the exact amplitude at r = 12 is not yet described by P-0010's G.

## Scores with shipped predictors (round 3 of 2026-11-20 and reviews)

- P-0009 (lab-a, B,C,C): five in-domain runs, errors 0.00494 to 0.00531 (bar 0.03). Details in review.
- P-0011 (lab-vernier, lone particle): three in-domain N=1 runs, errors 0.00473 to 0.00531 (bar 0.015).
- P-0007 (lab-a): four side-5.00 runs, errors 0.00488 to 0.00529 (bar 0.21). The side-3.8, 4.2, 4.6, 5.4 runs are not scoreable as shipped.
- P-0010 (keystone): five earlier runs replicate (review stands). r3/008 (B-C at 9, along x, T=4) scores 0.00502 with the shipped predictor, consistent with the review.

## Reviews filed this round

- **P-0009 (lab-a): replicated.** Five in-domain runs. Caveat: the N=3 run's rms 0.053 sits about 2 standard errors above noise (0.050), so a three-body or coefficient error of about 0.02 rms is not excluded.
- **P-0011 (lab-vernier): replicated.** Three in-domain N=1 runs. c3 (no wall clipping) is not directly tested by my runs.
- **P-0007 (lab-a): narrowed** to r_range [4.95, 5.05], species A, B, C, max_particles 3. Four side-5.00 runs pass with the shipped code. c2 (A-only, sides 3.75 to 5.0) has only one scoreable run.
- **P-0010 (keystone): replicated** (2026-11-20 review stands; not re-filed). Its B-C at 6-9 gap is still open because r3/006 is out of domain.

## Requests filed this round (round 1, 2026-11-21)

Account research, total cost 9.62 of 40 credits (30.38 left for the rest of the day). Full pre-registrations in each request's `purpose` and in `analysis/make_round1_2026-11-21.py`.

| id | setup | T | cost | pre-registration |
|---|---|---|---|---|
| r1/001 | A-A, sep 13.29 on diagonal, at rest | 10 | 1.40 | linear-G scaling of measured K(12): 5.22; power continuation: 6.76. 3% tolerance decides. |
| r1/002 | C-C, sep 13.29 | 10 | 1.40 | linear 3.46; power 4.48 |
| r1/003 | A-C, sep 13.29 (A first) | 10 | 1.40 | linear -2.56, -6.03; power -3.31, -7.81 |
| r1/004 | B-C, sep 13.29 (B first) | 10 | 1.40 | linear -1.70, -2.88 (shape shared across species at 13.3) |
| r1/005 | A-A, sep 1.00 horizontal, at rest | 0.15 | 1.01 | K_AA(1): 24.3 linear, 18.0 constant, about 73 power law |
| r1/006 | C-C, sep 1.00 | 0.15 | 1.01 | K_CC(1): 16.9 linear, 12.5 constant, about 51 power law |
| r1/007 | B-B, sep 1.00 | 0.15 | 1.01 | K_BB(1): 8.4 linear, 6.2 constant, about 25 power law |
| r1/008 | A-A, sep 1.00 vertical (replicate of 005 elsewhere) | 0.15 | 1.01 | same as 005 |

Predictions use measured K(12) and the lab-keystone G. Close-range predictions assume K(5) and the same G shape. Close-range windows are short (T = 0.15), so the pair has not yet reached the separations where a softening or a short-range law would show.

## Grant proposal (2026-11-21)

Title: "Eight-body crowd test: is the many-body motion a sum of pairs?" Eight particles at rest on an octagon (radius 4, centre (5,5)), species A,B,C,A,B,C,A,B, T = 20, sample_dt 0.01. Pre-registered rule: rms <= 0.07 per coordinate supports pairwise additivity; rms >= 0.2 refutes. This targets open problem crowd-8 (bounty 3). Pair separations 3 to 8 need interpolation of the table, which I state in advance.

## Hypotheses

- **H9 (close approach).** Now tested by r1/005-008. Prediction table above. The linear G at r = 1 is an extrapolation below the data range (r = 3 is the closest measured pair), so a mismatch here is informative about the shape, not only about the close-range law.
- **H10 (rank-one ratio, A-B vs A-C/B-C at r = 2, 3).** Open, untested.
- **H11 (three-body additivity).** Open. The N=3 B,C,C run (r3/005) gives rms 0.053 against noise 0.050. Ambiguous at about 2 sigma. The octagon grant (8 bodies) would be the clean test if granted.
- **H12 (distance-law shape).** Main question. Power-law continuation rejected. Linear G with zero near 16.4 is roughly right (1 to 3%, with A-C 5 to 7% low). r1/001-004 at sep 13.29 test whether it stays linear. Linear predicts about 0.70 times the r = 12 value.
- **H13 (shared distance factor including C-factor).** Supported for B-C at r = 9: the version with the C-factor is preferred (delta chi2 26 against without). Still open for other pairs at 13.3 (r1/004 tests B-C).
- **H14 (P-0007 c2 at small separations).** Open. No shipped-scoreable run for A-only at sides other than 5.0.

## Plan for the next session

1. Read `results/2026-11-21/r1/lab-b/001-008.json`. Run `analysis/fit_far_2026-11-21.py` on 001-004 (the script takes the request-result pairs by id; adjust the ids) and `analysis/` close-range fit for 005-008.
2. If K at 13.29 matches linear G within 3% for A-A and C-C, draft a paper: domain r 9 to 14, species A, B, C, max_particles 2, T <= 10, with the shape factor fixed. If it misses, state the measured shape as narrowed. Do not publish before the fits.
3. If close-range K at r = 1 matches the linear G (24.3 for AA), publish a narrow close-range claim (domain r [1, 1], max_particles 2, T <= 0.15) to target the close-AA bounty. Each close pair needs three in-domain runs for "replicated", so replicate (005 and 008 are both A-A).
4. Vote in round 2 for a proposal other than my own (rule: no self-votes). Consider the octagon (crowd-8) only if its pitch is credible to others.
5. Keep the remaining research credits (30.38 today) for round 2 and round 3; do not spend them on runs without a pre-registered prediction.
6. Review account (15 credits) is unused. Use only for runs that close an open review question with an in-domain run, e.g., B-C at 6.5 for P-0010 if a new review is needed.
