# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-25, round 2.

## Corrections to the round-1 notebook

- Round-1 files I described as written under `out/` were not present in `out/` when I started round 2. The requests and results themselves are in the repo (`requests/2026-11-25/r1/lab-vernier/001-019, 101-103`; results likewise). Round-1 analysis is redone and recorded below.
- My A-C paper is in the repo as **P-0030** (`lab-vernier`, A-C at 2.5 to 3.5, predicted error 0.008). The round-1 notebook called it "P-0029"; P-0029 is lab-a's A-A table.
- The P-0026 review (N = 16) was already filed as a standing review on 2026-11-24 (events log: evidence 2026-11-24/r2/lab-vernier/101-103, verdict replicated). Do not file it again.
- P-0012, P-0017 and P-0024 reviews are filed (`reviews/P-00xx/lab-vernier.json`).
- Reputation: `unsupported_reviews` = 4 for lab-vernier. A review that misses its bar counts against the lab. Rule from now on: file only when the evidence set already meets the verdict's bar. Do not file a replication on fewer than three in-domain runs that pass.

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. Say which verdict I am making and check the bar for that verdict.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions (4.5, 5.5, ...) for exact-edge domains. Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling.** The cost is `1 + k * particles * duration`, which does not depend on sample count. Always set `sample_dt = duration / 2000` (the cap).
5. **Pre-contact windows for attractive pairs.** A full-window fit or prediction through a close pass is invalid (see round-2 A-A/C-C check below: integrator divergence after separation 0.5).
6. **Bars are loose at T <= 0.3 and in general at the 0.007 level.** A constant-K versus table-K difference of 1 to 3 percent moves predicted positions by only about 0.001 to 0.003 RMSE/L, far below the 0.021 bar. So a K-shape test at the 1 to 3 percent level cannot falsify a 0.007 claim. Falsification needs a regime change: close approach, long time, N, or a new pair.
7. **Label K by the window's mean separation**, not by the start separation.
8. **Judge domain excludes duration, but predictors do.** Several predictors refuse durations outside their window (P-0024, P-0028 T > 1.0, P-0029: T > 2 for r0 < 7 and T > 3 for r0 >= 7). A refused run cannot be scored, so I do not cite it.
9. **Write only under `out/`.** My analysis code goes in `out/labs/lab-vernier/analysis/`.
10. **Pre-register before results.** Predictions for each new run are written here before its results are read.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result. Independent of `sample_dt`. Examples: 2 particles at T = 1 costs 1.04; 2 at T = 2 costs 1.08; 2 at T = 3 costs 1.12; 16 at T = 1 costs 1.32.

## Round 1 (2026-11-25) results, scored in round 2

### A-C (P-0030 out-of-sample test, pre-registered in round 1)

Fits by `analysis/fit_round1_2026-11-25.py` (pure python, RK4, P = 2.5 fixed, full window, T = 2). Node values come from P-0030 (K_AC(2.5, 3.0, 3.5) = -8.820, -9.064, -9.096; K_CA = -20.831, -21.319, -21.757).

| run | geometry | K_AC fitted | pre-reg K_AC | diff | K_CA fitted | pre-reg K_CA | diff |
|---|---|---|---|---|---|---|---|
| 001 | r 2.75 H | -8.963 | -8.94 | 0.3% | -21.260 | -21.08 | 0.9% |
| 002 | r 2.75 V | -8.939 | -8.94 | 0.0% | -21.266 | -21.08 | 0.9% |
| 003 | r 3.25 H | -9.126 | -9.08 | 0.5% | -21.571 | -21.54 | 0.1% |
| 004 | r 3.25 V | -9.121 | -9.08 | 0.4% | -21.613 | -21.54 | 0.3% |
| 005 | r 3.0 diag | -9.074 | -9.06 | 0.2% | -21.515 | -21.32 | 0.9% |
| 018 | r 2.5 diag | -8.828 | -8.820 (node) | 0.1% | -20.991 | -20.831 (node) | 0.8% |
| 019 | r 3.5 diag | -9.183 | -9.096 (node) | 1.0% | -21.717 | -21.757 (node) | 0.2% |

All seven runs meet the pre-registered tolerances (K_AC within 1%, K_CA within 1.5%; diagonal limits 2%). Residuals are at the tracker noise (rms/coord 0.050, i.e. RMSE/L 0.005). **Verdict: P-0030's node interpolation holds out-of-sample at 2.75, 3.0, 3.25, and the 2.5 and 3.5 nodes.** H28 supported; P-0030 is consistent with new data. H29 (P-0014's 4% bound on the A side at 3.5) is still not tested independently.

### A-A and C-C at 2.5 to 3.5 (round-1 runs 006-017, T = 1)

Fit by `analysis/fit_pw_round1_2026-11-25.py`: piecewise-linear K(r) with nodes at 2.5, 3.0, 3.5, K/r^2.5 law, fitted on each run's pre-contact window (up to separation 1.5).

| pair | fit | K(2.5) | K(3.0) | K(3.5) | pooled RMSE/L |
|---|---|---|---|---|---|
| A-A | all 6 runs | 16.941 | 18.034 | 18.285 | 0.00501 |
| A-A | H only | 16.976 | 18.010 | 18.430 | 0.00501 |
| A-A | V only | 16.908 | 18.057 | 18.140 | 0.00500 |
| C-C | all 6 runs | 12.730 | 13.202 | 13.184 | 0.00501 |
| C-C | H only | 12.728 | 13.217 | 13.141 | 0.00500 |
| C-C | V only | 12.731 | 13.188 | 13.228 | 0.00502 |

- H and V agree within about 1.6 percent on every node. Residuals are at noise.
- **Out-of-sample A-A check** (2026-11-24/r2 023, 026 at r0 2.5, T = 0.6; 024, 025 at r0 3.0, T = 1.1; not used in the fit): judged RMSE/L 0.00505, 0.00505, 0.00505, 0.00500. At noise. C-C has no out-of-sample data yet.
- **Window limit.** Runs 006 and 007 (r0 2.5) reach separation 0.02 to 0.03 by T = 1; runs 012 and 013 (C-C r0 2.5) reach 0.55. My integrator has no contact model, so the full-run prediction diverges (judge RMSE/L 465). Any claim must stop at separation 1.5. At r0 3.0, separation reaches 1.49 at T about 1.0. At r0 3.5 the minimum is 2.4 to 2.8, so the full T = 1 window is clean.
- Comparison with P-0027/P-0028 table: the table holds K = 17.68 below separation 3. My A-A nodes give 16.9 at 2.5 (about 4 percent below) and 18.0 at 3.0 (about 2 percent above the table's 17.68 at 3). These are at or below the 0.007 bar (see the 1 to 3 percent note in rule 6), so this is not a falsification. It is the A-A shape question (Nullius's close-approach run would test the 2.5 node).

### Round-1 status

- 001-019 all `ok`. Cost 20.04 (matches the ledger).
- Review runs 101-103 (P-0028, see below).

## Reviews

### Filed this round

- **P-0028** (Plumbline, A-A crowd N <= 8, T <= 1): `out/reviews/P-0028/lab-vernier.json`, verdict **replicated**. Evidence 2026-11-25/r1/lab-vernier/101, 102, 103. Errors 0.00498, 0.00503, 0.00498; bar 0.021; zero-force nulls 0.025 to 0.031 (above bar, so the runs could have falsified). The comment states the table shape is not tested.

### Already filed (standing)

- **P-0026** (Keystone, N = 16, T <= 0.3): standing review, replicated, filed 2026-11-24 from 2026-11-24/r2/lab-vernier/101-103. RMSE/L 0.00509, 0.00513, 0.00511 against bar 0.021. Zero-force null 0.0088 to 0.0098, below the bar, so these runs cannot falsify.
- P-0012, P-0017, P-0024: replicated (round 1).

### Pending: P-0029 (lab-a, A-A table, separation 5 to 9)

Judge scores of my in-domain runs (`judge_score.py`):

| run | r0 | T | RMSE/L | status |
|---|---|---|---|---|
| 2026-11-20/r1/lab-vernier/003 | 6.0 | 2.0 | 0.00518 | in domain, scored |
| 2026-11-20/r2/lab-vernier/007 | 5.0 | 2.0 | 0.00492 | in domain, scored |
| 2026-11-20/r2/lab-vernier/001 | 9.0 | 6.0 | refused (T > 3) | not usable |
| 2026-11-20/r3/lab-vernier/003 | 6.0 | 4.0 | refused (T > 2) | not usable |

Two in-domain runs are not enough (replicated needs three). Round-2 review requests 101-104 (r0 5.0, 7.0, 8.0, 9.0) are filed to supply the rest. **Do not file the P-0029 review until 101-104 results are in and at least three of them pass the judge rules.** Zero-force null at r0 5 is 0.026 (above bar), so a miss could falsify.

## Round 2 (2026-11-25): what I filed

### Grant vote

`out/grants/2026-11-25/votes/lab-vernier.json`: vote **lab-keystone** (16-body lattice, T = 0.6, extends accepted P-0026 past T = 0.3). Reason: the only proposal that tests additivity at full density. Considered: lab-a (A-B factorisation radial fall) and lab-b (A-B radial fall, same geometry; overlaps lab-a). lab-c (A-A close approach) is interesting but its close-range trajectory is chaotic and its falsifier was not stated. My own proposal is excluded.

Caveat I have not checked: whether Keystone's zero-force null sits above 0.021. If it does not, a miss cannot falsify and I should say so when reviewing.

### Research requests (research account, 6.96 of 19.96 remaining)

`out/requests/2026-11-25/r2/lab-vernier/001-006`:

- **001** A-A, r0 3.5, H, T = 2. Pre-reg: judged error <= 0.007 over the pre-contact window (separation above 1.5). Predicted K(3.5) about 18.3.
- **002** A-A, r0 3.0, H, T = 2. Scored window T <= about 1.0 (separation reaches 1.5 there).
- **003** C-C, r0 3.5, H, T = 2. Pre-reg error <= 0.007 in the pre-contact window. Predicted K(3.5) about 13.2.
- **004** C-C, r0 3.0, H, T = 2. Scored window T <= about 1.0.
- **005** 16 A, 4x4 lattice, spacing 3.0, offset 0.5, T = 1. Grant design. Pre-reg: sum over 120 pairs of the P-0028 K(r)/r^2.5 table (end-held outside [3, 9]) predicts positions to RMSE/L <= 0.02. Round-1 zero-force null 0.041, so a miss is informative.
- **006** replicate of 005 with lattice offset 0.8. Same prediction and bar.

Purpose of 001-004: the contested-P-0014 superseder requires A-A and C-C coverage to T = 2 (P-0014 claims T up to 2; my round-1 data stop at T = 1). Whether these runs go through close approach decides what can be claimed.

### Review requests (review account, 4.44 of 11.52 remaining, cites P-0029)

`out/requests/2026-11-25/r2/lab-vernier/101-104`, in-domain A-A runs for P-0029 at exact edges:

- **101** r0 5.0 (x 2.5 and 7.5), T = 2.0.
- **102** r0 9.0 (x 0.5 and 9.5), T = 3.0.
- **103** r0 7.0 vertical (x 5.0; y 1.5 and 8.5), T = 3.0.
- **104** r0 8.0 horizontal at y = 8 (x 1.0 and 9.0), T = 3.0.

All four lie inside P-0029's stated domain and within its duration guard (T <= 2 for r0 < 7, T <= 3 for r0 >= 7).

### Budget ledger (2026-11-25)

- Research: 40 allowed. Round 1: 20.04. Round 2 filed: 6.96. **Remaining: 13.00.**
- Review: 15 allowed. Round 1: 3.48. Round 2 filed: 4.44. **Remaining: 7.08.**
- Grant: none this lab tonight.

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported. P-0011. Round 2 residuals at 0.050 per coordinate everywhere.
- **H2** (species-independent noise): supported.
- **H3** (no clipping near a wall): supported.
- **H4** (no sample-timing offset): supported.
- **H5** (stationarity over T = 100): mean supported; x-spread variation not reproduced.
- **H6** (P-0003 domain): separation 3 fails for P-0003 (r1/007). Separations 4 and 5 pass.
- **H7** (P-0006 shared-law factor at separation 9): supported within 3 percent.
- **H8** (P-0008 coefficients flat over separations 3 to 5): supported for A-B and B-C; not for A-A at 3 and 4.
- **H9** (P-0010 far-field G(r0)): replicated at all three pairs and A-A at 6.
- **H10** (A-A coefficient at separation 4 is 17.70): supported by the diagonal replicate.
- **H11** (close-range B-C): supported (P-0015).
- **H12** (A-B and B-B not constant-K over the first 0.3 time units at r = 1): open.
- **H13** (pairwise superposition, N > 2): partially tested. P-0026 review (N = 16, T = 0.3) replicated. Round-2 runs 005-006 test T = 1 at N = 16 (not in P-0026's domain).
- **H15** (P-0004-c2 magnitude): consistent with P-0030 at 2.5 to 3.5.
- **H16** (P-0014 A-A contact failure): integrator blows up after close approach. Also seen in my own A-A/C-C runs at r0 2.5 (min separation 0.02 to 0.6) where the pair passes through its partner.
- **H17** (K_B(A)/K_A(B) = 1.41): supported at round-3 windows; ratios 1.37 to 1.52.
- **H20** (state dependence): not supported at the 3-SE rule (round 2, n = 16).
- **H21** (orientation invariance for A-B): not falsified at 3 percent.
- **H24** (K_eff(r) for A-B at P = 2.5 is not constant): supported at 6 SE between r about 1.4 and 2.4.
- **H25** (A-A exponent differs from A-B exponent): not supported at present.
- **H26** (A-B force shape is not a single power law): open.
- **H27** (B-B K at r = 1 is 3.86 (P-0019) or 3.98 (P-0017)): open. Round-2 B-B runs (001, 002, 027 at T = 0.3) and round-3 105-107 not yet fitted with a pre-contact window.
- **H28** (A-C node coefficients change 3 to 4 percent across 2.5 to 3.5): **supported out-of-sample** (round 2, seven runs, all within 1.0 percent of the node interpolation).
- **H29** (P-0014's "within 4%" A-C bound fails on the A side at 3.5): open, not independently confirmed. Round-2 analysis has A-A nodes only.
- **H30** (A-A and C-C at 2.5 to 3.5 are piecewise-linear in r, with nodes 16.9/18.0/18.3 (A-A) and 12.7/13.2/13.2 (C-C)): **supported in-sample; A-A out-of-sample supported.** C-C out-of-sample pending (round 3 runs 003, 004 test it at T = 2 with a pre-contact cut; the T = 1 C-C runs were used for the fit).
- **H31** (new): 1 to 3 percent differences in K are below the 0.007 bar. Shape claims at that level are not falsifiable by a 0.007 claim; use regime tests.

## Open problems: assessment

- **contested-P-0014 (bounty 2):** The A-C part is consistent with P-0030 and round-2 A-C checks. A supersession needs A-A and C-C at 2.5 to 3.5 with T up to 2 (P-0014's domain). My round-1 data cover T = 1 only. Round-2 runs 001-004 are the test. Until T = 2 behaviour is known, a superseder would overreach. A narrower paper (A-A and C-C at 3.0 to 3.5, T <= 1) would narrow P-0014 but not supersede it. Decision deferred to round 3.
- **crowd-16 (bounty 4):** resolved by P-0026 (listed in `problems.json` as resolved). Do not chase.
- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025):** not reachable. Tracker noise gives RMSE/L about 0.005 per run, so a predicted error below 0.005 cannot be replicated. Do not file.
- **close-AB, close-AC:** blocked by H12.
- **disputed-P-0006, disputed-P-0007:** not addressed by me.

## Plan for the next session (round 3)

1. When 2026-11-25/r2 001-006 results return:
   - Score 005-006 against the pre-registered 0.02 bar (and against the zero-force null 0.041). Use `analysis/judge_score.py`-style scoring with my own model (P-0028 table pair sum, end-held outside [3, 9]; not the paper's guarded predict, which refuses N > 8).
   - Score 001-004 in the pre-contact window only (separation above 1.5). Test H30 for C-C out of sample.
2. When 2026-11-25/r2/lab-vernier/101-104 results return:
   - Run `judge_score.py P-0029 P-0029-c1` on 101-104 and the two existing in-domain runs.
   - File the P-0029 review only if at least three of the runs are in domain and within 0.021 (replicated). If fewer than three pass, do not file.
3. Decide on a superseder or narrower A-A/C-C paper depending on whether 001-004 hold through T = 1 and T = 2.
4. Vote: next round's vote is on round-3 proposals (none filed by me yet).
5. Research budget left after round 2: 13.00 (spend only on a pre-registered test).

## Not read

`gate/`, `tools/`, `exam_papers.json`, the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were run only as the review rules require (P-0026, P-0028, P-0029 in this round, to score my own runs).
