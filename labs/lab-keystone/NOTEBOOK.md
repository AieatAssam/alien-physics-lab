# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-21, round 1.

## Status

- **Accepted papers: 1 (P-0010 was submitted in round 2; the scoreboard lists 1 accepted).** Submitted this round: **P-0012** (narrowed, species A and C only, separation 2.5 to 3.5; `out/papers/P-0012/`). The gate may renumber it; check final ids.
- **Unsupported reviews: 3** (unchanged). Standing reviews: P-0011 (replicated, stands), P-0004 (replicated), P-0007 (narrowed).
- **Bounties in play:** close-* (need r_range starting at 1 or less; my data start at 1.5, so runs 006-008 below are the first attempt at 1.0); crowd-8 (grant proposal below targets it).

## Budget, 2026-11-21

- **research:** allowance 40; filed this round: requests 006-010, cost about 5.06. About 35 left.
- **review:** allowance 15; filed this round: requests 001-005 (cites P-0009), cost 5.60. About 9.4 left.
- **grant:** proposal filed (`out/grants/2026-11-21/proposals/lab-keystone.json`). Round 2 voting still to come.

## Round 3 (2026-11-20) results, scored

Scripts: `out/labs/lab-keystone/analysis/round3_scoring_2026-11-21.py` (close-range 001-004, repo fitter `round2_r1_check.pair_run`), and the K5-table checks for 005-006 run inline with `table_run` and `pair_run`.

### Close-range pairs at r0 = 1.5, T = 0.4 (requests 001-004, research)

| req | pair | pre-reg ratio (universal 0.85) | fitted K (p0, p1) | fitted ratio | fit rms | verdict |
|---|---|---|---|---|---|---|
| 001 | A-A attractive | 0.85 | 10.61, 10.44 | 0.59, 0.57 | 0.077 | short (rms above noise) |
| 002 | B-B attractive | 0.85 | 3.51, 3.30 | 0.57, 0.54 | 0.051 | short |
| 003 | C-C attractive | 0.85 | 6.78, 6.88 | 0.55, 0.56 | 0.051 | short |
| 004 | A-B attractive | 0.85 | 4.85, 6.67 | 0.54, 0.54 | 0.051 | short |

- **Read-out:** every pair is short, by about 45%, not 15%. The shortfall is the same across species and across like and unlike pairs, so the **sign-dependent** and **C-only** hypotheses are dead (all four short, including attractive pairs with no C). The **universal** hypothesis survives qualitatively, but the factor is about 0.55, not 0.85. My pre-registered number was wrong.
- **Caveat that matters:** this contradicts my round-1/2 value of A-C at 1.5 being about 0.85. Either the constant-K r^-2.5 fit is inadequate at close range (the pair closes to about 0.9 within T = 0.4, so one constant K averages over a changing factor), or the earlier and current protocols differ. Requests 009-010 test this directly (A-C and B-C at 1.5 under the round-3 protocol).
- Do not publish a close-range factor yet. Constant K is not a good model at r = 1.5, and the species-pair list would have to cover pairs we have not measured at 1.5 under one protocol.

### Pairs at 3.0 (requests 005-006, research, K5 table, no factor)

| req | pair | T | error (judge metric) | fitted ratio (p0, p1) | verdict |
|---|---|---|---|---|---|
| 005 | A-B attractive | 0.8 | 0.0066 (rms 0.049, noise) | 0.68, 0.64 | fails 4% rule; K barely constrained by a T = 0.8 run |
| 006 | B-C repulsive | 1.0 | 0.0051 (rms 0.050, noise) | 1.06, 0.94 | misses 4% rule by 5.6% |

- The judge metric (error) is at noise level for both runs, but the K-ratio fit disagrees strongly for A-B. Error alone does not constrain K for short runs. Lesson: a claim should not rest on error alone when the notebook rule is about K.

### Round-2 runs 002-006 (2.5 to 3.5) and 007 (C-C at 9), unchanged from the prior notebook

- Ratios A-C 2.5 (0.97), A-C 3.5 (1.03), B-B 2.5 (0.98), C-C 2.5 (1.02), A-A 3.0 (0.96-0.98); all within 4% of 1.0.
- 007 (C-C at 9, T = 6): K = 8.03/8.11, so the shared factor 0.9475 stands at r = 9. No separate C-C factor.

## P-0012 (submitted this round, narrowed)

- **Claim:** two particles at rest, species A or C (pairs A-A, A-C, C-C), separation 2.5 to 3.5, T up to 2: the separation-5 P-0005 table with no radial factor, error at most 0.013.
- **Evidence:** 2026-11-20/r2/lab-keystone/002, 003, 005, 006 (all in domain).
- **Why narrowed:** the draft covered A, B and C. The A-B and B-C runs at 3.0 (005, 006 in round 3) fail the 4% K-ratio rule, and the species list cannot exclude B-B without also admitting A-B and B-C. The B-B run 004 (ratio 0.98) is therefore cited nowhere.
- **Re-scored with the judge metric** (`review_error.py` against `out/papers/P-0012/model.py`): errors 0.00504 (002), 0.00504 (003), 0.00517 (005), 0.00505 (006). The notebook's earlier 0.0126 for C-C came from `table_run`, a different scorer, so the 0.013 bound is conservative.
- **Limits:** two particles only, T up to 2, separations 2.5 to 3.5, A and C species only. Nothing for B pairs.

## Requests filed this round (`out/requests/2026-11-21/r1/lab-keystone/`)

Review account, cites P-0009 (paper by lab-a, B, C, C triangle at side 5):

| req | triangle | why | est. cost |
|---|---|---|---|
| 001 | B,C,C side 5, rotated 30 deg | orientation replicate | 1.12 |
| 002 | B,C,C side 4.99 | lower edge of paper's r_range | 1.12 |
| 003 | B,C,C side 5.0095 | upper edge (5.01 rounds outside the model's check) | 1.12 |
| 004 | C,C,C side 5 | paper's species list [B,C] includes C-only | 1.12 |
| 005 | B,B,B side 5 | paper's species list includes B-only | 1.12 |

Research account (close-range shape and the round-3 disagreement):

| req | pair | r0 | T | pre-reg (plateau 0.55 / power law G ~ r^1.83) |
|---|---|---|---|---|
| 006 | A-A | 1.0 | 0.2 | ratio 0.55 vs 0.25; decision: below 0.4 favours steepening |
| 007 | C-C | 1.0 | 0.2 | same |
| 008 | A-B | 1.0 | 0.2 | same |
| 009 | A-C repulsive | 1.5 | 0.4 | 0.85 (round 1-2) vs 0.55 (round 3); within 0.1 decides |
| 010 | B-C repulsive | 1.5 | 0.4 | same as 009 |

## Grant proposal (round 1, tonight)

- **Title:** Eight-particle pairwise additivity: octagon of A, B, C at rest (crowd-8 test).
- **Setup:** 8 particles, species cycling A, B, C, A, B, C, A, B, at rest on a circle of radius 4 centred at (5,5). Adjacent spacing 3.06; all pair separations 3.06 to 8.0. T = 2, sample_dt 0.02. Cost 1.32 per run.
- **Why:** N = 8 is untested (we have N <= 5). Pure pairwise sum with no three-body term, residual at tracker noise, would support H-additive at N = 8 and also give a candidate for the crowd-8 bounty (max_particles 8). A residual growing with N would refute it.
- **Caveat for the pre-registration:** the pair law at separations other than 5 is not settled (see the close-range section). A pairwise prediction at 3.06 to 8 must use the separation-appropriate factor (r = 3-3.5 with the no-factor table; r = 6-9 with the P-0010 factor). I have not pre-registered a numerical prediction yet; do that before any round-3 run.
- Grant pitch length 533 characters (limit 600), title under 120.

## P-0009 review (lab-a, B-C-C triangle, side 5)

- **Pending results.** Review cannot be written until requests 001-005 return (next session). Bar: 3 x 0.01 = 0.03.
- **Plan when results arrive:** score each run with `review_error.py` against `papers/P-0009/model.py`, check domain with `tools/domain.py`, and cite only in-domain runs. If 001-003 (B,C,C, incl. the two edges) are at or below 0.03, file `replicated` citing them and the others only if in domain and at or below 0.03. If 004 (C,C,C) or 005 (B,B,B) fails while 001-003 pass, the claim's species-level domain overreaches; file `narrowed` with `proposed_domain` species [B, C] and an explicit comment, citing only the passing runs.
- **Why I am not reviewing now:** the review account has no results yet, and a review with no in-domain results must not be filed.

## Hypotheses (state after this round)

- **H-shared-factor (P-0010 v1):** holds in its domain (two particles, r 6-9). Unchanged.
- **H-no-factor at 2.5-3.5 (P-0012, narrowed):** the separation-5 table with no radial factor holds for A-A, A-C, C-C. B-B is also within 4% (run 004), but is not claimed. A-B and B-C are not supported (K-ratio failure at 3.0).
- **H-close-range (revised):** the factor drops to about 0.55 at r = 1.5 for attractive pairs of all species (A-A, B-B, C-C, A-B), not about 0.85. Whether it is a constant factor or a shape is open; the constant-K fit may be the wrong model at close range. 006-010 test this.
- **H-additive (N >= 3):** supported at noise for N = 3 and N = 4, 5. Untested at N >= 6. The grant proposal tests N = 8.
- **H-lone-B (free flight):** unchanged; not retested.

## Corrections and what they change

1. **Round-3 pre-registration (0.85) was wrong; measured 0.55.** The sign and species structure is now resolved (universal, not sign-dependent), but the magnitude changes the close-range story. Claim-level consequence: no close-range claim this round.
2. **A-B at 3.0 (round 3 005).** The K-ratio fit (0.64-0.68) disagrees with the judge's error metric (noise level). Consequence: P-0012 excludes A-B; I will not rely on the error metric alone to validate K.
3. **P-0010 error strings still say "P-0009"** (cosmetic; fix only if v2 is ever filed).

## Plan for the next session

1. Score research 006-010 (`results/2026-11-21/r1/lab-keystone/`). Use the pre-registration table above. If 006-008 come back near 0.55, the factor is flat down to 1.0 and close-* bounties (r_range starting at 1) become reachable with a universal factor claim. If near 0.25, the law steepens and I write a shape claim only after a third r value.
2. Use 009-010 to decide between round 1-2 (0.85) and round 3 (0.55) for A-C and B-C at 1.5.
3. Score review-account runs 001-005 against P-0009 and file the review (see plan above). This uses the review account only.
4. Once the grant result comes out (round 2 votes), use any grant credits in round 3 on the N = 8 run, after writing the numerical pre-registration.
5. Keep at least about 4 research credits for any replicate of an unexpected result.

## Things we know about the editor (from tools/editor.py, as recorded in round 2)

- Standing status follows only `replicated` (at least three cited in-domain runs with error <= 3 x predicted_error, rid not in the paper's own evidence) or `falsified`. `narrowed` and `inconclusive` change nothing mechanically.
- Replicated checks at paper level, across claims. A run is in domain if it is in *some* claim's domain. Runs outside every domain give no verdict.
- Domain check is exact (`lo <= distance <= hi`). Check with `tools/domain.py` before citing. Float rounding can push a designed edge run out (5.01 failed; 5.0095 is safe).
- `narrowed` is recorded as text only; `proposed_domain` is not enforced.
- `far-*` bounties need r_range reaching 7 or more; `close-*` need r_range starting at 1 or less.
- The judge metric (RMSE/10) is noise-level (about 0.005) for every short run we have. A claim's predicted_error of 0.013 is conservative.

## Things not to do

- Do not try to locate simulator source or hidden parameters.
- Do not extend P-0010 beyond two particles, at rest, initial separation 6-9, or T > 6. Do not cite its runs for close range.
- Do not cite another lab's run ids, out-of-domain runs, or file `replicated` with fewer than three in-domain runs.
- Do not use research-account runs as review evidence; review runs go on the review account.
- Do not claim masses. K_B/K_A are not mass ratios without an assumed third law.
- Do not use the 0.9475 factor for C-C at close range, or the old G(6)=0.916 and G(7)=0.86 values.
- Do not publish a species-domain claim that covers an untested pair. The species list cannot express pairs, so a claim on species [A, B, C] covers every pair. (This was the P-0012 draft's mistake; the submitted P-0012 uses species [A, C] to avoid it.)
- Do not file a review until its runs have results; an empty or unsupported review costs reputation.

## Analysis files

- `out/labs/lab-keystone/analysis/make_review_p0009_2026-11-21.py`: review-account requests 001-005 for P-0009, with pre-registered predictions from the paper's model.
- `out/labs/lab-keystone/analysis/round3_scoring_2026-11-21.py`: round-3 close-range fits (001-004).
- `out/papers/P-0012/`: narrowed paper, claim, and model (imports only math; `predict` checked against the judge metric on four runs).
- Earlier scripts: `labs/lab-keystone/analysis/` (repo, read-only): `round2_r1_check.py` (pair_run, table_run), `review_error.py` (judge metric), `round3_check.py`.
