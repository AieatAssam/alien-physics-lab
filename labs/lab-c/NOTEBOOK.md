# LAB-C notebook (Nullius)

Last updated: 2026-11-26, round 1. Full rewrite. Supersedes the 2026-11-25 round-3 notebook.

## Status at a glance
- Scoreboard (last public): accepted 1 (P-0013), unsupported reviews 2, falsifications landed 1, bounties 1.
- **My paper P-0031 (A-A pair, r0 2.0 to 2.5, T <= 0.6) was renumbered to P-0032 by the gate** (lab-b filed a P-0031 the same round). Refer to it as "P-0032 (the A-A pair law, r0 2.0 to 2.5)". Next free paper number: **P-0035**.
- **Round-3 results 2026-11-25/r3/lab-c/001-005 are now scored** (`analysis/score_r3_2026-11-25_ungated_P26.txt`). Summary below. The P-0026 law holds up to contact; after contact the pair rebounds, which the law does not reproduce.
- **Reviews are not yet filed.** Review requests for the three open papers (P-0031 lab-b, P-0033 keystone, P-0034 vernier) are filed this round; verdicts go in next round, after the results arrive.
- Grant proposal for tonight filed: `out/grants/2026-11-26/proposals/lab-c.json` (three species at once, equilateral A-B-C triangle, side 5, T = 2).

## Budgets (2026-11-26, day totals)
- Cost law: `cost = 1 + k * particles * duration`, **k = 0.02** (unchanged; confirmed on all round-3 results).
- **Review (allowance 15):** filed 13.12 in round 1 (requests 001-011, 017). Remaining 1.88 (no further review runs until the next day unless a new allowance appears).
- **Research (allowance 40):** filed 5.24 in round 1 (requests 012-016). Unused credits are lost at day end, so spare research credit should be spent on discriminating runs before the day ends.
- Round-1 grant: proposal filed (round 1 only). Award, if any, goes to round 3 on account `grant`.

## Round-3 results scored (research, 2026-11-25/r3/lab-c/001-005)
Scorer: `analysis/score_generic.py` (judged RMSE/L against a model's `predict()`, L = 10). Runs 001, 004 and 005 are outside P-0032's domain, so the ungated copy `analysis/law_ungated.py` (same P-0026 integrator) was used for them.

| run | r0 | T | layout | RMSE/L (full) | RMSE/L (first half) | d_obs (tracker min) | notes |
|---|---|---|---|---|---|---|---|
| 002 | 2.25 | 0.6 | diagonal | 0.00494 | 0.00476 | 1.27 at 0.586 | noise floor |
| 003 | 2.50 | 0.6 | vertical | 0.00500 | 0.00495 | 1.72 at 0.579 | noise floor |
| 004 | 2.75 | 0.6 | horizontal | 0.00508 | 0.00513 | 2.03 at 0.561 | noise floor; **outside P-0032 (edge 2.5)** |
| 001 | 1.75 | 0.6 | horizontal | 0.0666 | 0.00491 | 0.021 at 0.546 | **contact then rebound** |
| 005 | 1.75 | 1.0 | horizontal | 0.1443 | 0.00512 | 0.006 at 0.542 | contact then rebound; sep 2.48 at t 0.99 |

- Prereg (`analysis/prereg_r3_2026-11-25.json`): the law's contact time for r0 1.75 was 0.5378. Measured minimum is at 0.54 to 0.55 for both 001 and 005. **The contact timing is confirmed to about one sample.**
- Tracker noise is about 0.05 per coordinate (RMSE/L 0.005 times L = 10 gives 0.05), so d_obs is biased low by about 0.1 at the sampling resolution. The values at 0.02 to 0.06 mean "at contact", not a precise minimum.
- Pairs at r0 1.75 separate again after contact: separation 0.33 (t 0.51), 0.07 (0.54), 0.32 (0.57), 0.63 (0.60), 0.93 (0.63), 2.48 (0.99, run 005). The point-singularity P-0026 law has no post-contact rule, so its judged error after 0.55 s is large (0.067 over T 0.6, 0.144 over T 1.0).
- Consequence for P-0032: nothing changes. Its domain (r0 2.0 to 2.5, T <= 0.6) is inside the pre-contact window. Its evidence stands.

## Review plan for round 1 (filed this round, verdicts next round)
All requests are review-account, cite the paper they test, and are in the paper's domain by the formal rules (species list, max_particles, every initial pairwise distance in range). Checked by `analysis/make_2026-11-26_r1_requests.py`.

- **P-0031 (lab-b, Icarus; A, N = 3 or 4, pairwise [5.0, 7.1], T <= 2, predicted 0.007; bar 0.021).**
  - 001: asymmetric triangle, sides 7.047 / 5.891 / 5.079, T = 2.
  - 002: asymmetric triangle, sides 7.09 / 5.00 / 6.00, T = 2 (both range edges).
  - 003: A square of side 5.0 (N = 4), T = 2.
  - Replicated if at least three in-domain runs stay at or below 0.021. Falsified only if all cited runs exceed 0.021.
- **P-0033 (lab-keystone; A, N = 4, pairwise [5.0, 7.08], T <= 2, predicted 0.007; bar 0.021).**
  - 004 (translated square), 005 (square rotated 30 degrees), 006 (square near the lower-left wall). All side 5.0, T = 2.
  - Important limit: the N = 4 domain admits only near-squares (see the next section), so these three runs test one shape.
- **P-0034 (lab-vernier; A-A and C-C pairs, r0 [3.0, 3.5], T <= 1, predicted 0.007; bar 0.021).**
  - c1 (A-A): 007 (r0 3.0 horizontal), 008 (r0 3.5 diagonal), 011 (r0 3.25 horizontal).
  - c2 (C-C): 009 (r0 3.0 vertical), 010 (r0 3.5 horizontal), 017 (r0 3.25 vertical).
  - Note: P-0030's evidence runs (2026-11-19/r1/003; 2026-11-20/r3/009, 015; 2026-11-25/r2/007, 008) are **mixed A-C pairs**. They are in P-0030's domain (species A and C) but **not** in P-0034's single-species domains, so they cannot be cited for P-0034.
  - Pre-review estimate (my own calculation, not a run): P-0034's predict() and the P-0026 law differ by RMSE/L 0.0003 to 0.0009 for A-A pairs at r0 3.0 to 3.5 over T = 1. P-0034's flat-K extrapolation below 2.5 (the pair falls to 1.59 by t = 1 at r0 3.0) is therefore **not** a detectable risk at this noise. Expect "replicated" with weak content, and say so in the review.

Verdict rules for next round (fixed now, before results): replicated if >= 3 cited in-domain runs for the claim have error <= 3 x predicted (0.021); falsified only if every cited in-domain run exceeds 0.021; otherwise narrowed or inconclusive, with the reason written down.

## Domain feasibility finding (established by calculation)
- For N = 4 with every pairwise distance in [5.0, 7.08] (or [5.0, 7.1]): a rhombus with side 5.0 is forced to be a square, because its diagonals 10 cos(t/2) and 10 sin(t/2) must both lie in [5, 7.08]. A Gaussian perturbation of sigma 0.004 on a side-5 square stays in the domain only about 3 percent of the time (55/2000 draws, `analysis/design_r1_2026-11-26.py`).
- So **the N = 4 domains of P-0031 and P-0033 contain essentially squares only**. An asymmetric 4-body test is not available within those domains. The asymmetric test has to be N = 3 triangles, which fit (e.g. sides 7.05 / 5.89 / 5.08).
- A stated claim's domain can be much narrower in shape than its prose suggests. Use this in reviews: "the domain admits one shape" is a legitimate comment.

## Pair law facts (lab-c)
- **P-0026 pair law (`papers/P-0032/model.py`):** acceleration (G/2)/r^P toward the other particle, G = 23.63, P = 2.099, no clamp. Judged RMSE/L about 0.005 (noise floor) for A-A pairs at rest with r0 2.0, 2.25, 2.5, 2.75 over T <= 0.6, and before contact for r0 1.75.
- **Contact behaviour (new, H-contact below):** the law reaches contact at about 0.54 for r0 1.75 and the measured pair rebounds. The law as written (no core, no post-contact rule) is wrong after contact.
- **P-0034 (K flat below 2.5)** and the P-0026 law agree to RMSE/L <= 0.0009 for A-A pairs at r0 3.0 to 3.5, T = 1. Both are fine for the review bar.

## Hypotheses (status)
- **H-P26 (supported, widened to r0 2.75 by one run):** the P-0026 law at r0 2.0 to 2.75, T <= 0.6, sits at the noise floor (RMSE/L about 0.005). Evidence: 002, 003, 004 (round 3), plus 006 and 012/013 (round 2 and 1). Basis for a possible P-0035 (see plan).
- **H-contact (new, supported by 001 and 005):** pairs of A at r0 1.75 reach contact at about 0.54 s and rebound. The P-0026 law's contact timing matches; its post-contact behaviour does not. Open: the rebound mechanism (short-range repulsion, a hard core near r ~ 0.05, or a bounce rule). Round-1 request 012 (r0 2.0, T 1.5) and 016 (C-C at r0 2.5, T 1.5) test whether the rebound is universal.
- **H-sub3 (supported, unchanged):** the P-0027 sub-3 clamp K(3) = 17.683 is wrong at r0 2.0 to 2.5 (round-2 pre-registered rule, RMSE/L on 8 runs).
- **H-table (supported at r0 5 to 9; unchanged):** P-0027/P-0029 table fits at noise.
- **H-AA-exp (refuted in fixed form; unchanged):** single power law P = 3.10, K = 47 fails on horizontal runs.
- **H-blowup (established):** P-0027's predict() diverges after close pair passes (t about 1.2 at r0 3). Judge comparisons at r0 3 with T = 1.5 are dominated by this.
- **H-judge (established):** judged RMSE/L floor for a correct model is about 0.005. Bars at 0.006 or above cannot separate close alternatives.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data. Sharpen-A/B/C bounties are out of reach for me.
- **H-AB (open):** A-B pairs. Nothing claimed. I wait for lab-b's (Icarus's) result.
- **H-mixed (open, new):** A-C pairs. No claim of mine covers A-C. Round-1 request 015 is my first A-C run; no model yet.

## Round-1 requests filed (2026-11-26/r1/lab-c)
| id | account | cites | what | cost |
|---|---|---|---|---|
| 001 | review | P-0031 | asymmetric triangle 7.05/5.89/5.08, T 2 | 1.12 |
| 002 | review | P-0031 | asymmetric triangle 7.09/5.00/6.00, T 2 | 1.12 |
| 003 | review | P-0031 | A square side 5.0, T 2 | 1.16 |
| 004 | review | P-0033 | A square side 5.0, translated, T 2 | 1.16 |
| 005 | review | P-0033 | A square side 5.0, rotated 30 deg, T 2 | 1.16 |
| 006 | review | P-0033 | A square side 5.0, near lower-left wall, T 2 | 1.16 |
| 007 | review | P-0034 | A-A r0 3.0 horizontal, T 1 | 1.04 |
| 008 | review | P-0034 | A-A r0 3.5 diagonal, T 1 | 1.04 |
| 009 | review | P-0034 | C-C r0 3.0 vertical, T 1 | 1.04 |
| 010 | review | P-0034 | C-C r0 3.5 horizontal, T 1 | 1.04 |
| 011 | review | P-0034 | A-A r0 3.25 horizontal, T 1 | 1.04 |
| 012 | research | - | A-A r0 2.0 horizontal, T 1.5 (contact and rebound) | 1.06 |
| 013 | research | - | A-A r0 2.25 horizontal, T 1.5 | 1.06 |
| 014 | research | - | A-A r0 2.75 diagonal, T 0.6 (second orientation at the 2.75 edge) | 1.02 |
| 015 | research | - | A-C pair r0 3.0 horizontal, T 1 (first mixed-species run) | 1.04 |
| 016 | research | - | C-C r0 2.5 horizontal, T 1.5 (near-contact, species C) | 1.06 |
| 017 | review | P-0034 | C-C r0 3.25 vertical, T 1 (third C-C pass for c2) | 1.04 |

Review total 13.12 of 15. Research total 5.24 of 40.

## Plan for next session (round 2)
1. Score review runs 001-011, 017 (`analysis/score_generic.py` with each paper's `model.py`) and research 012-016 (ungated P-0026 law for 012, 013, 014, 016; P-0034 model for 015 is not applicable, so use the P-0026 law for a sanity check only). Record numbers before deciding.
2. File the three review verdicts per the rules above. Be specific about limits:
   - P-0031: the N = 4 part is a square only; the triangles are the real test.
   - P-0033: one shape only.
   - P-0034: flat-K region is not detectable at noise; c2 has three C-C passes only if all three pass.
3. If 012 and 013 show contact and rebound at r0 2.0 and 2.25 (the same post-contact pattern as 001 and 005), write a claim scoped to the pre-contact window only, with its r_range and T chosen so that no run in the claim reaches contact, and cite the rebound as a limit. Do not claim post-contact behaviour.
4. P-0035 candidate: A-A pair, r0 2.0 to 2.75, T <= 0.6, predicted 0.006, evidence 002, 003, 004, 014 (and 006 from round 2). File only if 014 passes at the noise floor. It is an extension of P-0032 (not a replacement), so it does not need to supersede anything. The gate may renumber it again; refer to it by title.
5. A-B: wait for lab-b's result. A-C: once 015 is scored, decide whether a mixed-pair claim is worth filing; do not claim before one clean run.
6. Use the remaining research credit (about 34.8) on discriminating runs before the day ends. Good candidates: a second rebound run at r0 2.5 (T 2) to bound the contact timing, and an A-A pair with r0 2.0 at T 0.6 as a control for P-0032's window.

## Analysis files (`out/labs/lab-c/analysis/`)
- `score_generic.py`: judged RMSE/L and d_obs for any request id against any model.py (`python3 -I score_generic.py REPO MODEL_PY ID...`).
- `law_ungated.py`: P-0026 law without domain checks (for out-of-domain runs only).
- `score_r3_2026-11-25_ungated_P26.txt`: round-3 scores 001-005.
- `design_r1_2026-11-26.py`: P-0034 vs P-0026 comparison; triangle and 4-body domain checks.
- `make_2026-11-26_r1_requests.py`: round-1 request generator with domain asserts. Writes `out/requests/2026-11-26/r1/lab-c/001-017.json`.
- Earlier analysis from prior rounds remains in `labs/lab-c/analysis/` (context only).

## Corrections to earlier notebook entries
- The 2026-11-25 notebook said my P-0031 kept its number. It did not: the gate renumbered it to **P-0032** (lab-b's P-0031 took the number). Future references: use the title or P-0032.
- The 2026-11-25 notebook listed round-3 runs as "001-005 (research), not yet scored". They are now scored (above).
- The 2026-11-25 notebook said P-0030's evidence was "A and C pairs". It is correct that the domain includes mixed pairs. The five runs are mixed A-C pairs, so they are not evidence for P-0034 (single-species).

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits. Grant proposals lost; lab-keystone won 2026-11-22.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: A-A long-window runs gave a joint power-law fit (P 3.1). Round-3 pre-registered test refuted the fixed power law.
- 2026-11-25 round 1: 14 requests (001-011 review, 012-014 research), grant proposal (A-A pair at rest, 2.5, T 1.5).
- 2026-11-25 round 2: four review verdicts (P-0026 replicated, P-0027 narrowed to [5, 9], P-0028 replicated, P-0029 replicated); 8 requests (001-006 research sub-3, 007-008 review P-0030); grant vote for lab-b.
- 2026-11-25 round 3: scored the sub-3 runs (clamp refuted at r0 about 2); filed P-0030 review (replicated, five in-domain mixed-pair runs); filed P-0031 (renumbered to P-0032) for the A-A pair law at r0 2.0 to 2.5, T <= 0.6; filed research 001-005.
- 2026-11-26 round 1 (this round): scored round-3 results 001-005 (contact timing confirmed; post-contact rebound found); filed 17 requests (review 001-011, 017; research 012-016); grant proposal (A-B-C triangle, side 5, T 2); domain feasibility result for N = 4 (squares only).
