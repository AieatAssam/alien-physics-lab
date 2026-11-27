# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely, and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-27, round 2 (edge-run scoring, contact-probe analysis, follow-up requests, review update, vote).

## Round 2 summary (2026-11-27)

- **Round-1 edge runs scored (P-0035 review, 2026-11-27/r1/lab-vernier/003 to 005, review account):**
  - Judge score (`analysis/judge_score.py`, run with `python3 -I`): 003 (r0 2.75 horizontal) 0.00497; 004 (2.75 vertical) 0.00500; 005 (2.75 at the 2.0 wall corner) 0.00502. Bar 0.018. All in domain, all at the noise floor. Pre-registered prediction (about 0.005) matched.
  - **P-0035 review updated** (`out/reviews/P-0035/lab-vernier.json`): verdict stays **replicated**, now over the full stated r_range 2.0 to 2.75 (seven in-domain ids: 008 to 011 and 003 to 005). The review no longer carries the "covers 2.0 to 2.5 until edge runs report" scope note.
- **Contact probe scored** (requests 2026-11-27/r1/lab-vernier/001 and 002, research, A-A at rest, T 0.6, sample_dt 0.0003). Scripts: `analysis/contact_score_2026-11-27.py`, `analysis/contact_fit_2026-11-27.py`, `analysis/contact_softcore_window_2026-11-27.py`. Full results below. **H37 has no clean verdict.** None of the three pre-registered outcomes matches the data.
- **Follow-up requests filed this round** (research account, 2026-11-27/r2/lab-vernier/001 to 003): see the pre-registration table below. Cost 1.024 + 1.024 + 1.08 = 3.13.
- **Round-2 vote (`out/grants/2026-11-27/votes/lab-vernier.json`): lab-c (Nullius).** Reason: its dt-only replicate of r1-012 bears on whether the contact outcome is a sampling artefact, which would contaminate every contact measurement, including mine. Not my own proposal. Icarus (lab-b, B-B exponent) was the other strong candidate and is still untested; a future round should take it.

## Contact probe: detailed results (2026-11-27/r1, runs 001 and 002)

Bare law (P-0026, r'' = -G/r^P, G = 23.63, P = 2.099, no contact model) predicts collapse (separation 0.02, integrator floor) at t = 0.23 for r0 1.0 and t = 0.42 for r0 1.5.

**r0 = 1.0 (run 001):**
- Pre-contact: separation RMSE against the bare law is 0.073 in separation units (RMSE/L 0.007) on t <= 0.15. That is at the tracker-noise floor (separation noise about 0.07).
- Departure starts earlier than the noise can hide when smoothed (bins of 0.01, about 33 samples each, noise about 0.012 per bin). Smoothed separation vs bare: 0.46 vs 0.39 at t = 0.20; 0.36 vs 0.29 at 0.21; 0.27 vs 0.16 at 0.22. Mean bias (measured minus bare) +0.03 over the window of separations 0.15 to 0.8.
- Softened-core fits (force G/max(r, rc)^P) do not explain it: window RMSE 0.090 at rc = 0, 0.086 at rc = 0.45. So a softened core is not supported; the bias looks like a small weakening of the attraction at separation 0.2 to 0.8, not a cap. Unresolved at this sample size (about 0.03 in separation, within 2 to 3 sigma per window).
- Minimum: smoothed minimum 0.10 at t = 0.24; per-sample minimum 0.009 at t = 0.240. Below about 0.15 the tracker cannot distinguish contact from close approach.
- Post-contact (not symmetric pass-through): smoothed separation 0.62 at t = 0.30, 1.22 at 0.40, 1.48 at 0.46, 2.01 at 0.60. A time-symmetric pass-through of the bare law would be back at about 1.0 at t = 0.46 and at about 0.95 at t = 0.40. Measured is faster and larger.
- Post-contact speed: about 8 near t = 0.30 (incoming speed at separation 0.3 was about 10.9 under the bare law), decelerating to about 3.3 at separation 1.9 (t 0.58).
- **Energy estimate (bare potential, per unit reduced mass):** initial E = -21.5 at r0 1.0. At t = 0.58, E is about -5.0 (speed 3.3 at separation 1.93). Energy is not conserved through contact; the contact added about +16 under this estimate. If the bare potential holds after contact, the pair is bound with turning separation 2.7 to 8.6 across speeds 2.5 to 4.1 (3.8 at 3.3). This is the basis of the T = 2 prediction.

**r0 = 1.5 (run 002):**
- Pre-contact: separation RMSE against the bare law is 0.069 (RMSE/L 0.007) on t <= 0.37. At the noise floor. Bare law reaches 0.5 at t = 0.386; smoothed first crossing below 0.25 at t = 0.42; per-sample minimum 0.013 at t = 0.429 (bare collapse 0.42).
- Post-contact (smoothed): 0.55 at 0.50, 0.96 at 0.55, 1.07 at 0.60, maximum about 1.26 by t = 0.60 (per-sample). Symmetric pass-through would be back at 1.5 at t = 0.84. Not yet reached.
- The pre-registered outcome table (pass-through, bounce, softened) is not matched cleanly for either run. Pass-through fails the re-expansion timing; bounce fails the "few tenths" minimum (minimum below about 0.15); softened fails the rc fit (small bias only).

**H37 status:** open, no verdict. The contact outcome is not a bare law continuing and not a symmetric pass-through. The post-contact pair gains energy relative to the bare potential (inference from one run). Next test: reproducibility (r2/001), isotropy (r2/002), and the long-time outcome (r2/003).

**Note on my grant (2026-11-27, pending votes):** the pre-contact falsifier in the proposal (unclamped P-0026 law to RMSE/L 0.02 up to first separation below 0.5) is already met by runs 001 and 002 (0.007 each). The grant's remaining value is the post-contact measurement at four replicates and T = 2. Keep it, but know that its pre-contact claim is already in hand.

## Pre-registered predictions for 2026-11-27/r2 (written before results)

| request | setup | account | prediction | falsifier / bar |
|---|---|---|---|---|
| r2/001 | exact replicate of r1/001 (A-A, horizontal r0 1.0, T 0.6, dt 0.0003) | research | Smoothed separation (0.01 bins) agrees with r1/001 to 0.02 in separation units; contact is deterministic apart from tracker noise | disagreement above 0.02 means the simulator is not deterministic at contact (a serious instrument result) |
| r2/002 | A-A vertical r0 1.0, (5.0,4.5) and (5.0,5.5), T 0.6, dt 0.0003 | research | Same trace as horizontal r1/001 within 0.02 (isotropy). Separation at t = 0.60 about 2.0 (+/- 0.2) | trace differing by more than 0.02 at matched times means the post-contact rule depends on orientation |
| r2/003 | A-A horizontal r0 1.0, T 2.0, dt 0.001 | research | Bound orbit: maximum separation 2.7 to 4.5, reached near t 1.0 to 1.5, then separation falls again before t = 2.0 | maximum separation at or above 5, or still rising at t = 2.0 (ejection, energy gain above the bound estimate) |

Note on the bound-orbit prediction: it rests on a speed estimate of 3.3 (uncertain by about 0.4) at separation 1.93 at t about 0.58, which translates into a turning separation of 2.7 to 8.6 (see above). The predicted range 2.7 to 4.5 corresponds to speeds 2.5 to 3.5. A maximum above 4.5 but below 5 is "no verdict" on the ejection question; a maximum between 4.5 and 5 is also no verdict.

## Round-1 pre-registered predictions: outcomes

| request | prediction | result |
|---|---|---|
| r1/001 (r0 1.0 contact) | pre-contact follows bare law to sep 0.5 at t 0.19; post-contact one of pass-through/bounce/softened | pre-contact follows bare law to noise (sep 0.5 measured at t about 0.16 to 0.19); post-contact matches none cleanly (see above) |
| r1/002 (r0 1.5 contact) | sep 0.5 at t 0.39, collapse about 0.42 | sep 0.5 at t 0.37 (smoothed 0.39); minimum 0.013 at 0.429. Matches |
| r1/003 to 005 (P-0035 edge) | RMSE/L about 0.005 | 0.00497, 0.00500, 0.00502. Matches |

## Round-2 summary (2026-11-26), kept for the record

- Review runs (round 1 of 2026-11-26, cost 1.02 to 1.16 each): P-0031 (001 to 004), P-0033 (005 to 007), P-0032 (008 to 011). All in-domain runs at the noise floor (RMSE/L 0.00498 to 0.00506). Reviews filed: P-0031 replicated (4 of 4), P-0033 replicated (3 of 3), P-0032 replicated (4 of 4).
- Close approach from P-0032 runs (008, 011; T 0.6, r0 2.0): tracker minimum separations 0.57 and 0.51, paper's own predict gives 0.69 at T 0.6. The unclamped law fits to noise through near-contact at T 0.6.
- Grant vote cast for lab-keystone (A-B at 2.5). The 2026-11-26 award went to lab-a (votes lab-a 2, lab-vernier 2, lab-keystone 1).

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. State which verdict is being made and check the bar for that verdict. State any unreached part of the domain in the comment.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions (4.5, 5.5, 2.75, 4.75, ...) for exact-edge domains, or sit a small margin inside the edge. Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling.** The cost is `1 + k * particles * duration`, independent of sample count. Always set `sample_dt = duration / 2000` (the cap).
5. **Pre-contact windows for attractive pairs.** A full-window fit or prediction through a close pass is invalid when the integrator diverges. Scores for my own fits use the window before the first measured separation below 1.5 (or below 0.5 for contact runs). The judge scores the full run, so check the pre-contact prediction separately.
6. **Bars are loose at T <= 0.3 and in general at the 0.007 level.** A 1 to 3 percent K difference moves predicted positions by 0.001 to 0.003 RMSE/L. Falsification needs a regime change: close approach, long time, N, or a new pair.
7. **Label K by the window's mean separation**, not by the start separation.
8. **Judge domain excludes duration, but predictors do.** Several predictors refuse durations outside their window (P-0024, P-0028 T > 1.0, P-0029, P-0031 T > 2, P-0032 T > 0.6, P-0035 T > 0.6). A refused run cannot be cited as evidence.
9. **Write only under `out/`.** Analysis code and fits go in `out/labs/lab-vernier/analysis/`. The older source folder `labs/lab-vernier/analysis/` is read-only reference.
10. **Pre-register before results.** Predictions for each new run are written in this notebook before its results are read.
11. **Asymmetric layouts are in the judge domain but not in a paper's claim** when the claim says so. A miss there is "narrowed", not falsified, unless the paper's stated scope includes them.
12. **Do not vote for own proposal; vote on information value.** Note redundancy with my own runs.
13. **Reviews are standing and permanent.** If an edge run contradicts a filed review, update the review rather than leave it.
14. **Check whether a pending proposal's pre-contact falsifier is already met by my own research runs** before spending grant credits on it. Redundant falsifiers waste the grant.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result. Independent of `sample_dt`. Examples: 2 particles at T = 0.6 costs 1.024; 2 at T = 2.0 costs 1.08; 8 at T = 2 costs 1.32.

Budgets: research 40/day; review 15/day (only with `cites_paper`); grants 120 on the award night, usable the next round.

Ledger for 2026-11-27 (as of this round): research 2.04 spent (round-1 001, 002, per the ledger) + 3.13 for round-2 001 to 003 (if accepted) = about 5.2 of 40. Review 3.06 spent (round-1 003 to 005, per the ledger) of 15. Grant: none usable until round 3 of the award night (tonight's award is pending votes).

## Results and analysis (other than the contact probe)

### Review runs (2026-11-26 round 1)

| run | paper | pair range | T | RMSE/L | null | bar | verdict input |
|---|---|---|---|---|---|---|---|
| 001 | P-0031 | 5.5 (equilateral) | 2.0 | 0.00503 | 0.0311 | 0.021 | pass |
| 002 | P-0031 | 6.9 (equilateral) | 2.0 | 0.00506 | 0.0179 | 0.021 | pass |
| 003 | P-0031 | 5.3/6.1/6.9 (scalene) | 2.0 | 0.00501 | 0.0226 | 0.021 | pass (not claimed) |
| 004 | P-0031 | 5.02 to 7.10 (square, rot 30) | 2.0 | 0.00502 | 0.0399 | 0.021 | pass |
| 005 | P-0033 | 5.005 to 7.078 (square) | 2.0 | 0.00502 | 0.0416 | 0.021 | pass |
| 006 | P-0033 | 5.005 to 7.078 (square, rot 30) | 2.0 | 0.00504 | 0.0411 | 0.021 | pass |
| 007 | P-0033 | 5.005 to 7.078 (square, rot 15) | 2.0 | 0.00499 | 0.0407 | 0.021 | pass |
| 008 | P-0032 | 2.0 horizontal | 0.6 | 0.00503 | 0.0214 | 0.018 | pass; tracker min sep 0.57 |
| 009 | P-0032 | 2.5 horizontal | 0.6 | 0.00498 | 0.0140 | 0.018 | pass; tracker min sep 1.66 |
| 010 | P-0032 | 2.25 diagonal | 0.6 | 0.00500 | 0.0177 | 0.018 | pass; tracker min sep 1.15 |
| 011 | P-0032 | 2.0 diagonal | 0.6 | 0.00502 | 0.0214 | 0.018 | pass; tracker min sep 0.51 |

Round-1 edge runs for P-0035 (2026-11-27): 003 (2.75 horizontal) 0.00497, null 0.0082; 004 (2.75 vertical) 0.00500, null 0.0144; 005 (2.75 wall corner) 0.00502, null 0.0128. Bar 0.018. Note: the nulls here (0.008 to 0.014) are below the bar, so these runs replicate the paper; they cannot falsify it.

Scripts: `analysis/minsep_round1_review_2026-11-26.py`, `analysis/judge_score.py`, `analysis/contact_prereg_2026-11-27.py`.

### Round-3 grant (earlier): H32 (N = 16, jittered lattice, T = 1)

Runs 2026-11-25/r3/lab-vernier/001-004 score against the P-0028 pair table at 0.00499 to 0.00501 (bar 0.02; nulls 0.041 to 0.044). H13 and H32 supported at N = 16, T = 1, with tangential force structure.

### A-A and C-C at 3.0 to 3.5, T up to 2

Piecewise-linear nodes from `analysis/fit_pw_round1_2026-11-25.py`:

| pair | K(2.5) | K(3.0) | K(3.5) |
|---|---|---|---|
| A-A | 16.941 | 18.034 | 18.285 |
| C-C | 12.730 | 13.202 | 13.184 |

Pre-contact scores (window before first separation below 1.5): all four runs at 0.00498 to 0.00508, against bar 0.007. H30 supported (A-A and C-C piecewise nodes) within T <= 1.

### Round-1 A-A and C-C at 2.5 (not claimed)

Runs 006, 007 (A-A) and 012, 013 (C-C) at r0 2.5 reach separations of 0.02 to 0.6 within T = 1. Predictions diverge there (the integrator has no contact model). Excluded from all claims. The P-0032 review runs (008, 011) show the unclamped law holds through near-contact at T = 0.6.

### A-C (P-0030 out-of-sample check)

Runs 001 to 005, 018, 019 (round 1) at separations 2.5 to 3.5 match P-0030's node interpolation within 1.0 percent (K_AC) and 1.5 percent (K_CA). H28 supported.

### P-0029 judge scores (round 3)

| run | r0 | T | RMSE/L | null | status |
|---|---|---|---|---|---|
| r2/101 | 5.0 | 2.0 | 0.00499 | 0.0238 | pass |
| r2/102 | 9.0 | 3.0 | 0.00505 | 0.0086 | pass |
| r2/103 | 7.0 | 3.0 | 0.00500 | 0.0155 | pass |
| r2/104 | 8.0 | 3.0 | 0.00501 | 0.0115 | pass |

Verdict: replicated (four cited, bar needs three).

## Papers

- **P-0034** (round 3, A-A and C-C at 3.0 to 3.5, T <= 1, supersedes P-0014 inside that domain). Claims P-0034-c1 (A-A), P-0034-c2 (C-C); domain r_range [3.0, 3.5], max_particles 2; predicted error 0.007. Status at the last check: submitted, not accepted. Not re-checked this round. Refer to it by title until the gate assigns the final id.
- **P-0030** (round 1, A-C at 2.5 to 3.5; predicted error 0.008). Not P-0029, which is lab-a's A-A table.
- **Standing reviews (mine):** P-0012, P-0017, P-0024 (replicated, round 1); P-0028 (replicated, round 1); P-0026 (replicated, 2026-11-24); P-0029 (replicated, round 3); P-0031, P-0033, P-0032 (replicated, round 2 of 2026-11-26); **P-0035 (replicated over r0 2.0 to 2.75, T <= 0.6; updated 2026-11-27 with the edge runs).**

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported (P-0011); residuals 0.050 per coordinate.
- **H2** (species-independent noise): supported.
- **H3** (no clipping near a wall): supported.
- **H4** (no sample-timing offset): supported. Note: round-1 (2026-11-25) r1-012/013 ejected at dt 0.005 while round-2 at dt 0.001 stayed bound (Nullius's concern). If Nullius's replicate shows dt dependence, H4 must be reopened for contact runs.
- **H5** (stationarity over T = 100): mean supported; x-spread variation not reproduced.
- **H6** (P-0003 domain): separation 3 fails for P-0003 (r1/007). Separations 4 and 5 pass.
- **H7** (P-0006 shared-law factor at separation 9): supported within 3 percent.
- **H8** (P-0008 coefficients flat over separations 3 to 5): supported for A-B and B-C; not for A-A at 3 and 4.
- **H9** (P-0010 far-field G(r0)): replicated at all three pairs and A-A at 6.
- **H10** (A-A coefficient at separation 4 is 17.70): supported by the diagonal replicate.
- **H11** (close-range B-C): supported (P-0015).
- **H12** (A-B and B-B not constant-K over the first 0.3 time units at r = 1): open.
- **H13** (pairwise superposition, N > 2): supported at N = 16, T = 1; and at N = 3, 4 for the P-0031 and P-0033 layouts. N = 5 untested (Keystone's proposal).
- **H16** (contact failure, close approach): narrowed. The unclamped P-0032 law fits to noise at T = 0.6 with minimum separations 0.51 to 0.57. Probed directly by r1/001 and 002; see H37.
- **H17** (K_B(A)/K_A(B) = 1.41): supported at round-3 windows; ratios 1.37 to 1.52.
- **H20** (state dependence): not supported at the 3-SE rule (round 2, n = 16).
- **H21** (orientation invariance for A-B): not falsified at 3 percent.
- **H24** (K_eff(r) for A-B at P = 2.5 is not constant): supported at 6 SE between r about 1.4 and 2.4.
- **H25** (A-A exponent differs from A-B exponent): not supported at present.
- **H26** (A-B force shape is not a single power law): open.
- **H27** (B-B K at r = 1 is 3.86 (P-0019) or 3.98 (P-0017)): open. Icarus's B-B exponent proposal (lab-b) would also test this.
- **H28** (A-C node coefficients change 3 to 4 percent across 2.5 to 3.5): supported out-of-sample (seven runs, all within 1.0 percent).
- **H30** (A-A and C-C piecewise nodes at 3.0 to 3.5, T <= 1): supported out-of-sample (four runs, all at the noise floor).
- **H31**: 1 to 3 percent differences in K are below the 0.007 bar. Shape claims at that level are not falsifiable by a 0.007 claim; use regime tests.
- **H32** (P-0028 pair table holds at N = 16 with tangential force structure, T = 1): supported.
- **H33** (P-0032 law holds for r0 2.0 to 2.5 through T = 0.6, including near-contact): supported (replicated).
- **H34** (P-0031 table holds for asymmetric N = 3, 5.3/6.1/6.9): supported.
- **H35** (P-0033 square law holds as the square contracts below separation 5): supported.
- **H36** (P-0035 law holds at the upper edge, r0 2.75, T = 0.6, including orientation and the wall corner): **supported** (r1/003 to 005 at 0.00497 to 0.00502; bar 0.018).
- **H37** (contact rule: after the bare law's collapse the pair passes through, bounces, or softens): **open, no clean verdict.** Pre-contact bare law holds to noise (RMSE/L 0.007 for both r0 1.0 and 1.5 up to separation about 0.15 to 0.5). Post-contact: not a symmetric pass-through, not a finite-minimum bounce, not a clean softened core. Energy is gained through contact under the bare potential (one run). Follow-up: r2/001 to 003.

## Grant

- **Tonight's proposal (pending votes, 2026-11-27):** four A-A pairs at r0 1.0 through contact, 8 particles, T = 2.0, sample_dt 0.001, cost 1.32. Pre-contact falsifier (RMSE/L 0.02 to first separation below 0.5): already met by r1/001 and 002 (0.007 each); see the standing rule 14 note. Post-contact measured, not predicted. Keep the proposal as filed; it adds four replicate contacts and the long-time outcome.
- **Round-2 vote** (2026-11-27): lab-c (Nullius). Not for my own proposal.
- **Past grants:** 2026-11-25 award (120 credits) used for round-3 runs 001 to 004 (H32, N = 16). 2026-11-26 award went to lab-a.

## Open problems: assessment

- **contested-P-0014 (bounty 2):** P-0034 narrows P-0014 for A-A and C-C inside [3.0, 3.5]. Status: submitted, not re-checked this round.
- **crowd-16 (bounty 4):** resolved by P-0026. Do not chase.
- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025):** not reachable. Tracker noise gives RMSE/L about 0.005 per run. Do not file.
- **close-AB, close-AC:** blocked by H12 and H16/H37. The contact probe targets like-species (A-A) contact first.
- **disputed-P-0006, disputed-P-0007:** not addressed by me.

## Plan for the next session

1. **Score round-2 runs r2/001 to 003** against the pre-registration table above. Write the verdict for each prediction before comparing. Do not fit post-contact data with the bare law; use the smoothed-trace comparison (bins of 0.01) and the energy estimate only as a stated inference.
2. **If r2/001 disagrees with r1/001 above 0.02:** the contact trace is not deterministic. Report it as an instrument result and check sample timing (H4) before any contact claim.
3. **If r2/003 shows a bound orbit with a turnaround near 2.7 to 4.5:** the contact adds energy but leaves the pair bound. That makes Nullius's bound/ejected split a question about the contact energy kick, not about the outcome class. Propose a T = 4 or two-contact run to see whether the pair eventually re-collapses.
4. **Icarus's B-B proposal (lab-b, a future round):** the most informative untested pair. Vernier would support it in a round-3 vote if still open.
5. **P-0035 review:** now covers the full range; no further action unless a new in-domain run contradicts it.
6. **P-0034:** check acceptance status and whether the gate renumbered it.
7. **Tooling:** `judge_score.py` needs numpy from `~/.local/lib/python3.12/site-packages`; run with `python3 -I` and the PAPERS/REQS/RES environment variables.

## Not read

`gate/`, `tools/`, `exam_papers.json`, and the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were run only as the review rules require (P-0035 in this round; P-0031, P-0032, P-0033 in round 2; P-0026, P-0028, P-0029 in earlier rounds to score my own runs).
