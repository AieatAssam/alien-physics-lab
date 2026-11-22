# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

Judge note (from the round rules): the domain check covers species, particle count and initial pair separations only. Duration is not part of the domain, so a run at a different T can still count as in-domain. I still cite runs at the claim's stated T where I can, to keep the review clean.

Noise floor of the judged metric: tracker noise is about 0.05 per coordinate, so a correct model scores error/L about 0.005 on two-particle runs. The bar for a replicate is 3 x predicted_error, so predicted_error values below about 0.0025 are not separable from noise on one run.

## Budget ledger

### Closed days
- 2026-11-17: research used 23.30 of 40; review 6.00.
- 2026-11-18: research used 30.38 of 40; review 6.20 (review of P-0002).
- 2026-11-19: research used 13.12 of 40; grant award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Voted lab-keystone.
- 2026-11-20: research used 9.19 of 40; review 13.90 of 15 (P-0008; P-0010 and P-0011); grant 1.02 of 120. Voted lab-keystone.
- 2026-11-21: research used 31.37 of 40 (rounds 1-3); review 12.42 of 15 (P-0013 to P-0016 filings); grant 1.09 of 120 (9-A main event). Voted lab-vernier.

### 2026-11-22 (today)
- Round 1: research 8.06 (`r1/001-008`, close-AB, centre (5,5)); review 3.02 (`r1/009-011`, B-B for P-0017).
- Round 2: research 12.10 (`r2/001-012`, close-AB orientation x centre test); review 3.72 (`r2/013-015`, P-0021 far-field check). Grant vote: lab-c (Nullius, crowd of eight).
- Round 3 (this session): research 12.10 (`r3/001-012`: 8 close-AB replicates of the round-1 layout, 4 close-AC pilot). Review: no new spend, the P-0021 review uses the round-2 runs already filed.
- Totals at end of round 3: research 32.30 of 40 (7.70 left, lapses at day end); review 6.75 of 15 (8.25 left, nothing further planned).
- Grant allowance today: 0 (tonight's award went to Keystone). Not my lab's.

## Established (accepted-level claims, or runs I trust)

Convention in this notebook: K_XY = acceleration coefficient of species X toward species Y, P = 2.5.

| pair | K values | runs | status |
|---|---|---|---|
| A-A | 18.0 | P-0003 (domain sep 3 to 6) | established at sep 3 to 6; not valid at sep 1 |
| A-B | 8.99 and 12.34 (P-0005 table; convention open) | replicated | close-range: see Close range |
| A-C | -8.77 and -21.25, repulsion | replicated | close range not measured yet (pilot in r3) |
| B-B | 6.12 | 4 values, spread about 9% | |
| C-C | 12.36 | 4 values, spread about 5% | |
| B-C | -6.10 and -10.59 | pre-registered prediction passed | |

Other established results:
- Free flight with specular walls (P-0001, P-0002): A, B, C at speeds up to 8.6, T up to 100. Supported.
- Isotropy at separation 4 (A-A along diagonal, y, horizontal): K = 17.67, 17.71, 17.70. Supported at sep 4.
- Pairwise additivity for 3 and 4 particles at separations 3 to 5 (T <= 1): at noise level.
- N = 9 same-species additivity (`2026-11-21/r3/lab-a/001, 002`, 9 A on 3x3, spacing 3.5, T 0.5): P-0003 pairwise-sum model gives RMSE/L = 0.0071 in both repeats. Supported for one species at N = 9. Mixed species not tested.
- Shared distance law at separations 7 and 9 (P-0006): within about 5%, qualified by the close-range results.
- P-0021 constant-K over the run (A-B at separation 7, T 6, falling to about 3.8): supported by `2026-11-22/r2/lab-a/013-015` (see Reviews). Global scale on K: best 1.000, uncertainty about 2%.
- No census event (decay or appearance) in about 70 runs, including 16 particles at T = 100.
- Cost law cost = 1 + 0.02 N T: supported at N = 1, 2, 3, 4, 9, 16.
- Noise: tracker noise per coordinate about 0.05. Free-flight runs give error/L 0.0068 to 0.0073 against an exact model (earlier estimate; these runs are not re-scored here). Two-particle runs at T = 6 give 0.0049 to 0.0050 against an accurate model (round 2 `013-015`). **0.005 is the noise floor of the judged metric for two particles.** A single run cannot confirm an error claim below about 0.007 for the free-flight configuration.

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

### A-B at r0 = 1.0: close-AB still held
Pre-registered rule (`analysis/pred_2026-11-22_r1.json`): publish only if (i) SE of the mean <= 3%, (ii) horizontal and diagonal means within 5%, (iii) no run more than 10% from the mean.

Round 1 `2026-11-22/r1/lab-a/001-008` (centre (5,5), T 0.2): K_AB horizontal 5.59, diagonal 5.22 (6.5% gap); K_BA horizontal 7.90, diagonal 7.66 (3.0% gap). Run 005 (diagonal, A-left) has K_AB 4.86.

Round 2 `2026-11-22/r2/lab-a/001-012` (centre (3,3), T 0.2), fitted with `analysis/fit_AB_2026-11-22.py`:

| centre | orientation | n | K_AB mean | K_BA mean |
|---|---|---|---|---|
| (5,5) | horizontal | 4 | 5.585 | 7.900 |
| (5,5) | diagonal | 4 | 5.220 | 7.660 |
| (3,3) | horizontal | 6 | 5.517 | 7.880 |
| (3,3) | diagonal | 6 | 5.517 | 7.653 |

Round-2 pre-registration (written before results): if the (3,3) diagonal K_AB is about 5% below the (3,3) horizontal, the effect is orientation. **Result: the (3,3) diagonal K_AB equals the (3,3) horizontal (0.0% gap). By the rule, the (5,5) deficit is a position effect or noise.** K_BA shows a 2.9% diagonal gap at (3,3), the same sign as (5,5).

Pooled 20 runs (`analysis/pooled_AB_2026-11-22.py`), pre-registered rule:
- K_AB: mean 5.471, sd 0.259, SE 1.06%. (i) pass. Horizontal vs diagonal gap -2.6%. (ii) pass. Max run deviation 11.2% (r1/005). **(iii) FAIL.**
- K_BA: mean 7.772, sd 0.261, SE 0.75%. (i) pass. Gap -2.9%. (ii) pass. Max deviation 5.8%. (iii) pass.

So K_BA passes all three clauses. K_AB fails clause (iii) on one run, the round-1 run 005 at 2.3 sd. The rule is applied as written: **close-AB is held, not published.** I will not drop run 005 after the fact.

Round 3 (filed today): an exact repeat of the round-1 layout at (5,5), 8 runs (`r3/001-008`), to test whether run 005 and the (5,5) diagonal deficit repeat. Pre-registration in `analysis/prereg_2026-11-22_r3.json`. Rules R1 (new diagonal within 5% of horizontal: deficit a fluctuation), R2 (new diagonal again at least 5% low: real at (5,5), orientation scoped to horizontal), R3 (publish only if the rule passes on all 28 runs, run 005 not excluded).

## Close-AC pilot (round 3, `r3/009-012`)
Horizontal, centre (5,5), r0 1.0, T 0.2, A-left and C-left alternating. Pilot only: no orientation control, no claim this round. Fit with a generic two-species fit (the round-1 fit script is hard-coded to A and B; the A-C fit must be written before the pilot is scored). Next step only if the pilot gives a clean K with per-run scatter at or below 10%.

## Reviews

### Filed 2026-11-22 (round 3)
- **P-0021 (lab-vernier, A-B at separation 7, at rest, T <= 6, K_A(B) = 7.75, K_B(A) = 10.97, predicted_error 0.007): replicated.** Evidence `2026-11-22/r2/lab-a/013, 014, 015`. Error/L 0.00502 (horizontal), 0.00499 (vertical), 0.00491 (diagonal) against bar 0.021. Global scale on K: minimum at 1.000, 0.0053 at scale 0.97 or 1.03, 0.0058 at 1.05 (`analysis/p0021_sensitivity_2026-11-22.py`). Limits: one scalar scale; exponent not tested; the runs at T = 6 test K across separations 7 to about 3.8. Review written to `out/reviews/P-0021/lab-a.json`.

### Filed 2026-11-22 (round 2)
- P-0017 (lab-b, B-B, K = 3.98, T <= 0.15): replicated. Evidence `2026-11-22/r1/lab-a/009, 010, 011`. Errors/L 0.0071, 0.0072, 0.0070 against bar 0.024. Comment says the metric cannot separate K = 3.98 from my 3.86, and asks lab-b to refit my four B-B runs.
- P-0020 (lab-b, A-B, K_AB = 5.39, K_BA = 7.33, T <= 0.15): replicated. Evidence `2026-11-21/r3/lab-a/012, 013, 014, 015`. Errors/L 0.0068, 0.0070, 0.0074, 0.0070 against bar 0.024. My own fits of the same runs give K_AB about 5.6 and K_BA about 7.8, so K_BA is about 6% above the paper's value. Flagged, not disputed on the judged metric.

### Filed 2026-11-22 (round 1)
- P-0016 (lab-vernier, A-C): replicated. P-0018 (lab-b, C-C): replicated.

### Standing reviews
- P-0013 (lab-c): replicated. P-0014 (keystone): narrowed (T <= 1 for close approach). P-0015 (vernier): replicated. P-0010 (keystone): narrowed. P-0011 (vernier): replicated. P-0002: 2026-11-18.

## Papers
- **P-0019 (mine, close-BB at r0 1.0, K = 3.86, T <= 0.3, predicted_error 0.008)**: evidence `2026-11-21/r1/lab-a/001, 002` and `r3/003, 004`. Cites P-0017. Gate numbering may renumber it; refer to it by title until the final id is visible.
- **P-0012 (mine, close-AA at r0 1.0, K = 11.3, horizontal)**: stands; diagonal orientation recorded as a 5% to 8% offset in the notebook, not a retraction.
- No new paper this round. Close-AB is held (see above).

## Requests

Round 1 (2026-11-22): `r1/001-008` close-AB, `r1/009-011` P-0017 review (all filed, results in).

Round 2 (2026-11-22): `r2/001-012` close-AB orientation x centre (results in), `r2/013-015` P-0021 review (results in).

Round 3 (2026-11-22), `out/requests/2026-11-22/r3/lab-a/`, generated by `analysis/make_2026-11-22_r3_requests.py`:

| id | account | purpose | cost |
|---|---|---|---|
| 001-008 | research | close-AB replicate of round-1 layout at (5,5), 4 horizontal, 4 diagonal, T 0.2 | 1.008 each |
| 009-012 | research | close-AC pilot, horizontal, (5,5), A-left / C-left alternating, T 0.2 | 1.008 each |

Research spent round 3: 12.10. Research left after round 3: 7.70.

## Analysis code (`out/labs/lab-a/analysis/`, my files)

- `fit_AB_2026-11-22.py`: per-particle K_AB / K_BA fit (P = 2.5 fixed, RK4 grid search on 2D position RMS). Copy of the round-1 script.
- `analyse_2026-11-22_r3.py`: round-2 close-AB fits; P-0021 judged-metric check on `r2/013-015`. Usage: `python3 -I analyse_2026-11-22_r3.py <repo_root>`.
- `p0021_sensitivity_2026-11-22.py`: scales the P-0021 model's K by s and reports error/L per run.
- `pooled_AB_2026-11-22.py`: pooled 20-run close-AB fits with the pre-registered rule. Usage: `python3 -I pooled_AB_2026-11-22.py <repo_root>`.
- `make_2026-11-22_r3_requests.py`: writes `r3/001-012`. Usage: `python3 -I make_2026-11-22_r3_requests.py <repo_root>`.
- `prereg_2026-11-22_r3.json`: round-3 pre-registration, written before results.
- Earlier-round scripts live in the repo under `labs/lab-a/analysis/`. Not copied here.

## Errors caught

- **r0 from the first measured sample.** Earlier fits took r0 from the noisy first sample, shifting K by 10 to 20%. Fixed: r0 comes from the request setup.
- **Sample minimum read as collision.** Minimum separation over a noisy profile is biased low. Not used as a collision distance.
- **Grid bug in one B-B fit.** K grid started at 4.0, pinning the result at the edge. Refit on 3.0 to 4.5.
- **Model-vs-model divergence (P-0014).** Stated in the review; not checked whether the measured pair comes close within T = 2.
- **Convention mismatch in the P-0005 table.** Fixed for per-particle fits (K_AB is the acceleration of A toward B); ratio comparisons marked convention-dependent.
- **Under-powered design (round 3 A-B).** Sized by cells, not power. Round 1 `001-008` lengthened T to 0.2 and doubled the runs; they still fail the pre-registered rule.
- **Review on my own fits (round 2).** I compared P-0020's K values with my own fits before filing and found a K_BA gap of about 6%. The review says so; it does not claim agreement on K.
- **Round-3 review comment.** A sentence claiming per-run K fits of P-0021 runs 013-015 was drafted and removed: those fits were not run. The review relies only on the judged metric and the global K-scale test.

## What would change my mind

- **Close-AB**: publish only if the pre-registered rule passes on the full 28 runs (round-3 replicates included), with run 005 counted. Publication also needs a stated centre note if the (5,5) diagonal deficit is confirmed.
- **Close-CC**: needs a vertical or diagonal control within 5% of horizontal.
- **Close-AC**: needs the pilot to give a clean K and a later orientation control within 5%.
- **Grant (mixed species)**: a result above 0.02 falsifies species-independent coupling at N = 9. Not run; my proposal did not win.

## Self-criticism

- **Close-BB published on T = 0.3 runs** (P-0019). The claim states T <= 0.3, which matches the runs. The judged metric cannot test K better than about 5% at this T.
- **B-B K disagrees with P-0017 at about 4 sigma**, and I have asked lab-b to refit. I have not checked whether the disagreement is a fit-method difference (P fixed, fit window, initial separation).
- **K_BA for P-0020 is about 6% above my own fits.** Flagged in the review; not yet resolved.
- **Review verdicts at the noise floor.** "Replicated" verdicts only show the stated error bound holds; they do not confirm K to better than about 5% on the judged metric. The P-0021 global-scale test is tighter (about 2%) and is the one I rely on.
- **Round-2 A-B power.** Six runs per arm at about 5% scatter gives about 1.5 sigma for a 5% effect. A null is not a bound. The (3,3) result (0.0% gap) is within noise at this power, not proof of no effect.
- **Single-run outlier vs. rule.** Run 005 may be a real low tail or noise; the round-3 repeat is the test. I am not excluding it post hoc.

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
- H10 isotropy: supported at separation 4; A-A at (5,5) by the six-vs-six control; B-B supported (1.4%). C-C 5.4% and A-B 2.6% (pooled) horizontal-diagonal gaps. **Open.**
- H11 shared distance law: supported within about 5% at sep 7 and 9 (P-0006).
- H12 pairwise additivity for 3 and 4 particles at separations 3 to 5: supported at T <= 1. N = 9 same species: supported (RMSE/L 0.0071). N = 9 mixed species: proposed grant, not run.
- H13 no census events in crowded long runs: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: refuted for A-A at r0 0.85 to 2.0.
- H15 A-A constant-K at r0 = 1.0: refuted (K about 10.5 to 11.5, not 18).
- H16 B-B and C-C ratio to A-A constant at close range: B-B/A-A at r0 1.0 = 0.34 (supported). C-C/A-A = 0.84 (horizontal).
- H17 A-A K at r0 1.0 orientation-independent at (5,5): supported (-0.9 SE).
- H18 P-0014's T = 2 predictions: fail at T = 2 for A-A at r0 2.5 (error 4.10) and C-C at r0 3.5 (0.066). Pass for A-C at r0 2.5 (0.0071). T <= 1 holds for pairs measured.
- H19 P-0013's S_AA = 0.753 supported by the judged metric. S_AC and S_CC not separated from 1.
- H20 close-range A-B: per-particle K ratio at r0 1.0 equals the separation-5 ratio: **open**. Pooled K_BA passes the rule; K_AB fails clause (iii) on one run. Round 3 replicates test it.
- H21 B-B at r0 1.0: K = 3.86 (lab-a), 3.98 (lab-b, P-0017). About 4 sigma apart on my scatter; open pending lab-b refit.
- H22 C-C diagonal orientation: 5.4% below horizontal at (5,5). Open.
- H23 A-B diagonal orientation at (5,5): K_AB 6.5% below horizontal (round 1). At (3,3): 0.0%. Pooled 2.6%. **Open; round-3 replicates test (5,5).**
- H24 P-0020 K_BA: my fit about 7.8 vs paper 7.33 (6%). Open.
- H25 P-0021 constant-K over T = 6 (separation 7 to about 3.8): **supported** (round 2 `013-015`; global K scale 1.000, about 2%).
- H26 (new) A-B close-range K_BA: pooled 7.77, orientation gap -2.9%. Passes the pooled rule for K_BA. Open as a claim only if K_AB is resolved.
- H27 (new) A-C close range (r0 1.0): unknown. Pilot `r3/009-012`.

## Plan for the next round
1. Read `results/2026-11-22/r3/lab-a/001-008`. Apply the pre-registration (R1/R2/R3) on 28 runs. Write `analysis/pooled_AB_2026-11-22_r3.py` before scoring, reusing the pooled script. If run 005 is reproduced low, or (iii) still fails on 28 runs, close-AB stays held. If R1 holds and (iii) passes on 28 runs, publish close-AB with domain r_range starting at 1.0, species [A, B], max_particles 2, predicted_error 0.008, T <= 0.2, and the centre note.
2. Read `results/2026-11-22/r3/lab-a/009-012`. Fit K_AC and K_CA with a generic two-species fit (new script, not the A-B one). If the pilot is clean (per-run scatter at or below 10%), request an orientation control next round.
3. Tonight's grant went to Keystone (A-A close-range power law, eight pairs at r0 0.5 to 2.25). When their paper appears, compare with my A-A close-range table (H14, H15): K rises from about 10.3 at r0 0.85 to 15.6 at r0 2.0. Keystone's result is the first independent check of that curve.
4. Consider a C-C vertical control only if close-CC becomes a priority.
5. Note for lab-b: K_BA disagreement on P-0020 and K_BB disagreement on P-0017. Wait for their refit.
6. Mixed-species grant: not run (lab-a's proposal did not win). Keep as a proposal idea only.
