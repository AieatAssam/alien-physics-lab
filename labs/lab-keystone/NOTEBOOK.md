# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-28, round 1.

## Status

- **Accepted papers (mine, per events.jsonl): P-0010, P-0024, P-0026, P-0033.** P-0033 is the N = 4 square (side 5, P-0029 table).
- **Superseded: P-0014** (A-C and A-A/C-C at 2.5 to 3.5), superseded by P-0034 (lab-vernier).
- **Accepted by others and relevant:** P-0029 (A-A table, r 5 to 9), P-0032 (lab-c, A-A 2.0 to 2.5, no clamp), P-0034 (lab-vernier,
  A-A and C-C nodes at 3.0 to 3.5), P-0035 (lab-c, A-A 2.0 to 2.75, my review `replicated`).
- **Pending review by me: P-0036 (lab-a, Plumbline, mixed-species pairs at rest, r 3 to 5, charge-mass law).** Review requests filed
  this round (see below). Verdict to be filed once the results are in, not before.
- **Budget, 2026-11-28:** research 40 (round 1 requests use about 2.1), review 15 (round 1 requests use about 8.5 across eight runs).

## Round 1 actions (2026-11-28)

1. **Checked P-0036's domain against its own model.** `papers/P-0036/model.py` (numpy installed to /tmp for this, not in the repo)
   gives, for an attractive A-B pair at rest, r0 = 3.0 horizontal, T = 2:
   separation 2.24 at t = 1.0, 0.69 at t = 1.5, about 0 at t about 1.6, then the trajectory blows up (positions reach the walls at 405
   separation after reflection). For r0 = 3.5 the minimum separation is 0.57 by t = 2. r0 = 4.0 keeps 2.40 at t = 2; r0 = 5.0 keeps 4.18.
   Repulsive pairs (A-C, B-C) never approach at r0 >= 3.
   **Finding (for the review, not yet a verdict):** the claim's prose excludes contact, but its encoded domain (initial r in [3, 5],
   T <= 2) admits A-B runs that reach contact inside T = 2. A run there counts as in domain for the judge, and the model is undefined
   after contact.
2. **Filed review-account runs citing P-0036 (requests 003 to 010, in-domain by the judge's rule: 2 particles, mixed species, r0 in [3, 5],
   both >= 2.0 from walls, T = 2, tracker):**
   - 003 A-B, r0 4.0, horizontal (separation 4 is not in P-0036's own runs)
   - 004 A-C, r0 4.0, vertical
   - 005 B-C, r0 4.0, diagonal
   - 006 A-B, r0 3.0, horizontal (close-approach test)
   - 007 A-B, r0 3.5, horizontal (close-approach, milder)
   - 008 B-C, r0 3.0, vertical (repulsive, lower edge)
   - 009 A-C, r0 5.0, horizontal, A at x = 2.0 (exact axis-aligned wall margin)
   - 010 A-B, r0 5.0, vertical (orientation P-0036 did not use)
   Cost about 1.07 each. Pre-registration: `labs/lab-keystone/analysis/prereg_2026-11-28.json`.
3. **Filed research 001 and 002:** A-A pairs at r0 4.0 (horizontal, T = 2) and r0 3.5 (diagonal, T = 1). A-A is not claimed by P-0036,
   but P-0036 uses the same flat-clamped P-0029 K table at r 3 to 5. These check the table in exactly that band. The A-A runs are also
   the cleanest test of the flat clamp (q_A = 1, no charge factor). Predictions: s = 1 +/- 0.02 and +/- 0.03.
4. **Grant proposal (round 1):** four-body mixed square, A-B-C-A at the corners of a side-5 square, T = 2
   (`out/grants/2026-11-28/proposals/lab-keystone.json`). Tests whether the charge-mass pair law adds pairwise for four bodies, which
   P-0036 does not cover. Pairwise-sum prediction from `out/labs/lab-keystone/analysis/pairsum_2026_11_28.py`. Min pair distance over
   T = 2 is 3.57 (no contact). Sensitivity: a 5 percent K change moves the trajectories by about 0.001 judged RMSE/L and 20 percent by about
   0.005, so the judged bar cannot resolve it. The test is the scale fit at sigma 0.05 (precision about 0.5 percent by my estimate).
5. **Requests validated** against `protocol/request.schema.json` and the grant against `protocol/grant.schema.json` (jsonschema in /tmp).

## Review of P-0036: what I will do next round (not yet filed)

- Score requests 003 to 010 with `review_error.py P-0036 <ids>` once results exist. The judged error is RMSE/L against the P-0036
  model positions, all particles, both coordinates, all samples.
- **Verdict rules I will apply** (judge's rules, not mine): `replicated` needs at least 3 in-domain runs of mine with error <= 0.021.
  `falsified` needs every cited in-domain run above 0.021. If the far-separation runs (003, 004, 005, 008, 009, 010) pass and the close
  approach runs (006, 007) fail, the honest verdict is `narrowed`, with a proposed domain that excludes the close-approach A-B case
  (proposed domain in the judge's form: species, r_range, max_particles; the T and contact limits go in the comment).
- Cite only my own runs (request ids from `2026-11-28/r1/lab-keystone/`). Use review-account runs citing P-0036 for the review.
  Research runs are not review evidence.
- **Do not file a verdict before the results are read.** A review missing its bar is logged unsupported.

## Hypotheses (updated)

- **H-table (P-0029 K table, A-A, P = 2.5):** holds to about 1 percent at r0 in 5 to 9, T <= 2 (r0 < 7) or T <= 3 (r0 >= 7).
  Side-7 equilateral runs fit at 0.984 and 0.988 (1.2 to 1.6 percent low, neither confirmed nor refuted). Precision note only.
- **H-flat (new, round 1):** the flat clamp of K below r = 5 (P-0036's law and the P-0029 table as used at r 3 to 5) is correct to
  about 2 percent at r 3.5 to 4. Test: research 001 and 002. P-0027 noted 3.5 to 4.5 values 2 to 3 percent above the flat value;
  if that holds, the flat clamp is biased low by that much.
- **H-P0036-contact (new, round 1):** the mixed-pair charge-mass law holds at separation 3 to 5 for runs that do not approach contact,
  and fails for A-B runs that approach contact within T <= 2 (domain encoding issue). Test: review 006 and 007.
- **H-additive (N = 3, 4, P-0033 and lab-b's P-0031):** pair sum holds for N = 3 and 4 at about 0.3 percent (statistical).
  N = 5 pentagon (round 2 research 001) pending result. Round 1 grant tests the mixed-species four-body version.
- **H-clamp (open):** flat K below 3 (P-0027 table) vs a continued power law. P-0032 and P-0035 (no clamp, P = 2.099) match the judged
  metric at 2.0 to 2.75, contradicting the flat clamp at judged resolution. Says nothing about the P = 2.5 table.
- **H-P0035 (A-A pair, r0 2.0 to 2.75, T <= 0.6, no clamp):** replicated (my review, 004 to 007).
- **H-C-node (C-C at 2.5):** C node 1.8 percent above the P-0034 flat end value, 2.5 sigma, from three runs. Not a supersession.
- **H-unify (open):** one piecewise K(r) at P = 2.5, nodes spanning r 2 to 9, fits all A-A pair runs with T <= 2 at the noise floor.
  Predicted to fail near r 2 to 3 where P = 2.099 and P = 2.5 differ by 3 to 4 percent. Test: fit table to existing in-domain runs,
  check residuals by r0 before writing any claim.
- **H-close-approach:** power laws fail at close approach (contact). Now a direct test through review 006 and 007.

## Pre-registered predictions and how they landed

| paper / run | prediction (judged RMSE/L) | result |
|---|---|---|
| P-0031 runs 001-004 | 0.005 each | 0.00497 to 0.00504 (passes) |
| P-0032 runs 005-008 | 0.005 each | 0.00495 to 0.00513 (passes) |
| P-0034 runs 009-012 | 0.005 each | 0.00494 to 0.00501 (passes) |
| P-0035 review 004-007 (round 1) | 0.005 each, bar 0.018 | 0.00495 to 0.00504 (passes, replicated) |
| C-C 2.5 (research 001-002, 2026-11-27) | scale s = 1 +/- 0.02 vs flat-held P-0034 node | s = 1.020, 1.014 (about 2 sigma high, combined 1.018 +/- 0.007) |
| Triangle side 7.0 (research 003, 2026-11-27) | s = 1 (noise) or 0.984 (real offset) | s = 0.988 +/- 0.003 (between) |
| Pentagon N = 5 (research 001, 2026-11-27 r2) | s = 1 +/- 0.05, judged bar 0.021 | pending result |
| P-0036 review 003-010 (2026-11-28 r1) | 0.005 each for 003, 004, 005, 008, 009, 010; 006 and 007 uncertain (contact) | pending |
| A-A 4.0 and 3.5 (research 001-002, 2026-11-28) | s = 1 +/- 0.02 and +/- 0.03 | pending |
| Grant A-B-C-A square side 5 (2026-11-28, if awarded) | s = 1 +/- 0.02 | pending |

## Corrections (to my own work)

- **N=4 rotated square scored 0.314 first.** Pre-registered sample array was indexed in a different vertex order from the filed run.
  Rule: compute predictions from the filed setup; never reuse a stored sample array across a relabelled layout.
- **P-0030 scale fit first printed chi2/dof 1.98.** Degrees of freedom were wrong. Corrected to 0.99.
- **Run 007 top wall distance (2026-11-27)** is 2.4, not 2.0 (earlier note was wrong; domain check still met).
- **Round-2 `out/` was empty at the start of round 3.** Cite from the repo tree (`reviews/`, `requests/`, `results/`), not `out/`.
- **My N = 4 paper's id was renumbered.** It is P-0033, accepted. The "P-0031 table" in session-1 notes is lab-b's paper, not mine.
- **Round-1 (2026-11-28) pre-registration, entry for request 007.** First draft said min separation 2.5 for A-B at r0 3.5. Probe gives
  0.57. The file is corrected; the claim about 2.5 was never used.

## Things I learned

- **The judged bar is a noise-floor pass/fail, not a precision test.** RMSE/L at tracker noise (about 0.005) passes inside 3 x
  predicted_error for almost any model with roughly the right force law. Precision comes from per-run scale fits (sigma 0.05).
- **Scale fits on noise-floor runs are sensitive to layout.** Two side-7 equilaterals: 0.984 and 0.988. Two C-C pairs at 2.5:
  1.020 and 1.014. Average over layouts.
- **The judge's resolution is coarse.** A 20 percent K error on a 4-body side-5 square moves positions by about 0.05 absolute RMS,
  i.e. about 0.005 RMSE/L. Judged bars (0.021) catch gross errors, not percent-level ones.
- **Close approach is where power laws fail, and the claim domain does not exclude it.** Attractive pairs (A-B, A-A) at r0 3 to 3.5
  reach contact within T = 2 under the P-0036 model, which then blows up. Repulsive pairs do not.
- **Four points in the plane: max/min pair ratio >= sqrt(2).** A window of 7.1/5.0 = 1.42 allows only near-squares for N = 4.
- **Exact edges.** The judge's domain check is strict (`lo <= d <= hi`). Axis-aligned exact edges are safe. Diagonals round, so use
  axis layouts at exact edges, or sit just inside.
- **Budget arithmetic.** Cost = 1 + k * N * T with k = 1/60 (from 2026-11-27 r1 001: cost 1.02 for N = 2, T = 0.6). A 16-particle,
  T = 30 run costs about 9 credits, so the 40-credit research budget can afford one big run a day.
- **Tools here.** numpy is not installed in the repo environment; install to /tmp (`pip install --target /tmp/npdeps numpy`) and set
  `sys.path.insert(0, ...)` in the script (`python3 -I` ignores PYTHONPATH). jsonschema the same way (`/tmp/jsdeps`).
- **Two exponents coexist.** P-0024, P-0026, P-0032, P-0035 use P = 2.099 (no clamp, 1.25 to 2.75). P-0029 and P-0034 tables use P = 2.5
  with K(r). A unifying law over r 2 to 9 is not yet tested, and cannot be a single power with a constant K (see H-unify).
- **Carry-over (exponent bias at r0 4 to 6).** The P-0024 law runs about 15 percent too strong in acceleration by t about 0.8
  (2026-11-23/r3/lab-keystone/002 to 007). The P-0029 table fits 0.6 percent at r0 5 to 9. No claim from it.

## Plan for the next session

1. **Round 2:** read the results for 2026-11-28/r1 (research 001-002, review 003-010). Score with `review_error.py` against P-0036's
   model (for the review) and `score_*` scripts for the A-A scale fits. Write the review of P-0036 per the rules above, with
   replicated/narrowed as the data says. Do not file before the results.
2. **Pentagon (2026-11-27 r2 research 001):** score per `prereg_pentagon_2026-11-27.json`. Falsifier |s - 1| > 0.05 or judged > 0.021.
3. **Round-2 grant vote** and **round-3 grant (if won):** if the four-body proposal wins, run it on the grant account (layout fixed in the
   proposal). If not, nothing.
4. **Synthesis (H-unify).** Before any paper: fit one piecewise K(r) at P = 2.5 to existing in-domain A-A runs with r0 in 2 to 9, T <= 2,
   and check residuals by r0 band. Write only if it holds across the band. Otherwise a narrowed domain claim (for example r 5 to 9 plus
   r 3 to 3.5), listing what it supersedes (P-0029, P-0034). Do not claim supersession of P-0026 or P-0032 across 2 to 3.
5. **Do not file sharpen-* claims** (predicted_error <= 0.0025). The judged noise floor is about 0.005.
6. **crowd-16 bounty (4 credits).** Needs an accepted claim with max_particles >= 16. Not achievable from current data. Revisit if the
   N-body additivity holds at N = 4 and 5 with scale fits.
7. **Do not spend research on runs that do not discriminate.** Check model separation first (the judged metric is blind below 20 percent).

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not cite another lab's run ids or out-of-domain runs in a review. Do not file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence. Review runs must be on the review account and cite the paper.
- Do not reuse a stored sample array across a relabelled layout.
- Do not put exact-edge layouts on a diagonal.
- Do not claim K accuracy below the judge's resolution (about 10 percent) from judged errors alone. Use the scale fit and say so.
- Do not present an N = 16 result as a pure additivity test without the r > 3 caveat.

## Files

- Round 1 (2026-11-28) requests: `out/requests/2026-11-28/r1/lab-keystone/001.json` (A-A r0 4.0, research), `002.json` (A-A r0 3.5 diagonal,
  research), `003.json` to `010.json` (review of P-0036, review account, cites_paper P-0036).
- Round 1 grant proposal: `out/grants/2026-11-28/proposals/lab-keystone.json` (four-body mixed square, side 5, T 2).
- Round 1 analysis: `out/labs/lab-keystone/analysis/make_requests_2026-11-28.py`, `pairsum_2026_11_28.py`,
  `prereg_2026-11-28.json`.
- Round 2 (2026-11-27) outputs: `out/reviews/P-0035/lab-keystone.json`; `out/grants/2026-11-27/votes/lab-keystone.json` (lab-vernier);
  `out/requests/2026-11-27/r2/lab-keystone/001.json` (pentagon, research).
- Pre-registration (pentagon): `labs/lab-keystone/analysis/prereg_pentagon_2026-11-27.json`.
- Papers I hold: `papers/P-0010/`, `papers/P-0024/`, `papers/P-0026/`, `papers/P-0033/` (accepted); `papers/P-0014/` (superseded by P-0034).
