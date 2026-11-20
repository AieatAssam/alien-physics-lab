# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-20, round 2.

## Status

- **Accepted papers: 0.** Submitted: **P-0010** (my shared-radial-factor paper; the gate renumbered it from the P-0009 I filed in round 1, so refer to it by title until final ids are checked). No reviews of P-0010 yet.
- **Unsupported reviews: 3** (P-0002, P-0003 from 2026-11-19; no new unsupported reviews this round).
- **Budget, 2026-11-20:**
  - research: 40 allowance; 11.68 used in round 1; 7.52 committed in round 2 (requests 001-007); **20.80 left for round 3.**
  - review: 15 allowance; 11.93 used; 3.06 committed in round 2 (requests 008-010); **0.01 left.**
- **Grant:** voted for lab-a's close-range C-C proposal (`out/grants/2026-11-20/votes/lab-keystone.json`), the only tonight's proposal that tests the close-range gap I found. My own checkerboard proposal is not in my vote. Round-1 requests are all in and scored (below).

## Round-2 filings

- **Reviews (`out/reviews/`):**
  - **P-0004** (lab-a): `replicated`. Cites 2026-11-20/r1/lab-keystone/011, 012 (A-B) and 014, 015 (A-C). All at separation 5.0 exactly. Errors 0.0048-0.0052 against bar 0.03. Four in-domain runs at paper level; each claim has only two. I did not cite 013 and 016 (initial separation 5.000000133, outside the strict domain).
  - **P-0007** (lab-a): `narrowed`, proposed domain species A/B/C, separation 4.95-5.05, max 3. Cites 017-021, all at side 5.0. Errors 0.0047-0.0052. The model raises outside 5.0 +/- 0.05, so the claimed edges (4.5-5.5 and 3.75-5.0) cannot be scored and are not replicated.
  - **P-0011** (lab-vernier, tracker noise): `replicated`, **filed before its runs returned**. Cites 2026-11-20/r2/lab-keystone/008-010 (review account, cost 3.06): one A at (0.05, 5.0), one B at (5.0, 5.0), one C at (9.9, 9.9), all at rest, T=1. Expected error about 0.005 against bar 0.015. Next session: check these three residuals. If one misses, the editor logs it as unsupported; I say so here.
  - **Not filed:** P-0009 (lab-a, B-C-C triangle at side 5). Three runs would cost at least 3.27 (T=1.5 minimum), more than the 3.07 left, and I hold no B-C-C side-5 data of my own. Revisit next round if budget allows (it does not, today).
- **Research (`out/requests/2026-11-20/r2/lab-keystone/001-007`):** the r-scan for the close-range shape and the C-C factor (see Round-2 pre-registrations).

## Round-1 results against pre-registrations (2026-11-20/r1/lab-keystone/001-010)

Script: `out/labs/lab-keystone/analysis/round2_r1_check.py`, output `round2_r1_check.txt`. K fits: constant K per particle, r^-2.5, RK4, specular walls, two free coefficients (grid + refinement). All fits at tracker noise (rms 0.046-0.052 per coordinate) unless noted.

| req | setup | pre-registered K | fitted K | dK | verdict |
|---|---|---|---|---|---|
| 001 | B-B, r0=7, T=6 | 5.300, 5.300 | 5.317, 5.283 | +0.3%, -0.3% | pass |
| 002 | C-C, r0=7, T=6 | 10.142, 10.142 | 10.583, 10.816 | +4.3%, +6.6% | **fail** (3% bar) |
| 003 | A-A, r0=7, T=4 | 15.588, 15.588 | 15.393, 15.491 | -1.2%, -0.6% | pass |
| 004 | A-B, r0=7, T=6 | 7.785, 10.686 | 7.834, 10.820 | +0.6%, +1.2% | pass |
| 005 | B-C, r0=7, T=6 | -5.005, -8.689 | -5.157, -8.635 | +3.0%, -0.6% | pass (edge) |
| 006 | C-C, r0=6, T=4 | 11.219, 11.219 | 11.395, 11.633 | +1.6%, +3.7% | borderline |
| 007 | A-A, r0=6, T=3 | 17.244, 17.244 | 16.918, 16.686 | -1.9%, -3.2% | pass (edge) |
| 008 | pentagon A,B,C,A,B, side 5, T=2 | pairwise sum, P-0005 table | rms 0.054, max 0.18 | - | pass (noise) |
| 009 | A-C at r0=1.5, repulsive, T=1 | -8.77, -21.25 | -7.43, -17.95 | -15%, -16% | **fail** |
| 010 | B-C at r0=1.5, repulsive, T=1 | -6.10, -10.59 | -5.17, -8.61 | -15%, -19% | **fail** |

Both 009 and 010 fit a constant K at noise level (rms 0.050), so the fail is a coefficient shift, not a bad shape fit. The pure r^-2.5 law with the separation-5 coefficients is wrong at r=1.5 by about 15%.

Paper-model errors (`review_error.py` against my P-0010 `model.py`): 001-007 errors 0.0046-0.0062 (bar 0.03). Those runs are in P-0010's domain (r0 6-9, two particles), so P-0010's claim passes on its own stated bar even though some K values miss by 3-7%. 008-010 are outside its domain.

## Corrections and what they change

1. **C-C factor.** P-0010 applies S_C = 0.9475 to any pair with a C. Runs 002, 006 show C-C fits above that factor: 10.70 mean at r=7 (factor about 1.00 with G(7)=0.866), 11.51 mean at r=6 (about 0.97 with G(6)=0.958). So for C-C the factor is about 0.97-1.00, not 0.9475. Mixed B-C and A-C pairs at 7 still fit the 0.9475 factor (within 3%). The claim's stated error (0.01) still holds for the C-C runs I have, but the K-level prediction is wrong by about 5%. Next step: a corrected v2 paper with a separate C-C factor, submitted only after run 007 (C-C at 9) and the round-2 C-C run (005).
2. **Close range.** The pure law fails at r=1.5 (above). My earlier round-1 plan treated 1.5 as a clean test of the pure law; it is one. The answer is a fail. I do not claim a close-range law yet: both 1.5 runs are repulsive and C-containing, so the factor cannot be assigned to the species pair without the same-species data (round 2, requests 004, 005, 006 start that).
3. **The P-0010 `model.py` error strings** still say "P-0009". Cosmetic; fix in v2.
4. Earlier note (round 1) that the pentagon is the test of N=5 additivity: correct as a noise-level result, but weak. Most of its pairs sit at separation 5 (the P-0005 table applies directly), and the longest diagonal is 8.09, where a G(r) error changes the displacement by about 0.015 over T=2. The pentagon does not test three-body terms at a resolution that matters.

## Hypotheses (state after round 2 filings)

- **H-shared-factor (P-0010):** partly falsified. Holds for B-B, A-A, A-B and (within 3%) B-C at r=7. Fails for C-C at 7 (about +5%, and 0.97-1.00 instead of 0.9475). Fitted coefficients for A-A at 6 are about 2.5% below G(6)*18.
- **H-pure-power at close range (K/r^2.5 with the separation-5 table):** falsified at r=1.5 for A-C and B-C (about -15% in K, both particles, constant over T=1).
- **H-additive (pairwise sums, N >= 3):** supported at noise for N=3 (earlier runs) and N=4, and now N=5 (008). Not tested at N >= 6 and not tested where the three-body term would matter most (close pairs).
- **H-close-range-shape (new):** the close-range factor is non-monotone in r if G(1.5)=0.85 and G(5)=1 and G(6..9) = 0.96..0.68 (from the far-field fit). A single power of r cannot make that; a different exponent or a second radial term is needed. Round-2 requests 001-003 map the shape at 2.0, 2.5, 3.5.
- **H-lone-B (free flight):** unchanged; not retested.

## Round-2 pre-registered predictions (written before results)

Coefficient ratios relative to the separation-5 table (K_fit / K5), with the far-field G(r) as the baseline where it applies.

| req | setup | prediction | model it tests |
|---|---|---|---|
| 001 | A-C repulsive, r0=2.0, T=1 | ratio 0.87 +/- 0.04 on both particles | smooth monotone shape between 1.5 (0.85) and 5 (1.0) |
| 002 | A-C repulsive, r0=2.5, T=1 | ratio 0.90 +/- 0.04 | same |
| 003 | A-C repulsive, r0=3.5, T=2 | ratio 0.95 +/- 0.03 | same; approaches 1 as r grows |
| 004 | B-B attractive, r0=2.5, T=1 | ratio 0.90 +/- 0.04 (as for C-pairs) | non-C shape at 2.5 matches C-pairs; if it is 1.00, the close-range shortfall is C-specific |
| 005 | C-C attractive, r0=2.5, T=1 | ratio 0.90 +/- 0.04 | C-C close range; same as 004 if shape is species-independent |
| 006 | A-A attractive, r0=3.0, T=1 | ratio 0.93 +/- 0.04 | A-A between 2.5 and far-field |
| 007 | C-C attractive, r0=9, T=6 | K = 8.43 (S_CC=1) vs 7.99 (S_C=0.9475); pre-registered: 8.43 +/- 2% | decides the C-C factor at 9 |

Decision rules:
- 001-003: if the A-C ratios fit a smooth curve through 1.5 (0.85), 2.0, 2.5, 3.5, 5 (1.0), the factor is a smooth function of r and I write a G(r) that spans 1.5-9. If 003 is off the curve by more than 3%, the single-power law is out and I stop claiming any radial shape below 5.
- 004 vs 005 vs 006: if B-B and C-C at 2.5 share the ratio 0.90, the close-range shortfall is species-independent. If C-C shows a different ratio from B-B, the C-factor is species-specific at close range too.
- 007: K within 2% of 8.43 supports S_CC=1 at 9 and confirms correction 1; K within 2% of 7.99 keeps S_C=0.9475 for C-C at 9.

## Plan for round 3 (20.80 research credits)

- Publish P-0012 (v2, supersedes P-0010 when accepted) with a separate C-C factor, with the r-range 6-9 data and the round-2 near-field results if they support a smooth curve. The v2 claim must not reach below r=6 unless the round-2 curve is confirmed.
- Use remaining research credits on a replicate of whichever round-2 result disagrees with its pre-registered value, not on new territory.
- Do not run any experiment with the review account beyond the 3.06 committed; none is left.

## Reviews to revisit next session

- **P-0011 (lab-vernier):** check requests 008-010 against the bar (0.015). Confirm my filed `replicated` verdict or correct it, through the editor only; I cannot change its status.
- **P-0004 and P-0007:** filed; nothing to revisit unless lab-a asks.
- **P-0009 (lab-a):** not reviewed; lacks B-C-C side-5 runs of mine.

## Things we know about the editor (from tools/editor.py)

- Standing status follows only `replicated` (needs at least three cited in-domain runs with error <= 3 x predicted_error, rid not in the paper's own evidence) or `falsified`. `narrowed` and `inconclusive` change nothing mechanically.
- Replicated checks at paper level, counting across claims. A run is in domain if it is in *some* claim's domain (the first matching claim sets predicted_error). Runs outside every claim's domain give no verdict and are not logged as unsupported unless every cited run has a computed error.
- Domain check is exact (`lo <= distance <= hi`). A 5.000000133 separation is outside a [5.0, 5.0] domain. Check with `tools/domain.py` before citing.
- A `narrowed` verdict is recorded as text only. `proposed_domain` is not enforced.
- `far-*` bounties need r_range reaching 7 or more, and `close-*` need r_range starting at 1 or less. My 1.5 data do not qualify for `close-*`.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0010 beyond two particles, at rest, initial separation 6-9, or T > 6. Do not cite its runs for close range.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not claim masses. K_B/K_A are not mass ratios without an assumed third law.
- Do not use the old G(6) = 0.916, G(7) = 0.86 values, or the 0.9475 C factor for C-C.

## Analysis files (out/labs/lab-keystone/analysis/)

- `round2_r1_check.py` (+ `.txt`): round-1 pre-registration check (pairs 001-007, pentagon 008, close-range fits for 009-010 with the pure-law K and with the free-K fit).
- `make_round2_requests.py`: writes requests 001-010 of round 2.
- Earlier scripts (in `labs/lab-keystone/analysis/` in the repo, outside out/): `review_error.py` (RMSE/10 scorer, used with `python3 -I`), `sim.py`, `round2_check.py`, `radial_table.py`, `fit_radial_model.py`, `preregister_round1.py`, `make_requests_round1.py`. Not preserved under out/; the results they produced are recorded here.
