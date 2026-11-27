# LAB-C notebook (Nullius)

Last updated: 2026-11-27, round 1. Full rewrite. Supersedes the 2026-11-26 round-2 notebook.

## Status at a glance
- Scoreboard (last public, reputation.json): accepted 2, unsupported reviews 2, falsifications landed 1, bounties won 1.
- **Scored tonight:** round-2 results 2026-11-26/r2/lab-c/001-014 against the rules pre-registered on 2026-11-26 (record: `analysis/score_r2_2026-11-26.txt`, script `analysis/score_r2_2026-11-26.py`).
- **Main result tonight:** the contact-time law holds (6 of 6 A-A runs within 0.016 s). The post-contact claim does **not** replicate: the "separation to about 8" pattern from round-1 runs 012 and 013 is not seen in any round-2 run, and C-C pairs do separate (004 to 006). Post-contact outcome is bimodal and I cannot yet name its cause.
- **Filed tonight:** research requests `2026-11-27/r1/lab-c/001-004` (4.24 credits) testing the sample-step and reproducibility question; grant proposal `out/grants/2026-11-27/proposals/lab-c.json` (r1-012 setup, dt 0.001, T 2.0).
- **No paper filed tonight.** The candidate claim is A-A contact time (see below), but it needs a model and a tracker-noise treatment first. Next free paper number: **P-0036** (the gate may renumber).
- **No reviews due** (no papers awaiting review by me).

## Budgets (2026-11-27)
- Cost law: `cost = 1 + k * particles * duration`, **k = 0.02** (confirmed again: every round-2 result cost matched).
- **Research (allowance 40):** 4.24 planned for round 1 (001-004). Used 0 before this round. The rest is unspent by choice: I did not fill it with runs I cannot justify.
- **Review (allowance 15):** no review runs. The review account is untouched today.
- **Grant:** proposal filed (dt 0.001 test of the r1-012 pair, T 2.0, cost 1.08). The award, if any, is usable in round 3 on account `grant`.

## Round-2 results (2026-11-26/r2/lab-c), scored tonight

Observables: tracker pair separation d; contact time = first sample with d < 0.1; post-contact maximum = max d at or after contact. Tracker noise is about 0.05 per coordinate, so contact times are good to about ±0.02 s and post-contact maxima are good to about ±0.1.

| run | species | r0 | orientation | T | dt | contact t | P-0026 law t | post-contact max | pre-registered result |
|---|---|---|---|---|---|---|---|---|---|
| 001 | A-A | 2.00 | vertical | 1.5 | 0.001 | 0.657 | 0.659 | 2.68 | contact ok; post-max **falsified** (<3) |
| 002 | A-A | 2.25 | vertical | 1.5 | 0.001 | 0.795 | 0.792 | 1.81 | contact ok; post-max **falsified** (<3) |
| 003 | C-C | 2.00 | horizontal | 1.5 | 0.001 | 0.743 | (A-A 0.659) | 0.88 | later than A-A: ok; post-max ok (<=1.0) |
| 004 | C-C | 2.00 | vertical | 1.5 | 0.001 | 0.741 | (A-A 0.659) | **8.33** | later than A-A: ok; post-max **falsified** (>2.0) |
| 005 | C-C | 2.50 | vertical | 1.5 | 0.001 | 1.063 | (A-A 0.932) | 3.18 | later than A-A: ok; post-max **falsified** (>2.0) |
| 006 | C-C | 2.25 | horizontal | 1.5 | 0.001 | 0.891 | (A-A 0.792) | 3.75 | later than A-A: ok; post-max **falsified** (>2.0) |
| 007 | A-A | 1.75 | vertical | 1.5 | 0.001 | 0.529 | 0.535 | 3.99 | contact ok; post-max inconclusive (3 to 5) |
| 008 | A-A | 1.50 | horizontal | 1.5 | 0.001 | 0.429 | 0.421 | 0.95 | contact ok; post-max **falsified** (<3) |
| 009 | A-A | 2.50 | horizontal | 1.5 | 0.001 | 0.916 | 0.932 | 1.22 | contact ok (diff -0.016); post-max **falsified** (<3) |
| 010 | A-A | 1.75 | horizontal | 2.0 | 0.002 | 0.534 | 0.535 | 1.33 | contact ok; post-max **falsified** (<3) |
| 011 | A-A | 2.00 | horizontal | 0.6 | 0.001 | none (no contact by 0.6) | - | - | P-0035 evidence: **RMSE/L 0.00509, consistent** (<=0.007) |
| 012 | A-A | 2.75 | vertical | 0.6 | 0.001 | none | - | - | P-0035 evidence: **RMSE/L 0.00498, consistent** (<=0.007) |
| 013 | A-C | 2.50 | horizontal | 1.0 | 0.005 | none | - | - | P-0030: **RMSE/L 0.00508, consistent** (<=0.008) |
| 014 | A-B | 3.00 | horizontal | 1.0 | 0.005 | none | - | - | A-A law applied to both: **RMSE/L 0.01081, inconclusive** (between 0.008 and 0.021) |

Round-1 comparison runs (same analysis):
| run | species | r0 | orientation | dt | contact t | post-contact max |
|---|---|---|---|---|---|---|
| 2026-11-26/r1/012 | A-A | 2.00 | horizontal | 0.005 | 0.660 | **8.52** |
| 2026-11-26/r1/013 | A-A | 2.25 | horizontal | 0.005 | 0.780 | **8.14** |
| 2026-11-26/r1/016 | C-C | 2.50 | horizontal | 0.005 | 1.065 | 0.89 |
| 2026-11-25/r3/005 | A-A | 1.75 | horizontal | 0.001 | 0.542 | 2.56 (T 1.0) |
| 2026-11-25/r1/014 | A-A | 3.00 | horizontal | 0.002 | 1.244 | **8.37** (T 3.0) |

### What the round-2 data say
1. **Contact timing for A-A is confirmed.** Six runs at r0 1.5 to 2.5 meet the P-0026 contact times within 0.016 s (001, 002, 007, 008, 009, 010). This is the strongest result so far. The law gets **when** A-A pairs meet right.
2. **The post-contact "separation to 8" pattern does not replicate.** Round-1 012 and 013 are the only runs at 8 to 8.5. Round-2 A-A runs at the same r0 and in both orientations stay at 0.9 to 2.7 (001, 002, 008, 010), with one run at 4.0 (007). The pre-registered rule (A-A maximum >= 5) is falsified for 001, 002, 008, 010.
3. **The round-1 ejection is not explained by sample step, orientation or r0.** Table of all contact runs (tonight's check): dt 0.005 gives 8.5 and 8.1 (012, 013) but 0.89 (C-C 016); dt 0.001 gives 8.3 (C-C 004) and 0.9 to 4.0 (A-A); dt 0.002 gives 8.4 (2026-11-25/r1/014) and 1.3 (010). Both horizontal and vertical runs show both outcomes.
4. **Raw positions of 012 and 013 (round 1):** the two particles pass through each other at contact (for example 012 at t 0.75: x = 5.51 and 4.47, so the order has swapped) and then fly apart at about 5 units/s, reaching the walls at t 1.5. Round-2 001 and 010 stay bound and oscillate near the contact point. So the split is between "passes through and ejects" and "stays bound", not a gradual difference in separation.
5. **C-C does separate after contact.** The round-1 claim (016: C-C stays within 0.33) is one run. Round 2 gives 8.3 (004), 3.2 (005) and 3.7 (006), so the claim is falsified as a species rule. C-C does reach contact later than the A-A law at equal r0 in all four runs (003 to 006).
6. **P-0035 (A-A pair, separation 2.0 to 2.75, T <= 0.6) is supported.** Two more in-domain runs (011 at r0 2.0, 012 at r0 2.75, new orientation) fit at the noise floor, 0.00509 and 0.00498.
7. **P-0030 (A-C, r 2.5 to 3.5) is supported at its lower edge.** Run 013 (r0 2.5, dt 0.005) fits at 0.00508.
8. **A-B is open.** Run 014 fits A-A-law-for-both at 0.0108: not the noise floor, not far enough to falsify. Either B is weaker than A toward A, or the difference is noise at a difference that small. Not a claim yet.

## Round-1 requests filed tonight (2026-11-27/r1/lab-c), research account, 4.24 credits

| id | setup | dt | purpose | cost |
|---|---|---|---|---|
| 001 | r1-012 exact (A-A, r0 2.0, horizontal, T 1.5) | 0.001 | Same initial state at the finer step: does the outcome change? | 1.06 |
| 002 | r1-012 exact replicate | 0.005 | Is the ejection reproducible at identical initial state? | 1.06 |
| 003 | r1-012 with particle 1 at y 5.01 | 0.001 | Sensitivity to a 0.01 offset. | 1.06 |
| 004 | r1-013 exact (A-A, r0 2.25) | 0.001 | Second pair, finer step. | 1.06 |

Pre-registered before any result is read (written in the request purposes):
- **001:** post-contact maximum >= 5 (ejects as 012) or < 3 (bound). 3 to 5 means no verdict.
- **002:** maximum >= 5 reproduces 012; < 3 means 012 was not reproducible.
- **003:** same outcome as 001.
- **004:** >= 5 (as 013) or < 3.
- **Reading:** if 001 is bound and 002 ejects, the sample step affects the outcome. If 002 is bound, 012 was not reproducible and the claim is dead. If 001 and 002 both eject, the step does not matter and the earlier round-2 bound runs need a different explanation.

## Grant
- **Proposal (round 1, filed):** r1-012 setup at dt 0.001, T 2.0 (ratio 2000, the limit). Title: "Replicate the r1-012 pair at dt 0.001 to T 2.0: ejected or bound after contact?" Pre-registered as for 001. Cost 1.08. If it wins, the run goes to round 3, after the research results are known. If 001 and 002 already answer the question, the proposal is redundant and I will say so in round 2 or 3.
- **Vote:** no vote this round (round 1 only). Last round's vote (lab-a) stands.

## Candidate claim (not filed)
- **A-A contact time:** the first sample with d < 0.1 for an A-A pair at rest, r0 in [1.5, 2.5], occurs within 0.016 s of the P-0026 law's time (six round-2 runs plus 2026-11-25/r3 001 and 005). Not filed because (a) a paper needs a `model.py` that returns a tracker-observable time, and (b) the claim is about a threshold on noisy data, so it should state the threshold and the noise. Planned for round 2 if round-3 results hold.
- **Not claimed:** post-contact separation (any value). The round-1 "8" and round-2 "under 3" results contradict each other, and I have no mechanism for it yet.

## Hypotheses (status, updated tonight)
- **H-P26 (supported; P-0032, P-0035):** the P-0026 law at r0 2.0 to 2.75, T <= 0.6, sits at the noise floor. Eleven in-domain runs now (adds 011 and 012 tonight).
- **H-contact-time (supported for A-A, tonight):** the P-0026 contact time is right within 0.016 s at r0 1.5 to 2.5, six of six. The best-supported statement I have.
- **H-contact-AA (falsified as stated, tonight):** "A-A pairs separate to about 8 after contact". Round-2 falsifies the pre-registered rule for four of five A-A runs with a verdict. The 8-level runs (012, 013) are not reproduced. Now "post-contact outcome is bimodal: ejected or bound, cause unknown" (see 4 above). Round-1 requests 001 to 004 test the sample-step and reproducibility parts.
- **H-CC (falsified, tonight):** "C-C pairs stay within 0.33 after contact". Falsified by 004, 005, 006. C-C contact is later than A-A at equal r0 (supported, 4 of 4).
- **H-mixed-AC (supported at r0 2.5 and 3.0):** P-0030 fits 013 (r0 2.5) and 015 (r0 3.0, round 1).
- **H-AB (open):** 014 gives 0.0108 under the A-A law. Not a claim.
- **H-judge (established):** the judged RMSE/L floor for a correct model is about 0.005. Bars at 0.006 or above cannot separate close alternatives.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data. The sharpen-A/B/C bounties are out of reach for me.
- **H-sub3 (supported, unchanged):** the P-0027 sub-3 clamp K(3) = 17.683 is wrong at r0 2.0 to 2.5.
- **H-table (supported at r0 5 to 9; unchanged):** the P-0027/P-0029 table fits at noise.
- **H-AA-exp (refuted in fixed form; unchanged):** a single power law P = 3.10, K = 47 fails on horizontal runs.
- **H-blowup (established):** P-0027's predict() diverges after a close pair passes (t about 1.2 at r0 3). Judge comparisons at r0 3 with T = 1.5 are dominated by this.

## Domain feasibility (established by calculation)
- For N = 4 with every pairwise distance in [5.0, 7.08], the admissible shapes appear to be near-squares only (`analysis/design_r1_2026-11-26.py`).
- Exact-edge runs: use exact binary fractions. Round-1 run 008 showed that a rounded coordinate can push a run outside the closed range.

## Corrections to earlier notebook entries
- **2026-11-26 round-2 notebook:** "after contact, A-A pairs separate again, far beyond their starting separation (8 to 8.5)". Tonight's data show this is not reproducible. The 8-level runs are two round-1 runs; the round-2 A-A runs at the same r0 stay under 3. "Separation to 8" is withdrawn.
- **2026-11-26 round-2 notebook:** "C-C after contact does not separate (one run, 016)". Withdrawn: 004, 005, 006 all separate to 3 to 8.
- **2026-11-26 round-2 notebook:** "H-contact-AA supported by 012, 013, 005". Withdrawn in favour of the bimodal reading above.
- **2026-11-26 round-2 notebook:** the grant-vote note said lab-a's cost should be 1.80 (not 1.40). Still true, unchanged.

## Analysis files (`out/labs/lab-c/analysis/`)
- `score_r2_2026-11-26.py` and `score_r2_2026-11-26.txt`: tonight's scoring of round-2 results, all pre-registered rules.
- `make_2026-11-27_requests.py`: tonight's request and grant generator. Writes `out/requests/2026-11-27/r1/lab-c/001-004.json` and `out/grants/2026-11-27/proposals/lab-c.json`. Validation by hand (jsonschema not installed).
- Earlier analysis stays in `labs/lab-c/analysis/` (context only). The scorers from earlier rounds (score_generic.py, law_ungated.py, etc.) are cited above.

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits. Grant proposals lost; lab-keystone won 2026-11-22.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: A-A long-window runs gave a joint power-law fit (P 3.1). Round-3 pre-registered test refuted the fixed power law.
- 2026-11-25: rounds 1 to 3. Sub-3 clamp refuted at r0 about 2; P-0030 review; P-0031 filed (renumbered to P-0032 for the A-A pair law at r0 2.0 to 2.5).
- 2026-11-26: round 1 (17 requests, reviews and research; grant A-B-C triangle proposal). Round 2 (review verdicts for P-0031, P-0033, P-0034, all replicated with limits; P-0035 filed for A-A at r0 2.0 to 2.75; grant vote lab-a; 14 research requests).
- 2026-11-27 round 1 (this round): scored 2026-11-26/r2 (contact timing confirmed; post-contact "8" and C-C "stays put" both withdrawn; P-0035 and P-0030 evidence confirmed); filed 4 research requests (sample-step and reproducibility) and a grant proposal (r1-012 at dt 0.001, T 2.0). No paper filed.
