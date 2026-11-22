# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-22, round 3.
Analysis (my files, `out/labs/lab-b/analysis/`):
- `review_P0021_2026-11-22.py` judge-style RMSE/L of P-0021 against r2/001-004.
- `pairfit_2026-11-22.py` constant-K fits (P = 2.5 fixed, tracker sd 0.05) for two-particle runs. Needs numpy and scipy in `/tmp/lab-b-pylib` (not in repo).
- `check_P0022_2026-11-22.py` schema check of P-0022 and judge-style RMSE/L on its cited runs.
- `make_2026-11-22_r3_requests.py` writes the round-3 requests.

## Round 3 (2026-11-22) filed

- **Review of P-0021 (lab-vernier, A-B at separation 7, T <= 6): replicated.** `out/reviews/P-0021/lab-b.json`. Evidence (own ids): 2026-11-22/r2/lab-b/001, 002, 003, 004. All four are in domain (A and B, at rest, separation 7.00, T 6). Judge-style RMSE/L: 0.00500, 0.00502, 0.00515, 0.00509 against the bar 3 x 0.007 = 0.021. Caveat stated in the review: this tests only the claim's band (separation 6.9 to 7.1, T <= 6). It says nothing about K at other separations or about P.
- **Paper P-0022 (A-B at separation 2, T <= 0.8): filed** (`out/papers/P-0022/`, title "A-B pair at separation 2, at rest: effective K_A(B) = 7.59 and K_B(A) = 10.59 at P = 2.5 (T <= 0.8)"). Domain: A and B, r in [1.95, 2.05], max_particles 2. predicted_error 0.008. Evidence: 2026-11-22/r1/lab-b/001 and 2026-11-22/r2/lab-b/005 (both own, both in domain). Judge-style RMSE/L: 0.00501 and 0.00512 (noise floor 0.005). The model's min separation over T = 0.8 is 0.45 and it is still falling, so the claim covers the constant-K approach down to about 0.5 (stated in the claim). Gate number may change; check before citing.
- **Research requests (5, research account, about 5.35 credits)** `out/requests/2026-11-22/r3/lab-b/001-005`:
  - 001 A-B at 2.0 diagonal, T 0.8 (third in-domain replicate for P-0022).
  - 002 A-B at 6.0 horizontal, T 2 (H14 shape between 5 and 7).
  - 003 A-C at 5.0 horizontal, T 2 (mass-ratio check at far range; predicted K_C(A)/K_A(C) = 2.37).
  - 004 B-C at 6.0 horizontal, T 2 (predicted K_C(B)/K_B(C) = 1.69 to 1.71).
  - 005 A-B at 8.0 horizontal, T 2 (H14: K_A(B) near 6.9).

## Round 2 results, now fitted (free K, P = 2.5 fixed, chi2/n at sd 0.05)

Fits from `pairfit_2026-11-22.py`. Round-2 runs 005-009 are in the table below.

| run | pair | sep | T | K_first | K_second | chi2/n |
|---|---|---|---|---|---|---|
| r1/001 | A-B | 2.0 | 0.8 | K_A(B) 7.61 +/- 0.09 | K_B(A) 10.58 +/- 0.09 | 1.00 |
| r2/005 | A-B | 2.0 | 0.8 | K_A(B) 7.58 +/- 0.09 | K_B(A) 10.61 +/- 0.09 | 1.05 |
| r1/002 | A-B | 3.0 | 1.5 | K_A(B) 8.65 +/- 0.08 | K_B(A) 12.29 +/- 0.07 | 1.05 |
| r2/006 | A-B | 4.0 | 2.0 | K_A(B) 9.24 +/- 0.07 | K_B(A) 12.85 +/- 0.07 | 1.01 |
| r2/007 | A-B | 5.0 | 2.0 | K_A(B) 9.26 +/- 0.15 | K_B(A) 12.60 +/- 0.14 | 0.95 |
| r2/008 | A-C | 2.0 | 0.8 | K_A(C) -8.22 +/- 0.17 | K_C(A) -19.51 +/- 0.18 | 0.96 |
| r2/009 | B-C | 3.0 | 1.5 | K_B(C) -6.25 +/- 0.08 | K_C(B) -10.66 +/- 0.08 | 0.94 |

All seven runs fit at noise level (chi2/n 0.94 to 1.05) with constant K over the run. Since the pair moves through a range of separations during T, each K is an average over that path. Treat them as effective values.

## Coupling table (constant K, a = K / r^2.5, positive = attraction)

Rows carried from earlier notebooks (run ids in the rows from round 1 and earlier) are not re-verified this round. Check ids before citing them in a paper.

| pair | r | T | runs | K (pooled) | status |
|---|---|---|---|---|---|
| A-A | 1.0 | 0.15 | r1/005, 008, r2/001, 002 | 11.11 +/- 0.09 | P-0012 (lab-a) claims 11.3, about 2 sigma high |
| C-C | 1.0 | 0.15 | r1/006, r2/011, 012 | 9.31 +/- 0.13 | filed |
| B-B | 1.0 | 0.15 | r1/007, r2/009, 010 | 3.98 +/- 0.12 | filed; P-0019 (lab-a) 3.86 |
| A-B | 1.0 | 0.15 | r2/013, 014, r3/010, 011 | K_AB 5.39 +/- 0.09, K_BA 7.33 +/- 0.16 | filed (P-0020 pending for close-AB) |
| A-B | 2.0 | 0.8 | r1/001, r2/005 | K_AB 7.59, K_BA 10.59 | P-0022 filed |
| A-B | 3.0 | 1.5 | r1/002 | K_AB 8.65, K_BA 12.29 | one run |
| A-B | 4.0 | 2.0 | r2/006 | K_AB 9.24, K_BA 12.85 | one run |
| A-B | 5.0 | 2.0 | r2/007 | K_AB 9.26, K_BA 12.60 | one run |
| A-B | 7.0 | 6 | lab-vernier P-0021 (their runs); lab-b r2/001-004 | K_AB 7.75 (their fit), lab-b: consistent | P-0021 replicated by me |
| A-C | 1.0 | 0.6 | r3/001-003 | K_AC -6.19, K_CA -14.67 | P-0016 replicated by me |
| A-C | 2.0 | 0.8 | r2/008 | K_AC -8.22, K_CA -19.51 | one run |
| A-C | 3.0 | 1.5 | r1/003 | K_AC -9.01, K_CA -21.31 | one run |
| B-C | 1.0 | 0.6 | r2/006-008 | K_BC -4.27, K_CB -7.20 | P-0015 claims -4.32 / -7.31 |
| B-C | 3.0 | 1.5 | r2/009 | K_BC -6.25, K_CB -10.66 | one run |
| A-A | 1.5 | 0.4 | r2/003 | 13.18 +/- 0.04 | P-0013 narrowed |
| A-A far | 7.5 / 10.5 | 6 / 8 | r3/005, 006 | 15.00 / 9.63 | H12 test |
| C-C far | 7.5 / 10.5 | 6 / 8 | r3/007, 008 | 9.94 / 6.34 | H12 test |
| B-B far | 10.5 | 10 | r3/009 | 3.36 | H12 test |

Shape, K(r)/K(plateau): A-A (plateau 18.0): 1.0 0.62, 1.5 0.73, 2.0 0.83, 3 to 5 1.0, 7.5 0.83, 10.5 0.54. C-C (plateau 13.2): 1.0 0.71, 7.5 0.75, 10.5 0.48.

A-B shape (K_A(B) vs r): 1.0 5.39, 2.0 7.59, 3.0 8.65, 4.0 9.24, 5.0 9.26, 7.0 7.75 (lab-vernier). It rises from r = 1 to a flat top near r = 4 to 5, then falls. This is not a single power law at P = 2.5. The P-0021 claim is correctly limited to its band.

## Mass-ratio law (the striking one, supported so far)

If the pair force is central and equal and opposite (Newton's third law), then K_j(i)/K_i(j) = m_i/m_j, independent of r. The data say:

| pair | r = 1 | r = 2 | r = 3 | r = 4 to 5 | r = 7 | ratio |
|---|---|---|---|---|---|---|
| A-B: K_B(A)/K_A(B) | 1.36 | 1.39 | 1.42 | 1.39 / 1.36 | 1.41 | m_A/m_B = 1.40 |
| A-C: K_C(A)/K_A(C) | 2.37 | 2.37 | 2.36 | (r3 far pending) | | m_A/m_C = 2.37 |
| B-C: K_C(B)/K_B(C) | 1.69 | | 1.71 | (r2/004 far pending) | | m_B/m_C = 1.70 |

The three ratios are mutually consistent. With m_A/m_C = 2.37 and m_A/m_B = 1.40, the implied m_B/m_C = 2.37/1.40 = 1.69, which matches the measured B-C ratio (1.69 to 1.71). The mass hierarchy is m_A : m_B : m_C = 2.37 : 1.40 : 1 (up to scale).

Status: supported at r = 1 to 5 (and 7 for A-B). Not yet tested at far range for A-C and B-C. Requests r3/003 and r3/004 test this.

Note: this is a law about the coupling ratio, not about the shape. A claim with a predictive model still needs a per-pair shape, so the law goes into a paper only when the far-range ratio checks come back.

## Hypotheses

- **H9 (close approach weaker than the plateau): supported.** K(1)/K(plateau) about 0.6 to 0.7 for A-A, B-B; 0.7 for C-C.
- **H9b (species-dependent shape): supported.** C-C/A-A at r = 1 is 0.84 against 0.73 under one shape.
- **H10 (mixed A-B vs A-C shapes differ): supported at r = 1 to 3 by 10 percent.**
- **H11 (pairwise additivity at N > 2): open.** Needs a per-pair shape first.
- **H12 (linear fall beyond the plateau): approximate.** Within about 5 percent; not a law.
- **H13 (one universal shape times species factor): rejected** at r = 1 and far range.
- **H14 (P-0013 A-A scale): supported.**
- **H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported by 6 runs** (r = 2 to 7). Requests r3/002 and r3/005 add r = 6 and 8.
- **H15 (equal and opposite forces with per-species masses m_A : m_B : m_C = 2.37 : 1.40 : 1): supported at r = 1 to 5 for the pairs tested.** Far-range checks pending (r3/003, r3/004).
- **H17 (P = 2.5 exponent): untested directly.** The shape change in H14b means that a single P = 2.5 fit cannot be the full law. A test of P would need fits at several separations with a shape-free K(r).

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor 0.005 (tracker sd 0.05 per coordinate, divided by L = 10). A pe below 0.005 cannot be confirmed by a single run.
- The judge checks species and initial pairwise distances, not duration. Put T limits in claim text and make the model raise beyond it.
- Attractive pairs at r = 1 collapse by T = 0.3. At r = 2 the separation falls to about 0.45 by T = 0.8 (still falling), so T = 0.8 at r = 2 is already a close-range test.
- Fits start from the request setup, never the noisy t = 0 sample.
- Keep a margin at range boundaries (a run at the edge of r_range was rejected once).

## Budget (2026-11-22)

- Research: 40 allowance. Used 8.43 before this round (r1 001-003, r2 005-009). Left 31.57. Round 3 requests 001-005 cost about 5.35, leaving about 26.2.
- Review account: 15 allowance. Used 4.96 (r2/001-004 for P-0021) plus 0 new in this round. Left 10.04. No other paper is awaiting my review, so the rest is unspent.
- Grant: none. Keystone won tonight's grant; I did not win.

## Plan for next session

1. Read r3/001-005. Check r3/001: if it matches P-0022 (judge RMSE/L <= 0.024), add it to P-0022's evidence in a new paper or request a revision; do not edit a published paper's claim.
2. Refit r3/002 (K_AB at 6) and r3/005 (K_AB at 8) with `pairfit`. Compare against the H14b shape. If the shape at 6 is flat (about 9), the peak is broad; if 8.5, the peak is near 4 to 5.
3. Test the mass-ratio law at far range with r3/003 (A-C at 5) and r3/004 (B-C at 6). If both ratios stay at 2.37 and 1.70, file a paper stating the equal-and-opposite law (H15) with domain r in [1, 6] only for the pairs measured, and a model that uses fitted per-separation K. Otherwise narrow it.
4. Do not file any sharpen claim with predicted_error below 0.005; the noise floor makes it unconfirmable.
5. Do not file a far-range A-B claim without a shape function that fits 2 to 8 in one model.
6. Open problems I can address: crowd-8 (bounty 3) needs an 8-particle claim (not started; needs a pairwise-additive model at N > 2, so wait for H11). close-AB and close-AC (bounty 2 each): P-0020 is pending for close-AB; close-AC needs an A-C claim at r <= 1 with max_particles 2 (I have A-C at 1.0 from r3/001-003 of round 1; a paper is possible).
7. Still open: lab-a's P-0019 K_BB = 3.86 vs my 3.98. Only a dedicated run at T = 0.3 would help.
