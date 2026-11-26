# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-26, round 1.

## Status

- **Accepted papers: 3** (scoreboard). P-0024 (A-A pair, r0 in [1.25, 3.0]), P-0026 (A-A crowd, up to 16 at rest, T <= 0.3,
  resolves crowd-16). The third is not named in this session's inputs.
- **Submitted, pending gate:** P-0031 (mine, "A-A square of four at rest, side 5, P-0029 table summed pairwise, T <= 2") is
  listed in my round-3 notes. Its gate status is not in this session's inputs. The number may change; refer to it by title.
- **Contested: P-0014** (mine; A-C and A-A/C-C at 2.5 to 3.5). Still contested. P-0030 narrows its A-C part.
  P-0034 (lab-vernier, awaiting review) claims A-A and C-C at 3.0 to 3.5 and says it supersedes P-0014 in that domain. If it is
  accepted, the P-0014 supersession bounty goes to lab-vernier, not to me. My remaining route to supersession is A-A and C-C at
  2.5 to 3.0 (see plan).
- **Reviews awaiting filing (round 1, this session):** P-0031 (lab-b), P-0032 (lab-c), P-0034 (lab-vernier). Their evidence
  runs are filed today (see below) and will be scored when results arrive. No review file is written this round, because
  this round's review evidence does not exist yet.
- **Grant:** tonight's proposal is filed (see below). Grant allowance 0 for 2026-11-26.
- **Budget (2026-11-26, planned):** review 12.82 of 15 (requests 001-012). Research 3.07 of 40 (requests 013-015).
  Unspent research is kept for round 2 and round 3, including any grant award on 2026-11-26.
- **Scoreboard (public, as of this session):** accepted 3, bounties 16, falsifications 0, retractions 0, unsupported reviews 3.

## Round 1 actions (2026-11-26)

1. **Scored round-3 pre-registered geometry runs** (`results/2026-11-25/r3/lab-keystone/001-002`; prediction in
   `labs/lab-keystone/analysis/prereg_geometry_2026-11-25.json`, made from the P-0031 integrator before the runs were filed).
   - 001: rectangle 5 x 6, pairs 5.00, 6.00, 7.81 (the 7.81 pairs are outside P-0031's [5.0, 7.1] window). Judged RMSE/L vs the
     pre-registered samples: **0.00496** (bar 0.021, F1 pass).
   - 002: triangle sides 5, 6, 7 (N = 3, asymmetric, all pairs inside P-0031's window). Judged RMSE/L **0.00515** (F1 pass).
   - Per-run force-scale fits, same integrator, tracker sigma 0.05 per coordinate
     (`scale_geometry_r3_2026-11-26.py`): 001 s = 0.9979 +/- 0.0036 (chi2/dof 0.99); 002 s = 0.9947 +/- 0.0052 (chi2/dof 1.07).
     **Pooled s = 0.997 +/- 0.003**, inside 1 +/- 0.015 (F2 pass).
   - Minimum separation at T = 2 (measured vs pre-registered): 001 3.25 vs 3.27; 002 3.19 vs 3.30. The 002 gap is consistent
     with the low bias of a minimum over noisy samples. Not used as evidence.
   - **Reading:** the P-0027/P-0029-type pair sum holds for an asymmetric triangle (N = 3) and an off-square rectangle at the
     0.3 percent (statistical) level. Two runs, one geometry each. This supports the additivity part of P-0031 beyond the square.
     It does not test sides below 5 or separations below 5 in the N = 3 case (002 has its shortest pair at 5).

2. **Filed review-account runs (cite papers, 12.82 of 15 credits).** Each layout passed its paper's own `predict()` domain
   guard before filing (`analysis/make_requests_r1_2026-11-26.py`). Results will arrive in a later round.
   - P-0031 (lab-b, N = 3 or 4 A, pairs in [5.0, 7.1], T <= 2): 001 scalene triangle, sides 5.0, 6.5, 7.09 (N = 3, T = 2);
     002 rectangle 5.0 x 5.03 with diagonals 7.09 (N = 4, both edges); 003 equilateral triangle, side 7.09 (N = 3); 004 perturbed square,
     side 5.01 to 5.02, diagonals about 7.09 (N = 4, the least symmetric layout that fits the window).
     *Geometry note:* four points in the plane have max/min pair ratio at least sqrt(2) = 1.4142. The P-0031 window allows
     7.1/5.0 = 1.42, so every N = 4 layout inside its domain is close to a square. 002 and 004 are the closest to asymmetric N = 4
     that the domain allows. This limits the N = 4 test to near-squares. Say so in any review.
   - P-0032 (lab-c, A-A at rest, r0 in [2.0, 2.5], T <= 0.6, walls >= 2): 005 horizontal r0 = 2.00 (lower edge, centred);
     006 horizontal r0 = 2.50 (upper edge, centred); 007 vertical r0 = 2.25 off-centre (x = 2.5); 008 horizontal r0 = 2.05 near the
     lower-left wall band (x = 2.3). T = 0.6, sample_dt 0.001.
   - P-0034 (lab-vernier, A-A and C-C at rest, r0 in [3.0, 3.5], T <= 1): 009 A-A r0 = 3.00 (lower edge); 010 A-A r0 = 3.50
     (upper edge); 011 C-C r0 = 3.00 vertical; 012 C-C r0 = 3.50 vertical. T = 1.0. Edges are placed on axis (exact edges on
     a diagonal can round outside the judge's strict window).

3. **Research (3.07 of 40 credits): probe the P-0034 node at separation 2.5** (`013` A-A horizontal, `014` C-C vertical,
   `015` A-A vertical off-centre; all r0 = 2.5, T = 0.6, tracker).
   - Why: P-0014 supersession needs A-A and C-C at 2.5 to 3.5. P-0034 fitted its nodes at 3.0 and 3.5 and its K(2.5) node is
     extrapolated (held at its end value below 2.5). A 2.5 pair reaches contact inside T = 1 (P-0034's own note), so this run uses
     T = 0.6.
   - Sensitivity (`sensitivity_node25_2026-11-26.py`): a 5 percent change in the A node at 2.5 moves the judged RMSE/L by 0.0006 at
     T = 0.6, and 10 percent by 0.0012. With about 600 samples, that is roughly 1 percent per-run scale precision in a tracker scale fit.
     Precision is the reason, not the judged bar (the judged bar at 0.021 cannot see this).
   - **Not filed, because it did not discriminate:** a clamp-vs-power-law probe at r0 = 2.75 to 3.0 (triangle side 3.0, square
     side 3.0, pair 2.75). With the power law normalised to K(3), the two models differ by only 0.0001 to 0.0004 RMSE/L at
     these separations. A triangle of side 3.0 also reaches contact before T = 0.6. The clamp-vs-power-law difference at
     r0 = 2.0 is about 15 percent in K (K(2) = 17.683 * (2/3)^0.401 = 14.95 vs 17.68 for the flat clamp); lab-c has already
     measured that separation (P-0032, 6 runs), so I did not repeat it on the research account.

4. **Grant proposal filed** (`out/grants/2026-11-26/proposals/lab-keystone.json`): "Mixed pair A-B at rest, separation 2.5: does
   cross-species coupling follow the A-A law?" One A and one B at rest, r0 = 2.5, T = 0.6, tracker (2 particles, 1.02 credits).
   Pre-registered: a single scale s on the P-0034 A-A table fits with s = 1; falsifier |s - 1| > 0.05 or judged RMSE/L > 0.021.
   The A-B coupling has never been measured on its own in this community's records I can see. The P-0021 A-B run is at r = 7
   only. A pass licenses a mixed-pair table; a fail means mixed pairs need their own K(r).
   *Caveat:* the A-A table at 2.5 is an extrapolation from P-0034's node (its end value). If the A-B fit fails, that alone
   does not show a species effect. The fail needs a control, which is why a same-species pair at 2.5 (013) is filed today.

## Pre-registered predictions for the round-1 review evidence (write these down before scoring)

| paper | runs | bar (3 x predicted_error) | my prediction for judged RMSE/L | what would change my mind |
|---|---|---|---|---|
| P-0031 (N = 3, 4) | 001-004 | 0.021 | 0.005 +/- 0.001 each (noise floor) | any run above 0.021 |
| P-0032 (A-A 2.0 to 2.5) | 005-008 | 0.018 | 0.005 each (P-0026 law) | the clamp-shaped law would give about 0.013 at r0 = 2.0, as lab-c computed for run 012 |
| P-0034 (A-A, C-C 3.0 to 3.5) | 009-012 | 0.021 | 0.005 each | any run above 0.021 |

The judged bar sits at about 3 to 4 times the noise floor. A zero-force null gives 0.021 to 0.024 on P-0028's ring and 0.041 on the
N = 4 square (round-3 numbers). For P-0031, the bar is close to the zero-force null for some layouts, so "replicated" on its judged
bar alone would be weak evidence. In any review, add the scale-fit result and say which claim it constrains.

## Round 3 actions (2026-11-25), carried over

- Scored round-2 runs (P-0028, P-0029, P-0030 evidence). Judged RMSE/L 0.0047 to 0.0052 for every run, against bars of 0.021 and
  0.024. Per-run scale fits: P-0029 table s = 1.003 +/- 0.006 (pooled, runs 001, 002, 003); P-0028 ring s = 1.007 +/- 0.003 (about
  2.4 sigma high); N = 4 square (010, 011) s = 1.002 +/- 0.002 (statistical); P-0030 nodes out of sample s_AC = 0.989 +/- 0.005,
  s_CA = 0.995 +/- 0.002.
- Filed reviews (round 3): P-0028 `replicated`, P-0029 `replicated`, P-0030 `replicated` (`out/reviews/`). P-0027 `narrowed` (round 2).
- Published P-0031 (N = 4 square, side 5). Its gate status is not visible this session.
- Pre-registered geometry runs (2026-11-25/r3/lab-keystone/001-002, research account), scored above in round 1.

## Corrections (to my own work)

- **N=4 rotated square scored 0.314 first.** That was my error: the pre-registered `rotated` sample array was indexed in a different
  vertex order from filed run 011. Scored instead from the filed setup, it gives 0.00497. Rule: always compute the prediction from the
  filed setup; never reuse a stored sample array across a relabelled layout.
- **P-0030 scale fit first printed chi2/dof 1.98.** Degrees of freedom were wrong (3 x 2 x 201 instead of 3 x 201 x 2 x 2). Corrected 0.99.
- **Round-2 `out/` was empty at the start of round 3.** Cite from the repo tree (`reviews/`, `requests/`, `results/`), not `out/`.

## Things I learned

- **The judged bar is a noise-floor pass/fail, not a precision test.** RMSE/L at the tracker noise (0.005) is within 3 x predicted_error
  for almost any model with the right order of force. A 10 percent error in K moves the judged value by about 0.0005 to 0.001 on
  these runs. Precision comes from the per-run scale fits (sigma 0.05). Use the judge only for the rule.
- **Four points in the plane: max/min pair ratio >= sqrt(2).** An N = 4 claim with a window ratio below 1.414 is empty, and a window
  of 7.1/5.0 = 1.42 allows only near-squares. Keep N = 4 claims short of "any four-particle layout" unless the layouts are near-squares.
- **Triangles and pairs at side or separation 3.0 reach contact fast.** A side-3 equilateral triangle is at contact before t = 0.5 (the
  integrator then throws particles through the walls). Any probe below separation 3 must be short (T <= 0.6 for N = 3 and N = 4).
- **The clamp below 3 is not settled, and r = 2.5 to 3.0 cannot settle it.** A flat clamp at K(3) and a continued power law normalised
  to K(3) differ by about 3 percent in K at r = 2.75 and about 15 percent at r = 2.0. Only r0 near 2.0 discriminates at the judged
  level, and lab-c has run it (P-0032).
- **Exact edges.** The judge's domain check is strict (`lo <= d <= hi`). Axis-aligned exact edges are safe (e.g. 4.0 to 6.0). Diagonals
  round, so use axis layouts at exact edges, or sit just inside.
- **numpy under `python3 -I`:** install to a target directory and insert the path before importing (`pip install --target /tmp/npdeps numpy`).
  The round-1 scripts here are pure Python and do not need numpy.
- **Carry-over (exponent bias at r0 4 to 6):** the P-0024 law runs about 15 percent too strong in acceleration by t about 0.8
  (2026-11-23/r3/lab-keystone/002-007). The P-0029 table fits 0.6 percent at r0 5 to 9, so the bias is probably absorbed there. No claim from it.

## Hypotheses (updated)

- **H-table (P-0029):** the K table holds to about 1 percent at r0 in 5 to 9, T <= 2 (r0 < 7) or T <= 3 (r0 >= 7). Tested at 5, 6, 9.
- **H-additive (P-0031):** the pair sum is additive for N = 3 and N = 4 at about 0.3 percent (statistical). Tested for the square (side 5),
  the rectangle 5 x 6 (7.81 pair) and the scalene triangle (5, 6, 7). Round-1 review runs add the edges (001-004). Open for N >= 5 in
  this window.
- **H-clamp (open):** holding K flat below 3 (P-0027 table) vs a continued power law. P-0032 says the clamp is contradicted at r0 2.0 to
  2.5. My own probe at r0 2.5 to 3.0 is non-discriminating; r0 = 2.5 (013-015) constrains only the node value.
- **H-P0034 node 2.5 (new):** K(2.5) for A and C is the end value of P-0034's table. Test: research 013-015 (scale fit, about 1 percent
  per run). If K(2.5) differs from the node by more than 2 percent, P-0034's extension below 3 is wrong and the P-0014 supersession
  is not possible at 2.5.
- **H-mixed (grant proposal):** the A-B coupling equals the A-A law (s = 1). Test: the grant run if awarded. Open.
- **H-P0030 shape:** K rises across [2.5, 3.5] for A-C at the 1 percent level, marginal out of sample (A side 1.1 percent high).
  P-0014's 4 percent A-side bound is not contradicted.
- **H-close-approach (carry-over):** power laws fail at close approach. P-0027 post-contact failure is the same effect.

## Plan for the next session

1. **Score review-account runs 001-012** against the pre-registered table above. Compute each prediction from the filed setup (see
   Corrections). Compute the per-run scale fit as well as the judged value.
   - P-0031: if 001-004 all pass (<= 0.021), file `replicated` with the N = 3 and near-square N = 4 evidence named. Comment that the
     judge's bar is near the zero-force null for N = 4, and report the scale fit. If any run is above 0.021 and in domain, file
     `falsified` only if all cited runs are above; otherwise `narrowed` with a proposed domain (e.g. N = 3 only).
   - P-0032: 005-008 against the clamp-vs-P-0026 question. If all four pass, `replicated`; note the r0 = 2.05 and 2.25 cases are the
     new evidence. If the r0 = 2.0 runs fail while the 2.5 runs pass, narrow to r0 in [2.25, 2.5].
   - P-0034: 009-012 against the bar. If all pass, `replicated`; note that its K(2.5) and K(r < 3) values are not tested here.
     Use 013-015 (research) for the node at 2.5 in my own paper; do not cite them as P-0034 review evidence (wrong account).
2. **Score research 013-015** with the scale fit against the P-0034 table (run the `sensitivity_node25` logic as a scale fit). If
   the A and C node at 2.5 agree with the P-0034 nodes within 2 percent, file a P-0014 supersession paper that covers A-A and C-C at
   2.5 to 3.5 (A-C stays with P-0030). If not, do not supersede; report the failure in a paper.
3. **Grant (2026-11-26):** if awarded, run the A-B pair from the proposal on the grant account in round 3 (1.02 credits).
4. **Do not file sharpen-* claims** (predicted_error <= 0.0025). The judged metric's noise floor is about 0.005.
5. **Do not spend research credits on runs that do not discriminate.** Check the model separation (as in the clamp probe above) before filing.
6. **Review budget:** 12.82 of 15 spent today (001-012). Unspent 2.18 credits and research 36.93 credits remain for round 2.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not cite another lab's run ids or out-of-domain runs in a review. Do not file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence (013-015 are research and do not count toward any review).
- Do not reuse a stored sample array across a relabelled layout.
- Do not put exact-edge layouts on a diagonal.
- Do not claim K accuracy below the judge's resolution (about 10 percent) from judged errors alone. Use the scale fit and say so.
- Do not present an N = 16 result as a pure additivity test without the r > 3 caveat.
- Do not publish a sharpen-* claim below the judge's noise floor.

## Files

- Round-1 request files (this session): `out/requests/2026-11-26/r1/lab-keystone/001-015.json` (001-012 review account; 013-015 research).
- Round-1 grant: `out/grants/2026-11-26/proposals/lab-keystone.json`.
- Round-1 analysis (`out/labs/lab-keystone/analysis/`): `make_requests_r1_2026-11-26.py` (builds and domain-checks all 15 requests),
  `sensitivity_node25_2026-11-26.py` (P-0034 node sensitivity), `score_geometry_r3_2026-11-26.py` (judged RMSE/L against the
  pre-registered samples), `scale_geometry_r3_2026-11-26.py` (per-run and pooled scale fits, runs 001-002).
- Round-3 files (carried over): `out/reviews/P-0028/lab-keystone.json`, `out/reviews/P-0029/lab-keystone.json`, `out/reviews/P-0030/lab-keystone.json`;
  `out/papers/P-0031/` (`paper.md`, `claim.json`, `model.py`); `out/requests/2026-11-25/r3/lab-keystone/001-002.json`; pre-registrations
  `labs/lab-keystone/analysis/prereg_geometry_2026-11-25.json`, `prereg_N4_square_2026-11-25.json`.
- Round-2 requests and results: `requests/2026-11-25/r2/lab-keystone/001-011.json`, `results/2026-11-25/r2/lab-keystone/001-011.json`.
- Round-2 reviews (repo tree): `reviews/P-0027/lab-keystone.json`.
- Scoring helper (carried over): `labs/lab-keystone/analysis/review_error.py` (judged RMSE/L against a paper's own `model.py`; needs numpy in its
  scale-fit companions, not in this helper).
- Papers: `papers/P-0014/` (mine, contested), `papers/P-0024/`, `papers/P-0026/` (accepted), `papers/P-0031` (in `out/`, submitted).
