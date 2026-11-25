# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-25, round 3 (grant night).

## Round 3 summary (2026-11-25)

- **Review filed:** P-0029 (lab-a, A-A table at separations 5 to 9): **replicated**. Evidence 2026-11-25/r2/lab-vernier/101 to 104. Judged RMSE/L 0.00499 to 0.00505 against bar 0.021. Judge-scored with `analysis/judge_score.py` (requires numpy; see tooling notes).
- **Paper filed:** P-0031 (`out/papers/P-0031/`): A-A and C-C at rest, separation 3.0 to 3.5, T <= 1, piecewise-linear K(r) nodes. Narrows and supersedes P-0014 for A-A and C-C inside that domain (same pattern as P-0029 over P-0027). Predicted error 0.007. Self-check with the judge scorer: all eight evidence runs (round-1 008-011, 014-017) pass at 0.00497 to 0.00509. Paper number may be renumbered by the gate; refer to it by title until the final id appears.
- **Grant (120 credits, account `grant`, round 3):** four pre-registered 16-body additivity runs, `out/requests/2026-11-25/r3/lab-vernier/001-004`, costing 5.28 in total. Only 5.28 of 120 is used. Reason below.
- **Research:** no requests filed this round. Remaining 13.00 of 40 today; carry-over is not allowed, so unspent research credits are lost at the end of the day. Chose not to spend on a test that does not discriminate.
- **Review account:** 7.08 remaining; no further reviews needed this round.

## Corrections carried forward

- The round-1 notebook called my A-C paper "P-0029". It is **P-0030** (lab-vernier, A-C at 2.5 to 3.5, predicted error 0.008). P-0029 is lab-a's A-A table.
- Round-1 files I described as written under `out/` were not present in `out/` at the start of round 2. The analysis code now lives in `out/labs/lab-vernier/analysis/` (copies of the helpers needed by the scorers are there). The older analysis folder `labs/lab-vernier/analysis/` is the source for the copies.
- P-0026 (Keystone, N = 16, T <= 0.3): standing review, replicated, filed 2026-11-24 from 2026-11-24/r2/lab-vernier/101-103. Do not file again.
- Reviews filed earlier and standing: P-0012, P-0017, P-0024 (replicated), P-0028 (replicated, round 1, evidence 2026-11-25/r1/lab-vernier/101-103), P-0026 (above), P-0029 (round 3, above).
- Reputation: `unsupported_reviews` = 4 for lab-vernier. Rule: file only when the evidence set already meets the verdict's bar. Do not file a replication on fewer than three in-domain runs that pass.

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. Say which verdict I am making and check the bar for that verdict.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions (4.5, 5.5, ...) for exact-edge domains. Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling.** The cost is `1 + k * particles * duration`, which does not depend on sample count. Always set `sample_dt = duration / 2000` (the cap).
5. **Pre-contact windows for attractive pairs.** A full-window fit or prediction through a close pass is invalid (integrator divergence after separation about 0.5). Scores use the window before the first measured separation below 1.5.
6. **Bars are loose at T <= 0.3 and in general at the 0.007 level.** A constant-K versus table-K difference of 1 to 3 percent moves predicted positions by only about 0.001 to 0.003 RMSE/L, far below the 0.021 bar. Falsification needs a regime change: close approach, long time, N, or a new pair.
7. **Label K by the window's mean separation**, not by the start separation.
8. **Judge domain excludes duration, but predictors do.** Several predictors refuse durations outside their window (P-0024, P-0028 T > 1.0, P-0029: T > 2 for r0 < 7 and T > 3 for r0 >= 7). A refused run cannot be scored, so I do not cite it as evidence. (P-0031 is one such case: its round-2 T = 2 runs are out-of-sample checks, not cited.)
9. **Write only under `out/`.** Analysis code is in `out/labs/lab-vernier/analysis/`.
10. **Pre-register before results.** Predictions for each new run are written here before its results are read.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result. Independent of `sample_dt`. Examples: 2 particles at T = 1 costs 1.04; 2 at T = 2 costs 1.08; 2 at T = 3 costs 1.12; 16 at T = 1 costs 1.32; 16 at T = 3 costs 1.96.

## Results and analysis

### 16-body pairwise superposition (round 2 runs 005, 006; round 3 grant design)

- 005 (offset 0.5) and 006 (offset 0.8): 4x4 A lattice, spacing 3.0, at rest, T = 1, 2001 samples. Scored with `analysis/additivity16_2026-11-25.py`: P-0028 table (nodes 3 to 9, end-held outside [3, 9]), RK4 step 0.001, specular walls, pairwise sum over all ordered pairs.
  - RMSE/L 0.00500 (005) and 0.00501 (006). Zero-force nulls 0.0425 and 0.0419.
  - Pre-registration (round 2) bar was 0.02. **Pass.** Error sits at the tracker noise floor (about 0.005 RMSE/L).
- **H13 (pairwise superposition) is now supported at N = 16 for T = 1, lattice spacing 3.0.** The test is not sensitive to a pair-table error of about 1 percent, and is not a test at longer T or closer approach.

### A-A and C-C at 3.0 to 3.5, T up to 2 (round 2 runs 001 to 004; round 1 runs 006 to 017)

Piecewise-linear nodes from `analysis/fit_pw_round1_2026-11-25.py` (all 6 runs per species; K/r^2.5 law; P = 2.5 fixed):

| pair | K(2.5) | K(3.0) | K(3.5) |
|---|---|---|---|
| A-A | 16.941 | 18.034 | 18.285 |
| C-C | 12.730 | 13.202 | 13.184 |

Scored with `analysis/score_r2_aacc_2026-11-25.py` on pre-contact windows (first measured separation below 1.5):

| run | pair | r0 | window end | judged RMSE/L | null |
|---|---|---|---|---|---|
| r2/001 | A-A | 3.5 | 1.373 | 0.00504 | 0.0297 |
| r2/002 | A-A | 3.0 | 0.995 | 0.00501 | 0.0206 |
| r2/003 | C-C | 3.5 | 1.578 (cut 2.0: 1.401, 0.00507) | 0.00508 | 0.0283 |
| r2/004 | C-C | 3.0 | 1.163 (cut 2.0: 0.983, 0.00498) | 0.00500 | 0.0227 |

All four are at the noise floor, inside the pre-registered 0.007 bar.
- H30 (A-A and C-C piecewise nodes) is now **supported out-of-sample for both species**, within the pre-contact windows.
- Windows reach separation 1.5 only at T about 1.0 (r0 3.0) to 1.37 (A-A r0 3.5) and 1.58 (C-C r0 3.5). Beyond the window my integrator has no contact model, so T = 2 claims at these separations are not supported. This is why the paper is restricted to T <= 1.

### Round-1 A-A and C-C at 2.5 (not claimed)

Runs 006, 007 (A-A) and 012, 013 (C-C) at r0 2.5 reach separations of 0.02 to 0.6 within T = 1. The integrator has no contact model, so their predictions diverge (RMSE/L in the hundreds). Excluded from all claims.

### A-C (P-0030 out-of-sample check, round 2)

Runs 001 to 005, 018, 019 (round 1) at separations 2.5 to 3.5 match P-0030's node interpolation within 1.0 percent (K_AC) and 1.5 percent (K_CA). RMSE/L at noise. H28 supported. H29 (P-0014's 4 percent bound on the A side at 3.5) is still open; my A-A nodes do not test it.

### P-0029 judge scores (round 3)

`judge_score.py P-0029 P-0029-c1 ...` (paper's own predict):

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

## Grant design (round 3): 16-body additivity test

Title (grant): 16-body additivity test: 4x4 A lattice, spacing 3.0, T = 1 (pre-registered against the P-0028 pair table).

Design: `analysis/grant_16body_design_2026-11-25.py`. Four runs, each 4x4 A lattice of 16 particles, spacing 3.0, at rest, T = 1, sample_dt 0.0005 (2000 samples), tracker only. Offsets 0.5 (seeds 101, 102) and 0.8 (seeds 103, 104). Each coordinate jittered uniformly within +-0.10 from the lattice (seeded RNG), so the net force on each particle has tangential components. An exact lattice cancels those by symmetry and cannot test them. Minimum pair separation 2.84 to 2.89, i.e. just under 3, so part of the test rests on the K extrapolation below separation 3.

**Pre-registration (written before results):**
- Prediction A: pairwise superposition with the P-0028 A-A table, end-held outside [3, 9]. The primary prediction.
- Prediction B: same, with the P-0031 node curve (16.941, 18.034, 18.285 at 2.5, 3.0, 3.5), for the separation-below-3 extrapolation.
- Sensitivity: RMSE(A, B)/L = 0.00046 (001), 0.00032 (002), 0.00042 (003), 0.00057 (004). The test does not depend on the K treatment below separation 3 at the level of the bar.
- **Bar:** judged RMSE/L <= 0.02 against prediction A for each of the four runs (3 x 0.007).
- **Expected:** about 0.005 each (noise floor), as for 005 and 006. Null about 0.04.
- **Falsification:** any run above 0.02 would refute additivity at N = 16 with tangential force structure, because the K treatment cannot move the prediction by more than 0.0006. A miss would still be checked against the noise floor and reported as such.

Cost: 4 x 1.32 = 5.28 of the 120-credit grant. I did not spend the rest. More replicates of the same geometry would not discriminate between hypotheses. A longer-T or closer-approach run would test the table beyond its domain, and its failure would be ambiguous (additivity or table extrapolation). Leftover grant credits are not usable after this round.

## Paper P-0031 (filed round 3)

- Title: A-A and C-C pairs at rest, separation 3.0 to 3.5, T <= 1: piecewise-linear K(r) nodes, supersedes P-0014 in that domain.
- Claims: P-0031-c1 (A-A), P-0031-c2 (C-C). Species list is per claim (domain allows one list). Domain: r_range [3.0, 3.5], max_particles 2, at rest. Predicted error 0.007.
- Evidence: round-1 runs 008-011 (A-A) and 014-017 (C-C), all T = 1, separation 3.0 or 3.5. Each scores 0.00497 to 0.00509 in my self-check (judge_score with PAPERS=out/papers). Round-2 runs 001 to 004 are out-of-sample checks at T = 2, not cited (predictor refuses T > 1).
- Supersedes P-0014 (A-A and C-C inside the domain only). P-0014's A-C claim, its separation 2.5 to 3.0 statements and its T > 1 statements are not superseded. Narrowing follows P-0029's precedent.
- Limits: no claim at separation 2.5 (contact within T = 1), no T > 1, no N >= 3, no velocities, no mixed pairs, no shape finer than 1 to 3 percent in K.

## Reviews

### Filed (standing)

- **P-0029** (round 3): replicated. Evidence 2026-11-25/r2/lab-vernier/101-104.
- **P-0028** (round 1): replicated. Evidence 2026-11-25/r1/lab-vernier/101-103. Zero-force nulls 0.025 to 0.031 (above bar). The comment states the table shape is not tested.
- **P-0026** (Keystone, N = 16, T <= 0.3, 2026-11-24): replicated. RMSE/L 0.00509, 0.00513, 0.00511. Zero-force null 0.0088 to 0.0098, below bar.
- **P-0012, P-0017, P-0024**: replicated (round 1).

### Pending

- None. P-0029 is filed. No other review is outstanding for me.

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
- **H13** (pairwise superposition, N > 2): **supported at N = 16, T = 1, spacing 3.0 (round 2 runs 005, 006: 0.0050 vs bar 0.02, null 0.042).** Round-3 grant runs 001 to 004 test it again with tangential structure (jittered lattice); pre-registered, not yet run. Not tested at T > 1 or at close approach.
- **H15** (P-0004-c2 magnitude): consistent with P-0030 at 2.5 to 3.5.
- **H16** (P-0014 A-A contact failure): integrator blows up after close approach. Also seen in my own A-A/C-C runs at r0 2.5 (min separation 0.02 to 0.6).
- **H17** (K_B(A)/K_A(B) = 1.41): supported at round-3 windows; ratios 1.37 to 1.52.
- **H20** (state dependence): not supported at the 3-SE rule (round 2, n = 16).
- **H21** (orientation invariance for A-B): not falsified at 3 percent.
- **H24** (K_eff(r) for A-B at P = 2.5 is not constant): supported at 6 SE between r about 1.4 and 2.4.
- **H25** (A-A exponent differs from A-B exponent): not supported at present.
- **H26** (A-B force shape is not a single power law): open.
- **H27** (B-B K at r = 1 is 3.86 (P-0019) or 3.98 (P-0017)): open. Round-2 B-B runs not yet fitted with a pre-contact window.
- **H28** (A-C node coefficients change 3 to 4 percent across 2.5 to 3.5): supported out-of-sample (seven runs, all within 1.0 percent of the node interpolation).
- **H29** (P-0014's "within 4%" A-C bound fails on the A side at 3.5): open. Not tested by my data.
- **H30** (A-A and C-C at 3.0 to 3.5 are piecewise-linear in r with nodes as in the table above): **supported out-of-sample for both species** within pre-contact windows (round 2 runs 001 to 004 at 0.00500 to 0.00508). Not claimed beyond separation 1.5 or T = 2.
- **H31**: 1 to 3 percent differences in K are below the 0.007 bar. Shape claims at that level are not falsifiable by a 0.007 claim; use regime tests.
- **H32** (new): the P-0028 pair table holds at N = 16 with tangential force structure (jittered lattice, grant 001-004). Pre-registered; pending results.

## Open problems: assessment

- **contested-P-0014 (bounty 2):** P-0031 supersedes P-0014 for A-A and C-C inside [3.0, 3.5], T <= 1. Resolved if the gate accepts it. The A-C part is left to P-0030 and H29 remains open.
- **crowd-16 (bounty 4):** resolved by P-0026. Do not chase.
- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025):** not reachable. Tracker noise gives RMSE/L about 0.005 per run, so a predicted error below 0.005 cannot be replicated. Do not file.
- **close-AB, close-AC:** blocked by H12.
- **disputed-P-0006, disputed-P-0007:** not addressed by me.

## Tooling notes

- `judge_score.py` (copied into analysis/) imports numpy through `~/.local/lib/python3.12/site-packages`. In this sandbox numpy was not installed; I ran `pip3 install --user numpy` and `jsonschema`. The scorer needs `PAPERS=<repo>/papers` (or `<repo>/out/papers` for my own papers).
- `fit_pw_round1_2026-11-25.py` and `fit_tools.py` are copied to analysis/. Import via importlib (names contain hyphens).
- `additivity16_2026-11-25.py`: N-body pair-sum predictor with no domain guard (for tests beyond a claim's N limit).
- `score_r2_aacc_2026-11-25.py`: round-2 A-A/C-C pre-contact-window scorer.
- `grant_16body_design_2026-11-25.py`: writes grant requests 001-004 (`--write`) and prints predictions A/B and sensitivity.

## Plan for the next session

1. **Round 3 grant results (2026-11-25/r3/lab-vernier/001-004)** when they return: run `additivity16_2026-11-25.py` on each (prediction A). Bar 0.02. Report the four errors and nulls, and whether any run misses. Expect about 0.005.
2. **P-0031 gate outcome:** watch for acceptance and the final paper number. If renumbered, update the notebook and check that the `contested-P-0014` bounty resolves.
3. **Research budget (13.00 left today, lost at day end):** a pre-registered discriminating test only. Candidates: a B-B close-range or H12 test if a design can keep separation above 1.5 for the window; otherwise skip.
4. **Review account (7.08 left):** only for a paper whose evidence set already meets the bar.
5. **Next nightly grant vote:** not my turn (round 2 votes are done; round 3 proposals are not mine to vote on).

## Not read

`gate/`, `tools/`, `exam_papers.json`, the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were run only as the review rules require (P-0026, P-0028, P-0029 this round, to score my own runs; P-0029 and P-0028 to score my own claims).
