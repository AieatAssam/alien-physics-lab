# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Budget ledger

### Closed days
- 2026-11-17: research used 23.30 of 40; review 6.00.
- 2026-11-18: research used 30.38 of 40; review 6.20 (review of P-0002).
- 2026-11-19: research used 13.12 of 40; grant award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Voted lab-keystone.
- 2026-11-20: research used 9.19 of 40; review 13.90 of 15 (`r1/005-009` on P-0008; `r3/006-012` on P-0010 and P-0011); grant 1.02 of 120 (`r3/001`, C-C at r0 2). Voted lab-keystone.

### 2026-11-21 (round 3, today)
- Research: 13.11 used at round-3 start (round 1 9.07, round 2 4.02); 26.89 left.
- Round 3 filed (all research unless noted): `002` repeat of grant main event (1.09), `003-006` B-B and C-C diagonal controls (4.04), `007-011` A-A (5.03), `012-015` A-B (4.02), `019-022` A-A (4.02). Total 18.20. Research left after filing: 8.69. Unused research credits do not roll over, so the 8.69 lapses at day end unless the protocol changes this.
- Review: 9.36 of 15 used on `r2/005-013` (P-0013, P-0014, P-0015). Round 3 files `016-018` on P-0016 (3.07). Review used 12.43 of 15; 2.57 left.
- Grant: award 120, proposal (9 A on a 3x3 grid, spacing 3.5, T 0.5) costs 1.09 as filed. Grant main event `001` filed (1.09). **118.91 of the award will lapse unused.** I did not enlarge the main event: the proposal that won the vote is the pre-registered 1.1-credit design, and a larger run would be a different, unregistered experiment. Flag for the operator if credits should carry over.
- Vote: `grants/2026-11-21/votes/lab-a.json` votes lab-vernier (round 2, filed earlier).

## Established (accepted-level claims, or runs I trust)

Pair coefficients at separation 5 (P-0005, accepted; K_XY = acceleration coefficient of species X toward Y, P = 2.5):

| pair | K (species in first slot, on the second) | runs | status |
|---|---|---|---|
| A-A | 18.0 | P-0003 (domain sep 3 to 6) | established at sep 3 to 6; not valid at sep 1 (see below) |
| A-B | 8.99 (A on B), 12.34 (B on A) | replicated | |
| A-C | -8.77 (A on C), -21.25 (C on A) | replicated, repulsion | |
| B-B | 6.12 | 4 values, spread about 9% | |
| C-C | 12.36 | 4 values, spread about 5% | |
| B-C | -6.10 (B on C), -10.59 (C on B) | pre-registered prediction passed | |

Other established results:
- Free flight with specular walls (P-0001, P-0002): A, B, C at speeds up to 8.6, T up to 100, corner hits. Supported.
- Isotropy at separation 4 (A-A along diagonal, y, horizontal): K = 17.67, 17.71, 17.70. Supported at sep 4 (not at sep 1, see below).
- Pairwise additivity for three and four particles at separations 3 to 5 (T <= 1): at noise level.
- Shared distance law at separations 7 and 9 (P-0006): within about 5%, qualified by the close-range results.
- No census event (decay or appearance) in about 70 runs, including 16 particles at T = 100.
- Cost law cost = 1 + 0.02 N T: supported at N = 1, 2, 3, 4, 16 (round-2 costs match to 0.001). Not yet checked at N = 9; the grant request `001` (cost 1.09 as priced) will check it.
- Noise: tracker noise on separation sd about 0.07 (about 0.05 per coordinate). Single-particle free-flight runs give error/L 0.0068 to 0.0073 against any exact model. **0.007 is the noise floor of the judged metric.** Any claimed error below about 0.007 cannot be confirmed by a single run.

## Close range

### A-A at r0 = 1.0: orientation and position (round-2 control, 2026-11-21)
K fits: one coefficient K, P = 2.5 fixed, least squares on the separation profile, initial separation from the request setup. Method in `out/labs/lab-a/analysis/fit_r2_2026-11-21.py`. Per-run sd of K is about 0.33 (about 3%).

| run | orientation, centre | r0 | T | K_fit (1 sigma) |
|---|---|---|---|---|
| 2026-11-21/r2/lab-a/001 | horizontal, (3,3) | 1.0 | 0.15 | 10.87 (+-0.33) |
| 2026-11-21/r2/lab-a/002 | diagonal, (5,5) | 1.0 | 0.15 | 10.65 (+-0.32) |
| 2026-11-21/r2/lab-a/003 | diagonal, (3,3) | 1.0 | 0.15 | 10.64 (+-0.33) |
| 2026-11-21/r2/lab-a/004 | horizontal, (5,5) | 1.25 | 0.15 | 12.60 (+-0.64) |
| 2026-11-21/r1/lab-a/009 | diagonal, (3,3) | 1.0 | 0.15 | 10.35 (+-0.3), round 1 |
| 2026-11-20/r3/lab-a/003, 004 | horizontal, (5,5) | 1.0 | 0.15 | 11.52, 11.05 |
| 2026-11-21/r1/lab-a/005-008 | horizontal, (5,5) | 1.25, 0.85 | 0.12-0.15 | 11.55, 13.25, 10.55, 10.00 |

Round-2 pre-registration outcomes:
- `002` (diagonal, (5,5)) 10.65 against pre-registered 11.3 (about 2 sigma low). The prediction "near 11.3 if orientation does not matter" is not met at 2 sigma.
- `001` (horizontal, (3,3)) 10.87 against 11.3 (1.3 sigma low). Not significant.
- `003` (diagonal repeat at (3,3)) 10.64, consistent with round-1 `r1/009` at 10.35 (within 1 sigma of the pooled spread). The diagonal result reproduces.
- `004` (A-A r0 1.25) 12.60 against 12.5 (within 5%). Passes; the r0 = 1.25 point is resolved at 12.5 to 12.6.

Reading: at (5,5) the diagonal run sits about 0.6 below the horizontal pair (about 1.5 to 2 sigma). At (3,3) the horizontal run is about 0.4 below the (5,5) horizontal pair. So orientation and position each look like a few-percent effect, and neither is separated. **The A-A K at r0 1.0 scatters between 10.35 and 11.5 across runs, with a possible few-percent effect from orientation or position. Not resolved.** Four runs per arm is too few: a 5% effect needs about six runs per arm at 3% scatter (I sized round 2 by the number of cells, not by the scatter; see self-criticism).

Round-3 `007-011, 019-022` add A-A runs at (5,5) so that each orientation has six runs (horizontal: 2026-11-20/r3/003-004 plus 2026-11-21/r3/007, 008, 019, 020; diagonal: 2026-11-21/r2/002 plus r3/009, 010, 011, 021, 022). Pre-registered rule in `out/labs/lab-a/analysis/pred_2026-11-21_r3.json`.

### A-A is not constant-K below separation 2 (round 1 table, still valid)

| run | pair | orientation / centre | r0 | T | K_fit |
|---|---|---|---|---|---|
| 2026-11-20/r1/lab-a/001, 002 | A-A | horizontal, (5,5) | 2.0 | 0.5 | 15.6 (both) |
| 2026-11-20/r1/lab-a/003 | A-A | horizontal, (5,5) | 1.5 | 0.3 | 14.0 |
| 2026-11-20/r3/lab-a/003, 004 | A-A | horizontal, (5,5) | 1.0 | 0.15 | 11.52, 11.05 |
| 2026-11-21/r1/lab-a/005, 006 | A-A | horizontal, (5,5) | 1.25 | 0.15 | 11.55, 13.25 |
| 2026-11-21/r1/lab-a/007, 008 | A-A | horizontal, (5,5) | 0.85 | 0.12 | 10.55, 10.00 |

- K_eff(r0), P = 2.5 fixed: about 10.3 at r0 = 0.85; 10.3 to 11.5 at r0 = 1.0; 12.4 at 1.25; 14.0 at 1.5; 15.6 at 2.0; 17.7 at 4; 18.0 at 5. Not constant below separation 3.
- P-0003 (A-A, domain separation 3 to 6, K = 18.0) is not contradicted: its domain excludes these runs.
- The power-law shape is not tested below r0 = 1: the separation changes only about 0.2 in T = 0.15, so P and K are not separately determined.

### B-B and C-C at r0 = 1.0 (replicated, orientation control pending)
- B-B horizontal (5,5): K 3.82, 3.84 (round 1, +-0.05 each). Ratio to A-A(1.0) horizontal 0.34.
- C-C horizontal (5,5): K 9.43, 9.56 (round 1, +-0.3 each). Ratio to A-A(1.0) horizontal 0.84.
- Round 3 `003-004` (B-B) and `005-006` (C-C) are the diagonal controls at (5,5). These are the first test of orientation for these species. B-B K has ±0.05 precision, so the B-B control has real power.

### B-B at r0 = 2 and C-C deviation from 12.36 (unchanged)
- B-B at r0 2: pooled K about 5.56 (about 9% below 6.12). Not published.
- C-C at r0 3: K 13.05 and 13.13 (about 6% above 12.36). C-C at r0 2: 12.0. C-C at r0 1.0: 9.5. So K_CC falls steeply at close range.

### Round-2 review evidence (P-0014 at T = 2)
- `r2/008` A-A r0 2.5, T = 2: P-0014 error 4.10. Model output diverges. I did not check whether the real pair also comes close within T = 2.
- `r2/010` C-C r0 3.5, T = 2: P-0014 error 0.066 (fail against 0.039).
- `r2/009` A-C r0 2.5, T = 2: P-0014 error 0.0071 (pass).
- Consistent with the C-C coefficient drifting by a few percent with separation (C-C at r0 3 gave 13.1, 6% above 12.36).

### Publication status for close-range claims
- **P-0012 (close-AA, mine, filed 2026-11-20)**: K = 11.3 at r0 = 1.0 from two horizontal runs at (5,5). Its domain (species A, r0 exactly 1.0, max 2) does not state orientation. The diagonal K (10.65, 10.35 to 10.64) is 5% to 8% below 11.3. At T <= 0.15 that is about 0.0015 error/L by the earlier estimate, inside its predicted_error of 0.008. P-0012 stands; the orientation point is recorded here, not as a retraction.
- **close-BB and close-CC: held one more round.** The rule is: two replicates agree within 5% AND the orientation control passes. Horizontal replicates agree (B-B within 0.5%, C-C within 1.5%). The diagonal control has not been run. Round 3 `003-006` run it; publish next round if the pre-registered rule passes.
- **close-AB** (open bounty): no data until round 3 `012-015`. Per-particle fit (K_AB on A, K_BA on B). Pre-registered publication rule in `pred_2026-11-21_r3.json`.
- **close-AC**: covered by P-0016 (Vernier). Not competing; reviewing it (see below).
- **close-BC**: covered by P-0015 (Vernier). Not competing.

## Reviews

### Filed this round (2026-11-21, round 3)
- **P-0013 (lab-c, A/C at r0 1.5, T <= 0.4): replicated.** Evidence `2026-11-20/r1/lab-a/003`, `2026-11-21/r2/lab-a/005, 006, 007`. Errors/L 0.0069 to 0.0072 against 0.030. Caveat: with the scales set to 1 the A-A run fails (0.093), so S_AA is supported, but the unscaled A-C (0.0078) and C-C (0.0076) runs still pass. The metric cannot tell S_AC and S_CC from 1. Written in `out/reviews/P-0013/lab-a.json`.
- **P-0014 (lab-keystone, A/C at r0 2.5 to 3.5, T <= 2): narrowed in time.** Evidence: `2026-11-17/r3/lab-a/001, 002`, `2026-11-20/r2/lab-a/001`, `2026-11-20/r3/lab-a/002`, `2026-11-21/r2/lab-a/008, 009, 010`. T = 1 runs pass (0.0068 to 0.0077). T = 2 A-C passes (0.0071). T = 2 A-A at r0 2.5 fails (4.10) and C-C at r0 3.5 fails (0.066). Stated as T <= 1 in the comment (the domain has no time field). Written in `out/reviews/P-0014/lab-a.json`.
- **P-0015 (lab-vernier, B-C at r0 1.000, T <= 0.6): replicated.** Evidence `2026-11-21/r2/lab-a/011, 012, 013`. Errors/L 0.0071 to 0.0072 against 0.015. Two caveats: the claim's predicted_error 0.005 is below our noise floor (0.007), and the machine-readable species list (B, C) puts B-B and C-C pairs in domain, where the predictor raises ValueError. Those runs (`2026-11-21/r1/lab-a/001-004`) are not cited. Written in `out/reviews/P-0015/lab-a.json`.

### Pending
- **P-0016 (lab-vernier, A-C at r0 1.000, T <= 0.6, predicted_error 0.006, bar 0.018).** Runs `2026-11-21/r3/lab-a/016` (A left, horizontal), `017` (C left, horizontal; checks K_AC vs K_CA), `018` (diagonal). All at T = 0.6, the claim's time edge. Verdict next round by the pre-registered rule in `pred_2026-11-21_r3.json`. Note the error floor: a 0.006 predicted_error is below our noise floor (0.007), so the review can confirm only the 3x bar.
- Review account left after P-0016 filing: 2.57.

### Standing reviews
- P-0010 (keystone): narrowed (T <= 1 for close approach). `2026-11-20/r3/lab-a/006-009`.
- P-0011 (vernier): replicated. `2026-11-20/r3/lab-a/010-012`.
- P-0002: 2026-11-18.

## Round-3 requests (filed today)

All under `out/requests/2026-11-21/r3/lab-a/`, validated against `protocol/request.schema.json` (manual check; jsonschema is not installed here).

| id | account | purpose | cost |
|---|---|---|---|
| 001 | grant | grant main event: 9 A, 3x3, spacing 3.5, at rest, T 0.5 (pre-registered) | 1.09 |
| 002 | research | repeat of 001 | 1.09 |
| 003, 004 | research | B-B diagonal, (5,5), r0 1.0, T 0.3 (orientation control) | 1.012 each |
| 005, 006 | research | C-C diagonal, (5,5), r0 1.0, T 0.15 (orientation control) | 1.006 each |
| 007, 008 | research | A-A horizontal, (5,5), r0 1.0, T 0.15 | 1.006 each |
| 009, 010, 011 | research | A-A diagonal, (5,5), r0 1.0, T 0.15 | 1.006 each |
| 012, 013 | research | A-B horizontal, (5,5), r0 1.0 (A-left, B-left) | 1.006 each |
| 014, 015 | research | A-B diagonal, (5,5), r0 1.0 | 1.006 each |
| 016, 017, 018 | review (cites P-0016) | A-C r0 1.0, T 0.6: horizontal (A left), horizontal (C left), diagonal | 1.024 each |
| 019, 020 | research | A-A horizontal, (5,5), r0 1.0 | 1.006 each |
| 021, 022 | research | A-A diagonal, (5,5), r0 1.0 | 1.006 each |

Grant main event result is needed before round-3 grant analysis. Pre-registration is in `out/labs/lab-a/analysis/pred_2026-11-21_r3.json`. The grant rule (from the proposal and `make_2026-11-21_grant.py`): RMSE/L <= 0.01 supports pairwise additivity at N = 9; > 0.02 refutes.

## Analysis code (`out/labs/lab-a/analysis/`, my files)

- `fit_r2_2026-11-21.py`: separation-profile fits for `r2/001-004` (K, sd, closest measured separation). Usage: `python3 -I fit_r2_2026-11-21.py <repo_root>`.
- `score_reviews_2026-11-21.py`: RMSE/L of paper models vs my in-domain runs, P-0013 unscaled check, P-0015 machine-domain check (raises on B-B). Usage: `python3 -I score_reviews_2026-11-21.py <repo_root>`.
- `make_2026-11-21_r3_requests.py`: writes `r3/001-022` request files.
- `pred_2026-11-21_r3.json`: pre-registration for round 3 (written before any round-3 result).
- Earlier scripts (round 1 and before, plus `review_check_2026-11-21.py`, `fit_r1_2026-11-21.py`, `make_2026-11-21_grant.py`) are in `labs/lab-a/analysis/` in the repo.

## Errors caught

- **r0 from the first measured sample.** Earlier fits took r0 from the noisy first sample (noise about 0.07), shifting K by 10 to 20%. Fixed: r0 comes from the request setup.
- **Sample minimum read as collision.** Minimum separation over a noisy profile is biased low (r2/008 sample minimum 0.047 is noise). Not used as a collision distance; model minimum is used when needed.
- **Grid bug in one fit (round 1).** The first B-B fit's K grid started at 4.0, pinning the result at the edge. Refit on 3.0 to 4.5 gives 3.82 and 3.84.
- **Model-vs-model divergence (P-0014).** P-0014's model output diverges for A-A at r0 2.5, T = 2 (error 4.10). I have not checked whether the measured pair also comes close within T = 2 (the sample minimum 0.047 is noise-biased, so it does not settle it). Stated as such in the review.
- **P-0015 machine domain.** The species list [B, C] contains B-B and C-C pairs, which the predictor rejects. Flagged in the review, not cited.

## What would change my mind

- Round-3 `003-006` (B-B and C-C diagonal) within 5% of the horizontal means (B-B 3.83, C-C 9.50): close-BB and close-CC are publishable with orientation scope not stated; if not, scope them to horizontal orientation only.
- Round-3 A-A six vs six at (5,5): difference less than 2 SE supports no orientation effect (then the round-2 deficit was a fluctuation). Difference more than 2 SE, diagonal lower: A-A K at r0 1.0 is orientation-dependent; P-0012 scope needs an orientation note.
- Grant `001` RMSE/L <= 0.01 and `002` agrees: additivity at N = 9 supported at T = 0.5. Between 0.01 and 0.02: ambiguous, repeat with longer T before claiming. Above 0.02: pairwise sum or flat K fails at spacing 3.5 to 7.
- A-B ratio K_AB/K_BA at r0 1.0 within 5% of 0.728 (the separation-5 ratio): the close range has a common radial shape; not within 5%: species-specific shape at close range.
- P-0016 `016-018`: all three within 0.018 => replicated. All above => falsified (all three are in domain). Mixed => narrowed, with the failing ordering or orientation named.

## Self-criticism

- **Round-2 orientation design was too small.** Two runs per cell cannot resolve the few-percent effect at 3% per-run scatter. I sized the round by the number of cells, not by the power needed. Round 3 uses six runs per arm, and I should have done this in round 2.
- **Grant under-use.** The award is 120 credits and the proposal costs 1.1. I did not enlarge the main event (it is the pre-registered design). This leaves almost all of the award unused. The operator should know.
- **Reviews are narrower than the paper claims where they had to be.** P-0013's S_AC and S_CC are not tested by the metric; P-0014's T = 2 claim fails for two of its seven runs; P-0015's predicted_error is below the noise floor. Each is said in the review. I chose "replicated" for P-0013 and P-0015 because the rule is met, and "narrowed" for P-0014 because two in-domain runs fail the bar.
- **Close-BB and close-CC held a second round.** The hold is the right call under my own rule; the cost is that two bounties (2 each) stay open a little longer.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2 to 8.6. Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 16. N = 9 pending grant `001`.
- H4 no decay: no event in any run to date (about 70 runs).
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported at separations 3 to 9 as a shared-scale law. Close range (1.0 to 2): P = 2.5 fits the shape, strength lower for A-A (H14). P not tested at r0 = 1.0 alone.
- H8 pair force identical for all species pairs: refuted at sep 5.
- H9 coupling factorises as g_ij = q_i q_j: partially supported. C-C misses at sep 5 by about 20%; at r0 1.0 the ratio to A-A is 0.84. Not claimed.
- H10 isotropy: supported at separation 4. **Open at r0 = 1.0**: diagonal runs about 0.6 below horizontal at (5,5) (1.5 to 2 sigma). Round-3 `007-011, 019-022` test it at six runs per arm.
- H11 shared distance law: supported within about 5% at sep 7 and 9 (P-0006).
- H12 pairwise additivity for 3 and 4 particles at separations 3 to 5: supported at T <= 1. N = 9 at spacing 3.5: pending grant `001`.
- H13 no census events in crowded long runs: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: refuted for A-A at r0 = 0.85 to 2.0 (K 10.3 to 15.6 vs 18).
- H15 A-A constant-K at r0 = 1.0: refuted (K about 10.5 to 11.5, not 18).
- H16 B-B and C-C ratio to A-A constant at close range: B-B/A-A at r0 1.0 = 0.34 (pre-reg 0.35, inside 10%). C-C/A-A = 0.84. Supported at r0 = 1.0 with horizontal orientation. Diagonal control pending (round 3 `003-006`).
- H17 A-A K at r0 1.0 is orientation- and position-independent: **open**. Round 2 gave a 1.5 to 2 sigma diagonal deficit and a 1.3 sigma (3,3) horizontal deficit. Round 3 powers it.
- H18 P-0014's T = 2 predictions: **resolved in part.** Fails at T = 2 for A-A at r0 2.5 (error 4.10) and C-C at r0 3.5 (0.066). Passes for A-C at r0 2.5 (0.0071). T <= 1 holds for the pairs measured.
- H19 (new) P-0013's S_AA = 0.753 is supported by the judged metric. S_AC and S_CC are not separated from 1 by the metric (unscaled runs pass).
- H20 (new) Close-range A-B: per-particle K ratio at r0 1.0 equals the separation-5 ratio 0.728 (shape separable). Round-3 `012-015`.

## Papers
- P-0003 (A-A power law, domain separation 3 to 6, T up to 2): not falsified. Its domain excludes the close-range runs.
- P-0005, P-0006, P-0007, P-0009: accepted or other labs' papers as recorded in the scoreboard.
- P-0012 (mine, filed 2026-11-20): close-range A-A at r0 = 1.0, K = 11.3, horizontal orientation (orientation not in its stated domain; diagonal K 5 to 8% lower, inside its error bar at T <= 0.15). Pending gate numbering and reviews.
- No new paper filed this round. close-BB, close-CC held (orientation control in round 3). close-AB after round-3 `012-015`.

## Plan for the next round
1. Read `results/2026-11-21/r3/lab-a/001-022`. Check costs against the estimates above.
2. Grant `001` vs the pre-registered pairwise-sum model (`analysis/make_2026-11-21_grant.py`), with `002` as the independent repeat.
3. B-B and C-C diagonal (`003-006`): compare with the horizontal means (3.83, 9.50) against 5%. If passes, file close-BB and close-CC with domain r_range [0.99, 1.01], species B and C respectively, max_particles 2, predicted_error from the observed scatter (not below 0.007).
4. A-A (5,5) six vs six (`007-011, 019-022`): apply the pre-registered 2 SE rule. Report the result either way; set P-0012's scope note accordingly.
5. A-B per-particle fits (`012-015`): publish close-AB only if the rule in `pred_2026-11-21_r3.json` passes.
6. P-0016 verdict from `016-018` by the pre-registered rule. File the review (review account, 3.07 spent; 2.57 left).
7. No new research beyond these unless a result forces it. Research left after round 3 is 8.69 and lapses at day end.
