# LAB-C notebook (Nullius)

Last updated: 2026-11-27, round 3. Full rewrite. Supersedes the round-2 notebook of 2026-11-27 (kept in `labs/lab-c/NOTEBOOK.md` for history).

## Status at a glance
- Scoreboard (last public): accepted 2, unsupported reviews 2, falsifications landed 1, bounties won 1.
- **Scored tonight (round 2 replicates, 2026-11-27/r2/lab-c/001-012):** record `analysis/score_r2_replicates_2026-11-27.txt`, script `analysis/score_r2_replicates_2026-11-27.py`.
  - **r1-012 geometry (dt 0.005): 0 of 8 replicates ejected** (all bound, post-contact max 1.11 to 1.28). With the round-1 anchor (2026-11-26/r1/012, ejected) and 2026-11-27/r1/002 (bound), that is 1 ejection in 10 runs at identical setup and dt. The round-1 ejection did not reproduce, so the **per-run-random claim is withdrawn in its earlier form**.
  - **r1-013 geometry (dt 0.005): 4 of 4 replicates ejected** (post-contact max 5.98 to 8.21). With the anchor 2026-11-26/r1/013 (ejected), that is **5 of 5 ejected at dt 0.005**.
- **Correction (important):** my round-2 notebook said "sample step does not matter". That was based on the r1-012 geometry only (one ejected run at dt 0.005, one bound run at dt 0.001 and one bound at dt 0.005). For the r1-013 geometry, the only dt 0.001 run (2026-11-27/r1/004) is **bound**, while all 5 dt 0.005 runs ejected. So the sample-step dependence is **not ruled out**. It is now the leading open question. Test filed tonight (below).
- **Filed tonight (round 3):** 8 research requests `2026-11-27/r3/lab-c/001-008`, planned cost 8.48.
- **No paper filed.** Reason in "Why no paper tonight" below. Next free paper number: **P-0036** (the gate may renumber).
- **No reviews due** (no papers awaiting review by me). Review allowance (15) untouched.
- **Grant:** Vernier won tonight's grant (my vote went to lab-vernier). The 120-credit award goes to lab-vernier, not to me, so I have no grant credits this round.

## Budgets (2026-11-27)
- Cost law: `cost = 1 + k * particles * duration`, k = 0.02 (every 2-particle, T 1.5 run costs 1.06). Confirmed again tonight.
- **Research (allowance 40):** round 1 used 4.24 (001-004). Round 2 used 12.72 (001-012). Round 3 plans 8.48 (001-008). Total planned 25.44. Remaining after round 3: about 14.56, which I hold for the follow-up below. Unused credits do not roll over, so I will spend only on runs the test needs.
- **Review (allowance 15):** untouched (no paper to review).

## Round-2 scoring (2026-11-27/r2/lab-c/001-012), with the round-1 anchors

Rule (pre-registered before round 2 results were read): contact = first sample with pair separation < 0.1; post-contact max >= 5 = ejected, < 3 = bound, 3 to 5 = no verdict.

| run | geometry | dt | contact t | post max | verdict |
|---|---|---|---|---|---|
| 2026-11-26/r1/012 (anchor) | r1-012 | 0.005 | 0.66 | 8.52 | ejected |
| 2026-11-27/r1/002 | r1-012 | 0.005 | 0.665 | 1.15 | bound |
| 2026-11-27/r2/001-008 | r1-012 | 0.005 | 0.655 to 0.725 | 1.11 to 1.51 | bound (8 of 8) |
| 2026-11-26/r1/013 (anchor) | r1-013 | 0.005 | 0.78 | 8.14 | ejected |
| 2026-11-27/r2/009-012 | r1-013 | 0.005 | 0.79 to 0.80 | 5.98 to 8.21 | ejected (4 of 4) |
| 2026-11-27/r1/001 | r1-012 | 0.001 | 0.662 | 2.16 | bound |
| 2026-11-27/r1/003 | r1-012, y offset 0.01 | 0.001 | 0.655 | 2.60 | bound |
| 2026-11-27/r1/004 | r1-013 | 0.001 | 0.788 | 1.85 | bound |

Summary: at dt 0.005, r1-012 ejected 1 of 10, r1-013 ejected 5 of 5. At dt 0.001, bound in 3 of 3 runs over both geometries (r1-012 twice, r1-013 once).

Notes:
- Contact timing is noisy at the threshold. 2026-11-27/r2/001 crossed at 0.725, 0.06 later than its neighbours (0.655 to 0.67). A separation threshold of 0.1 sits at the tracker noise level (about 0.05 to 0.1 per coordinate). So contact time as a threshold observable is not clean enough to support a timing paper yet.
- The pre-contact trajectories of 012 and 002 agreed to tracker noise (round 2). The post-contact split is still unexplained.

## Hypotheses (status, updated tonight)
- **H-dt (open, leading):** the post-contact outcome for an A-A pair depends on sample_dt (or on the simulator's internal step, which may be set by sample_dt). Evidence so far: r1-013 geometry is ejected at dt 0.005 (5 of 5) and bound at dt 0.001 (1 of 1). r1-012 is bound at dt 0.001 (2 of 2) and mostly bound at dt 0.005 (1 of 10 ejected). Test: round-3 requests 001-008 (below).
- **H-outcome-random (weakened):** the earlier claim that the post-contact outcome is a per-run random draw at identical setup is **not supported** in that form. The r1-012 replicates (8 of 8 bound) argue against a large random element. A residual random element is not excluded at the r1-013 geometry, since its dt 0.001 count (1 run) is too small.
- **H-contact-AA-8 (withdrawn):** "A-A pairs separate to about 8 after contact" is not reproducible at r1-012. At r1-013 it reproduces only at dt 0.005.
- **H-contact-time (weakened):** the P-0026 contact time agreed within 0.016 s in six round-2 runs (r0 1.5 to 2.5). Tonight's runs give 0.655 to 0.725 at dt 0.005, so the threshold-based contact time is noisy at the 0.06 level. Not a claim yet.
- **H-CC (falsified, round 2):** "C-C pairs stay within 0.33 after contact". C-C separates to 3 to 8.
- **H-P26 (supported; P-0032, P-0035):** the P-0026 law at r0 2.0 to 2.75, T <= 0.6, sits at the noise floor.
- **H-mixed-AC (supported at r0 2.5 and 3.0):** P-0030 fits runs at r0 2.5 and 3.0.
- **H-AB (open):** 2026-11-26/r2/014 gives 0.0108 under the A-A law. Not a claim.
- **H-judge (established):** the judged RMSE/L floor for a correct model is about 0.005. Bars at 0.006 or above cannot separate close alternatives.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data.
- **H-sub3 (supported):** the P-0027 sub-3 clamp K(3) = 17.683 is wrong at r0 2.0 to 2.5.
- **H-table (supported at r0 5 to 9):** the P-0027/P-0029 table fits at noise.
- **H-AA-exp (refuted in fixed form):** a single power law P = 3.10, K = 47 fails on horizontal runs.
- **H-blowup (established):** P-0027's predict() diverges after a close pair passes (t about 1.2 at r0 3).

## Round-3 requests (2026-11-27/r3/lab-c), research account

Generator: `analysis/make_2026-11-27_r3_requests.py`. Output: `out/requests/2026-11-27/r3/lab-c/001-008.json`. Validated by hand (jsonschema not installed): ids, species, bounds, duration/dt ratio, instruments.

| id | geometry | dt | purpose |
|---|---|---|---|
| 001-004 | r1-013 (A-A at (3.875,5) and (6.125,5), at rest) | 0.001 | dt 0.001 replicates. With 2026-11-27/r1/004 gives 5 runs at dt 0.001 |
| 005-006 | r1-013 | 0.01 | coarse sample step, checks monotonicity of the dt effect |
| 007-008 | r1-012 (A-A at (4,5) and (6,5), at rest) | 0.001 | dt 0.001 replicates. With r1/001 and r1/003 gives 4 runs at dt 0.001 |

Cost each 1.06; total 8.48. T 1.5, tracker only.

**Pre-registered rule for round 3 (written before any round-3 result is read):**
- Ejected = post-contact max >= 5. Bound = < 3. 3 to 5 = no verdict.
- **H-dt supported** if: (a) the r1-013 geometry at dt 0.001 has 0 ejections in 5 runs (004 plus 001-004), AND (b) both dt 0.01 runs (005, 006) ejected. Then the outcome is step-dependent at this geometry, and the claim goes to a paper next round.
- **H-dt falsified** if any dt 0.001 run at r1-013 ejects. Then the step effect is not clean, and the difference from dt 0.005 is a per-run or geometry effect. Withdraw H-dt.
- **r1-012 at dt 0.001:** if 007 and 008 are both bound, the 012 geometry is bound at dt 0.001 in 4 of 4 runs. If either ejects, the 012 ejection is not a step-only effect, and the simple step story is wrong for 012.
- **Mixed or no-verdict results** (any run in 3 to 5): reported, not counted.

## Why no paper tonight
- The post-contact claim needs a `model.py` that predicts tracker-observable positions. The current evidence is about an ejection outcome, not positions, and the sample-step question is still open.
- The contact-time claim (my round-2 candidate) rests on a threshold at the noise level, and tonight's 001 crossed 0.06 later than its neighbours. I will not file a timing claim whose threshold is that close to noise.
- Filing a paper before the step test returns would repeat the round-2 error of over-claiming from one geometry. I will file after round 3 results, if H-dt survives.

## Plan for next round
1. Read `results/2026-11-27/r3/lab-c/001-008`. Score with the rule above (write `analysis/score_r3_2026-11-27.py` and a txt record).
2. If H-dt is supported: file a claim (A-A pair outcome as a function of sample_dt at r1-013 geometry), with domain species [A], r_range covering the 013 separation (initial separation 2.25), max_particles 2. Predicted error set from the trajectory before contact, not from the outcome. Name the request ids as evidence.
3. If H-dt is falsified: withdraw it and report it as a falsified candidate. Spend the ~14.56 remaining research credits on a per-run replicate at r1-013 to measure the random element.
4. Review any new paper the gate assigns to me (none so far).

## Corrections
- **2026-11-27 round-2 notebook:** "sample step does not matter (001 at dt 0.001 is bound, as is 002 at dt 0.005)". Not supported. Based on the r1-012 geometry only. At r1-013, dt 0.005 ejects 5 of 5 and dt 0.001 is bound in 1 of 1 so far. Withdrawn pending round 3.
- **2026-11-27 round-2 notebook:** "H-outcome-random: per-run ejection rate for an identical setup". Weakened: r1-012 replicates were 8 of 8 bound.
- **2026-11-26 round-2 notebook:** "after contact, A-A pairs separate again, far beyond their starting separation (8 to 8.5)". Still withdrawn at r1-012. At r1-013 it reproduces at dt 0.005 only.
- **2026-11-26 round-2 notebook:** "C-C after contact does not separate (one run, 016)". Still withdrawn.

## Analysis files (`out/labs/lab-c/analysis/`)
- `score_r2_replicates_2026-11-27.py` and `score_r2_replicates_2026-11-27.txt`: tonight's scoring of round-2 001-012 with the round-1 anchors.
- `make_2026-11-27_r3_requests.py`: round-3 requests (001-008).
- Earlier scripts stay under `labs/lab-c/analysis/` (context only).

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: A-A long-window runs gave a joint power-law fit (P 3.1). Round-3 pre-registered test refuted the fixed power law.
- 2026-11-25: sub-3 clamp refuted at r0 about 2; P-0030 review; P-0031 filed (renumbered to P-0032 for the A-A pair law at r0 2.0 to 2.5).
- 2026-11-26: round 1 (17 requests); round 2 (review verdicts for P-0031, P-0033, P-0034, all replicated with limits; P-0035 filed for A-A at r0 2.0 to 2.75; grant vote lab-a; 14 research requests). Round-2 scoring: contact timing confirmed, post-contact "8" and C-C "stays put" withdrawn.
- 2026-11-27 round 1: scored 2026-11-26/r2. Filed 4 research requests (sample step and reproducibility) and the r1-012 grant proposal.
- 2026-11-27 round 2: scored round-1 001-004 (all bound; r1-012 not reproduced at identical setup). Filed 12 replicate requests (001-012, 12.72 credits). Voted lab-vernier. No paper filed.
- 2026-11-27 round 3 (this round): scored round-2 001-012 (r1-012: 0 of 8 ejected; r1-013: 4 of 4 ejected). Corrected the sample-step claim. Filed 8 step-test requests (001-008, 8.48 credits), with a pre-registered rule. No paper filed. Grant went to lab-vernier; no grant credits for me.
