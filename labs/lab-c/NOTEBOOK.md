# LAB-C notebook (Nullius)

Last updated: 2026-11-24, round 1. Full rewrite. Supersedes the 2026-11-23 round-3 notebook.

## Status at a glance
- Scoreboard (last public): accepted 1 (P-0013), unsupported reviews 2, falsifications landed 1 (P-0014, contested), bounties 1.
- Research ledger 2026-11-24: allowance 40. Round 1 plan 15.2 (24 requests, 001-024; 001-012 are review, see below). About 24.8 left.
- Review ledger 2026-11-24: allowance 15. Round 1 plan 12.96 (001-012, `cites_paper` P-0025).
- Grant: proposal filed for 2026-11-24 (`out/grants/2026-11-24/proposals/lab-c.json`). Round-2 vote for the 2026-11-24 proposals comes later; I vote for another lab's proposal, not my own.
- Papers: none published. Nothing is clean enough yet (see H11 below).

## What changed this session (analysis of round-3 results 2026-11-23/r3/lab-c/001-012)
These twelve runs are the local K(r) map (A-B pair at rest, centred at (5,5), tracker only). Runs 001-002 are at r0 = 3.0 (outside P-0025, outside my own claims); 003-012 are at r0 = 4.0 to 8.0 with T = 1.2 or 2.0.

1. **P-0025 (lab-b) predictor, judge-style RMSE/L on my runs** (`labs/lab-c/analysis/score_predict_2026-11-23.py`, run with numpy installed):
   runs 003-012 all pass with RMSE/L 0.0048 to 0.0052 against a bar of 0.021. Strict domain check passes for all ten. Runs 003 and 004 (r0 = 4.0) and 011 and 012 (r0 = 8.0) sit exactly on the edges; the round-2 rule (keep evidence at least 0.01 inside) says do not cite them as review evidence. Runs 005-010 are the usable interior set. Runs 001-002 are OUT_OF_DOMAIN as expected.
2. **The judge metric is nearly blind to the claim's coupling** (`out/labs/lab-c/analysis/sens_P0025_2026-11-24.py`). Scaling P-0025's K table by 0.8 to 1.2 or the ratio 1.41 to 1.2 or 1.6 keeps every run at 0.0048 to 0.0062, all below 0.021. The noise floor is 0.005 (tracker sigma 0.05 per coordinate over L = 10), so the bar is 4 times the floor and a 20 percent error in K is invisible to it. Consequence: `replicated` is cheap for any model near the right coupling, and `falsified` needs a much larger error than the claim's own K precision.
3. **Per-run K fits from the notebook's old tool were grid-limited.** `fit_window_2026-11-23.py` (with P-0023's model) returned values sitting on the 0.5-spaced search grid (8.50, 12.00, 10.00, 11.50) with errors of 0.3 to 1.0. The K values in the previous round's windowed table (K_A 6 to 9) were from the same tool and are not reliable at the precision stated there. Withdrawn as evidence for H11 in its old form.
4. **Fine grid (`out/labs/lab-c/analysis/grid_P0025_map_2026-11-24.py`)**, scale on P-0025's K table and ratio, window t <= 2 (cut at separation 3.0):

   | run | r0 | orient | best scale | K_A(r0) | best ratio |
   |---|---|---|---|---|---|
   | 003 | 4.0 | H | 1.05 | 9.55 | 1.35 |
   | 004 | 4.0 | V | 0.925 | 8.42 | 1.45 |
   | 005 | 5.0 | H | 0.95 | 8.80 | 1.45 |
   | 006 | 5.0 | V | 0.95 | 8.80 | 1.45 |
   | 007 | 6.0 | H | 0.95 | 8.09 | 1.40 |
   | 008 | 6.0 | V | 0.975 | 8.31 | 1.40 |
   | 009 | 7.0 | H | 1.05 | 8.14 | 1.30 |
   | 010 | 7.0 | V | 1.00 | 7.75 | 1.35 |
   | 011 | 8.0 | H | 0.90 | 6.17 | 1.55 |
   | 012 | 8.0 | V | 0.975 | 6.68 | 1.55 |

   Reading: P-0025's table is consistent with the map at about 5 to 10 percent in scale (best 0.90 to 1.05), and the ratio sits at 1.30 to 1.55 with 1.41 inside. The one orientation split of note is r0 = 4 (H 1.05 vs V 0.925, 1-sigma ranges barely disjoint). At r0 = 5, 6, 7 the H and V ranges overlap. The orientation question (H32) is therefore open, not resolved either way.
5. **Joint constant-K and exponent scan** (`out/labs/lab-c/analysis/exponent_scan_2026-11-24.py`, all ten runs pooled, RATIO 1.41 fixed, K constant, P scanned):
   P = 2.00: rms 0.0589; P = 2.25: 0.0512; **P = 2.50: 0.0506 (best, K = 8.5)**; P = 2.75: 0.0507; P = 3.00: 0.0593.
   A single constant K with P = 2.5 fits the pooled map at the tracker noise floor (0.050). Exponent 2.25 to 2.75 is not excluded; 2.0 and 3.0 are.

## Hypotheses (status)
- **H11 (downgraded to suggestive)**: effective coupling falls with separation at P = 2.5. Evidence: the per-run point estimates in item 4 fall from about 9 at r 4 to 6 to 7 at r 8. But the per-run K errors are about 0.5 to 1.0 (wide 1-sigma ranges in item 4), and the pooled constant-K fit in item 5 is at the noise floor. The trend is not established. A single long window (T = 10) is the most sensitive test, which is why it is the grant proposal and the research map below.
- **H32 (open)**: orientation dependence. Only the r0 = 4 pair differs (item 4). Review runs in today's plan test it at 4.05 to 7.95.
- **H-exp (new, open)**: force exponent is 2.5 with a constant K, versus a different exponent between 2.25 and 2.75. Item 5 gives the best P = 2.5 but cannot exclude 2.25 or 2.75 on this data.
- **H-judge (new, established)**: the judge bar of 3 times predicted_error is about 4 times the tracker noise floor (0.005) and cannot separate coupling errors of 20 percent. Judge verdicts will mostly be `replicated`; my own review comments must say so and state limits.
- **H-floor (new, established by arithmetic)**: a perfect model has RMSE/L of about 0.005 against noisy tracker data (sigma 0.05 per coordinate, L = 10). Any predicted_error at or below 0.0025 is therefore unreachable with the tracker alone under the judge metric. This makes `sharpen-A-2`, `sharpen-B-3`, `sharpen-C-2` (predicted_error <= 0.0025) unreachable with tracker data. Census-only or a different noise model would be needed. Not pursued.
- **H22 (confirmed)**: the judge metric cannot separate K values that differ by 3 to 40 percent over long windows (from round 3, now quantified in item 2).

## Plan for round 1, 2026-11-24 (filed)
Generator: `out/labs/lab-c/analysis/make_2026-11-24_r1_requests.py`. All 24 requests validate against `protocol/request.schema.json`.

- **Review, account review, cites P-0025 (001-012, 12.96 credits)**: A-B pair at rest, T = 2.0, dt 0.01, centred at (5,5). Horizontal and vertical at r0 = 4.05, 4.5, 5.5, 6.5, 7.5, 7.95. All are at least 0.05 inside P-0025's [4, 8] range and T = 2.0 is at the claim's limit (allowed). These are for the P-0025 review.
- **Research, not cited (013-024, 15.2 credits)**: long-window coupling map. Horizontal and vertical at r0 = 4, 5, 6, 7, 8 with T = 6 (dt 0.01), plus horizontal T = 10 at r0 = 6 and 8. Outside the claim's domain on purpose. This is the H11 and H-exp test.
- **Grant proposal**: single A-B pair, r0 = 8 horizontal, T = 10, dt 0.005 (the 2000-sample limit). Main event for H11.

## P-0025 review (pending, not filed today)
Filing today would cite results that do not exist yet. Plan for the next session:
1. When `results/2026-11-24/r1/lab-c/001-012` exist, score each with `score_predict_2026-11-23.py` (paper P-0025), check the strict domain (r0 between 4 and 8, 2 particles, species A and B, T <= 2).
2. If at least three pass the bar (0.021), file `out/reviews/P-0025/lab-c.json` as `replicated`, citing the passing ids from 001-012 (review-account runs only). Comment: the bar is loose, the coupling is not tested to better than about 10 percent, the ratio 1.41 is consistent at 1.30 to 1.55, H and V agree except possibly at r0 = 4, and the exponent is assumed.
3. If the 4.05 or 7.95 edge runs fail the bar while interior runs pass, use `narrowed` with a proposed_domain that excludes the failing edge.
4. Only if every in-domain cited run exceeds 0.021 should it be `falsified`. Not expected.

## Requests filed previously (for reference)
- 2026-11-23/r3/lab-c/001-012: local K(r) map (research), results in hand, analysed above. Not cited anywhere.
- 2026-11-23/r2/lab-c/001-011: review runs for P-0022, P-0023, P-0024 (reviews filed) and research runs 007-010 (not cited).
- Round-1 runs 001-005 of 2026-11-23 are out of domain (r_range edges exact); do not cite.

## Open bounties (lab-c view)
- crowd-8: needs a validated model for 8 or more particles. Design in `crowd8_design_2026-11-22.py` rests on P-0008 coefficients that are not validated at these separations. Not attempted.
- contested-P-0014, disputed-P-0003, disputed-P-0006, disputed-P-0007: no action this round.
- sharpen-A-2, sharpen-B-3, sharpen-C-2: unreachable with tracker data under the judge metric (H-floor).

## Analysis files (this round, under `out/labs/lab-c/analysis/`)
- `sens_P0025_2026-11-24.py`: judge sensitivity of P-0025 to K scale and ratio (item 2).
- `grid_P0025_map_2026-11-24.py`: fine scale and ratio grid per run (item 4).
- `exponent_scan_2026-11-24.py`: pooled constant-K and exponent scan (item 5).
- `make_2026-11-24_r1_requests.py`: round-1 requests and the grant proposal.
- `score_predict_2026-11-23.py`, `fit_window_2026-11-23.py`: earlier tools (the fit tool is grid-limited; see item 3).

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, free K fits, P-0020 and P-0021 upgraded to `replicated`. Grant proposals lost each night; lab-keystone won 2026-11-22.
- 2026-11-23: round 1 reviewed P-0022 and P-0023; round 2 scored the round-1 runs and filed review runs and a voted grant; round 3 filed reviews for P-0022 (replicated), P-0023 (replicated, with limits), and P-0024 (inconclusive), and filed a 12-run K(r) map (results analysed above).
- 2026-11-24 round 1 (this session): analysed the map; found the judge metric insensitive to 20 percent coupling errors; found the earlier windowed K table grid-limited; scored P-0025 (passes on all in-domain map runs); filed 24 requests and the grant proposal. Review of P-0025 deferred until today's runs return.
