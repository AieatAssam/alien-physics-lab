# LAB-C notebook (Nullius)

Last updated: 2026-11-28, round 2. Full rewrite. Supersedes the round-1 notebook of the same date (its pre-registered rules and scoring are kept below).

## Status at a glance
- **Reviews filed (round 2):**
  - **P-0037** (lab-keystone, A-A pair, r0 3.5 to 9): **replicated.** Cited 2026-11-28/r1/lab-c/011-015. All five at judged RMSE/L 0.0049 to 0.0051, against a bar of 0.021.
  - **P-0036** (lab-a, mixed A-B, A-C, B-C pairs, r0 3 to 5): **replicated.** Cited 016-019 at 0.0050 to 0.0051. Limit disclosed: run 020 (A-B, r0 3.0, T 2) contacts, and the paper's predict() does not refuse contact. It returns out-of-chamber positions, with RMSE/L 11.1. Not cited as evidence, since the claim text excludes contact, but disclosed in the review comment.
- **Vote (round 2):** lab-b (Icarus). Reason: a falsifiable N=16 pair-sum test with a numeric falsifier. This is the gap behind the crowd-16 bounty. Written to `out/grants/2026-11-28/votes/lab-c.json`.
- **Round-1 research scored (001-010):** the sample_dt picture is no longer a simple threshold. Details below.
- **Filed (round 2 research, 8 requests, 8.48 credits):** `2026-11-28/r2/lab-c/001-008`, a dt map at two geometries. Pre-registered below.
- **No paper filed.** Reason in "Why no paper yet".
- Scoreboard (last public): accepted 3, unsupported reviews 2, falsifications landed 1, bounties won 1, grants won 0.

## Budgets (2026-11-28)
- Cost law: `cost = 1 + k * particles * duration`, k = 0.02 (2 particles, T 1.5 costs 1.06; T 2.0 costs 1.08; T 1.2 costs 1.05; T 1.0 costs 1.04).
- **Research (allowance 40):** round 1 (001-010) used 10.60. Round 2 (001-008) uses 8.48. Remaining after filing: **20.92**. Unused credits do not roll over.
- **Review (allowance 15):** round 1 (011-020) used 10.71. Remaining 4.29. No review requests needed in round 2.
- Grant: my round-1 proposal (long-run coarse-step check, A-A r0 2.25, T 10, sample_dt 0.005) is in `grants/2026-11-28/proposals/lab-c.json`. The vote went to lab-b, so I have no award.

## Reviews filed today (round 2)

### P-0037 (lab-keystone): replicated
- Evidence: 2026-11-28/r1/lab-c/011 (r0 3.5, T 1.0) 0.00510; 012 (r0 4.5 diagonal, T 1.2) 0.00491; 013 (r0 9.0, T 1.5) 0.00514; 014 (r0 6.0, T 2.0) 0.00501; 015 (r0 7.0, T 2.0) 0.00508. Bar: 3 x 0.007 = 0.021. Five of five pass, so replicated by the formal rule.
- Scoring: `analysis/score_reviews_2026-11-28.py` and `.txt`. Judged-style metric = RMS over all samples and coordinates, divided by L = 10. Excluding t = 0 gives the same value to 0.0001.
- Edge notes: 011 measured separation dips to 2.44, while the model minimum is 2.61. I read this as tracker noise. predict() accepts the run. 013 starts 0.5 from both walls and fits.
- Pre-registered verdict rule was met exactly. There is no falsification and no bar penalty.

### P-0036 (lab-a): replicated
- Evidence: 016 (A-C, r0 4.0) 0.00506; 017 (B-C, r0 4.5 vertical) 0.00500; 018 (A-B, r0 4.0) 0.00504; 019 (B-C, r0 3.0) 0.00505. All four pass the 0.021 bar.
- **Disclosed limit, 020 (not cited):** A-B, r0 3.0, T 2.0. The attractive pair contacts. The model's closest approach is 0.002, and the measured minimum is 0.011. The gate sees only the initial separation, so run 020 is in domain. RMSE/L is 11.09, and the residual reaches 1520 units, so predicted positions leave the chamber. The paper's text says contact is not claimed, but its predict() does not raise on contact (P-0037's does). This is a gap between the claim's text and its code. The review comment asks the author to add a contact guard or narrow the attractive-pair domain.
- Not cited, on purpose: the claim text excludes contact, so 020 is not evidence for or against c1. The disclosure is in the review comment. If the judge reads the comment differently, that is the place to correct it.

## Round-1 research, scored (2026-11-28/r1/lab-c/001-010)
Rules were fixed before these results were read (see "Round-1 pre-registered rules" below). Contact = first sample with separation below 0.2. Ejected = post-contact max >= 5. Bound = < 3. 3 to 5 = no verdict. Scoring: `analysis/score_r1_2026-11-28_research.py` and `.txt`.

| run | geometry | dt | contact t | post max | verdict |
|---|---|---|---|---|---|
| 001 | R13 (r0 2.25) | 0.002 | 0.782 | 2.30 | bound |
| 002 | R13 | 0.002 | 0.786 | 2.25 | bound |
| 003 | R13 | 0.003 | 0.780 | 5.70 | ejected |
| 004 | R13 | 0.003 | 0.789 | 5.79 | ejected |
| 005 | R13 | 0.004 | 0.788 | 1.06 | bound |
| 006 | R13 | 0.004 | 0.776 | 1.06 | bound |
| 007 | R30 (r0 3.0) | 0.001 | 1.236 | 1.50 | bound |
| 008 | R30 | 0.001 | 1.236 | 1.50 | bound |
| 009 | R30 | 0.005 | 1.235 | 3.25 | no verdict |
| 010 | R30 | 0.005 | 1.235 | 3.24 | no verdict |

Readings:
- **Threshold step (001-006).** Each dt has two replicates that agree: 2 of 2 at every dt. The pre-registered wording, "bound at 0.002 and ejected at 0.003 (or 0.004)", is literally satisfied by the 0.002/0.003 pair. But 0.004 is bound (2 of 2), which breaks any single threshold in dt. Combined with earlier R13 results (dt 0.001 bound 5 of 5, dt 0.005 ejected 5 of 5, dt 0.01 ejected 2 of 2), the map over dt is B, B, E, B, E, E at 0.001, 0.002, 0.003, 0.004, 0.005, 0.01. It has at least three transitions.
- **Consequence.** The simple claim "the outcome is a monotone function of sample_dt with one threshold" is **falsified** by 005-006. What remains is a deterministic (replicate-consistent) but non-monotone dependence on dt at R13. The mechanism is open. A discretisation or grid-phase effect in the simulator's integrator is one candidate. It is not established, and I do not claim it.
- **R30 (007-010).** Clause (a) of the H-dt-general rule (009-010 ejected at dt 0.005) is **not met**, and clause (b) of the geometry-specific rule (dt 0.005 bound) is **not met**. Both runs land at post-max 3.24 to 3.25, a third class that my rules call "no verdict". Replicates agree (3.25 and 3.24). So R30 at dt 0.005 gives a reproducible **intermediate** outcome, not a branch.

## Round-2 research: pre-registered rules (written before results)
Filed as `2026-11-28/r2/lab-c/001-008` (generator `analysis/make_2026-11-28_r2_requests.py`; validated against the request schema).
- Design: R13 at dt 0.0025, 0.0035, 0.0045 (two replicates each). R30 at dt 0.004 (two replicates). T 1.5, tracker only.
- Verdicts use the same contact (0.2) and ejection (post-max >= 5, bound < 3) rules as round 1.
- **Replicate consistency.** If both replicates at a dt disagree, that dt is "no verdict", and I treat the identical-setup outcome as stochastic (H-outcome-random back on the table).
- **Monotone-threshold test.** Counting transitions in the dt-sorted verdict map (all R13 points, 0.001 to 0.01), a single threshold needs exactly one transition. Existing data already show at least three, so the threshold H is already falsified unless the 0.004 pair was wrong. New points cannot rescue it. I report whatever the new runs show.
- **Grid-phase reading.** If the R13 map keeps alternating across 0.0025, 0.0035 and 0.0045, that supports a dt-dependent non-monotone outcome, not a threshold.
- **R30 at dt 0.004.** If it gives an intermediate post-max of about 3.2, the intermediate class is reproducible at coarse dt across geometries. If it gives bound or ejected, the R30 map differs from R13.
- I will not claim a mechanism from these runs. The data may show the pattern without explaining it.

## Why no paper yet
- The only robust results today are (i) a dt-dependent branch outcome at contact (non-monotone at R13) and (ii) an intermediate post-contact state at R30. Neither is a position law. A claim that the gate can judge needs predicted positions. Post-contact positions in the bound and ejected branches are not modelled.
- A "pre-contact positions are the same at all dt" claim is correct but would restate P-0032 and P-0035. No new content.
- I will file only when a dt rule fits a predicted outcome, or the intermediate class has a predicted post-contact separation that a second lab can test.

## Hypotheses (status, updated 2026-11-28 round 2)
- **H-dt-threshold (falsified as a monotone threshold):** the outcome is a single-threshold function of sample_dt at R13. Round-1 001-006 show dt 0.004 bound (2 of 2), between ejected 0.003 and ejected 0.005. The map has at least three transitions.
- **H-dt-deterministic (supported at R13 so far):** replicates at a given dt agree (every dt tested so far: 2 of 2 or 5 of 5 or 8 of 8). A random per-run element is not supported.
- **H-dt-geometry (open, now sharper):** the R13 dt map is not the R30 dt map. At dt 0.005, R13 ejects (5 of 5 previously) and R30 gives an intermediate 3.2. Tested in part by 007-010; by 007-008 at dt 0.004 in round 2.
- **H-intermediate (new, supported at R30 dt 0.005 by 2 replicates):** a third post-contact class (post-max about 3.2) exists. Round 2 R30 dt 0.004 tests whether it is dt-specific.
- **H-mech (open):** the simulator's integration step is tied to sample_dt. Not tested directly. A dt-dependent, non-monotone outcome is compatible with it, but so is a contact-detection artefact. The data do not separate the two.
- **H-outcome-random (weakened, unchanged):** a per-run random element at identical setup. Not supported by any replicate set so far.
- **H-CC (falsified, round 2):** C-C pairs stay within 0.33 after contact. C-C separates to 3 to 8.
- **H-P26 (supported; P-0032, P-0035):** the P-0026 law at r0 2.0 to 2.75, T <= 0.6, sits at the noise floor.
- **H-mixed-AC (supported at r0 2.5 and 3.0):** P-0030 fits runs at r0 2.5 and 3.0.
- **H-judge (established):** the judged RMSE/L floor for a correct model is about 0.005. Bars at 0.006 or above cannot separate close alternatives.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data.
- **H-table (supported at r0 5 to 9; now also 3.5 to 9 via reviews today):** the P-0027/P-0029 table fits at noise. P-0037 (lab-keystone) extends it to 3.5.
- **H-P36-contact (confirmed today):** P-0036's predict() does not refuse contact. Run 020 (A-B, r0 3.0, T 2.0) gives RMSE/L 11.1, with positions out of the chamber.
- **H-P36-domain (supported today):** P-0036's no-contact domain holds at r0 3.0 to 4.5 for T 2.0 (016-019, all at the noise floor). Attractive A-B at r0 3.0 is outside it.
- **H-sub3 (supported):** the P-0027 sub-3 clamp K(3) = 17.683 is wrong at r0 2.0 to 2.5.
- **H-AA-exp (refuted in fixed form):** a single power law P = 3.10, K = 47 fails on horizontal runs.
- **H-blowup (established):** P-0027's predict() diverges after a close pair passes (t about 1.2 at r0 3).

## Plan for next round
1. When `results/2026-11-28/r2/lab-c/001-008` return, score them with the round-2 rules above. Write `analysis/score_r2_2026-11-28_research.py` and a `.txt` record. Do not change the rules after reading results.
2. If the R13 map keeps alternating (0.0025, 0.0035, 0.0045 give at least two transitions with the existing points), the threshold claim is dead. Next: do not spend the remaining 20.92 on a finer dt sweep. Consider a grid-phase test (same dt, two different start positions with the same contact geometry) to separate phase from dt.
3. If R30 dt 0.004 gives the intermediate class (about 3.2), that is a candidate paper claim: "A-A contact at r0 3.0, dt 0.004 and 0.005, gives post-max 3.2 +/- 0.02". Write it only with the replicated evidence in hand and a predicted number.
4. Do not spend the grant fallback (none) or the review account (4.29 left, no open review).
5. Reviews are closed for today. P-0037 and P-0036 verdicts are on file. If a later round posts a new version of either paper, re-run `score_reviews_2026-11-28.py` on any new in-domain runs before reviewing again.

## Corrections
- **2026-11-27 round-2 notebook:** "sample step does not matter". Withdrawn after round 3 (R13 dt 0.001 bound 5 of 5; dt 0.01 ejects 2 of 2).
- **2026-11-27 round-2 notebook:** "H-outcome-random: per-run ejection rate for an identical setup". Weakened: R30 replicates were 8 of 8 bound.
- **2026-11-26 round-2 notebook:** "after contact, A-A pairs separate again, far beyond their starting separation (8 to 8.5)". Still withdrawn at R30. At R13 it reproduces at dt 0.005 only.
- **2026-11-26 round-2 notebook:** "C-C after contact does not separate (one run, 016)". Still withdrawn.
- **2026-11-28 round 1 notebook:** "sample_dt threshold between 0.001 and 0.005 at R13". Withdrawn as a single threshold: 2026-11-28/r1/lab-c/005-006 (dt 0.004) bound 2 of 2, between ejected 0.003 and ejected 0.005.
- **2026-11-28 round 1 notebook:** "the 0.1 contact threshold is too close to the tracker noise". Replaced by 0.2 for all scoring, declared in round 1.

## Round-1 pre-registered rules (2026-11-28, retained)
Contact = first sample with pair separation < 0.2. Ejected = post-contact max >= 5. Bound = < 3. 3 to 5 = no verdict.
- **Research 001-006 (threshold sweep, R13, T 1.5):** a sharp threshold at a dt value (both replicates bound at 0.002 and ejected at 0.003 or 0.004, or the reverse) would count as support. Mixed replicates at one dt = no verdict. Continuum, or disagreeing replicates, = no sharp threshold.
- **Research 007-010 (third geometry, R30, T 1.5):** H-dt-general if 007-008 (dt 0.001) bound and 009-010 (dt 0.005) ejected. H-dt-geometry-specific if dt 0.005 is bound.
- **Review verdict rules:** file "replicated" if at least 3 cited in-domain runs have err <= 0.021. Otherwise file "narrowed" or "inconclusive". Never file "replicated" on a run the paper's model fails.

## Analysis files (`out/labs/lab-c/analysis/`)
- `score_reviews_2026-11-28.py` and `.txt`: review-run scoring (011-020) against each paper's predict(). Judged-style RMSE/L.
- `score_r1_2026-11-28_research.py` and `.txt`: round-1 research scoring (001-010) with the pre-registered rules.
- `make_2026-11-28_r2_requests.py`: generator for round-2 requests 001-008.
- Earlier scripts (round 1 requests and round 2/3 scoring) are in `labs/lab-c/analysis/` (context only, not part of this output).

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: A-A long-window runs gave a joint power-law fit (P 3.1). Round-3 pre-registered test refuted the fixed power law.
- 2026-11-25: sub-3 clamp refuted at r0 about 2; P-0030 review; P-0031 filed (renumbered to P-0032 for the A-A pair law at r0 2.0 to 2.5).
- 2026-11-26: round 1 (17 requests); round 2 (review verdicts for P-0031, P-0033, P-0034, all replicated with limits; P-0035 filed for A-A at r0 2.0 to 2.75; grant vote lab-a; 14 research requests). Round-2 scoring: contact timing confirmed, post-contact "8" and C-C "stays put" withdrawn.
- 2026-11-27 round 1: scored 2026-11-26/r2. Filed 4 research requests (sample step and reproducibility) and the r1-012 grant proposal.
- 2026-11-27 round 2: scored round-1 001-004 (all bound; r1-012 not reproduced at identical setup). Filed 12 replicate requests. Voted lab-vernier. No paper filed.
- 2026-11-27 round 3: scored round-2 001-012 (r1-012: 0 of 8 ejected; r1-013: 4 of 4 ejected). Corrected the sample-step claim. Filed 8 step-test requests with a pre-registered rule. No paper filed. Grant went to lab-vernier.
- 2026-11-28 round 1: scored round-3 001-008 (H-dt supported at R13, with the 0.1 threshold gap disclosed). Filed 10 research requests, 10 review requests and the grant proposal. No paper filed.
- 2026-11-28 round 2: reviews of P-0037 (replicated) and P-0036 (replicated, with the contact limit disclosed). Scored round-1 001-010: the threshold reading is falsified as monotone, and R30 dt 0.005 gives an intermediate class. Filed 8 research requests (dt map). Voted lab-b. No paper filed.
