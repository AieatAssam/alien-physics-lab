# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-21, round 2.

## Status

- **Accepted papers: 1** (scoreboard). Submitted papers: **P-0010** (shared radial factor, separation 6 to 9; accepted per the scoreboard) and **P-0014** (two particles of species A or C at separation 2.5 to 3.5, no radial factor). P-0014 is the paper I called "P-0012" in round 1; the gate renumbered it.
- **Unsupported reviews: 3** (unchanged). Standing reviews: P-0011 (replicated), P-0004 (replicated), P-0007 (narrowed), and, new this round, **P-0009 (replicated)**.
- **Retraction (my own, this round):** the round-3 "universal close-range factor 0.55" (notebook of round 2, sections "Close-range pairs at r0 = 1.5") is withdrawn. It came from a fitter whose search window was too narrow for the fitted values. Re-fitted, the round-3 runs give 0.72 to 0.90 at r = 1.5. Details below.
- **Fitter bug (repo code):** `labs/lab-keystone/analysis/round2_r1_check.py` `simulate()` uses a fixed internal step `H = 0.005` and sets `steps per sample = round(sample_dt / H)`. Two failure modes:
  - `sample_dt < 0.0025` (e.g. 0.002): zero steps, particles never move, every K gives the same residual (this round's first pass, 006-010).
  - `sample_dt` not a multiple of 0.005 (e.g. 0.004): time is rounded to the nearest multiple of 0.005, so the simulated clock runs fast (0.004 becomes 0.005 per sample, about 25% fast). This affected the round-3 fits of 2026-11-20/r3 (dt = 0.004). Only dt = 0.005, 0.01, 0.02 and similar multiples are safe.
  - Fix used from this round: integrate at `h = sample_dt` (`out/labs/lab-keystone/analysis/round4_scoring_2026-11-21.py`, `round3_refit_2026-11-21.py`).

## Round-2 results scored this session

### Review account, P-0009 (lab-a, B, C, C triangle, side 5): **replicated**

Requests `2026-11-21/r1/lab-keystone/001-005`, all in P-0009's formal domain (species in [B, C], N = 3, pairwise separation in [4.99, 5.01]). Judge error (RMSE/10 vs tracker) from `labs/lab-keystone/analysis/review_error.py`:

| req | triangle | error |
|---|---|---|
| 001 | B,C,C side 5, rotated 30 deg | 0.00505 |
| 002 | B,C,C side 4.99 | 0.00492 |
| 003 | B,C,C side 5.0095 | 0.00509 |
| 004 | C,C,C side 5 | 0.00512 |
| 005 | B,B,B side 5 | 0.00491 |

Bar 3 x 0.01 = 0.03. All five are at the tracker-noise floor. Filed as `out/reviews/P-0009/lab-keystone.json`, verdict replicated. The comment says what the metric cannot show: it does not resolve coupling errors of a few percent.

### Research account, close-range pairs (006-010), corrected fit

Two-particle fits, constant K/r^2.5 with a free coupling for each direction (f0 = particle 0 on 1, f1 = particle 1 on 0), as fractions of the P-0005 sep-5 table. Integrated at h = dt = 0.002, search over f in [-0.2, 1.2].

| req | pair | r0 | T | f0 | f1 | fit rms | table (f=1) rms | zero-force rms |
|---|---|---|---|---|---|---|---|---|
| 006 | A-A | 1.0 | 0.2 | 0.61 | 0.57 | 0.052 | 0.391 | 0.097 |
| 007 | C-C | 1.0 | 0.2 | 0.76 | 0.74 | 0.051 | 0.059 | 0.085 |
| 008 | A-B | 1.0 | 0.2 | 0.61 | 0.67 | 0.050 | 0.060 | 0.070 |
| 009 | A-C (repulsive) | 1.5 | 0.4 | 0.82 | 0.80 | 0.049 | 0.054 | 0.118 |
| 010 | B-C (repulsive) | 1.5 | 0.4 | 0.76 | 0.79 | 0.050 | 0.052 | 0.077 |

Noise floor is about 0.05 per coordinate, so all five fits reach it. The pre-registration (plateau 0.55, or power-law steepening) was not confirmed: the factor is species-dependent and sits between 0.6 and 0.8 at r = 1.0 to 1.5. Fit precision is roughly ±0.03 (grid spacing), not profiled. Table (f=1) fits badly for A-A at r=1.0 (rms 0.39), so the table is not usable there.

### Round-3 re-fit (2026-11-20/r3/lab-keystone 001-004, r0 = 1.5, T = 0.4, dt = 0.004)

Same corrected fitter. This replaces the round-3 values.

| pair | old fit (window-limited) | corrected f0, f1 | rms |
|---|---|---|---|
| A-A | 0.59, 0.57 | 0.73, 0.72 | 0.047 |
| B-B | 0.57, 0.54 | 0.90, 0.80 | 0.051 |
| C-C | 0.55, 0.56 | 0.86, 0.87 | 0.051 |
| A-B | 0.54, 0.54 | 0.71, 0.74 | 0.049 |

Two errors in the old fit, both mine: (1) the old window was ±30% around the pre-registered 0.85 × table, so the lower edge (0.595) sat above the fitted values, and the fits were pinned to it; (2) the old integrator used step 0.005 for dt = 0.004 (see the fitter bug above), so simulated time ran about 25% fast. Either alone could produce the 0.55; together they did. **Claim-level consequence:** no universal factor; per-pair values at 1.5 sit at 0.7 to 0.9 and are close to lab-c's P-0013 scales (S_AA 0.753, S_AC 0.811, S_CC 0.874).

### Current picture of the close-range factor f(r)

- r = 1.0 (T = 0.2): A-A 0.59, A-B 0.64, C-C 0.75.
- r = 1.5 (T = 0.4): A-A 0.72, A-B 0.72, B-B 0.85, C-C 0.86, A-C 0.81, B-C 0.78.
- r = 2.5 to 3.5: about 1.0 (P-0014, my paper).

So f rises from about 0.6 at r = 1 to about 1 by 2.5. The shape between 1.5 and 2.5 is unmeasured.

## Review-account requests filed this round (`out/requests/2026-11-21/r2/lab-keystone/`)

Budget: review allowance 15, used 5.60 before this round, requests 001-009 cost 9.14, so 0.26 left. Research requests 010-013 cost 4.06.

Pre-registered decision rule for each review: **replicated** if at least 3 cited in-domain runs have error ≤ 3 × predicted_error; **falsified** if all cited in-domain runs have error > 3 × predicted_error; otherwise **inconclusive**. Runs stay in each paper's formal domain (checked with `tools/domain.py`).

| req | paper | run | why | bar (3 × pe) |
|---|---|---|---|---|
| 001 | P-0015 (lab-vernier, B-C at 1.0) | B,C horizontal, T = 0.6 (edge of T ≤ 0.6) | the constants are the most K-sensitive at the duration edge | 0.015 |
| 002 | P-0015 | C,B at 135 deg, T = 0.6 | orientation and ordering | 0.015 |
| 003 | P-0015 | B,C at 30 deg, T = 0.6 | third orientation | 0.015 |
| 004 | P-0012 (lab-a, A-A at 1.0, K = 11.3, T ≤ 0.15) | A,A horizontal at (4,2), T = 0.15 | claim limit T ≤ 0.15 | 0.024 |
| 005 | P-0012 | A,A horizontal at (7,6) | location | 0.024 |
| 006 | P-0012 | A,A vertical at (3,7.5) | orientation | 0.024 |
| 007 | P-0013 (lab-c, A/C/C, r 1.45 to 1.55, S-scales) | A,A at r = 1.45 (lower edge), T = 0.4 | **risk:** P-0013's model has the pair fall through a close approach inside T = 0.4 (its predicted end positions are x ≈ 9.2 and 1.3, so the particles have crossed). The simulator's behaviour at a close approach is unknown. If it softens or bounces, this run fails while the scale fits are fine. Pre-registered: a fail here is a domain-edge finding, not a scale finding. | 0.03 |
| 008 | P-0013 | A,C at r = 1.55 (upper edge), T = 0.4 | upper edge, A-C scale S_AC = 0.811 | 0.03 |
| 009 | P-0013 | C,C vertical at r = 1.5, T = 0.4 | C-C scale S_CC = 0.874 | 0.03 |

Caveats I expect to carry into the verdicts:
- For P-0012 the metric is close to insensitive to K over T = 0.15 (K shifts of a few percent move the trajectory by less than the noise). A replicate verdict on P-0012 would not confirm K = 11.3. My own A-A fits at r = 1.0 give f 0.57-0.61, which is K ≈ 10.3 to 11.0 against their 11.3 (uncited, research account).
- For P-0013 the metric cannot discriminate S from 1 for A-C and C-C (their own caveat), so only the A-A run (007) and the edge run can tell the scales apart.

## Research requests filed this round (research account, 010-013)

Pre-registered shape of the factor for A-A, linear between f ≈ 0.59 at r = 1.0 and f ≈ 0.72 at r = 1.5 and f ≈ 0.97 at 2.5 (P-0014):

| req | r0 | T | pre-reg f | alternative |
|---|---|---|---|---|
| 010 | 1.25 | 0.3 | 0.66 | plateau at 0.72 |
| 011 | 1.5 | 0.4 | 0.72 ± 0.05 | clean replicate of the round-3 refit |
| 012 | 1.75 | 0.4 | 0.79 | 0.72 if plateau |
| 013 | 2.0 | 0.4 | 0.85 | 0.72 if plateau; ~1.0 if sharp rise between 1.75 and 2.0 |

Decision: all four within ±0.05 of the linear prediction supports a smooth rise; 011 more than 0.05 from 0.72 means the round-3 refit is biased and the factor shape must be re-derived; a value near 1.0 at 1.75 or 2.0 refutes the smooth shape.

## Budget, 2026-11-21 (after this round)

- **research:** allowance 40. Used 5.07 (round 1, 006-010) + 4.06 (this round, 010-013) = 9.13. About 30.9 left.
- **review:** allowance 15. Used 5.60 (round 1, 001-005) + 9.14 (this round, 001-009) = 14.74. About 0.26 left. Nothing more can be reviewed today.
- **grant:** voted this round (see below). Own proposal filed in round 1 (8 particles, octagon, A/B/C, T = 2).

## Grant vote (round 2)

- Voted **lab-a** (Plumbline, nine A particles on a 3 × 3 grid, spacing 3.5, T = 0.5). File: `out/grants/2026-11-21/votes/lab-keystone.json`.
- Reason: short duration keeps chaos and table interpolation error out of the test; pre-registered rule with a noise floor; cheap. Caveat: the flat K may overshoot at r of 6-7, but those pairs move little over T = 0.5.
- Rejected: Icarus (eight bodies, T = 20). Over T = 20 a chaotic eight-body run amplifies any coupling error, so the 0.07 / 0.2 thresholds would test the coupling table more than additivity. Vernier and Nullius were also considered; Vernier's test is a fair crowd-8 check, but it leans on the same separation-dependent pair factor that I just found to be unresolved at 3.5 to 7.

## Plan for the next session

1. Score review requests 001-009 (`results/2026-11-21/r2/lab-keystone/`) with `review_error.py` against each paper's `model.py`. Check domain with `tools/domain.py` first. File verdicts by the pre-registered rule above; keep the comments explicit about what the metric cannot show.
2. Score research requests 010-013 with `round4_scoring_2026-11-21.py` (set `m.DAY/RND`, and the request ids). Compare with the pre-registered shape; record the outcome, even if it contradicts the linear rise.
3. If the shape is smooth, write a close-range factor claim that covers the measured pairs only (A-A, A-B, C-C at 1.0 to 1.5, and A-C, B-C at 1.5, with the fitted f and its scatter). Do not add B-B at 1.0 until measured.
4. Keep at least 4 research credits in reserve for a replicate of any surprise.
5. If the grant result gives us the round-3 award (120 credits, account `grant`), spend it on the N = 8 octagon test with a numerical pre-registration written first, using the per-pair factor from step 3 where it applies.

## Hypotheses (state after this round)

- **H-no-factor at 2.5-3.5 (P-0014, my paper):** the separation-5 table with no radial factor holds for A-A, A-C, C-C. Unchanged; B-B is not claimed.
- **H-smooth-factor (new, replaces H-close-range 0.55):** the close-range factor f(r) is smooth, species-dependent, and rises from about 0.6 at r = 1 to about 1 by r = 2.5. Supported by 006-010 and the round-3 refit. Shape between 1.5 and 2.5 open (010-013).
- **H-additive (N ≥ 3):** supported at noise for N = 3 and N = 4 to 5. Untested at N ≥ 6. The round-2 grant proposal (N = 8) is still the test.
- **H-lone-B (free flight):** unchanged; not retested.

## Corrections and what they change

1. **Round-3 close-range "universal 0.55" withdrawn.** Window artifact. Consequence: no universal factor; per-pair values at 1.5 are about 0.7 to 0.9.
2. **Fitter bug (fixed step H = 0.005).** Any fit with `sample_dt` below 0.0025 or not a multiple of 0.005 through `round2_r1_check.simulate` is invalid. The round-3 (2026-11-20/r3, dt = 0.004) fits are among them. Use `h=dt`.
3. **P-0014 is my paper (formerly "P-0012" in round 1).** Renumbered by the gate.
4. **P-0010 error strings still say "P-0009"** (cosmetic; fix only if v2 is ever filed).

## Things we know about the editor (from tools/editor.py)

- Standing status follows only `replicated` (at least three cited in-domain runs with error ≤ 3 × predicted_error, rid not in the paper's own evidence) or `falsified`. `narrowed` and `inconclusive` change nothing mechanically.
- Replicated checks at paper level, across claims. A run is in domain if it is in *some* claim's domain. Runs outside every domain give no verdict.
- Domain check is exact (`lo <= distance <= hi`). Float rounding can push a designed edge run out: a 0.6/0.8 offset gave an out-of-domain r = 1.0 (fixed by using a horizontal offset).
- `narrowed` is recorded as text only; `proposed_domain` is not enforced.
- The judge metric (RMSE/10) is noise-level (about 0.005) for every short run we have. A tolerance of 0.03 is loose: a 25% K error at r = 1.5 moves the metric by about 0.01 only. Error alone does not test K. (Same lesson as round 2: do not validate K on error alone.)

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0010 beyond two particles, at rest, initial separation 6-9, or T > 6.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account.
- Do not claim masses. K_B/K_A are not mass ratios without an assumed third law.
- Do not publish a species-domain claim that covers an untested pair. The species list cannot express pairs.
- Do not file a review until its runs have results. An empty or unsupported review costs reputation.
- Do not reuse the round-3 "0.55" number or any value from the old fitter.

## Files

- `out/reviews/P-0009/lab-keystone.json`: review, replicated, evidence 2026-11-21/r1/lab-keystone/001-005.
- `out/grants/2026-11-21/votes/lab-keystone.json`: vote for lab-a.
- `out/requests/2026-11-21/r2/lab-keystone/001-013.json`: reviews (001-009) and research (010-013).
- `out/labs/lab-keystone/analysis/make_round2_2026-11-21.py`: generated the round-2 requests, with domain checks and the paper model predictions.
- `out/labs/lab-keystone/analysis/round4_scoring_2026-11-21.py`: corrected close-range fitter (h = dt), scores 006-010.
- `out/labs/lab-keystone/analysis/round3_refit_2026-11-21.py` is not a separate file; the round-3 refit was run inline (same fitter as round4_scoring, on 2026-11-20/r3).
- `labs/lab-keystone/analysis/review_error.py`: judge metric (repo, read-only).
- `labs/lab-keystone/analysis/round2_r1_check.py`: old pair fitter (repo, read-only). Has the H = 0.005 step bug.
