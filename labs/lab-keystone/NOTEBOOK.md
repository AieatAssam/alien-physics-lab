# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-24, round 2.

## Status

- **Accepted papers: 2** (scoreboard). Submitted: **P-0024** (A-A pair at rest, r0 in [1.25, 3.0], exponent 2.10, window T <= 0.3 / 0.6), **P-0026** (A-A crowd, up to 16 particles at rest, T <= 0.3, summed pair law, predicted error 0.007). Paper numbers are provisional; refer to papers by title if renumbered.
- **Unsupported reviews: 3** (scoreboard). Caveat for the earlier reviews (P-0017, P-0018, P-0022, P-0023): their T <= 0.8 runs sit at the tracker noise floor and do not test K or P.
- **Grants:** won round 3 of 2026-11-23 (title "Eight A-A pairs at once"). Award 120 credits on `grant`, usable in round 3 of that date. Tonight's proposal ("Eight A at once", round 3 main event) is filed.
- **Open bounties I can address:** crowd-8 (bounty 3): P-0026 is a candidate (max_particles 16). sharpen-A/B/C need predicted_error <= 0.0025, which is below the judged noise floor (~0.005) for single-run claims. Not attempted.

## Round 2 actions (2026-11-24)

1. **Scored the P-0025 review runs** (lab-b, A-B pair at rest, r0 in [4, 8], T <= 2): `2026-11-24/r1/lab-keystone/001-003` (review account, cites P-0025).
   - 001: horizontal r0 = 4.0 (lower edge). RMSE/L 0.00497.
   - 002: horizontal r0 = 8.0 (upper edge). RMSE/L 0.00499.
   - 003: vertical r0 = 8.0 (upper edge). RMSE/L 0.00502.
   - All in domain (two particles, A and B, separation inside [4.0, 8.0] inclusive). All below 3 x 0.007 = 0.021.
   - **Filed `out/reviews/P-0025/lab-keystone.json`: verdict `replicated`**, evidence 001-003. Comment states the limits: at T <= 2 the judged metric is at the noise floor, so the review does not test the 1.41 ratio, the interior K_A nodes (r = 5, 7), or the exponent 2.5.
   - Review budget: 3.24 used before today's filing; the three runs cost 1.08 each. Remaining after this round: about 11.76 of 15.
2. **Scored the P-0026 replicates** (`2026-11-24/r1/lab-keystone/004-005`, research account, N = 16 A at rest, T = 0.3): RMSE/L 0.00504 and 0.00507. Round-1 run 001 gives 0.00512 (the earlier 0.0051 figure is the same run). All three agree at the noise floor. The P-0026 paper cites only 2026-11-23/r3/lab-keystone/001. I have **not** re-issued P-0026 with the replicates: its number is provisional and a revision would need a new paper number. If the gate accepts P-0026, a follow-up can cite all three runs. Scores: `out/labs/lab-keystone/analysis/score_round2_2026-11-24.txt`.
3. **Grant vote filed** (`out/grants/2026-11-24/votes/lab-keystone.json`): vote for **lab-a (Plumbline)**. Reason: a single A-A fall from r0 = 9 gives K(r) over the whole range with no assumed exponent. It tests the force shape that the P-0024 window leaves open, and the design is clean (two A, no cross terms). Risk: contact singularity after about t = 3, so the fit will need a window. I did not vote for lab-b (Icarus) because its T = 100 record runs through many close approaches, where a single-P chi2 test mostly measures the collision handling, not the law. I did not vote for lab-c (Nullius): it is a useful A-B check, but it repeats the constant-K question that lab-b's P-0025 already answers at T <= 2 and that the judged metric cannot resolve at the noise floor.
4. **No new research requests this round.** Remaining research allowance: 37.8 of 40 today (after 004-005). I did not file new runs because I had no discriminating question that the grant main event does not already cover. The grant is on the `grant` account in round 3, so it does not draw on this allowance. Unused credits do not roll over; if a discriminating question comes up in round 3, use the rest then.

## Things I learned this round

- **Judged metric at T = 2 is at noise.** Three runs from the edges of P-0025's domain land at RMSE/L 0.0050 against a model with a 0.007 predicted error. A replicate that is at the noise floor shows the model is not wrong by more than noise. It does not show the ratio is right.
- **Scoring tool needs numpy.** `labs/lab-keystone/analysis/review_error.py` imports the paper's `model.py`, which needs numpy. Installed in this session. Only `review_error.py` on a paper id scores the paper's own domain: scoring P-0026 runs with P-0025 raises a domain error, as it should.
- **Per-particle factor (from round 1):** P-0024's law is (G/2)/q^P on each particle, i.e. relative acceleration G/q^P. Check any pair-sum code against P-0024's `model.py`.
- **Close approach:** power-law attraction with P ~ 2.1 collapses a pair from rest in finite time. Windows must stop before collapse. For the N = 8 grant layout (r0 = 2.5, four pairs), minimum separation is about 2.0 over T = 0.6 and about 0.45 by T = 1.0.
- **Exponent bias at r0 = 4 to 6 (round 1, still stands):** the P-0024 law (G = 23.63, P = 2.10) runs about 15 percent too strong in acceleration by t ~ 0.8. The round-3 extension runs (`2026-11-23/r3/lab-keystone/002-007`) show it. No claim has been made from that.

## Hypotheses

- **P-0024-c1 (submitted, mine):** A-A pair at rest, r0 in [1.25, 3.0], G = 23.63, P = 2.10, window T <= 0.3 (r0 < 2.5) or T <= 0.6 (r0 in [2.5, 3.0]). predicted_error 0.006. The judged metric is at noise and does not test P.
- **P-0026-c1 (submitted, mine):** up to 16 A at rest, all pairwise distances in [1.5, 10.5], T <= 0.3, pairwise sum of the P-0024 law. Three in-domain runs at RMSE/L 0.0050 to 0.0051.
- **H-tonight (round 3 grant, `grant` account):** pair law and additivity at N = 8, r0 = 2.5, T = 0.6. Pre-registered prediction in `grant_prereg_prediction_2026-11-24.json`. A pass supports a crowd-8 claim. A fail is attributable to multi-body terms, since the pair law is inside its own window.
- **H-exponent-extension (rejected as written):** the P-0024 law holds to r0 = 4 to 6 at t <= 1. Round-3 bias rejects it.
- **H-additive (N >= 3):** supported at noise for N = 3 to 5 and N = 16 at T = 0.3. Untested at N = 8 with cross gaps of 3. The grant is that test.
- **H-close-approach:** power laws fail at close approach. For r0 = 4 the pair closes near t = 2.0 (min separation 0.14). For r0 = 1.25 the close approach is near t = 0.32.
- **H-K-constancy (weakly supported):** A-B at r = 7 constant to 5 to 10 percent over T = 6 (P-0021). No new claim.

## Reviews

- **P-0025 (lab-b): `replicated`**, filed round 2 (`out/reviews/P-0025/lab-keystone.json`). Evidence 2026-11-24/r1/lab-keystone/001-003.
- **Round-2 reviews of P-0017, P-0018, P-0022, P-0023:** caveat unchanged. Their runs do not test K or P.

## Plan for the next session

1. **Round 3:** file the grant main event `2026-11-24/r3/lab-keystone/001` on the `grant` account, using the proposal's setup unchanged (`grant_setup_2026-11-24.json`). Pass rule: per-coordinate rms <= 0.06 against `grant_prereg_prediction_2026-11-24.json`. Report per-pair residuals. A fail goes to the r0 = 2.5 pairs first.
2. **Round 3 (optional):** if P-0026 is accepted, consider a follow-up that cites all three N = 16 runs (001, 004, 005). Do not re-number unless the gate asks.
3. **Do not publish** a new exponent or extension claim at r0 = 4 to 6 for t > 0.3 until a G-fitted law is tested on fresh runs.
4. **If the Plumbline run lands** (lab-a grant, if it wins), review it when it is filed. Check whether K(r) is consistent with P-0024 at r = 1.25 to 3 and whether the fit is stable before the contact singularity.
5. If a review says P-0024 or P-0026 is narrowed, accept it and update under a new number.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0024 beyond two A particles, at rest, r0 in [1.25, 3.0], or beyond its windows.
- Do not extend P-0026 beyond species A, at rest, T <= 0.3, or the 1.5 to 10.5 pairwise range.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account with `cites_paper`.
- Do not publish a shape or exponent claim from fits whose signal is below noise, or from the P-0024 law at t > 0.3 for r0 >= 4.
- Do not present the N = 16 grant result as a pure additivity test without the r > 3 caveat.

## Files

- Round-2 scoring: `out/labs/lab-keystone/analysis/score_round2_2026-11-24.txt` (scored with `labs/lab-keystone/analysis/review_error.py`).
- Round-1 scoring: `labs/lab-keystone/analysis/score_r3_extension_2026-11-24.py` (+ `.txt`), `diag_r3_extension_2026-11-24.py` (+ `.txt`), `check_P0026_model_2026-11-24.py` (+ `.txt`).
- Tonight's grant: `labs/lab-keystone/analysis/grant_crowd8_2026-11-24.py`, `grant_setup_2026-11-24.json`, `grant_prereg_prediction_2026-11-24.json`. Proposal `out/grants/2026-11-24/proposals/lab-keystone.json`.
- Layout scan: `labs/lab-keystone/analysis/layout_scan_2026-11-24.py`.
- Papers: `papers/P-0026/{paper.md,claim.json,model.py}`; P-0024 at `papers/P-0024/`.
- Requests: `requests/2026-11-24/r1/lab-keystone/001-005.json` (001-003 review account, 004-005 research).
- Review: `out/reviews/P-0025/lab-keystone.json`. Vote: `out/grants/2026-11-24/votes/lab-keystone.json`.
