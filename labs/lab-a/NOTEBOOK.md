# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

Judge note (from the round rules): the domain check covers species, particle count and initial pair separations only. Duration is not part of the domain, so a run at a different T can still count as in-domain. I still cite runs at the claim's stated T where I can, to keep the review clean.

## Budget ledger

### Closed days
- 2026-11-17: research used 23.30 of 40; review 6.00.
- 2026-11-18: research used 30.38 of 40; review 6.20 (review of P-0002).
- 2026-11-19: research used 13.12 of 40; grant award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Voted lab-keystone.
- 2026-11-20: research used 9.19 of 40; review 13.90 of 15 (P-0008; P-0010 and P-0011); grant 1.02 of 120. Voted lab-keystone.
- 2026-11-21: research used 31.37 of 40 (rounds 1-3); review 12.42 of 15 (P-0013 to P-0016 filings); grant 1.09 of 120 (9-A main event). Voted lab-vernier.

### 2026-11-22 (today)
- Round 1 (earlier session): research 8.06 (`r1/001-008`, close-AB); review 3.02 (`r1/009-011`, B-B for P-0017). Grant proposal filed (9-body mixed-species Latin square).
- Round 2 (this session):
  - Research filed: 12.10 of 31.94 left (`r2/001-012`, close-AB orientation x centre test, 1.008 each). Research left after filing: 19.84. Unused research lapses at day end.
  - Review filed: 3.72 of 11.98 left (`r2/013-015`, P-0021 far-field infall, 1.24 each). Review left after filing: 8.26.
  - Reviews filed (verdicts, no new spend): P-0017 replicated; P-0020 replicated.
  - Grant vote: lab-c (Nullius, crowd of eight). Reason in `out/grants/2026-11-22/votes/lab-a.json`.

## Established (accepted-level claims, or runs I trust)

Convention in this notebook: K_XY = acceleration coefficient of species X toward species Y, P = 2.5.

| pair | K values | runs | status |
|---|---|---|---|
| A-A | 18.0 | P-0003 (domain sep 3 to 6) | established at sep 3 to 6; not valid at sep 1 |
| A-B | 8.99 and 12.34 (P-0005 table; convention open) | replicated | close-range: see Close range |
| A-C | -8.77 and -21.25, repulsion | replicated | |
| B-B | 6.12 | 4 values, spread about 9% | |
| C-C | 12.36 | 4 values, spread about 5% | |
| B-C | -6.10 and -10.59 | pre-registered prediction passed | |

Other established results:
- Free flight with specular walls (P-0001, P-0002): A, B, C at speeds up to 8.6, T up to 100. Supported.
- Isotropy at separation 4 (A-A along diagonal, y, horizontal): K = 17.67, 17.71, 17.70. Supported at sep 4.
- Pairwise additivity for 3 and 4 particles at separations 3 to 5 (T <= 1): at noise level.
- **N = 9 same-species additivity** (round-3 grant `2026-11-21/r3/lab-a/001, 002`, 9 A on 3x3, spacing 3.5, T 0.5): P-0003 pairwise-sum model gives RMSE/L = 0.0071 in both repeats, inside the pre-registered support threshold of 0.01. Supported for one species at N = 9. Mixed species not tested yet.
- Shared distance law at separations 7 and 9 (P-0006): within about 5%, qualified by the close-range results.
- No census event (decay or appearance) in about 70 runs, including 16 particles at T = 100.
- Cost law cost = 1 + 0.02 N T: supported at N = 1, 2, 3, 4, 9, 16.
- Noise: tracker noise on separation sd about 0.07 (about 0.05 per coordinate). Free-flight runs give error/L 0.0068 to 0.0073 against an exact model. **0.007 is the noise floor of the judged metric.** A single run cannot confirm an error claim below about 0.007.

## Close range

### B-B at r0 = 1.0: orientation control passes
Symmetric fits (P = 2.5 fixed), T = 0.3:

| run | orientation | K_fit |
|---|---|---|
| 2026-11-21/r1/lab-a/001 | horizontal | 3.822 |
| 2026-11-21/r1/lab-a/002 | horizontal | 3.838 |
| 2026-11-21/r3/lab-a/003 | diagonal | 3.884 |
| 2026-11-21/r3/lab-a/004 | diagonal | 3.884 |

Pooled K = 3.857 (sd 0.03). Published as P-0019 (close-BB), K = 3.86, T <= 0.3. P-0017 (lab-b, K = 3.98) differs by about 3%, roughly 4 sigma on my scatter. The judged metric cannot separate them.

### C-C at r0 = 1.0: orientation control fails the pre-registered rule (narrowly)
Horizontal mean 9.50, diagonal mean 8.99 (5.4% lower), at T 0.15 (`2026-11-21/r1/lab-a/003, 004` horizontal; `r3/005, 006` diagonal). The pre-registered window missed by 0.4%. Rule not met; close-CC held. Open: a real orientation effect, or a position effect of the (5,5) diagonal layout.

### A-A at r0 = 1.0
Round-3 six-vs-six control at (5,5): horizontal mean K 11.10 (sd 0.24), diagonal 10.92 (sd 0.43), difference -0.18 with SE 0.20 (-0.9 SE). No orientation effect at (5,5). Pooled 12-run K = 11.01. P-0012's K = 11.3 sits about 2.5% above this pool, inside its predicted_error at T <= 0.15; recorded as a known offset.

A-A K at r0 0.85 to 2.0 is not constant: about 10.3 (0.85), 10.3 to 11.5 (1.0), 12.4 (1.25), 14.0 (1.5), 15.6 (2.0). P-0003 is not contradicted (its domain is sep 3 to 6).

### A-B at r0 = 1.0: close-AB held (pre-registered rule fails)
Round 1 `2026-11-22/r1/lab-a/001-008` (T 0.2, per-particle fits, `analysis/fit_AB_2026-11-22.py`, pre-registration `analysis/pred_2026-11-22_r1.json`):

| run | layout | K_AB (on A) | K_BA (on B) |
|---|---|---|---|
| 001 | horizontal, A left | 5.20 | 7.92 |
| 002 | horizontal, B left | 5.66 | 7.86 |
| 003 | horizontal, A left | 5.94 | 8.02 |
| 004 | horizontal, B left | 5.54 | 7.80 |
| 005 | diagonal, A left | 4.86 | 7.56 |
| 006 | diagonal, B left | 5.18 | 7.62 |
| 007 | diagonal, A left | 5.34 | 7.66 |
| 008 | diagonal, B left | 5.50 | 7.80 |

Pre-registered rule, checked today:
- (i) SE of the 8-run mean <= 3%: K_AB SE 0.125 on mean 5.40 (2.3%); K_BA passes. **Pass.**
- (ii) horizontal vs diagonal means within 5%: K_AB horizontal 5.59, diagonal 5.22 (6.5% apart). **Fail.** K_BA horizontal 7.90, diagonal 7.66 (3.0%). Pass.
- (iii) no run more than 10% from the 8-run mean: run 005 K_AB 4.86 is 10.04% below 5.40. **Fail (marginal).**

Verdict: **close-AB held, not published.** The K_AB horizontal-diagonal gap is about 6.5%, the same direction as the C-C gap (diagonal lower). It is an open orientation-or-position question for A-B, which round 2 `001-012` is built to test.

Round 2 test design (`analysis/make_2026-11-22_r2_requests.py`): horizontal and diagonal A-B at r0 1.0, centre (3,3), T 0.2, six per orientation, A-left and B-left alternating. Combined with round 1 at (5,5), this gives a 2 x 2 (orientation x centre) table with 4 to 6 runs per cell. Power: per-run sd of K_AB is about 6.5%, so an orientation difference of 5% at 6 runs per arm is at about 1.5 sigma. This is underpowered for a 5% call. A null result will be read as "no detected effect at this power", not as a bound.

Pre-registration for round 2 A-B (written before results): if the (3,3) diagonal K_AB is again about 5% below the (3,3) horizontal, the effect is orientation, and close-AB will be scoped to horizontal only. If the (3,3) diagonal matches the (3,3) horizontal, the (5,5) deficit is a position effect and close-AB needs a note about the centre.

## Reviews

### Filed 2026-11-22 (round 2)
- **P-0017 (lab-b, B-B, K = 3.98, T <= 0.15): replicated.** Evidence `2026-11-22/r1/lab-a/009, 010, 011`. Errors/L 0.0071, 0.0072, 0.0070 against bar 0.024. Comment says the metric cannot separate K = 3.98 from my 3.86, and asks lab-b to refit my four B-B runs. `out/reviews/P-0017/lab-a.json`.
- **P-0020 (lab-b, A-B, K_AB = 5.39, K_BA = 7.33, T <= 0.15): replicated.** Evidence `2026-11-21/r3/lab-a/012, 013, 014, 015`. Errors/L 0.0068, 0.0070, 0.0074, 0.0070 against bar 0.024. My own fits of the same runs give K_AB about 5.6 and K_BA about 7.8, so K_BA is about 6% above the paper's value. Flagged, not disputed on the judged metric. `out/reviews/P-0020/lab-a.json`.

### Filed 2026-11-22 (round 1)
- P-0016 (lab-vernier, A-C): replicated. P-0018 (lab-b, C-C): replicated.

### Pending
- **P-0021 (lab-vernier, A-B at separation 7, T <= 6, K_A(B) = 7.75, K_B(A) = 10.97, predicted_error 0.007, bar 0.021): verdict next round.** Evidence to come: `2026-11-22/r2/lab-a/013, 014, 015` (horizontal, vertical, diagonal at separation 7.0, T 6, A left, centre (5,5)).
  - My model check on P-0021's model: the pair reaches r about 3.77 at T = 6 with no collision. So the claim's constant-K statement is tested over separations from 7 down to about 3.8, not just near 7.
  - Verdict rule I will apply: replicated if at least three of the three runs have error <= 0.021. Narrowed if all three pass but the orientation residuals differ by more than the noise floor, with the domain then narrowed to T <= 3 or the separation band shifted. Falsified only if all three fail.
- **P-0019 (mine, close-BB)**: no review requested.

### Standing reviews
- P-0013 (lab-c): replicated. P-0014 (keystone): narrowed (T <= 1 for close approach). P-0015 (vernier): replicated. P-0010 (keystone): narrowed. P-0011 (vernier): replicated. P-0002: 2026-11-18.

## Papers
- **P-0019 (mine, close-BB at r0 1.0, K = 3.86, T <= 0.3, predicted_error 0.008)**: evidence `2026-11-21/r1/lab-a/001, 002` and `r3/003, 004`. Cites P-0017.
- **P-0012 (mine, close-AA at r0 1.0, K = 11.3, horizontal)**: stands; diagonal orientation recorded as a 5% to 8% offset in the notebook, not a retraction.
- Gate numbering: P-0019 may be renumbered; refer to it by title until the final id is visible.

## Requests

Round 1 (2026-11-22): `r1/001-008` close-AB, `r1/009-011` P-0017 review (all filed, results in).

Round 2 (2026-11-22, this session), all under `out/requests/2026-11-22/r2/lab-a/`, generated by `analysis/make_2026-11-22_r2_requests.py`:

| id | account | purpose | cost |
|---|---|---|---|
| 001-006 | research | close-AB, horizontal, centre (3,3), A-left/B-left alternating, r0 1.0, T 0.2 | 1.008 each |
| 007-012 | research | close-AB, diagonal, centre (3,3), A-left/B-left alternating, r0 1.0, T 0.2 | 1.008 each |
| 013 | review (cites P-0021) | P-0021 horizontal, separation 7.0, T 6, A left | 1.24 |
| 014 | review (cites P-0021) | P-0021 vertical, separation 7.0, T 6, A left | 1.24 |
| 015 | review (cites P-0021) | P-0021 diagonal, separation 7.0, T 6, A left | 1.24 |

The request files were checked by field and length. I did not run the full JSON Schema validator (jsonschema is not installed here).

## Grant

- Round-3 event (`2026-11-21/r3/lab-a/001, 002`): RMSE/L 0.0071 both repeats against P-0003. Support for one-species additivity at N = 9.
- My proposal (round 1, 9-body mixed-species Latin square, spacing 3.5, T 0.5, cost 1.09). Question: does pairwise additivity hold across species? I will fix the prediction before the result, from pair couplings at separation 5. Support: RMSE/L <= 0.01. Refutation: > 0.02.
- Round-2 vote: **lab-c (Nullius, crowd of eight)**. Reason: the N=8 octagon has a fixed prediction (error <= 0.01), a stated falsifier (> 0.03, or a residual growing with N), and cost about 1.8. It tests the pair sum past N=3 and targets crowd-8. Icarus's 16-body plan defers its predictions until after the mixed-pair runs, so it is weaker as a pre-registration. I did not vote for my own proposal.

## Analysis code (`out/labs/lab-a/analysis/`, my files)

- `score_2026-11-22_r2.py`: scores P-0017 (`r1/009-011`) and P-0020 (`r3/012-015`) against the judge bar. Usage: `python3 -I score_2026-11-22_r2.py <repo_root>`.
- `make_2026-11-22_r2_requests.py`: writes `r2/001-015`.
- Round-1 scripts (in repo at `labs/lab-a/analysis/`): `analyse_2026-11-22.py`, `fit_AB_2026-11-22.py`, `grant_2026-11-22.py`, `make_2026-11-22_r1_requests.py`, `pred_2026-11-22_r1.json`.

## Errors caught

- **r0 from the first measured sample.** Earlier fits took r0 from the noisy first sample, shifting K by 10 to 20%. Fixed: r0 comes from the request setup.
- **Sample minimum read as collision.** Minimum separation over a noisy profile is biased low. Not used as a collision distance.
- **Grid bug in one B-B fit.** K grid started at 4.0, pinning the result at the edge. Refit on 3.0 to 4.5.
- **Model-vs-model divergence (P-0014).** Stated in the review; not checked whether the measured pair comes close within T = 2.
- **Convention mismatch in the P-0005 table.** Fixed for per-particle fits (K_AB is the acceleration of A toward B); ratio comparisons marked convention-dependent.
- **Under-powered design (round 3 A-B).** Sized by cells, not power. Round 1 `001-008` lengthened T to 0.2 and doubled the runs; they still fail the pre-registered rule.
- **Review on my own fits (today).** I compared P-0020's K values with my own fits before filing and found a K_BA gap of about 6%. The review says so; it does not claim agreement on K.

## What would change my mind

- **Close-AB**: publish only if a later design passes the pre-registered rule with horizontal and diagonal means within 5% at a stated centre. The current evidence shows a 6.5% horizontal-diagonal gap at (5,5) for K_AB.
- **Close-CC**: needs a vertical or diagonal control within 5% of horizontal.
- **P-0021 review**: replicated if three of `013-015` are within 0.021. If the three disagree with each other by more than the noise floor, that is evidence against the constant-K claim across the run.
- **Grant (mixed species)**: a result above 0.02 falsifies species-independent coupling at N = 9.

## Self-criticism

- **Close-BB published on T = 0.3 runs** (P-0019). The claim states T <= 0.3, which matches the runs. The judged metric cannot test K better than about 5% at this T.
- **B-B K disagrees with P-0017 at about 4 sigma**, and I have asked lab-b to refit. I have not checked whether the disagreement is a fit-method difference (P fixed, fit window, initial separation).
- **K_BA for P-0020 is about 6% above my own fits.** I flagged it in the review but have not yet resolved it.
- **Review verdicts at the noise floor.** "Replicated" verdicts only show the stated error bound holds; they do not confirm K to better than about 5%.
- **Round-2 A-B power.** Six runs per arm at about 6.5% scatter gives about 1.5 sigma for a 5% effect. A null is not a bound.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2 to 8.6. B at high speed not tested.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 9, 16.
- H4 no decay: no event in about 70 runs.
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported at separations 3 to 9 as a shared-scale law. Close range: P = 2.5 fits B-B and A-A at r0 1.0 to 2.0; P not tested alone at r0 = 1.0.
- H8 pair force identical for all species pairs: refuted at sep 5.
- H9 coupling factorises as g_ij = q_i q_j: partially supported. Not claimed.
- H10 isotropy: supported at separation 4; A-A at (5,5) by the six-vs-six control; B-B supported (1.4%). C-C 5.4% and A-B 6.5% horizontal-diagonal gaps, both not significant by the pre-registered rules. **Open.**
- H11 shared distance law: supported within about 5% at sep 7 and 9 (P-0006).
- H12 pairwise additivity for 3 and 4 particles at separations 3 to 5: supported at T <= 1. N = 9 same species: supported (RMSE/L 0.0071). N = 9 mixed species: proposed grant, not run.
- H13 no census events in crowded long runs: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: refuted for A-A at r0 0.85 to 2.0.
- H15 A-A constant-K at r0 = 1.0: refuted (K about 10.5 to 11.5, not 18).
- H16 B-B and C-C ratio to A-A constant at close range: B-B/A-A at r0 1.0 = 0.34 (supported). C-C/A-A = 0.84 (horizontal).
- H17 A-A K at r0 1.0 orientation-independent at (5,5): supported (-0.9 SE).
- H18 P-0014's T = 2 predictions: fail at T = 2 for A-A at r0 2.5 (error 4.10) and C-C at r0 3.5 (0.066). Pass for A-C at r0 2.5 (0.0071). T <= 1 holds for pairs measured.
- H19 P-0013's S_AA = 0.753 supported by the judged metric. S_AC and S_CC not separated from 1.
- H20 close-range A-B: per-particle K ratio at r0 1.0 equals the separation-5 ratio: **open**. Round 1 `001-008` do not pass the rule; round 2 `001-012` tests the orientation/centre question.
- H21 B-B at r0 1.0: K = 3.86 (lab-a), 3.98 (lab-b, P-0017). About 4 sigma apart on my scatter; open pending lab-b refit.
- H22 C-C diagonal orientation: 5.4% below horizontal at (5,5). Open.
- H23 (new) A-B diagonal orientation: K_AB 6.5% below horizontal at (5,5) (round 1 `001-008`, not significant at pre-registered power). K_BA only 3%. Open; round 2 `001-012` tests it at (3,3).
- H24 (new) P-0020 K_BA: my fit about 7.8 vs paper 7.33 (6%). Open.
- H25 (new) P-0021 constant-K over T = 6 (separation 7 to about 3.8): open; round 2 `013-015`.

## Plan for the next round
1. Read `results/2026-11-22/r2/lab-a/001-012` (close-AB orientation x centre). Apply the round-2 pre-registration above: if the (3,3) diagonal K_AB is about 5% below the (3,3) horizontal, scope close-AB to horizontal. If the (3,3) diagonal matches the horizontal, the (5,5) deficit is a position effect and close-AB needs a centre note. Either way, re-run the pre-registered rule on all 20 runs before publishing close-AB.
2. Read `results/2026-11-22/r2/lab-a/013-015` and file the P-0021 review (verdict rule above). Write `out/reviews/P-0021/lab-a.json`.
3. Check the grant event for mixed species once round 3 runs it (lab-a's proposal, if it wins the vote). Fix the prediction before the result.
4. Consider a C-C vertical control only if close-CC becomes a priority.
5. Note for lab-b: K_BA disagreement on P-0020 and K_BB disagreement on P-0017. Wait for their refit.
