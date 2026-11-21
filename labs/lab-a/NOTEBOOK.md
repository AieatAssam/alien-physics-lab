# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Budget ledger

### Closed days
- 2026-11-17: research used 23.30 of 40; review 6.00.
- 2026-11-18: research used 30.38 of 40; review 6.20 (review of P-0002).
- 2026-11-19: research used 13.12 of 40; grant award 120, spent 33.00 on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Voted lab-keystone.
- 2026-11-20: research used 9.19 of 40; review 13.90 of 15 (`r1/005-009` on P-0008; `r3/006-012` on P-0010 and P-0011); grant 1.02 of 120 (`r3/001`, C-C at r0 2). Voted lab-keystone.

### 2026-11-21
- Round 1: nine research requests `r1/001-009`, all run. Costs 1.00 to 1.01 each (cost = 1 + 0.02 N T confirmed again). Research used 9.07 of 40; `budget_remaining` on the last result 30.93.
- Round 2 (this round), filed:
  - Research `r2/001-004` (A-A close control and replicate): 4 x 1.006 = 4.02 of the 30.93 left.
  - Review `r2/005-013` (cites P-0013, P-0014, P-0015): 3 x 1.016 + 3 x 1.080 + 3 x 1.024 = 9.36 of 15.
- Grant: our proposal (9 A particles, 3x3 grid, spacing 3.5, `grants/2026-11-21/proposals/lab-a.json`) was filed in round 1. Award status is unknown until tomorrow. Grant allowance today is 0.
- Vote: `grants/2026-11-21/votes/lab-a.json` votes **lab-vernier** (8-body grid minus centre, all pairs at 3.5 or more, T = 2, with a no-force control). Reason is within 300 characters.

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
- Isotropy at separation 4 (A-A along diagonal, y, horizontal): K = 17.67, 17.71, 17.70. Supported at sep 4 (not at sep 1, see the new diagonal result below).
- Pairwise additivity for three and four particles at separations 3 to 5 (T <= 1): at noise level.
- Shared distance law at separations 7 and 9 (P-0006): within about 5%, qualified by the close-range results.
- No census event (decay or appearance) in about 60 runs, including 16 particles at T = 100.
- Cost law cost = 1 + 0.02 N T: supported at N = 1, 2, 3, 4, 16.

## Close range

### A-A is not constant-K below separation 2
K fits: one coefficient K, P = 2.5 fixed, least squares on the measured separation profile. Initial separation from the request setup, never from a noisy sample. Noise sd on separation is 0.0707.

| run | pair | orientation / centre | r0 | T | K_fit | 1-sigma (chi2 +1) |
|---|---|---|---|---|---|---|
| 2026-11-20/r1/lab-a/001, 002 | A-A | horizontal, (5,5) | 2.0 | 0.5 | 15.6 (both) | |
| 2026-11-20/r1/lab-a/003 | A-A | horizontal, (5,5) | 1.5 | 0.3 | 14.0 | |
| 2026-11-20/r3/lab-a/003, 004 | A-A | horizontal, (5,5) | 1.0 | 0.15 | 11.52, 11.05 | |
| 2026-11-21/r1/lab-a/005 | A-A | horizontal, (5,5) | 1.25 | 0.15 | 11.55 | +-0.6 (5%) |
| 2026-11-21/r1/lab-a/006 | A-A | horizontal, (5,5) | 1.25 | 0.15 | 13.25 | +-0.6 (4.5%) |
| 2026-11-21/r1/lab-a/007 | A-A | horizontal, (5,5) | 0.85 | 0.12 | 10.55 | +-0.4 (3.6%) |
| 2026-11-21/r1/lab-a/008 | A-A | horizontal, (5,5) | 0.85 | 0.12 | 10.00 | +-0.4 (3.8%) |
| 2026-11-21/r1/lab-a/009 | A-A | **diagonal, (3,3)** | 1.0 | 0.15 | 10.35 | +-0.3 (2.9%) |

- The r0 = 1.0 horizontal pair (2026-11-20/r3 003, 004) agree to 4%. The diagonal run at (3,3) sits about 3 sigma below their mean (11.29): the orientation or position control is in `r2/001-003`.
- K_eff(r0) for A-A, P = 2.5 fixed: about 10.3 at r0 = 0.85, 10.3 to 11.3 at r0 = 1.0 (horizontal 11.29, diagonal 10.35), 12.4 at 1.25 (two runs 11.55 and 13.25, about 2 sigma apart), 14.0 at 1.5, 15.6 at 2.0, 17.7 at 4, 18.0 at 5. Not constant below separation 3.
- The power-law shape is not tested below r0 = 1: the separation changes only about 0.2 in T = 0.15, so P and K are not separately determined.
- P-0003 (A-A, domain separation 3 to 6, K = 18.0) is not contradicted: its domain excludes these runs.

### Round-1 results against the pre-registered rules (written before results)

| run | pair | r0 | pre-registered band | K_fit (1 sigma) | verdict |
|---|---|---|---|---|---|
| r1/001, 002 | B-B | 1.0 | 4.0 within 10% | 3.82, 3.84 (+-0.05 each) | inside: ratio to A-A(1.0) = 0.34 |
| r1/003, 004 | C-C | 1.0 | [8.0, 9.6] | 9.43, 9.56 (+-0.3 each) | inside: ratio 0.84 to A-A(1.0) |
| r1/005, 006 | A-A | 1.25 | 12.5 within 5% | 11.55, 13.25 | mean 12.4 inside; the two runs are about 2 sigma apart. Third replicate in r2/004 |
| r1/007, 008 | A-A | 0.85 | [9.5, 11.5] | 10.55, 10.00 | both inside |
| r1/009 | A-A | 1.0, diagonal, (3,3) | 11.3 within 5% | 10.35 (-8%) | **outside**. Orientation or position effect, or a 3-sigma fluctuation. Control in r2/001-003 |

Result of the round-1 close-range batch: B-B and C-C at r0 = 1.0 replicate (ratio to A-A about 0.34 and 0.84). The A-A K at r0 1.0 depends on orientation or position at the 8% level, which is the new open question.

### Publication status for close-range claims
- **P-0012 (close-AA, mine, filed 2026-11-20)**: K = 11.3 at r0 = 1.0 from two horizontal runs at (5,5). The horizontal orientation is not in its stated domain. If the diagonal effect is real, P-0012's K is orientation-dependent. Its predicted error (0.008) is not threatened by an 8% K shift at T = 0.15 (estimated contribution about 0.0015 to error/L), so it is not falsifiable by the bar, but its scope must be stated.
- **close-BB and close-CC**: B-B (3.83) and C-C (9.50) at r0 = 1.0 each replicate within 1.5%. I am **holding** these claims until `r2/001-003` settle whether orientation matters. The rule for publishing: two replicates agree within 5% and the orientation control passes.
- **close-AB, close-AC, close-BC**: mixed pairs need per-particle K fits (K_ij and K_ji separately). Not attempted. close-BC is covered by Vernier's P-0015 if accepted; do not compete on the same runs.

### Noise extremes, not collisions
Minimum separation over a noisy profile is biased low. Do not read a sample minimum as a collision distance. Use the model's own minimum.

### B-B at r0 = 2 (replicated, about 9% below the separation-5 value)
K_fit 5.70 (2026-11-20/r1/004) and 5.42 (r3/005): pooled about 5.56 (about 9% below 6.12). No claim published (replicate only at the edge of the pre-registered 5% rule).

### C-C: deviation from 12.36 across separations 2 to 5 (not monotonic, not established as flat at 5%)
- r2/001 at r0 3: K 13.05; r3/002 (replicate) 13.13. Both about 6% above 12.36. Inconclusive between the 5% and 10% bounds.
- r3/001 at r0 2: K 12.0. Single run.
- Round-1 C-C at r0 1.0: 9.50. So K_CC falls from about 13 at r0 3 to about 9.5 at r0 1, a steeper radial shape than the separation-5 table implies.

## Reviews

### Filed earlier
- **P-0010** (lab-keystone): narrowed. Evidence `2026-11-20/r3/lab-a/006-009`. Bulk runs replicate (error/L 0.0071 to 0.0077 vs bar 0.03). Run 009 (A-A r0 6, T 6) fails (error/L 0.195; pair passes through itself at min separation 0.028). Narrowing stated in comment: exclude pairs approaching closer than about 1 within T = 6.
- **P-0011** (lab-vernier): replicated. Evidence `2026-11-20/r3/lab-a/010-012`, error/L 0.0071 to 0.0072 vs bar 0.015.
- **P-0002** review filed 2026-11-18 (see `out/reviews` in the repo).

### Pending reviews (filed this round as requests; verdicts after results)
Requests are on file under `out/requests/2026-11-21/r2/lab-a/`. I will read the results in the next round and then file the reviews. A review cannot cite runs whose results do not exist yet.

**P-0013 (lab-c, A/C at r0 1.45 to 1.55, T <= 0.4, S_AA 0.753, S_AC 0.811, S_CC 0.874)**
- My in-domain evidence today: only `2026-11-20/r1/lab-a/003` (A-A, r0 1.5, T 0.3), error/L 0.0071 vs bar 0.03. Not enough for "replicated" (needs 3).
- Pending: `r2/005` (A-A), `r2/006` (A-C), `r2/007` (C-C), all at r0 1.5, T 0.4. Note: P-0013's own remark says the judged metric does not separate its scales from the unscaled P-0008 coefficients for A-C and C-C. My review should say so if the runs agree.

**P-0014 (lab-keystone, A/C at r0 2.5 to 3.5, T <= 2, no radial factor)**
- My in-domain evidence today: `2026-11-17/r3/lab-a/001, 002` (A-A r0 3, T 1), `2026-11-20/r2/lab-a/001` and `r3/002` (C-C r0 3, T 1). All four error/L 0.0068 to 0.0077 vs bar 0.039. These pass, but all are at T = 1, while the claim says T up to 2.
- Important: P-0003's model (K = 17.7) matches my A-A runs at T = 2 (`2026-11-17/r3/lab-a/003, 004`, r0 4) with error 0.0072 and 0.0079. P-0014's model (K = 18.0, same integrator) gives 0.0235 on the same runs. The 0.3 difference in K becomes a 0.02 error at T = 2 because the pair comes close (closest approach about 0.14). So the claim's T = 2 is sensitive to the K choice.
- My own model check (not evidence): the P-0014 model passes A-A at r0 3 through itself to min separation 0.27 at T = 2 and then diverges (positions near 3e4). The real simulator does not do this in the separation 3 to 6 runs (P-0003 matches). The edge runs `r2/008-010` test this at the claim's T limit.
- Pending: `r2/008` (A-A r0 2.5, T 2), `r2/009` (A-C r0 2.5, T 2), `r2/010` (C-C r0 3.5, T 2). Likely outcome to test: "narrowed" in T, not "falsified". Decide on the data.

**P-0015 (lab-vernier, B-C at r0 1.000 +- 0.001, T <= 0.6, K_BC -4.32, K_CB -7.31)**
- My in-domain pair evidence today: **none**. The only lab-a runs that fall in its domain are single-particle runs (`2026-11-17/r3/lab-a/009`, `2026-11-20/r3/lab-a/011`, and others). With N = 1 there are no pairs, so they test nothing about the pair law; I will not cite them.
- Pending: `r2/011` (horizontal, B on the left), `r2/012` (diagonal, B at lower left), `r2/013` (vertical, C first). All at r0 1.0, T 0.6, centred (5,5).

Review account: 9.36 of 15 used on these requests. Review allowance remaining after this round: 5.64 (none for later reviews unless I add runs).

## Round-2 pre-registration (written before any round-2 result)

Research `r2/001-004` (A-A close control, same rules as round 1):
- **001** A-A r0 1.0, horizontal, centred (3,3). Prediction: K 11.3 if orientation and position do not matter. Rule: K within 1 sigma (about 0.3) of 11.3 supports orientation independence at (3,3). If K sits near 10.35 with horizontal runs at 11.3, the diagonal deficit is a position effect (at (3,3)), not orientation.
- **002** A-A r0 1.0, diagonal, centred (5,5). Prediction: K near 11.3 if orientation does not matter; near 10.35 if the diagonal itself is the cause.
- **003** repeat of r1/009 (diagonal, centred (3,3)). Prediction: K near 10.35. Rule: repeat within 1 sigma of 10.35 counts the diagonal result as reproducible. Together with 001 and 002 the 2x2 (orientation x position) is resolved.
- **004** A-A r0 1.25, horizontal, centred (5,5), third run. Rule: K mean of the three runs at 1.25 within 5% of 12.5 supports the interpolation; a third value outside 12.5 +- 1 sigma leaves the r0 = 1.25 point unresolved.

Review `r2/005-013`: described in the table above; pre-registered in the script `analysis/make_2026-11-21_r2_requests.py`.

## Analysis code (`out/labs/lab-a/analysis/`, my files)

- `review_check_2026-11-21.py`: lists every lab-a result on disk with setup and in-domain status for P-0013, P-0014, P-0015, and each paper model's error/L. Usage: `python3 -I review_check_2026-11-21.py <repo_root>`.
- `fit_r1_2026-11-21.py`: separation-profile fits (K, P = 2.5 fixed) for round-1 runs `r1/001-009` against the pre-registered bands.
- `make_2026-11-21_r2_requests.py`: writes `r2/001-013` request files.
- `make_2026-11-21_grant.py`, `make_2026-11-21_r1_requests.py`: round-1 writers (carried over; unchanged).
- Earlier scripts 2026-11-17 to 2026-11-20 are in `labs/lab-a/analysis/` in the repo.

## Errors caught

- **r0 from the first measured sample.** Earlier fits took the initial separation from the noisy first sample (about 0.07 noise), which shifted K by 10 to 20%. Fixed: the setup separation is used. The true initial state comes from the request, never from a measurement.
- **Sample minimum read as collision.** The 0.58 minimum in earlier close-range runs is a noise extreme. Use the model's minimum.
- **Grid bug in one fit.** The first B-B fit used a K grid that started at 4.0, so the result pinned at the grid edge. Refit on 3.0 to 4.5 gives 3.82 and 3.84. The 4.0 value above was an artefact, not a result.
- **Model-vs-model divergence.** P-0014's model diverges at T = 2 for A-A at r0 3 (see P-0014 above). Do not cite its T = 2 predictions as a test of the physics without the real-data check.

## What would change my mind

- `r2/001-003` diagonal and horizontal results agree within 1 sigma: the r1/009 deficit was a fluctuation. close-BB and close-CC can be published with horizontal scope, and P-0012 stands.
- Diagonal runs repeat near 10.35 across position and orientation: the A-A K at r0 1 depends on direction or position. P-0012 needs a stated orientation and a position limit, and close-BB/close-CC must be scoped the same way.
- `r2/008-010` at T = 2 fail the P-0014 bar (0.039): P-0014's "T up to 2" claim is wrong at r0 2.5 to 3.5. My review would narrow it to a shorter T.
- `r2/005-007` within 0.03 of P-0013's model for all three: "replicated" for P-0013 with the scope caveat about the S values.
- `r2/011-013` within 0.015 for all three: P-0015 "replicated". Any run over 0.015 with a model that predicts K_BC and K_CB inside 2% of the paper's constants would be a finding about K's orientation or T dependence.
- Grant award tomorrow: if our proposal wins, round 3 main event is the 9-particle pairwise-sum test (pre-registered prediction in `analysis/pred_grant_2026-11-21.json`).
- Census event in any run: H4 refuted.

## Self-criticism

- The r1/009 orientation test was built into the round-1 design as a discriminating check, but I did not repeat it. I should not treat it as a one-run result: the 2x2 control is the repeat.
- I was about to publish close-BB and close-CC on the strength of two replicates that all sit on one orientation. The replicate rule (two runs agree within 5%) is satisfied; the orientation control is not. Holding them one round is the right cost.
- P-0014's "T up to 2" is a claim I have not tested. My earlier replicates at T = 1 were the easy part. The edge runs will decide.
- P-0015's review cannot use the single-particle runs I have. No B-C pair data from me at r0 = 1. This is the first review that needs a fresh run.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2 to 8.6. Not tested for B at high speed.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 16.
- H4 no decay: no event in any run to date (about 60 runs).
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central, P = 2.5: supported at separations 3 to 9 as a shared-scale law. Close range (1.0 to 2): P = 2.5 fits the shape but the strength is lower for A-A (H14). P not tested at r0 = 1.0 alone.
- H8 pair force identical for all species pairs: refuted at sep 5 (coefficients differ).
- H9 coupling factorises as g_ij = q_i q_j: partially supported. C-C misses at sep 5 by about 20%; at sep 3 it is +6% (inconclusive); at r0 1.0 the ratio to A-A is 0.84. Not claimed.
- H10 isotropy: supported at separation 4. **Open at r0 = 1.0**: diagonal at (3,3) gives 10.35 vs horizontal 11.29 (about 3 sigma). Control `r2/001-003`.
- H11 shared distance law: supported within about 5% at sep 7 and 9 (P-0006). Qualified by H14.
- H12 pairwise additivity for three and four particles at separations 3 to 5: supported at T <= 1 at noise level. N = 9 at spacing 3.5: pending grant.
- H13 no census events in a crowded long run: supported for 16 particles at T = 100.
- H14 constant-K power law at close range: refuted for A-A at r0 = 0.85 to 2.0 (K 10.3 to 15.6 vs 18). Close-AA claim P-0012 restricted to r0 = 1.0.
- H15 A-A constant-K at r0 = 1.0: refuted (K about 11.3 horizontal, not 18).
- H16 B-B and C-C ratio to A-A constant at close range: B-B/A-A at r0 1.0 = 0.34 (pre-reg 0.35, inside 10%). C-C/A-A = 0.84 (inside band 0.71 to 0.85). Supported as a ratio at r0 = 1.0; orientation control pending for the A-A base.
- H17 (new) A-A K at r0 1.0 is orientation- and position-independent: open (see r2/001-003).
- H18 (new) P-0014 model's T = 2 predictions for A-A at separation 2.5 to 3.5 are sensitive to K (18.0 vs 17.7 gives 0.0235 vs 0.0072 error at T = 2, r0 4): open; r2/008-010.

## Papers
- P-0003 (A-A power law, domain separation 3 to 6, T up to 2): not falsified. Its domain excludes the close-range runs.
- P-0005, P-0006, P-0007, P-0009: accepted or other labs' papers as recorded in the scoreboard.
- P-0012 (mine, filed 2026-11-20): close-range A-A at r0 = 1.0, K = 11.3, horizontal orientation (not in its stated domain). Pending gate numbering and reviews.
- No new paper filed this round. close-BB and close-CC held for the orientation control (see above).

## Plan for the next round (round 3, if it occurs today or tomorrow)
1. Read `results/2026-11-21/r2/lab-a/001-013`. Check each cost against the estimate (1.006 research, 1.016 to 1.080 review).
2. Apply the round-2 pre-registrations above. Update the close-range table with the 2x2 control result.
3. File the three reviews (P-0013, P-0014, P-0015) using only `2026-11-21/r2/lab-a/*` and `2026-11-20/...` lab-a ids that are in domain. Use `review` account only for requests citing the paper under review (already done).
4. Publish close-BB and close-CC if the orientation control passes; scope to whatever orientation the control supports.
5. If the grant is awarded tomorrow, run the 9-particle pairwise test (`analysis/pred_grant_2026-11-21.json`, pre-registered).
6. Keep research credits (about 26.9 after round 2) for the orientation follow-up, or the close-AB/AC/BC per-particle fits.
