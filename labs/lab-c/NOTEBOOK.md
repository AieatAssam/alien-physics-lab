# LAB-C notebook

## Session 2026-11-18, round 3 (this session)

### What happened this session
- **Reviews filed (both on `out/reviews/`, both schema-valid):**
  - **P-0003 (lab-a, A-A at rest, K/r^2.5, K=17.74, r 3–6): `narrowed`.** Evidence 2026-11-18/r2/lab-c/004 (r=6) and 005 (r=3).
    - r=3 (005): consistent. Best K at P=2.5 = 17.70, rms 0.050.
    - r=6 (004): rms at noise (0.051–0.054), but the mean residual drifts after t≈1.0 (particle 0 x: −0.024 in the last half-unit; particle 1: +0.023). Best K = 16.60 at P=2.5, about 6% below the paper. Lab-a's own r=6 per-run K values (16.3, 16.8) agree with this.
    - Proposed domain: **species A, r in [3.0, 5.0], max 2 particles.** I did not falsify the constant at r 3–5. I do not endorse K=17.74 at r=6.
  - **P-0004 (lab-a, species-dependent coupling at r=5): `replicated`.** Evidence r1/lab-a 001, 002 (A-B), 005 and the repeat r2/lab-a/005 (A-C). Both claims fit the predictor at noise level. The A-C repeat confirms the repulsion sign and magnitude, so c2 (single-run in the paper) is now replicated. Edge check at r=4 (my r1/007, 008) also fits at noise level, T=0.8. I did not count that as evidence for the claim, which is r=5 only. The B-C factorisation prediction (r2/lab-a 001–002) is outside the stated domain and I did not review it.
- **Retraction (energy paragraph, round 2).** The pre-registered test was the replicate 2026-11-18/r2/lab-c/001 (identical setup to 2026-11-17/r2/lab-c/001: A-A at rest, x = 3.5 and 6.5, y = 5, T=2, dt 0.001 against T=10, dt 0.005 for the old run). Both runs close to contact near t≈1.25. After contact the separations disagree: t=1.5 gives 3.16 (old) vs 1.40 (new), and t=2.0 gives 8.60 vs 1.45. Tracker noise is 0.05 per coordinate, so a 1.8-unit gap cannot be tracking error. The post-contact track is not reproducible from identical initial conditions. Per the rule I set in round 2, **the energy-excess paragraph is retracted.** I cannot say whether the scatter is the simulator's own randomness at contact or a sensitivity the law does not capture. Both would make post-contact dynamics untestable with fixed-step integration.
- **Velocity pair (r2/002 approach, 003 recede, A-A, speed 2 each, r≈6).** Both fit the rest law at noise level (rms 0.049–0.051, mean residuals ≤0.002). Best-fit K differs: 17.80 (approach) vs 15.30 (recede). This is **not** evidence for a velocity term. The two runs sample different separations: approach covers r 1.40–6.07, recede covers r 5.86–9.66. The K difference is therefore most likely r-dependence (H11), not velocity (H8). H8 is not decided by these runs.

### Analysis files (this session, all in `out/labs/lab-c/analysis/`)
- `review_P0003_r2.py`: P-0003 predictor vs r2/004 and r2/005, with quarter-run mean residuals and best-K scan.
- `review_P0004_r2.py`: P-0004 predictor vs lab-a in-domain runs (r1/001, 002, 005; r2/005) and my r=4 edge runs (r1/007, 008).
- `r2_001_003_check.py`: replicate separation track, and rest-law fits to the approach/recede pair.
- `energy_replicate_compare.py`: old vs new energy case (identical setups), and separation ranges covered by 002/003.
- Earlier scripts (round 1–2) are unchanged: `check_papers_r1.py`, `traj_KP_r1.py`, `traj_scale_r1.py`, `law_scan_r1.py`, `sim_bias.py`, etc. Some are only in `labs/lab-c/analysis/` in the repo, not yet copied here. `sim_bias.py` is still not copied into `out/` (noted last round).
- Environment: numpy and jsonschema were pip-installed to run the checks. All scripts run with `python3 -I`.

### Budget (2026-11-18)
- Research: allowance 40. Used 11.36 (8.20 before round 2 plus 3.16 filed in round 2: r2/001–003). Remaining ≈ 28.6 if all accepted. No new research requests this session.
- Review: allowance 15. Used 4.32 (r1/006 = 2.20, r2/004 = 1.08, r2/005 = 1.04). Remaining ≈ 10.7. Reviews filed this session cost nothing.
- Cost constant k = 0.02 (unchanged). Cost = 1 + 0.02 × particles × duration.

### Round-1 results (2026-11-18/r1/lab-c, all `ok`, unchanged from round 2)

| Run | Config | Window | Result |
|---|---|---|---|
| 001 | A-A approach, r=2, speed 1 each | 0.4 | window mean a = 1.62; trajectory rest-law residual rms 0.050, mean ≤0.003 |
| 002 | A-A recede, r=2, speed 1 each | 0.4 | window mean a = 2.65; trajectory rest-law residual rms 0.050 |
| 003 | A-A co-moving (0,+1), r=2 | 0.4 | window mean a = 2.59 (= at rest 2.59); rest-law residual rms 0.050, mean ≤0.002 |
| 009 | A-A at rest, along y, r=2 (isotropy) | 0.4 | window mean a = 2.73 (x-pair at rest 2.59); rest-law residual rms 0.051 |
| 004 | A-A approach, r=4, speed 1 each | 0.8 | window mean a = 0.48; trajectory s = 1.025 ± 0.006 (P=2.5) |
| 005 | A-A recede, r=4, speed 1 each | 0.8 | window mean a = 0.57; trajectory s = 1.028 ± 0.012 (P=2.5) |
| 006 | lone C, speed 4.95, T=60 (P-0002 edge) | | rms 0.051/0.050; no speed decay (review filed) |
| 007 | A-B at rest, r=4 | 0.8 | per-particle a = 0.27 (A), 0.38 (B); mean 0.32 ± 0.03 |
| 008 | A-C at rest, r=4 | 0.8 | per-particle a = −0.33 (A), −0.69 (C); mean −0.51 ± 0.03 |

The window fits are biased when separation changes quickly, so the velocity comparisons rest on trajectory-level fits.

### Hypotheses (status after this session)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; speeds to 4.95; durations to 100). Also supported by lab-b P-0002 review (replicated).
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r ≥ 2: falsified.
- **H5** monotone attractive A-A static force (r = 1–8): supported. Power-law exponent P ≈ 2.1 fits r = 1–4 at noise level. P = 2.5 overpredicts the attraction at r ≈ 2 relative to r ≈ 4 (strength factor 0.886 at r=2 and 1.037 at r=4).
- **H6** pair force species-independent (as accelerations): falsified. Reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F ∝ q_i q_j / r²: not tested cleanly, because accelerations are confounded with masses.
- **H8** velocity-dependent pair force: **not decided.** Round-1 runs at relative speed ≤2 (r=2, r=4) show no velocity term at noise level. The round-2 approach/recede pair at r≈6 is confounded with r-dependence (see above). A matched-r test is needed before H8 is either falsified or supported.
- **H9** isotropy at r=2: supported (x vs y difference 0.14 ± 0.19).
- **H10** species masses m_A : m_B : m_C ≈ 1 : 0.67 : 0.39, with equal and opposite pair forces. Still a hypothesis. P-0004 (lab-a) gives a K_B/K_A ratio of 1.37, and that is only a mass ratio under Newton's third law. Test: a_A/a_C should be r-independent, and a 3-body run should satisfy momentum conservation.
- **H11** A-A central law steepens at large r (screened or non-power). **Strengthened this session.** P-0003's K_eff drops from about 17.7 (r=3) to 16.6 (r=6) at fixed P=2.5. The recede run fits K=15.3 over r 5.9–9.7 against 17.8 over r 1.4–6.1. Lab-a's screened form K e^{−r/λ}/r² (λ≈8) fits the same data as the power law. The two forms differ by about 15% at r=8–9, so far-field data can separate them.
- **H12 (new)** Post-contact outcomes for two A particles at rest are not reproducible from identical initial conditions. Evidence: r2/lab-c 001 vs the 2026-11-17 run (separation gap 1.8 at t=1.5). Status: one replicate pair. Needs a third and fourth replicate before any claim.

### Retractions and corrections
- **Energy-excess paragraph (round 2): retracted** (see above). The post-contact separation is not reproducible, so the KE ≈ 30 argument cannot stand.
- **H8 "falsified" (round 2): downgraded to not decided.** The round-1 rest-law fits show no velocity term at relative speeds ≤2 for r = 2 and 4. The round-2 approach/recede comparison at r≈6 cannot separate velocity from r-dependence.
- **Round-1 "F" is an acceleration, not a force** (unchanged; for unequal-species pairs the mean is not a pair force).

### Publications and reviews
- Publications: none yet. Candidate for a small claim once replicated: "Two A particles at rest at separation 3–5 accelerate with K/r^2.5, K = 17.7 ± 0.1" (matches P-0003 narrowed). Not published by me, since lab-a's paper already covers it.
- Reviews filed: P-0001 (replicated, round 1), P-0002 (replicated, round 2), **P-0003 (narrowed, round 3), P-0004 (replicated, round 3)**.
- Reviews pending: none assigned to me.

### Plan for next round
1. **Matched-r velocity test (H8).** Use the same r window with opposite v_r. Example: a pair starting at separation 5.5 approaching at speed 1.5 each, and one starting at 4.5 receding at speed 1.5 each, with T chosen so both spend time in r in [4.5, 5.5]. Compare the force inside that window. Predict: no velocity term means both fit the rest law at the same K.
2. **Far-field shape (H11).** Run A-A at rest at r=8 and r=9 (short T=1 to avoid contact) to separate power law P≈2.1 from screened λ≈8. Compare with lab-a's queued far-field runs before filing, to avoid duplicating them.
3. **Contact scatter (H12).** Two replicates at r=2 at rest, T=1.5, same dt as r2/lab-c/001. If the post-contact separations disagree again, publish H12 as a small claim: post-contact outcomes are not reproducible at dt 0.001 for this initial condition.
4. **Mass picture (H10).** Momentum check on a 3-body run. Only after 1–3.
5. Budget: research ≈28.6 left, review ≈10.7 left. Keep review credits for the next paper review.

### Requests filed this session
- None. The round-2 requests (r2/lab-c/001–005) are all `ok`. Their outcomes are reported above.
