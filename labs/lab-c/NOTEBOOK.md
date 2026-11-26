# LAB-C notebook (Nullius)

Last updated: 2026-11-26, round 2. Full rewrite. Supersedes the round-1 notebook of the same date.

## Status at a glance
- Scoreboard (last public): accepted 1 (P-0013), unsupported reviews 2, falsifications landed 1, bounties 1.
- **Filed this round:** three review verdicts (P-0031 replicated, P-0033 replicated, P-0034 replicated); paper **P-0035** (A-A pair at rest, separation 2.0 to 2.75, T <= 0.6; extends P-0032); grant vote for lab-a (Plumbline); 14 research requests `2026-11-26/r2/lab-c/001-014`.
- **Next free paper number after P-0035: P-0036.** The gate may renumber. Refer to my papers by title until the final id is known: P-0032 is "A-A pair, separation 2.0 to 2.5", P-0035 is "A-A pair, separation 2.0 to 2.75".
- **Round-1 results 2026-11-26/r1/lab-c/001-017 are scored** (record: `analysis/score_r1_2026-11-26.txt`).
- **New observation (not a claim yet):** after pair contact, A-A pairs separate again and fly to separation 8 to 8.5 by t = 1.5 (runs 012, 013). C-C pairs at r0 2.5 stay within 0.33 (run 016). C-C also reaches contact later than the A-A law predicts. Round 2 replicates this before any claim.

## Budgets (2026-11-26)
- Cost law: `cost = 1 + k * particles * duration`, **k = 0.02** (confirmed again on all round-1 results).
- **Review (allowance 15):** used 13.12 in round 1. Remaining 1.88. No review runs are planned: the three verdicts used only my round-1 runs.
- **Research (allowance 40):** used 5.24 in round 1. Round 2 plans 14.75 (001-014). That leaves about 20 unspent. Unused credits are lost at day end. I did not fill them with runs I could not justify.
- **Grant:** round-1 proposal filed (the equilateral A-B-C triangle). Award, if any, is usable in round 3 on account `grant`. My round-2 vote goes to Plumbline.

## Round-1 results (2026-11-26/r1/lab-c), scored

Scorers: `analysis/score_generic.py` (judged RMSE/L against a `model.py`; L = 10), `analysis/domain_check_r1_2026-11-26.py` (initial pairwise distances), `analysis/law_ungated.py` (P-0026 law without domain checks), `analysis/rebound_r1_2026-11-26.py` (post-contact separation), `analysis/window_r1_2026-11-26.py` (windowed RMSE).

### Review runs (cited for verdicts)
| run | layout | T | pairwise (exact, initial) | judged RMSE/L vs paper | in domain? |
|---|---|---|---|---|---|
| 001 | asymmetric triangle | 2 | 7.047 / 5.891 / 5.079 | 0.00514 (P-0031) | yes |
| 002 | asymmetric triangle | 2 | 7.09 / 5.00 / 6.00 | 0.00486 (P-0031) | yes (both edges) |
| 003 | square, side 5 | 2 | 5.0, 7.071 | 0.00501 (P-0031) | yes |
| 004 | square, translated | 2 | 5.0, 7.071 | 0.00490 (P-0033) | yes |
| 005 | square, rotated 30 deg | 2 | 5.0, 7.071 | 0.00497 (P-0033) | yes |
| 006 | square, near wall | 2 | 5.0, 7.071 | 0.00506 (P-0033) | yes |
| 007 | A-A horizontal | 1 | 3.0 | 0.00491 (P-0034 c1) | yes |
| 008 | A-A diagonal | 1 | 3.5000000000000004 | refused by model | **no** (float just above 3.5) |
| 011 | A-A horizontal | 1 | 3.25 | 0.00497 (P-0034 c1) | yes |
| 009 | C-C vertical | 1 | 3.0 | 0.00489 (P-0034 c2) | yes |
| 010 | C-C horizontal | 1 | 3.5 | 0.00495 (P-0034 c2) | yes |
| 017 | C-C vertical | 1 | 3.25 | 0.00536 (P-0034 c2) | yes |

Lesson: 008 was generated with a coordinate sum that rounded to 3.5000000000000004. **When an edge matters, use exact binary fractions** (for example 3.75 and 6.25 give exactly 2.5). Round-2 generator asserts the pairwise distances.

### Research runs (not review-cited)
| run | setup | T | result |
|---|---|---|---|
| 012 | A-A r0 2.0, horizontal | 1.5 | windowed RMSE/L 0.00519 to t = 0.6, then contact at 0.66 (d_obs 0.054), then separation 8.5 by 1.5 |
| 013 | A-A r0 2.25, horizontal | 1.5 | 0.00474 to t = 0.6; contact at 0.80 (d_obs 0.043); separation 8.1 by 1.5 |
| 014 | A-A r0 2.75 (2.7499999999999996), diagonal | 0.6 | 0.00507 full window (noise floor; no contact; d = 2.12 at 0.6) |
| 015 | A-C r0 3.0, horizontal | 1.0 | **0.00475 vs P-0030's model** (in domain, noise floor). The A-A law does not apply to A-C; the P-0030 model does. |
| 016 | C-C r0 2.5, horizontal | 1.5 | contact at 1.405 (d_obs 0.024); after contact stays within 0.33 (0.29 at 1.5). First half 0.0069 vs the A-A law. |

### Contact (new): what I know, and what I do not
- **Contact timing for A-A matches the P-0026 law.** The law's own contact times (first separation < 0.1): r0 1.5: 0.421; 1.75: 0.535; 2.0: 0.659; 2.25: 0.792; 2.5: 0.932 (`analysis/prereg_contact_times_r2_2026-11-26.json`). Observed minima: 1.75 at 0.542 to 0.546 (runs 001, 005), 2.0 at 0.66 (012), 2.25 at 0.80 (013). The law is right about **when** A-A pairs meet.
- **C-C reaches contact later:** r0 2.5 at 1.405, against 0.932 for the A-A law. C-C attraction is weaker, consistent with P-0034's C nodes (K_C(3.0) = 13.20 against K_A(3.0) = 18.03).
- **After contact, A-A pairs separate again, by a lot** (separation about 8 by t 1.5 at r0 2.0 and 2.25; 2.56 by t 1.0 at r0 1.75, run 005). Energy is not conserved at contact: a pair at rest in this attractive potential cannot exceed its starting separation without energy input. Separation walls at 0 and 10 limit the late values, so the 8 to 8.5 numbers are wall-limited.
- **C-C after contact does not separate (one run, 016).** That is one run, so it is a lead, not a result.
- **Caveat:** tracker noise is about 0.05 per coordinate. Minima below about 0.1 mean "at contact", not a precise minimum distance.

## Reviews filed this round (lab-c)
Each verdict cites only in-domain lab-c runs (checked by formal domain rule: species, max_particles, and every initial pairwise distance in range).

- **P-0031 (lab-b, Icarus): replicated.** Evidence 001, 002, 003 (all three in domain, errors 0.0049 to 0.0051, bar 0.021). Limits: the paper's prose excludes asymmetric layouts, but both asymmetric triangles fit at noise, so the prose is conservative. The N = 4 domain appears to admit near-squares only.
- **P-0033 (lab-keystone): replicated.** Evidence 004, 005, 006 (square side 5; errors 0.0049 to 0.0051). Limit: one shape; the square's diagonal (7.071) sits at the top edge.
- **P-0034 (lab-vernier): replicated.** Evidence 007, 011 (A-A) and 009, 010, 017 (C-C), all in domain (errors 0.0049 to 0.0054, bar 0.021). Excluded 008 (out of domain by float). Limits: the data cannot separate P-0034 from the P-0026 law at these separations (difference 0.0003 to 0.0009 over T = 1, below noise); run 007 closes to 1.56, inside the flat-K region, and still fits. Weak content, stated as such.

## Paper filed this round: P-0035 (A-A pair, separation 2.0 to 2.75, T <= 0.6)
- Claim: P-0026 pair law without clamp, RMSE/L 0.006, domain A, [2.0, 2.75], max 2.
- Evidence (in domain, T = 0.6): 2026-11-25/r3/lab-c/002 (0.00494), 003 (0.00500), 004 (0.00508); 2026-11-26/r1/lab-c/014 (0.00507); 2026-11-25/r2/lab-c/001 (0.00509), 006 (0.00495). Scored with the model in `out/papers/P-0035/model.py`.
- Limits written in paper: no validation through contact (r0 2.0 pairs are at about 0.5 by t = 0.6), T above 0.6 not claimed, no other species or N.
- Round-2 runs 011 and 012 add in-domain evidence once they are scored.

## Round-2 requests (2026-11-26/r2/lab-c, 14 runs, research account, 14.75 credits)
| id | setup | T | dt | purpose | cost |
|---|---|---|---|---|---|
| 001 | A-A r0 2.0 vertical | 1.5 | 0.001 | contact outcome, orientation replicate of 012 | 1.06 |
| 002 | A-A r0 2.25 vertical | 1.5 | 0.001 | contact outcome, orientation replicate of 013 | 1.06 |
| 003 | C-C r0 2.0 horizontal | 1.5 | 0.001 | species test of contact outcome (vs A-A 012) | 1.06 |
| 004 | C-C r0 2.0 vertical | 1.5 | 0.001 | replicate of 003 | 1.06 |
| 005 | C-C r0 2.5 vertical | 1.5 | 0.001 | replicate of 016 | 1.06 |
| 006 | C-C r0 2.25 horizontal | 1.5 | 0.001 | C-C contact curve between 2.0 and 2.5 | 1.06 |
| 007 | A-A r0 1.75 vertical | 1.5 | 0.001 | contact outcome at shortest r0, orientation replicate | 1.06 |
| 008 | A-A r0 1.5 horizontal | 1.5 | 0.001 | deeper contact start | 1.06 |
| 009 | A-A r0 2.5 horizontal | 1.5 | 0.001 | contact outcome at P-0032 upper edge | 1.06 |
| 010 | A-A r0 1.75 horizontal | 2.0 | 0.002 | long-run post-contact motion (extends 005) | 1.08 |
| 011 | A-A r0 2.0 horizontal | 0.6 | 0.001 | evidence for P-0035 (lower edge, pre-contact) | 1.02 |
| 012 | A-A r0 2.75 vertical (exact 2.75) | 0.6 | 0.001 | evidence for P-0035 (upper edge, new orientation) | 1.02 |
| 013 | A-C r0 2.5 horizontal | 1.0 | 0.005 | tests P-0030 at its lower edge (r 2.5) | 1.04 |
| 014 | A-B r0 3.0 horizontal | 1.0 | 0.005 | A-B gap (no claim covers 2.05 to 4.0) | 1.04 |

All are generated by `analysis/make_2026-11-26_r2_requests.py` and validated against `protocol/request.schema.json`. Coordinates are exact binary fractions.

### Pre-registered predictions (written before any round-2 result is read)
- **Contact timing (A-A, 001, 002, 007, 008, 009, 010):** the P-0026 law's contact times (table above). Falsified if an observed minimum (d < 0.1) differs from the predicted time by more than 0.05 s.
- **Post-contact, A-A (001, 002, 007, 008, 010):** maximum separation after contact >= 5 by the end of the run. Falsified if any A-A run stays below 3.
- **Post-contact, C-C (003, 004, 005, 006):** maximum separation after contact <= 1.0 by the end of the run (016 pattern). Falsified if any C-C run exceeds 2.0.
- **C-C contact is later than A-A at equal r0.** Falsified if a C-C run at r0 2.0 to 2.5 reaches contact earlier than the A-A law's time at the same r0.
- **P-0035 evidence (011, 012):** judged RMSE/L <= 0.007 against `out/papers/P-0035/model.py`. Falsified above 0.018.
- **A-C at r0 2.5 (013):** judged RMSE/L <= 0.008 against the P-0030 model. Falsified above 0.021.
- **A-B at r0 3.0 (014), pre-registered with P-0034's A-A law applied to both particles:** judged RMSE/L <= 0.008. Falsified above 0.021 (then B does not act as A toward A; that is a mixed-pair result, not a claim). Note that P-0034's model refuses A-B pairs by species, so the scoring uses a copy of P-0034 with species unchecked. Scoring is planned only after the results arrive.

## Grant
- **Vote (round 2):** lab-a (Plumbline). Reason: its test of factorisation g_ij = q_i q_j over separation 9 to contact is a clean structural test (a ratio moving by more than 5% refutes it), using two particles. **Note:** its stated cost (1.40 credits) should be 1.80 at k = 0.02 (1 + 0.02 x 2 x 10); this is in the vote reason.
- My round-1 proposal (A-B-C equilateral triangle, side 5, T = 2) is in the pool. Its prediction is in the proposal. If it wins a grant, the run is for round 3.

## Hypotheses (status)
- **H-P26 (supported; P-0032 and P-0035):** the P-0026 law at r0 2.0 to 2.75, T <= 0.6, sits at the noise floor (RMSE/L 0.0049 to 0.0051). Nine in-domain runs.
- **H-contact-time (supported for A-A):** the P-0026 law gets the contact time right for A-A (1.75, 2.0, 2.25 checked). Open for C-C (see H-CC).
- **H-contact-AA (supported by 012, 013, 005; open for replicates):** A-A pairs separate again after contact, far beyond their starting separation. Round-2 runs 001, 002, 007, 008, 010 test this across r0 1.5 to 2.25 and orientation.
- **H-CC (new, one run):** C-C pairs reach contact later than the A-A law predicts, and stay within 0.33 after contact (016). Round-2 runs 003 to 006 test species dependence and r0 dependence.
- **H-mixed-AC (supported at r0 3.0):** run 015 fits P-0030's model at the noise floor (0.00475). Round-2 run 013 tests the P-0030 lower edge (r 2.5).
- **H-AB (open):** A-B pairs. Nothing claimed by me. Round-2 run 014 is a single pre-registered run at r0 3.0 (see predictions).
- **H-judge (established):** the judged RMSE/L floor for a correct model is about 0.005. Bars at 0.006 or above cannot separate close alternatives.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data. The sharpen-A/B/C bounties are out of reach for me.
- **H-sub3 (supported, unchanged):** the P-0027 sub-3 clamp K(3) = 17.683 is wrong at r0 2.0 to 2.5.
- **H-table (supported at r0 5 to 9; unchanged):** the P-0027/P-0029 table fits at noise.
- **H-AA-exp (refuted in fixed form; unchanged):** a single power law P = 3.10, K = 47 fails on horizontal runs.
- **H-blowup (established):** P-0027's predict() diverges after a close pair passes (t about 1.2 at r0 3). Judge comparisons at r0 3 with T = 1.5 are dominated by this.

## Domain feasibility (established by calculation)
- For N = 4 with every pairwise distance in [5.0, 7.08], the admissible shapes appear to be near-squares only (`analysis/design_r1_2026-11-26.py`). Use this in reviews: "the domain admits one shape" is a legitimate comment.
- Exact-edge runs: use exact binary fractions. The round-1 run 008 showed that a rounded coordinate can push a run outside the closed range.

## Analysis files (`out/labs/lab-c/analysis/`)
- `score_generic.py`, `law_ungated.py`, `design_r1_2026-11-26.py`: copied from earlier lab-c work and cited above.
- `score_r1_2026-11-26.txt`: round-1 score record (all numbers in this notebook).
- `domain_check_r1_2026-11-26.py`: formal domain check (initial pairwise distances).
- `window_r1_2026-11-26.py`: windowed RMSE vs the ungated P-0026 law.
- `rebound_r1_2026-11-26.py`: post-contact separation profile.
- `prereg_r2_2026-11-26.py` and `prereg_contact_times_r2_2026-11-26.json`: pre-registered contact times from the ungated law.
- `make_2026-11-26_r2_requests.py`: round-2 request generator (writes `out/requests/2026-11-26/r2/lab-c/001-014.json`).
- Earlier lab-c analysis (rounds 1 to 3 of earlier days) stays in `labs/lab-c/analysis/` (context only).

## Corrections to earlier notebook entries
- The round-1 notebook said "contact then rebound" and "post-contact rebound". The round-1 data show more: separation grows far beyond the starting value after A-A contact, and C-C does not do the same (one run). "Rebound" is now "separation after contact".
- The round-1 notebook said "P-0034 model not applicable to A-C (015)". True for P-0034, but P-0030's model covers A-C at r 2.5 to 3.5, and it fits 015 at noise.
- The round-1 review plan expected P-0034 to be replicated "with weak content". Filed as replicated with explicit limits (see above).
- Request 008 in round 1 was out of domain by floating-point rounding (3.5000000000000004). The review excludes it. Round 2 uses exact fractions.

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits. Grant proposals lost; lab-keystone won 2026-11-22.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: A-A long-window runs gave a joint power-law fit (P 3.1). Round-3 pre-registered test refuted the fixed power law.
- 2026-11-25: round 1 (14 requests; grant proposal A-B fall); round 2 (four review verdicts; sub-3 runs; grant vote for lab-b); round 3 (sub-3 clamp refuted at r0 about 2; P-0030 review; P-0031 filed, renumbered to P-0032 for the A-A pair law at r0 2.0 to 2.5).
- 2026-11-26 round 1: scored round-3 results 001-005 (contact timing confirmed); filed 17 requests (review 001-011, 017; research 012-016); grant proposal (A-B-C triangle, side 5, T 2).
- 2026-11-26 round 2 (this round): scored round-1 results (reviews and research); filed reviews of P-0031, P-0033, P-0034 (all replicated with stated limits); filed P-0035 (A-A pair, separation 2.0 to 2.75); grant vote lab-a; 14 research requests (contact outcome, species test, P-0035 evidence, P-0030 edge, A-B gap).
