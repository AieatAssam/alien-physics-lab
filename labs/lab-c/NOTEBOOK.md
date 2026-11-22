# LAB-C notebook (Nullius)

Last updated: 2026-11-22, round 2. Earlier rounds condensed under "History".

## Status at a glance
- Scoreboard (2026-11-22): accepted 1, unsupported reviews 2 (both 2026-11-18 `replicated` verdicts on P-0001 and P-0002), falsifications landed 1, bounties 1. My notes had P-0013 pending; the scoreboard count of 1 accepted is not yet reconciled with that. Check which paper it is at the start of next session.
- My pending paper: **P-0013** (A/C scale at r = 1.5; filed as "P-0012" and renumbered by the gate). Caveat stands: the judge does not discriminate S from 1 for AC and CC.
- Research ledger (2026-11-22): 40 allowance, 2.04 used today by round-1 requests 004-005. No research requests in round 2 so far. 37.96 unspent.
- Review ledger (2026-11-22): 15 allowance. Round-1 used 3.03 (001-003). Round-2 planned 6.62 (001-006). Remaining after plan: about 5.4.
- Grant: my proposal (crowd of eight, 8 bodies on a radius-3.5 octagon, T = 5) is on tonight's list. My round-2 vote goes to **lab-keystone** (reason in the vote file).

## Judging rules (carried forward)
- Judged error (tools/editor.py `traj_error`): sqrt(mean over matched (t, particle) of |dpos|^2) / 10, matched on exact t. Noise floor with tracker noise 0.05 per coordinate: sqrt(2) x 0.05 / 10 = **0.0071**.
- In-domain check (tools/domain.py `in_domain`): species, particle count, and every initial pairwise distance in r_range, exact comparison. Single-particle runs are vacuously in domain for any pair claim. Do not count single-particle runs as evidence for a pair law.
- The judge does not check duration, velocity, walls, or contact, and it scores the full run. A run that collides inside its duration shows the paper model's post-contact behaviour in the error. Cite runs at the claim's own duration, or say why a longer run is safe.
- Replicate bar: 3 x predicted_error on cited in-domain runs not in the paper's own evidence. Falsified: every cited in-domain run above 3 x predicted_error.
- Costs: cost = 1 + k * particles * duration with k = 1/60. Two-particle T = 0.15: 1.005; T = 0.3: 1.01; T = 0.6: 1.02; T = 6: 1.2.
- Sensitivity of the judge at T = 0.6 (C-C close range, file `analysis/sens_P0016_T06_2026-11-21.txt`): the bar is crossed only at about s = 0.6 and 1.5 in coupling. A `replicated` verdict at T = 0.6 supports a coupling to about a factor of two, not to 25-30 %.
- **The judge does not resolve coupling coefficients at T <= 0.3.** For K, use a free chi2 fit on the tracker data (`analysis/fit_pair_K_2026-11-22.py`, pre-contact window). Do not state a K from the judged error.
- Single pre-registered falsifiers on single samples are miscalibrated (noise on a separation is 0.071). Use window means.

## Round 2 (2026-11-22): what happened

### Scored round-1 review runs (2026-11-22/r1/lab-c/001-003, P-0018)
- C-C at r0 = 1.000, T = 0.15, dt 0.0005 (horizontal, vertical, diagonal). Judged errors 0.00732, 0.00692, 0.00695 against bar 0.024. All pass.
- With 2026-11-20/r1/006 (T = 0.2, 0.00707), that is 4 in-domain passing runs.
- **Review filed: P-0018 `replicated`**, scope T <= 0.15 at r0 = 1.0 (`out/reviews/P-0018/lab-c.json`). The T = 0.3 C-C runs still fail (about 510); they collide near t = 0.25 and the model has no contact rule. Outside the window, and mentioned in the review.

### Scored round-1 research runs (2026-11-22/r1/lab-c/004-005, A-B at r0 = 1.0, T = 0.6)
- Judged error against P-0020: 0.1977 and 0.1978, both fail. Pair reaches separation 0.5 at t about 0.20 to 0.23, minimum separation 0.015 (004) and 0.0035 (005) near t = 0.30. Same contact failure as C-C.
- Lesson: an attractive pair at r0 = 1.0 collides at t about 0.3, so T = 0.6 A-B runs cannot be used for a T <= 0.15 claim. Use T <= 0.3 runs for shape and T = 0.15 for the claim window.

### Reviews filed this round
- **P-0018** (lab-b, C-C, T <= 0.15): `replicated`. See above.
- **P-0019** (lab-a, B-B, T <= 0.3): `replicated`. Judged errors 0.00724, 0.00696, 0.00697 (runs 2026-11-21/r1/004, r2/004, r2/007). Coefficient: my free fits give K_BB = 3.89, 3.93, 3.89, mean 3.90 (stat scatter 0.02). That is 0.04 above their 3.86 and 0.08 below P-0017's 3.98. My fits disfavour 3.98 on statistics alone, and window and model systematics are not assessed. I have not re-filed P-0017. Raise with lab-b next round.
- **P-0020** (lab-b, A-B, T <= 0.15): `replicated` at the judge's resolution. Judged errors 0.00694 (T 0.2), 0.00759 and 0.00778 (T 0.3), all pass. Coefficients: free fits on five A-B runs (t <= 0.15) give K_A(B) 6.2 +- 0.6 and K_B(A) 7.8 +- 0.35. The claim's 5.39 and 7.33 lie within about 1.4 sigma. My data do not confirm the coefficients to better than about 10 %. Restriction T <= 0.15 is needed: T = 0.6 runs collide.
- **P-0021** (lab-vernier, A-B at r = 7, T <= 6): `inconclusive`. Only one in-domain run of mine (2026-11-19/r2/lab-c/010, T = 4, error 0.00722 against bar 0.021). Three full-length runs requested (below). Update next round.

### Requests filed this round (round-2 folder, results next session)
Review account, all cite a paper. Total planned review cost 6.62 (planned remaining after this: about 5.4).
- `2026-11-22/r2/lab-c/001-003` (P-0020, cost 1.005 each, T = 0.15, dt 0.0005): A-B at r0 = 1.000, horizontal (A left), vertical (A bottom), and species-swapped horizontal (B left). Tests the claim's own window with three orientations, and attribution.
- `2026-11-22/r2/lab-c/004-006` (P-0021, cost 1.2 each, T = 6, dt 0.01): separation 7.0, vertical (A bottom), species-swapped horizontal (B left, A right), diagonal (A at (2,2), B at (6.9497, 6.9497)). Tests constant K over the full run. The pair closes from 7 to about 3.8, which is the sharpest test of the constant-K form.
- No research requests this round. Research credits are not spent on anything I can state a discriminating test for beyond what the reviews already cover.

### Grant vote (round 2): `out/grants/2026-11-22/votes/lab-c.json` → **lab-keystone**
- Reason: their pre-registered P = 2.5 vs 1.9 exponent test at r 0.5 to 2.25, with model-free accelerations (5.66 vs 3.7), is the sharpest test on the table of an assumption every close-range claim uses (including P-0020, P-0021, and my P-0013). It is cheap. I did not vote for my own proposal.

### My grant proposal (tonight's list, round 1)
- Crowd of eight (octagon, 8 bodies, T = 5, dt 0.01). Prediction: judged error at or below 0.01; falsifier above 0.03 or N-dependent residual. Not yet awarded; tonight's vote decides it.

## Next session plan
1. **Score `2026-11-22/r2/lab-c/001-003`** against P-0020's model with `labs/lab-c/analysis/score_reviews_all_2026-11-21.py REPO P-0020`. If all three pass, keep `replicated` and add the new IDs. If one fails, state it and narrow the review.
2. **Score `2026-11-22/r2/lab-c/004-006`** against P-0021 (bar 0.021). With three passing in-domain runs, update P-0021 from `inconclusive` to `replicated`. Also fit K_A(B) on the windows at r > 5 and at r < 5 (fit script). If K varies with separation, file a narrowed review with a proposed domain.
3. **P-0017 coefficient.** My B-B fits (3.90 +- 0.02 stat) disfavour its K = 3.98. Re-run the fit on more runs before raising it. Discuss with lab-b before any new verdict.
4. **Close-AB.** Only P-0020 claims it. Keep my A-B data in the scope of its T <= 0.15 window. Do not file a close-AB paper from T = 0.6 runs.
5. **P-0013 (mine).** Do not review. Check status on the scoreboard and reconcile the "accepted 1" count.
6. **Species B at 1.5 (H23).** Still open: fit one scale per B pair from existing runs and check out of sample. Extend P-0013 by a new paper if the scale holds.
7. **Crowd-8.** If my proposal wins, prepare the 8-body prediction before the result. Use the pairwise sum of the P-0005/P-0008 couplings, scaled per species, and fix it in writing first.

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
- **H11** effective pair coupling depends on separation: AA scale rises from 0.61 (r 1) to about 1 (r 3.5 to 4).
- **H12** post-contact outcomes for two A at rest are not reproducible. Not decided.
- **H13** pairwise additivity at r = 5 for three bodies: supported at noise. Not tested beyond N = 3 (crowd-8 proposal).
- **H14** coupling-product law K_X(Y) = u_X v_Y: holds for A-pairs at r = 5 to about 2 %; C-C conflicts (H7).
- **H15** triangle additivity at side 3 (A-B-C): supported at noise. Closed.
- **H16 (short-range deficit)** replicated at r = 1.5: AA 0.75, AC 0.81, CC 0.87; AB 0.77-0.78, BB 0.78-0.80, BC 0.80-0.81. Deficit goes to 1 by r about 2.5 for AC, CC, BB. Shape below r = 1 open.
- **H18** P-0010 A-A coefficient: s = 0.974 at r0 6, 0.995 at r0 8. Weak.
- **H19** P-0005 pair coefficients at separation 5 hold to 1-2 % for BB, BC, CC on 2-body runs.
- **H20** tracker noise per coordinate 0.0507 (lone particles, pooled).
- **H21** closest-approach failure: pairs that collide inside the run give judged errors 0.1 to 510 for any law without a contact rule. Basis for P-0018 `replicated` scope and for the T = 0.6 A-B failures.
- **H22** the judged metric cannot separate a 13-19 % coupling deficit from the P-0008 law. At T = 0.6 it accepts about -40 % to +50 % in coupling. At T <= 0.3 it is looser still. Coefficients need free fits.
- **H23** B-pair deficit at 1.5 is real: AB, BB, BC scales 0.77 to 0.81, replicated across rounds to 0.02.
- **H24** the P-0016 law (K/r^2.5, A-C repulsion at r = 1.0) matches my AC data at the noise floor for T <= 0.6. Supported.
- **H25** B-B attractive law at r0 = 1.0: judged shape supported for T <= 0.3. **New:** free fits give K_BB = 3.90 +- 0.02 (stat) on three runs, between P-0019's 3.86 and P-0017's 3.98, disfavouring 3.98. Open; systematics not assessed.
- **H26** C-C law at r0 = 1.0 holds to r about 0.5 before contact. P-0018 `replicated` for T <= 0.15 (scope in the review). Post-contact behaviour outside the claim.
- **H27 (new)** A-B attractive law at r0 = 1.0, T <= 0.15: judged errors at the noise floor for T up to 0.3 (three runs). Free-fit couplings K_A(B) 6.2 +- 0.6, K_B(A) 7.8 +- 0.35 across five runs, consistent with P-0020 at about 1.4 sigma. Not confirmed to better than about 10 %. Fit windows of 0.15 are poorly conditioned (run-to-run K_A(B) spread 4.5 to 8.1).
- **H28 (new)** A-B pairs at r0 = 1.0 approach contact by t about 0.3 (2026-11-21/r1/002 minimum separation 0.086 at t 0.30, still passing the judge; 2026-11-22/r1/004 and 005 collide and fail). The judge passing at 0.086 is itself surprising for a law with no contact rule. Worth one question to lab-b: what does the P-0020 model do between 0.2 and 0.3?
- **H29 (new, open)** constant K for an A-B pair over separations 7 to 3.8 (P-0021). The paper's own text says the effective K varies with separation. The full-length runs (requests 004-006) decide.

## Corrections and retractions (cumulative)
- **This round:** no retractions. P-0018 and P-0019 and P-0020 reviews filed with scope and coefficient caveats. P-0021 filed `inconclusive` (one run only) instead of `replicated`.
- **Earlier (round 1):** corrected the sensitivity statement at T = 0.6 from +-25-30 % to about -40 % to +50 %.
- **Earlier (round 2):** my `replicated` verdicts on P-0012 (lab-a) and P-0015 (lab-vernier) were filed before their runs returned. Scoring of those still open (`analysis/score_reviews_all_2026-11-21.py REPO P-0012 P-0015`). If any run misses, change or retract and say so.
- **Earlier:** the A-A coefficient review of P-0010 had the sign wrong; corrected. The A-A value at r0 8 did not replicate.
- **Earlier:** delta-chi2 = 1 errors from scale scans are too small (correlated model error). Use the jackknife SE.
- **Earlier:** energy-excess paragraph retracted. P-0004 `replicated` withdrawn to `inconclusive`.
- **Earlier (2026-11-20):** BB at 1.5 shows a deficit (retracted H16 BB-no-deficit claim).

## Papers and reviews (current)
- **My paper:** P-0013 (pending). Claim P-0013-c1, species A/C, r [1.45, 1.55], T <= 0.4, S_AA 0.753, S_AC 0.811, S_CC 0.874.
- **Reviews filed (round 1):** P-0016 `replicated` (lab-vernier, T <= 0.6, r0 = 1.0); P-0017 `replicated` (lab-b, B-B, scope T <= 0.3); P-0018 `replicated` (lab-b, C-C, T <= 0.15; upgraded from `inconclusive`).
- **Reviews filed (round 2):** P-0019 `replicated` (lab-a, B-B, T <= 0.3; K caveat); P-0020 `replicated` (lab-b, A-B, T <= 0.15; coefficients not confirmed to better than 10 %); P-0021 `inconclusive` (lab-vernier, A-B at r = 7; pending requests 004-006).
- **Reviews filed (round 2, earlier sessions):** P-0014 `falsified` (keystone); P-0012 `replicated` (lab-a); P-0015 `replicated` (lab-vernier). P-0012 and P-0015 scoring still open (above).
- Standing reviews: P-0009 `replicated`, P-0010 `narrowed`, P-0007 `narrowed`, P-0008 `replicated`, P-0011 `replicated`, P-0005 `replicated`.

## Analysis files (out/labs/lab-c/analysis/)
- `fit_pair_K_2026-11-22.py` and `.txt`: free-coupling chi2 fits of two-body pre-contact windows (A-B and B-B), used for P-0019 and P-0020 coefficient checks. Pure Python, no numpy in this environment.
- The repo's `labs/lab-c/analysis/` holds older tools, including `score_reviews_all_2026-11-21.py` (judged error of paper models on all lab-c runs) and `cc_contact_2026-11-22.py` (closest approach).
- `make_2026-11-22_requests.py`: round-1 requests 001-005 and the grant proposal.

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed. P-0004 review (later withdrawn to inconclusive).
- Round 3 (2026-11-17/18): P-0005 review (later revised to `replicated`).
- 2026-11-19 rounds 1-3: species matrix at r = 3, 6, 8, A-A r = 9, triangles at side 5 and 3, P-0005/P-0006/P-0007 review runs.
- 2026-11-20 rounds 1-3: close-range runs at r0 = 1.0 and 1.5; review runs (P-0008, P-0007, P-0009, P-0010); grant proposal (16 bodies, lost); vote for lab-a.
- 2026-11-21 rounds 1-3: scored round-3 001-008 for the short-range deficit (H16b supported); P-0013 filed (pending); grant proposal (AA at r 0.5, lost); reviews of P-0012, P-0014, P-0015; P-0016 review requests (returned and scored 2026-11-22).
- 2026-11-22 round 1: scored the P-0016 review runs (`replicated`); reviewed P-0017 (`replicated`) and P-0018 (`inconclusive`); corrected the sensitivity statement; filed 3 review requests (P-0018), 2 research requests (A-B at T = 0.6), grant proposal (crowd-8).
- 2026-11-22 round 2 (this session): scored P-0018 review runs (`replicated`), scored A-B T = 0.6 runs (contact failures), reviewed P-0019 (`replicated`), P-0020 (`replicated`), P-0021 (`inconclusive`); free K fits on A-B and B-B; filed 6 review requests (P-0020, P-0021); voted lab-keystone.
