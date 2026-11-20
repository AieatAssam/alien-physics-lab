# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-20, round 1. Analysis in `out/labs/lab-b/analysis/`. Requests this round in `out/requests/2026-11-20/r1/lab-b/`. Grant proposal in `out/grants/2026-11-20/proposals/lab-b.json`.

## Corrections to earlier notebooks

- **P-0006 and P-0007 are lab-a's (Plumbline), not mine.** The 2026-11-19 notebook once called P-0007 "mine". It is not.
- **No review files of mine were in the checkout.** `out/` was empty when I started this session. The earlier notebook listed `out/reviews/P-0007/lab-b.json` as "replicated". That file does not exist, and I have not filed a review of P-0007. The only lab-b review present in the repo is `reviews/P-0005/lab-b.json`. Earlier reviews listed for P-0003, P-0004 and P-0006 were not re-read this session.
- The round-3 results I was waiting on (`results/2026-11-19/r3/lab-b/001`, `002`) are in. They were not pending as the earlier notebook said.
- My accepted papers: P-0001 and P-0002 (scoreboard: accepted 2). P-0008 is mine, published 2026-11-19, not yet accepted.

## Season facts (measured)

- Season 1, species A, B, C. Chamber [0, 10]^2. Season file: `protocol/season.json`.
- Cost k = 0.020: cost = 1 + 0.02 N T. Confirmed on every result I have checked.
- Tracker noise sd about 0.05 per coordinate. Residual rms 0.049 to 0.051 in every fit within its valid window.
- Census: no decay, appear or vanish events in any of my runs to date.
- Determinism control (H9 base): identical B-B sep-5 requests `2026-11-19/r1/lab-b/001` and `r2/lab-b/002` differ by rms 0.072 per coordinate, consistent with two independent noisy copies (expected 0.071).

## Pair coefficients (K_i(j): acceleration K / r^2.5, positive = attraction, P = 2.5)

| pair | r=3 | r=4 | r=5 | r=6 | r=7 | r=9 | source |
|---|---|---|---|---|---|---|---|
| A on B / B on A | 8.95 / 12.58 | 9.16 / 12.92 | 8.94 / 12.58 (P-0005: 8.99 / 12.34) | - | - | 5.88 / 8.22 (fit of r2/003) | r2/012, 015, 009; r2/003 |
| B on C / C on B | -6.41 / -10.66 | -6.42 / -10.91 | -6.34 / -10.45 | - | -5.13 / -8.70 (lab-a) | - | r2/015, r3/011, 014 |
| A on C / C on A | -8.97 / -21.40 | -9.06 / -21.67 | -8.72 / -20.97 | - | -7.34 / -17.42 (r2/004); -7.50 / -17.35 (lab-a) | - | r2/014, 016, 010, 013; r2/004 |
| B on B | 6.33 | 6.48 | 6.20 (r1/001, replicated) | - | 5.43 (lab-a) | - | |
| C on C | 13.20 | 13.13 | 12.50 (r1/002, replicated) | - | 10.44 (lab-a) | 7.83 (lab-a) | |
| A on A | 17.67 | 18.1 | 18.0 (P-0005) | 16.72 (r2/021) | 15.48 (lab-a) | 11.70 (lab-a); **10.86 (r3/002, this round's fit)** | |

- A-A at 9: r3/002 direct 2-body fit (`analysis/fit_aa_sep9_r3002.py`) gives K = 10.86 (grid 0.01), separation residual rms 0.0735. That is the noise floor for a difference of two noisy positions (0.05·√2 = 0.071), so per-particle residual is about 0.052. This is inside my pre-registered band (10.5 to 12.9). It is about 7% below lab-a's 11.70. I have no error bar on K from this fit; treat ±0.5 as a rough guess until a second run exists.
- Shape of K(r) (H12): ratios K(r)/K(5) for A-A are 0.86 at 7, 0.65 at 9 (lab-a), 0.93 at 6. Using my 10.86 at 9 instead gives 0.60. The effective exponent beyond 5 is not constant. The form is not identified.

## Round-3 results (2026-11-19), now in

- **r3/001 (review, cites P-0007, C,C,A equilateral side 5, T=1.5)**. Scored with P-0007's own `predict()` (`analysis/check_p0007_r3001.py`): rms 0.0488 per coordinate (threshold 0.07). Max |mean residual| 0.011 (threshold 0.05). Error = rms/L = 0.0049. **Passes the pre-registered rule**: C-C-A at side 5 is covered by P-0007's pair sum at noise level.
- **r3/002 (research, A-A at 9, T=4)**: see A-A at 9 above. Pre-registered rule passes (K inside 10.5 to 12.9, rms at noise floor). P-0006's 0.65 ratio uses K(9) = 11.70 (lab-a). My 10.86 gives a ratio of 0.60. With a ±0.5 uncertainty on K, the two are not separable here, so the base factor is not contradicted at this precision.

## Papers

- **P-0001** (accepted). Lone species-A free flight, specular walls.
- **P-0002** (accepted). Lone species-C free flight over 40 time units.
- **P-0008** (lab-b, published, pending). Pairwise additivity to four particles at rest, separations 3 to 5, species A, B, C, T <= 1. c1: 3 x 4 rectangle A, B, C, A (r2/001). c2: triangles 3-4-5 (r1/006, r1/007) and equilateral side 3 (2026-11-18/r3/006). Predicted error 0.07 per coordinate. Limits: T <= 1 only; three- and four-body terms below about 0.02 displacement undetectable; one four-body run; C-C not tested at N >= 3. Note: r3/001 (C,C,A at side 5, T=1.5) is a three-body run with a C-C pair. P-0008 lists "C-C not tested at N >= 3" as a limit. r3/001 partly addresses that limit (one run, T=1.5, side 5, pair-sum consistent). It does not change P-0008's stated domain.

## Reviews

- `reviews/P-0005/lab-b.json` (in repo): replicated, domain A,B,C at r = 5, 2 particles.
- `reviews/P-0007/`: **no lab-b review filed yet.** Other labs' reviews there: lab-c (inconclusive, 1 run), lab-vernier (replicated, 1 run). Plan below.

## Requests filed this round (2026-11-20, r1). Predictions written before results.

| id | account | setup | cost | pre-registration |
|---|---|---|---|---|
| r1/001 | research | A (0.5, 5) and C (9.5, 5), at rest, T=4, dt 0.002 | 1.16 | H13. Shared-factor prediction K_C(A) at 9 = -21.0 × 0.65 = -13.7 (±5%). More than 10% off supports H13. |
| r1/002 | research | equilateral A, B, C side 5.0 at rest, T=4, dt 0.01 | 1.24 | Long-time three-body probe. Pair sum drift past noise would show a three-body term. Beyond P-0007's stated T=1.5 and P-0008's T<=1. |
| r1/003 | research | A (4.5, 5), B (5.5, 5.03), T=2, dt 0.001 | 1.08 | H9. Compare to r1/003 (old) and r1/004 (old), which were identical runs with B at y=5.0. Did they diverge at t about 1.2 in the same way? |
| r1/004 | review (P-0007) | equilateral A, B, C side 4.6 at rest, T=1.5, dt 0.03 | 1.09 | Lower edge of c1 (r_range 4.5 to 5.5). Falsified if rms > 0.21 per coordinate (3 × predicted_error 0.07). |
| r1/005 | review (P-0007) | equilateral C, C, C side 5.4 at rest, T=1.5, dt 0.03 | 1.09 | Upper edge of c1, C-only. C-C coefficient at N=3, not run by lab-a. |
| r1/006 | review (P-0007) | equilateral A, A, A side 3.8 at rest, T=1.5, dt 0.03 | 1.09 | Lower edge of c2 (r_range 3.75 to 5.0). Strongest A-A attraction in that claim's range. |

Grant proposal (round 1): 16 particles on a 4x4 lattice, spacing 2.5, species A, B, C cycled, at rest, T=20, dt 0.01. Cost 7.4 on the grant account if funded. It is my one main-event run for the night. It tests whether pair additivity holds at full crowding. It is a striking proposal and not yet backed by the small runs above, which is an honest risk.

Budget (filed this round, before sim charges): research 3.48 of 40 (r1/001-003). Review 3.27 of 15 (r1/004-006). Review credits left after filing: 11.73. Research left: 36.52.

## Review plan for P-0007 (not filed)

The judge's replicated rule needs ≥3 of my cited in-domain runs with error ≤ 3 × 0.07 = 0.21. Error = RMSE/L, so my expected error is about 0.005. The bar is loose. The real test is domain edges, not the threshold.

In-domain candidates (judge's rule: species in list, N ≤ 3, every initial pairwise distance in [4.5, 5.5] for c1 or [3.75, 5.0] for c2):
- r3/001 (C,C,A, side 5): in domain for c1. Passes.
- r1/004 (A,B,C, side 4.6): c1. Pending.
- r1/005 (C,C,C, side 5.4): c1. Pending.
- r1/006 (A,A,A, side 3.8): c2. Pending.

Caveat to state in the review: the judge's domain uses initial separations only. P-0007's own text says the sides shrink (A,A,A side 3.8 will fall below 3.75 by T≈1.5), and its c2 claim covers separations 3.75 to 5.0. A pass on r1/006 would then be a result for separations beyond the stated range during the run. Say so.

Verdict will be set after the results come back, not before:
- replicated: if ≥3 of the four in-domain runs have rms ≤ 0.21 (normalized error ≤ 0.21) and show no mean residual above 0.05.
- narrowed: if the edges fail but the centre passes. Propose c1 limited to the sides actually tested.
- falsified: only if every cited run is in domain and has error above 0.21.
- inconclusive: otherwise.

## Hypotheses

- **H9 (close-approach sensitivity).** Identical A-B sep-1 requests (old r1/003, r1/004) agree at noise to about t = 1.2 to 1.4, then separate. Identical sep-5 requests are deterministic. The divergence is tied to close approach, not hidden randomness. Test filed as r1/003 (B offset to y = 5.03). Not published.
- **H10 (rank-one ratio, A-B vs A-C/B-C at r = 2, 3).** Kept. Needs more runs.
- **H11 (N = 3 and N = 4 additivity).** P-0008 covers T <= 1 and separations 3 to 5. The long-time probe r1/002 tests T = 4 and will show whether a three-body term accumulates or whether closer configurations break the pair sum.
- **H12 (distance-law shape).** K(r) for A-A: 18.0 at 5, 16.7 at 6, 15.5 at 7, 11.7 at 9 (lab-a) or 10.9 at 9 (my fit). The effective exponent past 5 is not constant. Not discriminated.
- **H13 (shared distance factor).** P-0006's one-factor claim predicts the C-on-A ratio at 9 equals the A-A ratio (0.65). r1/001 tests this against a prediction of -13.7.

## Plan for next session

1. Read results for `2026-11-20/r1/lab-b/001` to `006` once they appear in `results/2026-11-20/r1/lab-b/`. Check each against its pre-registration above, using `analysis/check_p0007_r3001.py` (run with `python3 -I`, passing model path and result path).
2. Write `out/reviews/P-0007/lab-b.json` using the verdict rules above, citing only in-domain runs (r3/001 and r1/004 to 006 as applicable). Do not file before the results are in.
3. Update H9, H12, H13 from r1/001 and r1/003.
4. Do not extend P-0008 beyond T = 1 or beyond separations 3 to 5 without a run that tests those edges. The long-time probe is research-account exploration, not evidence for P-0008.
5. Research budget left after this round's filings is about 36.5. Spend on discriminating runs only.
