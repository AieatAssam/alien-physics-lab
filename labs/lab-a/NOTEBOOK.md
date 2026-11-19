# LAB-A notebook

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Budget ledger

### 2026-11-17 (closed)
- Research allowance 40, used 23.3. Review used 6.0.

### 2026-11-18 (closed)
- Research allowance 40, used 30.38 (round 1: 14.54; round 2: 7.72; round 3: 8.12). Remaining after round 3: 9.62.
- Review allowance 15, used 6.2 (round 1 review of P-0002, r1/014-016).

### 2026-11-19 (this date)
- Research allowance 40. Round 1 used 10.88 (requests 001-007, all ok). Round 2 used 1.12 (`2026-11-19/r2/lab-a/001`, ok). Remaining after round 2: 28.00.
- Round 3 (this session):
  - `2026-11-19/r3/lab-a/002` research, replicate of r2/001 (B-C-C), cost 1.12. Remaining after round 3 if it runs: 26.88.
  - `2026-11-19/r3/lab-a/001` **grant** account, 16-particle long crowded census, T = 100, cost 33.00 of the 120-credit award. Remaining on the grant account: 87.00. Unused grant credits do not roll over, so the remainder is unspent by choice: a second copy of the same main-event run would be a second main event, which the rules do not allow ("one main-event experiment per night").
- Review allowance 15, unused: no paper of mine was awaiting review, and no review requests were filed.
- Grant: my proposal won tonight's vote, 2-2 with lab-keystone (lab-b had 1). The award file (`grants/2026-11-19/award.json`) names lab-a the winner under the tie-break rule. My vote went to lab-keystone (`out/grants/2026-11-19/votes/lab-a.json`).

## Established

### Cost constant (H3): supported at N = 1, 2, 3, 16
- k = 0.02. All results to date match `1 + 0.02 N T`, including the round-1 triangles (N = 3, T = 1.5 and 4.0 for the pairs), round-2 request 001 (N = 3, T = 2, cost 1.12), and request 007 (N = 16, T = 10, cost 4.20).

### Tracker noise: about 0.05 per coordinate
- Residual rms 0.047-0.053 on every run that fits its model, across all rounds. Round 1 triangles: 0.047-0.051. Round 1 B-B: 0.052-0.053. Round 2 B-C-C: 0.047.

### No decays or census changes observed
- 0 census events in every run to date (about 38 runs). Includes the lone A at T = 100, the 16-particle run at T = 1, request 007 (16 particles, A/B/C, T = 10, 201 samples), and round-2 request 001 (B-C-C, T = 2, 101 samples).
- Still not tested: a long (T = 100) crowded run. This is the grant request, `2026-11-19/r3/lab-a/001`, pending.

### Pairwise additivity for three particles (H12): supported in the tested N = 3 domains
- **A-B-C and A-A-A at separation 5, T = 1.5** (round 1, 2026-11-19/r1/lab-a/001-004). Published as P-0007 (`out/papers/P-0007/`). Predictor reproduces request 001 at rms 0.051.
- **B-C-C at separation 5, at rest, T = 2** (round 2, 2026-11-19/r2/lab-a/001). Pre-registered prediction (`labs/lab-a/analysis/pred_2026-11-19_r2_BCC.json`, written before the run): pairwise sum of the P-0005 table (B on C -6.10, C on B -10.59, C on C 12.36).
  - Result, checked with `out/labs/lab-a/analysis/check_r2_BCC.py` (101 samples, no events, labels B/C/C constant):
    - residual rms (pairwise model): **0.047** per coordinate
    - residual rms (zero-force null): 0.141 per coordinate
    - verdict under the pre-registered rule (<= 0.07 supports): **supported**
  - This is the first N = 3 test that includes C-C. It is one run. Under the persona rule (repeat before trusting), it is not yet published. Replicate: `2026-11-19/r3/lab-a/002`.
  - What it does not show: it does not resolve the coupling factorisation (H9 for C-C), because the C-C value is taken as measured, not derived.
- Limits (all tests): equilateral starts only; N = 3 only; the three-body term below noise over T <= 2 is not excluded. No N = 4 or more data from me yet.

### B-B coefficient at separation 5 (P-0005 c3): two new run fits
- Round 1 runs 005 and 006 (B-B, sep 5, T = 4), fitted by 1-D grid search over K_B(B) on full trajectories with the pair law (`check_r1_2026-11-19.py`):
  - 005: K_B(B) = 6.30, rms 0.052
  - 006: K_B(B) = 6.28, rms 0.053
  - mean 6.29. Inside the P-0005 range 5.60-6.75 but above its mean of 6.12.
- **Not yet published.** P-0005 c3 and the P-0005/P-0007 `model.py` still use 6.12. Two runs fitted to full trajectories (not per-particle endpoints) are not strictly comparable with the earlier run means. Decision: next paper that revises B-B will use the pooled set. No change made to P-0005 now.

### Pair coefficients at separation 5, at rest, T = 2 (P-0005, replicated)
Acceleration on particle i = K_i / r^2.5 toward the partner for K > 0 (negative = repulsion). Chamber and time units.

| pair | particle | run means | runs | status |
|---|---|---|---|---|
| A-A | A | 18.0 | P-0003 (2026-11-17 r3/005-006) | established |
| A-B | A (on B) | 8.99 | 8.82 / 9.16 | replicated |
| A-B | B (on A) | 12.34 | 12.39 / 12.28 | replicated |
| A-C | A (on C) | -8.77 | -8.60 / -8.94 | replicated, repulsion |
| A-C | C (on A) | -21.25 | -21.38 / -21.12 | replicated, repulsion |
| B-B | B | 6.12 | 5.60, 6.28 (r1); 5.85, 6.75 (r2) | 4 values, spread about 9%; new 2-run fits 6.29 (see above) |
| C-C | C | 12.36 | 12.34, 12.70 (r1); 12.31, 12.08 (r2) | 4 values, spread about 5%; N = 3 check in B-C-C (see above) |
| B-C | B (on C) | -6.10 | -5.93 / -6.27 | pre-registered prediction passed |
| B-C | C (on B) | -10.59 | -10.65 / -10.53 | pre-registered prediction passed |

Published as P-0005. Predictor fits all 10 sep-5 runs at noise level, in-sample.

### Distance law (H7, H11): shared scale at separations 7 and 9
- A-A far field, effective K at P = 2.5 (shared-K fits): r = 4: 17.7; r = 5: 18.0; r = 6: 16.5; r = 7: 15.5 (mean of per-particle 15.45, 15.80, 15.25, 15.40); r = 8: 13.6; r = 9: 11.7 (per-particle 11.25, 12.25, 11.35, 11.95).
- Power law and screened inverse square (K exp(-r/8)/r^2) still not discriminated. Open.
- H11: sep 7 and sep 9 coefficients scale with one factor (0.86 at 7, 0.65 at 9) from the A-A reference. Round-3 sep-7/9 runs agree within about 5%. Published as P-0006 (`out/papers/P-0006/`).

### C-C factorisation (H9): still open
- B-C passed (P-0005 c5). B-B agrees with the product rule. C-C misses by about 20% at sep 5 (12.36 measured vs 10.3 predicted from the coupling-product rule used for B-C, H9). The C-C distance-law ratio (0.845 at 7) matches A-A's, so the miss is in the coefficient or in m_C, not in r-dependence.
- The B-C-C result (N = 3) uses the measured C-C value and matches it; this supports the table as a pairwise description, not the factorisation.
- Masses m_B = 0.73, m_C = 0.40 are inferred, not measured. Any claim that depends on them is weaker than its numbers.

### Free flight with specular walls (H1, H2, H6): supported
- A: P-0001 domain, runs to speed 7.8, T up to 100, corner hit.
- C: P-0002 (lab-b's paper, reviewed by me, verdict replicated within its domain): speeds 0.22-8.6, durations to 100.
- B and C at speed 1: consistent with the same reflected-line predictor.

### Isotropy at separation 4 (H10): supported
- A-A along diagonal, y, horizontal: K = 17.67, 17.71, 17.70 (0.2% agreement).

### P-0003 status
- Predictor reproduces its runs at noise level. Domain sep 3-6, T up to 2. Not falsified.
- Integrator note: separation 3-4 trajectories are sensitive to K and step. Converged at step 0.005 (to 0.0002 for K = 17.67). K = 17.74 unstable at step 0.001 on the diagonal. Round-1 A-A-A used step 0.002 and stayed at noise level down to 3.76.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2-8.6. Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 16.
- H4 no decay: no event in any run to date, including request 007 (N = 16, T = 10) and round-2 B-C-C (N = 3, T = 2). Long crowded census (T = 100) pending (grant request `2026-11-19/r3/lab-a/001`).
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported across separations 3-9 as a shared-scale law. Power vs screened form not discriminated.
- H8 pair force identical for all species pairs: refuted at sep 5 (coefficients differ), and the differences persist at sep 7 and 9 (same scale, different coefficients).
- H9 coupling factorises as g_ij = q_i q_j with masses m_B = 0.73, m_C = 0.40: partially supported. B-C passed; C-C misses by about 20% at sep 5. Not claimed for C-C.
- H10 isotropy at separation 4: supported.
- H11 shared distance law (factor 0.86 at 7, 0.65 at 9): supported within about 5% (P-0006).
- H12 pairwise additivity for three particles: supported in the N = 3 domains tested: A-B-C and A-A-A at side 5, T = 1.5 (P-0007); B-C-C at side 5, T = 2 (one run, rms 0.047; replicate pending). Not tested for four or more particles.
- H13 no census events in a crowded, long-duration run: untested at T = 100. Request 007 (N = 16, T = 10): no events. Grant request pending.

## Round 3 (2026-11-19): what I did
- Checked round-2 request 001 (B-C-C) against its pre-registered rule: supported, rms 0.047 (`out/labs/lab-a/analysis/check_r2_BCC.py`).
- Won tonight's grant with the long crowded census proposal. Filed it exactly as proposed (`out/requests/2026-11-19/r3/lab-a/001.json`, grant account, 33 credits): 16 particles, A/B/C, at rest on a 2.5 grid, T = 100, sample_dt 0.05 (2000 samples), tracker and census. Pre-registered: no census event (H4).
- Filed a replicate of the B-C-C run (`out/requests/2026-11-19/r3/lab-a/002.json`, research, 1.12 credits), to repeat it before publishing.
- Request files were generated and checked by `out/labs/lab-a/analysis/make_2026-11-19_r3_requests.py` (manual schema check; `jsonschema` is not installed here).
- No paper published this round. Reason: the B-C-C claim rests on one run, and the replicate result is not yet available.

## Plan for the next session
1. Check `2026-11-19/r3/lab-a/001` (grant, T = 100, 16 particles). Count census events and species changes. Also check the particle count at every sample (vanishing would show as a count drop, which the census may or may not report as an event). Record the result against H4 and H13 as pre-registered.
2. Check `2026-11-19/r3/lab-a/002` (B-C-C replicate). Compute the residual rms with `check_r2_BCC.py`, adapted to the new results path. If both runs are within 0.07, publish a narrow paper (P-0008): B-C-C at side 5, T = 2, pairwise sum of the P-0005 table, two runs, residual rms, zero-force null, domain stated, predictor using math only.
3. If the replicate misses the rule, do not publish. Check the C-C value and the B-C constants before blaming additivity.
4. B-B update paper (pooled B-B: 4 run-level values plus 2 new fits, 6.29): still pending. Keep P-0005 unchanged until then, and say so.
5. Do not claim anything for separation 3-4 with mixed species. Do not extend P-0007 or P-0008 to four or more particles without data.
6. Research budget: 26.88 left after round 3 (no rollover). Spend on a replicate or a discriminating run only; avoid new untested configurations on research credits.

## What would change my mind
- Grant run (T = 100) with any census event: H4 refuted for the crowded case; a species-by-species census is needed before any other claim. Vanishing without an event would also be a finding.
- B-C-C replicate above 0.07: the single-run pass was a fluke, or the pairwise table does not hold in N = 3 with C-C. P-0008 would not be written.
- B-C-C residual above 0.12 in either run: the C-C value (or pairwise additivity with C) is wrong. P-0005 c4 is then restricted, and H9 for C-C is reopened.
- A new B-B run (or pooled fit) that moves outside 5.6-6.8 per particle: P-0005 c3 widens.
- A triangle or N = 4 result that misses the pair model beyond noise: P-0007 narrows, and additivity is restricted to the N = 2 and N = 3 domains tested here.

## Self-criticism
- The notebook once said the sep-9 A-A factor came from one run. It is two runs (r1/008-009, four per-particle values). Corrected in P-0006.
- The earlier note called the C-C coupling 4.1 vs measured 5.0 a mismatch. The correct K-unit prediction is 10.3 vs 12.36. Both are about 20%. Corrected in P-0005.
- P-0005 c5 uses B-C constants fitted to the same two runs, so its residual rms is in-sample. The pre-registered comparison is the valid test.
- P-0007's pass rests on residuals near tracker noise (0.05), and the zero-force null is only 2-4 times that. A three-body term smaller than the noise over T = 1.5 is invisible here. The claim says so.
- The B-C-C pass (0.047) is one run, so it is not yet a trusted result. It counts as evidence only after the replicate.
- The B-C-C prediction was pre-registered, but the table it uses has C-C from a single two-run mean, not from a fit to the B-C-C run itself. Good: the test is not circular in that sense; the run was not used to set the table.
- The B-B 2-run fit (6.29) is not on the same footing as the four per-particle run means (6.12). Not used for any claim yet.
- The masses (m_B, m_C) are inferred, not measured.

## Analysis code (`out/labs/lab-a/analysis/`, my files)
- `check_r2_BCC.py`: round-2 B-C-C check against the pre-registered rule (rms, null, labels, events). Usage: `python3 -I check_r2_BCC.py <repo_root>`. Reads results from `<repo_root>/results/2026-11-19/r2/lab-a/001.json`.
- `make_2026-11-19_r3_requests.py`: writes round-3 requests 001 (grant, from the proposal) and 002 (research, replicate). Usage: `python3 -I make_2026-11-19_r3_requests.py <repo_root>`.
- Earlier round-1 checks: `labs/lab-a/analysis/check_r1_2026-11-19.py` (run from repo root, reads `labs/lab-a/analysis/pred_2026-11-19_r1_triangles.json`). Usage: `python3 -I check_r1_2026-11-19.py <repo_root>`.
- `labs/lab-a/analysis/pred_2026-11-19_r2_BCC.json`: pre-registered prediction for round-2 request 001 (also used for the replicate). Written before results.
- Earlier scripts (`labs/lab-a/analysis/`): `fit_r3_2026-11-18.py`, `check_p0006.py`, `make_2026-11-19_r1_requests.py`, `pred_2026-11-19_r1_triangles.json`, and earlier round scripts.
- Papers and requests: `out/papers/P-0007/` (paper.md, claim.json, model.py); `out/requests/2026-11-19/r3/lab-a/001.json` (grant) and `002.json` (research); `out/grants/2026-11-19/votes/lab-a.json`.
