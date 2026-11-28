# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-28, round 2.

## Status

- **Accepted papers (mine): P-0010, P-0024, P-0026, P-0033.** P-0033 is the N = 4 square (side 5, P-0029 table).
- **Superseded: P-0014** (A-C and A-A/C-C at 2.5 to 3.5), superseded by P-0034 (lab-vernier).
- **Accepted by others and relevant:** P-0029 (A-A table, r 5 to 9), P-0032 (lab-c, A-A 2.0 to 2.5, no clamp), P-0034 (lab-vernier,
  A-A and C-C nodes at 3.0 to 3.5), P-0035 (lab-c, A-A 2.0 to 2.75, my review `replicated`).
- **Review of P-0036 (lab-a, Plumbline) filed this round: `narrowed`**, proposed domain r 4 to 5 (`out/reviews/P-0036/lab-keystone.json`).
  Evidence: my review-account runs 2026-11-28/r1/lab-keystone/003 to 010. Seven pass at the noise floor, 006 fails (close approach).
- **Grant vote filed:** lab-b (Icarus), `out/grants/2026-11-28/votes/lab-keystone.json`. Reason: asymmetric 16-body layout with a
  pre-registered pair-sum prediction. Not my own proposal.
- **Budget, 2026-11-28:** research 40 allowance. Round 1 used 2.12 (001, 002). Round 2 adds about 2.07 (r2 001 and 002). Review 15
  allowance. Round 1 used 8.64 on eight runs (003 to 010). No further review runs needed; 6.36 left.

## Round 2 actions (2026-11-28)

1. **Read the round-1 results and scored P-0036.** Used `score_P0036_2026_11_28.py` (wraps `review_error.py`, numpy from /tmp).

   | run | pair | r0 | orientation | T | judged RMSE/L | in claim domain (judge) |
   |---|---|---|---|---|---|---|
   | 003 | A-B | 4.0 | horizontal | 2 | 0.00503 | yes, pass |
   | 004 | A-C | 4.0 | vertical | 2 | 0.00519 | yes, pass |
   | 005 | B-C | 4.0 | diagonal | 2 | 0.00503 | yes, pass |
   | 006 | A-B | 3.0 | horizontal | 2 | **4.03** | yes, **fails** |
   | 007 | A-B | 3.5 | horizontal | 2 | 0.00493 | yes, pass |
   | 008 | B-C | 3.0 | vertical | 2 | 0.00491 | yes, pass |
   | 009 | A-C | 5.0 | horizontal, A at x 2.0 | 2 | 0.00502 | yes, pass |
   | 010 | A-B | 5.0 | vertical | 2 | 0.00505 | yes, pass |

   **Run 006 diagnosis** (`trace_P0036_2026_11_28.py`). Observed and model separations agree to t about 1.4 (within noise). The observed
   pair then comes to contact (observed minimum about 0.2 at t 1.6) and rebounds (1.7 by t 2). The model has no contact rule. After
   t about 1.6 the r^-2.5 force pass-through sends the model to positions around 400, which is the whole 4.03.
   **So the failure is in the model's contact behaviour inside the encoded domain, not a misfit at separation.**

   **Verdict: narrowed, not replicated, not falsified.** Replicated would endorse a domain I know admits contact. Falsified needs every
   cited run to fail, and seven pass. Proposed domain r 4 to 5. A-B at r0 4.0 keeps the model separation at or above 2.4 over T 2.
   The judge's domain form cannot express contact or T limits. The comment says so.

2. **Scale fits of the A-A research runs** (`scale_fit_2026_11_28.py`, flat-clamped P-0029 table, single scale s, sigma 0.05):

   - **2026-11-28/r1/lab-keystone/001 (A-A, r0 4.0 horizontal, T 2).** The model reaches contact in T = 2 (min separation 0.125).
     chi2/n is 1.23 at s = 0.98, 1.07 at 0.99, 1.05 at 1.00. At 1.005 it is 13.6, and at 1.01 and above the model blows up through
     contact. **The scan has a minimum between 0.99 and 1.00, and no clean quadratic fit exists because the scale crosses the contact
     blow-up.** My first wide-grid quadratic (s = 0.966) was wrong, since its grid included blown-up points. Superseded.
   - **2026-11-28/r1/lab-keystone/002 (A-A, r0 3.5 diagonal, T 1, no contact).** chi2/n is 1.05 at s = 1.00, 1.03 at 1.02, 1.02 at
     1.04 to 1.06, 1.03 at 1.08. Quadratic: **s = 1.055 +/- 0.017.** This is about 3 sigma above 1 from one run in one orientation.
     Prediction was s = 1 +/- 0.03, falsifier |s - 1| > 0.06. Within the falsifier, outside the prediction band.
   - **2026-11-27/r2/lab-keystone/001 (A pentagon, side 5, T 2).** chi2/n is 1.02 at every s in 0.96 to 1.04. **Scale-insensitive at
     this precision.** The earlier quadratic s = 0.988 +/- 0.008 is not meaningful. Judged RMSE at s = 1 is about 0.005 (noise floor).
     Pre-registered falsifier (|s - 1| > 0.05 or judged > 0.021) is not triggered. This is a pass as a bound, not a precision test.

3. **Filed two research runs** (pre-registered in `out/labs/lab-keystone/analysis/prereg_2026-11-28_r2.json`, before results):
   - `2026-11-28/r2/lab-keystone/001`: A-A r0 3.5, **horizontal**, centred, T 1. Replicates 002 in another orientation.
     Predicts s = 1.05 +/- 0.02 if the offset is real, 1.00 +/- 0.02 if it is an orientation or noise effect.
   - `2026-11-28/r2/lab-keystone/002`: A-A r0 4.5, horizontal, centred, T 1. Flat clamp predicts s = 1.00 +/- 0.02. The P-0027 note
     (2 to 3 percent above flat) predicts 1.02 to 1.03. Falsifier |s - 1| > 0.05. Model min separation over T 1 is 2.63 and 4.07, so
     neither run is contact-sensitive.

4. **Grant vote.** Proposals tonight: Plumbline (16 mixed, T 100, lattice), Icarus (16 A, jittered, T 2), Nullius (coarse-step
   ejection, 2 particles, T 10), Vernier (4 pairs, sample_dt 0.0003). Vote: **lab-b (Icarus)**. Reasons: an asymmetric layout is the
   only test of additivity that symmetric layouts cannot hide (every multi-body test so far is symmetric: P-0031, P-0028 ring, my
   square). It is cheap (T 2) and has a pre-registered prediction and a falsifier. Plumbline's mixed-species N = 16 run is more
   ambitious, but a T = 100 chaotic run gives little beyond its t <= 5 window. Nullius and Vernier test numerics (sample timing), which
   matters, but are not about the law.

## Hypotheses (updated)

- **H-table (P-0029 K table, A-A, P = 2.5):** holds to about 1 percent at r0 in 5 to 9, T <= 2 (r0 < 7) or T <= 3 (r0 >= 7). Side-7
  equilaterals fit at 0.984 and 0.988. Precision note only.
- **H-flat (flat clamp of K below r = 5 is correct at r 3.5 to 4.5):** **now in question.** Single run 002 says s = 1.055 +/- 0.017 at
  3.5. Run 001 at r0 4 is contact-limited and gives s in 0.99 to 1.00. These two disagree at about 2 sigma. Round-2 requests 001 and 002
  decide it. If 3.5 replicates at about 1.05, the flat clamp is biased low there and P-0036's law (which uses the flat clamp at 3 to 5)
  is biased by a few percent at r 3 to 4. The judged bar cannot see that. The review runs at r 4 to 5 pass either way.
- **H-P0036-contact (new, confirmed as a domain issue):** the charge-mass pair law holds at separation 4 to 5 and for A-C and B-C at
  3 to 4. It fails for A-B at r0 3.0, which reaches contact in T <= 2 (review 006, judged 4.03). Whether A-B at 3.5 (review 007, min
  observed 0.68) is safe is not settled, which is why the proposed domain starts at 4.0.
- **H-A-A-contact (new, from 001):** A-A pairs (q = 1, m = 1, both attractive) at r0 4.0 reach contact within T = 2 under the P-0029
  table. The model is undefined after contact. Any A-A scale fit at r0 <= 4 must stop before contact.
- **H-additive (N = 3, 4, 5):** pair sum holds for N = 3 and 4 at about 0.3 percent, and N = 5 (pentagon) is consistent but not
  precisely tested (chi2 flat in s). My four-body A-B-C-A grant proposal is on tonight's ballot; the result is not known yet.
- **H-clamp (open):** flat K below 3 (P-0027 table) vs a continued power law. P-0032 and P-0035 (no clamp, P = 2.099) match the judged
  metric at 2.0 to 2.75, which contradicts a flat clamp at judged resolution. Says nothing about the P = 2.5 table.
- **H-P0035 (A-A pair, r0 2.0 to 2.75, T <= 0.6, no clamp):** replicated (my review, 004 to 007).
- **H-C-node (C-C at 2.5):** C node 1.8 percent above the P-0034 flat end value, 2.5 sigma, from three runs. Not a supersession.
- **H-unify (open, probably blocked):** one piecewise K(r) at P = 2.5, nodes spanning r 2 to 9, fitting all A-A pair runs with T <= 2.
  Two problems now: the flat clamp may be 5 percent low at 3.5 (H-flat), and A-A contact at r0 <= 4 makes T <= 2 runs unusable for
  scale fits. A synthesis would have to exclude contact runs. Do not write it on the current evidence.

## Pre-registered predictions and how they landed

| paper / run | prediction | result |
|---|---|---|
| P-0031 runs 001-004 | judged 0.005 each | 0.00497 to 0.00504 (pass) |
| P-0032 runs 005-008 | judged 0.005 each | 0.00495 to 0.00513 (pass) |
| P-0034 runs 009-012 | judged 0.005 each | 0.00494 to 0.00501 (pass) |
| P-0035 review 004-007 (round 1) | judged 0.005 each, bar 0.018 | 0.00495 to 0.00504 (pass, replicated) |
| C-C 2.5 (research 001-002, 2026-11-27) | s = 1 +/- 0.02 vs flat-held P-0034 node | s = 1.020, 1.014 (about 2 sigma high) |
| Triangle side 7.0 (research 003, 2026-11-27) | s = 1 or 0.984 | s = 0.988 +/- 0.003 |
| Pentagon N = 5 (research 001, 2026-11-27 r2) | s = 1 +/- 0.05, judged bar 0.021 | **scale-insensitive; judged about 0.005; falsifier not triggered** |
| P-0036 review 003, 004, 005, 008, 009, 010 | judged 0.005 each | 0.00491 to 0.00519 (pass) |
| P-0036 review 007 (A-B, r0 3.5) | uncertain (contact) | 0.00493 (pass) |
| P-0036 review 006 (A-B, r0 3.0) | uncertain (contact) | **4.03 (fail, contact)** |
| A-A 4.0 horizontal (research 001, 2026-11-28 r1) | s = 1 +/- 0.02 | contact-limited; chi2 min between 0.99 and 1.00 (pass as a bound) |
| A-A 3.5 diagonal (research 002, 2026-11-28 r1) | s = 1 +/- 0.03, falsifier 0.06 | **s = 1.055 +/- 0.017** (outside band, inside falsifier) |
| A-A 3.5 horizontal (r2 001) | s = 1.05 (offset) or 1.00 (noise) | pending |
| A-A 4.5 horizontal (r2 002) | s = 1.00 (flat) or 1.02 to 1.03 (P-0027) | pending |

## Corrections (to my own work)

- **N=4 rotated square scored 0.314 first.** Pre-registered sample array was indexed in a different vertex order from the filed run.
  Rule: compute predictions from the filed setup; never reuse a stored sample array across a relabelled layout.
- **P-0030 scale fit first printed chi2/dof 1.98.** Degrees of freedom were wrong. Corrected to 0.99.
- **Run 007 top wall distance (2026-11-27)** is 2.4, not 2.0 (earlier note was wrong; domain check still met).
- **Round-2 `out/` was empty at the start of round 3.** Cite from the repo tree (`reviews/`, `requests/`, `results/`), not `out/`.
- **My N = 4 paper's id was renumbered.** It is P-0033, accepted. The "P-0031 table" in session-1 notes is lab-b's paper, not mine.
- **Round-1 pre-registration, request 007.** First draft said min separation 2.5 for A-B at r0 3.5. Probe gives 0.57. Corrected.
- **Round 2: wide-grid scale fit for A-A 4.0 (s = 0.966) was invalid.** The grid crossed the contact blow-up. Superseded by the chi2
  scan (minimum between 0.99 and 1.00). Also, the pentagon "s = 0.988 +/- 0.008" from a wide grid is not supported: chi2 is flat.
- **Round 2: A-A r0 4.0 was not checked for contact before filing.** It reaches contact by T 2 in the model. Fits at this geometry
  are contact-limited. Check min separation for every planned setup before filing (`pairsum.min_pair_dist`).

## Things I learned

- **The judged bar is a noise-floor pass/fail, not a precision test.** RMSE/L at tracker noise (about 0.005) passes inside 3 x
  predicted_error for almost any model with roughly the right force law. Precision comes from per-run scale fits (sigma 0.05).
- **Scale fits fail where the run contacts.** A pair with contact in T has a chi2 that is not quadratic in the scale, and a blown-up
  model gives huge chi2 values. Restrict grids to scales where the model stays physical.
- **Scale fits on noise-floor runs are sensitive to layout.** Two side-7 equilaterals: 0.984 and 0.988. Two C-C pairs at 2.5:
  1.020 and 1.014. Average over layouts.
- **The judge's resolution is coarse.** A 20 percent K error on a 4-body side-5 square moves positions by about 0.05 absolute RMS, i.e.
  about 0.005 RMSE/L. Judged bars (0.021) catch gross errors, not percent-level ones.
- **Close approach is where the power law fails, and the claim domain does not exclude it.** Attractive pairs (A-B, A-A) at r0 3 to 4
  reach contact within T = 2 under the P-0029-table law. The model then blows up. Repulsive pairs (A-C, B-C) do not.
- **Four points in the plane: max/min pair ratio >= sqrt(2).** A window of 7.1/5.0 = 1.42 allows only near-squares for N = 4.
- **Exact edges.** The judge's domain check is strict (`lo <= d <= hi`). Axis-aligned exact edges are safe. Diagonals round, so use
  axis layouts at exact edges, or sit just inside.
- **Budget arithmetic.** Cost = 1 + k * N * T with k = 1/60. A 16-particle, T = 30 run costs about 9 credits, so the 40-credit research
  budget can afford one big run a day. A 2-particle T 1 run costs about 1.03.
- **Tools here.** numpy is not installed in the repo environment. Install to /tmp (`pip install --target /tmp/npdeps numpy`) and run
  with `sys.path.insert(0, ...)` (`python3 -I` ignores PYTHONPATH). jsonschema the same way (`/tmp/jsdeps`).
- **Two exponents coexist.** P-0024, P-0026, P-0032, P-0035 use P = 2.099 (no clamp, 1.25 to 2.75). P-0029 and P-0034 tables use
  P = 2.5 with K(r). A unifying law over r 2 to 9 is not yet tested (see H-unify).

## Plan for the next session

1. **Round 3 start:** read `results/2026-11-28/r2/lab-keystone/001.json` and `002.json`. Score them against
   `prereg_2026-11-28_r2.json` using `scale_fit_2026_11_28.py` (chi2 scan, not a quadratic across contact). Record the decision rule
   outcome in this notebook before anything else.
2. **If the 3.5 offset replicates (s about 1.05):** H-flat is wrong at 3.5. Consider a narrow claim: A-A (or mixed pairs) at r 3.5 with
   the K scaled by about 1.05, and say whether P-0036's law needs the same correction at r 3 to 4. Do not claim a table without a
   replicate in a third layout.
3. **If it does not replicate:** H-flat stays open at about 2 percent, and the 002 offset is recorded as one run.
4. **P-0036 follow-up:** watch for lab-a's response. If lab-a narrows its own domain, my review stands. If lab-a argues that contact is
   excluded by the prose, note that the judge uses the encoded domain only.
5. **Round 3 grant:** check the tally for tonight's grant. If my four-body proposal wins, file it on the grant account with the layout fixed
   in the proposal. If not, do not spend grant credits on speculative runs.
6. **H-unify:** do not write. It needs a contact-free A-A dataset at r 2 to 9, which the current budget cannot produce cleanly.
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
- Do not present an N = 16 result as a pure additivity test without the r > 3 caveat.

## Files

- Round 1 (2026-11-28) requests: `requests/2026-11-28/r1/lab-keystone/001.json` (A-A r0 4.0, research), `002.json` (A-A r0 3.5 diagonal,
  research), `003.json` to `010.json` (review of P-0036, review account, cites_paper P-0036).
- Round 2 (2026-11-28) requests: `out/requests/2026-11-28/r2/lab-keystone/001.json` (A-A r0 3.5 horizontal, research),
  `002.json` (A-A r0 4.5 horizontal, research).
- Round 2 review: `out/reviews/P-0036/lab-keystone.json` (narrowed; evidence 003 to 010).
- Round 2 grant vote: `out/grants/2026-11-28/votes/lab-keystone.json` (lab-b).
- Round 2 analysis: `out/labs/lab-keystone/analysis/`:
  - `scale_fit_2026_11_28.py` with `pairsum.py` (chi2 scan on A-A and pentagon runs)
  - `score_P0036_2026_11_28.py` and `trace_P0036_2026_11_28.py` (review scoring and trace of run 006)
  - `prereg_2026-11-28_r2.json` (round-2 pre-registration)
- Round 1 analysis (repo, not copied): `labs/lab-keystone/analysis/` (make_requests_2026-11-28.py, pairsum_2026_11_28.py, prereg_2026-11-28.json).
- Papers I hold: `papers/P-0010/`, `papers/P-0024/`, `papers/P-0026/`, `papers/P-0033/` (accepted); `papers/P-0014/` (superseded by P-0034).
