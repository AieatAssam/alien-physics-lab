# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-20, round 3. Analysis: `out/labs/lab-b/analysis/`. Requests this round: `out/requests/2026-11-20/r3/lab-b/` (001-010). Review filed this round: `out/reviews/P-0010/lab-b.json`.

## Corrections

- **The judge's error is RMSE / L (L = 10), and it is only as sensitive as the bar allows.** The bar is 3 x predicted_error. P-0010 has predicted_error 0.01, so a run passes at error 0.03 (rms 0.3). Scaling all pair coefficients of P-0010 by 0.9 or 1.1 moves the error on my runs by at most 0.0005 (`analysis/sens_p0010_2026-11-20.py`). So a judge "replicated" says a claim is at noise level, not that its coefficients are good to better than about 10%. My notes should use coefficient-shift tests, not error bars, for accuracy claims.
- **P-0007's shipped predict() refuses any side other than 5.0 +/- 0.05.** My round-2 review of P-0007 scored runs at sides 3.8, 4.2, 4.6 and 5.4 with `score_p0007_2026-11-20.py`, which overrides R0. That override is disclosed in the review, but it means the judge will be unable to score four of my five P-0007 runs with the shipped code. Only `2026-11-19/r3/lab-b/001` (side 5.0) is scoreable as shipped. Fix is in this round's filings (below), to be used next round.
- **Round-2 claim that A-A at 9 is "about 7% below lab-a's 11.70" was over-precise.** That is withdrawn. The A-A run at 9 (`2026-11-19/r3/lab-b/002`) changes error by only 0.0001 to 0.0002 between K scale 0.88 and 1.0. The data do not separate 10.9 from 12.3.
- **Review error units (round 2).** The judge's error is RMSE / L, so P-0007's predicted_error 0.07 gives a bar of error 0.21, which is rms 2.1 in absolute units. My earlier "rms <= 0.21" plan was stricter than the judge, so earlier verdicts used the judge's rule.
- **P-0006 and P-0007 are lab-a's (Plumbline), not mine.** P-0008 is mine (pending). My accepted papers: P-0001, P-0002.

## Season facts (measured)

- Season 1, species A, B, C. Chamber [0, 10]^2. Cost k = 0.020: cost = 1 + 0.02 N T. Checked on every result.
- Tracker noise sd about 0.05 per coordinate. Residual rms 0.048 to 0.053 in every run scored with a shipped predictor this round (per-run errors 0.0049 to 0.0053).
- Census: no decay, appear or vanish events in any run to date.
- Determinism: identical B-B sep-5 requests differ by rms 0.072 per coordinate, consistent with two independent noisy copies (expected 0.071).

## Pair coefficients (acceleration K / r^2.5 on the first particle, P = 2.5; positive = attraction)

| pair (acting on / by) | r=3 | r=4 | r=5 | r=6 | r=7 | r=9 | source |
|---|---|---|---|---|---|---|---|
| A on B / B on A | 8.95 / 12.58 | 9.16 / 12.92 | 8.94 / 12.58 (P-0005: 8.99 / 12.34) | - | - | 5.88 / 8.22 (fit r2/003) | r2/012, 015, 009; r2/003 |
| B on C / C on B | -6.41 / -10.66 | -6.42 / -10.91 | -6.34 / -10.45 | - | -5.13 / -8.70 (lab-a) | - | r2/015, r3/011, 014 |
| A on C / C on A | -8.97 / -21.40 | -9.06 / -21.67 | -8.72 / -20.97 | - | -7.34 / -17.42 (r2/004) | -5.61 / -14.45 (fit r1/001) | r2/014, 016, 010, 013; r2/004; r1/001 |
| B on B | 6.33 | 6.48 | 6.20 (r1/001 replicated) | - | 5.43 (lab-a) | - | |
| C on C | 13.20 | 13.13 | 12.50 (r1/002 replicated) | - | 10.44 (lab-a) | 7.83 (lab-a) | |
| A on A | 17.67 | 18.1 | 18.0 (P-0005) | 16.72 (r2/021) | 15.48 (lab-a) | 11.70 (lab-a); 10.9 (r3/002 fit, not resolved) | |

Shape of K(r): the three pair families fall by 5 to 35% between r = 5 and r = 9. Nothing is measured beyond r = 9 by any lab. The linear G in P-0010 (`G(r) = 1.51 - 0.092 r`, zero at r = 16.4) is an extrapolation past its data. That is the target of this round's far-range runs.

## Round 3 results and scores (all with shipped predictors unless stated)

Budget at the start of this session: research 36.52 of 40 unspent; review 10.64 of 15 unspent (ledger: 2026-11-20 research used 3.48, review used 4.36).

- **`2026-11-20/r2/lab-b/001` (review, P-0007 c2 probe, A,A,A side 4.2, T=1.5).** Shipped predict() raises (side 4.2). With the R0 override (my own scorer): rms 0.0506, error 0.0051, max mean residual 0.015. At noise. Interior run, so c2 has one interior and one edge run; see the plan.
- **`2026-11-20/r1/lab-b/002` (research, A,B,C side 5, T=4; H11 probe).** Scored with P-0007's shipped predict() (side 5.0 is accepted; the probe is not part of the claim's T=1.5 window). Windows (`analysis/window_r1_002_2026-11-20.py`):
  - t in [0, 1.5): rms 0.0514, error 0.00514, max |mean residual| 0.009.
  - t in [1.5, 2.5): rms 0.0517, error 0.00517, max |mean| 0.014.
  - t in [2.5, 4.0): rms 0.0586 (excess about 0.03 over noise), max |mean| 0.037.
  - Reading: the pair sum holds at noise to T = 2.5 and drifts after. Two explanations I cannot separate yet: (a) a three-body term (H11); (b) a small coefficient error at r about 4 (A-C at 4 differs from its r = 5 value by about 4%, and over T about 3 that gives a displacement of about 0.05). Read as an open question for H11 and H12, not as evidence for either.
- **Other labs' papers, scored with shipped predictors (for the reviews below):**
  - P-0009 (lab-a, B,C pair; sep 4.99-5.01; N<=3; T=2): four in-domain lab-b runs, all B,C at sep 5, T=2, N=2: `2026-11-19/r1/lab-b/001` (BB) 0.00494, `2026-11-19/r1/lab-b/002` (CC) 0.00499, `2026-11-19/r2/lab-b/002` (BB) 0.00503, `2026-11-18/r3/lab-b/014` (BC) 0.00505. None tests three-body additivity.
  - P-0010 (keystone, pairs at rest r0 6-9, T<=6): five in-domain runs, 0.00498 to 0.00505 (table in the review).
  - P-0011 (vernier, lone particle): two N=1 runs in domain: `2026-11-17/r1/lab-b/001` (A, moving, T=10) 0.00531; `2026-11-17/r2/lab-b/005` (C, moving, T=40) 0.00509. Need a third for the judge's >= 3.
  - P-0007 (lab-a, shipped): only `2026-11-19/r3/lab-b/001` (side 5.0, CCA) is scoreable, 0.00488.

## Reviews filed this round

- **P-0010 (keystone): replicated.** Evidence: 2026-11-19/r2/lab-b/003, 004; 2026-11-19/r3/lab-b/002; 2026-11-20/r1/lab-b/001; 2026-11-18/r2/lab-b/021. All five pass (error 0.0050 against bar 0.03). The comment says the replication is for A-A, A-B and A-C pairs only, that B-B, B-C and C-C at 6-9 are not tested, and that the bar is too loose to measure coefficient accuracy.
- **P-0009 (lab-a): held.** Four in-domain runs pass, but they are all N=2. The claim is about N=3 additivity, which none of my runs test. Verdict waits for `2026-11-20/r3/lab-b/005` (B,C,C at side 5, T=2).
- **P-0011 (vernier): held.** Two in-domain N=1 runs. Judge needs three. Verdict waits for `2026-11-20/r3/lab-b/004`.
- **P-0007 (lab-a): existing review "narrowed" stands.** Its replicate basis (sides 4.6, 5.4, 3.8, 4.2) relies on the R0 override described above. Next round I will update it with `r3/001` to `003` (side 5.0), which the shipped predictor can score.

## Requests filed this round (round 3, 2026-11-20)

Totals: review 6.83 of 10.64 spent (3.81 left after filing); research 4.88 of 36.52 spent (31.64 left). I am not spending the rest. Budget is scarce, and I have no further discriminating question yet.

| id | account | setup | cost | pre-registration |
|---|---|---|---|---|
| r3/001 | review (P-0007 c2) | A,A,A side 5.0, at rest, T=1.5, dt 0.03 | 1.09 | shipped P-0007 gives rms <= 0.07 per coordinate. Falsified for c2 if rms > 0.21. |
| r3/002 | review (P-0007 c1) | A,B,C side 5.0, T=1.5, dt 0.03 | 1.09 | same bar |
| r3/003 | review (P-0007 c1) | B,B,C side 5.0, T=1.5, dt 0.03 | 1.09 | same bar |
| r3/004 | review (P-0011) | one B particle from (2.0, 8.0), v (1.3, -0.7), T=10, dt 0.05 (bounces off walls) | 1.20 | rms <= 0.07 per coordinate; a wall-law error would raise it |
| r3/005 | review (P-0009) | B,C,C side 5.0, at rest, T=2, dt 0.02 (N=3 test) | 1.12 | rms <= 0.07 per coordinate |
| r3/006 | review (P-0010 edge) | B-C pair, sep 6.0 on the diagonal, at rest, T=6, dt 0.003 | 1.24 | P-0010 shipped: K_B(C) = -5.54, K_C(B) = -9.61, 3% tolerance |
| r3/007 | research (far range) | A-A pair, sep 12.0 on the diagonal, at rest, T=6, dt 0.003 | 1.24 | linear G (P-0010) predicts K_AA(12) = 7.3; power-law continuation of lab-a's 6-9 slope predicts about 9.1. Fit decides at 3%. |
| r3/008 | research (H13) | B-C pair, sep 9.0 along x, at rest, T=4, dt 0.002 | 1.16 | P-0010 with C-factor: K_B(C) = -3.94, K_C(B) = -6.85; without: -4.16, -7.22. 3% tolerance decides which. |
| r3/009 | research (far range) | A-C pair, sep 12.0 on the diagonal, T=6, dt 0.003 | 1.24 | linear G: K_A(C) = -3.37, K_C(A) = -8.17; continuation: about -4.4, -11.2 |
| r3/010 | research (far range) | C-C pair, sep 12.0 on the diagonal, T=6, dt 0.003 | 1.24 | linear G: K_C(C) = 4.75; continuation: about 6.1 |

All geometry was checked: separations are exact, all particles start inside the chamber, and every request has at most 2000 samples. Pairs at 12 sit on the 45-degree diagonal, from (0.757, 0.757) to (9.243, 9.243), so they stay inside the walls over T=6.

## Hypotheses

- **H9 (close-approach sensitivity).** Open. The P-0007 law cannot score close approach (r1/003 in round 2). Needs a predictor that does not blow up below separation 1. Not tested this round.
- **H10 (rank-one ratio, A-B vs A-C/B-C at r = 2, 3).** Kept. Needs more runs. Not tested this round.
- **H11 (three-body additivity).** Open. The ABC side-5 probe (r1/002) is at noise to T = 2.5, then drifts by about 0.03 rms with mean residuals up to 0.037. A three-body term and a coefficient error at r about 4 both fit. The clean test is an N=3 run with B,C,C (r3/005) plus a pair test at r about 4 that isolates the candidate coefficient.
- **H12 (distance-law shape).** Open, and this round's main question. Candidates: (i) linear G (P-0010), which is K(r) falling linearly to zero near r = 16.4; (ii) a power-law continuation of the 6-9 slope (about 0.88 on top of r^-2.5); (iii) constant K (already rejected at 9). r3/007 and r3/009 and r3/010 discriminate (i) from (ii) at about 25% in K.
- **H13 (shared distance factor).** Partly supported for A-C and A-B at r = 9 (lab-keystone's runs and my r1/001). Not yet tested for B-C at 9. r3/008 does that.
- **H14 (P-0007 c2 at small separations).** Open. The A-A miss at side 3.8 (round 2) is a shipped-predictor issue, not an edge failure. Resolved for the judge only by side-5.0 runs (r3/001), since the shipped code refuses everything else.

## Plan for next session

1. Read `results/2026-11-20/r3/lab-b/` for 001 to 010. Score with the shipped predictors (`analysis/score_shipped_2026-11-20.py`), not the R0 override.
2. Update P-0007 review with r3/001-003 (side 5.0, shipped-scoreable). Keep c2 as narrowed to side 5.0 unless the judge's metric says otherwise.
3. File the P-0009 verdict with r3/005 (N=3). File the P-0011 verdict with r3/004 (moving lone particle). Replicate only if all in-domain runs pass.
4. Score far-range runs r3/007, 009, 010 against linear G and the power-law continuation. If the measured K sits at 7.3 +/- 3%, that is a bold, striking, falsifiable law (linear G, zero at r about 16.4), and I can draft a paper with domain r 6-12 and max_particles 2. If it sits near 9.1, the claim is a power-law over 6-12 instead. If neither, state it as narrowed.
5. Score r3/008 (B-C at 9) to test the S_C factor and the shared G for B-C.
6. Do not publish a paper for H11 until the N=3 and coefficient-at-r4 tests are in. Do not extend close-approach claims without a predictor that works below r = 1 (H9).
