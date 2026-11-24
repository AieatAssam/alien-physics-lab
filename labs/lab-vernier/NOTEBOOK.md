# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-24, round 2.

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error (the judged bar). Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. Say which verdict I am making and check the bar for that verdict.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions (4.5, 5.5, ...) for exact-edge domains. Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling (new, round 2).** The cost is `1 + k * particles * duration`, which does not depend on sample count. Always set `sample_dt = duration / 2000` (the cap). Earlier runs at dt 0.005 threw away about a factor of sqrt(10) to sqrt(20) in precision.
5. **Full-window fits through a close pass are invalid (new, round 2).** A P = 2.5 pair law cannot follow a pair that falls to separation about 0.2 and rebounds. The round-3 runs r3/015, 016, 017, 019, 021, 022 gave residuals 0.017 to 0.058 RMSE/L in full-window fits (about 10 times the tracker floor). Those K values are retracted. Use pre-contact windows (samples while separation >= 1.0), as in `fit_K_P25_precontact_2026-11-24.py`.
6. **Bars are loose at T <= 0.3.** The judged RMSE/L bar at close range is about 0.024 (0.24 absolute). The zero-force null is only about 0.009 RMSE/L there, so those reviews can replicate but cannot falsify. The comment must say so.
7. **Label K by the window's mean separation**, not by the start separation. A window fit at P fixed = 2.5 gives K_eff(r) = a(r) r^2.5 at the mean r of the window.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result so far. Independent of `sample_dt`.

## Round-3 results, re-analysed (2026-11-23 r3, runs 011 to 022)

Pre-contact windows, P fixed 2.5, K fitted alone. Source: `analysis/fit_K_P25_precontact_2026-11-24.py`, table in `analysis/round3_precontact_table_2026-11-24.jsonl`.

| pair | r0 | runs | mean sep in window | K_eff (P = 2.5 frame) | per-run K | rmse/L |
|---|---|---|---|---|---|---|
| A-B | 1.5 | 011-014 | 1.36 | **6.70 +/- 0.13** | 6.62, 6.37, 6.86, 6.96 | 0.0048 to 0.0054 |
| A-B | 2.5 | 017-018 | 2.06 | **8.36 +/- 0.04** | 8.39, 8.33 | 0.0049 to 0.0050 |
| A-B | 3.0 | 015-016 | 2.44 | **8.74 +/- 0.02** | 8.75, 8.74 | 0.0051 |
| A-A | 2.0 | 019-020 | 1.70 | **15.40 +/- 0.15** | 15.48, 15.32 | 0.0048 to 0.0054 |
| A-A | 3.0 | 021-022 | 2.44 | **17.58 +/- 0.05** | 17.60, 17.56 | 0.0050 to 0.0052 |

All windows fit at the tracker noise floor (rmse/L about 0.005, noise sd 0.05).

What this says:
- **Constant K at P = 2.5 is rejected for A-B.** K_A(B) rises from 6.70 (r about 1.4) to 8.36 (r about 2.1) to 8.74 (r about 2.4). Constant K at the P-0022 value 7.6 is about 7 SE from the r about 1.4 window.
- **Local exponents** (p = 2.5 - dlnK_eff/dlnr). A-B from r 1.36 to 2.44: p = 2.05. A-B from 2.06 to 2.44: p = 2.23. A-A from 1.70 to 2.44: p = 2.13. Both pairs have local exponent near 2.1 at short range.
- **P-0022's K = 7.59 at "separation 2"** is consistent with a window whose mean separation is about 1.7 (it falls from 2.0 and the window averages across r). The label is the issue, not the fit.
- **A-A: P-0024's exponent form** (G/2 = 11.815, P = 2.099) gives K_eff = 11.815 r^0.4 in the P = 2.5 frame, i.e. 14.61 at r 1.70 and 16.88 at r 2.44. Observed 15.40 and 17.58. The observed K_eff is about 5 percent above the P-0024 form in this band. That is about 4 SE at the window-mean labelling, and that labelling is approximate, so treat it as a lead, not a result.

### Corrections to round-3 notes (kept)

1. The round-3 full-window K values (A-B r0 3 = 2.03; A-A r0 3 = 11.3; and the "9.8" A-A r0 2 value) are invalid. They come from `fit_r3_H24_H25_2026-11-24.py`, which fits through the close pass. Do not use them.
2. The round-3 pre-registered prediction "19.3 under P-0024" at A-A r0 3 was an arithmetic error. The P-0024 form gives 16.9 at mean separation 2.44. Observed 17.6. Constant K (13.55) is rejected.
3. The round-3 prediction "8.2" at A-B r0 2.5 was low; observed 8.36 +/- 0.04.
4. The round-3 pre-registered H24 prediction at r0 1.5 ("6.5 +/- 0.4") was close: observed 6.70 +/- 0.13.
5. **P-0013 review.** The round-3 notebook said "held". `reviews/P-0013/lab-vernier.json` exists (replicated, A-A part only, evidence r3/001-004). I re-scored today: the paper's model gives RMSE/L 0.0049 to 0.0052 against bar 0.030. The review stands.
6. **P-0018 and P-0020 reviews** (filed round 3, replicated). Re-scored today: P-0018 gives 0.0047 to 0.0052; P-0020 gives 0.0052 to 0.0055. Both are within the bar of 0.024. Both stand, with the caveat in the comments that the bar cannot resolve K to better than about 20 percent.

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported. P-0011.
- **H2** (species-independent noise): supported.
- **H3** (no clipping near a wall): supported.
- **H4** (no sample-timing offset): supported.
- **H5** (stationarity over T = 100): mean supported; x-spread variation not reproduced.
- **H6** (P-0003 domain): separation 3 fails for P-0003 (r1/007). Separations 4 and 5 pass.
- **H7** (P-0006 shared-law factor at separation 9): supported within 3 percent.
- **H8** (P-0008 coefficients flat over separations 3 to 5): supported for A-B and B-C; not for A-A at 3 and 4.
- **H9** (P-0010 far-field G(r0)): replicated at all three pairs and A-A at 6.
- **H10** (A-A coefficient at separation 4 is 17.70): supported by the diagonal replicate.
- **H11** (close-range B-C): supported (P-0015).
- **H12** (A-B and B-B not constant-K over the first 0.3 time units at r = 1): open.
- **H13** (pairwise superposition, N > 2): **untested by me.** Keystone's round-2 grant run (N = 8) and my review of P-0026 (N = 16, review runs 101-104) are the tests.
- **H15** (P-0004-c2 magnitude): K_C(A) about -20.7 from three repeats, published -21.38. Flagged.
- **H16** (P-0014 A-A contact failure): integrator blows up after close approach.
- **H17** (K_B(A)/K_A(B) = 1.41 at all separations): supported at the round-3 windows. Round-3 ratios 1.37 to 1.52. Re-check with dense data (round 2 runs 005-018).
- **H20** (state dependence): not supported at the 3-SE rule (round 2, n = 16).
- **H21** (orientation invariance for A-B): not falsified at 3 percent.
- **H24** (K_eff(r) for A-B at P = 2.5 is not constant; separation dependence): **supported at the 6 SE level between r about 1.4 and 2.4**. Shape from points labelled by mean separation: 6.70 (1.36), 8.36 (2.06), 8.74 (2.44), about 9.2 (r about 4.1, unverified), about 8.4 (4.8), about 8.3 (5.9), about 7.5 (6.4), 7.75 (7, P-0021), 6.16 (9, P-0023). Local exponent rises from about 2.05 at short range to about 3 at r 4 to 9. A single power law cannot describe the whole band.
- **H25** (A-A exponent differs from A-B exponent): **not supported at present.** Both show local exponent near 2.1 at r 1.4 to 2.4 (A-A 2.13, A-B 2.05). The difference, if any, is at r above 2.5 and is not yet tested with clean windows. P-0024's exponent 2.10 is consistent with the A-A band data to about 5 percent in K_eff.
- **H26** (new, working): the A-B force is r-dependent in a way a single power law cannot fit. A screened or cut-off form (for example K r^-p exp(-r/lambda)) would give a local exponent that rises with r. This matches the data qualitatively. A fit has not been done.
- **H27** (new, open): B-B K at r = 1 is either 3.86 (P-0019) or 3.98 (P-0017). Dense runs in round 2 (001, 002, 027) settle this if the difference is above about 0.03. Not decided yet.

## Round 2 (2026-11-24): what I filed

Script: `analysis/design_round2_2026-11-24.py` (requests; review setups checked against each paper's `predict()`; all 14 review setups pass). Requests in `out/requests/2026-11-24/r2/lab-vernier/`, all 41 files valid by my structural check (the `jsonschema` package is not installed here; I checked the schema keys, sample count, and particle count by hand).

Every run uses `sample_dt = duration / 2000` (dense sampling, rule 4).

### Research account (27 runs, 28.48 of 40 credits)

| request | pair | r0 | orientation | T | purpose |
|---|---|---|---|---|---|
| 001, 002, 027 | B-B | 1.0 | H, V, D | 0.3 | precise K_B(B) at r = 1 (H27) |
| 003, 004 | B-B | 2.5 | H, V | 1.0 | B-B shape vs r (H24 generality) |
| 005, 006, 007 | A-B | 1.5 | H, V, D | 0.5 | short-range K_eff, three orientations |
| 008, 009, 010 | A-B | 2.5 | H, V, D | 1.0 | K_eff at r about 2.1 (pre-contact) |
| 011, 012 | A-B | 3.0 | H, V | 1.5 | K_eff at r about 2.4 |
| 013, 014 | A-B | 4.0 | H, V | 1.5 | K_eff at r about 3.5 to 4 |
| 015, 016 | A-B | 6.0 | H, V | 2.0 | K_eff at r about 5 |
| 017 | A-B | 9.0 | H | 10.0 | long approach, K_eff at r 6 to 9 |
| 018 | A-B | 9.0 | V | 5.0 | orientation check at r 9 |
| 019, 020 | A-A | 1.0 | H, V | 0.15 | A-A at r 1 (P-0012 says K 11.3) |
| 021, 022 | A-A | 2.0 | H, V | 0.5 | A-A K_eff at r about 1.7 |
| 023, 026 | A-A | 2.5 | H, V | 0.6 | inside P-0024's window, orientations |
| 024, 025 | A-A | 3.0 | H, V | 1.1 | A-A K_eff at r about 2.4 |

Remaining research allowance: about 11.5 credits, kept for a round-3 follow-up (unused credits do not roll over, so spend them if round 3 needs no follow-up).

### Review account (14 runs, 14.53 of 15 credits)

| request | paper | design | bar (3 x predicted_error) |
|---|---|---|---|
| 101-104 | P-0026 | 16 A at rest, four irregular lattices, min separation 2.15, T = 0.3 | 0.021 RMSE/L |
| 105-108 | P-0024 | A-A at rest, r0 = 2.5 (H, V, H, V), T = 0.6 | 0.018 RMSE/L |
| 109-111 | P-0012 | A-A at rest, r0 exactly 1.0 (H, V, H), T = 0.15 | 0.024 RMSE/L |
| 112-114 | P-0019 | B-B at rest, r0 exactly 1.0 (H, V, H), T = 0.3 | 0.024 RMSE/L |

Not reviewed this round: P-0017 (B-B, K 3.98). The review budget (0.47 left) does not cover three more runs. It can be done on day 2026-11-25 or in round 3 if the research and review budgets allow.

## Pre-registered predictions (written before any round-2 results)

Results arrive in round 3. These are my expectations; a mismatch is a result.

- **B-B r0 1.0 (001, 002, 027):** K_B(B) mean across three orientations. P-0019 (3.86) and P-0017 (3.98) differ by 3 percent. Dense sampling should give a precision of about 0.03 per run (my estimate). Decision rule: if the mean is within 0.05 of 3.86 and not within 0.05 of 3.98, P-0019 is favoured. The reverse for P-0017. Otherwise neither.
- **A-B r0 1.5 (005, 006, 007):** K_eff about 6.70 at mean r 1.36 (round-3 value). Predict 6.7 +/- 0.1. A mean differing from 6.70 by more than 0.3 means the round-3 windows were biased.
- **A-B r0 2.5 (008, 009, 010):** K_eff about 8.36 at mean r about 2.06. Predict 8.36 +/- 0.05.
- **A-B r0 3.0 (011, 012):** K_eff about 8.74 at mean r about 2.44. Predict 8.74 +/- 0.05.
- **A-B r0 4.0 (013, 014):** predict K_eff of about 9.0 at mean r about 3.5. This is a guess (the notebook's 9.2 is unverified). Constant K at 8.4 would be rejected at about 3 SE.
- **A-B r0 6.0 and 9.0 (015-018):** predict K_eff about 8.0 at r 5 (015, 016) and about 6.5 at r 7 to 8 (017, 018). These values are weak predictions.
- **A-A r0 1.0 (019, 020):** P-0012 (K 11.3, constant) and P-0024's form (11.815 r^0.4 = 11.8 at r 1) differ by 4 percent. Predict 11.5 +/- 0.2 (between the two). A value above 12.0 or below 11.0 would falsify both at this precision.
- **A-A r0 2.0 (021, 022):** predict K_eff 15.4 +/- 0.1 at mean r 1.70 (round-3 value).
- **A-A r0 2.5 (023, 026):** P-0024's form, K_eff = 11.815 * q^0.4 in the P = 2.5 frame, gives 15.9 at a mean separation of 2.1 (the window mean is my guess; the fit will label it). Predict 15.9 +/- 0.3, with the round-3 trend as a cross-check.
- **A-A r0 3.0 (024, 025):** predict 17.6 +/- 0.05 (round-3 value).

Review predictions (paper model against my runs):
- **P-0026 (101-104):** RMSE/L about 0.002 to 0.005. The pairwise-additive law should pass. A fail above 0.021 would be a multi-body failure, and then the falsification rule applies. The null is not computed here (N = 16 null is large), so run it before judging.
- **P-0024 (105-108):** RMSE/L about 0.002 to 0.004, because the model's K_eff is within about 5 percent of my K_eff. The zero-force null at r0 2.5, T 0.6 is 0.022 RMSE/L (bar 0.018), so falsification is possible in principle, but I expect replication.
- **P-0012 (109-111):** RMSE/L about 0.005. Replication only; the null is 0.009 against a bar of 0.024.
- **P-0019 (112-114):** RMSE/L about 0.005. Replication only, and the bar cannot separate K = 3.86 from 3.98.

## Round-3 plan (same day, 2026-11-24)

1. Check the results of 001-027 (research) and 101-114 (review): status, cost, budget_remaining.
2. **Reviews.** Compute the paper model's RMSE/L on each review run with `analysis/score_reviews_2026-11-24.py` (run with `-I`, `PAPERS` pointing at the repo's papers). File P-0026, P-0024, P-0012 and P-0019 only where at least 3 of the cited in-domain runs meet the bar (replicated), or where all the cited runs exceed the bar (falsified, after checking that the zero-force null is above the bar). Otherwise file nothing.
3. **Dense K map.** Pre-contact fits on the research runs with `fit_K_P25_precontact` adapted to the 2026-11-24 ids. Compare with the predictions above. Then fit K(r) by a single screened form (H26) and a single power law, and compare chi2 on the whole map.
4. **Publish** the narrowest solid claims supported by dense data. Candidates, each with a domain and a predicted_error near the measured precision (0.005 or larger):
   - A-B at rest, r0 in [2.45, 2.55], duration at most 1.0: K_A(B) = 8.36 (P = 2.5). Evidence 008-010 (and 017-018 from round 3).
   - A-B at rest, r0 in [1.45, 1.55], duration at most 0.5: K_A(B) = 6.7 (P = 2.5).
   - A-A at rest, r0 in [1.95, 2.05], duration at most 0.5: K_AA = 15.4 (P = 2.5).
   Use the next free paper number (P-0027 at last count; the gate can renumber, so refer to papers by title in this notebook).
5. Use any remaining research credits (about 11.5) for the least precise point in the map.
6. **Grant.** Voted lab-keystone (`out/grants/2026-11-24/votes/lab-vernier.json`). No proposal filed by me tonight.

## Grant

- **2026-11-24 vote: lab-keystone.** Reason: their N = 8 run is the only proposal testing pairwise additivity beyond two bodies (H13), which P-0026 and crowd-8 depend on. Pre-registered pass and fail, 1.1 credits. Plumbline's and Nullius's runs overlap the dense K(r) map I am running myself.
- Earlier: round-2 2026-11-23 vote for lab-keystone (on file).

## Open problems: assessment

- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025):** not reachable with noise sd 0.05 at my cost (per-run K precision is about 1 percent, but the judged bar is about 0.005 RMSE/L). Do not file.
- **close-AB (bounty 2), close-AC (bounty 2):** need r_range starting at 1 or less. Blocked by H12.
- **crowd-8 (bounty 3):** multi-body. Keystone's round-2 run and my review of P-0026 both test it (H13).
- **contested-P-0014, disputed-P-0003, -P-0006, -P-0007:** not addressed.

## Reviews: other papers

- **P-0022 (Icarus, A-B at r 2):** replicated (round 2). Verified round 3. The window's mean separation is about 1.7, not 2.0.
- **P-0018 (Icarus), P-0020 (Icarus):** replicated (round 3). Verified today.
- **P-0013 (Nullius, A-A/A-C/C-C at r 1.5):** replicated (A-A part only). Verified today.
- **P-0012 (Plumbline), P-0019 (Plumbline), P-0024 (Keystone), P-0026 (Keystone):** runs filed today; reviews after round 3 results.
- **P-0017 (Icarus, B-B K 3.98):** not reviewed. Budget.

## Budgets (2026-11-24, after round-2 filing)

- **Research:** 40 allowed. Filed round 2: 28.48. **Remaining 11.52** (reserved for round 3).
- **Review:** 15 allowed. Filed round 2: 14.53. **Remaining 0.47** (no run of the cheapest kind fits).
- **Grant:** none for this lab (no award tonight).

## Not read

`gate/`, `tools/`, `exam_papers.json`, the predictor and score files. I did not read them and will not.
