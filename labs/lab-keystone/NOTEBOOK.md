# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-20, round 3.

## Status

- **Accepted papers: 0.** Submitted: **P-0010** (shared-radial-factor paper, v1; gate renumbered my round-1 P-0009, so check final ids). Unsupported reviews: 3, unchanged this round.
- **Papers held in draft (not submitted):** P-0012 draft at `out/labs/lab-keystone/drafts/P-0012-draft/` (narrow claim: separation 2.5 to 3.5 needs no radial factor). Held because A-B and B-C at 2.5 to 3.5 are not yet tested; the claim's species domain would cover them. See round-3 filings.
- **Reviews I filed:**
  - **P-0011** (lab-vernier, tracker noise), `replicated`, cites 2026-11-20/r2/lab-keystone/008-010. **Checked this round: stands.** Errors 0.00484, 0.00504, 0.00503 against bar 0.015 (all three pass). Script: `out/labs/lab-keystone/analysis/round3_check.py`.
  - **P-0004** (lab-a), `replicated`, and **P-0007** (lab-a), `narrowed`: filed in round 2. Not revisited; nothing changed.
- **Papers awaiting my review:** **P-0009** (lab-a, B-C-C triangle at side 5). **Not reviewed this round.** Reasons: (1) I hold zero in-domain runs of B-C-C at side 5 (domain: species B, C; sides 4.99 to 5.01; max 3 particles); (2) the review account has 0.01 credits left, so I cannot run any review-account experiment; (3) I will not cite research-account runs as review evidence, because the round instructions say review runs go on the review account. Next session (review budget refreshes): file three B-C-C side-5 runs on the review account with `cites_paper: P-0009`, T = 2 (each about 1.12 credits, about 3.4 total). Bar is 3 x 0.01 = 0.03. A review with no in-domain cites is not allowed (evidence must not be empty).
- **Budget, 2026-11-20:**
  - research: 40 allowance; 19.20 used in rounds 1-2; 20.80 left at start of round 3; **round-3 filings cost about 6.14** (001-006, see below). About 14.7 credits left after this round.
  - review: 15 allowance; 14.99 used; **0.01 left.**
- **Grant:** voted for lab-a's close-range C-C proposal (`out/grants/2026-11-20/votes/lab-keystone.json`). Plumbline won; nothing for me to use.

## Round-2 results, scored against their pre-registrations

Script: `out/labs/lab-keystone/analysis/round3_check.py` (+ `round3_check.txt`). Constant K per particle, r^-2.5 law, RK4, specular walls; two free coefficients (grid + refinement), via `round2_r1_check.pair_run` in the repo analysis dir. Ratios are fitted K divided by the separation-5 table (P-0005 values, A-A 18.0, A-B 8.99/12.34, A-C -8.77/-21.25, B-B 6.12, C-C 12.36, B-C -6.10/-10.59).

| req | pair | r0 | T | pre-reg ratio | fitted ratio (p0, p1) | verdict |
|---|---|---|---|---|---|---|
| 001 | A-C repulsive | 2.0 | 1 | 0.87 | 0.93, 0.92 | **miss** (+6 to +7%) |
| 002 | A-C repulsive | 2.5 | 1 | 0.90 | 0.97, 0.98 | **miss** (+7 to +9%) |
| 003 | A-C repulsive | 3.5 | 2 | 0.95 | 1.03, 1.02 | **miss** (+7 to +9%) |
| 004 | B-B attractive | 2.5 | 1 | 0.90 | 0.97, 0.98 | **miss** (+8%) |
| 005 | C-C attractive | 2.5 | 1 | 0.90 | 1.02, 1.02 | **miss** (+13%) |
| 006 | A-A attractive | 3.0 | 1 | 0.93 | 0.96, 0.98 | **miss** (+3 to +6%) |
| 007 | C-C attractive | 9.0 | 6 | S_CC=1: 8.43 (ratio 0.68); S_C=0.9475: 7.99 | K = 8.03, 8.11 (-5% vs 8.43; +0.5 to +1.5% vs 7.99) | **supports S_C=0.9475 at r=9** |

Read-out:
- **The 10% close-range shortfall I predicted at 2.5 is not there.** B-B, C-C and A-A at 2.5 to 3.0 all sit at 0.96 to 1.02. The round-1 shortfall at 1.5 (about -15%, repulsive A-C and B-C) is still real, but the curve is steeper than my pre-registration: A-C is 0.85 at 1.5, 0.93 at 2.0, 0.97 at 2.5, 1.03 at 3.5.
- **The species-independence rule (004 vs 005 vs 006) would have been decisive** only if the shortfall had appeared; it did not appear at 2.5 for any species pair, so the rule is inconclusive.
- **007 settles the C-C factor at r=9 in favour of the existing 0.9475.** This reverses my round-2 suggestion (correction 1) that C-C needed its own factor near 1.00. The C-C fits at r=6 and 7 were 0.97 and 1.00, but at 9 the factor is 0.9475 within 1.5%. Given fit scatter of about 2% per particle, no separate C-C factor is supported. **No v2 paper with a separate C-C factor.** P-0010 stays as it is.
- The fits at 2.0-3.5 are at noise level (rms 0.050 to 0.051 per coordinate), so the misses are coefficient shifts, not bad shape fits.

## Paper-model error at 2.5 to 3.5 (K5 table, no factor)

Runs 002-006 scored against the separation-5 table with no radial factor (`round3_check.py` and the `table_run` helper): errors 0.0087 (002, A-C 2.5), 0.0050 (003, A-C 3.5, T=2), 0.0064 (004, B-B 2.5), 0.0126 (005, C-C 2.5), 0.0093 (006, A-A 3.0). The C-C run is sensitive: a 2% change in K moves its error between about 0.005 and 0.013, because the pair collapses within T=1.

This is why the P-0012 draft uses predicted_error 0.013 and holds the claim to the tested pairs.

## P-0012 draft (held, not submitted)

- Claim: two particles at rest, initial separation 2.5 to 3.5, pure r^-2.5 with the P-0005 table (no radial factor), error at most 0.013 (RMSE/10). Evidence: round-2 runs 002-006.
- **Problem found this session:** the draft's species domain is `[A, B, C]`, so any pair from those species is in-domain, but only A-A, B-B, C-C and A-C are tested in 2.5-3.5. The draft's statement "any pair of species in A, B, C" overreaches.
- **Plan:** publish P-0012 next session once requests 005 (A-B, 3.0, T=0.8) and 006 (B-C, 3.0, T=1) return and fit within 4% of the table. Cite 005 and 006 as added evidence. If either misses by more than 4%, narrow the species domain (drop the missing pair from the statement and species list) rather than publish the overreach.
- Model smoke test: `predict` runs on a real round-2 setup (001-002 style). Imports only math.

## Round-3 filings (`out/requests/2026-11-20/r3/lab-keystone/001-006`, research account, cost about 6.14)

Close-range attractive pairs at r=1.5, at rest, T=0.4 (001-004), then the two missing pairs at 3.0 (005-006). All use the tracker only. The four close-range runs test the **sign/species structure** that the round-1 shortfall could come from. Round 1 found the shortfall only for repulsive pairs with C (A-C, B-C at 1.5). Four attractive pairs at 1.5 separate the hypotheses:

| hypothesis | A-A (18.0) | B-B (6.12) | C-C (12.36) | A-B (8.99 / 12.34) |
|---|---|---|---|---|
| **universal shortfall** G(1.5)=0.85 for all pairs | 15.3 (0.85) | 5.20 (0.85) | 10.51 (0.85) | 7.64 / 10.49 (0.85) |
| sign-dependent (only repulsive pairs short) | 18.0 | 6.12 | 12.36 | 8.99 / 12.34 |
| unlike-species only | 18.0 | 6.12 | 12.36 | 7.64 / 10.49 |
| C-only | 18.0 | 6.12 | 10.51 | 8.99 / 12.34 |

Decision rules (written before results): fitted ratio below 0.925 supports the shortfall for that pair. Universal predicts all four short; sign predicts none short; unlike predicts only A-B short; C-only predicts only C-C short.

Also: 005 A-B at r=3.0, T=0.8 and 006 B-C at r=3.0, T=1, both repulsive or attractive as the table gives (A-B attractive, B-C repulsive), with the separation-5 table and no factor, each K within 4% (rule). These close the A-B and B-C gaps for the P-0012 claim.

Remaining research budget after these filings: about 14.7 credits. Next round: depends on 001-004.

## Hypotheses (state after round 3 filings)

- **H-shared-factor (P-0010, v1):** holds in its domain (two particles, r 6-9). Errors 0.0046-0.0062 against bar 0.03 in round 2. Its K-level claim is about 3-7% off for some pairs (C-C at 6-7), but the paper's stated bar is loose enough to pass. **Not changed.**
- **H-no-factor at 2.5-3.5 (new):** the separation-5 table with no radial factor holds within 4% for A-A, B-B, C-C, A-C (five runs). A-B and B-C are untested in this range. Basis for the P-0012 draft.
- **H-close-range-shape (revised):** the factor rises from about 0.85 at r=1.5 to about 0.93 at 2.0 and about 0.97 at 2.5 (A-C) and is 0.96-1.02 for B-B, C-C, A-A at 2.5-3.0. The shortfall is confined to r below about 2.5 and may depend on species or sign. Round-3 requests 001-004 decide between universal, sign, unlike-species and C-only.
- **H-additive (pairwise sums, N >= 3):** supported at noise for N=3 (earlier runs) and N=4, N=5 (pentagon 008 in round 1). Not tested at N >= 6, nor at close range where a three-body term would matter most.
- **H-lone-B (free flight):** unchanged; not retested.
- **H-C-factor-9 (settled this round):** C-C at r=9 is 0.9475 within about 1.5%; the separate-C-C-factor idea is dropped.

## Corrections and what they change

1. **C-C factor (round 2 correction 1 withdrawn).** I had argued for a separate C-C factor near 1.00 at r=6-7. Run 007 (C-C at 9, T=6) gives 0.9475 within 1.5%, so the shared factor is adequate there. The round-2 pre-registered 10% shortfall at 2.5 also failed. Both corrections come from this round's data.
2. **P-0010 error strings still say "P-0009"** (cosmetic; fix only if v2 is ever filed).
3. **Round-1 note that the pentagon tests N=5 additivity:** still weak, as before (most pairs at separation 5, long diagonal 8.09, where G(r) errors are about 0.015 over T=2).

## Plan for the next session

1. Read round-3 results 001-006 (`results/2026-11-20/r3/lab-keystone/`). Score 001-004 against the table in this notebook with `round3_check.py` (extend it to a 1.5 block, using `m.RND='r3'` and the pre-registered K's above). Score 005-006 against the separation-5 table (ratio rule, 4%).
2. If 005 and 006 are within 4%, publish P-0012 with those ids added as evidence (`out/papers/P-0012/`), and drop the draft from `drafts/`. If not, narrow the species domain as described above.
3. If the close-range result is universal (all four short), write a G(r) claim covering 1.5 to 3.5 for all pairs, with predicted_error about 0.015 and the r_range from 1.5. That would also be the first claim that could bear on the close-* bounties (r_range starting at 1 or less needs a run at 1.0 or below; not yet). If it is sign-dependent or species-dependent, write one claim per structure, not a universal one.
4. Review P-0009 (lab-a) on the review account once it refreshes (see Status). Do not use research credits for review evidence.
5. Use remaining research credits (about 14.7) only on discriminating experiments, not on new territory, and keep at least about 4 credits for any replicate of an unexpected result.

## Things we know about the editor (from tools/editor.py, as recorded in round 2)

- Standing status follows only `replicated` (at least three cited in-domain runs with error <= 3 x predicted_error, rid not in the paper's own evidence) or `falsified`. `narrowed` and `inconclusive` change nothing mechanically.
- Replicated checks at paper level, across claims. A run is in domain if it is in *some* claim's domain. Runs outside every domain give no verdict.
- Domain check is exact (`lo <= distance <= hi`). Check with `tools/domain.py` before citing.
- `narrowed` is recorded as text only; `proposed_domain` is not enforced.
- `far-*` bounties need r_range reaching 7 or more; `close-*` need r_range starting at 1 or less. My 1.5 data do not qualify for `close-*` (the domain would start at 1.5).

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0010 beyond two particles, at rest, initial separation 6-9, or T > 6. Do not cite its runs for close range.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account.
- Do not claim masses. K_B/K_A are not mass ratios without an assumed third law.
- Do not use the 0.9475 factor for C-C at close range, or the old G(6)=0.916 and G(7)=0.86 values.
- Do not publish a species-domain claim that covers an untested pair (the P-0012 draft mistake).

## Analysis files (out/labs/lab-keystone/analysis/)

- `round3_check.py` (+ `round3_check.txt`): scores round-2 requests 001-007 against their pre-registered K's and the P-0011 review runs 008-010. Imports `round2_r1_check.py` from the repo analysis dir with `python3 -B -I` (no bytecode written outside out/).
- `round2_r1_check.py` (repo, read-only import): pair fit (`pair_run`), pentagon/close-range table scorer (`table_run`), RK4 simulator.
- Repo analysis dir (`labs/lab-keystone/analysis/`, not under out/): `review_error.py`, `sim.py`, `round2_check.py`, `radial_table.py`, `fit_radial_model.py`, `make_round2_requests.py`, `round3_fit.py`, and others. Their outputs are summarised here, not preserved under out/.
- `drafts/P-0012-draft/` (under `out/labs/lab-keystone/drafts/`): held claim, paper and model.
