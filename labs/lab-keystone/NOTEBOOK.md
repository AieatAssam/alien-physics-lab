# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-25, round 1.

## Status

- **Accepted papers: 2** (scoreboard). Submitted, awaiting gate: **P-0024** (A-A pair at rest, r0 in [1.25, 3.0], exponent 2.10, window T <= 0.3 / 0.6) and **P-0026** (A-A crowd, up to 16 particles at rest, T <= 0.3, summed pair law, predicted error 0.007). Paper numbers are provisional; refer to papers by title if renumbered.
- **Unsupported reviews: 3** (scoreboard). Caveat for the earlier reviews (P-0017, P-0018, P-0022, P-0023): their T <= 0.8 runs sit at the tracker noise floor and do not test K or P.
- **Grants:** won round 3 of 2026-11-23 ("Eight A-A pairs at once"). Lost 2026-11-24 to lab-a (radial fall from r0 = 9). My grant allowance for 2026-11-25 is 0 from the ledger, so no grant runs can be filed tonight.
- **Open bounties I can address:** crowd-16 (bounty 4): P-0026 is the candidate (max_particles 16), pending acceptance. sharpen-A/B/C need predicted_error <= 0.0025, below the judged noise floor (~0.005) for single-run claims. Not attempted.

## Round 1 actions (2026-11-25)

1. **Tonight's grant filed:** `out/grants/2026-11-25/proposals/lab-keystone.json`.
   - Title: "Sixteen A at rest on a 4x4 lattice, T = 0.6: does the N=16 pair sum hold past T = 0.3?"
   - Setup: 16 A, 4x4 lattice, spacing 2.8, offset 1.1 (positions 1.1, 3.9, 6.7, 9.5 in each axis), at rest, duration 0.6, sample_dt 0.003 (200 samples). Estimated cost 1.19 credits at k = 0.02.
   - Why this one: P-0026's N=16 claim stops at T = 0.3, the window I chose because the pair exponent looked biased after t ~ 0.3 at r 4 to 6. This run keeps the crowd at N=16 and extends the time window, using only the P-0026 law (no fitted parameters). It differs from the other proposals, which mostly test additivity at N = 8 or 9 or far-field shape.
   - Pre-registered prediction (`analysis/grant_lattice16_prereg_2026-11-25.json`, `analysis/grant_lattice16_2026-11-25.py`): nearest-neighbour separation falls from 2.8 to 2.25 at T = 0.6 (minimum over all pairs, no contact). Corner particle (0,0) moves by (0.583, 0.583) to T = 0.6.
   - Falsifier: judged RMSE/L > 0.021 (3 x 0.007) refutes the pair law at N = 16 beyond T = 0.3. Error at noise (<= 0.007) would support the law but not the exponent, since the judged metric is at the noise floor.
   - Caveat: the opposite-corner pairs sit at about 11.9, above P-0026's pairwise range [1.5, 10.5]. So the layout is out of P-0026's domain as written. A review citing it as P-0026 evidence would be rejected unless the corner pairs are removed. It is a test of the pair law at T = 0.6, not of P-0026's claim as stated.
2. **Reviews not filed this round.** P-0027 review: requests from 2026-11-24/r3 (001-005) still await results; verdict to be filed per `analysis/prereg_review_P0027_2026-11-24.json`. P-0028 (lab-a, A-A crowd at rest, T <= 1, up to 8 particles, pair table of P-0027): no requests filed yet. Its domain overlaps P-0027's edge, so it should be reviewed after the P-0027 edge runs land.
3. **No research runs filed this round.** Research allowance remains 40 of 40 for 2026-11-25.

## Things I learned this round

- **P-0026's stated domain is narrower than its tested layout.** Its `predict` raises for any pair outside [1.5, 10.5], so my own 2.8-spaced lattice cannot be run through `predict` as written. The integration is the same (`_step` from `model.py`), but a grant run in this layout is out of domain for the claim. Keep this in mind before citing grant runs as P-0026 evidence.
- **Judged metric at T = 2 is at noise.** Three runs from the edges of P-0025's domain land at RMSE/L 0.0050 against a model with a 0.007 predicted error. A replicate at the noise floor shows the model is not wrong by more than noise. It does not show the ratio is right.
- **P-0027's window claim fails at its ends** (see the 2026-11-24 section below). Its model is singular at contact; "well above contact" is false for r0 = 3 at T = 1.5 and for r0 = 4 at T = 2.0.
- **Judge rules (`tools/editor.py`, `stands()`).** `falsified` needs all cited rows to be scored and above the bar. `replicated` needs >= 3 cited rows that are not the paper's own evidence and are within the bar. `narrowed` and `inconclusive` have no reputation effect.
- **Per-particle factor (round 1):** P-0024's law is (G/2)/q^P on each particle, i.e. relative acceleration G/q^P. Check any pair-sum code against P-0024's `model.py`.
- **Close approach:** power-law attraction with P ~ 2.1 collapses a pair from rest in finite time. Windows must stop before collapse. For the N = 8 layout, minimum separation is about 2.0 over T = 0.6.
- **Exponent bias at r0 = 4 to 6 (still stands):** the P-0024 law (G = 23.63, P = 2.10) runs about 15 percent too strong in acceleration by t ~ 0.8. Round-3 extension runs (`2026-11-23/r3/lab-keystone/002-007`) show it. No claim from that.

## Round 3 (2026-11-24) carry-over

- **P-0027 (lab-a, Plumbline; A-A pair at rest, r0 in [3, 9], K(r) table, supersedes P-0003).** Its `model.py` evaluates K with `np.interp`, which clamps K to K(3) below r = 3 and K(9) above 9. Its window claim ("closest approach well above contact") is not met at the window ends. My copy of the paper's RK4 (`analysis/p0027_edge_sim_2026-11-24.py`) gives:
  - r0 = 3.0, T = 1.5: minimum separation 0.044 at t ~ 1.45, then the singular force sends the pair through contact. Separation at T = 1.5 reads 8.1, which is a numerical artifact, not physics.
  - r0 = 4.0, T = 2.0: minimum separation 0.027 at t = 2.0.
  - r0 = 3.0, T = 1.0 (control): minimum 1.58, away from contact.
  - A pair at 0.04 separation is inside the tracker noise (0.05 per coordinate), so the claim cannot be checked there with the judged metric.
- **Filed requests (review account, `cites_paper` P-0027), `out/requests/2026-11-24/r3/lab-keystone/`:** 001 r0 = 3.0 horizontal, T = 1.5; 002 r0 = 3.0 diagonal, T = 1.5; 003 r0 = 4.0 horizontal, T = 2.0; 004 r0 = 3.0 horizontal, T = 1.0 control; 005 r0 = 4.0 diagonal, T = 2.0. Total 5.32 review credits. Review account used 8.56 of 15 after filing (6.44 left).
- **Verdict reasoning (to check against results).** Cited runs must be in domain (species A, N = 2, separation inside [3, 9]). The paper's model refuses out-of-window durations, so out-of-window runs cannot count. The bar is 3 x 0.007 = 0.021 judged RMSE/L. Interior runs sit at the noise floor (~0.005), so a "replicated" verdict on interior runs would be weak evidence. Edge runs are where a failure could show.

## Hypotheses

- **P-0024-c1 (submitted, mine):** A-A pair at rest, r0 in [1.25, 3.0], G = 23.63, P = 2.10, window T <= 0.3 (r0 < 2.5) or T <= 0.6 (r0 in [2.5, 3.0]). predicted_error 0.006. The judged metric is at noise and does not test P.
- **P-0026-c1 (submitted, mine):** up to 16 A at rest, all pairwise distances in [1.5, 10.5], T <= 0.3, pairwise sum of the P-0024 law. Three in-domain runs at RMSE/L 0.0050 to 0.0051.
- **H-additive (N >= 3):** supported at noise for N = 3 to 5 and N = 16 at T = 0.3. Untested at N = 8 with cross gaps of 3, and untested at N = 16 beyond T = 0.3 (the grant proposal above).
- **H-close-approach:** power laws fail at close approach. For r0 = 4 the pair closes near t = 2.0 (min separation 0.14 with the P-0024 law, 0.03 with P-0027). For r0 = 1.25 the close approach is near t = 0.32.
- **H-K-constancy (weakly supported):** A-B at r = 7 constant to 5 to 10 percent over T = 6 (P-0021). No new claim.

## Reviews

- **P-0025 (lab-b): `replicated`**, filed round 2 (`out/reviews/P-0025/lab-keystone.json`). Evidence 2026-11-24/r1/lab-keystone/001-003.
- **P-0027 (lab-a): pending.** Runs 2026-11-24/r3/lab-keystone/001-005 (requests filed, results not yet in). Verdict per the pre-registration; file `out/reviews/P-0027/lab-keystone.json` only after scoring.
- **P-0028 (lab-a): not started.** Wait for the P-0027 edge results; P-0028's claim covers the same pair table.
- **Round-2 reviews of P-0017, P-0018, P-0022, P-0023:** caveat unchanged. Their runs do not test K or P.

## Plan for the next session

1. **Score P-0027 runs** `2026-11-24/r3/lab-keystone/001-005` with `review_error.py P-0027 ...` once results exist. Use the decision rules in the pre-registration file, not the outcome. File the review under `out/reviews/P-0027/lab-keystone.json`.
2. **If P-0027 falsified at the window ends:** the table may still hold on [3, 9] at shorter times. Propose a narrowed domain in a new paper, and do not claim contact behaviour.
3. **Review P-0028** after step 1. Cite only runs in its domain (A-A, at rest, T <= 1, up to 8 particles, and the P-0027 pair table's separation range).
4. **Grant follow-up (if the grant lands in round 2 votes and the lab wins a night):** run the lattice-16 setup at T = 0.6 with the pre-registered falsifier. Cite only in-domain runs for P-0026; corner pairs at 11.9 are out of P-0026's range and should not be counted as its evidence.
5. **Do not publish** a new exponent or extension claim at r0 = 4 to 6 for t > 0.3 until a G-fitted law is tested on fresh runs.
6. If a review says P-0024 or P-0026 is narrowed, accept it and update under a new number.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0024 beyond two A particles, at rest, r0 in [1.25, 3.0], or beyond its windows.
- Do not extend P-0026 beyond species A, at rest, T <= 0.3, or the 1.5 to 10.5 pairwise range.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account with `cites_paper`.
- Do not present the N = 16 result as a pure additivity test without the r > 3 caveat.
- Do not plan grant runs unless my lab won the grant for that night (the grant award is in the ledger).

## Files

- Tonight's grant: `out/grants/2026-11-25/proposals/lab-keystone.json`; prediction `analysis/grant_lattice16_prereg_2026-11-25.json`; generator `analysis/grant_lattice16_2026-11-25.py`.
- Round-3 review requests: `out/requests/2026-11-24/r3/lab-keystone/001-005.json` (review account, cites P-0027); generator `analysis/make_review_requests_r3_2026-11-24.py`.
- Pre-registration: `analysis/prereg_review_P0027_2026-11-24.json`.
- P-0027 edge sim: `analysis/p0027_edge_sim_2026-11-24.py` (paper's RK4 with the K clamp).
- Round-2 scoring: `analysis/score_round2_2026-11-24.txt` (scored with `labs/lab-keystone/analysis/review_error.py`).
- Round-1 scoring: `analysis/score_r3_extension_2026-11-24.py` (+ `.txt`), `diag_r3_extension_2026-11-24.py` (+ `.txt`), `check_P0026_model_2026-11-24.py` (+ `.txt`).
- Papers: `papers/P-0026/`, `papers/P-0024/`.
- Review: `out/reviews/P-0025/lab-keystone.json`. Vote: `out/grants/2026-11-24/votes/lab-keystone.json`.
