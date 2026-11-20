# LAB-A notebook

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Budget ledger

### 2026-11-17 (closed)
- Research allowance 40, used 23.3. Review used 6.0.

### 2026-11-18 (closed)
- Research allowance 40, used 30.38. Review allowance 15, used 6.2 (review of P-0002, r1/014-016).

### 2026-11-19 (closed)
- Research allowance 40, used 13.12 (rounds 1-3). Remaining 26.88, not rolled over.
- Grant account: award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Remaining 87.00, unspent by choice (one main event per night).
- Review allowance 15, used 0.0 (no paper of mine awaiting review).
- Tonight's vote: lab-keystone. Grant award to lab-a (tie-break after a 2-2 vote).

### 2026-11-20 (this date, round 1)
- Research allowance 40. Planned: 4 requests, total 4.07 (`2026-11-20/r1/lab-a/001-004`, close-range pairs).
- Review allowance 15. Planned: 5 requests, total 5.34 (`2026-11-20/r1/lab-a/005-009`, cite P-0008).
- Grant proposal filed (`out/grants/2026-11-20/proposals/lab-a.json`): close-range C-C pair, cost 1.02 if it wins the round-2 vote and runs in round 3.

## Established

### Cost constant (H3): supported at N = 1, 2, 3, 16
- k = 0.02. Every result matches `1 + 0.02 N T`, including 2026-11-19/r3/lab-a/001 (N = 16, T = 100, cost 33.00).

### Tracker noise: about 0.05 per coordinate
- Residual rms 0.047-0.053 on every run that fits its model. The 16-particle T = 100 run has no model, but its wall excursions are consistent with the same noise (see H13 below).

### Pairwise additivity for three particles (H12): supported in the N = 3 domains tested
- A-B-C and A-A-A at separation 5, T = 1.5 (round 1). Published as P-0007 (`out/papers/P-0007/`).
- **B-C-C at separation 5, at rest, T = 2.** Pre-registered prediction (`labs/lab-a/analysis/pred_2026-11-19_r2_BCC.json`, written before the run). Two runs, both inside the pre-registered supporting band (rms <= 0.07):
  - `2026-11-19/r2/lab-a/001`: rms 0.047 (zero-force null 0.141).
  - `2026-11-19/r3/lab-a/002` (replicate): rms 0.050 (null 0.141). Checked with `out/labs/lab-a/analysis/check_r3_2026-11-20.py`.
  - Published as **P-0009** (lab-a, `out/papers/P-0009/`). Note that P-0008 is lab-b's paper, so my earlier notebook label "P-0008" is obsolete. The gate may renumber P-0009.
- Limits: equilateral start at side 5 only; N = 3; no three-body term excluded below noise over T = 2.

### Pair coefficients at separation 5, at rest, T = 2 (P-0005, replicated)
Acceleration on particle i = K_i / r^2.5 toward the partner for K > 0 (negative = repulsion). Chamber and time units.

| pair | particle | run means | runs | status |
|---|---|---|---|---|
| A-A | A | 18.0 | P-0003 (2026-11-17 r3/005-006) | established |
| A-B | A (on B) | 8.99 | 8.82 / 9.16 | replicated |
| A-B | B (on A) | 12.34 | 12.39 / 12.28 | replicated |
| A-C | A (on C) | -8.77 | -8.60 / -8.94 | replicated, repulsion |
| A-C | C (on A) | -21.25 | -21.38 / -21.12 | replicated, repulsion |
| B-B | B | 6.12 | 5.60, 6.28 (r1); 5.85, 6.75 (r2) | 4 values, spread about 9%; 2-run full-trajectory fits 6.29 (round 1 005/006) not yet pooled |
| C-C | C | 12.36 | 12.34, 12.70 (r1); 12.31, 12.08 (r2) | 4 values, spread about 5%; N = 3 check in B-C-C (P-0009) |
| B-C | B (on C) | -6.10 | -5.93 / -6.27 | pre-registered prediction passed |
| B-C | C (on B) | -10.59 | -10.65 / -10.53 | pre-registered prediction passed |

Published as P-0005. Predictor fits all 10 sep-5 runs at noise level, in-sample.

### Distance law (H7, H11): shared scale at separations 7 and 9
- A-A far field, effective K at P = 2.5: r = 4: 17.7; r = 5: 18.0; r = 6: 16.5; r = 7: 15.5; r = 8: 13.6; r = 9: 11.7.
- Power law and screened inverse square (K exp(-r/8)/r^2) still not discriminated. Open.
- H11: sep 7 and sep 9 coefficients scale with one factor (0.86 at 7, 0.65 at 9) from the A-A reference. Published as P-0006.

### Close range (H14): untested until today's requests
- No data below separation 3 for any species pair from me. P-0003 domain is 3-6 with the A-A coefficient; below 3 integrator sensitivity is high (step 0.005 needed for K = 17.67 at sep 3-4).
- Pre-registered today (see "Pre-registrations" below): A-A at 2.0 and 1.5, B-B at 2.0, C-C at 2.0 (grant proposal).

### C-C factorisation (H9): still open
- B-C passed (P-0005 c5). B-B agrees with the product rule. C-C misses by about 20% at sep 5 (12.36 measured vs 10.3 from the coupling-product rule). The C-C distance-law ratio matches A-A's, so the miss is in the coefficient or in m_C.
- The B-C-C result (P-0009) uses the measured C-C value. It supports the table as a pairwise description, not the factorisation.
- Masses m_B = 0.73, m_C = 0.40 are inferred, not measured.

### Free flight with specular walls (H1, H2, H6): supported
- A: P-0001 domain, runs to speed 7.8, T up to 100, corner hit.
- C: P-0002 (lab-b's paper, reviewed by me, verdict replicated within its domain).
- B and C at speed 1: consistent with the same reflected-line predictor.

### Isotropy at separation 4 (H10): supported
- A-A along diagonal, y, horizontal: K = 17.67, 17.71, 17.70 (0.2% agreement).

### Crowded, long run (H4, H13): no census event in 16 particles over T = 100
- `2026-11-19/r3/lab-a/001` (grant, requested as pre-registered): 16 particles, A/B/C mixed, starting on a 2.5 grid, T = 100, 2001 samples, tracker and census. **0 census events. Particle count 16 at every sample. Species labels constant.** The pre-registered prediction "no census event (H4)" holds.
- The run does not disperse. Found by `out/labs/lab-a/analysis/inspect_grant_2026-11-20.py`:
  - Tracker excursions outside [0, 10]: worst 0.156, one coordinate beyond 0.15. Consistent with the tracker noise tail, not a wall problem.
  - Closest tracker approach: 0.010 between two C particles (indices 5 and 11) at t = 65.85. Tracker noise (0.05) is larger than this, so the true separation at that time is not measured. No event.
  - 2341 pair-samples with tracker separation below 0.5, first at t ~ 1.2. The system clusters into bound groups. This is not modelled by any predictor of mine (none is valid at separation below 3).
- Consequence: H13 (no census events in a crowded long run) is supported for this run, including close encounters. Nothing is claimed about positions in this run.

### Census events (H4): no decays observed
- 0 census events in every run to date (about 40 runs). Includes the 16-particle T = 100 run above.

### P-0003 status
- Predictor reproduces its runs at noise level. Domain sep 3-6, T up to 2. Not falsified.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2-8.6. Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 16.
- H4 no decay: no event in any run to date, including the 16-particle T = 100 run.
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported across separations 3-9 as a shared-scale law. Power vs screened form not discriminated.
- H8 pair force identical for all species pairs: refuted at sep 5 (coefficients differ), and the differences persist at sep 7 and 9.
- H9 coupling factorises as g_ij = q_i q_j: partially supported. B-C passed; C-C misses by about 20% at sep 5. Not claimed.
- H10 isotropy at separation 4: supported.
- H11 shared distance law: supported within about 5% (P-0006).
- H12 pairwise additivity for three particles: supported in the N = 3 domains tested: A-B-C and A-A-A at side 5, T = 1.5 (P-0007); B-C-C at side 5, T = 2 (P-0009, two runs).
- H13 no census events in a crowded, long-duration run: supported for 16 particles at T = 100 (one run).
- H14 power law at close range (separation 1.5-2): untested. Pre-registered today.

## Pre-registrations (written before any result)
- `out/labs/lab-a/analysis/pred_2026-11-20_*.json`, from `pred_close_2026-11-20.py` (pair law a = K/r^2.5, P = 2.5, at rest, pair centred at (5,5)):
  - `AA_r2` (`2026-11-20/r1/lab-a/001`): K = 18.0, r0 = 2.0, T = 0.5. Predicted separation at T: 0.985.
  - `AA_r2_rep` (`002`): same prediction.
  - `AA_r1p5` (`003`): K = 18.0, r0 = 1.5, T = 0.3. Predicted separation at T: 0.754.
  - `BB_r2` (`004`): K = 6.12, r0 = 2.0, T = 0.5. Predicted separation at T: 1.712.
  - `CC_r2_grant` (grant proposal, round 3 main event): K = 12.36, r0 = 2.0, T = 0.5. Predicted separation at T: 1.370.
- Rule (same as earlier): residual rms per coordinate <= 0.07 supports the power-law extension to this separation; > 0.12 refutes it.

## Reviews
- **P-0008 (lab-b, "Pairwise additivity to four particles at rest, separations 3 to 5, species A, B, C (T <= 1)"):** review pending the results of `2026-11-20/r1/lab-a/005-009` (review account, `cites_paper` P-0008). Not yet written: the review must cite the review-account ids, and those results are not available this session.
  - Designed to test the domain edges: separation 3 (A-A, C-C, B-C), separation 4 (B-B, A-B), and the 4-body ceiling (N = 4 with C-C at 3, and the 4 x 3 rectangle with diagonals at 5). The claim's C-C coverage is only the 3-body P-0005 table, so the C-C pair at separation 3 is the most informative.
  - Judge rule: "replicated" needs at least three in-domain cited runs with error <= 3 x 0.07 = 0.21 normalised (RMSE <= 2.1 in chamber units). That bar is loose. My own stated bar is absolute rms <= 0.07 per coordinate against the paper model, which is the stricter reading. The review comment should say which bar was applied.

## Round 1 (2026-11-20): what I did
- Checked the grant run (`2026-11-19/r3/lab-a/001`): 0 events, 16 particles, close approaches, no dispersal. Recorded above.
- Checked the replicate of B-C-C (`2026-11-19/r3/lab-a/002`): rms 0.050 vs pre-registered prediction. Supported.
- Published P-0009 (B-C-C at side 5, T = 2; two in-domain runs; predictor reproduces both at rms 0.047 and 0.050 per coordinate, `out/papers/P-0009/model.py`).
- Filed 4 research requests (close-range pairs, 4.07 credits) and 5 review requests (P-0008 domain edges, 5.34 credits). Schema checked by hand (jsonschema not installed; pip install failed).
- Grant proposal: close-range C-C pair at separation 2.0, T = 0.5.

## Plan for the next session
1. Read the results of `2026-11-20/r1/lab-a/001-004`. Compare each with its pre-registered prediction (rule above). Replicate (001 vs 002) first. Do not publish before both agree.
2. Read `2026-11-20/r1/lab-a/005-009` (review runs of P-0008). Compute rms against the P-0008 `model.py` for each. Write the review file with those ids, citing only runs whose setup satisfies the claim's domain (species A/B/C, all pairs in [3,5], N <= the claim's max_particles).
3. If the close-range A-A pair follows the power law (rms <= 0.07 at both r = 2 and r = 1.5), write a narrow claim for the close-AA bounty: A-A pair, r_range [1.5, 2.0], T = 0.5. Do not extend to r < 1.5.
4. B-B pooled update (P-0005 c3): still pending. Keep P-0005 unchanged until pooled.
5. Research budget left after today: about 35 (40 - 4.07, review 15 - 5.34 unused on research).

## What would change my mind
- Close-range A-A rms > 0.12 at r = 2: the power law fails inside the domain 3-6 that P-0003 claims. P-0003 would need narrowing to r >= 3.
- Close-range A-A rms in the supporting band, but the two replicates disagree by more than 0.02: the run-to-run spread is larger than the tracker noise. Repeat before claiming.
- Any P-0008 review run with rms > 0.07 per coordinate at separation 3 for C-C: the C-C pair at the domain floor is not flat, and the claim's C-C coverage is overstated. I would say so in the review.
- A census event in any future crowded run: H4 refuted for the crowded case.

## Self-criticism
- The earlier notebook called my B-C-C paper "P-0008" before the number was taken by lab-b. Corrected: P-0009.
- The B-C-C replicate was filed in round 3 and checked in round 1 of the next day: the pre-registered rule passed on both runs, but the claim is still one domain (side 5). I did not claim more.
- The 16-particle run's close approaches (0.010 at t = 65.85) are at the tracker noise level: I cannot tell whether two C particles collided, passed through, or only came near. The census shows no event, which is the H4 test, but says nothing about position.
- P-0003's domain (sep 3-6) has no data below 3 from me, so claims about separation below 3 are untested.
- The B-B 2-run fit (6.29) is not on the same footing as the four per-particle run means (6.12). Not used for any claim.

## Analysis code (`out/labs/lab-a/analysis/`, my files)
- `check_r3_2026-11-20.py`: grant run (16-particle census check) and replicate of B-C-C against the pre-registered rule. Usage: `python3 -I check_r3_2026-11-20.py <repo_root>`.
- `inspect_grant_2026-11-20.py`: wall excursions and closest approach in the 16-particle run. Usage: `python3 -I inspect_grant_2026-11-20.py <repo_root>`.
- `pred_close_2026-11-20.py`: writes the close-range pre-registrations `pred_2026-11-20_*.json`. Usage: `python3 -I pred_close_2026-11-20.py <repo_root>`.
- Earlier: `check_r2_BCC.py`, `check_r1_2026-11-19.py`, `make_2026-11-19_r3_requests.py`, `make_2026-11-19_r1_requests.py` (the last two in `labs/lab-a/analysis/`).
- Papers: `out/papers/P-0009/` (paper.md, claim.json, model.py). Earlier: `out/papers/P-0007/`.
- Requests: `out/requests/2026-11-20/r1/lab-a/001-009.json` (001-004 research, 005-009 review account citing P-0008). Grant proposal: `out/grants/2026-11-20/proposals/lab-a.json`.
