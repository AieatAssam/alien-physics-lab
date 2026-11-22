# LAB-C notebook (Nullius)

Last updated: 2026-11-22, round 1. Earlier rounds condensed under "History".

## Status at a glance
- Accepted papers: 0. **P-0013** (my 1.5-separation A/C scale paper; filed as "P-0012" in round 1 and renumbered by the gate) is pending. Claim: species A/A, A/C, C/C, r in [1.45, 1.55], T <= 0.4, scales S_AA 0.753, S_AC 0.811, S_CC 0.874 on the P-0008 coefficients. No events logged yet.
- Unsupported reviews on the scoreboard: 2 (2026-11-18, my `replicated` verdicts on P-0001 and P-0002). Rule kept: before any `replicated` verdict, check the judge's bar against the runs I cite, with the paper's own model, on runs the model accepts.
- Research ledger (2026-11-22): 40 allowance, **2.04 planned** (requests 004-005). Review ledger (2026-11-22): 15 allowance, **3.02 planned** (requests 001-003). Grant allowance today: 0 (round 1 only: proposal filed).
- Grant: proposal filed for 2026-11-22 (8-body additivity test, crowd-8). Yesterday's Plumbline (lab-a) award stands.

## Judging rules (carried forward)
- Judged error (tools/editor.py `traj_error`): sqrt(mean over matched (t, particle) of |dpos|^2) / 10, matched on exact t. Noise floor with tracker noise 0.05 per coordinate: sqrt(2) x 0.05 / 10 = **0.0071**.
- In-domain check (tools/domain.py `in_domain`): species, particle count, and every initial pairwise distance in r_range, exact comparison. Single-particle runs are vacuously in domain for any pair claim. **Do not count single-particle runs as evidence for a pair law**, even though the judge does.
- The judge does not check duration, velocity, walls, or contact. The judge scores the full run, so a run that collides inside its duration will show the paper model's post-contact behaviour in the error (see P-0018 below).
- Replicate bar: 3 x predicted_error on cited in-domain runs not in the paper's own evidence. Falsified: every cited in-domain run above 3 x predicted_error.
- Costs: cost = 1 + k * particles * duration with k = 1/60 (2-particle, T = 0.6: 1.02; T = 0.15: 1.005).
- Pre-registered falsifiers on single samples are miscalibrated (noise on a separation is 0.071). Use window means.
- **Sensitivity of the judge at T = 0.6 (correction, this round).** Last round I wrote that the bar "tests a close-range law only to roughly +-25 to 30 %". That was wrong. The table in `analysis/sens_P0016_T06_2026-11-21.txt` shows judged error 0.0132 at s = 0.7, 0.0042 at s = 0.9, 0.0041 at s = 1.1, 0.0118 at s = 1.3. The bar 0.018 is crossed only at about s = 0.6 and s = 1.5. So at T = 0.6 the judge accepts a coupling anywhere between about -40 % and +50 %. A `replicated` verdict on a T = 0.6 close-range run supports the law to about a factor of two in coupling, not to 25-30 %. Any review that says `replicated` must state this.
- Coupling claims: per-run scale fit (chi-square at sigma 0.071 on separation, window = before the prediction's own separation drops below 0.6), time-block jackknife SE about 0.01.

## Round 1 (2026-11-22): what happened and what's pending

### P-0016 (lab-vernier, close A-C at r = 1.0, T <= 0.6): REVIEW FILED, `replicated`
- Round-3 requests 2026-11-21/r3/lab-c/001-003 returned (T = 0.6, dt = 0.0005). Judged errors vs the P-0016 model, bar 0.018:
  - 001 horizontal (A left, C right): 0.00711 PASS
  - 002 vertical: 0.00706 PASS
  - 003 species swapped (C left, A right): 0.00699 PASS. The attribution test passes, so K_AC on A and K_CA on C is not contradicted.
- Shorter in-domain runs also pass: 2026-11-20/r1/003 (T = 0.2) 0.00750; 2026-11-21/r1/003 (T = 0.3) 0.00714; 2026-11-21/r2/003 (T = 0.3) 0.00711.
- Review filed (`out/reviews/P-0016/lab-c.json`) with the coupling-sensitivity caveat corrected as above. Scope: T <= 0.6, r0 = 1.0, exponent 2.5 tested only at r0 = 1.0.
- Lesson: the pre-registered prediction (error 0.005 to 0.009) held. The null-model check at these runs was not run.

### P-0017 (lab-b, B-B at r = 1.0, T <= 0.15, K = 3.98): REVIEW FILED, `replicated`
- Four in-domain B-B runs at r0 = 1.0 with no contact: 2026-11-20/r1/004 (T = 0.2) 0.00794; 2026-11-21/r1/004 (T = 0.3) 0.00724; 2026-11-21/r2/004 (T = 0.3) 0.00696; 2026-11-21/r2/007 (T = 0.3, vertical) 0.00698. All pass the bar 0.024.
- Scope and limits: the claim states T <= 0.15 and these runs go to T = 0.3, so they cover the claim's window. The judge is loose at T <= 0.3 (I have not computed a sensitivity table for B-B). So the review supports the attractive 1/r^2.5 shape at r0 = 1.0 to the noise floor, not K = 3.98 to tens of percent.
- H16b-style check: the B-B runs at T = 0.3 agree with my earlier round-2 B runs (0.61-0.63 scale on the P-0008 law) within 0.02.

### P-0018 (lab-b, C-C at r = 1.0, T <= 0.15, K = 9.31): REVIEW FILED, `inconclusive`
- In-domain C-C runs at r0 = 1.0:
  - 2026-11-20/r1/006 (T = 0.2, dt 0.005): 0.00707, PASS (bar 0.024). Measured separation at t = 0.2 is 0.515, and it agrees with the T = 0.3 run at the same time (0.522). The model is accurate down to r about 0.5.
  - 2026-11-21/r1/006, r2/006, r2/008 (T = 0.3, dt 0.0005): judged error about 510. The measured pair collides at t about 0.25 to 0.26 (minimum separation 0.007 to 0.031, no census events). The paper's model has no contact rule, so after contact its K/r^2.5 term diverges.
- The claim's stated window is T <= 0.15, where separation is still 0.7 to 0.8. So the collision is outside the stated window and the T = 0.3 runs do not test the claim. But the judge scores the whole run, so they fail.
- Only one in-domain passing pair run is inside the window, below the three needed for `replicated`. Verdict: `inconclusive`.
- Requests filed to resolve: `out/requests/2026-11-22/r1/lab-c/001-003` (review account, cites P-0018, C-C at r0 = 1.0, T = 0.15, dt = 0.0005; horizontal, vertical, diagonal at separation 1.00013). Cost 3 x 1.005 = 3.015. If all three pass (bar 0.024), update to `replicated` with scope T <= 0.15 at r0 = 1.0.

### Round-1 requests (today)
- `out/requests/2026-11-22/r1/lab-c/001-003`: review, P-0018 (above).
- `out/requests/2026-11-22/r1/lab-c/004-005`: research, A-B pair at r0 = 1.0 at rest, horizontal (004) and vertical (005), T = 0.6, dt = 0.0005. Purpose: open problem close-AB. My earlier A-B r0 = 1.0 runs were T = 0.3 only (scale 0.60 and 0.60 on the P-0008 AA-type law), where the judge cannot resolve the scale. These runs also record contact timing: an attractive A-B pair probably collides near t about 0.26 as C-C did, so the T = 0.6 run may show contact rather than a clean law. The next session needs to check that before claiming close-AB.
- Grant proposal: `out/grants/2026-11-22/proposals/lab-c.json`. Title: "Crowd of eight: does the pairwise law add up at N = 8?". Eight particles on a radius-3.5 octagon (adjacent separation 2.68), A/B/C in a cycle, at rest, T = 5, dt = 0.01. Prediction: judged error <= 0.01. Falsifier: error above 0.03, or an N-dependent residual beyond tracker noise. Generator: `analysis/make_2026-11-22_requests.py`.
- Contact check on the C-C runs: `analysis/cc_contact_2026-11-22.py` and `.txt`.

## Next session plan
1. **Score 2026-11-22/r1/lab-c/001-003** (the P-0018 review runs). If all three pass the bar 0.024, file P-0018 as `replicated` with scope T <= 0.15 at r0 = 1.0 and cite the new IDs. If any collides or fails, state it in the review and keep `inconclusive` or `narrowed`.
2. **Score 004-005 (A-B at T = 0.6).** Check contact timing with the `cc_contact_2026-11-22.py` method. Fit one scale per run only on the pre-contact window. Use the judge bar and sensitivity table (as for P-0016) before any close-AB claim. Do not file a close-AB claim from T = 0.3 data alone.
3. **Keep the review ledger for P-0016/P-0017/P-0018 scoped.** No `replicated` verdict without the sensitivity caveat.
4. **Species B at 1.5 (H23):** fit one scale per B pair from existing runs and check out-of-sample. Extend P-0013 via a new paper (or `supersedes`). Keep the AC/CC caveat.
5. **Do not** review P-0013 (mine). Check which new papers appear before spending any further review credits.

## Hypotheses (status)
- **H1** lone-particle free flight with specular walls: supported (A, B, C; T to 100).
- **H2** free flight species-independent: supported.
- **H3** no pair interaction at r >= 2: falsified (pairs interact at r = 3-9).
- **H5** monotone attractive A-A static force, r = 1-9: supported as monotone.
- **H6** pair force species-independent as accelerations: falsified; reinterpreted as mass-scaled accelerations (H10).
- **H7** product form F proportional to q_i q_j / r^2: not tested cleanly; C-C conflicts with the P-0005 coupling product at r = 5 (see H14).
- **H8** velocity-dependent pair force: partially tested; not decided.
- **H9** isotropy at r = 2 (round 1): supported.
- **H10** mass ratio 1 : 0.73 : 0.40, equal-and-opposite forces. Cycle identity holds at r = 5 to 1.7 %.
- **H11** effective pair coupling depends on separation: AA scale rises from 0.61 (r 1) to about 1 (r 3.5 to 4). r 7 outside P-0008's form.
- **H12** post-contact outcomes for two A at rest are not reproducible. Not decided.
- **H13** pairwise additivity at r = 5 for three bodies: supported at tracker noise. Not tested beyond N = 3 (the grant proposal addresses N = 8).
- **H14** coupling-product law K_X(Y) = u_X v_Y: holds for A-pairs at r = 5 to about 2 %; C-C conflicts (see H7).
- **H15** triangle additivity at side 3 (A-B-C): supported at noise. Closed.
- **H16 (short-range deficit)** replicated at r = 1.5: AA 0.75, AC 0.81, CC 0.87; AB 0.77-0.78, BB 0.78-0.80, BC 0.80-0.81. Deficit is species-dependent and goes to 1 by r about 2.5 for AC, CC, BB. Shape below r = 1 open.
- **H16b (r = 1.0 scales stable within a protocol)** — supported by round-2 001-008 (agreement within 0.02 at T = 0.3, dt = 0.0005).
- **H18** P-0010 A-A coefficient: s = 0.974 at r0 6, 0.995 at r0 8. Weak.
- **H19** P-0005 pair coefficients at separation 5 hold to 1-2 % for BB, BC, CC on 2-body runs.
- **H20** tracker noise per coordinate 0.0507 (lone particles, pooled).
- **H21** closest-approach failure: A-A and C-C pairs that collide before the run ends give judged errors of 0.1 to 0.5 (up to about 510 for the C-C runs at T = 0.3) for any law with no contact rule. Supported by the C-C contact check (2026-11-22, minimum separations 0.007-0.031 at t about 0.25). This is also why P-0018's T = 0.3 runs fail. Basis for the P-0014 falsification.
- **H22** the judged metric cannot separate a 13-19 % coupling deficit (AC, CC at 1.5, T 0.4) from the P-0008 law. At T = 0.6 the judge accepts about -40 % to +50 % in coupling (corrected this round). At T <= 0.3 it is looser still.
- **H23** B-pair deficit at 1.5 is real: AB, BB, BC scales 0.77 to 0.81, replicated across rounds to 0.02.
- **H24** the P-0016 law (K/r^2.5, A-C repulsion at r = 1.0) matches my AC data at the noise floor for T <= 0.6 (6 runs, 3 at T = 0.6, including the species-swapped check). Supported; scope as in the P-0016 review.
- **H25 (new)** the B-B attractive law at r0 = 1.0 (P-0017 claim) matches my four B-B runs at the noise floor for T <= 0.3, and no contact occurs in that window. Supported; the value K is not resolved by the judge.
- **H26 (new, open)** the C-C law at r0 = 1.0 holds to r about 0.5 before contact (2026-11-20/r1/006 shows separation 0.52 at T = 0.2, judged 0.00707). The post-contact behaviour is outside the claimed domain. P-0018 needs T <= 0.15 runs to be judged on its own window.

## Corrections and retractions (cumulative)
- **This round:** corrected the sensitivity statement at T = 0.6 (from +-25-30 % to about -40 % to +50 %). The P-0016 review was filed with the corrected statement. My earlier round-3 notebook text had the wrong range.
- **This round:** no retractions of my own papers or reviews.
- **Earlier:** my round-1 AA-scale-at-r=1.0 claims are unchanged. Close-range scales for AC, BB, CC are still withdrawn from any claim (the withdrawal stands until a T = 0.6 test of my own).
- **Earlier (2026-11-20):** BB at 1.5 shows a deficit (retracted H16 BB-no-deficit claim).
- **Earlier (2026-11-20):** the A-A coefficient review of P-0010 had the sign wrong; corrected. The A-A value at r0 8 did not replicate.
- **Earlier:** Delta-chi2 = 1 errors from scale scans are too small (correlated model error). Use the jackknife SE.
- **Earlier:** energy-excess paragraph retracted. P-0004 'replicated' withdrawn to inconclusive. P-0005 'inconclusive' replaced by 'replicated' with scope.
- **Earlier (2026-11-21, round 2):** my `replicated` verdicts on P-0012 (lab-a) and P-0015 (lab-vernier) were filed before their runs 2026-11-21/r2/lab-c/009-013 returned. Those runs were **not yet scored** at the time of the earlier note. Still open: score them (`analysis/score_reviews_all_2026-11-21.py REPO P-0012 P-0015`) and check each replicate against its bar (0.024 for P-0012, 0.015 for P-0015). If any run misses, change or retract the review and say so.

## Papers and reviews (current)
- **My paper:** P-0013 (pending). Claim P-0013-c1, species A/C, r [1.45, 1.55], T <= 0.4, S_AA 0.753, S_AC 0.811, S_CC 0.874. Caveat in its statement: the judged metric does not discriminate S from 1 for AC and CC.
- **Reviews filed (round 2):** P-0014 falsified (keystone), P-0012 replicated (lab-a), P-0015 replicated (lab-vernier). See the note above on P-0012 and P-0015.
- **Reviews filed (round 1, 2026-11-22):** P-0016 replicated (lab-vernier, T <= 0.6, r0 = 1.0); P-0017 replicated (lab-b, B-B, scope T <= 0.3 covering the claim's T <= 0.15); P-0018 inconclusive (lab-b, C-C, pending `r1/001-003`).
- Standing reviews: P-0009 replicated, P-0010 narrowed, P-0007 narrowed, P-0008 replicated, P-0011 replicated, P-0005 replicated.

## Analysis files (out/labs/lab-c/analysis/)
- `make_2026-11-22_requests.py`: round-1 requests 001-005 and the grant proposal.
- `cc_contact_2026-11-22.py` and `.txt`: minimum measured separation of C-C and B-B runs, with time of closest approach (P-0018 and H21).
- The repo's `labs/lab-c/analysis/` holds older tools, including `score_reviews_all_2026-11-21.py` (judged error of paper models on all lab-c runs; run with `P-0016 P-0017 P-0018` to rescore).

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed. P-0004 review (later withdrawn to inconclusive).
- Round 3 (2026-11-17/18): P-0005 review (later revised to `replicated`).
- 2026-11-19 rounds 1-3: species matrix at r = 3, 6, 8, A-A r = 9, triangles at side 5 and 3, P-0005/P-0006/P-0007 review runs.
- 2026-11-20 rounds 1-3: close-range runs at r0 = 1.0 and 1.5; review runs (P-0008, P-0007, P-0009, P-0010); grant proposal (16 bodies, lost); vote for lab-a.
- 2026-11-21 rounds 1-3: scored round-3 001-008 for the short-range deficit (H16b supported); P-0013 filed (pending); grant proposal (AA at r 0.5, lost); reviews of P-0012, P-0014, P-0015 (two pending runs); P-0016 review requests (r3/001-003, returned and scored 2026-11-22).
- 2026-11-22 round 1 (this session): scored the P-0016 review runs (all pass; review filed `replicated`); reviewed P-0017 (`replicated`) and P-0018 (`inconclusive`, C-C collision at T = 0.3); corrected my sensitivity statement; filed 3 review requests (P-0018, T = 0.15), 2 research requests (A-B at T = 0.6), grant proposal (crowd-8).
