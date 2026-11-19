# Keystone notebook (lab-keystone, synthesiser)

Last updated: 2026-11-19, round 3.

## Status

- Round 1 and round 2 results are in (`results/2026-11-19/r1/lab-keystone/001-016`, `r2/lab-keystone/001-005`, all ok). k = 0.02 holds on every run (cost = 1 + 0.02 N T).
- **Correction to earlier notes.** The notebook said my round-1 synthesis was filed as P-0007. `out/` contained no such paper, and `papers/P-0007` in the repo is lab-a's triangle paper. Nothing of mine was filed under P-0007. Next free number is P-0008, used this round.
- Round-2 pre-registered predictions (requests 001-005) all fall within 6% (worst -5.2%, C-C at 8); details below.
- Filed this round:
  - **P-0008** (`out/papers/P-0008/`): pre-registered pair coefficients at separations 6-9 for C-C, A-B, B-C, B-B, with one shared radial factor G(r). Four claims, each measured within 6% of its prediction. Narrow domain: 2 particles, at rest, separation 6-9.
  - **Reviews:** P-0004 `replicated` (on lab-b's runs at r=5, which I refit; lab-a's runs not used). P-0007 `inconclusive` (my reanalysis of lab-a's runs matches at noise level, but it is their own data, not an independent experiment; edge tests queued).
  - **Round-3 research requests** 001, 003, 004, 005, 007, 008 (cost 7.12, research account).
  - **Round-3 review requests** 009, 010 (cost 2.18, review account, cite P-0007, edge tests at the domain edges 4.5 and 3.75).
  - Request numbering skips 002 and 006 (dropped during drafting; nothing references them).
- Budget, day 2026-11-19:
  - Research: 40 allowance, 13.24 used through round 2, 7.12 committed this round, about 19.6 left. Unused credits do not roll over, so the remainder should be spent or deliberately left.
  - Review: 15 allowance, 11.32 used through round 2, 2.18 committed this round, about 1.5 left.
  - Grant: 0 today (lab-a won the grant).

## What the data say now

**Radial factor, species pairs at separations 6-9.** Round-2 fits (two-particle, r^-2.5 shape, both coefficients free; procedure `analysis/round2_check.py`), compared with K5 x G(r) with G(6)=0.916, G(7)=0.860, G(8)=0.773, G(9)=0.6585:

| request | pair, r | measured K (per particle) | predicted | deviation |
|---|---|---|---|---|
| r2/001 | C-C, 8 | 9.06, 9.09 | 9.55 | -5.2%, -4.8% |
| r2/002 | C-C, 9 | 8.16, 7.97 | 8.14 | +0.3%, -2.1% |
| r2/003 | A-B, 9 | K_A(B) 6.06, K_B(A) 8.53 | 5.92, 8.13 | +2.3%, +4.9% |
| r2/004 | B-C, 6 | K_B(C) -5.59, K_C(B) -9.39 | -5.59, -9.70 | 0.0%, -3.2% |
| r2/005 | B-B, 8 | 4.71, 4.79 | 4.73 | -0.4%, +1.1% |

All residual rms 0.048-0.052, no census events. The only systematic signal is that C-C at 8 comes out about 5% below the factor fixed by A-A data at 8. Possible explanations: species-dependent shape at 8, or noise in the single A-A run that set G(8). Round-3 requests 001 and 004 test this with the same geometry and duration for A-A and C-C.

Implied species ratios at 9 (ratio to r=5): C-C 0.653 (from 002), A-B 0.674 (K_A(B)), 0.691 (K_B(A)). B-C at 6 gives 0.916 (B side) and 0.887 (C side). The C-side ratio is 3% below the B-side ratio, which points the same way as the C-C signal.

**Hypotheses (state after round 2 data):**
- **H-shared-factor** (one radial factor G(r) for all species, K5 x G(r)): supported at 6-9 for all pairs measured, within 6%. Open at 8 (C-C vs A-A, 5%) and at 6-7 for A-A and mixed pairs beyond the single runs.
- **H-species-shape** (shape differs by species): not rejected; the C-C-at-8 result and the C-side B-C ratio are the evidence for it. Round-3 requests 001, 004, 005 are the decisive tests.
- **H-additive** (pairwise sum for N>2): supported at N=3 (A,A,C at sides about 4-4.5; round-1 run 011, rms 0.050) and N=4 (A,B,C,A; run 012, rms 0.051), both within noise. Not tested beyond N=4 anywhere.
- **H-lone-B** (free flight of species B, lone particle): supported by round-1 run 016.
- **H-power** (pure r^-2.5, constant K over 3-9): rejected; coefficients fall with separation (K_eff falls ~33% from r=5 to 9).

**P-0004 check (this round).** lab-b's separation-5 runs 2026-11-18/r3/lab-b/012-014, refit by me (sample_dt 0.001 subsampled to 0.01): A-B K_A(B) 8.97 (claim 9.0), K_B(A) 12.54 (12.3); A-C K_A(C) -8.96 (-8.6), K_C(A) -20.69 (-21.4); B-C K_B(C) -6.24 (predicted -5.9), K_C(B) -9.98 (predicted -10.7). Replicated within 4%. P-0004 is superseded by P-0005, so this is a check of the claims as written.

**P-0007 check (this round).** lab-a's triangle runs 2026-11-19/r1/lab-a/001-004, refit under my integrator with the P-0005 table and A-A at 17.7 or 18.0: rms 0.047-0.051 per coordinate. Consistent. Inconclusive as a review verdict because it is reanalysis of lab-a's own data (same standard as lab-c applied to P-0004).

## Plan for the next session

1. **Read round-3 results** for `2026-11-19/r3/lab-keystone/` 001, 003, 004, 005, 007, 008 and review 009, 010. Analysis script: copy `round2_check.py`, set the request path to r3, and use the pre-registered numbers in `analysis/predictions_round3.json`.
2. **Decision rules** (from `predictions_round3.json`):
   - 001 (A-A at 8): measured > 13.4 means the shared factor holds for A-A at 8; below 13.4 means A-A is closer to C-C (0.735).
   - 004 (C-C at 8, T=6): above 9.3 means the shared factor holds for C-C; below means C-C at 8 is species-dependent.
   - If 001 and 004 both sit near the shared factor, P-0008 c1 stands and the 5% C-C deviation was run noise. Publish a short update.
   - If A-A and C-C differ at 8 by more than 4%, file P-0009: the shared-factor claim narrows to same-species or mixed pairs, and P-0008 gets a narrowing note.
   - 005 (A-C at 7): K_C(A) near -17.35 would confirm P-0006 c4's shortfall, a species effect on the C side. Near -18.3 would mean P-0006 c4 was run noise.
   - 007, 008 (B-B and A-B at 6): test G(6) = 0.916 for species other than B-C.
3. **Reviews 009, 010** (P-0007 edge tests): update `out/reviews/P-0007/lab-keystone.json`. Verdict `replicated` or `narrowed` if both pass rms <= 0.07; `falsified` if either fails with clear rms above 0.12. The proposed domain should only narrow where a test fails.
4. **Budget:** about 19.6 research credits remain today. Do not spend them just because they exist. If round 3 is the last round today, the unused budget is lost.
5. **Reply to challenges:** read any review of P-0008. Check the cited run first.
6. Not yet requested and deliberately deferred: N >= 5 additivity (a 16-particle test needs G beyond 9 and close-approach handling; it is the most valuable untested extension, and it belongs to a later day).

## Things not to do

- Do not try to locate simulator source or hidden parameters. Attempts are logged and disqualify the lab.
- Do not claim masses. The K_B/K_A ratios are not mass ratios without an assumed Newton's third law.
- Do not extend P-0008 beyond two particles, separation 6-9, or T=6, without new runs.
- Do not extend the synthesis to N>=3 on the basis of these pairs. That is P-0007 (lab-a) and the 4-particle test above.

## Analysis files (out/labs/lab-keystone/analysis/)

- `round2_check.py`: two-particle fit (grid + refinement, r^-2.5 shape, both coefficients free) for round-2 requests; also imported by the review check. Self-contained pure python.
- `review_p0004_check.py`: refit of lab-b's separation-5 pair runs (P-0004 check).
- `review_p0007_check.py`: pairwise-sum check of lab-a's triangle runs (P-0007 check). Uses `labs/lab-keystone/analysis/sim.py` (integrator) from the repo.
- `predictions_round3.json`: round-3 pre-registrations with decision rules.

Older analysis files (`check_nbody.py`, `fit_aa.py`, `keff_aa.py`, etc.) are in `labs/lab-keystone/analysis/` in the repo. `validate_p0007.py` expects an out/papers/P-0007 model that does not exist; treat it as broken.
