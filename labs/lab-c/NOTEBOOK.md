# LAB-C notebook

## Session 2026-11-18, round 2

### Corrections to earlier notes (read first)
- **H8 (velocity-dependent pair force) is falsified.** The round-1 approach/recede asymmetry (001 approach F=1.62 vs 002 recede F=2.65, Δ≈1.0) is a finite-window artifact of the cubic fit. A pure K/r^2 law with no velocity term reproduces it in simulation: approach 1.57, recede 2.50 (window 0.4, same geometry; `out/labs/lab-c/analysis/sim_bias.py` run at K=10.4). Trajectory-level fits (no window) also show no approach/recede difference at r=4, and the rest-fitted law predicts approach and recede at noise level at r=2 and r=4. My round-1 prediction (|F_app − F_rec| ≥ 1.0 with the sign reversed) was wrong in sign and the magnitude was an artifact.
- **The round-2 energy argument was built on the wrong law.** It used K/r² with K=9.5. The approach-phase KE in the round-2 001 table is closer to a shallower law. Its "impossibility" statement (KE ≈ 30 at r = 3–10 for any attractive conservative pair) still stands arithmetically, but I have not resolved whether the post-crossing excess is real. My own trajectory integrator blows up through the close approach (singular force at r ≈ 0.6, fixed step), so the comparison is inconclusive. See request 001 below.
- **The `F` in the round-1 and round-3 tables is an acceleration, not a force.** For unequal-species pairs, F_on0 and F_on1 differ, and the mean is not a pair force. The per-particle accelerations are consistent with equal-and-opposite forces plus species masses (m_A : m_B : m_C ≈ 1 : 0.67 : 0.39). That mass picture is a hypothesis, not established (see H10).
- **Shape of the A-A law is not a single power law.** Rest runs at r = 1, 2, 4 fit a power law with P ≈ 2.1 (K ≈ 11.4) at noise level. P = 2.5 (P-0003, K = 17.74) is too steep between r = 2 and 4 by about 12% (trajectory-level strength factor s = 0.886 at r=2 and 1.037 at r=4). At r=8 (2026-11-17/r3/lab-c/004) the P = 2.1 law overpredicts (mean residual −0.025, rms 0.068), so the falloff steepens at large r. Consistent with screening (lab-a's K e^{−r/λ}/r² is an alternative). Scan in progress, see below.

### Budget
- Research 2026-11-18: allowance 40. Used before this session 8.20. Filed this session: r2/001 (1.08), r2/002 (1.04), r2/003 (1.04) = 3.16 → total 11.36, remaining ≈ 28.6 if all accepted.
- Review 2026-11-18: allowance 15. Used before 2.20 (r1/006). Filed this session: r2/004 (1.08), r2/005 (1.04) = 2.12 → total 4.32, remaining ≈ 10.7 if accepted.
- Cost constant k = 0.02 (unchanged). Cost = 1 + 0.02 × particles × duration.

### Round-1 results (2026-11-18/r1/lab-c, all `ok`)

Method: trajectory-level and cubic-window fits. The cubic window (x0 + v0 t + a t²/2 + j t³/6, known x0, v0) is biased when the separation changes quickly, so the approach/recede comparison uses trajectory-level fits (`traj_scale_r1.py`, `traj_KP_r1.py`, `velocity_term_and_r2_001.py`).

| Run | Config | Window | Result |
|---|---|---|---|
| 001 | A-A approach, r=2, speed 1 each | 0.4 | window fit mean a = 1.62; trajectory rest-law residual rms 0.050, mean ≤0.003 |
| 002 | A-A recede, r=2, speed 1 each | 0.4 | window fit mean a = 2.65; trajectory rest-law residual rms 0.050 |
| 003 | A-A co-moving (0,+1), r=2 | 0.4 | window fit mean a = 2.59 (= at rest 2.59); rest-law residual rms 0.050, mean ≤0.002 |
| 009 | A-A at rest, along y, r=2 (isotropy) | 0.4 | window fit mean a = 2.73 (x-pair at rest 2.59); rest-law residual rms 0.051 |
| 004 | A-A approach, r=4, speed 1 each | 0.8 | window mean a = 0.48; trajectory s = 1.025 ± 0.006 (P=2.5) |
| 005 | A-A recede, r=4, speed 1 each | 0.8 | window mean a = 0.57; trajectory s = 1.028 ± 0.012 (P=2.5) |
| 006 | P-0002 review edge (see below) | | |
| 007 | A-B at rest, r=4 | 0.8 | per-particle a = 0.27 (A), 0.38 (B); mean 0.32 ± 0.03 |
| 008 | A-C at rest, r=4 | 0.8 | per-particle a = −0.33 (A), −0.69 (C); mean −0.51 ± 0.03 |

What this says:
- **H8 (velocity-dependent pair force) falsified.** Approach, recede and co-moving are all predicted at noise level by the rest-fitted law with no velocity term. A fitted velocity coefficient g in a = F(r)(1 + g v_r) is ≈ −0.01 on the grid edge and needs a finer scan (see below). The co-moving run (003) shows absolute velocity does not matter at this sensitivity.
- **H9 (isotropy)** survives at r=2: x-pair 2.59 vs y-pair 2.73, difference 0.14 (~1σ at per-particle se 0.19).
- **H6/H7 (species table) needs reinterpreting.** The per-particle accelerations satisfy a_A/a_C = 0.39 (r=2) and 0.48 (r=4), a_A/a_B = 0.67 (r=2) and 0.70 (r=4), and a_B/a_C = 0.58 (r=2). These obey transitivity (0.67 × 0.58 = 0.39). The data fit equal and opposite pair forces with species masses m_A : m_B : m_C ≈ 1 : 0.67 : 0.39. Under that reading the "species-dependent force" in the round-3 table is a mass effect on acceleration. Not yet separated from a species-dependent coupling. Prediction 007/008 at r=4 is in the stated ranges, but I now think the H7 product-form test was confounded by masses.
- **P-0003 agreement.** The P-0003 law (K=17.74, P=2.5) is consistent at r=4 with strength factor s = 1.037 ± 0.009 (trajectory level). That is about 4σ from s = 1 on my noise model, so the constant is 4% low in my data. At r=2 P-0003 gives s = 0.886, so the shape P = 2.5 is too steep between r=2 and r=4.

### Round-2 energy case (2026-11-17/r2/lab-c/001)
- Status: **open.** The round-2 notes said a conservative pair cannot produce KE ~30 at r = 3–10 after the close approach. That statement depends on the post-crossing velocities, which come from noisy differences through a crossing where tracker ids swap. Separation is id-free and is the robust observable. Observed separation: 2.67 (t=0.5), 0.58 (t=1.2), 3.16 (t=1.5), 8.60 (t=2.0), 0.26 (t=3.0), 6.62 (t=4.0).
- My integrator cannot follow the close approach (singular force, fixed step): predicted separation diverges to >10³. So I cannot test the energy claim with the existing tools. Before the close approach the separation track agrees with both laws to ~0.05.
- Request 2026-11-18/r2/lab-c/001 (replicate, dt 0.001, T=2.0) tests whether the post-crossing excess reproduces. If it does, the anomaly is real and a close-approach resolved model (adaptive step or softening) is required before any claim. If not, it was a tracking artifact and I retract the energy paragraph.

### Shape scan (in progress)
- Rest-only trajectory fits on r = 1, 2, 2, 4, 8 runs (2026-11-17/r3/lab-c/001–004 and 2026-11-18/r1/lab-c/009).
- Power law: best P ≈ 2.1 (K ≈ 11.4) at noise (rms 0.0503). P ≥ 2.3 gives large SSE, the golden search on K is unreliable there (no result yet from the refined scan).
- Per-run at P=2.1: r=2 rms 0.050, r=1 rms 0.050, r=4 rms 0.050, r=8 rms 0.068 (overpredicts).
- Screened form K e^{−r/λ}/r²: scan running (`analysis/law_scan_r1.py`, output in `/tmp/labc/scan.txt`). Result to be entered here.

### Review verdicts
- **P-0001 (lab-b): replicated** (filed in round 1).
- **P-0002 (lab-b, lone species-C free flight): replicated**, filed this session to `out/reviews/P-0002/lab-c.json`.
  - Evidence: 2026-11-18/r1/lab-c/006 (speed 4.95, duration 60, corner hits at t=2.57 and return to origin at t=5.43): residual rms 0.0510 (x), 0.0496 (y); segment means ≤0.005, no speed decay. Last segment is a single sample (−0.098 in y, 2σ, no weight). 0 census events.
  - Sanity: 2026-11-17/r2/lab-c/007 (lone C, speed 1.0, duration 100): rms 0.0514/0.0493, segment means ≤0.006.
  - Not tested: other species in the same chamber, speeds above 5, noise Gaussianity.
- **P-0003 (lab-a, A-A at rest, K/r^2.5, separation 3–6): pending.**
  - Pre-review evidence (not used as the review evidence; my own data on lab-a's claim):
    - 2026-11-17/r3/lab-c/003 (A-A at rest, r=4, T=0.8): P-0003 predictor rms 0.0499 / 0.0495, mean residual ≤0.003. **Consistent** at r=4, in domain.
    - 2026-11-17/r3/lab-c/001 (r=2, out of domain): rms 0.053/0.051, mean ±0.012. Trajectory-level residual is weak at T=0.4.
    - 2026-11-17/r3/lab-c/004 (r=8, out of domain, T=2): rms 0.055, mean ±0.017 (overpredicts, see shape).
  - Domain-edge requests filed this session: 2026-11-18/r2/lab-c/004 (r=6, at rest, T=2.0; P-0003 predicts 0.201 per particle) and 005 (r=3, at rest, T=1.0; predicts 1.138). Verdict to be filed when they return. Expected: replicated if rms ≈0.05 at both edges and mean residual ≤0.01 over the run; narrowed if the r=6 residual drifts.

### Hypotheses (status after this session)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; speeds to 4.95; durations to 100).
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r ≥ 2: falsified.
- **H5** monotone attractive A-A static force (r = 1–8): supported. Power-law P ≈ 2.1 at r = 1–4, steeper at r = 8.
- **H6** pair force species-independent (as accelerations): falsified. Reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F ∝ q_i q_j / r²: not tested cleanly, because accelerations are confounded with masses.
- **H8** velocity-dependent pair force: **falsified** (approach/recede/co-moving at noise level under the rest law; bound on g to be sharpened).
- **H9** isotropy at r=2: supported (x vs y difference 0.14 ± 0.19).
- **H10 (new)** species masses m_A : m_B : m_C ≈ 1 : 0.67 : 0.39, with equal and opposite pair forces. Supported by transitivity at r=2 (0.67 × 0.58 = 0.39 vs 0.39 measured) and by the r=4 ratios (0.70 and 0.48, within ~1.5σ of 0.67 and 0.39). Test: a_A/a_C should be r-independent, and a 3-body run should satisfy momentum conservation.
- **H11 (new)** A-A central law steepens at large r (screened or non-power). Test: scan result and the r=6 review edge.

### Requests filed this session (out/requests/2026-11-18/r2/lab-c/)
- 001 (research): replicate of the round-2 energy case, A-A at rest r=3, T=2.0, dt 0.001. Tests post-crossing separation.
- 002 (research): A-A approach r=6, speed 2 each, T=1.0, dt 0.0005. Velocity-term test at relative radial speed −4.
- 003 (research): A-A recede r=6, speed 2 each, T=0.9, dt 0.00045. Pair with 002.
- 004 (review, cites P-0003): A-A at rest r=6, T=2.0, dt 0.001. Far domain edge.
- 005 (review, cites P-0003): A-A at rest r=3, T=1.0, dt 0.0005. Near domain edge.
All validated against `protocol/request.schema.json`.

### Plan for next session
1. When 2026-11-18/r2 results return:
   - 001: compare the separation after the crossing to 2026-11-17/r2/lab-c/001. If both show the excess, it is real. Then build a close-approach-resolved integrator (adaptive step) before any energy claim.
   - 002/003: refit g with the finer scan; the bound on g must include r=6 (relative speed 4).
   - 004/005: run P-0003 predictor (`papers/P-0003/model.py`) on both; file the P-0003 review. Use the rest-fit law as a competitor on the same data.
2. Decide the shape question (power P≈2.1 vs screened) from the scan. Only publish a shape claim once the r=6 edge data are in.
3. Publish candidate P-0004 only once a domain is stated with a model.py and out-of-sample residuals. Current best candidate: "A-A pair acceleration has no velocity term for relative speed ≤2 at r = 1–4" (domain species A, two particles, r 1–4, speed ≤1 each). Model: rest-fitted central law (K≈11.4, P≈2.1, pending the scan), with out-of-sample predicted_error from 002/003 once they return. Not filed yet.
4. Mass picture (H10): design a 3-body or a C-C vs A-C comparison to test momentum conservation before claiming masses.

### Analysis files (out/labs/lab-c/analysis/)
- `moving_pair_fit.py`, `r3_force_known_ic.py`, `check_P0001_r3.py`: copied from the repo (round-1 and round-3 fits). Window fits; biased for fast-changing separation.
- `sim_bias.py`: synthetic check that the window fit gives approach 1.57, recede 2.50 for a velocity-independent K/r² law. Run with `/tmp/labc/sim_bias.py`; copy in `out/labs/lab-c/analysis/` is not yet present.
- `traj_scale_r1.py`: trajectory-level strength factor s for P=2.5 (K=17.74).
- `traj_KP_r1.py`: rest-fitted power law scan (P 2.0–2.6) and moving-run prediction.
- `check_papers_r1.py`: P-0002 and P-0003 predictors against lab-c data.
- `velocity_term_and_r2_001.py`: velocity term fit (grid too coarse) and the energy-case comparison (integrator fails past the close approach; inconclusive).
- `law_scan_r1.py`: screened vs power scan on rest runs (running).
- Caveat: the fitted velocity-term value (g ≈ −0.01) is at the edge of its grid and must not be cited until `law_scan_r1.py` has finished.

### Publications and reviews
- Publications: none yet.
- Reviews filed: P-0001 (replicated, round 1), P-0002 (replicated, round 2).
- Reviews pending: P-0003 (waiting on 2026-11-18/r2/lab-c/004–005).
