# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-26, round 1 (grant proposal night).

## Round 1 summary (2026-11-26)

- **Grant result scored (H32 closed):** round-3 grant runs 2026-11-25/r3/lab-vernier/001-004 (jittered 4x4 A lattice, spacing 3.0, T = 1, N = 16) score against the P-0028 pair table at **0.00501, 0.00499, 0.00501, 0.00501** (bar 0.02; zero-force nulls 0.041 to 0.043). H13 and H32 are supported at N = 16 with tangential force structure, T = 1. Scored with `analysis/additivity16_2026-11-25.py` (argument order: request file, then result file).
- **Reviews requested (pending results):** eleven review-account requests, `out/requests/2026-11-26/r1/lab-vernier/001-011`, each with `cites_paper` set. Reviews are filed in the next session, once the results return. Projected cost (1 + 0.02 x N x T, from the cost model): 12.10 of 15 review credits.
  - **P-0031** (lab-b, 3 or 4 A, pairs 5.0 to 7.1, T <= 2): 001 equilateral side 5.5; 002 equilateral side 6.9 (upper edge); 003 scalene 5.3/6.1/6.9 (asymmetric N = 3, not claimed by the paper but in the judge domain); 004 square side 5.02 rotated 30 deg (diagonal 7.099).
  - **P-0033** (lab-keystone, 4 A, pairs 5.0 to 7.08, T <= 2): 005 square side 5.005 axis-aligned (5,5); 006 square side 5.005 rotated 30 deg (4,4); 007 square side 5.005 rotated 15 deg (6,5). Side 5.005 keeps the diagonal (7.078) inside the claim's 7.08 limit.
  - **P-0032** (lab-c, 2 A, r0 2.0 to 2.5, T <= 0.6, walls >= 2.0): 008 r0 = 2.0 horizontal; 009 r0 = 2.5 horizontal; 010 r0 = 2.25 diagonal; 011 r0 = 2.0 diagonal.
- **Grant proposal filed (round 1):** "Close-approach probe: four A pairs at rest, initial separation 1.0, T=2" (`out/grants/2026-11-26/proposals/lab-vernier.json`). Eight particles, pair centres at (2.5, 2.5), (7.5, 2.5), (2.5, 7.5), (7.5, 7.5). The pitch asks what contact does below separation 2, where no paper currently has coverage.
- **Research:** no research requests filed this round. Reasoning below under "Research budget".

## Pre-registered predictions for the round-1 review runs (written before results)

Each prediction is the cited paper's own `predict()`, run on the same setup (accepted by all 11 setups; scripts in `out/labs/lab-vernier/analysis/design_reviews_2026-11-26.py`).

| request | paper | setup | predicted min pair separation over run | expected judged RMSE/L if the paper's law holds |
|---|---|---|---|---|
| 001 | P-0031 | equilateral 5.5, T = 2 | 3.80 | about 0.005 (noise floor) |
| 002 | P-0031 | equilateral 6.9, T = 2 | 6.12 | about 0.005 |
| 003 | P-0031 | scalene 5.3/6.1/6.9, T = 2 | 3.82 | about 0.005 |
| 004 | P-0031 | square 5.02, rot 30, T = 2 | 3.13 | about 0.005 |
| 005 to 007 | P-0033 | square 5.005, T = 2 | 3.09 | about 0.005 (K held flat below 5 is the stated weak point; a deviation would show here) |
| 008 | P-0032 | r0 2.0, T = 0.6 | **0.69** | uncertain: the paper's law closes the pair to 0.69, below the separation range where its evidence was taken; this is the main test |
| 009 | P-0032 | r0 2.5, T = 0.6 | 1.81 | about 0.005 |
| 010 | P-0032 | r0 2.25 diag, T = 0.6 | 1.34 | about 0.005 to 0.01 |
| 011 | P-0032 | r0 2.0 diag, T = 0.6 | 0.69 | same as 008 |

Null (zero-force) RMSE/L for these runs is expected to be 0.02 to 0.04 for T = 2 and about 0.005 to 0.01 for T = 0.6 (attraction is weaker over less time). Power: the null sits above the bar in every T = 2 run, so each run discriminates the law from no force. For the T = 0.6 runs the null is probably below the bar, so those runs test the law's shape, not whether a force exists.

Verdict plan (per the review rules):

- **P-0031:** "replicated" if at least 3 of 4 runs score at most 0.021 (3 x 0.007). "falsified" only if all four are in domain and above 0.021. An asymmetric run (003) that misses while the symmetric ones pass is a "narrowed" verdict (not claimed: asymmetric N = 3), not a falsification.
- **P-0033:** same bar (0.021) on 005 to 007. Note that the paper's domain is judged on distances only, so a 3-particle run (not planned here) would also be in domain. I did not file one, because it is outside the claim's stated scope.
- **P-0032:** bar is 3 x 0.006 = 0.018. Runs 009 and 010 are the separation-range core; 008 and 011 are the lower edge. Replicated needs at least 3 passing runs. If only 008 and 011 miss while 009 and 010 pass, the verdict is "narrowed" (proposed domain: separation in [2.25, 2.5], or the lower edge excluded), not falsified. Falsified only if all four miss.
- No review is filed unless the evidence already meets the verdict's bar. The `unsupported_reviews` counter for lab-vernier is 4; do not add to it.

## Grant proposal (round 1): close-approach probe

- Why this and not the round-3 extension: the round-3 jittered lattice runs to close passes if extended to T = 2 (my check: minimum pair separation 0.007 to 0.014 by T = 2, and 1.2 to 1.3 already by T = 1). A T = 3 extension would confound additivity with contact, so the proposal would give an unreadable result.
- Design: four isolated A pairs at rest, initial separation 1.0 each. Measurement first: what does contact do? (follows K/r^2.5, softens, bounces, merges). Pre-registered falsifier: the unclamped P-0026 law predicts all four pairs to RMSE/L 0.02 or better through T = 2. A miss marks the contact gap.
- Caveat for the next session: pair centres 5 apart couple weakly (about 0.24 acceleration at separation 5). Scoring must include this coupling through the tables, not assume isolated pairs.

## Research budget

- 40 credits today (research). None spent. Reason: at the 0.007 bar and tracker noise of 0.05, a parameter shift of 1 to 3 percent moves the prediction by about 0.001 to 0.003 RMSE/L and cannot be seen. Candidates examined and rejected this round: an A-C 4 percent check at separation 3.5 (H29; undetectable at this bar), H12 (A-B close range; blocked, the window closes too fast), extension of the N = 16 lattice to T = 2 or 3 (close passes; see above).
- Research credits do not roll over; the 40 are lost at day end. Spending on the grant main event is separate.

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. Say which verdict I am making and check the bar for that verdict.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions (4.5, 5.5, ...) for exact-edge domains, or sit a small margin inside the edge (as with side 5.005 and 5.02 this round). Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling.** The cost is `1 + k * particles * duration`, which does not depend on sample count. Always set `sample_dt = duration / 2000` (the cap).
5. **Pre-contact windows for attractive pairs.** A full-window fit or prediction through a close pass is invalid (integrator divergence after separation about 0.5). Scores use the window before the first measured separation below 1.5. The judge scores the full run, so a review on a run that closes below 1.5 can be decided by what the simulator does in the close-approach part; check the pre-contact prediction separately.
6. **Bars are loose at T <= 0.3 and in general at the 0.007 level.** A constant-K versus table-K difference of 1 to 3 percent moves predicted positions by only about 0.001 to 0.003 RMSE/L, far below the 0.021 bar. Falsification needs a regime change: close approach, long time, N, or a new pair.
7. **Label K by the window's mean separation**, not by the start separation.
8. **Judge domain excludes duration, but predictors do.** Several predictors refuse durations outside their window (P-0024, P-0028 T > 1.0, P-0029: T > 2 for r0 < 7 and T > 3 for r0 >= 7). A refused run cannot be scored, so I do not cite it as evidence. P-0031 refuses T > 2 and P-0032 refuses T > 0.6 (the review runs above stay inside both).
9. **Write only under `out/`.** Analysis code is in `out/labs/lab-vernier/analysis/`. Copies of `judge_score.py`, `additivity16_2026-11-25.py` and `fit_tools.py` are there now; the older source folder is `labs/lab-vernier/analysis/`.
10. **Pre-register before results.** Predictions for each new run are written here before its results are read.
11. **Asymmetric layouts are in the judge domain but not in a paper's claim** when the claim says so. A miss there is a "narrowed" verdict, not a falsification, unless the paper's stated scope includes them.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result. Independent of `sample_dt`. Examples: 2 particles at T = 1 costs 1.04; 2 at T = 0.6 costs 1.024; 4 at T = 2 costs 1.16; 16 at T = 1 costs 1.32; 16 at T = 3 costs 1.96; 8 at T = 2 costs 1.32.

## Results and analysis

### Round-3 grant: H32 (N = 16, jittered lattice, T = 1)

| run | offset / seed | RMSE/L vs P-0028 pair table | null | status |
|---|---|---|---|---|
| r3/001 | 0.5 / 101 | 0.00501 | 0.0419 | pass (bar 0.02) |
| r3/002 | 0.5 / 102 | 0.00499 | 0.0418 | pass |
| r3/003 | 0.8 / 103 | 0.00501 | 0.0408 | pass |
| r3/004 | 0.8 / 104 | 0.00501 | 0.0435 | pass |

Verdict on the pre-registered falsifier: no miss. Additivity holds at N = 16 with tangential force structure, T = 1, minimum pair separation about 1.2 (close enough that the table below 3 is extrapolated flat; the pre-registered sensitivity to that choice was 0.0006).

### 16-body pairwise superposition, earlier (round 2 runs 005, 006; lattice spacing 3.0, T = 1)

- RMSE/L 0.00500 and 0.00501; zero-force nulls 0.0425 and 0.0419. Pre-registered bar 0.02. Pass.
- H13 now supported at N = 16, T = 1 (both untilted and jittered lattices). Not tested at T > 1 or close approach.

### A-A and C-C at 3.0 to 3.5, T up to 2 (round 2 runs 001 to 004; round 1 runs 006 to 017)

Piecewise-linear nodes from `analysis/fit_pw_round1_2026-11-25.py` (all 6 runs per species; K/r^2.5 law; P = 2.5 fixed):

| pair | K(2.5) | K(3.0) | K(3.5) |
|---|---|---|---|
| A-A | 16.941 | 18.034 | 18.285 |
| C-C | 12.730 | 13.202 | 13.184 |

Scored on pre-contact windows (first measured separation below 1.5):

| run | pair | r0 | window end | judged RMSE/L | null |
|---|---|---|---|---|---|
| r2/001 | A-A | 3.5 | 1.373 | 0.00504 | 0.0297 |
| r2/002 | A-A | 3.0 | 0.995 | 0.00501 | 0.0206 |
| r2/003 | C-C | 3.5 | 1.578 (cut 2.0: 1.401, 0.00507) | 0.00508 | 0.0283 |
| r2/004 | C-C | 3.0 | 1.163 (cut 2.0: 0.983, 0.00498) | 0.00500 | 0.0227 |

All four are at the noise floor, inside the pre-registered 0.007 bar. H30 (A-A and C-C piecewise nodes) is supported out-of-sample for both species within the pre-contact windows. Windows reach separation 1.5 only at T about 1.0 to 1.58, so the paper is restricted to T <= 1.

### Round-1 A-A and C-C at 2.5 (not claimed)

Runs 006, 007 (A-A) and 012, 013 (C-C) at r0 2.5 reach separations of 0.02 to 0.6 within T = 1. The integrator has no contact model, so their predictions diverge (RMSE/L in the hundreds). Excluded from all claims. This is the same contact gap the close-approach probe (grant) targets, and it bears directly on P-0032's 0.69 prediction (review runs 008 and 011).

### A-C (P-0030 out-of-sample check, round 2)

Runs 001 to 005, 018, 019 (round 1) at separations 2.5 to 3.5 match P-0030's node interpolation within 1.0 percent (K_AC) and 1.5 percent (K_CA). H28 supported. H29 (P-0014's 4 percent bound on the A side at 3.5) is open and untestable at the 0.007 bar.

### P-0029 judge scores (round 3)

Judge scores with the paper's own predict:

| run | r0 | T | RMSE/L | null | status |
|---|---|---|---|---|---|
| r2/101 | 5.0 | 2.0 | 0.00499 | 0.0238 | in domain, pass |
| r2/102 | 9.0 | 3.0 | 0.00505 | 0.0086 | in domain, pass |
| r2/103 | 7.0 | 3.0 | 0.00500 | 0.0155 | in domain, pass |
| r2/104 | 8.0 | 3.0 | 0.00501 | 0.0115 | in domain, pass |
| 2026-11-20/r1/003 | 6.0 | 2.0 | 0.00518 | 0.0181 | in domain, pass (not cited) |
| 2026-11-20/r2/007 | 5.0 | 2.0 | 0.00492 | 0.0264 | in domain, pass (not cited) |
| 2026-11-20/r2/001 | 9.0 | 6.0 | refused (T > 3) | | not usable |
| 2026-11-20/r3/003 | 6.0 | 4.0 | refused (T > 2) | | not usable |

Verdict: replicated (four cited, bar needs three).

## Papers

- **P-0034** (round 3, A-A and C-C at 3.0 to 3.5, T <= 1, supersedes P-0014 inside that domain). Title: "A-A and C-C pairs at rest, separation 3.0 to 3.5, T <= 1: piecewise-linear K(r) nodes, supersedes P-0014 in that domain." Claims P-0034-c1 (A-A), P-0034-c2 (C-C); domain r_range [3.0, 3.5], max_particles 2; predicted error 0.007. Evidence: round-1 runs 008-011 (A-A) and 014-017 (C-C), all T = 1; self-check 0.00497 to 0.00509. It is in `papers/P-0034` under my lab id; I have not checked its acceptance status. Limits: no separation 2.5, no T > 1, no N >= 3, no velocities, no mixed pairs.
- **P-0030** (round 1, A-C at 2.5 to 3.5; predicted error 0.008). Not the same number as the round-1 notebook's "P-0029" note; P-0029 is lab-a's A-A table.
- Standing reviews: P-0012, P-0017, P-0024 (replicated, round 1); P-0028 (replicated, round 1, evidence 2026-11-25/r1/lab-vernier/101-103); P-0026 (replicated, filed 2026-11-24 from 2026-11-24/r2/lab-vernier/101-103); P-0029 (replicated, round 3, evidence 2026-11-25/r2/lab-vernier/101-104).

Paper numbers: P-0031 (lab-b), P-0032 (lab-c), P-0033 (lab-keystone) are the three awaiting my review. P-0014 is lab-keystone's paper (A-C / separation-5 table), which P-0034 supersedes for A-A and C-C inside [3.0, 3.5].

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported. P-0011. Residuals at 0.050 per coordinate in all runs.
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
- **H13** (pairwise superposition, N > 2): **supported at N = 16, T = 1** (round 2 runs 005, 006; round-3 grant runs 001 to 004 with tangential structure).
- **H15** (P-0004-c2 magnitude): consistent with P-0030 at 2.5 to 3.5.
- **H16** (contact failure, close approach): integrator blows up after close approach in P-0014 (lab-keystone) and in my own A-A/C-C runs at r0 2.5 (min separation 0.02 to 0.6). Open; the grant proposal probes it.
- **H17** (K_B(A)/K_A(B) = 1.41): supported at round-3 windows; ratios 1.37 to 1.52.
- **H20** (state dependence): not supported at the 3-SE rule (round 2, n = 16).
- **H21** (orientation invariance for A-B): not falsified at 3 percent.
- **H24** (K_eff(r) for A-B at P = 2.5 is not constant): supported at 6 SE between r about 1.4 and 2.4.
- **H25** (A-A exponent differs from A-B exponent): not supported at present.
- **H26** (A-B force shape is not a single power law): open.
- **H27** (B-B K at r = 1 is 3.86 (P-0019) or 3.98 (P-0017)): open. Round-2 B-B runs not yet fitted with a pre-contact window.
- **H28** (A-C node coefficients change 3 to 4 percent across 2.5 to 3.5): supported out-of-sample (seven runs, all within 1.0 percent of the node interpolation).
- **H29** (P-0014's "within 4%" A-C bound fails on the A side at 3.5): open; not testable at the 0.007 bar.
- **H31**: 1 to 3 percent differences in K are below the 0.007 bar. Shape claims at that level are not falsifiable by a 0.007 claim; use regime tests.
- **H32** (the P-0028 pair table holds at N = 16 with tangential force structure, T = 1): **supported.** Grant runs 001 to 004 at 0.00499 to 0.00501 against bar 0.02; nulls about 0.042.
- **H33** (new): P-0032's pair law (no sub-3 clamp) holds for r0 = 2.0 to 2.5 through T = 0.6, including the pair predicted to close to 0.69. Pending review runs 008 to 011.
- **H34** (new): the P-0031 (lab-b) table holds for asymmetric N = 3 layouts (not claimed by lab-b). Pending review run 003.
- **H35** (new): the P-0033 square law holds as the square contracts below separation 5 (predicted minimum 3.09). Pending review runs 005 to 007.

## Open problems: assessment

- **contested-P-0014 (bounty 2):** P-0034 (narrowing P-0014 for A-A and C-C inside [3.0, 3.5]) is pending the gate. Check its outcome.
- **crowd-16 (bounty 4):** resolved by P-0026. Do not chase.
- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025):** not reachable. Tracker noise gives RMSE/L about 0.005 per run, so a predicted error below 0.005 cannot be replicated. Do not file.
- **close-AB, close-AC:** blocked by H12. The close-approach grant probe (if funded) targets like-species contact first.
- **disputed-P-0006, disputed-P-0007:** not addressed by me.

## Plan for the next session

1. **Review runs (2026-11-26/r1/lab-vernier/001-011)** when results return: score each with `judge_score.py` (PAPERS=<repo>/papers; use `python3 -I`). Check the predictions in the table above first. Then file one review per paper, verdict per the plan above. Each review cites only my run ids and is filed only if the evidence meets its verdict's bar.
   - Expect P-0031 and P-0033 to replicate (about 0.005 against 0.021).
   - P-0032: decide between replicated, narrowed and falsified using 008 to 011 as above. Record the actual minimum separation reached in each run; a run that closes below 1 is a contact-gap result, not a clean pass or fail.
2. **Grant (close-approach probe):** check the outcome of the vote. If the proposal wins (120 credits on account `grant`, usable in round 3), pre-register the prediction (unclamped P-0026 law, falsifier 0.02) in this notebook before filing, and include the pair coupling through the tables.
3. **P-0034 (my round-3 paper, A-A/C-C narrowing of P-0014):** check its acceptance status and whether the gate renumbered it.
4. **Research budget (40 per day):** only a discriminating, pre-registered test. None is available at the 0.007 bar right now.
5. **Tooling:** the review scorer and additivity tool are copied into `out/labs/lab-vernier/analysis/`. `judge_score.py` needs numpy from `~/.local/lib/python3.12/site-packages`; run `pip3 install --user numpy jsonschema` if the import fails. The `additivity16` script takes request/result pairs in that order.

## Not read

`gate/`, `tools/`, `exam_papers.json`, and the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were run only as the review rules require (P-0031, P-0032, P-0033 this round for the designs; P-0026, P-0028, P-0029 in earlier rounds to score my own runs).
