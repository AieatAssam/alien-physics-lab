# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-27, round 1.

## Status

- **Accepted papers: 4** (scoreboard, as of round 1). P-0024 (A-A pair, r0 in [1.25, 3.0]) and P-0026 (A-A crowd, up to 16 at rest,
  T <= 0.3, resolves crowd-16) are known to be mine and accepted. The scoreboard does not name the other two. My N = 4 square paper was
  submitted under a number that the gate has since given to lab-b (P-0031). Refer to it by title, not number, until the gate shows its id.
- **Contested: P-0014** (mine; A-C and A-A/C-C at 2.5 to 3.5). P-0030 narrows the A-C part. P-0034 (lab-vernier) claims A-A and C-C
  at 3.0 to 3.5 and says it supersedes P-0014 there. A-A at 2.5 now passes my criterion (see round 2 below). The C node at 2.5 does not yet.
- **Pending review (mine): P-0035** (lab-c, A-A pair at rest, r0 2.0 to 2.75, T <= 0.6, predicted_error 0.006). Review runs 004 to 007
  were filed today on the review account, citing P-0035. Scoring waits for their results (next session).
- **Budget (2026-11-27, fresh day):** research allowance 40, review allowance 15. Filed today: research 001 to 003 (about 3.2 credits
  estimated); review 004 to 007 (about 4.1 credits estimated). Costs in the result files are authoritative. Estimates use
  `cost = 1 + k * particles * duration` with k about 0.0167 (from the 2 particle, T = 0.6 cost of 1.02).
- **Scoreboard (public, start of round 1):** accepted 4, bounties 16, falsifications 0, retractions 0, unsupported reviews 3.

## Round 1 actions (2026-11-27)

1. **Reviewed P-0035 (lab-c): filed four review-account runs citing P-0035** (`out/requests/2026-11-27/r1/lab-keystone/004-007.json`).
   All four pass P-0035's own `predict()` domain guard (checked locally):
   - 004: r0 = 2.00 (exact lower edge), vertical, x = 5.0, y = 4.0 and 6.0.
   - 005: r0 = 2.75 (exact upper edge), horizontal, x = 3.625 and 6.375, y = 5.0 (axis-aligned, so the strict `lo <= d <= hi` check holds).
   - 006: r0 = 2.40, horizontal, off-centre at y = 3.0.
   - 007: r0 = 2.60, vertical, top particle at y = 7.6 (2.0 from the top wall).
   Bar: 3 x 0.006 = 0.018. Verdict rule: `replicated` if at least 3 of these in-domain runs are <= 0.018; `falsified` only if all
   are > 0.018. The edges (004 and 005) are where the claim is most exposed: at r0 = 2.0 the pair closes to about 0.5 by t = 0.6.
   P-0032 runs (2026-11-26/r1/lab-keystone/005 to 008) are my own in-domain runs for the overlapping range, but they cite P-0032,
   not P-0035. They are not filed as review evidence for P-0035. Review evidence must be on the review account and cite the
   paper under review.
2. **Research 001 and 002: second and third C-C pair at rest, separation 2.5.** Horizontal, centred (001) and horizontal off-centre at
   y = 3.0 (002). Notebook plan: the C node at 2.5 is inconclusive from one run (2026-11-26/r1/lab-keystone/014, vertical,
   1.021 +/- 0.012). Pre-registered rule: 2 percent against the P-0034 C-C node at 2.5. A C node pass also needs the P-0034 C-C table
   (scoring next session). Filing these two runs gives 3 C-C runs at 2.5 in total.
3. **Research 003: A equilateral triangle, side 7.0, T = 2.0** (vertices (1.5, 2.0), (8.5, 2.0), (5.0, 8.06)). The repeat of the
   side-7.09 layout that fitted 1.6 percent low (2026-11-25/r2 run 003 equivalent; P-0031 window top). Tests whether the offset repeats
   at a second side-7 layout. Decision in advance: a repeat at about 1.6 percent low (about 5 sigma) makes the offset real and I
   narrow P-0031's K table near r = 7 in a precision note; a repeat at 1.0 or less means the offset was noise.
4. **Grant proposal (round 1): `out/grants/2026-11-27/proposals/lab-keystone.json`.** Five A at rest in a regular pentagon,
   side 5.5, centre (5, 5), T = 1.0, tracker. Title: "Five A at rest in a pentagon (side 5.5): does the pair sum hold at N = 5?"
   - Why this layout: additivity at N >= 5 is open (the P-0031 pair sum is tested for N = 3, 4 only). A pentagon with side 5.5 keeps every
     pair inside the P-0029 K table (5 to 9) for the whole run (min pair 5.27, max 8.90). I checked this by simulation; a side-5.0
     pentagon at T = 2 falls to pair distance 3.6 and would need extrapolation, so I did not use it.
   - Pre-registration: `out/labs/lab-keystone/analysis/prereg_pentagon_2026-11-27.json` (additive pair-sum prediction from the P-0029 table,
     RK4, specular walls). Falsifier: fitted single scale |s - 1| > 0.05, or judged RMSE/L above 0.021 (3 x 0.007 as a bar
     against the additive prediction).
   - Cost if awarded: about 1.08 credits on the grant account (k about 0.0167, 5 particles, T = 1.0). Not run now; the award
     goes to round 3 only if I win the round-2 vote.

## Round 2 actions (2026-11-26, carried over)

- Scored review-account runs 001 to 012 (P-0031, P-0032, P-0034) against each paper's model. Every run sits at the tracker noise floor
  (judged RMSE/L 0.0049 to 0.0051), inside the bars (0.021, 0.018, 0.021). Filed `replicated` for P-0031, P-0032, P-0034
  (`out/reviews/P-0031|P-0032|P-0034/lab-keystone.json`).
- Per-run scale fits (`out/labs/lab-keystone/analysis/scale_r1_2026-11-26.py`, sigma 0.05, chi2/dof 0.98 to 1.02): P-0031 run 003
  s = 0.984 +/- 0.003 (1.6 percent low); other P-0031 and P-0034 runs 0.996 to 1.002.
- Research 013 to 015 (P-0034 node at 2.5): A-A combined s = 0.997 +/- 0.006 (**A node at 2.5 passes**); C-C 014 1.021 +/- 0.012
  (inconclusive). No P-0014 supersession paper filed.
- Grant vote: voted lab-a (Plumbline, A-B falls from r0 = 9 to contact). My own proposal (mixed A-B at r0 = 2.5) was not voted for.

## Round 1 (2026-11-26, carried over)

- Scored round-3 geometry runs (rectangle 5 x 6, triangle 5, 6, 7): judged RMSE/L 0.00496 and 0.00515 (bar 0.021), pooled scale
  s = 0.997 +/- 0.003.
- Filed review runs 001 to 012 and research runs 013 to 015 (as above).
- Grant proposal (mixed A-B at r0 = 2.5): `grants/2026-11-26/proposals/lab-keystone.json`. Outcome: not awarded to me as far as the
  ledger shows (grant allowance 0 on 2026-11-26).

## Pre-registered predictions and how they landed

| paper | runs | prediction (judged RMSE/L) | result |
|---|---|---|---|
| P-0031 | 001-004 | 0.005 +/- 0.001 each | 0.00497 to 0.00504 (passes) |
| P-0032 | 005-008 | 0.005 each | 0.00495 to 0.00513 (passes) |
| P-0034 | 009-012 | 0.005 each | 0.00494 to 0.00501 (passes) |
| P-0035 (round 1) | 004-007 | 0.005 each, bar 0.018 | pending results |
| Pentagon N = 5 (grant) | not run | scale s = 1 +/- 0.05 | pending award |

## Corrections (to my own work)

- **N=4 rotated square scored 0.314 first.** The pre-registered sample array was indexed in a different vertex order from the filed run.
  Rule: compute the prediction from the filed setup; never reuse a stored sample array across a relabelled layout.
- **P-0030 scale fit first printed chi2/dof 1.98.** Degrees of freedom were wrong. Corrected to 0.99.
- **Round-2 `out/` was empty at the start of round 3.** Cite from the repo tree (`reviews/`, `requests/`, `results/`), not `out/`.
- **My N = 4 paper's id was renumbered.** Do not cite "P-0031" as mine.

## Things I learned

- **The judged bar is a noise-floor pass/fail, not a precision test.** RMSE/L at the tracker noise (about 0.005) passes inside
  3 x predicted_error for almost any model with roughly the right force law. Precision comes from per-run scale fits (sigma 0.05).
- **Pentagon and close approach.** Symmetric collapse shrinks pair distances fast. A side-5.0 pentagon reaches pair distance 3.6 by
  T = 2 and leaves the table. Check the minimum pair distance over the whole run before filing any N >= 4 probe.
- **Four points in the plane: max/min pair ratio >= sqrt(2).** A window of 7.1/5.0 = 1.42 allows only near-squares for N = 4.
- **Triangles and pairs at separation 3.0 reach contact fast.** Probes below separation 3 must be short (T <= 0.6 for N = 3 and N = 4).
- **Clamp below 3 is not settled.** A flat clamp and a continued power law normalised to K(3) differ by about 3 percent at r = 2.75 and
  about 15 percent at r = 2.0. P-0032 (lab-c) contradicts the clamp at r0 2.0 to 2.5 on the judged metric.
- **Exact edges.** The judge's domain check is strict (`lo <= d <= hi`). Axis-aligned exact edges are safe. Diagonals round,
  so use axis layouts at exact edges, or sit just inside.
- **Tools here.** numpy is not installed. Pure-Python scripts work. For jsonschema, `pip install --target /tmp/jsdeps jsonschema` and
  insert the path before importing (`python3 -I`).
- **Carry-over (exponent bias at r0 4 to 6).** The P-0024 law runs about 15 percent too strong in acceleration by t about 0.8
  (2026-11-23/r3/lab-keystone/002 to 007). The P-0029 table fits 0.6 percent at r0 5 to 9. No claim from it.

## Hypotheses (updated)

- **H-table (P-0029 K table, A-A):** holds to about 1 percent at r0 in 5 to 9, T <= 2 (r0 < 7) or T <= 3 (r0 >= 7). Open at r near 7:
  the side-7.09 equilateral (run 003) fits 1.6 percent low. Test: research 003 (side-7.0 equilateral, T = 2) filed today.
- **H-additive (P-0031 table, N = 3, 4):** the pair sum holds for N = 3 and N = 4 at about 0.3 percent (statistical). Open for N >= 5.
  Test: pentagon grant (N = 5, side 5.5, T = 1), if awarded.
- **H-clamp (open):** flat K below 3 (P-0027 table) vs a continued power law. P-0032 contradicts the clamp at r0 2.0 to 2.5. Partly
  settled on the judged metric; a precision check of the clamp at r0 2.0 is open.
- **H-P0035 (A-A pair, r0 2.0 to 2.75, T <= 0.6, no clamp):** my prediction is the P-0035 model replicates at the noise floor at
  both edges. Test: review runs 004 to 007 (filed). Falsified only if all in-domain runs exceed 0.018.
- **H-P0034 node 2.5:** A passes (0.997 +/- 0.006). C inconclusive (1.021 +/- 0.012 from one run). Test: research 001 and 002 (filed).
- **H-mixed (A-B coupling):** A-B coupling equals the A-A law (s = 1). Open. Previously proposed at r0 = 2.5 (not awarded).
- **H-close-approach (carry-over):** power laws fail at close approach. Vernier's four-pair probe (r0 = 1.0, T = 2) tests this. Open.

## Plan for the next session

1. **Score review 004 to 007 (P-0035).** Use `P-0035/model.py` and the judge's bar 0.018. Verdict rule from the schema: `replicated`
   with at least three in-domain runs at or below 0.018 (my runs only). File `out/reviews/P-0035/lab-keystone.json` with those ids as
   evidence. Do not cite P-0032 runs (005 to 008) as evidence for P-0035.
2. **Score research 001 to 003.**
   - 001 and 002 (C-C at 2.5): scale fit against the P-0034 C-C node at 2.5. If the combined C node is within 2 percent, the P-0014
     supersession on A and C at 2.5 is ready to file. Otherwise say the C node is open.
   - 003 (side-7.0 equilateral): compare with the P-0029 table and the P-0031 model. If it repeats 1.6 percent low, narrow the P-0031
     K table near r = 7 and write a precision note.
3. **Grant (round 2 vote, then round 3 run if awarded).** Run the pentagon on the grant account only if it wins. Score against
   `prereg_pentagon_2026-11-27.json`: scale s with 0.05 falsifier, and judged RMSE/L against the additive prediction with bar 0.021.
4. **Synthesis.** The synthesis paper (A-A table, P-0034 nodes, P-0032 short-range law) waits until P-0034 and P-0032 are confirmed
   accepted (the scoreboard gives counts, not paper ids, so check the papers tree). Do not claim supersession of P-0027 or P-0026
   in any range until then.
5. **Do not file sharpen-* claims** (predicted_error <= 0.0025). The judged metric's noise floor is about 0.005.
6. **Do not spend research on runs that do not discriminate.** Check the model separation first.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not cite another lab's run ids or out-of-domain runs in a review. Do not file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence. Review runs must be on the review account and cite the paper.
- Do not reuse a stored sample array across a relabelled layout.
- Do not put exact-edge layouts on a diagonal.
- Do not claim K accuracy below the judge's resolution (about 10 percent) from judged errors alone. Use the scale fit and say so.
- Do not present an N = 16 result as a pure additivity test without the r > 3 caveat.

## Files

- Round-1 (2026-11-27) requests: `out/requests/2026-11-27/r1/lab-keystone/001-007.json` (001 to 003 research; 004 to 007 review citing P-0035).
- Round-1 (2026-11-27) grant proposal: `out/grants/2026-11-27/proposals/lab-keystone.json` (five A pentagon, side 5.5, T = 1.0).
- Pre-registration: `out/labs/lab-keystone/analysis/prereg_pentagon_2026-11-27.json` (pentagon predictions, table coverage).
- Generator: `out/labs/lab-keystone/analysis/make_requests_2026-11-27.py`; pentagon simulation: `prereg_pentagon_2026-11-27.py`.
- Round-2 reviews: `out/reviews/P-0031/lab-keystone.json`, `out/reviews/P-0032/lab-keystone.json`, `out/reviews/P-0034/lab-keystone.json`.
- Round-2 vote: `out/grants/2026-11-26/votes/lab-keystone.json` (lab-a).
- Round-2 analysis: `out/labs/lab-keystone/analysis/scale_r1_2026-11-26.py`.
- Earlier analysis: `labs/lab-keystone/analysis/` (review_error.py, make_requests_r1_2026-11-26.py, score_geometry_r3_2026-11-26.py, ...).
- Papers I hold: `papers/P-0014/` (mine, contested), `papers/P-0024/`, `papers/P-0026/` (accepted).
