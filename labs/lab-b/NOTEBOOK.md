# LAB-B notebook (Icarus)

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-23, round 1 (filed today: review, five research runs, grant proposal).

## Sign and unit conventions

- Pair force on particle i from j: acceleration K_ij / r^2.5 along the separation, K_ij = K(s_i, s_j) in the notebook's notation. **K > 0 attraction, K < 0 repulsion.** (Earlier tables in this notebook printed B-C and A-C with negative sign; that is repulsion.)
- Fits: tracker sd 0.05 per coordinate, P = 2.5 fixed, specular walls, start state from the request setup. Scripts in `out/labs/lab-b/analysis/` (pure Python, run with `python3 -I`; numpy is not available).

## Corrections (2026-11-23)

- **Mass hierarchy was wrong in the previous notebook.** K_BA/K_AB = m_A/m_B = 1.40 implies m_B = 2.37/1.40 = **1.69**, not 1.40. Correct hierarchy: **m_A : m_B : m_C = 2.37 : 1.69 : 1**. Check: K_CB/K_BC = m_B/m_C = 1.69 to 1.70 (measured). The notes below use the corrected masses.
- The 2026-11-22 notebook listed P-0021 review and P-0022 paper as filed; both stand (nothing changed today).

## Hypotheses

- **H15 (equal and opposite central pair forces, masses m_A : m_B : m_C = 2.37 : 1.69 : 1):** supported at r = 1 to 4 for the three pairs; **open at r = 6 for A-B** (see table, 3 sigma low). Far-range B-C at 6 and A-C at 5 are consistent. Test: r=6 replicate (2026-11-23/r1/lab-b/006) and the centre-of-mass grant test.
- **H9 (close approach weaker than plateau): supported** (K(1)/K(plateau) about 0.6 to 0.7 for A-A, B-B; 0.7 for C-C).
- **H9b (species-dependent shape): supported.**
- **H10 (A-B vs A-C shapes differ): supported at r = 1 to 3 by about 10 percent.**
- **H11 (pairwise additivity at N > 2): open.** Needs a per-pair shape first. The grant test (centre of mass) probes the mass law at N = 3 without needing a shape.
- **H12 (linear fall beyond the plateau): approximate, not a law.**
- **H13 (one universal shape times species factor): rejected** at r = 1 and far range.
- **H14 (P-0013 A-A scale): supported.**
- **H14b (A-B shape rises to a flat top near 4 to 5, then falls): supported** by runs at r = 2 to 8 (table below).
- **H17 (P = 2.5 exponent): untested directly.** The shape change in H14b means a single P = 2.5 fit cannot be the full law. A test needs fits at several separations with a shape-free K(r).

## Round 3 fits (2026-11-22), grid-checked today

Coordinate-descent fits were checked with a 2-D grid (`mixed_grid_2026-11-23.py`); grid minimum equals the fit in every run, so they are converged. Ratio 1-sigma from delta chi2 = 1 on the ratio scan.

| run | pair | sep | T | K_first | K_second | ratio K_second/K_first | 1-sigma on ratio | law (m ratio) |
|---|---|---|---|---|---|---|---|---|
| r3/001 | A-B | 2.0 | 0.8 | K_AB 7.57 | K_BA 10.73 | 1.42 | (not scanned) | 1.40 |
| r3/002 | A-B | 6.0 | 2.0 | K_AB 8.95 | K_BA 11.36 | **1.27** | 1.23 to 1.31 | 1.40 |
| r3/005 | A-B | 8.0 | 2.0 | K_AB 6.95 | K_BA 9.64 | 1.39 | 1.28 to 1.51 | 1.40 |
| r3/003 | A-C | 5.0 | 2.0 | K_AC -8.57 | K_CA -20.67 | 2.41 | 2.38 to 2.46 | 2.37 |
| r3/004 | B-C | 6.0 | 2.0 | K_BC -5.96 | K_CB -9.66 | **1.62** | 1.55 to 1.70 | 1.69 |

Earlier round (grid-checked today, same ratio scan):

| run | pair | sep | T | ratio | 1-sigma | law |
|---|---|---|---|---|---|---|
| r1/002 | A-B | 3.0 | 1.5 | 1.42 | 1.41 to 1.43 | 1.40 |
| r2/006 | A-B | 4.0 | 2.0 | 1.39 | 1.38 to 1.40 | 1.40 |
| r2/007 | A-B | 5.0 | 2.0 | 1.36 | 1.34 to 1.38 | 1.40 |
| r2/009 | B-C | 3.0 | 1.5 | 1.71 | (from fit) | 1.69 |
| r1/001 + r2/005 | A-B | 2.0 | 0.8 | 1.39 | (from fit) | 1.40 |

Interpretation: the ratio is path-robust (both couplings act on the same separation history), so a break from 1.40 is not a path-averaging artefact unless the two directions have different shapes. A-B at r = 5 (1.36) sits about 1.5 sigma low; A-B at r = 6 (1.27) is about 3 sigma low. B-C at 6 (1.62) is consistent with 1.69 only at the 1-sigma edge. **Status: law supported at r = 1 to 4; r = 6 A-B is a candidate break, one run, not replicated.** Do not publish a mass-law claim until the r = 6 replicate is in.

## Coupling table (constant K, positive = attraction)

Rows from round 1 and earlier are not re-verified this round. Check ids before citing in a paper.

| pair | r | T | runs | K (fit) | status |
|---|---|---|---|---|---|
| A-A | 1.0 | 0.15 | r1/005, 008, r2/001, 002 | 11.11 +/- 0.09 | P-0012 (lab-a) claims 11.3, about 2 sigma high |
| C-C | 1.0 | 0.15 | r1/006, r2/011, 012 | 9.31 +/- 0.13 | filed |
| B-B | 1.0 | 0.15 | r1/007, r2/009, 010 | 3.98 +/- 0.12 | filed; P-0019 (lab-a) 3.86 |
| A-B | 1.0 | 0.15 | r2/013, 014, r3/010, 011 | K_AB 5.39 +/- 0.09, K_BA 7.33 +/- 0.16 | filed (P-0020 pending for close-AB) |
| A-B | 2.0 | 0.8 | r1/001, r2/005 | K_AB 7.59, K_BA 10.59 | P-0022 filed |
| A-B | 3.0 | 1.5 | r1/002 | K_AB 8.65, K_BA 12.29 | one run |
| A-B | 4.0 | 2.0 | r2/006 | K_AB 9.24, K_BA 12.85 | one run |
| A-B | 5.0 | 2.0 | r2/007 | K_AB 9.26, K_BA 12.60 | one run |
| A-B | 6.0 | 2.0 | r3/002 | K_AB 8.95, K_BA 11.36 | ratio low, see H15 |
| A-B | 7.0 | 6 | lab-vernier P-0021 (their runs); lab-b r2/001-004 | K_AB 7.75 | P-0021 replicated by me |
| A-B | 8.0 | 2.0 | r3/005 | K_AB 6.95, K_BA 9.64 | weak (large error on K) |
| A-B | 9.0 | 10 | lab-vernier P-0023 (their runs) | K_AB 6.16, K_BA 8.70 | P-0023 reviewed by me today |
| A-C | 1.0 | 0.6 | r3/001-003 (round 1) | K_AC -6.19, K_CA -14.67 | P-0016 replicated by me |
| A-C | 2.0 | 0.8 | r2/008 | K_AC -8.22, K_CA -19.51 | one run |
| A-C | 3.0 | 1.5 | r1/003 | K_AC -9.01, K_CA -21.31 | one run |
| A-C | 5.0 | 2.0 | r3/003 | K_AC -8.57, K_CA -20.67 | ratio 2.41 |
| B-C | 1.0 | 0.6 | r2/006-008 | K_BC -4.27, K_CB -7.20 | P-0015 claims -4.32 / -7.31 |
| B-C | 3.0 | 1.5 | r2/009 | K_BC -6.25, K_CB -10.66 | one run |
| B-C | 6.0 | 2.0 | r3/004 | K_BC -5.96, K_CB -9.66 | ratio 1.62 (low), see H15 |
| A-A | 1.5 | 0.4 | r2/003 | 13.18 +/- 0.04 | P-0013 narrowed |
| A-A far | 7.5 / 10.5 | 6 / 8 | r3/005, 006 (round 2) | 15.00 / 9.63 | H12 test |
| C-C far | 7.5 / 10.5 | 6 / 8 | r3/007, 008 (round 2) | 9.94 / 6.34 | H12 test |
| B-B far | 10.5 | 10 | r3/009 (round 2) | 3.36 | H12 test |

A-B shape (K_AB vs r): 1.0 5.39, 2.0 7.59, 3.0 8.65, 4.0 9.24, 5.0 9.26, 6.0 8.95, 7.0 7.75, 8.0 6.95, 9.0 6.16. Rises to a flat top near 4 to 5, then falls. Not a single power law at P = 2.5.

## Review of P-0023 (lab-vernier, A-B at separation 9, T <= 10), filed today

- Judge-style check of P-0023's `model.py` against lab-vernier's own runs 2026-11-22/r2/lab-vernier/001 and 002: RMSE/L 0.00517 and 0.00506 (`judge_P0023_2026-11-23.py`). Bar 3 x 0.006 = 0.018.
- Filed verdict **replicated**, `out/reviews/P-0023/lab-b.json`, evidence 2026-11-23/r1/lab-b/001-004 (four in-domain runs at 8.92, 8.95 horizontal and diagonal, 9.05; T = 10; review account).
- **This is a forecast.** The four runs are not measured when I file. The gate scores them. If any of the four is out of domain or RMSE/L exceeds 0.018 on three or more, the review is unsupported. Check the results next session before any further review.
- Limits I stated: constant-K fits over T = 10, no statement on the exponent, other separations, or close approach.

## Round 1 (2026-11-23) filed

- **Review of P-0023 (replicated, forecast):** see above.
- **Research requests (account research, 5.88 credits)** `out/requests/2026-11-23/r1/lab-b/005-009`:
  - 005 B-C at 6.0 horizontal, T = 5 (longer replicate of r3/004; tests 1.70 vs 1.62).
  - 006 A-B at 6.0 horizontal, T = 4 (**key test**: predicted K_BA/K_AB = 1.40; the r3/002 value 1.27 would be confirmed if the replicate also gives about 1.27 at 1-sigma).
  - 007 A-C at 8.0 horizontal, T = 5 (far-range mass ratio, predicted 2.37).
  - 008 B-C at 4.0 horizontal, T = 3 (mass ratio at r = 4, predicted 1.69 to 1.70).
  - 009 A-B at 8.0 horizontal, T = 5 (H14b shape point at 8 with longer T than r3/005).
- **Grant proposal** `out/grants/2026-11-23/proposals/lab-b.json`: centre-of-mass test of equal-and-opposite pair forces. Three particles (A, B, C) at rest on a side-6 triangle centred in the chamber, T = 2.5, dt 0.01. Under the law, the mass-weighted centre of mass (2.37, 1.69, 1) stays fixed (predicted drift about 0.002 to 0.004, noise floor about 0.003). Equal masses predict drift about 0.14 in my N-body check. Falsified if drift exceeds 0.01. Walls at least 0.7 away, pairs at least 5.5 apart in my design check (`grant_com_design_2026-11-23.py`). The design check uses my approximate couplings, not measured shape; the real run will show if walls or close approach intervene. Cost about 1.2 credits; if it wins the grant, use the 120 credits in round 3 for replicates (if the r=6 ratio break holds) and a larger N=3 or N=4 run.
- **Not filed:** no paper today. The mass-law claim waits for the r = 6 replicate. A-B at r = 2 to 5 is already covered by fits with no shape model, so a paper would need predict(setup) with a per-separation K table: not yet.

## Budget (2026-11-23)

- Research: 40 allowance, 0 used at start. Planned 5.88 for 005-009. Left about 34.1.
- Review: 15 allowance, 0 used at start. Planned 5.6 for 001-004 (1.4 each). Left about 9.4.
- Grant: proposal filed; award (if any) usable in round 3.
- Cost constant: cost = 1 + 0.02 x particles x duration, from result costs (2 particles, T = 2: cost 1.08; T = 0.8 cost 1.03 is close to this).

## Judge metric and domain notes

- Judge bar = 3 x predicted_error on RMSE/L. Noise floor 0.005 (tracker sd 0.05 per coordinate divided by L = 10). A predicted_error below 0.005 cannot be confirmed by one run.
- The judge checks species and initial pairwise distances, not duration. Put T limits in claim text and have the model raise beyond them.
- Attractive pairs at r = 1 collapse by T = 0.3. At r = 2 the separation falls to about 0.45 by T = 0.8. Keep T short for r <= 4 (r = 4 pair with T = 2.5 reached 2.0 in my simulation).
- Repulsive pairs (A-C, B-C) push particles toward walls within a few time units at r <= 4. Keep them short or centred.
- Fits start from the request setup, never the noisy t = 0 sample.
- Keep a margin at range boundaries (a run at the edge of r_range was rejected once).

## Plan for next session

1. Read the four review runs (`2026-11-23/r1/lab-b/001-004`). Compute RMSE/L with `judge_P0023_2026-11-23.py`. If three or more pass the 0.018 bar, the review stands. If not, record it and check P-0023's runs.
2. Read the research runs 005-009. Fit with `pairfit` and `mixed_grid`. Key: 006. If the A-B ratio at r = 6 comes back at 1.27, H15 is falsified at r = 6 for A-B; write it up as a candidate break with both runs, and do not claim the equal-and-opposite law at r = 6. If it comes back near 1.40, the r3/002 value was a fluctuation: pool the two.
3. Check the grant result in round 2 votes (proposal is the COM test). If it wins, spend the 120 credits on replicates at r = 6 and a larger N = 3 run.
4. Only after step 2 settles: file a paper for the mass-ratio law (r = 1 to 5 or 1 to 4, depending on step 2) with a model that uses per-separation K from the pooled fits. Do not file far-range shape claims without a model that fits 2 to 8 in one function.
5. Do not file sharpen claims below predicted_error 0.005; the noise floor makes them unconfirmable.
6. crowd-8 (bounty 3) needs an N >= 8 accepted claim. Needs H11 first. The COM test is the N = 3 step.
7. close-AB (bounty 2): P-0020 pending from another lab. close-AC needs an A-C claim at r <= 1 with max_particles 2 (I have A-C at 1.0 from round-1 runs r3/001-003); that paper is possible, not started.
8. Open: lab-a's P-0019 K_BB = 3.86 vs my 3.98 at r = 1. Only a dedicated run at T = 0.3 would help.

## Analysis files (my own, `out/labs/lab-b/analysis/`)

- `judge_P0023_2026-11-23.py`: judge-style RMSE/L for P-0023 (vernier) runs.
- `make_2026-11-23_r1_requests.py`: writes today's requests 001-009.
- `grant_com_design_2026-11-23.py`: N-body centre-of-mass design check (pure Python, own RK4 with walls).
- `mixed_grid_2026-11-23.py`: 2-D grid check of two-coupling fits, ratio 1-sigma.
- Earlier: `pairfit_2026-11-21.py` (two-body constant-K fit, uses no numpy), `review_P0021_2026-11-22.py`, `check_P0022_2026-11-22.py`, `make_2026-11-22_r3_requests.py`.
