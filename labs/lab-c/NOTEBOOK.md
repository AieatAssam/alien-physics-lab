# LAB-C notebook (Nullius)

## Session 2026-11-19, round 1 (this session)

### What happened this session
- **Reviews (verdicts revised, both `inconclusive`).** I have no independent in-domain runs of lab-a's pair claims yet.
  - **P-0005 (lab-a, supersedes P-0004): `inconclusive`.** Evidence: my edge runs 2026-11-18/r1/lab-c/007, 008 (A-B and A-C at r=4).
    - A-B at r=4 matches the r=5 values scaled by r^-2.5 (4% on A, 1.5% on B).
    - A-C at r=4: the A-side coefficient is about 20% larger in magnitude than the scaled r=5 value; the C-side agrees within 4%. Possible window-fit bias (8% separation change in 0.8 time units). Not resolved.
    - Claims c1 (A-B) and c2 (A-C sign) are not in dispute. c3 (B-B) and c4 (C-C) need independent runs. c5 (B-C prediction) needs an independent test.
  - **P-0004 (lab-a): `inconclusive`.** Correction: my round-3 'replicated' verdict (2026-11-18) rested on lab-a's own repeats. A repeat by the same lab is not an independent replication. I withdraw it.
  - The out/reviews files from round 3 are not present in this checkout's `out/`. The P-0004 file above is written fresh.
- **Analysis of P-0005 structure (no new data, from the paper's K table).**
  - Rank-1 (coupling-product) test: a 2x2 minor check on K_X(Y) = u_X v_Y. Minors that involve only A and B, or A and C off-diagonal, pass to about 2%. Minors that involve C-C fail by 15-19%: (A,C)x(A,C) and (B,C)x(B,C). So the product form holds only for pairs with A, and C-C breaks it. This is the same warning P-0005 gives.
  - Newton-third-law mass cycle: K_A(B)/K_B(A) * K_B(C)/K_C(B) * K_C(A)/K_A(C) = 0.7285 * 0.576 * 2.423 = 1.017. The cycle identity holds at 1.7%, which is inside the run-to-run spread (about 4%). No test is possible from one separation.
- **Pre-registered prediction (triangle, not yet run).** Equilateral A-B-C, side 5, at rest, with pairwise additivity and the P-0005 run means (r=5 only). Predicted initial accelerations (`analysis/triangle_prediction.py`): A (-0.159, -0.003); B (+0.001, +0.191); C (+0.380, -0.329). Over T=2 these give displacements of order 0.3-0.4, well above the 0.05 noise. A miss beyond about 0.1 in acceleration falsifies pairwise additivity at r=5.

### Requests filed this session (all `ok` as of filing; results due round 2)
Round 1, `out/requests/2026-11-19/r1/lab-c/`:
- **001-006, species matrix at r=3.0** (x = 3.5, 6.5; y=5; at rest; T=1.0, sample_dt 0.01). Pairs AA, AB, AC, BB, BC, CC.
- **007-012, species matrix at r=6.0** (x = 2, 8; T=3.0, sample_dt 0.02). Same pair order.
- **013-018, species matrix at r=8.0** (x = 1, 9; T=3.0, sample_dt 0.02). Same pair order. Repulsive pairs are short enough (T=3) that particles do not reach the walls.
- **019, A-A at r=9.0** (x = 0.5, 9.5; T=3.0). Far-field check (H11).
- **020, equilateral A-B-C triangle, side 5** (T=2.0, sample_dt 0.01). Pairwise additivity test.
- **021, 022, identical replicates of 2026-11-18/r2/lab-c/001** (A-A at rest, T=2, sample_dt 0.001). H12 test.
- **023-025 (review account, cites P-0005):** B-C at r=5 along the diagonal (c5 orientation); C-C at r=5 along y (c4); B-B at r=5 along the anti-diagonal (c3). All at rest, T=2.

Cost: research 24.08 of 40 (k=0.02, cost = 1 + 0.02 N T). Review 3.24 of 15.

Grant proposal filed: `out/grants/2026-11-19/proposals/lab-c.json`, the equilateral triangle test with T=4, sample_dt 0.01. Pitch (546 characters) says the test is cheap and the grant allowance is not needed for it.

### Analysis files (this session, in `out/labs/lab-c/analysis/`)
- `make_2026-11-19_requests.py`: generates all round-1 requests and the proposal. Checks cost and sample limits by hand (jsonschema is not installed here).
- `triangle_prediction.py`: the pre-registered additive prediction above.
- Earlier scripts from rounds 1-3 are in `out/labs/lab-c/analysis/` only where copied. Others remain in `labs/lab-c/analysis/` in the repo.

### Budget (2026-11-19)
- Research: allowance 40. Used 24.08 this round. About 15.9 unspent (does not roll over).
- Review: allowance 15. Used 3.24 this round (023-025). About 11.8 unspent.
- Cost constant k = 0.02, confirmed again by the research cost of 2-particle and 3-particle requests.

### Hypotheses (status after this session)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; speeds to 4.95; durations to 100). Also supported by lab-b P-0002 review.
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r >= 2: falsified.
- **H5** monotone attractive A-A static force (r = 1-8): supported. Exponent P ~ 2.1 at r = 1-4; P = 2.5 overpredicts at r ~ 2 vs r ~ 4 (factor 0.886 at r=2, 1.037 at r=4). Far field at r=8-9 is open. (This round: requests 013 and 019.)
- **H6** pair force species-independent (as accelerations): falsified. Reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F proportional to q_i q_j / r^2: not tested cleanly. Partly tested this round: the rank-1 structure holds for A-pairs at r=5, fails for C-C at r=5 (see analysis above).
- **H8** velocity-dependent pair force: **not decided.** Round-1 runs at relative speed <= 2 show no velocity term at noise level. The matched-r velocity test is still open; the cost of a clean design is high because windows are short and small speeds make the effect small. Deferred.
- **H9** isotropy at r=2: supported (x vs y difference 0.14 +/- 0.19).
- **H10** species masses m_A : m_B : m_C = 1 : 0.73 : 0.40 with equal-and-opposite pair forces. Consistent with the cycle identity at r=5 (1.7%). Not a measurement. The r=3, 6, 8 species matrix (001-018) tests whether the cycle identity holds at other separations.
- **H11** A-A central law steepens or screens at large r. Open. The species matrix at r=6 and r=8 (007-018) and A-A at r=9 (019) add the points. P-0003 found K about 15.5 at r=7 and K about 16.6 at r=6; the power law is not confirmed beyond r=5.
- **H12** post-contact outcomes for two A at rest are not reproducible. Evidence: one replicate pair (2026-11-17 vs 2026-11-18/r2/lab-c/001), separation gap 1.8 at t=1.5. Replicates 021, 022 are identical requests. If 021 and 022 agree with each other but not with 2026-11-18/r2/lab-c/001, the scatter is tied to setup (T or sample_dt). If 021 and 022 disagree with each other, it is simulator randomness.
- **H13 (new)** pairwise additivity at r=5 (three bodies). Tested by 020 against the P-0005 values. Pre-registered prediction above.
- **H14 (new)** coupling-product law K_X(Y) = u_X v_Y. Holds for A-pairs at r=5 to about 2%. Fails for C-C by 15-19%. Test at other r via 001-018.

### Retractions and corrections
- **Energy-excess paragraph (round 2): retracted** (2026-11-18). Post-contact separation is not reproducible, so the KE ~ 30 argument cannot stand.
- **H8 "falsified" (round 2): downgraded to not decided.**
- **P-0004 'replicated' (round 3): withdrawn to inconclusive** (this session). It rested on lab-a's repeats, not on an independent run.
- **Round-1 "F" is an acceleration, not a force** (unchanged; for unequal-species pairs the mean is not a pair force).

### Reputation note
- My scoreboard shows 2 unsupported reviews. The fix is to file verdicts only where I have independent runs, or to file 'inconclusive' with honest evidence. The round-1 reviews above follow that rule.

### Publications
- None yet. Candidate small claims once round-2 results arrive:
  1. "Two A at rest at r=3.0, 6.0, 8.0 accelerate with K(r) = (values from 001-018 A-A), power exponent P(r) ..." Only if the data show clean power or screened form.
  2. "Pairwise additivity holds to noise for the r=5 triangle (if 020 fits)." If it fails, that is the claim.
  3. H12, if 021 and 022 disagree with each other or with 2026-11-18/r2/lab-c/001.

### Plan for next round
1. Read round-2 results (001-025). Fit each request with the P-0005 model and the rest law, per-particle K and P, and compare with the r=5 values.
2. Publish the first claim that the data support. Do not publish until the fit is at noise level.
3. Triangle 020: compare with the pre-registered prediction above.
4. Review 023-025: decide c3, c4, c5. Update out/reviews/P-0005/lab-c.json with the verdict and the request ids.
5. H12: decide from 021 vs 022 first, then from 021/022 vs 2026-11-18/r2/lab-c/001.
6. Grant vote (round 2): vote for the proposal with the clearest falsifiable pitch. Do not vote for my own.
