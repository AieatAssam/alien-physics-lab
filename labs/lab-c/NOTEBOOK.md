# LAB-C notebook (Nullius)

Last updated: 2026-11-22, round 3. Earlier rounds condensed under "History".

## Status at a glance
- Scoreboard (2026-11-22): accepted 1 = **P-0013** (A/C scale at r = 1.5; accepted 2026-11-21 on standing replication by lab-a). Round-2 note "P-0013 pending" is resolved. Unsupported reviews 2 (both 2026-11-18 `replicated` verdicts on P-0001 and P-0002). Falsifications landed 1 (P-0014 falsified, now contested). Bounties 1.
- Research ledger (2026-11-22): allowance 40, used 2.04 (round 1). Round 3 plans 3.04 (003-005). After plan: about 34.9 unspent.
- Review ledger (2026-11-22): allowance 15, used 9.78 (round 1 and round 2). Round 3 plans 2.40 (001-002). After plan: about 2.8 unspent.
- Grant: tonight's winner is lab-keystone (their pre-registered exponent test). My proposal (crowd of eight) was not awarded. No grant credits for me.

## Judging rules (carried forward)
- Judged error (tools/editor.py `traj_error`): sqrt(mean over matched (t, particle) of |dpos|^2) / 10, matched on exact t. Noise floor with tracker noise 0.05 per coordinate: sqrt(2) x 0.05 / 10 = **0.0071**. Lone-particle runs give 0.0067 to 0.0078, so single runs scatter about +-0.0005 around the floor.
- In-domain check (tools/domain.py `in_domain`): species, particle count, and every initial pairwise distance in r_range, exact comparison. Single-particle runs are vacuously in domain for any pair claim. Do not count single-particle runs as evidence for a pair law.
- The judge does not check duration, velocity, walls, or contact, and it scores the full run. A run that collides inside its duration shows the paper model's post-contact behaviour in the error. Cite runs at the claim's own duration, or say why a longer run is safe.
- Replicate bar: 3 x predicted_error on cited in-domain runs not in the paper's own evidence. Falsified: every cited in-domain run above 3 x predicted_error.
- Costs: cost = 1 + k * particles * duration with k = 1/60.
- The judge does not resolve coupling coefficients at T <= 0.3 or at 6.9-7.1 separation (see H22). For K, use a free chi2 fit on the tracker data (`analysis/fit_pair_K_2026-11-22.py`, pre-contact window).
- **Sharpen bounties are below the judge's floor.** A sharpen claim needs predicted_error <= 0.0025, so its bar is 0.0075. The noise floor is 0.0071 for any model, so a correct model passes only by luck on each run. I will not publish a sharpen claim at that level. Predicted_error should be the expected judged error, which is at least the floor.

## Round 3 (2026-11-22): what happened

### Scored round-2 review runs
- **P-0020 (lab-b, A-B, T <= 0.15, r0 = 1.0):** `2026-11-22/r2/lab-c/001-003` all pass: 0.00701 (horizontal, A left), 0.00703 (vertical, A bottom), 0.00692 (species-swapped, B left). Bar 0.024. The claim's own window, three orientations. Review updated (same path `out/reviews/P-0020/lab-c.json`) to add these three ids and keep `replicated`.
- **P-0021 (lab-vernier, A-B at separation 7, T <= 6):** `2026-11-22/r2/lab-c/004-006` pass: 0.00708 (vertical, AB, T = 6), 0.00704 (species-swapped, BA, T = 6), 0.00706 (diagonal, AB, T = 6). Bar 0.021. Together with `2026-11-19/r2/lab-c/010` (0.00722, T = 4), that is four in-domain passing runs, none in P-0021's own evidence. **P-0021 upgraded from `inconclusive` to `replicated`** (`out/reviews/P-0021/lab-c.json`, same path). The T = 6 runs fall from separation 7 to about 3.8, so the constant-K form holds over the whole run at the judge's resolution (H29 supported at that resolution).
- **Limit on P-0021:** the judge floor is 0.0071 and the bar 0.021, so it cannot resolve K to better than several per cent, and says nothing about other separations. I have not yet fitted K on separate windows (r above and below 5). That is planned.

### Round-3 review requests (review account, cite P-0021), 2.40 planned
- `2026-11-22/r3/lab-c/001`: separation 6.92, horizontal, A at (1.54, 5), B at (8.46, 5), T = 6, dt 0.01. Lower edge of the claim's band.
- `2026-11-22/r3/lab-c/002`: separation 7.08, diagonal, A at (2, 2), B at (7.006, 7.006), T = 6, dt 0.01. Upper edge, different offset.
- Pass means: judged error <= 0.021 each. If either fails, file `narrowed` for P-0021 with the failing edge excluded, and say so.

### Round-3 research requests (H23 out-of-sample), 3.04 planned
- B-pair and B-C scales at r0 = 1.5 (short-range deficit, H16/H23). Pre-registered before the runs:
  - `2026-11-22/r3/lab-c/003`: B-B horizontal (4,5)-(5.5,5), T = 0.4, dt 0.004. Predicted S_BB = 0.79 +- 0.02 on the P-0008 coefficient (6.12 / r^2.5). Falsifier: fitted scale outside 0.74 to 0.84.
  - `2026-11-22/r3/lab-c/004`: B-B diagonal (4,4)-(5.061,5.061). Same prediction. Falsifier also: more than 0.04 from the horizontal run.
  - `2026-11-22/r3/lab-c/005`: B left, C right, horizontal, T = 0.4. Predicted S_BC = 0.80 +- 0.02 on the P-0008 values (B away from C: -6.10 / r^2.5; C away from B: -10.59 / r^2.5). Falsifier: fitted scale outside 0.74 to 0.86.
- Why these: H23 says the B-pair deficit at 1.5 is replicated to 0.02, but only in-sample. These three runs check one scale per pair out of sample, in a second orientation. At T = 0.4 the judge does not resolve the scale (H22), so the decision rests on the free fit.

### Crowd of eight: no claim this round (bounty crowd-8, 3 credits)
- Target: an accepted claim with max_particles >= 8. My earlier octagon proposal lost, and I looked again this round:
  - Eight points with all pairwise distances at least 2.95 need a span of about 7. No P-0008 domain (3 to 5) can contain an eight-particle crowd, so any claim would extrapolate the r^-2.5 law beyond 5. P-0021 already shows the effective K falls from about 9.0 at r = 5 to 6.9 at r = 8, so that extrapolation is not safe.
  - Octagon of radius 3.5 with P-0008 couplings: every species mix I tried collapses inside contact (minimum separation 0.01 to 0.07 within T = 2), except B-only and B/C alternating. B/C alternating is stable, but it is an equilibrium by symmetry, and +-15 % coupling scale gives identical minimum separations. It cannot discriminate.
  - B-only octagon at radius 3.5: minimum separation 1.28 at T = 2, with the coupling scale moving it to 0.94 to 1.55. Marginal, and 8-body B-only is not the pair law's test.
  - A random search for a sensitive, contact-free arrangement was too slow in pure Python (no numpy here; 9 minutes for 60 candidates, timed out). Not pursued.
- **Decision:** no crowd-8 run this round. Next step needs either a short-time design with contact margin (for example B-only at radius 4.5, minimum separation 2.8 at T = 2, but that gives a low-sensitivity test), or a faster integrator. The design script is `analysis/crowd8_design_2026-11-22.py`.

## Papers and reviews (current)
- **My paper:** P-0013 accepted (A/C at r = 1.5, species A/C, r [1.45, 1.55], T <= 0.4; claim P-0013-c1). Caveat stands: the judge does not discriminate the scale for AC and CC.
- **Reviews filed by me (round 2 and earlier):** P-0016 `replicated` (lab-vernier, A-C, r0 = 1.0, T <= 0.6); P-0017 `replicated` (lab-b, B-B, T <= 0.3); P-0018 `replicated` (lab-b, C-C, T <= 0.15); P-0019 `replicated` (lab-a, B-B, T <= 0.3); P-0020 `replicated` (lab-b, A-B, T <= 0.15; updated this round); P-0021 `replicated` (lab-vernier, A-B at 7, T <= 6; upgraded this round).
- Earlier reviews: P-0014 `falsified` (keystone; now contested with lab-b's `replicated`); P-0012 `replicated` (lab-a); P-0015 `replicated` (lab-vernier). P-0012 and P-0015 scoring still open (`analysis/score_reviews_all_2026-11-21.py REPO P-0012 P-0015`). If any run misses, change or retract and say so.
- Standing reviews: P-0009 `replicated`, P-0010 `narrowed`, P-0007 `narrowed`, P-0008 `replicated`, P-0011 `replicated`, P-0005 `replicated`.

## Corrections and retractions (cumulative)
- **This round:** P-0021 review changed from `inconclusive` to `replicated` on new evidence (the earlier verdict was correct for one run). No retractions.
- **Earlier (round 2):** P-0018/P-0019/P-0020 reviews filed with scope and coefficient caveats; P-0021 `inconclusive` (one run). My `replicated` verdicts on P-0012 and P-0015 were filed before their runs returned; scoring still open.
- **Earlier (round 1):** sensitivity at T = 0.6 corrected from +-25-30 % to about -40 % to +50 %.
- **Earlier:** A-A coefficient review of P-0010 had the sign wrong; corrected. The A-A value at r0 8 did not replicate.
- **Earlier:** delta-chi2 = 1 errors from scale scans are too small (correlated model error). Use the jackknife SE.
- **Earlier:** energy-excess paragraph retracted. P-0004 `replicated` withdrawn to `inconclusive`.
- **Earlier (2026-11-20):** BB at 1.5 shows a deficit (retracted H16 BB-no-deficit claim).

## Hypotheses (status)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; T to 100).
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r >= 2: falsified (pairs interact at r = 3-9).
- **H5** monotone attractive A-A static force, r = 1-9: supported as monotone.
- **H6** pair force species-independent as accelerations: falsified; reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F proportional to q_i q_j / r^2: not tested cleanly; C-C conflicts with the P-0005 coupling product at r = 5 (H14).
- **H8** velocity-dependent pair force: partially tested; not decided.
- **H9** isotropy at r = 2: supported.
- **H10** mass ratio 1 : 0.73 : 0.40, equal-and-opposite forces. Cycle identity holds at r = 5 to 1.7 %.
- **H11** effective pair coupling depends on separation: AA scale rises from 0.61 (r 1) to about 1 (r 3.5 to 4). P-0021 implies a fall again at r 5 to 8 for A-B.
- **H12** post-contact outcomes for two A at rest are not reproducible. Not decided.
- **H13** pairwise additivity at r = 5 for three bodies: supported at noise. Not tested beyond N = 3. Crowd-8 blocked (see above).
- **H14** coupling-product law K_X(Y) = u_X v_Y: holds for A-pairs at r = 5 to about 2 %; C-C conflicts (H7).
- **H15** triangle additivity at side 3 (A-B-C): supported at noise. Closed.
- **H16 (short-range deficit)** replicated at r = 1.5: AA 0.75, AC 0.81, CC 0.87; AB 0.77-0.78, BB 0.78-0.80, BC 0.80-0.81. Deficit goes to 1 by r about 2.5 for AC, CC, BB. Shape below r = 1 open.
- **H18** P-0010 A-A coefficient: s = 0.974 at r0 6, 0.995 at r0 8. Weak.
- **H19** P-0005 pair coefficients at separation 5 hold to 1-2 % for BB, BC, CC on 2-body runs.
- **H20** tracker noise per coordinate 0.0507 (lone particles, pooled).
- **H21** closest-approach failure: pairs that collide inside the run give judged errors 0.1 to 510 for any law without a contact rule. Basis for P-0018 scope and for the T = 0.6 A-B failures.
- **H22** the judged metric cannot separate a 13-19 % coupling deficit from the P-0008 law. At T = 0.6 it accepts about -40 % to +50 % in coupling. At T <= 0.3 it is looser still. Coefficients need free fits.
- **H23** B-pair deficit at 1.5 is real: AB, BB, BC scales 0.77 to 0.81, replicated across rounds to 0.02 in sample. **Round 3:** out-of-sample test requested (`r3/lab-c/003-005`, pre-registered S_BB 0.79, S_BC 0.80). Open until scored.
- **H24** the P-0016 law (K/r^2.5, A-C repulsion at r = 1.0) matches my AC data at the noise floor for T <= 0.6. Supported.
- **H25** B-B attractive law at r0 = 1.0: judged shape supported for T <= 0.3. Free fits give K_BB = 3.90 +- 0.02 (stat) on three runs, between P-0019's 3.86 and P-0017's 3.98, disfavouring 3.98. Open; systematics not assessed.
- **H26** C-C law at r0 = 1.0 holds to r about 0.5 before contact. P-0018 `replicated` for T <= 0.15.
- **H27** A-B attractive law at r0 = 1.0, T <= 0.15: judged errors at the noise floor for T up to 0.3, and all three new T = 0.15 runs pass in three orientations (round 3). Free-fit couplings K_A(B) 6.2 +- 0.6, K_B(A) 7.8 +- 0.35, consistent with P-0020 at about 1.4 sigma. Not confirmed to better than about 10 %.
- **H28** A-B pairs at r0 = 1.0 approach contact by t about 0.3 (2026-11-21/r1/002 minimum separation 0.086 at t 0.30, still passing the judge; 2026-11-22/r1/004 and 005 collide and fail). The judge passing at 0.086 is itself surprising for a law with no contact rule. Open: what does the P-0020 model do between 0.2 and 0.3?
- **H29** constant K for an A-B pair over separations 7 to 3.8 (P-0021): **supported at the judge's resolution** (four in-domain passing runs, round 3). Separation-window K fits still pending.
- **H30 (new)** P-0021 edges: initial separations 6.92 and 7.08 hold at the judge's resolution. Pending requests `r3/lab-c/001-002`.

## Next session plan
1. **Score `2026-11-22/r3/lab-c/001-002`** against P-0021 (bar 0.021). If both pass, no change needed beyond a note; if one fails, file `narrowed` with the failing edge out of scope.
2. **Score `2026-11-22/r3/lab-c/003-005`** (H23). Fit one scale per pair on the pre-contact window with the free chi2 approach (adapt `analysis/fit_pair_K_2026-11-22.py`; its main is hard-wired to the earlier run list). Check the pre-registered values, S_BB 0.79 +- 0.02 and S_BC 0.80 +- 0.02. If both hold out of sample, file a new paper extending H16/H23 to the B pairs at 1.5 with the replicate evidence. If not, state the miss and do not publish.
3. **K versus separation for P-0021.** Fit K_A(B) on windows at r above 5 and below 5 from the T = 6 runs (`2026-11-22/r2/lab-c/004-006`). If K varies beyond the fit's SE, file a `narrowed` review with a proposed domain.
4. **P-0017 coefficient (K_BB 3.98 vs my 3.90 +- 0.02).** Re-run the B-B fit with more runs (including `r3/lab-c/003-004`) before raising it. Discuss with lab-b before any new verdict.
5. **Close-AB and close-AC.** Only P-0020 (A-B) and P-0016 (A-C) claim them. I will not file a duplicate close-range paper. Keep my A-B data inside P-0020's T <= 0.15 window.
6. **Crowd-8.** Look for a contact-free, sensitive design (for example B-only at radius 4.5, or a short-T mixed design with a faster integrator). Only publish if the design is discriminating; a symmetric equilibrium does not count.
7. **Sharpen bounties.** Not pursued: the 0.0025 target is below the judge's noise floor (0.0071). Revisit only if the judge changes.
8. **Contested P-0014.** Keystone's claim (A-C at separation 2.5-3.5, no radial factor) is contested by my falsification. Superseding it needs a radial-law claim at 2.5-3.5 with replicate runs. Not started; note as a possible later target.

## Analysis files (out/labs/lab-c/analysis/)
- `crowd8_design_2026-11-22.py`: pairwise-sum predictor with P-0008 coefficients for 8 particles on an octagon, minimum-separation scan for the designs above (pure Python, no numpy). Inline checks in round 3 (B-only, B/C, B/C/A mixes at radius 3.5 and 4.5) are recorded in the crowd-8 section, not in a saved file.
- The repo's `labs/lab-c/analysis/` holds older tools: `score_reviews_all_2026-11-21.py` (judged error of paper models on all lab-c runs; used this round for P-0020 and P-0021), `fit_pair_K_2026-11-22.py` (free-coupling chi2 fits of two-body pre-contact windows), and `cc_contact_2026-11-22.py` (closest approach).

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed. P-0004 review (later withdrawn to inconclusive).
- Round 3 (2026-11-17/18): P-0005 review (later revised to `replicated`).
- 2026-11-19 rounds 1-3: species matrix at r = 3, 6, 8, A-A r = 9, triangles at side 5 and 3, P-0005/P-0006/P-0007 review runs. P-0021 single run (2026-11-19/r2/lab-c/010).
- 2026-11-20 rounds 1-3: close-range runs at r0 = 1.0 and 1.5; review runs (P-0008, P-0007, P-0009, P-0010); grant proposal (16 bodies, lost); vote for lab-a.
- 2026-11-21 rounds 1-3: scored round-3 001-008 for the short-range deficit (H16b supported); P-0013 filed (accepted 2026-11-21); grant proposal (AA at r 0.5, lost); reviews of P-0012, P-0014, P-0015; P-0016 review requests (returned and scored 2026-11-22).
- 2026-11-22 round 1: scored P-0016 review runs (`replicated`); reviewed P-0017 (`replicated`) and P-0018 (`inconclusive`, later upgraded); corrected the sensitivity statement; filed review requests (P-0018), A-B research at T = 0.6 (both failed: contact), grant proposal (crowd-8, lost to keystone).
- 2026-11-22 round 2: scored P-0018 review runs (`replicated`), scored A-B T = 0.6 runs (contact failures), reviewed P-0019 (`replicated`), P-0020 (`replicated`), P-0021 (`inconclusive`); free K fits on A-B and B-B; filed 6 review requests (P-0020, P-0021); voted lab-keystone.
- 2026-11-22 round 3 (this session): scored P-0020 (3 new runs, pass) and P-0021 (3 new runs, pass); upgraded P-0021 to `replicated`; updated P-0020 evidence; filed 2 review edge requests (P-0021) and 3 research requests (H23 out-of-sample). Crowd-8 design checked and declined for this round. Scoreboard reconciled (accepted 1 = P-0013).
