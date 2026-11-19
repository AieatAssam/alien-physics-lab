# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost) before making physics claims on top of it, then replicate other labs' claims at their edges.

## Status (round 2, 2026-11-19)

- Round-1 results are back (001-009, all ok). Analysis is done for 001-006 (noise) and 007-009 (reviews).
- **Published:** P-0007 (tracker noise of a lone particle: sd 0.050 per coordinate, species-independent, unbiased at a corner, no mean drift over T=100). Claims c1-c4, with the stationarity anomaly in 006 x stated as open.
- **Reviews written:**
  - P-0003 (lab-a): **falsified** for its stated domain at r=3, T=2. Its own predictor fits run 007 to noise for t<=1.1 but fails after the close encounter at t~1.24 (rms 2.68 for t in (1.1,2.0]). The same predictor fits lab-a's sep-4 runs 003-004 at noise level, including their approach to 0.14. Proposed domain: r 4-6 for T<=2; r=3 only for t<=1.1.
  - P-0005 (lab-a): **replicated** off-axis. Runs 008 (B-C diagonal) and 009 (A-C diagonal): best-fit K within 3% of the paper's values; the paper's model.py gives rms 0.0497 and 0.0511.
- **Review not written yet:** P-0006 and P-0001 (requests 003 and 004 are filed; reviews next session), P-0002 (not reviewed), P-0004 (superseded by P-0005; not reviewed).
- **Vote cast:** lab-keystone (see reason in the vote file). Reason: N=16 additivity is the regime no pair-based paper covers, and the test is cheap and pre-registered.
- **Grant:** my own proposal (three-body triangle, side 5, T=2) is now redundant. I have filed the same setup as research request 2026-11-19/r2/lab-vernier/001 (1.12 credits). If the grant is awarded to me in round 3, I will not run this setup again; I would spend the 120 credits on something else (see plan).

## Facts I rely on (verified this session)

- Cost: `cost = 1 + 0.02 * N * T` holds on every request I have run (N=1 T=20 -> 1.40; N=1 T=4 -> 1.08; N=2 T=2 -> 1.08; N=1 T=100 -> 3.00).
- Samples: `T/dt + 1` samples per result (001-004: 2001; 005: 401; 006: 2001 at dt=0.05).
- Season: L=10, species A, B, C, difficulty 2.
- Tracker noise (001-006, 10,005 residual samples per coordinate pooled over at-rest runs): sd x 0.0502, y 0.0501. Per-species sd within 4%. Kurtosis 2.9 to 3.3. Lag-1 |r| at most 0.056.
- Three-body prediction recomputed (`analysis/predict_three_body_grant.py`): A (+0.0824, -0.1359), B (-0.1662, -0.0945), C (+0.0953, +0.4933). Matches the earlier notebook values.
- Encounter physics (007): the sep-3 A-A pair closes to separation 0.17 at t~1.24 (tracker) and the particles pass through each other, then separate. The power law without a core does not describe the post-encounter motion. The sep-4 pair in lab-a's 003-004 approaches only to 0.14 at t=2 and does not pass, and the predictor fits it.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported. sd 0.050, kurtosis 2.9-3.3, lag-1 at most 0.056 (mean +0.016, s.e. 0.007). Not falsified.
- **H2 (species-independent noise).** Supported at this N. A, B, C sd within 4%, below the 5% falsifier.
- **H3 (no boundary effect at the corner (0.3,9.7)).** Supported but weak. Mean offset (-0.001, +0.0003), sd 0.0505/0.0506, no clipping. The nominal point is about six sd from each wall, so it is not a clipping test. A proper wall test needs a point within about 1 sd of a wall.
- **H4 (no timestamp jitter).** Not falsified, not strongly tested. Run 005 (speed 2): sd_x 0.0497, sd_y 0.0542 (y/x = 1.09). Jitter would make sd_x larger, the opposite sign. The excess in y is about 2 s.e. in one run and has no mechanism; I do not claim anything about it. Could be chance.
- **H5 (stationarity over T=100).** Mean: supported (quarter-run means within 0.0043 of truth). sd: **open anomaly**. Run 006 x has segment sds 0.0470, 0.0527, 0.0535, 0.0476, a 13% spread, p=0.004 uncorrected. Nine other series are consistent with a constant sd (p 0.27-0.83). The pre-registered threshold was 10%, so the x-spread is above it. Replicate filed: 2026-11-19/r2/lab-vernier/002. If the replicate reproduces the spread (>10%, p<0.01), H5 is falsified for x and P-0007 c4 must be corrected to say so.

## Reviews: method and results

- Method: `analysis/pair_fit.py` (RK4 two-body with directed couplings K_i(j)/r^2.5), `analysis/review_fits2.py` (2-parameter grid over the full window), `analysis/review_paper_models.py` (runs the reviewed paper's own `model.py` on the review request, windowed at t<=1.1 and t>1.1). Use the paper's own predictor for the verdict; my integrator is a cross-check only.
- 007 (P-0003 at r=3, T=2): own predictor rms 0.0487 for t<=1.1; 2.68 for t in (1.1,2.0]. K-only fit t<=1.1: 17.5, rms 0.048. Verdict: falsified as stated, narrowed domain proposed.
- 008 (P-0005 B-C diagonal): best K_B(C) -5.94 (paper -6.10), K_C(B) -10.36 (paper -10.59). Paper model rms 0.0497.
- 009 (P-0005 A-C diagonal): best K_A(C) -8.68 (paper -8.77), K_C(A) -20.76 (paper -21.25). Paper model rms 0.0511.
- Caveat: my K fits have no uncertainty estimate. The 1-3% agreement is an agreement statement, not a precision claim.

## Issues I noticed in other labs' papers (for review next session)

- P-0001 (lab-b): the falsification text says "RMSE above 0.03 in chamber units, i.e. 0.3 absolute", which is 10x inconsistent. Its own noise sd is 0.05 absolute, so an RMSE threshold of 0.03 chamber units (0.3 absolute) is not the right number. The review should say which unit it uses.
- P-0003 (lab-a): the falsification rule says "0.03 normalized units (0.3 chamber units)". The domain statement "durations 1 to 2 at separations 3-6" is what 007 falsifies. Also the lab-a runs 003-004 are at separation 4, not 3, as the paper's text might be read.
- P-0006 (lab-a): the factor 0.65 at r=9 is from two A-A runs only. Predicted A-C at r=9 is pre-registered in 2026-11-19/r2/lab-vernier/003.

## Budget ledger

| day/round | account | requests | cost | remaining |
|---|---|---|---|---|
| r1 | research | 001-006 | 9.68 | 30.32 at start of r2 (matches ledger) |
| r1 | review | 007-009 | 3.24 | 11.76 at start of r2 |
| r2 | research | 001 (three-body triangle) | 1.12 | |
| r2 | research | 002 (replicate of 006, T=100) | 3.00 | 26.20 after r2 |
| r2 | review | 003 (P-0006, A-C r=9, T=3) | 1.12 | |
| r2 | review | 004 (P-0001, corner, T=10) | 1.20 | 9.44 after r2 |

Grant: none in round 2 (votes only). Round-3 award, if any, will be at most 120 credits on account `grant`.

## Plan for next round (round 3)

1. Read r2 results. Priority:
   - 002 (replicate of 006): decides whether H5 is falsified for x.
   - 001 (three-body triangle): pre-registered; falsified if rms > 0.06 per coordinate over t<=2 for any particle. If it passes, a paper on additivity at N=3 for this geometry (P-0008). If it fails, a notebook note and a paper only once the failure is checked against noise.
   - 003 (P-0006, A-C at r=9): pre-registered K within 10%. Write a review of P-0006.
   - 004 (P-0001, corner): write a review of P-0001, using the lab-b claim's own unit convention (see issues above).
2. If the round-2 grant is awarded to me, use the 120 credits for a test I do not already have: the three-body setup is now run, so spend on a near-wall noise test (a particle at 1 sd from a wall, to test H3 properly) or on the sep-3 encounter (r=3 pair, T=2, at a different orientation, to test the core).
3. Consider a P-0003 narrowing paper only if a repeat of 007 confirms the encounter.

## Notes for reproducibility

- All analysis code is in `out/labs/lab-vernier/analysis/` (`load_results.py`, `pair_fit.py`, `review_fits2.py`, `review_paper_models.py`, `noise_stationarity.py`, `predict_three_body_grant.py`).
- Run with plain `python3` from the analysis directory (not `-I`) because numpy and scipy are installed in the user site.
- The wall-less integrator in `pair_fit.py` is valid only while particles stay away from walls. Do not use its full-window fits for runs with encounters or wall contact.
- I have not read `gate/`, `tools/`, `exam_papers.json` or any predictor/score files. I will not.
