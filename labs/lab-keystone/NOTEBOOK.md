# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-27, round 2.

## Status

- **Accepted papers (mine, per events.jsonl): P-0010, P-0024, P-0026, P-0033.** P-0033 is the N = 4 square (side 5, P-0029 table),
  accepted 2026-11-26. Scoreboard shows 4 accepted, which matches.
- **Superseded: P-0014** (A-C and A-A/C-C at 2.5 to 3.5), superseded by P-0034 (lab-vernier) on 2026-11-26.
- **Lab-b's P-0031** is the N = 3, 4 symmetric-layout paper (P-0027 table). It is not mine. My square is P-0033.
- **Accepted by others and relevant:** P-0029 (A-A table, r 5 to 9), P-0032 (lab-c, A-A 2.0 to 2.5, no clamp), P-0034 (lab-vernier,
  A-A and C-C nodes at 3.0 to 3.5). P-0027 superseded by P-0029. P-0035 (lab-c, A-A 2.0 to 2.75) is pending my review, now filed.
- **Budget, 2026-11-27:** research 40 (round 1 used 3.16; 36.84 left before round 2), review 15 (round 1 used 4.08 on runs 004 to 007).

## Round 2 actions (2026-11-27)

1. **Reviewed P-0035 (lab-c): `replicated`** (`out/reviews/P-0035/lab-keystone.json`). Evidence: review runs 004 to 007 (review account,
   citing P-0035, all in domain). Judged RMSE/L against P-0035 model.py: 004 0.00495 (r0 2.00), 006 0.00497 (2.40), 007 0.00500 (2.60),
   005 0.00504 (2.75). Bar 0.018 = 3 x 0.006. All four pass. Scope is T <= 0.6. Scored by `out/labs/lab-keystone/analysis/score_p0035_review_2026-11-27.py`.
2. **Scored research 001 to 003** (`out/labs/lab-keystone/analysis/score_research_001_003_2026-11-27.py`, RK4 h = 0.001, sigma 0.05 per coordinate):
   - **001 and 002 (C-C pair at rest, r0 = 2.5, T = 0.6):** scale s = 1.020 +/- 0.012 and 1.014 +/- 0.012 against the P-0034 C node
     table, with that table held flat at its 2.5 end value. Judged RMSE/L at s = 1: 0.00500 and 0.00505 (both pass the 0.021 bar at
     noise). With the earlier run 2026-11-26/r1/lab-keystone/014 (s = 1.021 +/- 0.012, from session 1), three runs give about
     1.018 +/- 0.007. That is about 2.5 sigma above 1 and 1.8 percent above the flat-held node. **Not a supersession.** The 2.5 node is
     outside P-0034's claim (3.0 to 3.5), so this is a fit, not a prediction. No C claim filed.
   - **003 (A equilateral triangle, side 7.0, T = 2.0):** scale s = 0.988 +/- 0.003 against the P-0029 table summed pairwise (chi2/dof 1.02).
     Judged RMSE/L at s = 1: 0.00504 (passes). The first side-7 layout (2026-11-25/r2 run 003, side 7.09) gave s = 0.984 +/- 0.003.
     **Decision rule:** I had said a repeat at about 1.6 percent low would make the offset real, and a repeat at 1.0 or less would
     mean noise. The repeat is 1.2 percent low, which is neither. Honest reading: a real residual of about 1 to 1.5 percent at r near 7 in
     the P-0029 table, smaller than the first estimate. Not enough for a narrowing claim; the judged metric resolves about 10 percent.
3. **Grant vote (round 2): voted lab-vernier** (`out/grants/2026-11-27/votes/lab-keystone.json`). Reason: four replicate A-A contacts in
   one run, a pre-registered pre-contact check, and measured post-contact behaviour. It covers the close-range gap that blocks a
   unifying A-A synthesis. Nullius's replicate of r1-012 (dt 0.001) asks one of the same questions with less coverage. Icarus (B-B
   pair, one constant K) is clean and cheap but does not touch the close-range gap. Plumbline (16 A, T = 30) is chaotic over that
   duration, so a failure would be uninterpretable. I did not vote for my own pentagon.
4. **Research 001 (round 2): pentagon N = 5** (`out/requests/2026-11-27/r2/lab-keystone/001.json`, research account, cost about 1.08).
   Same layout and setup as my round-1 grant proposal, pre-registered in `labs/lab-keystone/analysis/prereg_pentagon_2026-11-27.json`.
   **Why run now and not wait for the grant:** research credits are unused today and do not roll over. Running it now gets the N = 5
   additivity answer tonight, whatever the vote. The cost is that if I win the grant, round 3 needs a different N = 5 layout. Noted here.
   Prediction and falsifier: `|s - 1| > 0.05` or judged RMSE/L above 0.021 fails. Score it next session after the result is in.
5. **Synthesis status:** the condition in round 1 (P-0032 and P-0034 accepted) is now met. I have not written the synthesis. See the plan.

## Round 1 actions (2026-11-27, carried over)

- Reviewed P-0035 runs filed: review 004 to 007 (scored above). Research 001 and 002 (C-C at 2.5), research 003 (side-7 equilateral).
- Grant proposal (round 1): five A at rest in a pentagon, side 5.5, centre (5, 5), T = 1.0 (listed tonight).
- Note from round 1 that was wrong: I wrote that run 007's top particle is 2.0 from the top wall. It is at y = 7.6, so 2.4 from the top wall.
  The claim domain (>= 2.0) is met either way.

## Round 2 (2026-11-26, carried over)

- Scored review-account runs 001 to 012 (P-0031, P-0032, P-0034). All at the tracker noise floor (judged RMSE/L 0.0049 to 0.0051).
  Filed `replicated` for P-0031, P-0032, P-0034.
- Research 013 to 015 (P-0034 node at 2.5): A-A combined s = 0.997 +/- 0.006 (A node at 2.5 passes); C-C 014 1.021 +/- 0.012.
- Grant vote: lab-a (Plumbline, A-B falls from r0 = 9 to contact).

## Round 1 (2026-11-26, carried over)

- Round-3 geometry runs (rectangle 5 x 6, triangle 5, 6, 7): judged RMSE/L 0.00496 and 0.00515 (bar 0.021), pooled scale 0.997 +/- 0.003.
- Grant proposal (mixed A-B at r0 = 2.5): not awarded.

## Pre-registered predictions and how they landed

| paper / run | prediction (judged RMSE/L) | result |
|---|---|---|
| P-0031 runs 001-004 | 0.005 each | 0.00497 to 0.00504 (passes) |
| P-0032 runs 005-008 | 0.005 each | 0.00495 to 0.00513 (passes) |
| P-0034 runs 009-012 | 0.005 each | 0.00494 to 0.00501 (passes) |
| P-0035 review 004-007 (round 1) | 0.005 each, bar 0.018 | 0.00495 to 0.00504 (passes, replicated) |
| C-C 2.5 (research 001-002) | scale s = 1 +/- 0.02 vs flat-held P-0034 node | s = 1.020, 1.014 (about 2 sigma high, combined 1.018 +/- 0.007) |
| Triangle side 7.0 (research 003) | scale s = 1 (noise), or 0.984 (real offset) | s = 0.988 +/- 0.003 (in between; neither rule decides) |
| Pentagon N = 5 (round 2 research 001) | s = 1 +/- 0.05, judged bar 0.021 | pending result |

## Corrections (to my own work)

- **N=4 rotated square scored 0.314 first.** The pre-registered sample array was indexed in a different vertex order from the filed run.
  Rule: compute the prediction from the filed setup; never reuse a stored sample array across a relabelled layout.
- **P-0030 scale fit first printed chi2/dof 1.98.** Degrees of freedom were wrong. Corrected to 0.99.
- **Round-2 `out/` was empty at the start of round 3.** Cite from the repo tree (`reviews/`, `requests/`, `results/`), not `out/`.
- **My N = 4 paper's id was renumbered.** It is P-0033, accepted. The "P-0031 table" in session-1 notes is lab-b's paper, not mine.
- **Run 007 top wall distance** is 2.4, not 2.0 (see round 1 note).

## Things I learned

- **The judged bar is a noise-floor pass/fail, not a precision test.** RMSE/L at the tracker noise (about 0.005) passes inside
  3 x predicted_error for almost any model with roughly the right force law. Precision comes from per-run scale fits (sigma 0.05).
- **Scale fits on noise-floor runs are sensitive to layout.** Two side-7 equilaterals gave 0.984 and 0.988. Two C-C pairs at 2.5 gave
  1.020 and 1.014. Averaging over layouts is safer than trusting any one.
- **Pentagon and close approach.** Symmetric collapse shrinks pair distances fast. A side-5.0 pentagon reaches pair distance 3.6 by
  T = 2 and leaves the table. Check the minimum pair distance over the whole run before filing any N >= 4 probe.
- **Four points in the plane: max/min pair ratio >= sqrt(2).** A window of 7.1/5.0 = 1.42 allows only near-squares for N = 4.
- **Triangles and pairs at separation 3.0 reach contact fast.** Probes below separation 3 must be short (T <= 0.6 for N = 3 and N = 4).
- **Clamp below 3 is not settled.** A flat clamp and a continued power law normalised to K(3) differ by about 3 percent at r = 2.75 and
  about 15 percent at r = 2.0. P-0032 and P-0035 (no clamp, P = 2.099) match the judged metric at 2.0 to 2.75. That contradicts the
  flat clamp at the judged resolution but says nothing about the P = 2.5 table.
- **Two exponents coexist.** The P-0024, P-0026, P-0032, P-0035 pair law uses P = 2.099 (no clamp, 1.25 to 2.75). The P-0029 and
  P-0034 tables use P = 2.5 with K(r). Both fit their own domains. A unifying law over r 2 to 9 is not yet tested, and it cannot be
  a single power with a constant K (see H-unify).
- **Exact edges.** The judge's domain check is strict (`lo <= d <= hi`). Axis-aligned exact edges are safe. Diagonals round,
  so use axis layouts at exact edges, or sit just inside.
- **Tools here.** numpy is not installed. Pure-Python scripts work. For jsonschema, `pip install --target /tmp/jsdeps jsonschema` and
  insert the path before importing (`python3 -I`).
- **Carry-over (exponent bias at r0 4 to 6).** The P-0024 law runs about 15 percent too strong in acceleration by t about 0.8
  (2026-11-23/r3/lab-keystone/002 to 007). The P-0029 table fits 0.6 percent at r0 5 to 9. No claim from it.

## Hypotheses (updated)

- **H-table (P-0029 K table, A-A, P = 2.5):** holds to about 1 percent at r0 in 5 to 9, T <= 2 (r0 < 7) or T <= 3 (r0 >= 7). Side-7
  equilateral runs fit at 0.984 and 0.988 (1.2 to 1.6 percent low). Open: is the residual real and at what level? Precision note only.
- **H-additive (N = 3, 4, P-0033 and lab-b's P-0031):** the pair sum holds for N = 3 and 4 at about 0.3 percent (statistical). Open for N >= 5.
  Test: pentagon (round 2, research 001, filed).
- **H-clamp (open):** flat K below 3 (P-0027 table) vs a continued power law. P-0032 and P-0035 contradict the flat clamp at the judged
  resolution at r0 2.0 to 2.75.
- **H-P0035 (A-A pair, r0 2.0 to 2.75, T <= 0.6, no clamp):** replicated (review 004 to 007).
- **H-C-node (C-C at 2.5):** C node 1.8 percent above the P-0034 flat end value, 2.5 sigma, from three runs. Not a P-0014 supersession.
  Do not file a C claim at 2.5 until a table at 2.5 is fitted or a run at 2.5 with a different layout shows the same offset.
- **H-unify (new):** one piecewise K(r) at P = 2.5, nodes spanning r 2.0 to 9, fits all A-A pair runs with T <= 2 at the noise floor
  (judged RMSE/L about 0.005). Open. Predicted to fail somewhere near r 2 to 3, where P = 2.099 and P = 2.5 differ by about 3 to 4 percent.
  Test: fit the table to existing in-domain runs and check residuals by r0 before writing a claim.
- **H-mixed (A-B coupling):** A-B coupling equals the A-A law (s = 1). Open. Previously proposed at r0 = 2.5 (not awarded).
- **H-close-approach:** power laws fail at close approach. Vernier's four-pair probe (r0 = 1.0, T = 2, grant proposal) tests this. Open.

## Plan for the next session

1. **Score round-2 research 001 (pentagon N = 5).** Use `prereg_pentagon_2026-11-27.json` (predicted positions from the filed setup;
   do not reuse a sample array across layouts). Falsifier: |s - 1| > 0.05 or judged RMSE/L > 0.021. If it passes, the N = 5 additivity
   statement is a small claim. Paper id: next free number at filing time. Do not claim N >= 6 from it.
2. **Round 3 grant.** Results of the vote are not known to me yet. If my pentagon proposal wins, its layout is already used by
   research 001, so run a different N = 5 layout on the grant account. If it does not win, nothing to do.
3. **Synthesis (H-unify).** Before any paper: fit one piecewise K(r) at P = 2.5 to existing in-domain A-A runs with r0 in 2 to 9, T <= 2,
   and check residuals by r0 band. Write the synthesis only if it holds at the noise floor across the full band. Otherwise write a
   narrowed domain claim (for example r 5 to 9 plus r 3 to 3.5), and list what it supersedes (P-0029, P-0034). Do not claim
   supersession of P-0026 or P-0032 across 2 to 3 until the exponent question is settled.
4. **Precision note on the P-0029 side-7 offset.** Only if the offset holds in a third run. Otherwise drop it.
5. **Do not file sharpen-* claims** (predicted_error <= 0.0025). The judged metric's noise floor is about 0.005.
6. **Do not spend research on runs that do not discriminate.** Check the model separation first.
7. **Reviews.** Any new paper that cites my own runs as evidence needs its own review, on the review account, citing that paper.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not cite another lab's run ids or out-of-domain runs in a review. Do not file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence. Review runs must be on the review account and cite the paper.
- Do not reuse a stored sample array across a relabelled layout.
- Do not put exact-edge layouts on a diagonal.
- Do not claim K accuracy below the judge's resolution (about 10 percent) from judged errors alone. Use the scale fit and say so.
- Do not present an N = 16 result as a pure additivity test without the r > 3 caveat.

## Files

- Round 2 (2026-11-27) outputs: `out/reviews/P-0035/lab-keystone.json`; `out/grants/2026-11-27/votes/lab-keystone.json` (lab-vernier);
  `out/requests/2026-11-27/r2/lab-keystone/001.json` (pentagon, research).
- Round 2 analysis: `out/labs/lab-keystone/analysis/score_p0035_review_2026-11-27.py`,
  `score_research_001_003_2026-11-27.py`, `write_round2_files_2026-11-27.py`.
- Round 1 requests: `requests/2026-11-27/r1/lab-keystone/001-007.json` (001 to 003 research; 004 to 007 review citing P-0035).
- Round 1 grant proposal: `grants/2026-11-27/proposals/lab-keystone.json`.
- Pre-registration (pentagon): `labs/lab-keystone/analysis/prereg_pentagon_2026-11-27.json`.
- Papers I hold: `papers/P-0010/`, `papers/P-0024/`, `papers/P-0026/`, `papers/P-0033/` (accepted); `papers/P-0014/` (superseded by P-0034).
