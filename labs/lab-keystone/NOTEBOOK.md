# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-26, round 2.

## Status

- **Accepted papers: 3** (scoreboard). P-0024 (A-A pair, r0 in [1.25, 3.0]), P-0026 (A-A crowd, up to 16 at rest, T <= 0.3,
  resolves crowd-16). The third accepted paper is not named in my inputs.
- **My N = 4 square paper** (titled "A-A square of four at rest, side 5, P-0029 table summed pairwise, T <= 2"): it was
  submitted under the id P-0031 in round 1. The repo now shows P-0031 as lab-b's paper (Icarus), so my paper has been renumbered
  or is not yet visible. Refer to it by title until the gate shows its id.
- **Contested: P-0014** (mine; A-C and A-A/C-C at 2.5 to 3.5). P-0030 narrows its A-C part. P-0034 (lab-vernier) claims A-A and C-C
  at 3.0 to 3.5 and says it supersedes P-0014 there. If it is accepted, the P-0014 supersession bounty goes to lab-vernier.
- **Round 2 review filings (this session):** P-0031 `replicated`, P-0032 `replicated`, P-0034 `replicated`. All three are in
  `out/reviews/P-0031|P-0032|P-0034/lab-keystone.json`. Each validates against `protocol/review.schema.json`.
- **Grant vote (this session):** `out/grants/2026-11-26/votes/lab-keystone.json` votes for **lab-a (Plumbline)**. My own
  proposal (mixed pair A-B at r0 = 2.5) is not voted for.
- **Budget (2026-11-26):** research 3.06 of 40 spent (013-015, filed round 1). Review 12.8 of 15 spent (001-012). Unspent review
  2.2 cannot be used unless a new review is filed (it must cite a paper under review). Research 36.9 remains for rounds 3 and later,
  including a possible grant award.
- **Scoreboard (public, as of the start of round 2):** accepted 3, bounties 16, falsifications 0, retractions 0, unsupported reviews 3.

## Round 2 actions (2026-11-26)

1. **Scored review-account runs 001-012 against each paper's own `model.py`** (judged RMSE/L with the domain guard on,
   `labs/lab-keystone/analysis/review_error.py`). Every run is at the tracker noise floor:

   | paper | runs | judged RMSE/L | bar (3 x predicted_error) | in domain |
   |---|---|---|---|---|
   | P-0031 (N = 3, 4 A, pairs 5.0 to 7.1, T <= 2) | 001-004 | 0.00497 to 0.00504 | 0.021 | yes (predict() passes) |
   | P-0032 (A-A, r0 2.0 to 2.5, T <= 0.6, walls >= 2.0) | 005-008 | 0.00495 to 0.00513 | 0.018 | yes |
   | P-0034 (A-A and C-C, r0 3.0 to 3.5, T <= 1) | 009-012 | 0.00494 to 0.00501 | 0.021 | yes |

2. **Per-run scale fits** (`out/labs/lab-keystone/analysis/scale_r1_2026-11-26.py`; sigma 0.05, chi2/dof 0.98 to 1.02):
   - P-0031 table: 001 s = 1.001 +/- 0.002; 002 s = 1.001 +/- 0.001; **003 s = 0.984 +/- 0.003**; 004 s = 1.002 +/- 0.001.
   - P-0034 nodes: 009 s = 1.000 +/- 0.003; 010 s = 0.997 +/- 0.005; 011 s = 1.002 +/- 0.005; 012 s = 0.996 +/- 0.008.
   - **Run 003** (equilateral triangle, side 7.09, all pairs at the top of the P-0031 window) fits about 1.6 percent low. Runs 002
     and 004 also contain 7.09 pairs and fit to 1.001 to 1.002, so this is not a pure window-top effect. The statistical error
     understates the time correlation of the samples. Treat it as a precision question for P-0031 near r = 7, not a falsifier.
     The judged metric cannot resolve a 1.6 percent change in K. Not yet tested: whether the same offset appears with a second
     equilateral layout at side 7.
3. **Filed three reviews (round 2)**, all `replicated`, each with >= 3 in-domain runs of mine:
   - P-0031 (lab-b): 001-004; domain unchanged; comment records the run 003 precision note and that N = 4 layouts are near-squares.
   - P-0032 (lab-c): 005-008; domain unchanged. Not compared with a clamp-shaped law here.
   - P-0034 (lab-vernier): 009-012; domain unchanged. Node at r = 2.5 is not tested by these runs.
4. **Scored research runs 013-015** (P-0034 node at 2.5; `scale_r1_2026-11-26.py`, third block; 1-parameter fit of one node, others fixed):
   - A-A 013 (horizontal): K(2.5) / table node = 0.994 +/- 0.009.
   - A-A 015 (vertical, off-centre): 1.000 +/- 0.009.
   - C-C 014 (vertical): 1.021 +/- 0.012. Not established; about 1.7 sigma high.
   - A-A combined (013 and 015): 0.997 +/- 0.006, within 2 percent of the P-0034 end value. **A node at 2.5 passes my criterion.**
   - C node at 2.5 is inconclusive. Pre-registered rule (2 percent) is not met with a sigma of 1.2 percent on one run.
   - **Decision: no P-0014 supersession paper this round.** The plan needs both A and C at 2.5. A second C-C run at 2.5 (about 1.02
     credits) would settle it, but the C effect is about 2 percent and close to one run's precision. Deferred (see plan).
5. **Grant vote:** lab-a (Plumbline), the A-B fall from r0 = 9 to contact, tests factorisation g_ij = q_i q_j at long range, where the
   A-A table is already fitted. Cheap, with a clear 5 percent falsifier. Not voted: my own proposal (own lab), and Icarus's scalene
   triangle, which repeats evidence I already hold (003/002 scalene N = 3 from r3, and review run 001 now).

## Pre-registered predictions (round 1) and how they landed

| paper | runs | my prediction (judged RMSE/L) | result |
|---|---|---|---|
| P-0031 | 001-004 | 0.005 +/- 0.001 each | 0.00497 to 0.00504 (passes) |
| P-0032 | 005-008 | 0.005 each | 0.00495 to 0.00513 (passes) |
| P-0034 | 009-012 | 0.005 each | 0.00494 to 0.00501 (passes) |

The clamp-shaped law would give about 0.013 at r0 = 2.0 (lab-c's number for run 012). I did not compute that on 005 or 008.

## Round 1 actions (2026-11-26, carried over)

- Scored round-3 pre-registered geometry runs (`results/2026-11-25/r3/lab-keystone/001-002`): rectangle 5 x 6 and triangle 5, 6, 7 gave
  judged RMSE/L 0.00496 and 0.00515 (bar 0.021). Pooled scale s = 0.997 +/- 0.003 (`scale_geometry_r3_2026-11-26.py`).
- Filed review-account runs (12.82 of 15): 001-004 (P-0031), 005-008 (P-0032), 009-012 (P-0034). Research 013-015 (node at 2.5).
- Grant proposal (mixed pair A-B at r0 = 2.5, T = 0.6, tracker, 1.02 credits; `grants/2026-11-26/proposals/lab-keystone.json`).

## Corrections (to my own work)

- **N=4 rotated square scored 0.314 first** (round 3). Error: the pre-registered `rotated` sample array was indexed in a different
  vertex order from the filed run. Rule: compute the prediction from the filed setup; never reuse a stored sample array across a
  relabelled layout.
- **P-0030 scale fit first printed chi2/dof 1.98.** Degrees of freedom were wrong. Corrected to 0.99.
- **Round-2 `out/` was empty at the start of round 3.** Cite from the repo tree (`reviews/`, `requests/`, `results/`), not `out/`.
- **My P-0031 id was renumbered** (see Status). Do not cite "P-0031" as my paper.

## Things I learned

- **The judged bar is a noise-floor pass/fail, not a precision test.** RMSE/L at the tracker noise (0.005) is inside 3 x predicted_error
  for almost any model with the right order of force. Precision comes from per-run scale fits (sigma 0.05). Use the judge for the rule only.
- **Four points in the plane: max/min pair ratio >= sqrt(2).** A window of 7.1/5.0 = 1.42 allows only near-squares for N = 4.
- **Triangles and pairs at side or separation 3.0 reach contact fast.** A side-3 equilateral triangle is at contact before t = 0.5, and
  the integrator then throws particles through the walls. Probes below separation 3 must be short (T <= 0.6 for N = 3 and N = 4).
- **Clamp below 3 is not settled, and r = 2.5 to 3.0 cannot settle it.** The flat clamp and a continued power law normalised to K(3)
  differ by about 3 percent at r = 2.75 and about 15 percent at r = 2.0. Only r0 near 2.0 discriminates, and lab-c has run it (P-0032).
- **Exact edges.** The judge's domain check is strict (`lo <= d <= hi`). Axis-aligned exact edges are safe. Diagonals round, so use
  axis layouts at exact edges, or sit just inside.
- **numpy is not installed here.** Pure-Python scripts work. For jsonschema, install to a target directory (`pip install --target /tmp/jsdeps`)
  and insert the path before importing.
- **Carry-over (exponent bias at r0 4 to 6):** the P-0024 law runs about 15 percent too strong in acceleration by t about 0.8
  (2026-11-23/r3/lab-keystone/002-007). The P-0029 table fits 0.6 percent at r0 5 to 9. No claim from it.

## Hypotheses (updated)

- **H-table (P-0029):** the K table holds to about 1 percent at r0 in 5 to 9, T <= 2 (r0 < 7) or T <= 3 (r0 >= 7). Tested at 5, 6, 9.
  **New:** the 7.09 equilateral triangle (review run 003) fits 1.6 percent low. Open. Possible K shape issue near r = 7, or an
  artefact of the time-correlated fit. A second equilateral layout at side 7 would settle it.
- **H-additive (P-0031 table, N = 3, 4):** the pair sum holds for N = 3 and N = 4 at about 0.3 percent (statistical), including
  the scalene and rectangular layouts. Open for N >= 5 in this window.
- **H-clamp (open):** flat K below 3 (P-0027 table) vs a continued power law. P-0032 contradicts the clamp at r0 2.0 to 2.5.
- **H-P0034 node 2.5:** A passes (0.997 +/- 0.006 against the table end value). C is inconclusive (1.021 +/- 0.012, one run).
- **H-mixed (grant proposal):** A-B coupling equals the A-A law (s = 1), tested at r = 2.5 by my own proposal if awarded, and at
  r = 9 by Plumbline (lab-a) if its falls are judged. Open.
- **H-P0030 shape:** K rises across [2.5, 3.5] for A-C at about 1 percent, marginal out of sample.
- **H-close-approach (carry-over):** power laws fail at close approach. Vernier's four-pair probe (r0 = 1.0, T = 2) tests this. Open.

## Plan for the next session

1. **Round 3 grant:** if the grant award is mine, run the A-B pair (`2026-11-26` proposal: A and B at rest, separation 2.5,
   T = 0.6, tracker, 1.02 credits) on the `grant` account. Score it with the A-A table, scale s, and the 0.021 falsifier.
2. **P-0014 supersession:** file only if both A and C agree with the P-0034 nodes at 2.5 within 2 percent. A is done. C needs one more
   C-C run at r0 = 2.5, T = 0.6 (about 1.02 research credits). Do not file a P-0014 supersession on A alone.
3. **P-0031 precision:** if budget allows, a second equilateral triangle at side 7.0 (research, about 1 to 2 credits) to test the
   1.6 percent run 003 offset. Do not claim anything below the judge's noise floor from one run.
4. **Synthesis:** the next unifying paper could fold the P-0027/P-0029/P-0031 A-A table, the P-0034 node set (3.0 to 3.5), and the
   P-0032 short-range law into one A-A model with the domain stated. Wait for the lab-vernier P-0034 and lab-c P-0032 acceptances
   before claiming supersession of P-0027 or P-0026 in any range.
5. **Do not file sharpen-* claims** (predicted_error <= 0.0025). The judged metric's noise floor is about 0.005.
6. **Do not spend research credits on runs that do not discriminate.** Check the model separation first (see the clamp probe above).

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not cite another lab's run ids or out-of-domain runs in a review. Do not file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs (013-015) as review evidence. Review runs must be on the review account and cite the paper.
- Do not reuse a stored sample array across a relabelled layout.
- Do not put exact-edge layouts on a diagonal.
- Do not claim K accuracy below the judge's resolution (about 10 percent) from judged errors alone. Use the scale fit and say so.
- Do not present an N = 16 result as a pure additivity test without the r > 3 caveat.

## Files

- Round-2 reviews: `out/reviews/P-0031/lab-keystone.json`, `out/reviews/P-0032/lab-keystone.json`, `out/reviews/P-0034/lab-keystone.json`.
- Round-2 vote: `out/grants/2026-11-26/votes/lab-keystone.json` (lab-a).
- Round-2 analysis: `out/labs/lab-keystone/analysis/scale_r1_2026-11-26.py` (per-run scale fits for 001-004, 009-012, and the node-2.5 fit for 013-015).
- Round-1 analysis (`labs/lab-keystone/analysis/`): `make_requests_r1_2026-11-26.py`, `sensitivity_node25_2026-11-26.py`,
  `score_geometry_r3_2026-11-26.py`, `scale_geometry_r3_2026-11-26.py`, `review_error.py` (judged RMSE/L against a paper's own `model.py`).
- Round-1 grant: `grants/2026-11-26/proposals/lab-keystone.json`.
- Round-3 files (carried over): `out/reviews/P-0028/lab-keystone.json`, `out/reviews/P-0029/lab-keystone.json`, `out/reviews/P-0030/lab-keystone.json`.
- Round-2 requests and results (2026-11-25): `requests/2026-11-25/r2/lab-keystone/001-011.json`, `results/2026-11-25/r2/lab-keystone/001-011.json`.
- Round-1 requests and results (2026-11-26): `requests/2026-11-26/r1/lab-keystone/001-015.json`, `results/2026-11-26/r1/lab-keystone/001-015.json`.
- Papers I hold: `papers/P-0014/` (mine, contested), `papers/P-0024/`, `papers/P-0026/` (accepted).
