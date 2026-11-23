# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

Judge notes that govern my claims:
- The domain check covers species, particle count and initial pair separations only. Duration is not in the domain, so a run at a different T can count as in-domain. I still cite runs at the claim's stated T, to keep reviews clean.
- Boundary runs: a run placed exactly on a domain edge can fail the paper's own check by float rounding (seen 2026-11-23 with `1.95` read as `1.94999...`). Place edge runs 0.01 inside the edge. Verify with the paper's `predict()` before filing.
- Noise floor of the judged metric: tracker noise is about 0.05 per coordinate, so a correct model scores RMSE/L about 0.005. A replicate bar of 3 x predicted_error is therefore only informative when predicted_error is above about 0.0025.

## Budget ledger

### Closed days
- 2026-11-17: research used 23.30 of 40; review 6.00.
- 2026-11-18: research used 30.38 of 40; review 6.20 (review of P-0002).
- 2026-11-19: research used 13.12 of 40; grant award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Voted lab-keystone.
- 2026-11-20: research used 9.19 of 40; review 13.90 of 15 (P-0008; P-0010 and P-0011); grant 1.02 of 120. Voted lab-keystone.
- 2026-11-21: research used 31.37 of 40 (rounds 1-3); review 12.42 of 15 (P-0013 to P-0016 filings); grant 1.09 of 120 (9-A main event, `2026-11-21/r3/lab-a/001`). Voted lab-vernier.
- 2026-11-22: research used 32.32 of 40; review 6.75 of 15. Grant allowance 0 (tonight's award went to Keystone).

### 2026-11-23 (today, round 1)
- Filed research: 20.31 of 40 (`r1/009-024`). Reserve 19.69 for rounds 2-3.
- Filed review: 9.73 of 15 (`r1/001-008`, both papers under review).
- Grant: proposal filed (`out/grants/2026-11-23/proposals/lab-a.json`), no spend today.

## Established (accepted-level claims, or runs I trust)

Convention: K_XY = acceleration coefficient of species X toward species Y, P = 2.5 unless stated.

| pair | K values | runs | status |
|---|---|---|---|
| A-A | 17.7 to 18.0 | P-0003 (domain sep 3 to 6) | established at sep 3 to 6; not valid at sep 1 |
| A-B | see Close range | | close-AB held |
| A-C | -5.75 (K_AC), -13.6 (K_CA) at r0 1.0, horizontal | `2026-11-22/r3/lab-a/009-012` | pilot clean; orientation control filed |
| B-B | 6.12 | 4 values, spread about 9% | |
| C-C | 12.36 | 4 values, spread about 5% | |
| B-C | -6.10 and -10.59 | pre-registered prediction passed | |

Other established results:
- Free flight with specular walls (P-0001, P-0002): A, B, C at speeds up to 8.6, T up to 100. Supported.
- Isotropy at separation 4 (A-A along diagonal, y, horizontal): K = 17.67, 17.71, 17.70. Supported at sep 4.
- Pairwise additivity for 3 and 4 particles at separations 3 to 5 (T <= 1): at noise level.
- Shared distance law at separations 7 and 9 (P-0006, C-C and mixed pairs): within about 5%.
- P-0021 constant K over T = 6 (A-B at sep 7 falling to about 3.8): supported (`2026-11-22/r2/lab-a/013-015`). Global K scale 1.000, uncertainty about 2%.
- No census event (decay or appearance) in about 70 runs, including 16 particles at T = 100.
- Cost law cost = 1 + 0.02 N T: supported at N = 1, 2, 3, 4, 9, 16.
- Noise: tracker noise per coordinate about 0.05.

## Close range

### A-B at r0 = 1.0: held (rule failed on one run)
Pre-registration in `analysis/prereg_2026-11-22_r3.json`, written before round-3 results. Rule clauses: (i) SE of the mean <= 3%; (ii) horizontal vs diagonal within 5%; (iii) no run more than 10% from the pooled mean.

Round-3 scoring (2026-11-23, `out/labs/lab-a/analysis/pooled_AB_2026-11-22_r3.py`, all 28 runs: r1 001-008 at (5,5), r2 001-012 at (3,3), r3 001-008 at (5,5)):

| set | horizontal K_AB | diagonal K_AB | horizontal K_BA | diagonal K_BA |
|---|---|---|---|---|
| r1 (5,5) | 5.585 (n 4) | 5.220 (n 4) | 7.900 | 7.660 |
| r3 (5,5) replicate | 5.540 (n 4) | 5.520 (n 4) | 7.745 | 8.020 |
| r2 (3,3) | 5.517 (n 6) | 5.517 (n 6) | 7.880 | 7.653 |

Pooled 28 runs:
- **K_AB**: mean 5.488, sd 0.239, SE 0.82%. (i) pass. Horizontal vs diagonal gap -1.98%. (ii) pass. Max deviation 11.44% (`2026-11-22/r1/lab-a/005`, K_AB 4.86). **(iii) FAIL.**
- **K_BA**: mean 7.804, sd 0.268, SE 0.65%. (i) pass. Gap -1.11%. (ii) pass. Max deviation 7.39% (`r3/008`). (iii) pass.

Pre-registered R1 (new diagonal at (5,5) within 5% of new horizontal): **passes**. The round-1 diagonal deficit did not repeat (gap -0.4% on the round-3 replicate). It is treated as a fluctuation.
Pre-registered R3 (publish only if the rule passes on all 28 runs with run 005 counted): **K_AB fails clause (iii)**. Close-AB stays held. I am not excluding run 005 after the fact, and I am not adding runs to dilute it. A pooled K_AB fit does not clear clause (iii) with run 005 in the set: its deviation from the mean is 2.6 sd and stays above 10% as the mean moves.

What this means: K_BA alone passes every clause, but a pair claim needs both K values. No A-B claim is published this round.

### C-C at r0 = 1.0: orientation control incomplete
Horizontal mean 9.50 (`2026-11-21/r1/lab-a/003, 004`), diagonal mean 8.99 (`r3/005, 006`), 5.4% lower at T 0.15. The pre-registered window missed by 0.4%, so the orientation rule was not met. Vertical control filed (`r1/015-018`), see Requests.

### A-A at r0 = 1.0
Six-vs-six control at (5,5): horizontal K 11.10, diagonal 10.92, difference -0.9 SE. Pooled 12-run K = 11.01. P-0012's K = 11.3 sits about 2.5% above the pool (recorded as a known offset). A-A K at r0 0.85 to 2.0 is not constant: about 10.3 (0.85), 10.3 to 11.5 (1.0), 12.4 (1.25), 14.0 (1.5), 15.6 (2.0). P-0003 is not contradicted (domain sep 3 to 6).

### Close-AC pilot (round 3, `2026-11-22/r3/lab-a/009-012`), scored today
Horizontal, centre (5,5), r0 1.0, T 0.2. Fit with `analysis/fit_AC_2026-11-23.py` (generic two-species, signed K, grid step 0.1):

| run | species left | K_AC | K_CA | RMSE/L |
|---|---|---|---|---|
| 009 | A | -6.0 | -13.7 | 0.0050 |
| 010 | C | -5.7 | -13.5 | 0.0051 |
| 011 | A | -5.7 | -13.3 | 0.0049 |
| 012 | C | -5.6 | -13.9 | 0.0050 |

K_AC mean -5.75 (sd 3.0%); K_CA mean -13.6 (sd 1.9%). Per-run scatter is within the pilot criterion (10%). Ratio K_CA/K_AC = 2.36; the older round-1 values (-8.77, -21.25) give 2.42 at a different separation. Both signs are repulsive. Not a claim yet: the pre-registered rule needs the orientation control.

### Crowd of nine (crowd-8), scored today: not published
Problem `crowd-8` (bounty 3) is still open. I checked the existing 9-A runs (`2026-11-21/r3/lab-a/001` grant, `002` research; 3x3 grid, spacing 3.5, at rest, T 0.5) against a uniform pairwise-sum A-A law (`analysis/crowd9_check_2026-11-23.py`):

| K (uniform, P 2.5) | RMSE/L run 001 | RMSE/L run 002 |
|---|---|---|
| 0 (no interaction) | 0.0080 | 0.0080 |
| 12 | 0.0053 | 0.0054 |
| 17.0 | 0.0050 | 0.0050 |
| 17.7 | 0.0050 | 0.0051 |
| 25 | 0.0058 | 0.0059 |

Two findings:
1. At T = 0.5 the test is weak on K. Any K from 12 to 25 is at the noise floor. Only "no interaction" is clearly separated (0.008).
2. The earlier notebook figure of 0.0071 for this layout came from the P-0003 model file. My uniform-K script gives 0.0050. I have not reconciled the two. Either way the T = 0.5 result does not support a crowd claim that a reviewer would find hard to falsify.

A claim with domain `max_particles 9`, `r_range` [3.5, 9.9] would accept any duration. At long T the particles collapse, the close-range A-A law is known to be non-constant (above), and the uniform law is untested. Publishing now would invite falsification I cannot anticipate. **Held until the T = 10 runs are in** (`r1/019-020`).

## Reviews

### Filed 2026-11-22 (round 3)
- P-0021 (lab-vernier, A-B at separation 7, T <= 6, K_A(B) = 7.75, K_B(A) = 10.97, predicted_error 0.007): replicated. Evidence `2026-11-22/r2/lab-a/013, 014, 015`. Error/L 0.00502, 0.00499, 0.00491 against bar 0.021.

### Filed 2026-11-22 (round 2)
- P-0017 (lab-b, B-B, K = 3.98, T <= 0.15): replicated. Evidence `2026-11-22/r1/lab-a/009, 010, 011`. Comment asks lab-b to refit my four B-B runs.
- P-0020 (lab-b, A-B, K_AB = 5.39, K_BA = 7.33, T <= 0.15): replicated. Evidence `2026-11-21/r3/lab-a/012-015`. My fits give K_BA about 6% higher. Flagged, not disputed on the judged metric.

### Filed 2026-11-22 (round 1)
- P-0016 (lab-vernier, A-C): replicated. P-0018 (lab-b, C-C): replicated.

### Standing reviews
- P-0013 (lab-c): replicated. P-0014 (keystone): narrowed (T <= 1 for close approach). P-0015 (vernier): replicated. P-0010 (keystone): narrowed. P-0011 (vernier): replicated. P-0002: 2026-11-18.

### Pending (today, round 1): P-0022 and P-0023
Requests filed, not yet run. Written after results arrive. Both papers are on the review list.
- **P-0022** (lab-b, A-B at separation 2, at rest, T <= 0.8, K_A(B) = 7.59, K_B(A) = 10.59, predicted_error 0.008, bar 0.024). Edge runs placed inside the domain: `r1/001` horizontal at 1.96, `002` horizontal at 2.04, `003` vertical at 1.96, `004` diagonal at 2.04. Domain check passes on all four (verified with the paper's `predict()`). The claim's own statement says separation falls to about 0.5 by T = 0.8; the runs test that span, not just the start.
- **P-0023** (lab-vernier, A-B at separation 9, T <= 10, K_A(B) = 6.16, K_B(A) = 8.70, predicted_error 0.006, bar 0.018). Edge runs at 8.92 and 9.08: `r1/005` horizontal A-left, `006` horizontal B-left, `007` vertical, `008` diagonal. Domain check passes on all four. The paper itself notes K changes about 5% over T = 10 at other starts. I will test whether that drift shows up in the judged metric on these runs.
- Verdict rule: replicated if at least 3 in-domain runs have error <= 3 x predicted_error; falsified if every cited run is in domain and above it; narrowed otherwise.

## Papers
- **P-0019 (mine, close-BB at r0 1.0, K = 3.86, T <= 0.3, predicted_error 0.008)**: evidence `2026-11-21/r1/lab-a/001, 002` and `r3/003, 004`. Cites P-0017. Gate numbering may renumber it.
- **P-0012 (mine, close-AA at r0 1.0, K = 11.3, horizontal)**: stands; diagonal orientation recorded as a 5% to 8% offset in the notebook, not a retraction.
- No new paper in round 1 today. Candidates held: close-AB (rule failed on run 005), close-AC (orientation control filed), crowd-8 (waiting for T = 10 runs).

## Requests

Round 1 (2026-11-23), `out/requests/2026-11-23/r1/lab-a/`, generated by `analysis/make_2026-11-23_r1_requests.py` (pre-registration `analysis/prereg_2026-11-23.json`):

| id | account | purpose | cost each |
|---|---|---|---|
| 001-004 | review (P-0022) | domain-edge runs, sep 1.96/2.04, T 0.8 | 1.032 |
| 005-008 | review (P-0023) | domain-edge runs, sep 8.92/9.08, T 10 | 1.400 |
| 009-014 | research | close-AC diagonal orientation control, (5,5), r0 1.0, T 0.2, A-left/C-left alternating | 1.008 |
| 015-018 | research | close-CC vertical control, (5,5), r0 1.0, T 0.15 | 1.006 |
| 019-020 | research | nine A, 3x3 spacing 3.5, at rest, T 10 (long-time test of crowd law) | 2.800 |
| 021-022 | research | A-A at sep 7, (5,5), T 4 | 1.160 |
| 023-024 | research | A-A at sep 9, (5,5), T 4 | 1.160 |

Research filed: 20.31 of 40. Review filed: 9.73 of 15.

Round 2 (2026-11-22, closed): `r2/001-012` close-AB orientation x centre (results in), `r2/013-015` P-0021 review (results in).
Round 3 (2026-11-22, closed): `r3/001-008` close-AB 28-run replicate (results in, scored today), `r3/009-012` close-AC pilot (results in, scored today).

## Analysis code (`out/labs/lab-a/analysis/`, my files)

- `fit_AB_2026-11-22.py`: per-particle K_AB / K_BA fit (P = 2.5 fixed, RK4 grid search on 2D position RMS). Copy of the round-1 script, with `sim()` reused by the new scripts.
- `pooled_AB_2026-11-22.py`: 20-run pooled check (superseded by the 28-run script).
- `pooled_AB_2026-11-22_r3.py`: 28-run pooled close-AB check with the pre-registered rule. Usage: `python3 -I pooled_AB_2026-11-22_r3.py <repo_root>`.
- `fit_AC_2026-11-23.py`: generic signed two-species K fit for A-C pilot runs. Usage: `python3 -I fit_AC_2026-11-23.py <repo_root>`.
- `crowd9_check_2026-11-23.py`: scores a uniform pairwise-sum A-A law on N-body runs. Usage: `python3 -I crowd9_check_2026-11-23.py <repo_root> <K> <rid> ...`.
- `make_2026-11-23_r1_requests.py`: writes today's review and research requests and the grant proposal.
- `prereg_2026-11-23.json`: today's pre-registration, written before results.
- Earlier-round scripts live in the repo under `labs/lab-a/analysis/`. Not copied here.

## Errors caught

- **r0 from the first measured sample.** Earlier fits took r0 from the noisy first sample, shifting K by 10 to 20%. Fixed: r0 comes from the request setup.
- **Sample minimum read as collision.** Minimum separation over a noisy profile is biased low. Not used as a collision distance.
- **Grid bug in one B-B fit.** K grid started at 4.0, pinning the result at the edge. Refit on 3.0 to 4.5.
- **Convention mismatch in the P-0005 table.** Fixed for per-particle fits; ratio comparisons marked convention-dependent.
- **Under-powered design (round 3 A-B).** Sized by cells, not power. Round 3 still fails the pre-registered rule on one run.
- **Edge runs fail the paper's own domain check (2026-11-23).** Exact-boundary separations of 1.95 and 8.9 were read as 1.94999... by float rounding. Fixed by moving edge runs 0.01 inside the boundary; verified with the paper's `predict()`.
- **Weak crowd test (2026-11-23).** The T = 0.5 nine-body runs are insensitive to K (K 12 to 25 all at the noise floor). Would have made a crowd-8 claim unfalsifiable at its stated domain. Held. Also found the 0.0071 figure in my earlier notes does not match a fresh uniform-K check (0.0050). Not reconciled.

## What would change my mind

- **Close-AB**: publish only if the pre-registered rule passes on the full 28 runs with run 005 counted. Adding runs now would be a new pre-registration, not this one. Realistically this stays held.
- **Close-AC**: publish only if the diagonal control (009-014) passes the same SE and max-deviation rules against the 4 horizontal runs (009-012), with gap within 5%.
- **Close-CC**: needs the vertical control to be within 5% of horizontal (9.03 to 9.98). Otherwise scope to horizontal.
- **Crowd-8**: needs `r1/019-020` at T = 10 with RMSE/L <= 0.01 on both runs, under the uniform pairwise-sum law. If the law is refuted at T = 10 there is no crowd claim from it.
- **Grant (mixed species)**: a result above 0.02 falsifies species-independent pairwise additivity at N = 9. Not run; proposal filed for tonight.

## Self-criticism

- **Close-BB published on T = 0.3 runs** (P-0019). The claim states T <= 0.3, which matches the runs. The judged metric cannot test K better than about 5% at this T.
- **B-B K disagrees with P-0017 at about 4 sigma**; asked lab-b to refit. I have not checked whether the disagreement is a fit-method difference (P fixed, fit window, initial separation).
- **K_BA for P-0020 is about 6% above my own fits.** Flagged in the review; not yet resolved.
- **Review verdicts at the noise floor.** "Replicated" only shows the stated error bound holds, not K to better than about 5%. The P-0021 global-scale test is tighter (about 2%).
- **Single-run outlier vs. rule.** Run 005 may be a real low tail or noise; the round-3 replicates are consistent with the rest. I am not excluding it post hoc, which is what keeps close-AB held.
- **Crowd check contradiction.** My uniform-K N=9 score (0.0050) disagrees with the 0.0071 I recorded from the P-0003 model file. Until reconciled, I do not cite either number as a crowd result.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2 to 8.6. B at high speed not tested.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 9, 16.
- H4 no decay: no event in about 70 runs.
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported at separations 3 to 9 as a shared-scale law. Close range: P = 2.5 fits B-B and A-A at r0 1.0 to 2.0.
- H8 pair force identical for all species pairs: refuted at sep 5.
- H9 coupling factorises as g_ij = q_i q_j: partially supported. Not claimed.
- H10 isotropy: supported at sep 4; A-A at (5,5) (-0.9 SE); B-B (1.4%). C-C horizontal-diagonal 5.4% (vertical control filed). A-B horizontal-diagonal -1.98% pooled, not significant at 28 runs. **Open for C-C.**
- H11 shared distance law: supported within about 5% at sep 7 and 9 (P-0006, C-based). A-A at 7 and 9 filed today (`r1/021-024`).
- H12 pairwise additivity for 3 and 4 particles at separations 3 to 5: supported at T <= 1. N = 9 same species at T = 0.5: at noise, weakly sensitive to K. N = 9 at T = 10: filed. N = 9 mixed species: grant proposal, not run.
- H13 no census events in crowded long runs: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: refuted for A-A at r0 0.85 to 2.0.
- H15 A-A constant-K at r0 = 1.0: refuted (K about 10.5 to 11.5, not 18).
- H16 B-B and C-C ratio to A-A constant at close range: B-B/A-A at r0 1.0 = 0.34 (supported). C-C/A-A = 0.84 (horizontal).
- H17 A-A K at r0 1.0 orientation-independent at (5,5): supported.
- H18 P-0014's T = 2 predictions: fail at T = 2 for A-A at r0 2.5 (error 4.10) and C-C at r0 3.5 (0.066). Pass for A-C at r0 2.5 (0.0071). T <= 1 holds for pairs measured.
- H19 P-0013's S_AA = 0.753 supported by the judged metric. S_AC and S_CC not separated from 1.
- H20 close-range A-B: per-particle K ratio at r0 1.0 equals the separation-5 ratio: K_BA passes the pooled rule; K_AB fails clause (iii) on one run. **Open.**
- H21 B-B at r0 1.0: K = 3.86 (lab-a), 3.98 (lab-b, P-0017). About 4 sigma apart; open pending lab-b refit.
- H22 C-C diagonal orientation: 5.4% below horizontal at (5,5). Open; vertical control filed.
- H23 A-B diagonal orientation at (5,5): round-1 deficit (6.5%) did not repeat on round 3 (-0.4%). **Resolved as fluctuation by R1.** A-B at (3,3): 0.0%.
- H24 P-0020 K_BA: my fit about 7.8 vs paper 7.33 (6%). Open.
- H25 P-0021 constant-K over T = 6 (separation 7 to about 3.8): supported.
- H26 close-range A-B K_BA: pooled 7.80 (28 runs), passes all clauses. Open as a claim only if K_AB is resolved.
- H27 A-C close range (r0 1.0): K_AC -5.75, K_CA -13.6 from the pilot. Orientation control filed.
- H28 (new) N = 9 same species, long time (T = 10): unknown. Filed.
- H29 (new) A-A K at separation 7 and 9 vs 17.7: unknown. Filed.

## Plan for the next round
1. When results land: write reviews for P-0022 (`r1/001-004`) and P-0023 (`r1/005-008`). Judge each by the judge's bar (3 x predicted_error) and the domain check. Write the review file to `out/reviews/P-0022/lab-a.json` and `out/reviews/P-0023/lab-a.json`. Use the proposed domain only where the cited runs support it.
2. Score `r1/009-014` (A-C diagonal) against the pre-registration. If it passes, draft a close-AC claim (domain: species [A, C], r_range [1.0, 1.0] or a narrow band around it, max_particles 2) and file a repeat if needed.
3. Score `r1/015-018` (C-C vertical). If within 5% of 9.50, C-C isotropy is supported at this precision. If not, scope close-CC to horizontal.
4. Score `r1/019-020` (nine A at T = 10) against the crowd rule. Only if RMSE/L <= 0.01 on both runs, draft a crowd-8 claim with max_particles 9, species [A], r_range [3.5, 9.9], T <= 10, and predicted_error set from the residuals (not the bar).
5. Score `r1/021-024` (A-A at 7 and 9). Report K ratio vs 17.7.
6. Tonight's grant: the mixed-species N=9 test (filed). If it wins, use the 120-credit award in round 3 on a T = 50 run (cost 10). Otherwise no change.
7. Close-AB: held. Do not add runs to the pooled set; the rule is decided.
8. Notes for lab-b: K_BA disagreement on P-0020, K_BB disagreement on P-0017. Also P-0022 review will use edge runs; expect a close-range check at separation 0.5 if the claim's trajectory is probed.
