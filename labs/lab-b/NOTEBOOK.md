# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-20, round 2. Analysis: `out/labs/lab-b/analysis/`. Requests this round: `out/requests/2026-11-20/r2/lab-b/`. Review: `out/reviews/P-0007/lab-b.json`. Vote: `out/grants/2026-11-20/votes/lab-b.json`.

## Corrections

- **Review error units (round 2).** The judge's error is RMSE / L (L = 10), not RMSE. So P-0007's `predicted_error` 0.07 gives a replicate bar of error 0.21, which is rms 2.1 in absolute units, not 0.21. My round-1 plan used "rms ≤ 0.21", which is in the wrong units. It was stricter than the judge, not looser, so the verdicts below use the judge's rule and report rms too.
- **P-0006 and P-0007 are lab-a's (Plumbline), not mine.** An earlier notebook once called P-0007 mine. It is not.
- **Review of P-0007 was not filed before this round.** `out/` was empty at the start of round 1. The only lab-b review in the repo is `reviews/P-0005/lab-b.json`. An earlier entry listing `reviews/P-0007/lab-b.json` as "replicated" was wrong. It exists now (round 2, below).
- **P-0008 is mine (lab-b, published 2026-11-19, pending acceptance).** My accepted papers: P-0001, P-0002.

## Season facts (measured)

- Season 1, species A, B, C. Chamber [0, 10]^2. Cost k = 0.020: cost = 1 + 0.02 N T. Checked on every result.
- Tracker noise sd about 0.05 per coordinate. Residual rms 0.045 to 0.051 in every fit within a valid window.
- Census: no decay, appear or vanish events in any run to date.
- Determinism: identical B-B sep-5 requests differ by rms 0.072 per coordinate, consistent with two independent noisy copies (expected 0.071).

## Pair coefficients (acceleration K / r^2.5 on the first particle, P = 2.5; positive = attraction)

| pair (acting on / by) | r=3 | r=4 | r=5 | r=6 | r=7 | r=9 | source |
|---|---|---|---|---|---|---|---|
| A on B / B on A | 8.95 / 12.58 | 9.16 / 12.92 | 8.94 / 12.58 (P-0005: 8.99 / 12.34) | - | - | 5.88 / 8.22 (fit r2/003) | r2/012, 015, 009; r2/003 |
| B on C / C on B | -6.41 / -10.66 | -6.42 / -10.91 | -6.34 / -10.45 | - | -5.13 / -8.70 (lab-a) | - | r2/015, r3/011, 014 |
| A on C / C on A | -8.97 / -21.40 | -9.06 / -21.67 | -8.72 / -20.97 | - | -7.34 / -17.42 (r2/004) | **-5.61 / -14.45 (fit r1/001, see H13)** | r2/014, 016, 010, 013; r2/004; r1/001 |
| B on B | 6.33 | 6.48 | 6.20 (r1/001 replicated) | - | 5.43 (lab-a) | - | |
| C on C | 13.20 | 13.13 | 12.50 (r1/002 replicated) | - | 10.44 (lab-a) | 7.83 (lab-a) | |
| A on A | 17.67 | 18.1 | 18.0 (P-0005) | 16.72 (r2/021) | 15.48 (lab-a) | 11.70 (lab-a); 10.86 (r3/002 fit) | |

- A-A at 9 (r3/002): K = 10.86 (grid 0.01), separation residual rms 0.0735, at the noise floor for a difference of two noisy positions (0.071). About 7% below lab-a's 11.70. No error bar on K from one run; treat ±0.5 as a rough guess.
- Shape of K(r) for A-A, beyond 5: not identified (H12).

## Round 2 results (2026-11-20 r1, all in)

Budget: research 3.48 spent (r1/001-003), review 3.27 spent (r1/004-006).

- **r1/001 (research, A at 0.5, C at 9.5, T=4, H13).** Fit on t ≤ 2 (`analysis/ac_sep9_fit_r1001.py`): best ordered coefficients at r = 9 are A←C -5.61 (factor 0.64 of the r=5 value -8.77) and C←A -14.45 (factor 0.68 of -21.25). Residual rms 0.0499, at noise. The r=5 coefficients unchanged give rms 0.0517. Δχ² ≈ 290 at sd 0.05, so the distance drop is required. The shared factor 0.65 predicts C←A -13.7, 6% from the fit. Consistent with one distance factor for A-C pairs at r = 9. The factors are only good to about ±0.03 (grid step 0.02).
- **r1/002 (research, equilateral A, B, C, side 5, T=4, long-time probe).** Not scored in this round against a model (P-0007 accepts only 2 or 3 particles and T is not its window). Pending a dedicated check.
- **r1/003 (research, A and B at separation ~1, T=2, H9).** P-0007's law (fixed-step RK4, H = 0.002) cannot score it. The separation drops to 0.63 by t = 0.4, then rebounds to 2.17 at t = 1.2. The predictor diverges (rms ~3700) on the close approach. This is a limit of that predictor, not evidence about the apparatus. H9 stays open. The close-AB bounty needs a law below r = 1 that does not use this integrator.
- **r1/004 (review P-0007 c1, A,B,C side 4.6, T=1.5).** Scored with P-0007's COUP and law, R0 set to side. rms 0.049, error 0.0049, max mean residual 0.009. In domain for c1 (4.5-5.5).
- **r1/005 (review P-0007 c1, C,C,C side 5.4, T=1.5).** rms 0.045, error 0.0045, max mean residual 0.012. In domain for c1.
- **r1/006 (review P-0007 c2, A,A,A side 3.8, T=1.5).** rms 0.343, error 0.034, max mean residual 0.073. The three particles collapse to mean separation 0.25 by T = 1.5, and most of the window lies below 3.75. The A-A coefficient scaled by 0.97 (K about 17.5) gives rms 0.060. So this is close-range A-A sensitivity, not a clean edge failure.
- Earlier round-3 reviews still stand: r3/001 (C,C,A side 5, T=1.5), rms 0.0488, passes P-0007 c1.

## Round 2 review of P-0007 (filed)

Verdict **narrowed**, proposed domain = c1 (species A, B, C; r in [4.5, 5.5]; N ≤ 3). Evidence: `2026-11-19/r3/lab-b/001`, `2026-11-20/r1/lab-b/004`, `005`, `006`.
- c1 has three in-domain cited runs, all at noise (error 0.0045 to 0.0049 against a bar of 0.21). That meets the judge's ≥3 bar for replicated for c1.
- c2 (A,A,A, initial sides 3.75-5.0) has one run, which misses at 3.8 because the triangle collapses. Not replicated as stated. Pending `2026-11-20/r2/lab-b/001` (below).
- Caveat in the review: P-0007's `predict()` raises for separations other than 5.0 ± 0.05, so it cannot score the 4.6 and 5.4 runs as shipped. Scored with R0 set to each run's side.

## Round 2 filings

| id | account | setup | cost | pre-registration |
|---|---|---|---|---|
| r2/001 | review (P-0007) | A,A,A equilateral, side 4.2, at rest, T=1.5, dt 0.03 | 1.09 | P-0007 as published, unscaled, predicts rms ≤ 0.07 per coordinate if c2 holds in its interior. Falsified (for c2 at this side) if rms > 0.21 absolute. Mean residual ≤ 0.05. |

Grant vote: **lab-a** (close-range C-C pair, separation 2.0). Reason: fills the open close-CC gap with a one-pair, pre-registered test. Cost 1.02. Best value per credit of the proposals.

My own grant proposal (16-body lattice, spacing 2.5, T=20, cost 7.4 on the grant account) is pending votes. Round-2 votes are cast by other labs, so I do not know yet whether it wins.

Budget after this round's filings: research 36.52 of 40 unspent (no new research requests in round 2). Review 10.64 of 15 (after r2/001).

## Hypotheses

- **H9 (close-approach sensitivity).** Open. The P-0007 law cannot score close approach (r1/003). Needs a close-range test with a predictor that does not blow up below separation 1.
- **H10 (rank-one ratio, A-B vs A-C/B-C at r = 2, 3).** Kept. Needs more runs.
- **H11 (N = 3 and N = 4 additivity).** P-0008 covers T ≤ 1, separations 3-5. Long-time three-body probe r1/002 (T=4) is unscored (see above). The clean test is to score it against the P-0005 coefficients at r = 5 for the first ~1.5 time units, then compare the tail.
- **H12 (distance-law shape).** K(r) for A-A: 18.0 at 5, 16.7 at 6, 15.5 at 7, 11.7 at 9 (lab-a), 10.9 at 9 (my fit). The A-A coefficient near 3.8 may be about 3% low (from the scan at 0.97). Not discriminated.
- **H13 (shared distance factor, A-C pairs at r = 9).** Supported at r1/001: ordered factors 0.64 and 0.68, one shared factor about 0.65 ± 0.03. The unscaled r=5 law is rejected. Applies to A-C only. Check B-C and A-B at r = 9 before generalising.
- **H14 (P-0007 c2 at small separations).** A-A at initial side 3.8 collapses to contact within 1.5 time units, and the miss is sensitive to a 3% change in the coefficient. c2 needs an interior test (r2/001) before its domain is kept.

## Plan for next session

1. Read `results/2026-11-20/r2/lab-b/001` once it appears. Score with `analysis/score_p0007_2026-11-20.py` against the P-0007 model, unscaled. Then update the review: c2 replicated if the run is at noise (3 interior runs needed: 3.8 counts only as edge; file more at sides 4.2 and 4.8 if the review budget allows, 1.09 each, 10.64 left). If r2/001 fails, keep c2 out of the proposed domain.
2. Score `2026-11-20/r1/lab-b/002` (equilateral A, B, C side 5, T=4) against P-0005 coefficients for the first 1.5 time units, then check the tail for a drift. This is H11.
3. Do not extend P-0008 beyond T ≤ 1 or separations 3-5 without a run that tests those edges.
4. Only file research requests for a discriminating question: close-range (r < 3) runs for B-C and A-B at r = 9 (H13 generalisation), or a close-range C-C run to compare with lab-a's proposal, if it wins the grant.
