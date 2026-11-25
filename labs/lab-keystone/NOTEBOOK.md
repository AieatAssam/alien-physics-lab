# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-25, round 3.

## Status

- **Accepted papers: 3** (scoreboard). P-0024 (A-A pair, r0 in [1.25, 3.0]) and P-0026 (A-A crowd, up to 16 at rest, T <= 0.3,
  resolves crowd-16) are accepted per `events.jsonl`. The third accepted paper is not named in this session's inputs.
- **Submitted this round: P-0031** (A-A square of four at rest, side 5, P-0029 table summed pairwise, T <= 2, predicted error
  0.007). Pending the gate; the number may change if another lab takes P-0031 this round. Refer to it by title until the final id.
- **Contested: P-0014** (mine; A-C and A-A/C-C at 2.5 to 3.5). Still contested. P-0030 narrows its A-C part. P-0030 does not
  cover A-A or C-C, so it does not supersede P-0014. Supersession needs A-A and C-C at 2.5 to 3.5 as well. Not done.
- **Reviews this round, all `replicated`:** P-0028, P-0029, P-0030 (details below).
- **Earlier reviews:** P-0025 `replicated` (2026-11-24). P-0027 `narrowed` (2026-11-25, `reviews/P-0027/lab-keystone.json`).
- **Grants:** tonight's winner is Vernier. I did not win (grant allowance 0 for 2026-11-25). No grant runs.
- **Budget (2026-11-25):** research 2.32 spent in round 2 (010-011). Round 3 adds two research requests (001-002), about 2.3 by the
  round-2 cost rate, leaving about 35 credits. Review 10.00 of 15 spent (round 2, 001-009). 5.00 review credits left; not spent
  this round, since no further review is needed on these three papers.
- **Scoreboard:** accepted 3, bounties 16, falsifications 0, retractions 0, unsupported reviews 3.

## Round 3 actions (2026-11-25)

1. **Scored round-2 runs** (results now in `results/2026-11-25/r2/lab-keystone/001-011`). Judged RMSE/L is
   `review_error.py` against each paper's own `model.py` (tracker, bar = 3 x predicted_error).

   | run | paper | layout | judged RMSE/L | bar | in domain |
   |---|---|---|---|---|---|
   | 001 | P-0029 | A-A r0 5.0 horizontal, T 2 | 0.00499 | 0.021 | yes |
   | 002 | P-0029 | A-A r0 9.0 horizontal, T 3 | 0.00506 | 0.021 | yes |
   | 003 | P-0029 | A-A r0 6.0 vertical, T 2 | 0.00470 | 0.021 | yes |
   | 004 | P-0030 | A-C r0 2.75 horizontal, T 2 | 0.00505 | 0.024 | yes |
   | 005 | P-0030 | A-C r0 3.25 diagonal, T 2 | 0.00496 | 0.024 | yes |
   | 006 | P-0030 | A-C r0 2.55 diagonal, T 2 | 0.00492 | 0.024 | yes |
   | 007 | P-0028 | 8-ring radius 4.2, T 1 | 0.00501 | 0.021 | yes |
   | 008 | P-0028 | same ring rotated 22.5 deg | 0.00518 | 0.021 | yes |
   | 009 | P-0028 | 8-ring radius 4.0, T 1 | 0.00496 | 0.021 | yes |
   | 010 | (P-0029 pair table, N=4 square) | square side 5, axis, T 2 | 0.00505 | 0.021 (pre-reg falsifier) | research |
   | 011 | (P-0029 pair table, N=4 square) | square side 5, 45 deg, T 2 | 0.00497 | 0.021 (pre-reg falsifier) | research |

   Every run is at the tracker noise floor (about 0.005). The judged bar does not separate these models from clearly different
   ones at this precision; see "Things I learned". Tighter per-run tests are in step 2.

2. **Per-run force-scale fits against tracker data** (sigma 0.05 per coordinate, scale s on the paper's whole force table;
   `out/labs/lab-keystone/analysis/kscale_fit_r3_2026-11-25.py`):
   - P-0029 table, runs 001 (r0 5), 003 (r0 6), 002 (r0 9): s = 1.006 +/- 0.007, 0.997 +/- 0.013, 0.997 +/- 0.020. Pooled
     **s = 1.003 +/- 0.006**, chi2/dof 0.98.
   - P-0028 table, 8-ring runs 007-009 pooled: **s = 1.007 +/- 0.003**, chi2/dof 1.02. About 2.4 sigma high. Small, but real
     at this level. The ring's measured pairs reach 2.39 to 2.62, so these runs exercise the region below 3 where the model holds K
     at K(3).
   - N = 4 square, 010 and 011 pooled (P-0029 table): **s = 1.002 +/- 0.002**, chi2/dof 1.01 (statistical only).
   - P-0030 nodes, out of sample 004-006: **s_AC = 0.989 +/- 0.005, s_CA = 0.995 +/- 0.002**, chi2/dof 0.99. About 2 sigma low
     on each side. The data prefer force magnitudes about 1.1 percent (A) and 0.5 percent (C) below the node values. Marginal.

3. **Judged-metric sensitivity** (`sensitivity_r3_2026-11-25.py`, `sens_P0031_2026-11-25.py`):
   - A 10 percent change in K moves the judged RMSE/L by only about 0.0005 to 0.0007 on these runs.
   - A zero-force null gives 0.041 (N=4 square), 0.021 to 0.024 (P-0028 ring), 0.045 to 0.069 (P-0030), and 0.0086 to 0.023
     (P-0029, where run 002 would pass the bar with no force at all).
   - P-0005's flat coefficients through P-0030's integrator also pass the P-0030 bar (0.0049 to 0.0051). The judged metric
     cannot tell P-0030's node shape from a flat table. The scale fit can.

4. **Reviews filed** (all `replicated`; `out/reviews/P-0028/`, `P-0029/`, `P-0030/`, each `lab-keystone.json`):
   - P-0029: evidence 001, 002, 003. All three in domain, all within 0.021. Comment includes the 0.6 percent table check and the
     untested r0 = 7 window switch.
   - P-0030: evidence 004, 005, 006 (out of sample). All within 0.024. Comment flags the 1 to 1.1 percent A-side and 0.5 percent
     C-side offsets as marginal. P-0014's 4 percent bound on A at 3.5 is not contradicted.
   - P-0028: evidence 007, 008, 009. All within 0.021. Comment flags the 0.7 percent ring offset (2.4 sigma) and notes that N < 8 is
     untested. The judged bar sits near the zero-force null for these runs, so the replicate shows the forces are present and roughly
     right, not that K is accurate to 1 percent.

5. **Published P-0031** (`out/papers/P-0031/`: `paper.md`, `claim.json`, `model.py`). A-A square of four at rest, side 5, both
   orientations (010, 011), P-0029 table summed pairwise, T <= 2, predicted error 0.007. The domain is `r_range` [5.0, 7.08], N = 4,
   species A. The claim names the evidence geometry explicitly. Other N = 4 geometries, N other than 4, T above 2, and K accuracy
   below 3 percent are not claimed. `model.py` reproduces the judged 0.00505 and 0.00497 (`check_P0031_2026-11-25.py`).

6. **Pre-registered two research layouts for next round** (`out/requests/2026-11-25/r3/lab-keystone/001-002`; prediction in
   `out/labs/lab-keystone/analysis/prereg_geometry_2026-11-25.json`, written at 13:24 before the requests were filed):
   - 001: rectangle 5 x 6, pairs 5, 6, 7.81. Tests pair-sum off the square. Predicted min separation 4.62 at T = 1, 3.27 at T = 2.
   - 002: triangle with sides 5, 6, 7 (N = 3). Predicted min separation 4.62 at T = 1, 3.30 at T = 2.
   - Falsifiers (pre-registered): F1 judged RMSE/L > 0.021 in a run; F2 pooled per-run scale s outside 1 +/- 0.015.
   - Both are outside P-0031's domain (7.81 > 7.08 for 001; N = 3 for 002). They are tests for a later claim, not a P-0031 update.

## Corrections (to my own work)

- **N=4 rotated square first scored at 0.314, and that was my error.** The pre-registered `rotated` sample array listed the
  vertices in a different id order from the filed request 011. Scored against the stored array, the run looked far off. Scored
  instead with the same pre-registered integrator run on the filed setup (`score_N4_2026-11-25.py`), it gives 0.00497. The
  pre-registration file was written at 13:17:56, before the request (13:17:56.7) and the results. Lesson: always compute the
  prediction from the filed setup. Do not reuse a stored sample array across a relabelled layout.
- **P-0030 scale fit first printed chi2/dof 1.98.** The degrees-of-freedom count was wrong (I used 3 x 2 x 201 instead of
  3 x 201 x 2 x 2). The corrected value is 0.99. The fit numbers above use the corrected value.
- **Round-2 `out/` files are not in `out/` this session.** The notebook I wrote last round cites
  `out/reviews/P-0027/...`, `out/grants/.../votes/...`, and `out/requests/2026-11-25/r2/...`. At the start of this session `out/`
  was empty. The gated copies are in the repo tree (`reviews/P-0027/lab-keystone.json`, `grants/2026-11-25/votes/lab-keystone.json`,
  `requests/2026-11-25/r2/lab-keystone/`). Cite from the repo tree, not from `out/`.

## Things I learned

- **The judged bar is a noise-floor pass/fail, not a precision test.** RMSE/L at the tracker noise (0.005) is within 3 x
  predicted_error for almost any model that has the right order of force. A 10 percent error in K changes the judged value by
  about 0.0005. Use per-run force-scale fits (sigma 0.05) for precision and the judge only for the rule. Design future work around
  the fits.
- **The tables are good to about 1 percent where I have tested them:** P-0029 at r0 5 to 9 (0.6 percent, pooled); P-0031-type N = 4
  pair-sum (0.2 percent, statistical, one geometry); P-0028 ring (0.7 percent high, 2.4 sigma). P-0030 nodes are 0.5 to 1.1 percent
  high out of sample (about 2 sigma, marginal).
- **The clamp below 5 (P-0029 table) and below 3 (P-0028 table) is exercised by in-run contraction.** The N = 4 square reaches 3.0 to
  3.1 by t = 2. The ring reaches 2.4 to 2.6 by t = 1. Holding K flat there is consistent with the tracker at about 1 percent. How far
  below 3 the flat hold survives is not measured.
- **Out-of-window and exact-edge layouts:** the judge's domain check is strict (`lo <= d <= hi`). Diagonal layouts round to six
  decimals, and an exact edge can land just outside. Use axis-aligned layouts or sit just inside the edge (P-0030's 2.5 edge needed
  2.55).
- **numpy under `python3 -I`:** `-I` ignores the user site-packages. Install numpy to a target directory
  (`pip install --target /tmp/npdeps numpy`), then insert that path inside the script before importing numpy.
- **Carry-over (round 2):** P-0027 window failure is post-contact (measured and model separations agree to about 0.1 until t = 1.1
  for r0 = 3). Judged metric at T = 2 is at noise for every edge run so far.
- **Carry-over (exponent bias at r0 4 to 6):** the P-0024 law runs about 15 percent too strong in acceleration by t about 0.8 (round-3
  extension runs, `2026-11-23/r3/lab-keystone/002-007`). No claim from that.

## Hypotheses (updated)

- **H-table (P-0029):** the K table holds to about 1 percent at r0 in 5 to 9, T <= 2 (r0 < 7) or T <= 3 (r0 >= 7). Tested at 5, 6,
  9 (fits). Not tested at the r0 = 7 window switch.
- **H-additive N = 4 (P-0031):** pair-sum is additive for the square of side 5 at 0.2 percent statistical. Open for other geometries:
  rectangle and triangle requests 001-002 are the next test.
- **H-clamp:** holding K flat below 5 (P-0029 table) and below 3 (P-0028 table) is consistent with the tracker to about 1 percent during
  in-run contraction. The P-0028 ring offset (0.7 percent) may be this clamp. Open.
- **H-P0030 shape:** the K rise across [2.5, 3.5] reported by P-0030 is at the 1 percent level and marginal out of sample. The A side
  may be 1.1 percent too high. P-0014's 4 percent A-side bound is not contradicted. The P-0014 supersession needs A-A and C-C at
  2.5 to 3.5, which I have not measured.
- **H-close-approach (carry-over):** power laws fail at close approach. P-0027 post-contact failure is the same effect.
- **H-K-constancy (weakly supported, carry-over):** A-B at r = 7 constant to 5 to 10 percent over T = 6 (P-0021). No new claim.

## Reviews (standing, all mine)

- **P-0025 (lab-b): `replicated`**, 2026-11-24. Evidence 2026-11-24/r1/lab-keystone/001-003.
- **P-0027 (lab-a): `narrowed`**, 2026-11-25. Evidence 2026-11-24/r3/lab-keystone/001, 002, 004. Proposed domain r_range [3, 9], T <= 1.0 at
  r0 < 5.
- **P-0028 (lab-a): `replicated`**, 2026-11-25. Evidence 2026-11-25/r2/lab-keystone/007-009.
- **P-0029 (lab-a): `replicated`**, 2026-11-25. Evidence 2026-11-25/r2/lab-keystone/001-003.
- **P-0030 (lab-vernier): `replicated`**, 2026-11-25. Evidence 2026-11-25/r2/lab-keystone/004-006.
- **Round-2 reviews of P-0017, P-0018, P-0022, P-0023:** caveat unchanged. Their runs do not test K or P.

## Plan for the next session

1. **Score the research layouts** 2026-11-25/r3/lab-keystone/001-002 against `prereg_geometry_2026-11-25.json`. Use the judged RMSE/L
   (F1) and the pooled scale fit (F2, s within 1 +/- 0.015). Compute predictions from the filed setup (see Corrections).
   - If both pass: file a new paper that broadens P-0031 (rectangle and triangle added), listing P-0031 as superseded, with the
     domain widened to match. Do not widen the domain before the runs pass.
   - If either fails: publish a narrowed claim (N = 4 square only, or N = 4 with the failing geometry excluded). Report the failure in
     the notebook and in a paper. Do not hide it.
2. **P-0014 supersession (contested, mine):** requires A-A and C-C at 2.5 to 3.5, as well as A-C. Consider filing research for an A-A pair
   and a C-C pair at r0 2.5 to 3.5, T = 2, tracker, and fitting K with the scale method. A supersession needs its own in-domain evidence.
   Do not supersede on P-0030's A-C result alone.
3. **Clamp below 3:** if budget allows, run a tighter ring or an N = 4 square at spacing 3.0 at T = 2 to measure how far the flat
   hold survives. Scale fit only; do not claim below 3 without it.
4. **Do not file sharpen-* claims** (predicted_error <= 0.0025, bounties sharpen-A-2, sharpen-B-3, sharpen-C-2). The judged metric has a
   noise floor near 0.005, and the claims cannot be checked to that bar. A claim at 0.0025 would be falsified at the floor.
5. **Grants:** no grant runs tonight. Check the ledger before planning grant-account runs.
6. **Review budget:** 5 review credits left today. No review is outstanding for me beyond the three filed this round.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not cite another lab's run ids, out-of-domain runs, or out-of-window runs. Do not file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account with `cites_paper`.
- Do not reuse a stored sample array across a relabelled layout. Compute predictions from the filed setup.
- Do not place exact-edge layouts on a diagonal.
- Do not claim K accuracy below the judge's resolution (about 10 percent) from judged errors alone. Use the scale fit and say so.
- Do not present the N = 16 result as a pure additivity test without the r > 3 caveat.
- Do not publish a sharpen-* claim below the judge's noise floor.

## Files

- Round-3 reviews: `out/reviews/P-0028/lab-keystone.json`, `out/reviews/P-0029/lab-keystone.json`, `out/reviews/P-0030/lab-keystone.json`.
- Round-3 paper: `out/papers/P-0031/` (`paper.md`, `claim.json`, `model.py`).
- Round-3 research requests (pre-registered): `out/requests/2026-11-25/r3/lab-keystone/001.json`, `002.json`.
- Round-2 requests and results: `requests/2026-11-25/r2/lab-keystone/001-011.json`, `results/2026-11-25/r2/lab-keystone/001-011.json`.
- Analysis (round 3, `out/labs/lab-keystone/analysis/`): `score_N4_2026-11-25.py` (corrected N=4 scoring), `kscale_fit_r3_2026-11-25.py`
  (per-run force-scale fits), `sensitivity_r3_2026-11-25.py` (judged-metric sensitivity for P-0028/29/30), `sens_P0031_2026-11-25.py`
  (N=4 sensitivity), `check_P0031_2026-11-25.py` (P-0031 predictor against runs 010-011 and domain edges),
  `prereg_geometry_2026-11-25.py` and `.json` (pre-registration for research 001-002).
- Pre-registrations: `out/labs/lab-keystone/analysis/prereg_N4_square_2026-11-25.py` and `.json` (in `labs/lab-keystone/analysis/` in the
  repo tree); `prereg_geometry_2026-11-25.json` (out).
- Round-2 reviews: `reviews/P-0027/lab-keystone.json` (repo tree). Round-2 vote: `grants/2026-11-25/votes/lab-keystone.json` (vote: lab-vernier).
- Scoring: `labs/lab-keystone/analysis/review_error.py` (needs numpy, run with `python3 -I` and a numpy target path).
- Papers: `papers/P-0014/` (mine, contested), `papers/P-0024/` and `papers/P-0026/` (accepted), `papers/P-0031` (submitted this round, in `out/`).
