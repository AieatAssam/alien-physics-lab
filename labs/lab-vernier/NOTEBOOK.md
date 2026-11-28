# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then measure force-law shape precisely, and review other labs' claims at their edges with exact numbers.

Last updated: 2026-11-28, round 1 (scored round-3 contact runs of 2026-11-27; reviewed P-0036 and P-0037 against my own runs; filed review-account runs for both; filed tonight's grant proposal and four research runs).

## Round 1 summary (2026-11-28)

- **Round-3 contact runs scored (2026-11-27/r3). Two pre-registered falsifiers fired.**
  - **H_dt is falsified.** The dt = 0.001 runs (r3/007 to 010, exact r2/003 setup, T 2) all exceed separation 1.0 in [0.5, 2.0]: max 1.164, 1.329, 1.405, 1.037. Their minimum separations are 0.004 to 0.012 and each run has 40 to 70 entries below 0.3. The oscillation is real and near-contact, but it is not confined below 1.0.
  - **The three-class story for H37 is not supported.** Of the five dt = 0.0003 replicates at t = 0.60 (r3/002 to 006), two fall in the plateau band (003 at 1.165, 005 at 1.166), and three fall between the plateau and rise bands (002 at 1.451, 004 at 1.299, 006 at 1.715). The pre-registered falsifier "a class in between" fired. Post-contact separation at t = 0.60 looks like a continuum over about 1.15 to 1.75 (plus the r1/001 value of 2.0 and r2/002 at 1.2), not three discrete classes.
- **Grant run r3/001 (four A-A pairs, T 2, dt 0.001) shows within-run variation.** Pair separations at t = 2.0 are 0.56 (pair 0-1), 1.18 (pair 2-3), 1.64 (pair 4-5) and 0.68 (pair 6-7). Pairs in the same run do not share one post-contact outcome. So the outcome varies between encounters within one run. This is evidence for per-encounter variation. It does not rule out per-run variation as well.
- **Consequence for H37.** No post-contact point prediction is supportable. The claim type must be a distribution (see Standing rule 15). A dt-dependence test is still open and is set up below in a matched form.
- **Reviews.** P-0036 (lab-a, mixed pairs) and P-0037 (lab-keystone, A-A 3.5 to 9) were checked against my own in-domain runs with `judge_score.py` (numpy installed to the user site; see Tooling). Both look replicated. Written review files are **not yet filed**: the review verdicts will be written when the review-account runs filed this round return, so the cited ids are the new ones (Standing rule 13 and the review account rule). Details in "Reviews" below.
- **Budget.** Research: 4.10 planned of 40 (r1/001 to 004). Review: 5.38 planned of 15 (r1/005 to 012, cites P-0036 and P-0037). Grant: proposal filed, no spend yet.
- **No paper filed this round.** The contact result is now a distribution-level finding, and the one model that could be published (pre-contact law) is already covered by P-0026. A paper waits for the round-1 dt test.

## Round-3 results, scored (2026-11-27/r3)

Script: `out/labs/lab-vernier/analysis/score_r3_contact_2026-11-28.py` (stdlib, run with `python3 -I`, repo root as argument).

### r3/002 to 006 (exact r1/001 setup, A-A at rest, r0 1.0 horizontal, T 0.6, dt 0.0003)

| run | separation at t = 0.60 (0.02-bin mean) | class (pre-registered bands) |
|---|---|---|
| 002 | 1.451 | in between (falsifier) |
| 003 | 1.165 | plateau |
| 004 | 1.299 | in between (falsifier) |
| 005 | 1.166 | plateau |
| 006 | 1.715 | in between (falsifier) |

Pre-contact (t up to about 0.24) is the bare law to tracker noise in every run, as before. The spread at t = 0.60 is wide (1.17 to 1.72), and the r1/001 run (1.996) sits at the top of it.

### r3/007 to 010 (exact r2/003 setup, A-A at rest, r0 1.0 horizontal, T 2.0, dt 0.001)

| run | max separation in [0.5, 2.0] | min separation | dips below 0.3 (entries) | H_dt (pre-registered: max < 1.0 and at least two dips) |
|---|---|---|---|---|
| 007 | 1.164 | 0.0080 | 48 | fails (max above 1.0) |
| 008 | 1.329 | 0.0119 | 44 | fails |
| 009 | 1.405 | 0.0082 | 42 | fails |
| 010 | 1.037 | 0.0035 | 73 | fails (max just above 1.0) |

All four dt = 0.001 runs oscillate through near-contact, as r2/003 did, so the qualitative class recurs. The quantitative prediction (confined below 1.0) fails in all four.

### r3/001 grant (four A-A pairs, r0 1.0, T 2, dt 0.001, eight particles)

| pair (initial positions) | sep at 0.60 | sep at 1.0 | sep at 2.0 | min (t > 0.3) | max (t > 0.3) |
|---|---|---|---|---|---|
| 0-1 (x 2, 3; y 2.5) | 0.393 | 0.782 | 0.562 | 0.005 | 1.334 |
| 2-3 (x 7, 8; y 2.5) | 0.531 | 0.484 | 1.178 | 0.025 | 1.966 |
| 4-5 (x 2, 3; y 7.5) | 0.539 | 0.526 | 1.641 | 0.009 | 1.759 |
| 6-7 (x 7, 8; y 7.5) | 0.515 | 0.128 | 0.675 | 0.015 | 0.979 |

Pairs in one run diverge from each other after contact. Pre-contact fits to the unclamped P-0026 law are the same as in the other runs (not re-scored separately this round; the pre-contact prediction stands).

## Reviews (status and evidence)

### P-0036 (lab-a): mixed-species pairs at rest, r0 3 to 5, T ≤ 2

From my own filed runs (judge rule: species, N ≤ 2, every pair distance in [3, 5]; `judge_score.py`, bar 3 × 0.007 = 0.021):

- In-domain, predict() does not refuse, judged error ≤ 0.0054 (noise floor): 2026-11-19/r1/008 (0.00497), 009 (0.00510); 2026-11-20/r1/005 (0.00521), 006 (0.00510); 2026-11-22/r1/008 (0.00531), 2026-11-22/r2/003 (0.00496); 2026-11-24/r2/011 (0.00511), 013 (0.00503); 2026-11-24/r3/005 (0.00498), 009 (0.00509), 010 (0.00506); 2026-11-25/r1/003 (0.00507), 005 (0.00502), 019 (0.00509). Thirteen runs; all pass the bar.
- **Contact failure (not a bar failure of the claim as written).** 2026-11-23/r3/015 and 016 (A-B, r0 3.0, T 2, horizontal and vertical). Pre-contact fit is good (error ≤ 0.009 to t ≈ 1.4). The pair reaches separation 0.2 to 0.3 at t ≈ 1.5 to 1.6 and crosses. The paper's model (no contact handling) diverges: judged error 3.88 over the run. P-0036 says "Not claimed: contact", but its domain fields do not exclude it, and `predict()` does not refuse it. These two runs are in-domain by the judge's rule. I am not citing them as support.
- A-C and B-C are repulsive, so they do not reach contact in T 2. The contact issue is specific to A-B (attractive).
- Planned verdict: **replicated** for the pre-contact scope, with the contact failure stated in the comment and a suggestion that `predict()` refuse when any pair separation falls below ~1.0 (as P-0037 does at 2.5). Final verdict after the review-account runs r1/005, 006, 007, 008, 009 return (predicted in the table below).

### P-0037 (lab-keystone): A-A at rest, r0 3.5 to 9, separation ≥ 2.5 throughout

Own in-domain runs with predict() not refusing, judged error ≤ 0.0052 (bar 0.021): 2026-11-20/r1/003 (r0 6, 0.00518); 2026-11-20/r2/007 (r0 5, 0.00492); 2026-11-20/r2/001 (r0 9, T 6, 0.00496); 2026-11-25/r1/010 (r0 3.5, T 1, 0.00509); 011 (r0 3.5, T 1, 0.00503); 2026-11-25/r2/101 (r0 5, 0.00499); 102 (r0 9, T 3, 0.00505); 103 (r0 7, T 3, 0.00500); 104 (r0 8, T 3, 0.00501). Nine runs, all replicate.

Predict refuses (pair comes within 2.5, so no prediction, as the paper says): 2026-11-20/r1/002 (r0 4, T 2), 2026-11-20/r3/004 (r0 4, T 2), 2026-11-25/r2/001 (r0 3.5, T 2). Not cited.

Planned verdict: **replicated**, with the 3.5 edge covered at T 1 only (no T 2 run at 3.5 that stays ≥ 2.5 apart). Final verdict after review-account runs r1/010, 011, 012 return.

### Review-account runs filed this round (cite the paper they test)

| request | paper | setup | cost | pre-registered prediction |
|---|---|---|---|---|
| r1/005 | P-0036 | A-C, r0 3.0 horizontal (A at x 2.0, C at x 5.0), T 2 | 1.08 | repulsive, no contact; judged error ≤ 0.0075 |
| r1/006 | P-0036 | B-C, r0 5.0 horizontal, T 2 | 1.08 | judged error ≤ 0.0075 |
| r1/007 | P-0036 | A-B, r0 4.0 vertical, T 1.5 | 1.06 | pre-contact; judged error ≤ 0.0075; predict must not refuse |
| r1/008 | P-0036 | A-C, r0 4.5 diagonal, T 2 | 1.08 | judged error ≤ 0.0075 |
| r1/009 | P-0036 | B-C, r0 3.5 vertical, T 2 | 1.08 | judged error ≤ 0.0075 |
| r1/010 | P-0037 | A-A, r0 4.5 horizontal, T 1.5 | 1.06 | judged error ≤ 0.0075; predict must not refuse |
| r1/011 | P-0037 | A-A, r0 6.5 diagonal, T 3 | 1.12 | judged error ≤ 0.0075; predict must not refuse |
| r1/012 | P-0037 | A-A, r0 3.5 vertical, centre (5, 5), T 1 | 1.04 | judged error ≤ 0.0075 |

Falsifier for each: any run with judged error > 0.021 that predict() does not refuse. A refused run is not evidence. Any run that reaches contact (separation < 1) is reported as contact, not counted as a bar failure for the claim.

## Round-1 requests (2026-11-28/r1)

- **001 to 004 (research, cost 1.02 each):** A-A at rest, r0 1.0 horizontal (x 4.5 and 5.5, y 5.0), T 0.6, **sample_dt 0.001** (not duration/2000; a deliberate matched dt test against r3/002 to 006 at 0.0003).
  - **Pre-registered prediction (dt does not set the class):** at t = 0.60 the four dt = 0.001 runs are spread over at least 0.2 (range 1.15 to 1.75, like r3/002 to 006), with at least one run in each of the two bands and no run below 1.0 separation.
  - **Falsifier (dt sets the class):** all four dt = 0.001 runs sit in one tight cluster (sd < 0.05 at t = 0.60) that differs from the dt = 0.0003 distribution. If that happens, H4 is reopened and sample_dt becomes a controlled variable.
- **005 to 012 (review account):** see the table above.

## Grant

- **Tonight's grant (2026-11-28), proposed.** `out/grants/2026-11-28/proposals/lab-vernier.json`. Title: "Four A-A pairs at r0 1.0: post-contact sample-timing test at sample_dt 0.0003 (T 0.6)". Setup: the r3/001 geometry (eight particles, pairs at x 2,3 and 7,8 and y 2.5 and 7.5), duration 0.6, sample_dt 0.0003 (2000 samples).
  - **Why this design.** It tests the same four pairs at dt 0.0003 against r3/001 at dt 0.001, pair by pair over t ≤ 0.6. The T = 2 version at dt 0.0003 is not allowed (2000-sample cap: 2/0.0003 > 2000).
  - **Pre-registration.** If sample timing does not matter, each pair's smoothed separation (0.02 bins) at t ≤ 0.6 matches r3/001 to 0.05 or better. Falsifier: a pair-level difference larger than 0.05 at any t ≤ 0.6 that persists over more than 0.05 time units.
  - **Cost.** 1 + 0.02 × 8 × 0.6 = 1.096. The rest of the grant (118.9) is unused by this design; it was not proposed. Flag to the user if that is a problem.
- **Round-3 request (to be filed if the grant is awarded and wins its vote).** 2026-11-28/r3/lab-vernier/001, account `grant`.
- **Past grants.** 2026-11-27 (round-2 vote: lab-c; round-1 proposal: four A-A pairs at r0 1.0 through contact, won with 3 votes, filed as r3/001 of 2026-11-27).

## Hypotheses: status

- **H1** (white Gaussian tracker noise, sd about 0.05): supported (P-0011); residuals 0.050 per coordinate. Consequence: the judged-RMSE noise floor is about 0.005 of L, so a prediction_error below about 0.005 is not checkable by the judge's RMSE (a perfect model scores about 0.005). Sharpen bounties (predicted_error ≤ 0.0025) are therefore not claimed here.
- **H2** (species-independent noise): supported.
- **H3** (no clipping near a wall): supported.
- **H4** (no sample-timing offset): **open, reopened for contact runs.** The matched dt test (r1/001 to 004 at dt 0.001 vs r3/002 to 006 at 0.0003) and the grant (r1 proposal at 0.0003 vs r3/001 at 0.001) test it.
- **H5** (stationarity over T = 100): mean supported; x-spread variation not reproduced.
- **H6** (P-0003 domain): separation 3 fails for P-0003 (r1/007 of 2026-11-27). Separations 4 and 5 pass.
- **H7** (P-0006 shared-law factor at separation 9): supported within 3 percent.
- **H8** (P-0008 coefficients flat over separations 3 to 5): supported for A-B and B-C; not for A-A at 3 and 4.
- **H9** (P-0010 far-field G(r0)): replicated at all three pairs and A-A at 6.
- **H10** (A-A coefficient at separation 4 is 17.70): supported by the diagonal replicate.
- **H11** (close-range B-C): supported (P-0015).
- **H12** (A-B and B-B not constant-K over the first 0.3 time units at r = 1): open.
- **H13** (pairwise superposition, N > 2): supported at N = 16, T = 1; and at N = 3, 4. N = 5 untested.
- **H16** (contact failure, close approach): narrowed. Pre-contact is fine; post-contact is H37.
- **H17** (K_B(A)/K_A(B) = 1.41): supported at round-3 windows; ratios 1.37 to 1.52.
- **H20** (state dependence): not supported at the 3-SE rule (round 2, n = 16).
- **H21** (orientation invariance for A-B): not falsified at 3 percent.
- **H24** (K_eff(r) for A-B at P = 2.5 is not constant): supported at 6 SE between r about 1.4 and 2.4.
- **H25** (A-A exponent differs from A-B exponent): not supported at present.
- **H26** (A-B force shape is not a single power law): open.
- **H27** (B-B K at r = 1 is 3.86 (P-0019) or 3.98 (P-0017)): open.
- **H28** (A-C node coefficients change 3 to 4 percent across 2.5 to 3.5): supported out-of-sample.
- **H30** (A-A and C-C piecewise nodes at 3.0 to 3.5, T ≤ 1): supported out-of-sample.
- **H31**: 1 to 3 percent differences in K are below the 0.007 bar. Use regime tests.
- **H32** (P-0028 pair table holds at N = 16, T = 1): supported.
- **H33** (P-0032 law holds for r0 2.0 to 2.5 through T = 0.6, including near-contact): supported (replicated).
- **H34** (P-0031 table holds for asymmetric N = 3): supported.
- **H35** (P-0033 square law holds as the square contracts below separation 5): supported.
- **H36** (P-0035 law holds at the upper edge, r0 2.75, T = 0.6): supported (0.00497 to 0.00502 against bar 0.018).
- **H37** (post-contact outcome of A-A at rest, r0 1.0): **open, reframed again.** Pre-contact is the bare law to noise. Post-contact separation at t = 0.60 is a spread (1.15 to 1.75 in the dt 0.0003 replicates; 2.0 in r1/001) with no discrete classes; pairs within one run differ at t = 2 (r3/001). Near-contact oscillation at dt 0.001 is real, with max separation 1.04 to 1.4 over [0.5, 2] (H_dt falsified as pre-registered).
- **H_dt** (dt = 0.001 runs confined below separation 1.0 for t in [0.5, 2]): **falsified** on 2026-11-27/r3/007 to 010 (max 1.04 to 1.40).
- **P-0036 scope (new).** Pre-contact law fits my own mixed-pair runs to noise. A-B at r0 3.0, T 2 reaches contact at t ≈ 1.5 and then diverges (2026-11-23/r3/015, 016). Pending: review-account runs r1/005 to 009.
- **P-0037 scope (new).** A-A 3.5 to 9 fits my own runs at noise (nine runs). Predict refuses the three runs that come within 2.5. Pending: review-account runs r1/010 to 012.

## Standing rules

1. **Falsification needs a null above the bar.** A review can falsify only if the zero-force null on the cited runs sits above 3 x predicted_error. Check the null before filing.
2. **Replication is a different test.** "replicated" stands when the paper's own model is within the bar on at least 3 cited in-domain runs. State which verdict is being made and check the bar for that verdict. State any unreached part of the domain in the comment, and disclose in-domain runs that fail even when they are not cited.
3. **Domain on the request positions.** Start separations at an r_range edge are risky (strict float guards). Use exact binary fractions for exact-edge domains, or sit a small margin inside the edge. Run each setup through the paper's own `predict()` before filing.
4. **Dense sampling.** The cost is `1 + k * particles * duration`, independent of sample count. Use `sample_dt = duration / 2000` unless a matched dt test needs otherwise, and then stay within the 2000-sample cap (so at T = 2, sample_dt must be at least 0.001).
5. **Pre-contact windows for attractive pairs.** A full-window fit or prediction through a close pass is invalid when the integrator diverges. Scores for my own fits use the window before the first measured separation below 1.5 (or below 0.5 for contact runs). The judge scores the full run, so check the pre-contact prediction separately.
6. **Bars are loose at T ≤ 0.3 and in general at the 0.007 level.** Falsification needs a regime change: close approach, long time, N, or a new pair.
7. **Label K by the window's mean separation**, not by the start separation.
8. **Judge domain excludes duration, but predictors do.** Several predictors refuse durations outside their window. A refused run cannot be cited as evidence.
9. **Write only under `out/`.** Analysis code and fits go in `out/labs/lab-vernier/analysis/`. The older source folder `labs/lab-vernier/analysis/` is read-only reference.
10. **Pre-register before results.** Predictions for each new run are written in this notebook before its results are read.
11. **Asymmetric layouts are in the judge domain but not in a paper's claim** when the claim says so. A miss there is "narrowed", not falsified, unless the paper's stated scope includes them.
12. **Do not vote for own proposal; vote on information value.** Note redundancy with my own runs.
13. **Reviews are standing and permanent.** If an edge run contradicts a filed review, update the review rather than leave it.
14. **Check whether a pending proposal's falsifier is already met by my own research runs** before spending grant credits on it.
15. **Identical requests are not guaranteed identical outcomes.** After a singular contact, two runs with the same request can differ by up to 0.85 in separation, and pairs in one run differ too. A post-contact claim must be a distribution (class or quantile frequencies with n), not a point prediction. Pre-contact claims are unaffected.
16. **Score a replicate against the replicate, not only against a reference run.** Round 3 showed a reference run can itself be the outlier (r1/001). Report both comparisons.
17. **Predict refusal is part of the claim.** For a paper whose text says "not claimed: contact" (P-0036), a run that reaches contact is a scope failure. Say so in the review comment, and do not count it as support.

## Cost and budget model

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season). Confirmed by every result. Independent of `sample_dt`. Examples: 2 particles at T = 0.6 costs 1.024; 2 at T = 2.0 costs 1.08; 8 at T = 0.6 costs 1.096; 8 at T = 2 costs 1.32; 16 at T = 0.6 costs 1.19.

Budgets: research 40/day; review 15/day (only with `cites_paper`); grants 120 on the award night, usable in round 3 of that date.

Ledger for 2026-11-28 (as of round 1): research 4.10 planned of 40; review 5.38 planned of 15; grant proposal filed (no spend).

## Tooling

- `out/labs/lab-vernier/analysis/scan_inscope_2026-11-28.py`: lists own two-particle at-rest requests with species, separation, duration and result status. Use it to find own in-domain evidence.
- `out/labs/lab-vernier/analysis/score_r3_contact_2026-11-28.py`: scores round-3 contact runs against the pre-registered bands.
- `out/labs/lab-vernier/analysis/p0036_ab_fall_2026-11-28.py`: per-time error and contact diagnosis for the P-0036 A-B fall runs.
- `out/labs/lab-vernier/analysis/file_round1_2026-11-28.py`: writes this round's request JSONs and the grant proposal.
- The judge-rule scorer `labs/lab-vernier/analysis/judge_score.py` (read-only reference) runs paper models. Run with `python3 -I`. Paper models import numpy: it was missing from this environment and was installed with `pip install --user numpy` (2.5.5). With `-I`, `judge_score.py` appends `~/.local/lib/python3.12/site-packages` itself.

## Not read

`gate/`, `tools/`, `exam_papers.json`, and the predictor and score files of the gate. I did not read them and will not. Other labs' `papers/*/model.py` were run only as the review rules require (P-0036 and P-0037 this round, on my own runs).

## Plan for the next session

1. **Score the round-1 review-account runs (r1/005 to 012)** against the table above. Then file the review JSONs for P-0036 (lab-vernier) and P-0037 (lab-vernier) with the new ids (plus the existing in-domain ids in the comment if useful). Verdicts: P-0036 replicated pre-contact (with the contact failure and a `predict()` suggestion in the comment); P-0037 replicated.
2. **Score the dt matched test (r1/001 to 004)** against the pre-registered prediction and falsifier above. Then decide whether H4 is closed (dt does not matter) or reopened.
3. **Score the grant (if awarded and it wins its vote) in round 3:** r3/001 geometry at dt 0.0003, pair by pair against 2026-11-27/r3/001 over t ≤ 0.6.
4. **Decide the H37 claim type.** A distribution claim (post-contact separation at t = 0.60 with n and quantiles, plus the repeatability caution for all labs running contacts) is the candidate. Publish only after the dt test lands, so the claim states whether dt matters.
5. **Icarus's B-B proposal (lab-b):** still the most informative untested pair. Vernier would support it in a round vote if it is still open.
