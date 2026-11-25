# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-25, round 1.

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing. (Round 1: the P-0028 bar 0.021 is close to the zero-force null of the ring geometries, see round-1 notes.)
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. Say which verdict I am making and check the bar for that verdict.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions (4.5, 5.5, ...) for exact-edge domains. Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling.** The cost is `1 + k * particles * duration`, which does not depend on sample count. Always set `sample_dt = duration / 2000` (the cap).
5. **Full-window fits through a close pass are invalid.** A P = 2.5 pair law cannot follow a pair that falls to separation about 0.2 and rebounds. Use pre-contact windows for attractive pairs.
6. **Bars are loose at T <= 0.3.** The judged RMSE/L bar at close range is about 0.024. The zero-force null is only about 0.009 RMSE/L there, so those reviews can replicate but cannot falsify. The comment must say so.
7. **Label K by the window's mean separation**, not by the start separation.
8. **Judge domain does not include duration, but predictors do (round 1).** The review rules define a run's domain by species, particle count and pair distances only. Several papers' `predict()` refuse durations outside their own window (P-0024: T > 0.3 for r0 < 2.5, T > 0.6 for r0 >= 2.5; P-0028: T > 1.0). A refused run cannot be scored, so I do not cite it. I cite only runs inside both the paper's stated scope and its predictor's guard.
9. **Write only under `out/`.** My analysis scripts go in `out/labs/lab-vernier/analysis/`. (Round 1: I first wrote one into the repo's `labs/` tree by mistake and moved it.)
10. **Pre-register before results.** Predictions for each new run are written in this notebook before its results are read (see the round-1 section).

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result so far. Independent of `sample_dt`. Examples: 2 particles at T = 1 costs 1.04; 8 particles at T = 1 costs 1.16; 16 at T = 1 costs 1.32; 16 at T = 100 costs 33.

## Round 1 (2026-11-25): what I did

### Reviews filed (3, all "replicated"; review account, 2026-11-24 runs)

Each cites only runs inside the claim's domain and the paper's predictor guard. Judge-rule RMSE/L computed with my scorer `judge_score.py` (in the lab's repo analysis folder; it applies the review rules and a zero-force null).

| review | paper | evidence (my ids) | errors (RMSE/L) | bar | null (zero-force) | verdict |
|---|---|---|---|---|---|---|
| `out/reviews/P-0012/lab-vernier.json` | P-0012 (A-A r0 1.0, K 11.3, T <= 0.15) | 2026-11-24/r2/019, 020; r3/103, 104 | 0.00500 to 0.00504 | 0.024 | 0.0072 to 0.0101 | replicated |
| `out/reviews/P-0017/lab-vernier.json` | P-0017 (B-B r0 1.0, K 3.98, T <= 0.15) | 2026-11-24/r3/105, 106, 107 | 0.00496 to 0.00502 | 0.024 | 0.0061 to 0.0068 | replicated |
| `out/reviews/P-0024/lab-vernier.json` | P-0024 (A-A r0 1.25 to 3, exponent 2.10) | 2026-11-24/r2/023, 026; r3/101, 102 | 0.00496 to 0.00506 | 0.018 | 0.0102 to 0.0151 | replicated |

Limits written into the comments: none of the three can falsify at these durations (null below bar). P-0024's exponent is not tested by the bar (its own paper says so). P-0017's bar cannot separate K = 3.98 from 3.86.

Not filed: P-0028 (no in-domain run yet; see below).

### Paper P-0029 (A-C narrowing, not a supersession)

- `out/papers/P-0029/` (paper.md, claim.json, model.py). Claim c1: A and C at rest, separation 2.5 to 3.5, duration <= 2. Each particle is pushed away from the other with K(r)/r^2.5 (P = 2.5), K piecewise-linear with nodes at 2.5, 3.0, 3.5.
- Node values: K_AC (on A) = -8.820, -9.064, -9.096; K_CA (on C) = -20.831, -21.319, -21.757. The separation-5 P-0005 values are -8.77 and -21.25.
- Fitted to 2026-11-24/r3 001-010 (`out/labs/lab-vernier/analysis/fit_AC_sep_2026-11-25.py`). In-sample judge error 0.00496 to 0.00505 on all ten runs (bar for predicted error 0.008 is 0.024).
- Findings: K on A rises about 3 percent from 2.5 to 3.5; K on C rises about 4 percent. P-0014's "within 4%" bound is too tight on the A side at 3.5 (runs 006, 009, 010: 5.2, 4.1, 4.4 percent). At 3.5 with T = 1 the horizontal run (005, A ratio 1.012) and vertical run (006, 1.052) disagree; at T = 2 they agree. Not resolved.
- **Did not supersede P-0014.** P-0014 also covers A-A and C-C. The bounty "contested-P-0014" stays open until a paper covers those pairs too (see plan).

### Round-1 research requests (research account, 20.04 of 40 credits)

`out/requests/2026-11-25/r1/lab-vernier/001-019.json`:

- 001-005: A-C at rest, T = 2. r = 2.75 (H, V), r = 3.25 (H, V), r = 3.0 diagonal. Out-of-sample test of the node interpolation.
- 006-011: A-A at r = 2.5, 3.0, 3.5 (H, V each), T = 1. Groundwork for an A-C + A-A + C-C superseder.
- 012-017: C-C at r = 2.5, 3.0, 3.5 (H, V each), T = 1.
- 018-019: A-C diagonal at r = 2.5 and 3.5, T = 2 (isotropy at the edges).

**Pre-registered predictions (written before results):**

- A-C node interpolation (linear in r between the P-0029 nodes):
  - K_AC(2.75) = -8.94 (predicted), K_CA(2.75) = -21.08. Run 001 (H) and 002 (V) should each give K_AC within 1 percent of -8.94 and K_CA within 1.5 percent of -21.08.
  - K_AC(3.25) = -9.08, K_CA(3.25) = -21.54 (runs 003, 004).
  - Diagonal r = 3.0 (005): K_AC = -9.06 and K_CA = -21.32, i.e. the node values, within 1 percent.
  - Diagonal at 2.5 (018) and 3.5 (019): node values within 1.5 percent. If K differs from the H/V value by more than 2 percent, orientation matters and P-0029's claim needs a shape or isotropy caveat.
- A-A (K at P = 2.5, guess): r = 2.5 about 16.5 +/- 1.0 (the P-0024 form K = 11.815 r^0.4 gives 16.0 at r = 2.5 by my arithmetic; the round-3 pre-contact A-A values are 15.4 at 2.0 and 17.6 at 2.44). r = 3.0 about 17.6 +/- 0.3. r = 3.5 about 17.8 +/- 0.5.
- C-C: no prediction. This is the first C-C coefficient set at 2.5 to 3.5 in my data.

### P-0028 edge-of-domain review requests (review account, 3.48 of 15 credits)

`out/requests/2026-11-25/r1/lab-vernier/101-103.json` (cite P-0028; 8 A particles; every pair in [3, 9]; T = 1):

- 101: 3x3 minus centre, spacing 3.02 (min pair 3.02, max 8.54). Chosen because the zero-force null (model-vs-null 0.029) is above the bar 0.021.
- 102: same grid rotated 30 degrees (tests isotropy of the pair sum at N = 8).
- 103: ring of 8 at radius 3.95 (min 3.02, max 7.90). Model-vs-null 0.024, above the bar.

**What these runs can and cannot do.** The table-versus-constant-K difference on every in-domain geometry I tried is 0.001 to 0.003 RMSE/L, far below the bar 0.021. So these runs cannot test the K(r) table against constant K. They can only test whether the summed pair law is within the bar (replication) or misses by more than 0.021 (falsification, which the nulls allow). Expect "replicated" if the pair sum holds at N = 8; the comment must say the table shape is untested.

**Pre-registered:** model-vs-measured RMSE/L for 101-103 is at or below 0.021 (replicated). A miss above 0.021 on all three would falsify P-0028's summed-pair claim at N = 8.

### Grant (round 1)

`out/grants/2026-11-25/proposals/lab-vernier.json`: 16 A at rest on a 4x4 lattice, spacing 3.0, centred at (5,5), T = 1, dense tracker.

- Pre-registered: sum over all 120 pairs of the P-0028 table K(r)/r^2.5 predicts positions to RMSE/L <= 0.02.
- My own (non-guarded) integration, no walls, RK4 dt 0.0005: zero-force null 0.041, table-vs-constant-K 0.0026 at T = 1. At T = 0.5 the null is only 0.009 (too weak). At T = 2 my quick integrator gave unphysical escape (particles 26 apart, no walls), so I did not use it. T = 1 is the only duration I checked. Final minimum pair about 1.7 at T = 1, so close range is inside the test.
- Limit stated in the pitch: this tests additivity at N = 16, not the table shape.

## Round 3 of 2026-11-24 (carried over, analysed this round)

- Review runs 101-107 (filed under 2026-11-24/r3) were run but never filed as reviews. They are now used in the three reviews above.
- A-C runs 001-010 (r3): analysed and used in P-0029 (above).
- Note: the earlier notebook said review runs 104-114 were filed in round 2. The request folder shows only 101-103 in round 2; the P-0012, P-0017 and P-0024 review runs are actually round 3 (101-107). Corrected here.

## Round-3 results (2026-11-24, from round 2), carried forward

Pre-contact windows, P fixed 2.5, K fitted alone. Source: `analysis/fit_K_P25_precontact_2026-11-24.py`, table in `analysis/round3_precontact_table_2026-11-24.jsonl`.

| pair | r0 | runs | mean sep in window | K_eff (P = 2.5 frame) | per-run K | rmse/L |
|---|---|---|---|---|---|---|
| A-B | 1.5 | 011-014 | 1.36 | **6.70 +/- 0.13** | 6.62, 6.37, 6.86, 6.96 | 0.0048 to 0.0054 |
| A-B | 2.5 | 017-018 | 2.06 | **8.36 +/- 0.04** | 8.39, 8.33 | 0.0049 to 0.0050 |
| A-B | 3.0 | 015-016 | 2.44 | **8.74 +/- 0.02** | 8.75, 8.74 | 0.0051 |
| A-A | 2.0 | 019-020 | 1.70 | **15.40 +/- 0.15** | 15.48, 15.32 | 0.0048 to 0.0054 |
| A-A | 3.0 | 021-022 | 2.44 | **17.58 +/- 0.05** | 17.60, 17.56 | 0.0050 to 0.0052 |

- Constant K at P = 2.5 is rejected for A-B (6.70 at r about 1.4 vs 8.74 at r about 2.4).
- Local exponents near 2.1 at short range for A-B and A-A.
- P-0022's K = 7.59 "at separation 2" is a window averaging across r; the label is the issue.
- Round-3 full-window K values (A-B r0 3 = 2.03; A-A r0 3 = 11.3; "9.8" A-A r0 2) are invalid (close-pass fits). Do not use.
- Round-3 pre-registered "19.3 under P-0024" was an arithmetic error (P-0024 form gives 16.9 at mean 2.44).

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported. P-0011.
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
- **H13** (pairwise superposition, N > 2): **partially tested.** Keystone's N = 8 run and my review of P-0026 (N = 16, round 2 runs 101-103). Round-1 grant proposal (16-body lattice) and P-0028 review runs (N = 8) are the next tests.
- **H15** (P-0004-c2 magnitude): K_C(A) about -20.7 from my A-C fits at 2.5 to 3.5 and -21.25 from P-0005 at separation 5. P-0029 shows the magnitude is consistent within about 3 percent at 2.5 to 3.5.
- **H16** (P-0014 A-A contact failure): integrator blows up after close approach.
- **H17** (K_B(A)/K_A(B) = 1.41 at all separations): supported at round-3 windows; ratios 1.37 to 1.52.
- **H20** (state dependence): not supported at the 3-SE rule (round 2, n = 16).
- **H21** (orientation invariance for A-B): not falsified at 3 percent.
- **H24** (K_eff(r) for A-B at P = 2.5 is not constant): supported at the 6 SE level between r about 1.4 and 2.4.
- **H25** (A-A exponent differs from A-B exponent): not supported at present.
- **H26** (A-B force shape is not a single power law; a screened form would fit): open, no fit yet.
- **H27** (B-B K at r = 1 is 3.86 (P-0019) or 3.98 (P-0017)): **open.** Round-2 B-B runs (001, 002, 027 at T = 0.3) and round-3 105-107 (T = 0.15) are not yet fitted. P-0017's review bar (0.024) cannot decide it. A dedicated fit would.
- **H28** (new, round 1): A-C node coefficients change by about 3 to 4 percent across separation 2.5 to 3.5 (K_AC rises with r, K_CA rises with r). Supported at about 3 sigma by my rough estimate, not a formal test. Out-of-sample test: 2026-11-25/r1 001-005 (predictions above).
- **H29** (new, round 1): P-0014's "within 4%" A-C bound fails on the A side at separation 3.5 for three of my ten runs. Not yet confirmed by an independent run.
- **H30** (new, round 1): A-A and C-C at 2.5 to 3.5: no data in my lab before this round. Round-1 runs 006-017 are the test.

## Reviews: other papers (carried forward and updated)

- P-0022 (Icarus, A-B at r 2): replicated (round 2). The window's mean separation is about 1.7, not 2.0.
- P-0018 (Icarus), P-0020 (Icarus): replicated (round 3).
- P-0013 (Nullius, A-A/A-C/C-C at r 1.5): replicated (A-A part only).
- **P-0012, P-0017, P-0024 (round 1, this session): replicated (filed).**
- **P-0028 (Plumbline, A-A crowd N <= 8): not yet reviewed.** Runs 2026-11-25/r1 101-103 are filed; the review follows when they return.
- P-0026 (Keystone, N = 16): review runs were round 2 101-103 (results in); the review is not yet filed. Re-score before filing.

## Open problems: assessment

- **contested-P-0014 (bounty 2):** the A-C part is narrowed by P-0029 (not a supersession). A paper that covers A-A and C-C at 2.5 to 3.5 too would supersede P-0014 in full. Round-1 runs 006-017 are the data for that. Target: round 2 or 3 if the A-A and C-C results are consistent.
- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025):** not reachable with noise sd 0.05 at this cost (judged bar about 0.005 RMSE/L). Do not file.
- **crowd-16 (bounty 4):** a 16-particle claim. The round-1 grant proposal would give a dense N = 16 test. P-0026 (Keystone) is the existing N = 16 paper.
- **close-AB, close-AC:** blocked by H12.
- **disputed-P-0006, disputed-P-0007:** not addressed.

## Grant

- **2026-11-25 proposal:** 16-body additivity test (above). No vote tonight.
- **2026-11-24 vote:** lab-keystone (on file). Reason: their N = 8 run is the only proposal testing pairwise additivity beyond two bodies.

## Budgets (2026-11-25, after round-1 filing)

- **Research:** 40 allowed. Filed round 1: 20.04 (001-019). **Unused: 19.96** (kept for later rounds today).
- **Review:** 15 allowed. Filed round 1: 3.48 (101-103, P-0028). **Unused: 11.52.** The 2026-11-24 round-3 review runs (101-107) cost 10.39 and were already on the account.
- **Grant:** none this lab tonight (no award).

## Plan for the next session

1. When 2026-11-25/r1 results return: score 001-005 (A-C) against the pre-registered predictions above. Fit K per run (analysis `fit_AC_sep_2026-11-25.py`, with the r1 ids).
2. Score 006-017 (A-A and C-C) with the same fitter and compare to the P-0027 table (A-A, 3 to 9) and the P-0005 values (C-C at 5: 12.36). Decide whether an A-C + A-A + C-C superseder is supported.
3. Review P-0028 from 101-103: replicated if all three are within 0.021; falsified only if all three exceed it. Comment must say the table shape is untested (table-vs-constant difference 0.001 to 0.003).
4. Fit H27 (B-B K at r = 1) from 2026-11-24/r2 001, 002, 027 and r3 105-107 with a pre-contact window. Decide 3.86 vs 3.98 if the spread is below 1 percent.
5. Vote in round 2 (out/grants/2026-11-25/votes/lab-vernier.json, not my own proposal). Candidate: the 16-body test if it is the best single crowd experiment on offer.
6. Spend the remaining research credits (19.96) only on a pre-registered test, and only if a round-2 or round-3 question needs it.

## Not read

`gate/`, `tools/`, `exam_papers.json`, the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were read and run only as the review rules require.
