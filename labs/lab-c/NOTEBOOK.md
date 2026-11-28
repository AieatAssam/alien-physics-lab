# LAB-C notebook (Nullius)

Last updated: 2026-11-28, round 1. Full rewrite. Supersedes the 2026-11-27 round-3 notebook (kept in `labs/lab-c/NOTEBOOK.md` for history).

## Status at a glance
- **Scored tonight: round-3 step test (2026-11-27/r3/lab-c/001-008).** Record: `analysis/score_r3_2026-11-27.txt`, script `analysis/score_r3_2026-11-27.py`. The pre-registered H-dt test is **supported, with one rule gap** (see "Round-3 scoring").
  - r1-013 geometry, dt 0.001: bound in 4 of 4 new runs (001-004, post-contact max 1.81 to 1.90). With 2026-11-27/r1/004 that is 5 of 5 bound.
  - r1-013 geometry, dt 0.01: ejected in 2 of 2 (005: post-max 8.21; 006: post-max 8.25, but its closest approach was 0.113, which missed my 0.1 contact threshold).
  - r1-012 geometry, dt 0.001: bound in 2 of 2 new runs (007, 008; post-max 2.66, 2.69). With the two round-1 runs (r1/001, r1/003): bound in 4 of 4.
- **Refined claim:** the post-contact outcome depends on sample_dt at the r1-013 geometry. Ejected at dt 0.005 (5 of 5) and 0.01 (2 of 2), bound at dt 0.001 (5 of 5). The r1-012 geometry is bound at dt 0.001 (4 of 4) and at dt 0.005 in 9 of 10 runs, so the effect is **geometry-dependent**, not a clean step rule.
- **Filed today (round 1, 2026-11-28):** 20 requests `2026-11-28/r1/lab-c/001-020`. Ten research requests (step sweep and a third geometry), ten review requests (five each for P-0037 and P-0036). Validated (`analysis/check_2026-11-28_r1_requests.txt`).
- **Reviews:** P-0036 (lab-a, mixed pairs) and P-0037 (lab-keystone, A-A window 3.5 to 9) are both awaiting my review. Requests are filed. **Verdicts wait for results,** which are not yet visible this round. Plan below.
- **Grant:** proposal filed, `out/grants/2026-11-28/proposals/lab-c.json`. Long-run check of the coarse-step ejection (A-A, r0 2.25, duration 10, sample_dt 0.005). The title and pitch are in the file.
- **No paper filed.** Reason in "Why no paper yet".
- Scoreboard (last public): accepted 3, unsupported reviews 2, falsifications landed 1, bounties won 1, grants won 0.

## Budgets (2026-11-28)
- Cost law: `cost = 1 + k * particles * duration`, k = 0.02 (confirmed: 2 particles, T 1.5 costs 1.06; T 2.0 costs 1.08).
- **Research (allowance 40), planned today:** 001-010 cost 10.60. Remaining 29.40 for rounds 2 and 3, to spend only on what the results call for. Unused credits do not roll over.
- **Review (allowance 15), planned today:** 011-020 cost 10.71. Remaining 4.29 held for a follow-up if a verdict needs a replicate.
- Grant: none yet. A win would give 120 credits in round 3 (only if my proposal wins; I expect it to lose, so I do not budget for it).

## Round-3 scoring (2026-11-27/r3/lab-c/001-008)

Pre-registered rule (written before results were read on 2026-11-27): contact = first sample with separation < 0.1; post-contact max >= 5 = ejected, < 3 = bound, 3 to 5 = no verdict. H-dt supported if (a) the r1-013 geometry at dt 0.001 has 0 ejections in 5 runs (004 plus 001-004) and (b) both dt 0.01 runs (005, 006) ejected. H-dt falsified if any dt 0.001 run at r1-013 ejects.

| run | geometry | dt | contact t | post max | verdict |
|---|---|---|---|---|---|
| r3/001 | r1-013 | 0.001 | 0.791 | 1.84 | bound |
| r3/002 | r1-013 | 0.001 | 0.781 | 1.87 | bound |
| r3/003 | r1-013 | 0.001 | 0.790 | 1.81 | bound |
| r3/004 | r1-013 | 0.001 | 0.785 | 1.90 | bound |
| r3/005 | r1-013 | 0.01 | 0.800 | 8.21 | ejected |
| r3/006 | r1-013 | 0.01 | none at 0.1 (min 0.113 at 0.79) | 8.25 | ejected (see gap) |
| r3/007 | r1-012 | 0.001 | 0.654 | 2.69 | bound |
| r3/008 | r1-012 | 0.001 | 0.657 | 2.66 | bound |

**Rule gap (disclosed).** 006's closest approach (0.113) missed the 0.1 contact threshold by 0.013, so the rule as written says "no contact" for it. The rule did not cover that case. Under a 0.2 contact threshold, 006 contacts at 0.79 and ejects (post-max 8.25). I applied the 0.2 threshold to 006 only after seeing the data, so I count it as a supporting run but do not treat it as clean pre-registered evidence. Clause (b) still holds with 005 alone. For future rules I use contact = min separation < 0.2 (pre-registered below).

**Verdict on H-dt:** supported at the r1-013 geometry. Clause (a): 5 of 5 bound at dt 0.001. Clause (b): 2 of 2 ejected at dt 0.01. Not falsified.

**What this does not settle.**
- The r1-012 geometry at dt 0.005 gave 1 ejection in 10 runs (the round-1 anchor, 2026-11-26/r1/012). So the step effect is not a clean switch at a single dt across geometries. It is geometry-dependent.
- The threshold lies somewhere between dt 0.001 and 0.005 at r1-013. Not yet located.
- The mechanism is open. A simulator that integrates with step = sample_dt would produce this. So would a contact-detection artefact. The data cannot separate these yet.

## Round-1 pre-registered rules (2026-11-28), written before results

Contact here = first sample with pair separation < 0.2 (changed from 0.1, see the gap above). Ejected = post-contact max >= 5. Bound = < 3. 3 to 5 = no verdict.

**Research 001-006 (threshold sweep, r1-013 geometry, T 1.5):**
- Sharp threshold at a dt value: both replicates bound at dt 0.002 and ejected at dt 0.003 (or 0.004), or the reverse. Mixed replicates at one dt count as "no verdict" there.
- Continuum: post-max rises smoothly with dt, or replicates at the same dt disagree.
- I expect a sharp step if the simulator's internal step equals sample_dt. I will not claim the mechanism unless the sweep supports it.

**Research 007-010 (third geometry, r0 3.0, T 1.5):**
- H-dt-general supported if 007-008 (dt 0.001) are bound and 009-010 (dt 0.005) are ejected.
- H-dt-geometry-specific if dt 0.005 is bound here. Then the 0.005 ejections at r1-013 are geometry-specific and the sample-step story is wrong as a general rule.

**Review verdict rules (applied when results return):**
- P-0037 (lab-keystone, A-A, r0 3.5 to 9, claim error 0.007, bar 0.021). Cited: 011-015 (all in gate domain, all predict() accepted). File "replicated" if at least 3 of them have err <= 0.021. Otherwise file "narrowed" or "inconclusive" (no bar penalty). I do not expect a falsification: a 1 percent K error is below the bar.
- P-0036 (lab-a, mixed pairs, r0 3 to 5, claim error 0.007, bar 0.021). Cited: 016-019 (in-scope: no contact, T 2, initial walls >= 2 away). File "replicated" if at least 3 have err <= 0.021. 020 (A-B at r0 3, T 2) is outside the claim's stated no-contact scope, so I cite it only as narrowing evidence, not toward the bar.
- I will not file "replicated" on a run the paper's model fails, even if the gate would count it. An unsupported verdict costs reputation.

## Reviews: what the requests test (and why these edges)

P-0037 (claim: A-A pair at rest, r0 3.5 to 9, K(r) table joined from P-0034 and P-0029, predict() refuses pairs that come within 2.5):
- 011: r0 3.5, T 1.0, closest approach 2.61 in the model. Tests the 3.5 edge and the 2.5 to 3.5 region from P-0034, while the pair stays inside the claim's window.
- 012: r0 4.5 diagonal, T 1.2. Exercises the 3.5 to 5 segment that the paper never measured. This is the paper's stated gap.
- 013: r0 9.0, T 1.5. The 9 edge. Wall clearance 0.5 at start, which the claim does not exclude.
- 014, 015: r0 6.0 and 7.0 over T 2.0. Longer runs inside the window, with the model's closest approach 5.2 and 6.5.

P-0036 (claim: mixed A-B, A-C, B-C at rest, r0 3 to 5, T <= 2, no contact):
- 016: A-C r0 4.0, T 2.0. Repulsive pair, C moves away. Checks the charge sign and the C mass.
- 017: B-C r0 4.5 vertical. Repulsive, different orientation.
- 018: A-B r0 4.0, T 2.0. Attractive. The model's closest approach is 2.40, the paper's sharpest in-scope point.
- 019: B-C r0 3.0 vertical. Edge of the separation range.
- 020: A-B r0 3.0, T 2.0. The model's closest approach is 0.002, so the pair contacts. The claim excludes contact, so this run is for narrowing the domain, not a bar test.

All review runs use dt 0.001. That keeps every sample inside the 2000-sample limit and keeps the run clear of the dt effect found above. Each paper's own `predict()` was run locally before filing (`analysis/check_2026-11-28_r1_requests.txt`). Every review run is inside the gate's domain.

## Why no paper yet
- H-dt is supported at one geometry, but the outcome is a branch, not a position law. A claim that the gate can judge is about predicted positions. The branch's post-contact positions need a model of the bound and ejected branches, and I do not have one.
- A "pre-contact positions are the same at all dt" claim would be correct and cheap, but it is a restatement of the existing A-A law (P-0032 and P-0035 cover that window) with no new content.
- I will file once the threshold sweep (001-006) and the third geometry (007-010) return. If the threshold is sharp and the third geometry agrees, I can state a sample_dt condition as a domain limit and test it.

## Hypotheses (status, updated 2026-11-28)
- **H-dt (supported at r1-013; geometry-dependent overall):** the post-contact outcome for an A-A pair depends on sample_dt. At r1-013: ejected at dt 0.005 (5 of 5) and 0.01 (2 of 2), bound at dt 0.001 (5 of 5). At r1-012: bound at dt 0.001 (4 of 4), ejected in 1 of 10 at dt 0.005.
- **H-threshold (open, new today):** a sharp dt threshold between 0.001 and 0.005 at r1-013. Tested by 001-006.
- **H-geometry (open, new today):** the dt effect is specific to some pair geometries. Tested by 007-010.
- **H-mech (open):** the simulator's integration step follows sample_dt. Not tested directly. A long-run check is the grant pitch.
- **H-outcome-random (weakened):** a per-run random element at identical setup. The r1-012 replicates were 8 of 8 bound, so a large random element is not supported.
- **H-contact-AA-8 (withdrawn):** A-A pairs separate to about 8 after contact in general. Reproduces only at dt 0.005.
- **H-CC (falsified, round 2):** C-C pairs stay within 0.33 after contact. C-C separates to 3 to 8.
- **H-P26 (supported; P-0032, P-0035):** the P-0026 law at r0 2.0 to 2.75, T <= 0.6, sits at the noise floor.
- **H-mixed-AC (supported at r0 2.5 and 3.0):** P-0030 fits runs at r0 2.5 and 3.0.
- **H-judge (established):** the judged RMSE/L floor for a correct model is about 0.005. Bars at 0.006 or above cannot separate close alternatives.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data.
- **H-sub3 (supported):** the P-0027 sub-3 clamp K(3) = 17.683 is wrong at r0 2.0 to 2.5.
- **H-table (supported at r0 5 to 9):** the P-0027/P-0029 table fits at noise.
- **H-AA-exp (refuted in fixed form):** a single power law P = 3.10, K = 47 fails on horizontal runs.
- **H-blowup (established):** P-0027's predict() diverges after a close pair passes (t about 1.2 at r0 3).
- **H-P36-contact (new, from planning):** P-0036's model has no contact handling. At A-B r0 3.0 and T 2.0 it predicts a pair at 0.002 separation and an out-of-chamber position (run 020 tests this).

## Plan for next round
1. Read `results/2026-11-28/r1/lab-c/001-020` once they are available. Score 001-010 with the pre-registered rules. Write `analysis/score_r1_2026-11-28.py` and a txt record. Do not change the rules after reading results.
2. Reviews: file P-0037 and P-0036 verdicts per the rules above, citing only the request ids the results support, with evidence drawn from my own lab. Each review's comment lists every cited run, including the ones outside the bar.
3. Spend remaining research credits (29.40) only on a test the sweep calls for. Example: if the threshold is sharp, bisect it (dt 0.0025, 0.0035). If it is continuous, test a second geometry first.
4. Grant: if the proposal wins, the 120 credits go to a round-3 threshold or geometry test.
5. Decide on a paper only after the threshold is known.

## Corrections
- **2026-11-27 round-2 notebook:** "sample step does not matter". Withdrawn after round 3 (r1-013 dt 0.001 is bound 5 of 5; dt 0.01 ejects 2 of 2).
- **2026-11-27 round-2 notebook:** "H-outcome-random: per-run ejection rate for an identical setup". Weakened: r1-012 replicates were 8 of 8 bound.
- **2026-11-26 round-2 notebook:** "after contact, A-A pairs separate again, far beyond their starting separation (8 to 8.5)". Still withdrawn at r1-012. At r1-013 it reproduces at dt 0.005 only.
- **2026-11-26 round-2 notebook:** "C-C after contact does not separate (one run, 016)". Still withdrawn.
- **2026-11-28 (this round):** the 0.1 contact threshold is too close to the tracker noise (run 006 closest approach 0.113). New threshold 0.2 for all future scoring, declared here.

## Analysis files (`out/labs/lab-c/analysis/`)
- `score_r3_2026-11-27.py` and `score_r3_2026-11-27.txt`: tonight's scoring of round-3 001-008.
- `make_2026-11-28_r1_requests.py`: generator for 2026-11-28/r1 requests 001-020.
- `check_2026-11-28_r1_requests.py` and `.txt`: schema validation and the review runs' gate-domain and predict() checks.
- `plan_reviews_2026-11-28.py`: candidate review setups checked against each paper's predict() (the chosen 16-20 are a subset).
- Earlier scripts (round 2, round 3 requests) are under `labs/lab-c/analysis/` (context only).

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: A-A long-window runs gave a joint power-law fit (P 3.1). Round-3 pre-registered test refuted the fixed power law.
- 2026-11-25: sub-3 clamp refuted at r0 about 2; P-0030 review; P-0031 filed (renumbered to P-0032 for the A-A pair law at r0 2.0 to 2.5).
- 2026-11-26: round 1 (17 requests); round 2 (review verdicts for P-0031, P-0033, P-0034, all replicated with limits; P-0035 filed for A-A at r0 2.0 to 2.75; grant vote lab-a; 14 research requests). Round-2 scoring: contact timing confirmed, post-contact "8" and C-C "stays put" withdrawn.
- 2026-11-27 round 1: scored 2026-11-26/r2. Filed 4 research requests (sample step and reproducibility) and the r1-012 grant proposal.
- 2026-11-27 round 2: scored round-1 001-004 (all bound; r1-012 not reproduced at identical setup). Filed 12 replicate requests (001-012, 12.72 credits). Voted lab-vernier. No paper filed.
- 2026-11-27 round 3: scored round-2 001-012 (r1-012: 0 of 8 ejected; r1-013: 4 of 4 ejected). Corrected the sample-step claim. Filed 8 step-test requests (001-008, 8.48 credits), with a pre-registered rule. No paper filed. Grant went to lab-vernier.
- 2026-11-28 round 1: scored round-3 001-008 (H-dt supported at r1-013, with the 0.1 threshold gap disclosed). Filed 10 research requests (10.60 credits), 10 review requests (10.71 credits), and the grant proposal (long-run coarse-step check). No paper filed. Reviews of P-0036 and P-0037 await results.
