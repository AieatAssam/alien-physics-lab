# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-19, round 2.

## Status

- Round-1 results are in (`results/2026-11-19/r1/lab-keystone/001-016`, all ok, k = 0.02 confirmed: cost = 1 + 0.02 N T on every run).
- Filed this round:
  - Paper **P-0007** (`out/papers/P-0007/`): pair couplings times one shared radial factor, separations 3 to 9, 2 to 4 particles at rest. Supersedes P-0003 and lists P-0004. Four claims (c1 A-A radial factor 3-9; c2 shared factor at r=8 for mixed species; c3 r=3 consistency, weak; c4 N=3,4 additivity).
  - Reviews: P-0001 replicated, P-0002 replicated, P-0003 replicated, P-0005 inconclusive, P-0006 replicated. P-0004 not reviewed (superseded by P-0005).
  - Round-2 research requests `2026-11-19/r2/lab-keystone/001-005` (pre-registered, not yet run).
  - Grant vote for lab-a (Plumbline), reason on file.
- Budget today: research 40 allowance, 7.2 used in round 1, 6.04 committed to round-2 requests, about 26.8 left for later rounds. Review: 11.32 used, 3.68 left, unused.

## What round 1 told me

Each row is a run; "K" is the coefficient in the magnitude K * g(r), with g(r) = r^-2.5 unless stated. All residuals are tracker rms per coordinate (noise about 0.05).

1. **Lone particles (reviews 001, 002, 016).** Species A at speed 4.2 for T=10 (rms 0.055), species C at speed 6.0 for T=20 (rms 0.049), species B at speed 1.8 for T=20 (rms 0.050, same reflected-line law). Free flight holds beyond P-0001's and P-0002's tested speeds. Lone B was not claimed by anyone; it now is in the data.

2. **Radial law, A-A (reviews 003, 004, 005; in pool with lab-a runs).** The effective coefficient K_eff at fixed shape r^-2.5 falls with separation: 17.5 (r=3), 17.7 (4), 18.0 (5), 16.5 (6), 15.5 (7), 13.9 (8), 11.9 (9). Run 003 (r=8) and 004 (r=9) are my own. My round-1 pre-registered predictions for run 003 (final separation): H1 power law 3.17, H2 screened form 3.85. Measured 4.45. For run 004: H1 5.88, H2 6.47; measured 6.92. Both forms predicted too much attraction at 8 and 9. (Re-running the K=17.74 model gives 3.28 at r=8, which is not the same as H1 in the file; I use the file values as the pre-registered ones.) Pooled fit over all A-A runs: exp(-r/6)/r^2 gives rms 0.0525 against 0.056 for r^-2.75 (power law best at 2.75). Both rms are near noise, so the shape is not settled; the decline is clear.
   - Verdict on my own pre-registration: H1 and H2 both rejected at 8 and 9, the data show more decline than either. The plan said to fit an exponent instead of choosing a form if neither matched. I did that: K_eff(r) is fitted per run and pooled.

3. **Pair table at r=3 (review 005-010, T=1).** Signed coefficients as fractions of the P-0005 table: A-A 0.97, 0.98; A-B 0.97, 0.93; A-C 1.13, 1.02; B-B 1.04, 1.25; C-C 1.09, 0.95; B-C 1.02, 1.15. Mean about 1.04. The two B-B coefficients (same species, should be equal) differ by 20%, so single-coefficient precision at T=1 is about 10%. **H-pair-scaling (H3 in old notes) is not falsified, but this test has too little power to confirm it at 10%.** Several coefficients sit at 1.13-1.25, outside a 10% bar; I do not claim they are real.

4. **Mixed pairs at r=8 (research 013-015).** A-B: 0.763, 0.767 (agreeing at 0.5%). A-C: 0.814, 0.776. B-C: 0.842, 0.756. A-A factor at 8: 0.773. So one shared radial factor matches mixed pairs to 5-9% per coefficient, pair means to about 3%. This is the test I wanted before a synthesis: out of sample for mixed species, although the factor came from one A-A run.

5. **N=3 and N=4 additivity (research 011, 012, T=2).** Pairwise sum with the P-0005 table and r^-2.5: rms 0.050 (011) and 0.051 (012), at noise; no-interaction baseline 0.44-0.47. Largest single end-point miss 0.097 (011) and 0.103 (012), at endpoint-noise level. The pre-registered 0.1 threshold on final positions is touched, not clearly crossed. With G(r) instead of plain r^-2.5: rms 0.053 and 0.052, slightly worse. The table at 4-5 is best without the factor, consistent with G ~ 1 there.

## Hypotheses (state after round 1 data)

- **H-additive (N>2 pairwise additive).** Supported at N=3 and 4 within noise (see 5). Still untested at 16 particles (my grant proposal is for that). Not tested at N>=5 anywhere.
- **H-shared-factor (one radial factor for all species pairs).** Supported at r=8 for three mixed pairs (4); consistent at r=3 at the 10% precision available (3). Not tested at 6, 7 for mixed species, or at 9 beyond A-A and C-C (P-0006).
- **H-power (pure r^-2.5 with constant K over 3-9).** Rejected: K_eff falls by 33% from r=5 to r=9.
- **H-lone-B.** Supported by 016.

## Synthesis paper

P-0007 folds P-0003 (A-A 3-6), P-0005 (table), and P-0006 (factors at 7, 9) into one predictor: table x G(r) x r^-2.5 for separations 3-9, 2-4 particles, at rest, durations up to 6. Claim wording is narrow: c2 is at 8 only, c3 is explicitly weak, c4 is at separations 4-5.7 only. The P-0005 table at separation 5 is inherited and not re-measured. Predictor validated on all in-domain repo runs at tracker noise (rms 0.046-0.056 for A-A, which is in-sample for G; 0.048-0.053 for mixed and N-body runs, out of sample).

Known weak points to watch for in review:
- G(8) rests on one A-A run; G(6) on two; G(9) on three.
- Equal radial shape for all species is assumed, tested at one separation (8).
- Plain table (no G) fits N=3/4 slightly better than G-model. I kept G for consistency with the r=8 finding; a challenger could use this.
- The B-C pair at r=8 has the largest scatter (+8.8% and -2.2%).

## Round-2 pre-registered requests (not yet run)

Filed as `out/requests/2026-11-19/r2/lab-keystone/001-005`, cost 6.04, research account. Predictions in `out/labs/lab-keystone/analysis/predictions_round2.json` (from P-0007 predictor, G(r) as above).

| # | pair | r | T | pre-registered K (per particle) |
|---|---|---|---|---|
| 001 | C-C | 8 | 5 | 9.55 |
| 002 | C-C | 9 | 6 | 8.13 |
| 003 | A-B | 9 | 6 | K_A(B) 5.92, K_B(A) 8.12 |
| 004 | B-C | 6 | 4 | K_B(C) -5.59, K_C(B) -9.71 |
| 005 | B-B | 8 | 5 | 4.73 |

Falsification: any measured coefficient (fit with r^-2.5 shape, two-particle, tracker noise) more than 10% from its prediction counts against P-0007 c1/c2 at that separation. If the G=1 alternative (no decline) fits 002 (C-C at 9) better than G, c1 fails at 9. C-C at 8 and 9 and B-B at 8 test species-dependent shape, which c2 does not cover.

## Grant

- My proposal (16 particles, 4x4 lattice, T=1, mixed species, pre-registered 15% additivity threshold) is on file for round 2.
- My vote: **lab-a** (Plumbline, long crowded census T=100). Reason: it is the only proposal testing long-time, crowded dynamics and census events; the pre-registered null is falsifiable. I did not vote for my own.
- Other proposals I judged redundant with round-1 data: lab-b (4-body rectangle, our N=4 test 012 already covers that), lab-c and lab-vernier (equilateral triangle at side 5 at T=4 and T=2; our N=3 test at sides 4-4.5 already matches the pairwise sum).

## Reviews filed this round

- P-0001 replicated (run 001): speed 4.2 at T=10 fits the reflected-line law.
- P-0002 replicated (run 002): speed 6.0 at T=20 fits.
- P-0003 replicated (run 005 at r=3; 003, 004 outside and used as evidence for the domain edge, not against the claim). Upper edge at 6 not settled: rms difference between K=17.74 and per-run best K at 6 is 0.0006-0.0013, too small to narrow the claim.
- P-0005 inconclusive: all claims are at r=5, my runs are at 3 and 8. r=3 and r=8 data are consistent with the table times one shared factor, not a test of the table itself.
- P-0006 replicated: r=8 mixed-pair coefficients agree with the shared factor (c6 domain 7-9 interior); run 004 (A-A at 9) gives factor 0.68 vs 0.65 claimed, within the 0.06 predicted error.
- P-0004 not reviewed: superseded by P-0005.

## Plan for next session

1. Read round-2 results for `2026-11-19/r2/lab-keystone/001-005`. Compare each to `predictions_round2.json` with `analysis/make_round2.py` logic (or a new script). Write the comparison into `analysis/`.
2. If C-C at 8 and 9 and B-B at 8 come in within 10% of P-0007, file a short P-0008 or an update note: "P-0007 extended to all species at 8 and 9". Otherwise file a narrowing (c2 restricted to A-B and A-C at 8, or c1 domain reduced).
3. Look at round-1 review responses (other labs' reviews of P-0007 once published). Respond to any falsification by checking the cited run first.
4. Optional: the r=3 pair test is limited by approach time (T=1), so longer runs are not possible there. Replicating the r=3 runs with sample_dt 0.02 would give about 1.6x the information for the same cost. Not yet requested.
5. The N=16 lattice test (grant, if won) is the only N>4 test. Do not claim additivity beyond N=4 until it runs.

## Caveats (own work)

- All K_eff values use a fixed shape r^-2.5. A different shape would move each node, but the ratios across separations are what the claim uses; I have not fitted a free shape per run.
- Node values for G at 6, 8, 9 rest on 1-3 runs each. Per-run K precision is about 2-3% at T=2-6.
- The round-1 H1/H2 numbers (3.17, 3.85) are in `labs/lab-keystone/analysis/predictions_round1.json`. A separate check with K=17.74 gives 3.28 for run 003; that is not the pre-registered H1, and I do not quote it as one.

## Things not to do

- Do not try to locate simulator source or hidden parameters. Attempts are logged and disqualify the lab.
- Do not claim masses. P-0004 and P-0005 infer mass ratios from Newton's third law, which is an assumption; P-0007 does not use them.
- Do not extend P-0007 beyond four particles, separations 3-9, or durations above 6 without new runs.

## Analysis files (out/labs/lab-keystone/analysis/)

- `sim.py`: shared pure-python integrator and loaders (no numpy in this environment).
- `check_lone.py`: lone-particle checks (reviews 001, 002, 016).
- `fit_aa.py`, `pool_aa.py`, `keff_aa.py`: A-A radial law, per-run K_eff, pooled power vs screened fits.
- `fit_mixed.py`: signed two-coefficient fits for r=3 (005-010) and r=8 (013-015).
- `check_nbody.py`: N=3, N=4 additivity against the table and the G-factor version.
- `check_p0003_domain.py`: P-0003 constant K on its own separation-6 runs.
- `validate_p0007.py`: P-0007 predictor against all in-domain runs.
- `make_round2.py`, `predictions_round2.json`: round-2 requests and their predictions.
