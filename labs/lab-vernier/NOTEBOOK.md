# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then replicate and review other labs' claims at their edges with precise numbers.

## Cost model (confirmed)

`cost = 1 + 0.02 * particles * duration` (k = 0.02 this season; matches every result so far, e.g. 2 particles, T = 10 gives 1.40). Two-body runs are cheap. A T = 10 pair run costs 1.4, so budget is rarely the binding limit. Design is.

## Corrections to my own earlier work (read first)

1. **The round-1 far-field table was mislabelled. H14 (steepening) is withdrawn.** Each round-1 K was a fit over the whole trajectory, but I labelled it by the *starting* separation. Runs with T = 6 at start 8 or 9 move to about 6 to 7.8 during the window, so "K(8) = 6.78" is an average over roughly r = 6.2 to 8, not a value at r = 8. The steepening (local exponent 2.6 to 3.5) was derived from those labels and is not supported. The pre-registered round-2 predictions were built on the same table, so their "falsification" tests a mislabelled table, not the physics.
2. **Window fits replace trajectory averages.** Free K at fixed P = 2.5 in time windows, labelled by the mean observed separation inside each window (`analysis/windows_all_P2.5.jsonl`, `analysis/windows_all_2026-11-22.py`). This is the correct way to read K(r) from these runs.
3. **Short windows are unidentified.** A window of 2 time units starting at r = 9 gives K anywhere from 4.7 to 7.1 (2026-11-22 r1 006/007, first window: R = 1.17 and 1.77). Only use windows where the pair moves enough for the fit to bite (fit null RMSE/L > 2 times fit RMSE/L), and treat R from short windows as noise.
4. **Standing: lone-particle runs pass the domain test vacuously**, as before. 2026-11-19 r1 001, 002, 005, 006; r2 002, 004; r3 003 are not pair evidence.
5. **Null errors must exceed the bar.** Filed claims with null errors below 3 times predicted_error are not discriminating (see Reviews below).
6. **Fit exponent and coupling are not separately identified over a short window.** Read exponents only from the separation dependence over a wide range, never from one run.
7. **Close-pass breaks runs.** 2026-11-21 r3 001 (A-B, separation 6, T = 6) passes through contact (r 1.46). Excluded. Use T <= 4 for separation 6.
8. **Model-blow-up check.** Singular r^-2.5 models can blow up near contact (P-0014). Check minimum separation first.

## Reusable tools (`out/labs/lab-vernier/analysis/`)

- `fit_tools.py`: pair-law simulator (RK4, specular walls), tracker SSE, golden-section coupling fits at fixed P. Copied from `labs/lab-vernier/analysis/` so the folder is self-contained.
- `fit_r1_2026-11-22.py`, `fit_r2_2026-11-22.py`: free K_A(B), K_B(A) at fixed P, full window (r1 001-008, r2 001-004), and r2 001/002 time windows. `python3 -I <script> [P]` from repo root.
- `windows_all_2026-11-22.py` (+ `windows_all_P2.5.jsonl`): time-window fits for all A-B runs of 2026-11-22. Labels by observed separation.
- `xpred_infall_2026-11-22.py`: cross-orientation out-of-sample check for the separation-9 infall (r2 001/002).
- `file_round3_2026-11-22.py`: writes the round-3 requests and checks their fields by hand (jsonschema is not installed here).
- Older scripts remain in `labs/lab-vernier/analysis/`.

## Papers

- **P-0011** tracker noise for a lone particle (published).
- **P-0015** close-range B-C at separation 1.0.
- **P-0016** close-range A-C at separation 1.0.
- **P-0021** A-B pair at separation 7, at rest: constant K_A(B) = 7.75, K_B(A) = 10.97 at P = 2.5, T <= 6. Named "P-0021" in the repo. Its model docstring still says "P-0019" (stale label, `papers/P-0021/model.py`, in the repo; I only write under `out/`).
  - **At risk.** Its constant K is a whole-trajectory value from start 7 and T <= 6. Window fits show K differs along that kind of trajectory (about 8.4 near r 5, about 6.3 near r 6.5 to 7.6). Its own two runs fit at the noise floor, so it stands as written. Round-3 request 005 (start 7.0, T = 2, at rest) tests its early-time value directly.
- **P-0022 (filed this round, by title: "A-B pair at separation 9, at rest: constant K_A(B) = 6.16 and K_B(A) = 8.70 at P = 2.5 (T <= 10)")**. Domain: A-B, initial separation 8.9 to 9.1, T <= 10, max_particles 2, predicted_error 0.006. Evidence: round-2 r2/001 (horizontal) and r2/002 (vertical). Out-of-sample across orientations: 0.0051 and 0.0052 RMSE/L (noise floor 0.005). Model residuals with averaged K: 0.00517 and 0.00506. Limits stated in the paper: K drifts about 5% along the run; the claim is trajectory-level, with no functional form. The gate may renumber it.

## Round 2 results (2026-11-22 r2 001-004), analysed this round

Full-window free fits at P = 2.5 (all in domain; no contact):

| run | start sep | T | K_A(B) | K_B(A) | R | fit RMSE/L | null RMSE/L | min. sep observed |
|---|---|---|---|---|---|---|---|---|
| 001 | 9 horizontal infall | 10 | 6.18 | 8.68 | 1.404 | 0.0052 | 0.056 | 5.11 |
| 002 | 9 vertical infall | 10 | 6.14 | 8.71 | 1.419 | 0.0051 | 0.056 | 5.08 |
| 003 | 3 centred | 1 | 9.42 | 12.73 | 1.35 | 0.0049 | 0.013 | 2.09 |
| 004 | 2 centred | 0.5 | 7.73 | 11.65 | 1.51 | 0.0050 | 0.009 | 1.49 |

- **Infall windows (001, 002):** K_A(B) = 5.87, 5.97, 6.09, 6.22 (001) and 5.86, 5.96, 5.92, 6.22 (002) for windows centred at r = 8.8, 8.2, 7.4, 6.1. This is flat to about 6%. My pre-registered comparison to the old table (K(8) = 6.8, K(7) = 7.75) fails, but per correction 1 that comparison was invalid.
- **Short runs (003, 004):** not informative about the local exponent. Window K in 004 goes 10.0 then 7.7 within 0.5 time units, and 003 goes 10.4 then 9.4. Null RMSE is only 1.5 to 3 times the fit RMSE. The pre-registered K(3)/K(4) ratio is not meaningful with these windows.

## Window collapse across all A-B runs (2026-11-22, P = 2.5, `windows_all_P2.5.jsonl`)

Windows labelled by mean observed separation. Only windows with good sensitivity are listed:

| r (mean in window) | K_A(B) values | runs |
|---|---|---|
| 4.80 to 4.90 | 8.38, 8.77, 8.37, 8.41 | r1 001, 002, 003, 004 |
| 5.85 | 8.15, 8.53 | r1 003, 004 (window 0 to 2) |
| 6.55 to 6.77 | 6.20, 6.16, 6.70 | r2 001, 002 (6.7 to 10); r1 005 (4 to 6) |
| 7.4 to 7.6 | 6.41, 6.09, 5.92 | r1 005 (2 to 4); r2 001, 002 (6 to 8) |
| 8.20 to 8.23 | 6.02, 5.99, 6.00, 5.91 | r1 006, 007 (4 to 6); r2 001, 002 (3.3 to 6.7) |
| 8.7 to 8.9 | 6.06, 5.85, 5.82, 6.12 | r1 006, 007 (2 to 4); r2 001, 002 (0 to 3.3) |

Reading:
- **Same r, same K, across runs** at r = 4.8 to 4.9 (about 8.4), at r = 8.2 (about 6.0), and at r = 6.2 to 6.8 (about 6.2 to 6.7). Those are reproducible to about 2%, except the r1 002 window at 4.86 (8.77, R = 1.28), which I treat as an outlier.
- **There is a step-like drop between r = 5.9 and r = 6.5**: K goes from about 8.3 (r 5.85, two runs, both at rest at t = 0) to about 6.2 (r 6.55, two runs at t = 6.7 to 10). A smooth power law cannot make a 25 percent drop over a 10 percent change in r. The step location is not yet known to better than 5.9 to 6.5.
- **Two explanations for the step:**
  - (a) K depends on r only, with a sharp change near r about 6.
  - (b) K depends on the state of the run (time since start, speed, or history). The 5.85 windows come from runs at rest at t = 0. The 6.55 windows come from later times at higher speed.
  - Round-3 requests 001 to 005 and 008 separate these: all start at rest at t = 0, so start-state is controlled, while r0 varies.
- Early windows at r 8.7 to 9 are unidentified (see correction 3). Use the long windows.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported. Published as P-0011.
- **H2 (species-independent noise at N = 1).** Supported at 2.4% spread.
- **H3 (no clipping near a wall).** Supported at x = 0.05 and in the corner.
- **H4 (no sample-timing offset).** Supported at about 0.005 time units.
- **H5 (stationarity over T = 100).** Mean supported; x-spread variation not reproduced.
- **H6 (P-0003 domain).** Separation 3 fails for P-0003 (r1/007, error 0.181). Separations 4 and 5 pass.
- **H7 (P-0006 shared-law factor at separation 9 for A-C).** Supported within 3% in one fit; one run only.
- **H8 (P-0008 coefficients flat over separations 3 to 5).** Supported for A-B at 4 and B-C at 3, 5. Not for A-A at 3 and 4.
- **H9 (P-0010 far-field G(r0) with C-factor 0.9475).** Replicated at all three pairs and at A-A at 6. The C-C run at 7 is 5.6% above the paper's K. The A-B far field has a step-like feature (see above), so P-0010's separation range should be checked before any far-field claim relies on it.
- **H10 (A-A coefficient at separation 4 is 17.70, not 18.0).** Supported by the diagonal replicate. Integrator caveat open.
- **H11 (close range B-C).** Supported: K_BC -4.32, K_CB -7.31 at r = 1.0 for T <= 0.6. Published as P-0015.
- **H12 (A-B and B-B are not constant-K over the first 0.3 time units at r = 1).** Open.
- **H13 (pairwise superposition).** Untested for more than two bodies.
- **H14 (A-B far-field power law at P = 2.5, steepening over r = 4 to 9).** **Withdrawn** (correction 1). It rested on trajectory averages labelled by starting separation.
- **H17 (K_B(A)/K_A(B) = 1.41 at all separations).** Supported. Long-window R values: 1.38 to 1.44 (r 4.8 to 8.9); infall full-window 1.404 and 1.419; separation-9 cross-orientation ratio 1.411. Short-window R is noise (correction 3).
- **H18 (masses m_A/m_B = 1.41 with momentum conservation).** Inference from H17. Not tested directly.
- **H15 (P-0004-c2 magnitude).** K_C(A) about -20.7 from three repeats, against published -21.38. Published error passes the bar; magnitude flagged.
- **H16 (P-0014 A-A contact failure).** Integrator blows up after close approach at t about 1.2 for A-A at r0 = 3. Filed as the P-0014 falsification.
- **H19 (new, to test this round).** K_A(B) at P = 2.5, measured at t in [0, 2] from rest, has a step near r = 6: about 8.3 for r <= 5.9 and about 6.3 for r >= 6.5, with no change within each side.
- **H20 (new, to test this round).** The window K depends only on the current separation, not on start state, time or speed. Falsified if early at-rest windows at r0 = 6.5 and 7.0 give about 8.3 (the value at r0 = 5.5 to 6.0 from rest).
- **H21 (new).** The A-B law is independent of position in the chamber and of orientation (horizontal vs vertical, centre vs y = 2).

## Round-3 requests (filed this round, research account, tracker only, 8 runs, est. 8.64 credits)

All A-B, both at rest, horizontal unless noted, centred on (5, 5) unless noted, duration 2.0, sample_dt 0.005, fit at P = 2.5 over t in [0, 2]. Files under `out/requests/2026-11-22/r3/lab-vernier/`.

| request | start separation | placement | purpose |
|---|---|---|---|
| 001 | 5.5 | centred | step control (predict K about 8.3 under H19/H20) |
| 002 | 5.8 | centred | approach to step |
| 003 | 6.0 | centred | replicate of r1 003 window 0 to 2 (predict K = 8.15 +/- 3%) |
| 004 | 6.5 | centred | far side of step (predict K about 6.3 under H19; about 8.3 under H20 falsified) |
| 005 | 7.0 | centred | P-0021 band start (predict 6.3 under H19; about 7.75 would mean P-0021 holds early) |
| 006 | 6.0 | y = 2 | position control vs 003 (H21: within 3%) |
| 007 | 6.0 | vertical | orientation control vs 003 (H21: within 3%) |
| 008 | 4.5 | centred | plateau check inside r < 6 (predict about 8.3; falsified below 8.0) |

Falsification rules, written before the results:
- **H19 falsified** if K(004) or K(005) is within 3% of 8.3, or K(001) is within 3% of 6.3.
- **H20 falsified** if K(004) or K(005) is within 3% of 8.3 (the at-rest early K would then be a start-state effect, not an r effect).
- **H21 falsified** if K(006) or K(007) differ from K(003) by more than 3%.
- **Reproducibility:** K(003) must be within 3% of 8.15. If not, the window fit is less precise than I think, and H19 is not testable at 3% resolution.

Expected precision: about 2 to 3% on K per run (estimated from noise 0.05 and 400 samples; the round-1 full-window fits gave about 1%).

## Reviews this round: none filed

- **P-0012, P-0013, P-0017, P-0018, P-0019, P-0020**: every zero-force null sits below 3 times predicted_error (the bar). A no-force model would pass, so a "replicated" verdict would not test the claim. Filing it would be an unsupported review. Not filed. Estimates from earlier in this session: P-0017 and P-0018 null about 0.0014 against a bar of 0.024; P-0019 null about 0.017 against 0.024; P-0020 null about 0.007 against 0.024; P-0012 null about 0.004 against 0.024; P-0013 null 0.011 to 0.017 against 0.03.
- Review credits (15) lapse unused. I would rather spend them on a claim whose null exceeds its bar.

## Grant

- Round 2 vote: **lab-keystone** (the local A-A exponent test at r = 0.5 to 2.25). Keystone won tonight's grant (120 credits, usable in round 3). **That grant is for Keystone, not for this lab.** I have no grant credits.
- The vote file (`out/grants/2026-11-22/votes/lab-vernier.json`) is not in this checkout's `out/` at the start of this session. The vote was cast in round 2; I cannot re-verify its file here.

## Open problems: assessment

- **sharpen-A-2, sharpen-B-3, sharpen-C-2 (predicted_error <= 0.0025).** Not reachable with this tracker. A correct model's measured RMSE/L is at the noise floor, 0.005 (noise 0.05 per coordinate). No honest claim can meet 0.0025. Do not file.
- **close-AB (bounty 2), close-AC (bounty 2).** Need r_range starting at 1 or less, max_particles >= 2. Blocked by H12 (A-B at r = 1 not constant-K over 0.3 time units). Do not file until H12 is settled.
- **crowd-8 (bounty 3).** Multi-body designs collapse in the 10-unit chamber with these couplings (H13). Not attempted.
- **contested-P-0014, disputed-P-0003, -P-0006, -P-0007.** Not addressed this round.

## Plan for next round

1. Read `results/2026-11-22/r3/lab-vernier/001-008`. Use `windows_all_2026-11-22.py` (or a new round-3 version) to fit K in [0, 2] per run.
2. Apply the falsification rules above, in order: reproducibility (003), then H19/H20 (004, 005, 001), then H21 (006, 007), then the plateau (008).
3. Decision tree:
   - **If H19 holds (step in r, start-state independent):** publish a narrow claim for the A-B plateau on each side of the step, with the step bracket (5.9 to 6.5) stated as the unresolved part. Domain: A-B, at rest, r0 between 4.5 and 5.9 (or 6.5 and 7.0), T <= 2. Do not claim the step's form.
   - **If H20 holds (start-state or time dependence, no step in r):** the window K is not an r-function. Then P-0021 (T <= 6 constant K) and P-0022 (T <= 10 constant K) are both start-state claims, not r-claims. Say so in the notebook, and test a moving-start run (non-zero initial velocity) at r = 6.5.
   - **If K(004) is near 8.3 but K(005) is near 6.3:** the step sits between 6.5 and 7.0 at the start, which would be a different claim. Re-check at r0 = 6.25 and 6.75 before filing.
4. Check P-0021 against request 005. If K(005) is far from 7.75, note that P-0021 is valid as a trajectory-level claim from start 7 (its own runs fit at the noise floor) but not as an early-time K.
5. Do not file a far-field exponent claim. The local exponent is not identified from these runs.
6. Reviews: none pending that discriminate. File only when the null exceeds 3 times predicted_error.
7. Rerun `aa_integrator_scan.py` before any further A-A claim.
8. If lab-b's 16-body runs (2.0 and 3.0 mixed-pair runs) arrive, check whether the step at about r = 6 explains any pair-law mismatch at 2.2 to 4.4 (the step is not in that range, so this would be a test of H20 for other pairs).

## Budgets, 2026-11-22

- **Research:** 40 allowed. Used 9.36 (round 1), 4.86 (round 2, 001-004), 8.64 (round 3, 001-008, estimated). Total 22.86 of 40 after this round, about 17.1 remaining.
- **Review:** 15 allowed. 0 used. None filed (see above).
- **Grant:** none for this lab. Vote for Keystone in round 2.

## Not read

`gate/`, `tools/`, `exam_papers.json`, predictor or score files. I did not read them and will not.
