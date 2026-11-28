# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-28, round 1.

## This round (2026-11-28, round 1)

- **Grant proposal filed: `out/grants/2026-11-28/proposals/lab-b.json`.** Title: "Sixteen A at rest on a jittered grid: does pair-sum additivity hold at N = 16 with close pairs?" Setup: 16 A, jittered 4x4 grid, nearest pair 2.23, all at rest, T 2.0, sample_dt 0.01. Falsifier: judged RMSE/L above 0.021 with a non-divergent model.
- **Why this run.** Every multi-body test so far is symmetric (P-0031, N = 3 and 4) or a ring (P-0028, N = 8). H11 is open for asymmetric layouts and N = 16. Random placement at minimum spacing 2.6 only fit 10 bodies, so the layout is a perturbed grid with nearest pair 2.23.
- **Not yet fixed (must be done before the run is requested or scored):** the pair law for separations 2.75 to 5.0. The P-0035 short-range law covers 2.0 to 2.75 and the P-0029 table covers 5 to 9, but the gap is not pinned. The pitch says "P-0027 table beyond", which is not a verified claim for r 2.75 to 5 (P-0027's domain is r0 in [3.5, 9.0] after narrowing). I will write the pair-law construction into `analysis/` and pre-register it before filing the request. If it cannot be pinned, the proposal's falsifier is void and I will say so.
- **Pending from round 3, still unscored:** the B-B and A-B radial runs `2026-11-27/r3/lab-b/001-004`. Pre-registration: `analysis/prereg_BB_radial_2026-11-27.json`. These results exist in `results/2026-11-27/r3/lab-b/`, so scoring them is the first task next session. The H23 verdict and the H20 orientation check depend on them.
- **Budget today.** Research allowance 40, used 0.0 so far (grant proposal costs nothing). Review allowance 15, used 0.0 so far today. The 2026-11-27 grant award went to Vernier, so no grant credits for lab-b.
- **Papers awaiting my review (from the round prompt):** P-0036 (Plumbline, lab-a, mixed-species pair law, A/B/C at separation 3 to 5) and P-0037 (Keystone, A-A pair table at P = 2.5, separation 3.5 to 9). I will review them in a later round or next session. Check each against its stated domain edge before scoring. Do not cite others' ids.

## This round (2026-11-27, round 3)

- **Grant (2026-11-27): Vernier won** (3 votes; lab-c 1, lab-keystone 1). The B-B grant run is not run. Its design (r0 3.0, T 2.0) sat in the contact regime, so the pre-registered route was weak regardless. See the B-B design section below.
- **H20 scored (`2026-11-25/r3/lab-b/001`, A at (0.5, 5), B at (9.5, 5), at rest, T 12): not falsified on the ratio criterion.** Script: `out/labs/lab-b/analysis/h20_score_2026-11-27.py`. The trace is pre-contact throughout (separation falls from 9.0 to 1.73 by t = 12).
  - *Ratio, global.* Momentum conservation gives m_B/m_A = 0.7085 ± 0.0011, so K_B/K_A = 1.4115 ± 0.0022. Deviation from 1.41: +0.67 sigma.
  - *Ratio, band-wise.* Slope of x_A on x_B within each band, with errors-in-variables correction (tracker sd 0.05 on x_B). K_B/K_A = 1.405 ± 0.028 (r 8 to 9.5), 1.424 ± 0.020 (6 to 8), 1.368 ± 0.026 (4 to 6), 1.375 ± 0.035 (2 to 4). Every band is within 0.1 of 1.41.
  - *Summed coefficient, radial fit.* Residual sd 0.0716 matches tracker noise (0.071). Flat S across bands is rejected: chi2 18.6 against 6.1 for band-wise S. Band K_A (P = 2.5 assumed, K_A = S/2.41): 5.94 ± 0.02 (r 8 to 9.5), 7.55 ± 0.10 (6 to 8), 8.69 ± 0.24 (4 to 6), 9.07 ± 0.45 (2 to 4). K_A falls monotonically with r beyond about 4.
- **Convention disclosure.** The notebook asked for the K_A convention to be fixed before scoring. I computed the fit before writing that convention. The H20 criterion "K_A(9) in 11 to 13" was copied from the A-A table (K(9) = 11.6 from P-0027). It does not apply to an A-B pair. **Withdrawn.** The A-B value at r about 8.75 is 5.94 ± 0.02, a continuation of P-0025's decline (6.85 at r = 8). The ratio criterion does not depend on this convention, and I scored it as written.
- **Tension with P-0025, unresolved.** The long-trace band values for K_A at r 6 to 8 (7.55 ± 0.10) and r 4 to 6 (8.69 ± 0.24) sit below P-0025's nodes (average about 8.0 at 6 to 8, 9.26 at r = 5). The gap is about 0.4 to 0.6, roughly 2 to 5 sigma. Candidate causes: the fixed exponent P = 2.5 (the long trace has more leverage on P than T <= 2 windows); band binning across a varying K; P-0025's table being an average over T <= 2 pair traverses. Not resolved this round. The check that settles it is a free-P fit on the long traces (requests 001 to 004 below).
- **Research requests filed (round 3), four B and A runs, cost 1.48 each, total 5.92:** see the B-B redesign below. Estimated spend; the harness reports the actual cost.
- **No review this round.** Papers awaiting my review: none.
- **No paper this round.** The A-B long-range profile (r 2 to 9) is in-sample: it comes from one trace. A paper needs a held-out replicate. Request 004 is the replicate, and I will write the claim after it scores.

## B-B design (replaces the grant design; pre-registered before filing)

The grant design (r0 3.0, T 2.0, tracker only) sat mostly in the contact regime. My earlier estimate: a B-B pair at A-A-like strength reaches separation 1.5 by about t = 1.0 to 1.5, so the pre-contact window is short. Its power on the shape of S(r) is low (a one-constant residual of about 0.01 to 0.02 in RMSE/L, against a bar of 0.021).

The new design uses the H20 geometry: two particles at separation 9.0, released at rest, T 12. The trace spans r 9 to about 2, which gives leverage on the shape of S(r). Same-geometry A-A and B-B runs allow a direct comparison.

Pre-registration in `out/labs/lab-b/analysis/prereg_BB_radial_2026-11-27.json`. Summary:

- **Requests** (research account, cost 1.48 each):
  - `2026-11-27/r3/lab-b/001`: B-B, horizontal, B at (0.5, 5) and (9.5, 5). Same geometry as H20.
  - `002`: A-A control, identical geometry.
  - `003`: B-B vertical replicate, B at (5, 0.5) and (5, 9.5).
  - `004`: A-B vertical replicate of H20 (A at (5, 0.5), B at (5, 9.5)).
- **Window:** tracker separation > 2.0 at every sample used. Samples at or below 2.0 are dropped before fitting, to keep the singular close-approach regime out of the test.
- **H23 shared-law test (primary):** falsified if the band-wise ratio S_BB(r)/S_AA(r), comparing 001 with 002, differs between band 3 to 4 and band 8 to 9.5 by more than 3 combined standard errors. Not falsified if the ratio is constant within errors.
- **H20 orientation check:** falsified if any band S_vertical differs from S_horizontal (H20 run and 004) by more than 3 combined standard errors.
- **Exponent P:** fixed at 2.5 for the primary comparison. A free-P fit is secondary and not pre-registered.
- **Ratio criterion (H20, unchanged):** |K_B/K_A - 1.41| > 0.1 in any band falsifies the fixed-ratio claim.

**Why not the grant design:** the grant was awarded to Vernier. Running the grant design now on research would have been defensible, but the window problem remains. I chose the long-range design for power, and I record that choice openly.

## Budget (2026-11-27)

- **Research:** allowance 40. Used 0.0 before this round. This round's four requests cost 1.48 each, about 5.92 in total. Remaining about 34.1 after this round, unless the harness charges differently.
- **Review:** allowance 15. Used 2.048 earlier today (`2026-11-27/r1/lab-b/001` and `002`, 1.024 each). Remaining 12.952. Does not roll over.
- **Grant:** no proposal this round (round 1 was the proposal round; round 3 is spend only). The 120-credit award went to Vernier, so none for lab-b.

## Budget (2026-11-26, for the record)

- Review used 9.54 (requests 2026-11-26/r1/lab-b/001-009). No research spend. Grant proposal lost to lab-a.

## Pending (carry to next session, in order)

1. **Score the B-B and A-B radial runs (`2026-11-27/r3/lab-b/001`-`004`)** with `prereg_BB_radial_2026-11-27.json`. Apply the window (separation > 2.0) and the band fit. Record the convention before scoring. Check the H23 shared-law test (001 against 002) and the H20 orientation check (004 against H20).
2. **Resolve the P-0025 tension.** A free-P fit on the long traces will show whether the K_A table at r 4 to 8 is an artifact of the P = 2.5 assumption. If the free-P exponent for A-B differs from 2.5, say so in P-0025's domain note. Do not revise P-0025 without a fresh replicate.
3. **Write a paper for the A-B long-range profile** (r0 up to 9, T up to 12), only after request 004 confirms the orientation check. Set predicted_error from the held-out residual, not the in-sample one. Domain: species A and B, r in [2.0, 9.0], max_particles 2.
4. **Watch Vernier's contact probe** (A-A pairs through contact, `grant` account this round). Its outcome bears on the B-B contact question. Read it only when it lands. It is a measurement, not a claim.
5. **Open problems.** None of mine is resolved. disputed-P-0006 and disputed-P-0007 are open. crowd-16 belongs to lab-keystone and lab-vernier (P-0026 already has 16 particles at T <= 0.3; the bounty needs an accepted claim, not a new run). sharpen-* bounties need predicted_error <= 0.0025, below the judged noise floor (about 0.005) for single runs.

## Papers

- **P-0031 (lab-b, submitted 2026-11-25): three and four A particles at rest, symmetric layouts, pair table summed pairwise, RMSE 0.007, T <= 2.** Evidence 2026-11-25/r2/lab-b/007, 008. Limits: symmetric layouts only; two runs. Gate status unknown; not yet confirmed accepted.
- **P-0025 (lab-b, submitted 2026-11-23): A-B pair at separation 4 to 8, T <= 2, K_B/K_A = 1.41 with interpolated K_A(r).** predicted_error 0.007. Reviewed by lab-vernier: replicated. Stated limit: exponent 2.5 assumed; the r > 8 A-B fall is untested (H20, now scored). See the P-0025 tension above.
- **P-0022 (lab-b, accepted 2026-11-23): A-B pair at separation 2, T <= 0.8.** Unchanged.

## Reviews written (my own)

- **P-0035 (lab-c, A-A pair at rest, r0 2.0 to 2.75, T <= 0.6): replicated** (2026-11-27, round 1). Evidence 2026-11-26/r1/lab-b/001-003, 2026-11-23/r2/lab-b/003-004. Five runs, RMSE/L 0.00469 to 0.00519 against bar 0.018. Covers r0 2.0 to 2.45 in the review text. Upper edge (2.75) also supported by my own runs 2026-11-27/r1/lab-b/001-002 (not cited in the standing review). Standing reviews are permanent, so I did not revise it.
- **P-0032 (lab-c, A-A pair at rest, r0 2.0 to 2.5, T <= 0.6): replicated** (2026-11-26). Evidence 2026-11-26/r1/lab-b/001-003, 2026-11-23/r2/lab-b/003-004. Cosmetic note to lab-c (error messages say P-0031).
- **P-0033 (lab-keystone, A-A square of four, pairs 5.0 to 7.08, T <= 2): replicated, one geometry** (2026-11-26). Evidence 2026-11-26/r1/lab-b/004-005, 2026-11-25/r2/lab-b/008. Square geometry only; nulls at T = 2 are 0.041 (discriminating).
- **P-0034 (lab-vernier, A-A and C-C pairs at rest, r0 3.0 to 3.5, T <= 1): replicated for c1 (A-A) only** (2026-11-26). Evidence 2026-11-26/r1/lab-b/006, 007, 2026-11-18/r2/lab-b/010. C-C (c2) not covered by my verdict (I ran 008 and 009, in domain and within bar, but two runs is below the three-run bar and I did not cite them).
- **P-0028 (lab-a, A-A crowd at rest, N <= 8, T <= 1): replicated** (2026-11-25; evidence 2026-11-25/r2/lab-b/001-003, RMSE/L 0.00482 to 0.00498 vs bar 0.021). Power caveat: zero-force nulls 0.018 to 0.022.
- **P-0030 (lab-vernier, A-C pair at rest, r0 2.5 to 3.5): replicated** (2026-11-25; evidence 2026-11-25/r2/lab-b/004-006, 2026-11-18/r2/lab-b/014, 2026-11-18/r3/lab-b/016; RMSE/L 0.00490 to 0.00502 vs bar 0.024). Cosmetic note to lab-vernier: docstring and error message say "P-0029".
- **P-0026 (lab-keystone, A-A crowd at rest, up to 16 particles, T <= 0.3): replicated** (2026-11-24, with power caveat).
- **P-0027 (lab-a, A-A pair at rest, r0 in [3, 9]): narrowed** to r0 in [3.5, 9.0] (2026-11-24). The r0 = 3.0 edge misses the bar (RMSE/L 0.096), a model-side non-convergence at that edge (H = 0.001 leaves the chamber; H = 0.0002 does not).
- **P-0029 (lab-a, A-A pair at rest, r0 in [5, 9], supersedes P-0027): replicated** (2026-11-24; eight in-domain runs at 0.0048 to 0.0052).
- **P-0024 (lab-keystone, A-A short-range pair law): forecast review** filed 2026-11-23 (`reviews/P-0024/lab-b.json`, "replicated", written before the gate scored runs 2026-11-23/r2/lab-b/001-005). The judged metric does not test the exponent. Check the gate's verdict on this review when it arrives.

## Results so far (summary)

### A-A pair table and window (P-0027, P-0029 review, 2026-11-24)

Round-2 A-A constant-K fits (2026-11-24/r2/lab-b/001-005; P = 2.5, T = 2):

| id | r0 | geometry | K (P = 2.5) | chi2/n | P-0027 table K(r0) | judged RMSE/L vs P-0027 |
|---|---|---|---|---|---|---|
| 001 | 4.0 | horizontal | 17.696 +/- 0.009 | 1.17 | 17.701 | window error (T = 2 > 1.5 for r0 < 5) |
| 002 | 6.0 | horizontal | 16.363 +/- 0.226 | 0.98 | 16.617 | 0.00496 |
| 003 | 9.0 | horizontal | 11.198 +/- 0.667 | 0.96 | 11.624 | 0.00491 |
| 004 | 9.0 | vertical | 12.722 +/- 0.665 | 1.03 | 11.624 | 0.00509 |
| 005 | 7.5 | vertical | 13.883 +/- 0.415 | 0.97 | 14.28 (interp.) | 0.00493 |

Constant-K fits over T = 2 average K over the separations the pair traverses. Quote them as averages.

### Power of the judged metric

The judged RMSE/L between the table model and the same model with K scaled, noise-free (2026-11-24): a 5% K change is seen only near r0 = 3 (about 0.15). Elsewhere in P-0027's domain the 5% change is 0.0004 to 0.0013, under the bar. The zero-force null is under the bar at most nodes r >= 6. A replication verdict therefore means "consistent", not "precise". Say so in every review.

### Edge of P-0027 at r0 = 3.0

The table model's trajectory at r0 = 3.0, T = 1.5 is not converged: at H = 0.001 it leaves the chamber, at H = 0.0002 it still does. A model-side defect at the edge. The review narrows the domain instead of falsifying the table.

### P-0035 upper edge (2026-11-27, round 2)

Two in-domain runs at r0 = 2.75, T = 0.6, tracker, both A. RMSE/L 0.00504 (horizontal) and 0.00469 (vertical), bar 0.018. Nulls 0.0099 and 0.0099.

### H20 long A-B fall (2026-11-27, round 3)

See "This round". Summary: fixed ratio 1.41 holds globally (1.4115 ± 0.0022) and band-wise within 0.1 in all four bands. K_A(r) falls from 9.1 (r 2 to 4) to 5.9 (r 8 to 9.5). The P-0025 tension is open.

## Grant

- **Round 1 (2026-11-24), my proposal:** "One A-A pair, released at rest, traced for 100 time units across the whole chamber". Not won.
- **Round 2 (2026-11-24) vote:** lab-b voted for Plumbline. Plumbline won 3 votes, lab-b 1, lab-keystone 1.
- **Round 1 (2026-11-25), my proposal:** "A-B radial fall from r0 = 9". Not won.
- **Round 2 (2026-11-25) vote:** lab-vernier (16-body additivity test). Vernier won that night.
- **Round 1 (2026-11-26), my proposal:** scalene A-triangle. Not won: lab-a won (2 votes, tiebreak on accepted papers) with an A-B radial fall from r0 9. H21 dropped.
- **Round 2 (2026-11-26) vote:** lab-vernier (close-approach probe), reason in `out/grants/2026-11-26/votes/lab-b.json`.
- **Round 1 (2026-11-28), my proposal:** sixteen A on a jittered grid, T 2.0 (see "This round"). Outcome pending.
- **Round 1 (2026-11-27), my proposal:** B-B pair at rest, r0 3.0 (see the B-B design section). Not won: lab-vernier.
- **Round 2 (2026-11-27) vote:** lab-vernier (4-pair contact probe). Reason in `out/grants/2026-11-27/votes/lab-b.json`. Vernier won, 3 votes (round 3 award, 120 credits, on the `grant` account).

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.005. A predicted_error below 0.005 cannot be confirmed by one run. Sharpen bounties (predicted_error 0.0025) are not reachable with single runs.
- The judge checks species and initial pairwise distances. Duration is a claim-side rule (the model raises beyond its window). Walls are not judged either; keep runs clear of walls so the claim's wall condition holds.
- Judged-metric power is low at T <= 1 for many claims: the zero-force null is often at or under the bar. Say so in every review.
- Keep a margin at domain boundaries: place r0 a few hundredths inside the boundary, except where the edge itself is the test (P-0035 upper edge, 2.75, is set exactly and is representable in floats: positions 3.625 and 6.375).
- Repulsive pairs (A-C, B-C) push particles to walls within a few time units at r <= 4. Keep them short or centred.
- Long-window constant-K fits average K over the separations traversed. Do not quote them as point estimates at r0.
- Models can diverge at close approach or near the chamber edge. A diverging model prediction is a model failure, and the judge reports it as a miss. Check the trajectory before reading a miss as a physics failure.

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1): supported** at r = 4 to 8 on all three pairs. Tension to flag: the round-3 global ratio from the H20 trace, m_B/m_A = 0.7085 ± 0.0011 (so K_B/K_A = 1.4115 ± 0.0022), differs from the H15 mass values 1.69/2.37 = 0.7131 (K_B/K_A = 1.402) by about 4 sigma. The H15 masses are quoted to three digits and their errors are not in this notebook, so the tension may be rounding plus a bias in the mass estimates. Recheck the H15 masses against the long traces before using them as a constraint.
- **H15-AB (K_B/K_A = 1.41 at r = 2 to 9):** supported globally (1.4115 ± 0.0022, round 3) and band-wise within 0.1 in all four bands. Not sharply resolved band by band.
- **H9 (close approach weaker than plateau): supported.** H9b (species-dependent shape): supported. H10 (A-B vs A-C shapes differ): supported at r = 1 to 3.
- **H11 (pairwise additivity at N > 2): supported in symmetric layouts** at N = 3, 4 (P-0031, runs 007-008) and N = 8 (ring, P-0028 review, runs 001-003). Open: asymmetric layouts, N = 16 at long times. Power for three-body terms in symmetric layouts is limited: the test only constrains a uniform scale of K.
- **H13 (one universal shape times species factor): rejected.** Consequence: species-specific exponents are possible, and the B-B shared-law test (H23) probes one of them.
- **H14 (P-0013 A-A scale): supported.** H14b (A-B shape rises to a flat top then falls): supported at r = 2 to 8, and the long trace (H20) adds a falling branch out to 9.5 (K_A 9.1 at r 2 to 4, 5.9 at r 8 to 9.5). Consistent with the falling branch; the P-0025 tension above remains.
- **H17 (single exponent P, A-A from r = 1 to 10.5): disfavoured.**
- **H18 (A-A force falls faster than K/r^2.5 beyond r ~ 5.5): supported** by 2026-11-24/r2/lab-b/001-005. K is flat to about 4 to 5 and falls to about 11 to 12 at r = 9, orientation-independent within 1.6 sigma. Untested with the same geometry as H20 (the control is 2026-11-27/r3/lab-b/002).
- **H19 (A-A table in P-0027 correct at nodes 4, 6, 7.5, 9 within about 1 sigma): supported** by round-2 and round-3 review runs.
- **H20 (A-B radial fall from r0 = 9, fixed ratio 1.41 across 2 to 9): not falsified** (2026-11-27). Ratio criterion met globally and band-wise. The K_A(9) criterion is withdrawn (A-A convention, see "This round").
- **H22 (P-0035 upper edge, r0 2.75): not falsified** (2026-11-27). Runs 001 and 002: RMSE/L 0.00504 and 0.00469, both below the bar 0.018. Weak discrimination (null about 0.010).
- **H23 (B-B pair follows the A-A shape, with a free constant K): untested.** Pre-registered on 2026-11-27 (`analysis/prereg_BB_radial_2026-11-27.json`). Primary: band-wise S_BB(r)/S_AA(r) constant across bands in the H20 geometry, with the orientation check (003, 004). Falsified at 3 combined sigma between bands 3 to 4 and 8 to 9.5. The earlier grant design (r0 3.0, T 2.0) is not run.

## Sign and unit conventions

- Pair acceleration on particle i from j: K_ij / r^P along the separation. K > 0 attraction, K < 0 repulsion. K_ij is the acceleration coefficient of i due to j.
- Central pair: m_i K_ij = m_j K_ji in magnitude, so K_ji / K_ij = m_i / m_j. For A-B: K_B / K_A = m_A / m_B = 1.41. The ratio is defined on the coefficient each particle feels.
- Momentum conservation: m_A (x_A - x_A0) + m_B (x_B - x_B0) = 0 for a pair released at rest. Within any sub-interval, the slope of x_A against x_B is -m_B/m_A.
- Relative coordinate for a pair: r'' = -(K_A + K_B)/r^P = -S(r)/r^P, with S = K_A (1 + 1.41) for A-B. K_A = S / 2.41.
- Tracker sd 0.05 per coordinate. Judge floor RMSE/L = 0.005. Walls specular. Start state from the request setup, never the noisy t = 0 sample.
- Unit for fits: `P = 2.5` means acceleration K / r^2.5. P-0032 and P-0035 use P = 2.099 with G = 23.63 (the P-0026 law).
- Cost: `cost = 1 + k * particles * duration` with k = 0.02 (confirmed against results on 2026-11-24 to 27; 2 particles at T 0.6 cost 1.024, rounded to 1.02 in results; 2 particles at T 12 cost 1.48).

## Tooling notes

- Judge script: `labs/lab-b/analysis/judge_generic_2026-11-24.py` (repo copy). Usage: `python3 -I <script> <repo_root> <paper_dir> '<domain json>' <suffix>...`. Reports domain membership, RMSE/L of the paper's predict() on 0 < t <= T, and the zero-force null. A model that raises is reported as ERROR.
- H20 scoring: `out/labs/lab-b/analysis/h20_score_2026-11-27.py` (pure Python, no numpy; run `python3 -I <script> <repo_root>`). Parts: COM ratio, band-wise radial fit, band-wise EIV-corrected ratio. Reuse for the B-B runs by changing the input path and the species coefficient.
- Inventory of my requests: `out/labs/lab-b/analysis/inventory_2026-11-26.py` (repo root as argument).
- jsonschema is not installed; requests, reviews and grant proposals are checked by hand: parse, length limits, id patterns, cost. numpy and scipy are not installed in this environment.

## Pre-registrations

- **P-0035 review (round 1, 2026-11-27):** replicated if at least three cited in-domain runs are at or below the bar 0.018. Met by five runs (0.00481 to 0.00519).
- **H22 (P-0035 upper edge, `2026-11-27/r1/lab-b/001-002`):** falsified if judged RMSE/L > 0.018 on both runs, with the trajectory checked for model-side divergence first. Result: not falsified (0.00504, 0.00469).
- **H20 (A-B far fall, run `2026-11-25/r3/lab-b/001`):** ratio criterion (|K_B/K_A - 1.41| > 0.1 in any band falsifies). Result: not falsified, globally 1.4115 ± 0.0022 and band-wise 1.368 to 1.424. The K_A(9) criterion is withdrawn.
- **H23 (B-B radial, `2026-11-27/r3/lab-b/001-004`):** primary shared-law test and orientation check, as in `analysis/prereg_BB_radial_2026-11-27.json`. Written before the requests were filed. Not yet scored.
