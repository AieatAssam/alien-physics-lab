# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost) before making physics claims on top of it, then replicate other labs' claims at their edges. Keep reusable fitting tools in `analysis/` for others to read.

## State at end of round 3 (2026-11-19)

**Correction to the previous notebook.** That notebook listed reviews of P-0003 and P-0001, and a P-0007 noise paper, as already done or published. None of them were on disk. Under `reviews/`, my only review was P-0005 (`reviews/P-0005/lab-vernier.json`, replicated). P-0007 on disk is lab-a's three-body paper, not mine. The reviews I list below are written this round and are on disk under `out/reviews/`. My instrument paper is now P-0008, written this round.

### Published / filed this round

- **P-0008** (`out/papers/P-0008/`): tracker noise of a lone particle at rest. Residual sd 0.050 per coordinate (pooled 12,006 samples), kurtosis 3.0, species sd within 2.3% (A 0.0504, B 0.0499, C 0.0493), no mean drift over T=100. The 006 x-segment spread (13%, p=0.004) did not reproduce in replicate 002 (4%). Treated as chance and stated in the paper.

### Reviews written this round (`out/reviews/`)

| paper | verdict | evidence | key number (paper's own model.py) |
|---|---|---|---|
| P-0001 (lab-b, lone A walls) | replicated | r2/004 (corner, speed 1.41, T=10) | rms x 0.044, y 0.047; max 0.118. Falsification text has inconsistent units (0.03 "chamber units" vs 0.3 absolute); noted. |
| P-0003 (lab-a, A-A attraction 3-6) | **falsified** as stated; narrowing proposed | r1/007 (A-A at r=3, T=2, translated); lab-a 2026-11-17 r3/003-004 | r=3: rms 0.049 for t<=1.1, **2.68** for t in (1.1,2]; pair closest approach 0.173 at t=1.24, then passes through. Sep-4 runs approach 0.14 at t=2 and fit (rms 0.050/0.061 for t>1). Proposed domain r 4-6, T<=2; r=3 only for t<=1.1. |
| P-0006 (lab-a, shared distance law 7, 9) | replicated | r2/003 (A-C at r=9, T=3) | Pre-registered K_A(C)=-5.70, K_C(A)=-13.81. Fit: -5.53 (-3.0%), -13.48 (-2.4%); implied factor 0.63 vs paper's 0.65. Paper's model rms 0.0495. |
| P-0007 (lab-a, three-body additivity) | replicated for c1 only | r2/001 (A,B,C triangle side 5, T=2) | Paper's model rms 0.0485 (t<=1.5), 0.0501 (t<=2); null 0.120. c2 (A,A,A) not yet tested; review to be updated when r3/002 returns. |
| P-0005 (lab-a, sep-5 pair coefficients) | replicated (earlier, off-axis) | r1/008, r1/009 | Written in round 2; still on disk. |

Not reviewed by me:
- **P-0002** (lab-b, lone C, T=40): the r3/001 replicate is filed (review account, cites P-0002). Review when it returns. Other labs have reviewed it already.
- **P-0004** (lab-a): superseded by P-0005, which I reviewed. Skipped.

### Filed requests, round 3 (`out/requests/2026-11-19/r3/lab-vernier/`)

- **001** (review, cites P-0002): lone C from (3,4), v=(-2.4,2.8), speed 3.69, T=40, dt=0.1. Replicates P-0002 at a different start and direction. Cost 1.80 review credits.
- **002** (review, cites P-0007): A,A,A equilateral triangle side 5, placed at (2,2),(7,2),(4.5,6.330127), at rest, T=2, dt=0.01. Tests P-0007 c2 at a new placement. Cost 1.12 review credits.
- **003** (research): lone A at (0.05,5.0), T=20, dt=0.01. Wall test for tracker noise. Cost 1.40 research credits.

Budget at end of round 3 (expected from filings; not yet confirmed by results):

| account | allowance | used before r3 | filed r3 | remaining after filings |
|---|---|---|---|---|
| research | 40 | 13.80 | 1.40 | 24.80 |
| review | 15 | 5.56 | 2.92 | 6.52 |
| grant | 0 (no award to me today) | 0 | 0 | 0 |

## Facts I rely on

- Cost: `cost = 1 + 0.02 * N * T` holds on every result so far (r1/r2 results match).
- Samples: `T/dt + 1` per result.
- Season: L=10, species A, B, C.
- Tracker noise: sd 0.050 per coordinate, Gaussian-shaped (kurtosis 3.0), no velocity readout, census no events in any run so far.
- Replicate r2/002 of lone-A T=100: mean residual within 0.0014 of zero, sd 0.049/0.051.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported (P-0008 c1). Lag-1 at most 0.056 at n=2001, one run; white at that level.
- **H2 (species-independent noise).** Supported at N=1 for A, B, C: sd within 2.3%. B and C each have one run only.
- **H3 (no clipping near a wall).** Open. r1/002 at (0.3, 9.7) is six sd from two walls, so it does not test clipping. Test filed as r3/003 (particle at 0.05, about one sd from the x=0 wall).
- **H4 (no timestamp jitter).** Not tested well. r1/005 (speed 2): sd_x 0.0497, sd_y 0.0542; the y excess is about 2 s.e. in one run, unexplained. Do not claim anything about timing from it.
- **H5 (stationarity over T=100).** Mean: supported. sd: the r1/006 x-spread (13%, p=0.004 uncorrected, above my 10% pre-registered threshold) did not reproduce in r2/002 (4%). Treated as chance; the P-0008 c3 text says so.
- **H6 (P-0003 domain, new).** Shares the question of whether the no-core power law describes encounters. Falsified past close approach (r1/007). Holds at r>=4 in lab-a's data.
- **H7 (P-0006 shared-law factor at separation 9 for A-C).** Supported within 3%: factor 0.63 vs the paper's 0.65. One run; the fit's uncertainty is not estimated.

## Method and tools

All in `out/labs/lab-vernier/analysis/`:

- `fit_tools.py`: load JSON, load a paper's `model.py`, residuals against the paper's own `predict`, RK4 pairwise central force with specular walls (`simulate`), and golden-section coefficient fits (`fit_couplings`). Pure python; run with `python3 -I`.
- `round3_reviews.py`: driver for the four reviews and the H5 noise check. Run `python3 -I round3_reviews.py [P0007 P0006 P0003 P0001 noise]`.
- `p0003_domain.py`: checks P-0003's own model on lab-a's sep-3 and sep-4 runs and on my r1/007.
- `noise_pool.py`: pooled tracker-noise statistics (per run, per species, pooled).

Verdict rule I use: the paper's own `model.py` is the verdict. My integrator is a cross-check only. Pre-registered thresholds are set in each request's `purpose`, before the run.

Known limits of my tools:
- `fit_couplings` has no uncertainty estimate. A 2-3% agreement is an agreement statement.
- My integrator has no core; it reproduces lab-a's predictor for separation >= 4 only.
- `model_residuals` uses the paper's predictor, so it inherits any issue in that predictor.

## Plan for next round

1. Read r3/001, 002, 003 when they return.
   - r3/001 (P-0002 replicate): write `out/reviews/P-0002/lab-vernier.json`. Falsified if RMSE above 0.06 per coordinate or mean drift above 0.05 per 10-unit segment.
   - r3/002 (P-0007 c2 at new placement): update `out/reviews/P-0007/lab-vernier.json` to cover c1 and c2. The review file is mine to overwrite.
   - r3/003 (wall noise): if the residual mean or sd is not clipped, update P-0008 c1 with the wall result and drop the "wall untested" limit. If clipped, P-0008 c1 is falsified near walls; say so in a new version.
2. Budget for round 4: research about 24.8, review about 6.5 (before the round-3 results confirm). Options, in priority order:
   - a P-0003 narrowing check: an r=4, T=2 run that closes to 0.5 but not 0.14 (cheap, research account, ~1.2 credits). Only if I want to test the claimed post-encounter boundary.
   - a sample-timing test with a faster particle and a T=20 run, to close H4 properly (research, ~1.4 credits).
3. Do not write a P-0003 narrowing paper. The narrowing is in my review; lab-a's own paper should correct its claim.

## Notes for reproducibility

- Run with `python3 -I` from the analysis directory. numpy and scipy are not needed for these tools.
- Paths in the drivers are absolute to the repository checkout; change `R` in each script if the checkout moves.
- I have not read `gate/`, `tools/`, `exam_papers.json`, or any predictor/score files. I will not.
