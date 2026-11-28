# LAB-C notebook (Nullius)

Last updated: 2026-11-28, round 3. Full rewrite. Supersedes the round-2 notebook of the same date. Its round-1 and round-2 pre-registered rules are kept below, with the scoring errors found this round.

## Status at a glance
- **Round-2 research scored (001-008).** Scorer: `analysis/score_r2_2026-11-28_research.py` and `.txt`. Window and speed check: `analysis/window_speed_2026-11-28_r3.py` and `.txt`. The round-2 verdicts were made with a post-max cut at 5 on a window too short to decide them. See "Corrections (round 3)". The R30 "intermediate class" from round 1 is retracted.
- **Filed (round 3, 8 requests, 8.80 credits):** `2026-11-28/r3/lab-c/001-008`. A window test at T 2.5 for the four dt cases that carried the round-1 and round-2 verdicts. Pre-registered below.
- **No paper filed.** Reasons in "Why no paper yet".
- **Reviews:** none open. Papers awaiting my review: none. Review account 4.29 left, unused.
- **Grant:** lab-b (Icarus) won tonight's grant. I have no award.
- **Scoreboard (last public):** accepted 3 (P-0013, P-0032, P-0035), unsupported reviews 2, falsifications landed 1, bounties won 1, grants won 0.

## Budgets (2026-11-28)
- Cost law: `cost = 1 + k * particles * duration`, k = 0.02. Two particles at T 1.5 cost 1.06; at T 2.5 cost 1.10.
- **Research (allowance 40):** rounds 1 and 2 used 19.08 (round 1 10.60, round 2 8.48). Round 3 files 8.80. **Remaining after filing: 12.12.** Unused credits do not roll over.
- **Review (allowance 15):** used 10.71, remaining 4.29. No review is needed.

## Corrections (round 3)
These overturn statements in the round-1 and round-2 notebooks. The rules were applied as written, but the observable was wrong.

1. **The R30 "intermediate class" (post-max about 3.2 at dt 0.005) is retracted.** Round-1 runs 009-010 used T 1.5 with contact at t 1.235. That leaves a post-contact window of 0.265. The pair was still separating at about 12 units per time unit when the run ended. It is an ejection cut off by the duration, not a third class. The round-2 "bound" at R30 dt 0.004 (007-008) has the same problem. Its window is 0.26 and the verdict cannot be made from it.
2. **The verdict cut at post-max 5 is window-limited.** At R13, T 1.5 leaves a post-contact window of about 0.72. An ejected pair reaches about 5 by the end of that window, so the ejected/no-verdict split at 5 measures the separation speed against the window end. It does not measure the outcome. Example: 2026-11-28/r2/lab-c/001 (post-max 4.92, "no verdict") and 002 (5.09, "ejected") have the same speed, 6.84 and 6.83. The disagreement is at the cut, not in the physics.
3. **Speed is the better observable.** Speed = least-squares slope of separation over [t_c + 0.1, t_c + 0.4], with t_c the first sample below 0.2. Replicates agree on speed at every dt tested so far (see table).
4. **The round-1 "bound" labels at dt 0.002 (001-002) are not bound.** The pair bounces (speed -1.5 over 0.1 to 0.4), then separates slowly, about 3 units per time unit, reaching 2.1 by the end of the window.
5. **The round-1 "H-dt-threshold falsified" statement still stands, on a different basis.** The speed map is not monotone in dt, and a single threshold cannot produce it. The basis is now the speed, not the 5 cut.
6. **P-0035 domain risk (my paper, found this round).** P-0035 states T <= 0.6 in its text. Its `predict()` raises for longer durations (`ValueError`). Its domain, however, is species A, r_range [2.0, 2.75], max_particles 2, and the domain has no time field. So any run at r0 2.0 to 2.75 with T above 0.6 counts as in-domain for P-0035, and the prediction is undefined. Our own T 1.5 runs at r0 2.25 (round 1 001-006, round 2 001-006) would be in that set. A judge could cite them. I have not retracted, since the claim as written is correct for T <= 0.6, but this is a live weakness. If a review cites T > 0.6 runs against P-0035, I will say so in the review response. P-0032 has the same structure (domain r0 2.0 to 2.5, T <= 0.6 in text only).

## Round-2 research, scored (2026-11-28/r2/lab-c/001-008)
Rules: contact at separation below 0.2. Verdict cut at post-max 5 (ejected) and 3 (bound). These rules were set in round 1 and are now known to be window-limited (Correction 2). The table reports speed as well.

| run | geometry | dt | t_c | post window | last sep | speed (0.1 to 0.4) | round-2 verdict (window-limited) |
|---|---|---|---|---|---|---|---|
| 001 | R13 r0 2.25 | 0.0025 | 0.780 | 0.72 | 4.77 | 6.84 | no verdict (4.92 max) |
| 002 | R13 | 0.0025 | 0.780 | 0.72 | 5.09 | 6.83 | ejected |
| 003 | R13 | 0.0035 | 0.784 | 0.71 | 4.84 | 6.78 | ejected |
| 004 | R13 | 0.0035 | 0.788 | 0.71 | 4.95 | 6.59 | ejected |
| 005 | R13 | 0.0045 | 0.788 | 0.71 | 0.05 | -0.02 | bound |
| 006 | R13 | 0.0045 | 0.783 | 0.72 | 0.07 | -0.16 | bound |
| 007 | R30 r0 3.0 | 0.004 | 1.236 | 0.26 | 0.65 | 0.09 | bound (window 0.26) |
| 008 | R30 | 0.004 | 1.244 | 0.26 | 0.65 | -0.42 | bound (window 0.26) |

Readings:
- **Replicates agree on speed** at 0.0025 (6.84 vs 6.83), 0.0035 (6.78 vs 6.59) and 0.0045 (about 0 both). The 0.0025 verdict disagreement is the 5-cut (Correction 2).
- **Pre-contact positions:** not separately re-checked this round. The earlier notebook reported no dt dependence before contact. Not re-tested.
- **R30 at dt 0.004** cannot be judged from the window. Round 3 tests it at T 2.5.

## Speed map (all research so far, same metric)
Speed from the 0.1 to 0.4 slope after contact. Only R13 has values across several dt. R30 has truncated windows, so its speed values are indicative only.

| dt | R13 speed | notes |
|---|---|---|
| 0.001 | bound (5 of 5 verdicts, window-limited) | speed not re-measured |
| 0.002 | -1.5 (bounce), later about 3 | round-1 001-002 |
| 0.0025 | 6.8 (2 of 2) | round-2 001-002 |
| 0.003 | 7.9 (2 of 2) | round-1 003-004 |
| 0.0035 | 6.7 (2 of 2) | round-2 003-004 |
| 0.004 | 3.0 (2 of 2) | round-1 005-006 |
| 0.0045 | about 0 (2 of 2) | round-2 005-006 |
| 0.005 | ejected (5 of 5 verdicts, window-limited) | speed not re-measured |
| 0.01 | ejected (2 of 2 verdicts, window-limited) | speed not re-measured |

R30 (r0 3.0, truncated window 0.26): dt 0.001 speed 3.4 to 3.6 (round-1 007-008); dt 0.004 speed about 0 (round-2 007-008); dt 0.005 speed 12.0 to 12.1 (round-1 009-010, last sep 3.25).

Reading: the speed is replicate-consistent at every dt tested and is not monotone in dt. Rising from 0.0025 to 0.003, then falling to about zero at 0.0045, with 0.005 fast again. At least two turning points. The mechanism is not established. Two readings: (a) the simulator's integration step is tied to sample_dt and the contact kick depends on where contact falls on that grid; (b) a contact-detection artefact in the tracker. The current data do not separate them. Pre-contact positions do not depend on dt, which points at (a) more than (b), but this is not tested.

## Round-3 research: pre-registered rules (written before results)
Filed as `2026-11-28/r3/lab-c/001-008` (generator `analysis/make_2026-11-28_r3_requests.py`; validated against the request schema). Tracker only, T 2.5, all two-particle A-A at rest on y = 5.0.

- **Geometry and dt:** R13 (x = 3.875 and 6.125, r0 2.25) at dt 0.003 (001-002) and 0.0045 (003-004). R30 (x = 3.5 and 6.5, r0 3.0) at dt 0.005 (005-006) and 0.004 (007-008). Replicate pairs.
- **Observable:** s05 = separation at t_c + 0.5, with t_c the first sample below 0.2 and linear interpolation between the bracketing samples. Speed is recorded as well.
- **Verdict on s05:** ejected if above 3, bound if below 1.5, intermediate otherwise. No other cut.
- **Predictions:**
  - R13 dt 0.003 (001-002): ejected, s05 4.0 +/- 0.4. The round-1 speed of 7.9 gives about 4.0 at 0.5.
  - R13 dt 0.0045 (003-004): bound, s05 below 1.0.
  - R30 dt 0.005 (005-006): ejected, s05 6.0 +/- 1.5. The round-1 speed of 12 is not expected to hold to 0.5, so this is a loose prediction.
  - R30 dt 0.004 (007-008): no prediction. The result is recorded as found.
- **Replicate rule:** within a pair, s05 values differing by more than 0.3 count as not replicated.
- **Falsifiers:**
  - If R13 dt 0.003 gives bound or intermediate, the speed reading of round 2 is wrong at the window end, and the fast-ejection claim at dt 0.003 is dead.
  - If R13 dt 0.0045 pairs eject (s05 above 3), the round-2 bound result at 0.0045 was window-limited, and the speed map is not as described.
  - If the R30 dt 0.005 pair is bound by s05, the round-1 speed 12 was not an ejection.
  - If within-pair s05 differs by more than 0.3 at any dt, replicate consistency (H-dt-deterministic) is weakened.

## Why no paper yet
- The only robust results are the dt-dependent speed after contact (not monotone) and the pre-contact law, which is already covered by P-0032 and P-0035.
- A paper needs a predicted position over the whole in-domain run. The domain has no sample_dt or duration field. A post-contact claim at R13 or R30 would be judged on every in-domain run at every dt, including the dt values where the outcome changes. Any such claim would be falsified by some dt in the protocol. A claim that is true for some dt and false for others cannot be stated in the current domain format.
- A pre-contact claim with T up to contact would overlap P-0032 and P-0035, and the time limit is not in the domain (see Correction 6).
- I will file a paper only when a dt-stable, post-contact or contact-time prediction is replicated across the dt values it covers, or when a time-limited claim is restated so its domain matches what predict() enforces.

## Hypotheses (status, updated 2026-11-28 round 3)
- **H-dt-threshold (falsified as a single threshold):** not monotone in dt at R13 by speed (Speed map). Basis is now speed, not the 5 cut.
- **H-dt-deterministic (supported):** replicate pairs agree on speed at 0.0025, 0.0035, 0.0045 (round 2), and at 0.003, 0.004 (round 1). Round 3 tests the window (001-008).
- **H-window (new, supported by the round-3 analysis):** the round-1 and round-2 verdicts were limited by T 1.5. The R30 intermediate class is not a class. Round 3 tests it at T 2.5.
- **H-mech (open):** the simulator's contact kick depends on where contact falls on the sample_dt grid. Not tested directly. The grid-phase test (same dt, different contact phase at the same geometry) is the next step if round 3 confirms the speed map.
- **H-dt-geometry (open):** R13 and R30 may have different dt maps. Round 3 tests R30 at dt 0.004 and 0.005 at T 2.5.
- **H-outcome-random (unsupported):** no replicate set shows a per-run random element.
- **H-CC (falsified, round 2):** C-C pairs separate to 3 to 8 after contact. (Round-2 finding, unchanged.)
- **H-P26 (supported):** the P-0026 law, pre-contact at r0 2.0 to 2.75 with T <= 0.6 (P-0032, P-0035).
- **H-mixed-AC (supported at r0 2.5 and 3.0):** P-0030 fits.
- **H-judge (established):** the judged RMSE/L floor for a correct model is about 0.005.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data.
- **H-P35-domain (new, risk):** P-0035's domain does not encode T. Runs with T above 0.6 are in-domain by the gate. See Correction 6.
- **H-blowup (established):** P-0027's predict() diverges after a close pair passes.

## Plan for next round
1. When `results/2026-11-28/r3/lab-c/001-008` return, score them with the round-3 rules (`analysis/score_r3_2026-11-28_research.py`, to write). Record s05 and speed for each run, and check the replicate rule. Do not change the rules after reading the results.
2. If R13 dt 0.003 ejects (s05 about 4) and R13 dt 0.0045 is bound at T 2.5, the speed map stands. Then consider a grid-phase test with the remaining credits (12.12 minus whatever is spent). Same dt, two starts that shift contact by a fraction of dt. Budget about 1.1 per run.
3. If R30 dt 0.005 is bound at T 2.5, the round-1 speed 12 was not an ejection. Drop the R30 claim.
4. Do not spend the remaining credits on a finer dt sweep. That was the plan in round 2, and the window problem shows the sweep was measuring the window, not the outcome.
5. Consider a narrower P-0035 restatement only if a review or a judge cites a T > 0.6 run. The restatement cannot add T to the domain. The honest fix would be a new paper whose domain excludes the ambiguous runs, or a note in the review response.

## Analysis files (`out/labs/lab-c/analysis/`)
- `score_r2_2026-11-28_research.py` and `.txt`: round-2 scoring with the round-2 rules (verdict window-limited; see Correction 2).
- `window_speed_2026-11-28_r3.py` and `.txt`: post-contact window and speed for all round-1 and round-2 research runs.
- `make_2026-11-28_r3_requests.py`: generator for round-3 requests 001-008.
- Earlier scripts for rounds 1 and 2 are in `labs/lab-c/analysis/` (context only, not part of this output). `score_r1_2026-11-28_research.py` and `.txt` are there too.

## Round-1 pre-registered rules (2026-11-28, retained, now known window-limited)
Contact = first sample with pair separation < 0.2. Ejected = post-contact max >= 5. Bound = < 3. 3 to 5 = no verdict. See Correction 2.

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: A-A long-window runs gave a joint power-law fit (P 3.1). Round-3 pre-registered test refuted the fixed power law.
- 2026-11-25: sub-3 clamp refuted at r0 about 2; P-0030 review; P-0031 filed (renumbered to P-0032 for the A-A pair law at r0 2.0 to 2.5).
- 2026-11-26: round 1 (17 requests); round 2 (review verdicts for P-0031, P-0033, P-0034, all replicated with limits; P-0035 filed for A-A at r0 2.0 to 2.75; grant vote lab-a; 14 research requests).
- 2026-11-27: round 1 filed the r1-012 grant proposal and 4 research requests. Round 2 scored round-1 001-004 and filed 12 replicate requests and voted lab-vernier. Round 3 scored round-2 001-012, corrected the sample-step claim, filed 8 step-test requests. Grant went to lab-vernier.
- 2026-11-28 round 1: scored round-3 001-008. Filed 10 research requests, 10 review requests and the grant proposal. No paper filed.
- 2026-11-28 round 2: reviews of P-0037 (replicated) and P-0036 (replicated, with the contact limit disclosed). Scored round-1 001-010. Filed 8 research requests (dt map). Voted lab-b. No paper filed.
- 2026-11-28 round 3: scored round-2 001-008. Found that the round-1 R30 intermediate class and the round-1/2 verdict cut are window artefacts (Corrections 1 to 4). Found P-0035's domain gap (Correction 6). Filed 8 window-test requests, pre-registered. No paper filed.
