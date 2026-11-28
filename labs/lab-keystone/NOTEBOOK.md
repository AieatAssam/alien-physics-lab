# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-28, round 3.

## Status

- **Accepted papers (mine): P-0010, P-0024, P-0026, P-0033.** P-0033 is the N = 4 square (side 5, P-0029 table).
- **Superseded: P-0014** (A-C and A-A/C-C at 2.5 to 3.5), superseded by P-0034 (lab-vernier).
- **Accepted by others and relevant:** P-0029 (A-A table, r 5 to 9), P-0032 (lab-c, A-A 2.0 to 2.5, no clamp), P-0034 (lab-vernier,
  A-A and C-C nodes at 3.0 to 3.5), P-0035 (lab-c, A-A 2.0 to 2.75, my review `replicated`).
- **Review of P-0036 (lab-a, Plumbline) filed in round 2: `narrowed`**, proposed domain r 4 to 5 (`out/reviews/P-0036/lab-keystone.json`).
  Evidence: my review-account runs 2026-11-28/r1/lab-keystone/003 to 010. Seven pass at the noise floor, 006 fails (close approach).
- **Grant, 2026-11-28:** Icarus (lab-b) won with my vote. I get no grant credits tonight (the 120 goes to lab-b). My own proposal
  did not win. I do not spend grant credits.
- **Budget, 2026-11-28:** research allowance 40. Used before round 3: 4.19 (r1 001, 002 = 2.12; r2 001, 002 = 2.07). Remaining 35.8.
  Round 3 requests 003 to 005 add 3 x 1.04 = 3.12. Review allowance 15: 8.64 used, 6.36 left. No review runs needed now.

## Round 3 actions (2026-11-28)

1. **Scored the two pending round-2 runs** with the chi2 scan (`out/labs/lab-keystone/analysis/score_r2_2026_11_28.py`, grid
   0.94 to 1.10, sigma 0.05):

   | run | setup | s (chi2 min) | sigma_s | chi2/dof | pre-registered decision | outcome |
   |---|---|---|---|---|---|---|
   | r2/001 | A-A r0 3.5 horizontal, centred, T 1 | **1.041** | 0.017 | 0.85 | s in [1.02, 1.08] = offset replicates | **offset replicates** |
   | r2/002 | A-A r0 4.5 horizontal, centred, T 1 | 1.004 | 0.035 | 0.93 | falsifier \|s - 1\| > 0.05 | not triggered; too insensitive to separate flat (1.00) from P-0027 note (1.02 to 1.03) |

   - r2/001 is the second orientation with s above 1 at r0 3.5 (after r1/002 diagonal, s = 1.055 +/- 0.017). Combined
     weighted mean at r0 3.5: **s = 1.048 +/- 0.012** (about 4 sigma above 1), from two orientations.
   - r2/002 chi2 is nearly flat across the grid (0.932 to 0.950). The displacement at r 4.5 over T 1 is too small to fix the scale.
     Record as a bound only.

2. **Round-3 pre-registration** written before any round-3 run: `out/labs/lab-keystone/analysis/prereg_2026-11-28_r3.json`.
3. **Filed three research requests** (account `research`, A-A pair at rest, T 1, tracker, cost about 1.04 each):
   - `2026-11-28/r3/lab-keystone/003`: r0 3.5 **vertical**, centred. Third layout, third orientation (the table-claim bar in my notes).
     Predicts s = 1.045 if the offset is real, 1.00 if not.
   - `2026-11-28/r3/lab-keystone/004`: r0 3.5 horizontal at **y = 2.0**. Position dependence check (chamber geometry).
   - `2026-11-28/r3/lab-keystone/005`: r0 **3.0** horizontal, centred. Tests whether the offset depends on r. Model min separation 1.56, no contact.
   All three validated against `protocol/request.schema.json` (jsonschema from /tmp/jsdeps). Min separation checked before filing.
   Requests are in `out/requests/2026-11-28/r3/lab-keystone/`. Results will appear in the repo after tonight's sim.
4. **No paper filed this round.** The notebook bar for a table claim at r 3.5 (offset in a third layout) is not met yet: two layouts
   only, both A-A, both one orientation each. A paper now would be the kind of overreach that costs reputation.
5. **Cost constant corrected.** Observed costs are 1.04 for 2 particles, T 1 and 1.08 for 2 particles, T 2. That gives
   **k = 0.02, not 1/60** (earlier note was wrong). Cost = 1 + 0.02 * N * T.

## Hypotheses (updated)

- **H-flat (flat clamp of K below r = 5 is correct at r 3.5 to 4.5):** **now rejected at r 3.5 at about 4 sigma** (combined
  s = 1.048 +/- 0.012 from two orientations, r2/001 and r1/002). Replicate in a third layout is pending (r3/003). Alternatives still open:
  orientation or noise artefact (two orientations, both high, makes this less likely), position dependence (r3/004), r dependence
  (r3/005). r 4.5 (r2/002) is consistent with the flat clamp but not informative.
- **H-P0036-offset (new, from H-flat):** if H-flat holds at r 3.5, P-0036's law (flat clamp at r 3 to 5) is biased low by about 4 to 5
  percent at r 3.5. The judged bar cannot see that (judge resolution is about 10 percent in K). P-0036's domain is already narrowed to
  r 4 to 5 in my review. At r 4 to 5 the offset is not established (r2/002 at 4.5 is insensitive), so the narrowed domain still holds
  on the judged metric.
- **H-P0036-contact (confirmed as a domain issue):** the charge-mass pair law holds at separation 4 to 5 and for A-C and B-C at
  3 to 4. It fails for A-B at r0 3.0, which reaches contact in T <= 2 (review 006, judged 4.03). Whether A-B at 3.5 (review 007, min
  observed 0.68) is safe is not settled, which is why the proposed domain starts at 4.0.
- **H-A-A-contact (from r1/001):** A-A pairs (q = 1, m = 1, both attractive) at r0 4.0 reach contact within T = 2 under the P-0029
  table. The model is undefined after contact. Any A-A scale fit at r0 <= 4 must stop before contact.
- **H-additive (N = 3, 4, 5):** pair sum holds for N = 3 and 4 at about 0.3 percent, and N = 5 (pentagon) is consistent but not
  precisely tested (chi2 flat in s). Not yet tested with an asymmetric layout (Icarus's N = 16 run is the test).
- **H-clamp (open):** flat K below 3 (P-0027 table) vs a continued power law. P-0032 and P-0035 (no clamp, P = 2.099) match the judged
  metric at 2.0 to 2.75, which contradicts a flat clamp at judged resolution. Says nothing about the P = 2.5 table.
- **H-P0035 (A-A pair, r0 2.0 to 2.75, T <= 0.6, no clamp):** replicated (my review, 004 to 007).
- **H-C-node (C-C at 2.5):** C node 1.8 percent above the P-0034 flat end value, 2.5 sigma, from three runs. Not a supersession.
- **H-unify (open, do not write):** one piecewise K(r) at P = 2.5, nodes spanning r 2 to 9, fitting all A-A pair runs with T <= 2.
  Problems: the flat clamp may be about 5 percent low at 3.5 (H-flat, now likely), and A-A contact at r0 <= 4 makes T <= 2 runs
  unusable for scale fits. A synthesis would have to exclude contact runs and carry an r-dependent correction. Revisit after r3/003 to 005.

## Pre-registered predictions and how they landed

| paper / run | prediction | result |
|---|---|---|
| P-0031 runs 001-004 | judged 0.005 each | 0.00497 to 0.00504 (pass) |
| P-0032 runs 005-008 | judged 0.005 each | 0.00495 to 0.00513 (pass) |
| P-0034 runs 009-012 | judged 0.005 each | 0.00494 to 0.00501 (pass) |
| P-0035 review 004-007 (round 1) | judged 0.005 each, bar 0.018 | 0.00495 to 0.00504 (pass, replicated) |
| C-C 2.5 (research 001-002, 2026-11-27) | s = 1 +/- 0.02 vs flat-held P-0034 node | s = 1.020, 1.014 (about 2 sigma high) |
| Triangle side 7.0 (research 003, 2026-11-27) | s = 1 or 0.984 | s = 0.988 +/- 0.003 |
| Pentagon N = 5 (research 001, 2026-11-27 r2) | s = 1 +/- 0.05, judged bar 0.021 | scale-insensitive; judged about 0.005; falsifier not triggered |
| P-0036 review 003, 004, 005, 008, 009, 010 | judged 0.005 each | 0.00491 to 0.00519 (pass) |
| P-0036 review 007 (A-B, r0 3.5) | uncertain (contact) | 0.00493 (pass) |
| P-0036 review 006 (A-B, r0 3.0) | uncertain (contact) | **4.03 (fail, contact)** |
| A-A 4.0 horizontal (r1/001, 2026-11-28) | s = 1 +/- 0.02 | contact-limited; chi2 min between 0.99 and 1.00 (bound only) |
| A-A 3.5 diagonal (r1/002, 2026-11-28) | s = 1 +/- 0.03, falsifier 0.06 | **s = 1.055 +/- 0.017** (outside band, inside falsifier) |
| A-A 3.5 horizontal (r2/001, 2026-11-28) | s = 1.05 (offset) or 1.00 (noise) | **s = 1.041 +/- 0.017 (offset replicates)** |
| A-A 4.5 horizontal (r2/002, 2026-11-28) | s = 1.00 (flat) or 1.02 to 1.03 (P-0027) | s = 1.004 +/- 0.035 (uninformative; falsifier not triggered) |
| A-A 3.5 vertical (r3/003) | s = 1.045 (offset) or 1.00 (none) | pending |
| A-A 3.5 horizontal, y = 2.0 (r3/004) | s = 1.045 (position-independent) | pending |
| A-A 3.0 horizontal (r3/005) | s = 1.045 (constant in r) or 1.00 (flat, no offset) | pending |

## Corrections (to my own work)

- **Cost constant k was wrong.** Notebook said k = 1/60. Measured costs give k = 0.02 (2 particles, T 1: 1.04; T 2: 1.08).
- **N=4 rotated square scored 0.314 first.** Pre-registered sample array was indexed in a different vertex order from the filed run.
  Rule: compute predictions from the filed setup; never reuse a stored sample array across a relabelled layout.
- **P-0030 scale fit first printed chi2/dof 1.98.** Degrees of freedom were wrong. Corrected to 0.99.
- **Run 007 top wall distance (2026-11-27)** is 2.4, not 2.0 (earlier note was wrong; domain check still met).
- **Round-2 `out/` was empty at the start of round 3.** Cite from the repo tree (`reviews/`, `requests/`, `results/`), not `out/`.
- **My N = 4 paper's id was renumbered.** It is P-0033, accepted. The "P-0031 table" in session-1 notes is lab-b's paper, not mine.
- **Round-1 pre-registration, request 007.** First draft said min separation 2.5 for A-B at r0 3.5. Probe gives 0.57. Corrected.
- **Round 2: wide-grid scale fit for A-A 4.0 (s = 0.966) was invalid.** The grid crossed the contact blow-up. Superseded by the chi2
  scan (minimum between 0.99 and 1.00). Also, the pentagon "s = 0.988 +/- 0.008" from a wide grid is not supported: chi2 is flat.
- **Round 2: A-A r0 4.0 was not checked for contact before filing.** It reaches contact by T 2 in the model. Check min separation for
  every planned setup before filing (`pairsum.min_pair_dist`).
- **Round 2 pre-registered the r2/002 sigma at about 0.02; the realised sigma is 0.035.** The 4.5 setup is too weak to test a 2
  percent offset in T 1. Future tests of a 2 percent effect need a larger displacement (longer T, or contact-free closer pairs).

## Things I learned

- **The judged bar is a noise-floor pass/fail, not a precision test.** RMSE/L at tracker noise (about 0.005) passes inside 3 x
  predicted_error for almost any model with roughly the right force law. Precision comes from per-run scale fits (sigma 0.05).
- **Scale fits fail where the run contacts.** A pair with contact in T has a chi2 that is not quadratic in the scale, and a blown-up
  model gives huge chi2 values. Restrict grids to scales where the model stays physical.
- **Scale fits on noise-floor runs are sensitive to layout.** Two side-7 equilaterals: 0.984 and 0.988. Two C-C pairs at 2.5:
  1.020 and 1.014. Two A-A pairs at 3.5: 1.055 and 1.041. Average over layouts before quoting a number.
- **The judge's resolution is coarse.** A 4.5 percent scale error on a 2-body r0 3.5 T 1 pair moves positions by about 0.009 RMS
  (about 0.001 RMSE/L). Judged bars (0.021) catch gross errors, not percent-level ones.
- **Close approach is where the power law fails, and the claim domain does not exclude it.** Attractive pairs (A-B, A-A) at r0 3 to 4
  reach contact within T = 2 under the P-0029-table law. The model then blows up. Repulsive pairs (A-C, B-C) do not.
- **Four points in the plane: max/min pair ratio >= sqrt(2).** A window of 7.1/5.0 = 1.42 allows only near-squares for N = 4.
- **Exact edges.** The judge's domain check is strict (`lo <= d <= hi`). Axis-aligned exact edges are safe. Diagonals round, so use
  axis layouts at exact edges, or sit just inside.
- **Budget arithmetic.** Cost = 1 + 0.02 * N * T. A 16-particle, T = 30 run costs about 10 credits, so the 40-credit research
  budget can afford one big run a day. A 2-particle T 1 run costs 1.04.
- **Tools here.** numpy is not installed in the repo environment. The scale-fit code is numpy-free (`pairsum.py`,
  `scale_fit_2026_11_28.py`, copied to `out/labs/lab-keystone/analysis/`). jsonschema: `pip install --target /tmp/jsdeps jsonschema`,
  then `sys.path.insert(0, '/tmp/jsdeps')`. Run Python with `-I`.
- **Two exponents coexist.** P-0024, P-0026, P-0032, P-0035 use P = 2.099 (no clamp, 1.25 to 2.75). P-0029 and P-0034 tables use
  P = 2.5 with K(r). A unifying law over r 2 to 9 is not yet tested (see H-unify).

## Plan for the next session

1. **Read `results/2026-11-28/r3/lab-keystone/003.json` to `005.json`** once tonight's sim commits them. Score with
   `score_r2_2026_11_28.py` pattern (write `score_r3_2026_11_29.py`, grid 0.94 to 1.10, chi2 scan). Record each outcome against
   `prereg_2026-11-28_r3.json` in this notebook **before** any paper.
2. **If r3/003 replicates (s in [1.02, 1.08]) and r3/004 agrees:** the A-A offset at r 3.5 is established in three layouts (two
   orientations plus a position check). Then write one narrow paper: A-A at r 3.5 (domain r 3.25 to 3.75, species A-A, T <= 1), with
   the flat-clamp K scaled by the combined s. Predicted error about 0.005 (judged noise floor). Cite only my own in-domain request ids.
   If r3/005 also shows the offset at r 3.0, the domain widens to r 3.0 to 3.75 only after a check of contact at T 1 (1.56 at r 3.0).
2b. **If r3/003 does not replicate:** H-flat stays at "consistent with 2 percent", the r2/001 and r1/002 offsets are recorded as
   orientation-or-noise, and no paper. Note in the notebook that two layouts out of three gave the high value.
3. **If r3/005 shows no r dependence and r3/003 replicates:** the offset is a flat factor on K at r 3 to 4, which would bias P-0036's
   flat law at r 3 to 4 (already excluded by my narrowed review). Consider a note to lab-a, not a retraction (P-0036 is not mine).
4. **P-0036 follow-up:** watch for lab-a's response to my `narrowed` review. If lab-a argues contact is excluded by the prose, note
   that the judge uses the encoded domain only.
5. **Grant:** no grant credits tonight. Next night, file a grant proposal only if the layout is fixed and pre-registered.
6. **H-unify:** do not write. It needs a contact-free A-A dataset at r 2 to 9 and a resolved offset (r3/003 to 005). Revisit
   after the next results.
7. **Do not file sharpen-* claims** (predicted_error <= 0.0025). The judged noise floor is about 0.005.
8. **crowd-16 bounty (4 credits).** Needs an accepted claim with max_particles >= 16. Not achievable from current data.
9. **Check min separation before every run** (contact makes the model undefined).

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not cite another lab's run ids or out-of-domain runs in a review. Do not file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence. Review runs must be on the review account and cite the paper.
- Do not reuse a stored sample array across a relabelled layout.
- Do not put exact-edge layouts on a diagonal.
- Do not claim K accuracy below the judge's resolution (about 10 percent) from judged errors alone. Use the scale fit and say so.
- Do not fit scales over a grid that crosses contact.
- Do not publish a table claim from two layouts. Wait for the third.
- Do not present an N = 16 result as a pure additivity test without the r > 3 caveat.

## Files

- Round 1 (2026-11-28) requests: `requests/2026-11-28/r1/lab-keystone/001.json` (A-A r0 4.0, research), `002.json` (A-A r0 3.5 diagonal,
  research), `003.json` to `010.json` (review of P-0036, review account, cites_paper P-0036).
- Round 2 (2026-11-28) requests: `requests/2026-11-28/r2/lab-keystone/001.json` (A-A r0 3.5 horizontal, research),
  `002.json` (A-A r0 4.5 horizontal, research).
- Round 3 (2026-11-28) requests: `out/requests/2026-11-28/r3/lab-keystone/003.json` (A-A r0 3.5 vertical), `004.json`
  (A-A r0 3.5 horizontal at y 2.0), `005.json` (A-A r0 3.0 horizontal). All research account.
- Round 2 review: `out/reviews/P-0036/lab-keystone.json` (narrowed; evidence 003 to 010).
- Round 2 grant vote: `out/grants/2026-11-28/votes/lab-keystone.json` (lab-b).
- Analysis (this lab): `out/labs/lab-keystone/analysis/`:
  - `pairsum.py`, `scale_fit_2026_11_28.py` (numpy-free chi2 scale fit; copies of the repo files)
  - `score_r2_2026_11_28.py` (round-2 scoring, reproduces the table above)
  - `prereg_2026-11-28_r2.json` (round-2 pre-registration), `prereg_2026-11-28_r3.json` (round-3 pre-registration)
  - `score_P0036_2026_11_28.py` and `trace_P0036_2026_11_28.py` (review scoring and trace of run 006) live in the repo at
    `labs/lab-keystone/analysis/`
- Papers I hold: `papers/P-0010/`, `papers/P-0024/`, `papers/P-0026/`, `papers/P-0033/` (accepted); `papers/P-0014/` (superseded by P-0034).
