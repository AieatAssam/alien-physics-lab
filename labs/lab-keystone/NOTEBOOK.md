# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-24, round 3.

## Status

- **Accepted papers: 2** (scoreboard). Submitted: **P-0024** (A-A pair at rest, r0 in [1.25, 3.0], exponent 2.10, window T <= 0.3 / 0.6), **P-0026** (A-A crowd, up to 16 particles at rest, T <= 0.3, summed pair law, predicted error 0.007). Paper numbers are provisional; refer to papers by title if renumbered.
- **Unsupported reviews: 3** (scoreboard). Caveat for the earlier reviews (P-0017, P-0018, P-0022, P-0023): their T <= 0.8 runs sit at the tracker noise floor and do not test K or P.
- **Grants:** won round 3 of 2026-11-23 ("Eight A-A pairs at once"). **Tonight's grant (2026-11-24) went to Plumbline (lab-a)**, not to me. My grant allowance today is 0, so the round-3 grant main event I planned in round 2 is **void**. Nothing was filed on the `grant` account tonight.
- **Open bounties I can address:** crowd-8 (bounty 3): P-0026 is a candidate (max_particles 16). sharpen-A/B/C need predicted_error <= 0.0025, below the judged noise floor (~0.005) for single-run claims. Not attempted.

## Round 3 actions (2026-11-24)

1. **Review of P-0027 (lab-a, Plumbline; A-A pair at rest, r0 in [3, 9], K(r) table, supersedes P-0003). Not yet filed.** The review needs results that do not exist yet (round 3 results are produced after this session). Requests are filed; the verdict will be decided when they land, under the rules pre-registered in `analysis/prereg_review_P0027_2026-11-24.json`.
   - **Concern found in P-0027's own model (not yet tested by data).** `model.py` evaluates K with `np.interp`, which clamps K to K(3) below r = 3 and K(9) above 9. Its own window claim ("closest approach well above contact") is not met at the window ends. My copy of the paper's RK4 (`analysis/p0027_edge_sim_2026-11-24.py`) gives:
     - r0 = 3.0, T = 1.5: minimum separation 0.044 at t ~ 1.45, then the singular force sends the pair through contact. Separation at T = 1.5 reads 8.1, which is a numerical artifact, not physics.
     - r0 = 4.0, T = 2.0: minimum separation 0.027 at t = 2.0.
     - r0 = 3.0, T = 1.0 (control): minimum 1.58, away from contact.
     - A pair at 0.04 separation is inside the tracker noise (0.05 per coordinate), so the claim cannot be checked there with the judged metric.
   - **Consequence for the claim:** the table is measured only on [3, 9], so separations below 3 (reached by every r0 = 3 run within the window) are an unmeasured extrapolation. The judged error at the window edge is the test that matters.
   - **Filed requests (review account, `cites_paper` P-0027), `requests/…` in `out/requests/2026-11-24/r3/lab-keystone/`:**
     - 001: r0 = 3.0 horizontal, T = 1.5 (cost 1.06)
     - 002: r0 = 3.0 diagonal, T = 1.5 (cost 1.06)
     - 003: r0 = 4.0 horizontal, T = 2.0 (cost 1.08)
     - 004: r0 = 3.0 horizontal, T = 1.0 control (cost 1.04)
     - 005: r0 = 4.0 diagonal, T = 2.0 (cost 1.08)
     - Total 5.32 review credits. Review used after filing: 3.24 + 5.32 = 8.56 of 15 (6.44 left). Research unchanged: 2.2 used, 37.8 left.
   - **Reasoning for the verdict (to be checked against results).** Cited runs must be in domain (species A, N = 2, separation inside [3, 9]). The paper's model refuses out-of-window durations, so out-of-window runs cannot count. The bar is 3 x 0.007 = 0.021 judged RMSE/L. The judged metric is at the noise floor (~0.005) for interior runs, so a "replicated" verdict on interior runs would be weak evidence. Edge runs are where a failure could show.
2. **No research runs filed this round.** I did not find a discriminating question beyond the P-0027 edge test. Remaining research allowance: 37.8 of 40 today.
3. **Scoring tools.** `labs/lab-keystone/analysis/review_error.py` still works (needs numpy; installed this session with `pip install numpy`). Round-3 scoring has not been run yet.

## Things I learned this round

- **Judged metric at T = 2 is at noise.** Three runs from the edges of P-0025's domain land at RMSE/L 0.0050 against a model with a 0.007 predicted error. A replicate at the noise floor shows the model is not wrong by more than noise. It does not show the ratio is right.
- **P-0027's window claim fails at its ends** (see above). Its model is singular at contact; "well above contact" is false for r0 = 3 at T = 1.5 and for r0 = 4 at T = 2.0.
- **Judge rules (`tools/editor.py`, `stands()`).** `falsified` needs all cited rows to be scored and above the bar. `replicated` needs >= 3 cited rows that are not the paper's own evidence and are within the bar. `narrowed` and `inconclusive` have no reputation effect.
- **Per-particle factor (round 1):** P-0024's law is (G/2)/q^P on each particle, i.e. relative acceleration G/q^P. Check any pair-sum code against P-0024's `model.py`.
- **Close approach:** power-law attraction with P ~ 2.1 collapses a pair from rest in finite time. Windows must stop before collapse. For the N = 8 layout, minimum separation is about 2.0 over T = 0.6.
- **Exponent bias at r0 = 4 to 6 (round 1, still stands):** the P-0024 law (G = 23.63, P = 2.10) runs about 15 percent too strong in acceleration by t ~ 0.8. Round-3 extension runs (`2026-11-23/r3/lab-keystone/002-007`) show it. No claim from that.

## Hypotheses

- **P-0024-c1 (submitted, mine):** A-A pair at rest, r0 in [1.25, 3.0], G = 23.63, P = 2.10, window T <= 0.3 (r0 < 2.5) or T <= 0.6 (r0 in [2.5, 3.0]). predicted_error 0.006. The judged metric is at noise and does not test P.
- **P-0026-c1 (submitted, mine):** up to 16 A at rest, all pairwise distances in [1.5, 10.5], T <= 0.3, pairwise sum of the P-0024 law. Three in-domain runs at RMSE/L 0.0050 to 0.0051.
- **H-additive (N >= 3):** supported at noise for N = 3 to 5 and N = 16 at T = 0.3. Untested at N = 8 with cross gaps of 3 (the grant run that was not filed tonight).
- **H-close-approach:** power laws fail at close approach. For r0 = 4 the pair closes near t = 2.0 (min separation 0.14 with the P-0024 law, 0.03 with P-0027). For r0 = 1.25 the close approach is near t = 0.32.
- **H-K-constancy (weakly supported):** A-B at r = 7 constant to 5 to 10 percent over T = 6 (P-0021). No new claim.

## Reviews

- **P-0025 (lab-b): `replicated`**, filed round 2 (`out/reviews/P-0025/lab-keystone.json`). Evidence 2026-11-24/r1/lab-keystone/001-003.
- **P-0027 (lab-a): pending.** Runs 2026-11-24/r3/lab-keystone/001-005 (requests filed, results not yet in). Verdict per the pre-registration; file `out/reviews/P-0027/lab-keystone.json` only after scoring.
- **Round-2 reviews of P-0017, P-0018, P-0022, P-0023:** caveat unchanged. Their runs do not test K or P.

## Plan for the next session

1. **Score P-0027 runs** `2026-11-24/r3/lab-keystone/001-005` with `review_error.py P-0027 ...` once results exist. Use the decision rules in the pre-registration file, not the outcome. File the review under `out/reviews/P-0027/lab-keystone.json`. If the verdict is `falsified` or `replicated`, cite only in-domain runs and check the >= 3 / all-above-bar counts.
2. **If P-0027 falsified at the window ends:** the table may still hold on [3, 9] at shorter times. Propose a narrowed domain in a new paper, and do not claim contact behaviour.
3. **Round 3 (optional):** if P-0026 is accepted, consider a follow-up that cites all three N = 16 runs (001, 004, 005). Do not renumber unless the gate asks.
4. **Do not publish** a new exponent or extension claim at r0 = 4 to 6 for t > 0.3 until a G-fitted law is tested on fresh runs.
5. If a review says P-0024 or P-0026 is narrowed, accept it and update under a new number.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0024 beyond two A particles, at rest, r0 in [1.25, 3.0], or beyond its windows.
- Do not extend P-0026 beyond species A, at rest, T <= 0.3, or the 1.5 to 10.5 pairwise range.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account with `cites_paper`.
- Do not present the N = 16 result as a pure additivity test without the r > 3 caveat.
- Do not plan grant runs unless my lab won the grant for that night (the grant award is in the ledger).

## Files

- Round-3 review requests: `out/requests/2026-11-24/r3/lab-keystone/001-005.json` (review account, cites P-0027); generator `analysis/make_review_requests_r3_2026-11-24.py`.
- Pre-registration: `analysis/prereg_review_P0027_2026-11-24.json`.
- P-0027 edge sim: `analysis/p0027_edge_sim_2026-11-24.py` (paper's RK4 with the K clamp; output as above).
- Round-2 scoring: `analysis/score_round2_2026-11-24.txt` (scored with `labs/lab-keystone/analysis/review_error.py`).
- Round-1 scoring: `analysis/score_r3_extension_2026-11-24.py` (+ `.txt`), `diag_r3_extension_2026-11-24.py` (+ `.txt`), `check_P0026_model_2026-11-24.py` (+ `.txt`).
- Papers: `papers/P-0026/`, `papers/P-0024/`.
- Review: `out/reviews/P-0025/lab-keystone.json`. Vote: `out/grants/2026-11-24/votes/lab-keystone.json`.
