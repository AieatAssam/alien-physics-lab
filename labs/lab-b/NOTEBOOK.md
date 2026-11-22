# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-22, round 2.
Analysis: `out/labs/lab-b/analysis/round2_2026-11-22.txt` (judge errors and fits this round). Tools: `labs/lab-b/analysis/judge_check_2026-11-22.py` (judge-style RMSE/L), `labs/lab-b/analysis/pairfit_2026-11-21.py` (constant-K chi2 fit, P = 2.5).

## Round 2 (2026-11-22) filed

- **Review of P-0019 (lab-a, Plumbline; close-range B-B at 1.0, T <= 0.3): replicated.** `out/reviews/P-0019/lab-b.json`. Evidence: 2026-11-21/r1/lab-b/007, r2/009, r2/010 (all B-B at exactly 1.0, T 0.15, in domain). Judge errors 0.00707, 0.00715, 0.00706 against bar 0.024. Coefficient caveat: my K_BB = 3.98 +/- 0.12 vs their 3.86 (about 1 sigma apart). Their stated run spread (0.03) is smaller than my scatter. T in (0.15, 0.3] not tested by me.
- **Review of P-0021 (lab-vernier, A-B at 7, T <= 6): DEFERRED.** I have no in-domain A-B run at separation 7. Round-2 review-account runs 001-004 (cites P-0021, 1.24 credits each, 4.96 of 15) are filed. Verdict to be written when their results arrive (next session). Evidence must be my own ids from these runs.
- **Research requests (5 of about 36.8 remaining; 5.28 credits):** 005 A-B at 2.0 vertical (replicate of r1/001); 006 A-B at 4.0 horizontal T 2; 007 A-B at 5.0 horizontal T 2; 008 A-C at 2.0 horizontal T 0.8; 009 B-C at 3.0 horizontal T 1.5.
- **Grant vote:** lab-vernier (P-0021's author). Reason: one far-field infall run samples the pair law from r = 9 to ~4 cheaply, with a falsifiable shape prediction. Disclosed that I review P-0021. Not voted for Keystone: its acceleration estimates at T = 0.1 are dominated by tracker noise (sd 0.05); the displacement 0.5 a T^2 ~ 0.055 for a(1.0) ~ 11, comparable to the noise. Not voted for Nullius: attractive octagon at 2.68 separation collapses inside T = 5, so the error would track close-encounter sensitivity, not additivity.

## Round 1 results (2026-11-22/r1), now fitted

Constant-K fits, P = 2.5 fixed, chi2/n with tracker sd 0.05:

| run | pair | sep | T | K_i | K_j | chi2/n |
|---|---|---|---|---|---|---|
| r1/001 | A-B (A,B) | 2.0 | 0.8 | K_AB 7.62 | K_BA 10.57 | 1.00 |
| r1/002 | A-B | 3.0 | 1.5 | K_AB 8.65 | K_BA 12.29 | 1.05 |
| r1/003 | A-C | 3.0 | 1.5 | K_AC -9.01 | K_CA -21.31 | 0.96 |

Mixed-pair shape: K_AB(2)/K_AB(1) = 1.41, K_AB(3)/K_AB(1) = 1.60, K_BA(3)/K_BA(1) = 1.68. A-C: K_AC(3)/K_AC(1) = 1.45, K_CA(3)/K_CA(1) = 1.45. So the A-B and A-C shapes differ by about 10 percent (A-B grows faster). The A-B shape drifts toward the A-A pattern (0.62 at r = 1 relative to plateau).

Note: the constant-K fit at chi2/n 1.00 over T = 0.8 from r = 2 to ~1 (r1/001) fits at noise level, but the same K would not hold at r = 1 (5.39 from T = 0.15). The short-window K values are not one shape. Use the free shape fit, not one constant.

## Filed earlier (from round 1, prior session, numbering may have changed at the gate)

- Papers filed by lab-b: B-B at 1.0 (K 3.98), C-C at 1.0 (K 9.31), A-B at 1.0 (K_AB 5.39, K_BA 7.33, T <= 0.15). Check the gate for final ids before citing.
- Reviews filed: P-0016 (lab-vernier, A-C at 1.0, T <= 0.6): replicated. P-0015 (lab-vernier): replicated for T <= 0.6 (filed). P-0013 (lab-c): narrowed (A-A at 1.5 is 13.18 +/- 0.04, not 13.55). P-0012 (lab-a): replicated, coefficient caveat.
- Round-1 grant proposal: 16 bodies on a 4 x 4 lattice, spacing 2.2, species A B C cycling, T = 1.0. Predictions to be filed after the mixed-pair shape is known.

## Coupling table (constant K, a = K / r^2.5, positive = attraction)

| pair | r | T | runs | K (pooled) | status |
|---|---|---|---|---|---|
| A-A | 1.0 | 0.15 | r1/005, 008, r2/001, 002 | 11.11 +/- 0.09 | P-0012 (lab-a) claims 11.3, about 2 sigma high |
| C-C | 1.0 | 0.15 | r1/006, r2/011, 012 | 9.31 +/- 0.13 | filed |
| B-B | 1.0 | 0.15 | r1/007, r2/009, 010 | 3.98 +/- 0.12 | filed; P-0019 (lab-a) 3.86 |
| A-B | 1.0 | 0.15 | r2/013, 014, r3/010, 011 | K_AB 5.39 +/- 0.09, K_BA 7.33 +/- 0.16 | filed |
| A-B | 2.0 | 0.8 | r1/001 (r2/005 pending) | K_AB 7.62, K_BA 10.57 | one run, chi2 1.00 |
| A-B | 3.0 | 1.5 | r1/002 | K_AB 8.65, K_BA 12.29 | one run, chi2 1.05 |
| A-C | 1.0 | 0.6 | r3/001-003 | K_AC -6.19, K_CA -14.67 | P-0016 replicated by me |
| A-C | 3.0 | 1.5 | r1/003 | K_AC -9.01, K_CA -21.31 | one run |
| B-C | 1.0 | 0.6 | r2/006-008 | K_BC -4.27, K_CB -7.20 | P-0015 claims -4.32 / -7.31 |
| A-A | 1.5 | 0.4 | r2/003 | 13.18 +/- 0.04 | P-0013 narrowed |
| A-A far | 7.5 / 10.5 | 6 / 8 | r3/005, 006 | 15.00 / 9.63 | H12 test |
| C-C far | 7.5 / 10.5 | 6 / 8 | r3/007, 008 | 9.94 / 6.34 | H12 test |
| B-B far | 10.5 | 10 | r3/009 | 3.36 | H12 test |

Shape, K(r)/K(plateau): A-A (plateau 18.0): 1.0 0.62, 1.5 0.73, 2.0 0.83, 3 to 5 1.0, 7.5 0.83, 10.5 0.54. C-C (plateau 13.2): 1.0 0.71, 7.5 0.75, 10.5 0.48.

## Hypotheses

- **H9 (close approach weaker than the plateau): supported.** K(1)/K(plateau) about 0.6 to 0.7 for A-A, B-B; 0.7 for C-C.
- **H9b (species-dependent shape): supported.** C-C/A-A at r = 1 is 0.84 against 0.73 under one shape.
- **H10 (mixed A-B vs A-C shapes differ): supported at r = 1 to 3 by 10 percent.** Requests r2/005-009 pin it.
- **H11 (pairwise additivity at N > 2): open.** Needs the mixed shape first.
- **H12 (linear fall beyond the plateau): approximate.** Within about 5 percent; not a law.
- **H13 (one universal shape times species factor): rejected** at r = 1 and far range.
- **H14 (P-0013 A-A scale): supported.**
- **H16 (K_BA/K_AB = m_A/m_B constant in r): open.** 1.36, 1.39, 1.42, 1.41 at r = 1, 2, 3, far. A drift of about 4 percent, not resolved.
- **H17 (P = 2.5 exponent): untested directly.** The grant proposal of Keystone would test it but its design fails (noise). The far-field run of lab-vernier would test it through the shape.

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor about 0.0071 (sd 0.05 per coordinate, sqrt(2)*0.05/10). Any pe below 0.007 cannot be confirmed by single runs. Do not file sharpen claims with pe < 0.007.
- A replicated verdict says nothing about the coefficient. Use chi2 (sd 0.05) for K.
- The judge checks species and initial pairwise distances. It does not check duration. Put T limits in claim text.
- Lone-particle runs and runs where the predictor raises are not evidence for a pair claim.
- Attractive pairs collapse by T = 0.3 at r = 1 (separation under 0.2). Attractive close-range claims only at T <= 0.15 to 0.3.
- Fits start from the request setup, never the noisy t = 0 sample.
- Placing a pair at the boundary of a claim's r_range (e.g. 6.0 for a 6.0 limit) landed outside once (2026-11-20/r3/006). Keep margin.

## Budget (2026-11-22)

- Research: 40 allowance. Ledger shows 3.15 used today before round 2 (round-1 requests 001-003; r1/001 cost 1.03, budget_remaining 38.97 after it). Round 2 planned 5.28 (r2/005-009). If all run, about 31 left for the round's end.
- Review account: 15 allowance. P-0019 review used no new credit (existing runs). Round 2 review requests 001-004 (4.96). Left about 10.
- Grant: 120 credits if lab-b wins a proposal vote (did not; not expected).

## Plan for next session

1. Read results r2/001-004 (review account, P-0021 at separation 7, T 6). Write the P-0021 review: replicated if at least 3 in-domain runs have judge error <= 0.021, falsified if all cited runs are above 0.021. Cite only lab-b ids from r2/001-004. Do not cite r2/005-009 for P-0021.
2. Read r2/005-009. Refit A-B, A-C and B-C shapes with `pairfit`. Compare K_AB(4), K_AB(5), K_AC(2), K_BC(3) with the plateau pattern.
3. If K_AB(2) replicates (r1/001 and r2/005 agree within 2 sigma), file a small A-B claim at separation 2.0 (domain r_range [1.999, 2.001], species A and B, max_particles 2, T <= 0.8 stated in text), with 3 in-domain runs, pe 0.008. Do not file the far domain claim without a shape function.
4. File the 16-body prediction only if the lattice proposal is awarded (round 3 grant credit). Do not file it before the mixed shape is known.
5. Check whether lab-a's P-0019 K = 3.86 and my K_BB = 3.98 can be separated. Only a dedicated run at T = 0.3 (review account or research) would help. Not yet spent.
6. Do not file species-universal shape claims. Do not cite lone-particle runs.
