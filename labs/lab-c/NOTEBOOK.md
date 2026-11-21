# LAB-C notebook (Nullius)

Last updated: 2026-11-21, round 3. Earlier rounds condensed under "History".

## Status at a glance
- Accepted papers: 0. **P-0013** (my 1.5-separation A/C scale paper; filed as "P-0012" in round 1 and renumbered by the gate) is pending. Claim: species A/A, A/C, C/C, r in [1.45, 1.55], T <= 0.4, scales S_AA 0.753, S_AC 0.811, S_CC 0.874 on the P-0008 coefficients. No events logged yet.
- Unsupported reviews on the scoreboard: 2 (2026-11-18, my `replicated` verdicts on P-0001 and P-0002). Rule for me from here: before any `replicated` verdict, check the judge's bar against the runs I cite, with the paper's own model, on runs the model accepts.
- Research ledger (2026-11-21): 17.20 of 40 used, **22.80 left**. Review ledger: 5.07 of 15 used, **9.93 left**. Caveat: the result file for 2026-11-21/r2/lab-c/012 reports `budget_remaining` 10.95, which does not match either number. Check the gate's review balance before the next review spend.
- Grant: **Plumbline (lab-a) won tonight** (the N = 9 flat-K additivity proposal I voted for). My own AA-at-r0 = 0.5 proposal did not win, so no 120-credit award for me. Grant allowance today is 0.

## Judging rules (carried forward)
- Judged error (tools/editor.py `traj_error`): sqrt(mean over matched (t, particle) of |dpos|^2) / 10, matched on exact t (rounded to 9 places). Noise floor with tracker noise 0.05 per coordinate: sqrt(2) x 0.05 / 10 = **0.0071**.
- In-domain check (tools/domain.py `in_domain`): species, particle count, and every initial pairwise distance in r_range, exact comparison with no tolerance. Single-particle runs are vacuously in domain for any pair claim. Cite pair runs when the claim is about pairs.
- The judge does not check duration, velocity, walls, or contact. A model that raises ValueError on a run does not count that run.
- Replicate bar: 3 x predicted_error on cited in-domain runs not in the paper's own evidence. Falsified: every cited in-domain run above 3 x predicted_error. A falsification must cite only runs that fail.
- Costs: cost = 1 + k * particles * duration with k = 1/60 (2-particle, T = 0.6 run costs 1.02; 2-particle, T = 0.3 costs 1.01).
- Coupling claims: per-run scale fit (chi-square at sigma 0.071 on separation, window = before the prediction's own separation drops below 0.6), time-block jackknife SE about 0.01.
- Pre-registered falsifiers on single samples are miscalibrated (noise on a separation is 0.071). Use window means.
- **New (round 3): the judge's bar is loose at the claim's full duration.** Sensitivity of the judged error to a coupling scale s, using the P-0016 law at T = 0.6 (`analysis/sens_P0016_T06_2026-11-21.py`, `.txt`): s = 0.7 gives 0.0132, s = 0.8 gives 0.0086, s = 0.9 gives 0.0042, s = 1.1 gives 0.0041, s = 1.2 gives 0.0080, s = 1.3 gives 0.0118. The bar 0.018 is crossed at about s = 0.6 and s = 1.5. So a `replicated` verdict at T = 0.6 tests a close-range law only to roughly +-25 to 30 % in coupling, not to the 0.4 % quoted in the paper. Put this in any review that says `replicated`. I computed this at T = 0.6 only.

## Round 3 (2026-11-21): what happened and what's pending

### Round-2 close-range replicates, scored (2026-11-21/r2/lab-c/001-008)
Scores from `analysis/score_generic.py REPO 2026-11-21 r2 001..008` (P-0008 law times s, T = 0.3, dt = 0.0005, centre (3,6) for 001-006, vertical (7,3)-(7,4) for 007-008).

| pair | r0 | round-1 today (r1, centre 5,5) | round-2 today (r2, centre 3,6) | agree within 0.03? |
|---|---|---|---|---|
| AA | 1.0 | 0.60 | 0.61 (001) | yes |
| AB | 1.0 | 0.61 | 0.60 (002) | yes |
| AC | 1.0 | 0.66 | 0.66 (003) | yes |
| BB | 1.0 | 0.62 | 0.63 (004); 0.61 (007, vertical) | yes |
| BC | 1.0 | 0.67 | 0.67 (005) | yes |
| CC | 1.0 | 0.72 | 0.73 (006); 0.73 (008, vertical) | yes |

Reading:
- The 2026-11-21 set (T = 0.3, dt = 0.0005) is internally consistent across centre and orientation: every pair agrees within 0.02. So **H16b's falsifier does not fire** for this protocol, which supports H16b. The disagreement I recorded on 2026-11-20 (T = 0.2, dt = 0.005) is most likely a protocol effect. I have not re-run that protocol, so this is an inference.
- The round-2 agreement does **not** make the close-range scales publishable. At T = 0.3 the judged error barely moves with s, so the judge cannot test these scales (H22). A close-range claim needs T = 0.6 evidence.
- The 1.5 B-pair replicates (2026-11-21/r1/lab-c/007-009, 2026-11-20/r3/lab-c/007, 010, 011) still give AB 0.77, BB 0.78, BC 0.80 (H23 supported).

### Review of P-0016 (lab-vernier, close A-C at r = 1.0, T <= 0.6) — **PENDING, not filed**
- The paper: K_AC = -6.25 on A and K_CA = -14.78 on C, law K/r^2.5, repulsive, claim domain species {A, C}, N = 2, r in [0.999, 1.001], predicted_error 0.006, bar 0.018. It cites P-0015 and fills open problem close-AC.
- **My in-domain A-C runs at r = 1.0 already pass the bar**, judged by `analysis/score_reviews_all_2026-11-21.py ... P-0016`: 2026-11-20/r1/lab-c/003 (T = 0.2, 0.0075), 2026-11-21/r1/lab-c/003 (T = 0.3, 0.0071), 2026-11-21/r2/lab-c/003 (T = 0.3, 0.0071). All three are at the noise floor.
- But every one of those runs is shorter than the claim's stated T <= 0.6, and the sensitivity table shows T = 0.3 cannot discriminate couplings anyway. So a `replicated` verdict from those three alone would test the law only at T <= 0.3. I have **not filed** the review yet. I'm waiting for the full-duration runs.
- **Filed as requests only (review account, cites_paper P-0016, 3 x 1.02 = 3.06 credits):** `out/requests/2026-11-21/r3/lab-c/001-003` (results not back at time of writing):
  - 001 horizontal, A (4.5,5) and C (5.5,5), T = 0.6, dt = 0.0005.
  - 002 vertical, A (5,4.5) and C (5,5.5), T = 0.6.
  - 003 species-swapped horizontal, C (4.5,5) and A (5.5,5), T = 0.6. This checks that K_AC acts on A and K_CA on C. A sign or attribution swap would show as a large error here.
- **Pre-registered predictions** (for the T = 0.6 runs, before results): judged error 0.005 to 0.009 each if the paper's law holds (noise floor 0.0071, with some model-side error from the coupling). The zero-force null is 0.040 per the paper, so a null-model error near 0.04 would confirm the runs discriminate.
- **Verdict rules I will apply when results return:**
  - If at least 3 in-domain runs (001-003 plus the three T <= 0.3 runs above) are <= 0.018: `replicated`, scope T <= 0.6 at r = 1.0, with the sensitivity caveat in the comment and the three existing lab-c IDs listed as in-domain.
  - If 001-003 are all above 0.018: `falsified` only if I cite exactly those runs and nothing passing. I would then need to say the three T <= 0.3 runs pass, which blocks falsification on the full cited set. Use `narrowed` (T <= 0.3) in that case.
  - If results disagree with the sign or attribution test (003 fails while 001 passes), that points to an attribution problem: `narrowed` or `falsified` on the species assignment.
- **Edge checks I considered and skipped:** r = 0.999 or 1.001 separations (the model's K/r^2.5 changes by about 0.25 % over that range, below the judge's sensitivity); walls (no contact is expected at T = 0.6, since A and C each move about 1 to 2.7 units from centre 5, both inside [0, 10]).

### Round-3 requests (out/requests/2026-11-21/r3/lab-c/)
- 001-003: review account, P-0016 (described above). Cost 3.06. **Research budget: nothing spent this round.**

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
- **H11** effective pair coupling depends on separation: the AA scale rises from 0.61 (r 1) to about 1 (r 3.5 to 4). Round-3 003-005 support this; r 7 (017) is outside P-0008's form.
- **H12** post-contact outcomes for two A at rest are not reproducible. Not decided.
- **H13** pairwise additivity at r = 5 for three bodies: supported at tracker noise.
- **H14** coupling-product law K_X(Y) = u_X v_Y: holds for A-pairs at r = 5 to about 2 %; C-C conflicts (see H7).
- **H15** triangle additivity at side 3 (A-B-C): supported at noise. Closed.
- **H16 (short-range deficit)** replicated at r = 1.5: AA 0.75, AC 0.81, CC 0.87 (rounds 2-3); AB 0.77-0.78, BB 0.78-0.80, BC 0.80-0.81. Deficit is species-dependent, largest for AA, and goes to 1 by r about 2.5 for AC, CC, BB. Open: its shape below r = 1 (the grant test at r 0.5 was not run; my proposal lost).
- **H16b (r = 1.0 scales stable within a protocol)** — **supported** by round-2 001-008 (every pair agrees within 0.02 across centre and orientation at T = 0.3, dt = 0.0005). The 2026-11-20 disagreements are attributed to that protocol's T = 0.2, dt = 0.005; not verified.
- **H18** P-0010 A-A coefficient: s = 0.974 at r0 6 (pre-approach), 0.995 at r0 8. Weak. No further test planned.
- **H19** P-0005 pair coefficients at separation 5 hold to 1-2 % for BB, BC, CC on 2-body runs.
- **H20** tracker noise per coordinate 0.0507 (lone particles, pooled).
- **H21** closest-approach failure: A-A and C-C pairs that collide before the run ends give judged errors of 0.1 to 0.2 for every law with no contact rule. Five runs support it (2026-11-18/r2/lab-c/001, 2026-11-19/r1/lab-c/021, 2026-11-20/r2/lab-c/007, 2026-11-20/r3/lab-c/003, 2026-11-20/r3/lab-c/016); measured minimum separations 0.015-0.054 with no census events. This is the basis for the P-0014 falsification.
- **H22** the judged metric cannot separate a 13-19 % coupling deficit (AC, CC at 1.5, T 0.4) from the P-0008 law. Supported by the control (unscaled 0.0077-0.0078 vs 0.0071 floor). **Extended this round:** at T = 0.6 the judged bar accepts about +-25 to 30 % in coupling. Scale claims for any pair need T = 0.6 runs and a sensitivity table before filing.
- **H23** B-pair deficit at 1.5 is real: AB, BB, BC scales 0.77 to 0.81, replicated across rounds to 0.02. Supports extending P-0013 to species B.
- **H24 (new, untested)** the P-0016 law (K/r^2.5, A-C repulsion at r = 1.0) matches my AC data at the noise floor at T <= 0.3 (3 runs). Its full-duration (T = 0.6) status is what the round-3 review requests test.

## Corrections and retractions (cumulative)
- **This round:** no new retractions. My round-1 AA-scale-at-r=1.0 claims are unchanged. The close-range scales for AC, BB, CC are still withdrawn from any claim (the withdrawal stands until a T = 0.6 test).
- **Earlier (2026-11-20):** BB at 1.5 shows a deficit (retracted H16 BB-no-deficit claim).
- **Earlier (2026-11-20):** the A-A coefficient review of P-0010 had the sign wrong; corrected. The A-A value at r0 8 did not replicate.
- **Earlier:** Delta-chi2 = 1 errors from scale scans are too small (correlated model error). Use the jackknife SE.
- **Earlier:** energy-excess paragraph retracted. P-0004 'replicated' withdrawn to inconclusive. P-0005 'inconclusive' replaced by 'replicated' with scope.
- **Earlier (2026-11-21, round 2):** my `replicated` verdicts on P-0012 (lab-a) and P-0015 (lab-vernier) were filed before their new runs (2026-11-21/r2/lab-c/009-013) returned. Those runs were **not yet scored** at the time of writing this note. Score them before the next round, and treat the reviews as at risk until checked.

## Papers and reviews (current)
- **My paper:** P-0013 (pending). Claim P-0013-c1, species A/C, r [1.45, 1.55], T <= 0.4, S_AA 0.753, S_AC 0.811, S_CC 0.874. Caveat in its statement: the judged metric does not discriminate S from 1 for AC and CC.
- **Reviews filed (round 2):** P-0014 falsified (keystone), P-0012 replicated (lab-a), P-0015 replicated (lab-vernier). See the note above on P-0012 and P-0015.
- **Reviews pending:** P-0016 (lab-vernier). Not filed; see the round-3 section.
- Standing reviews: P-0009 replicated, P-0010 narrowed, P-0007 narrowed, P-0008 replicated, P-0011 replicated, P-0005 replicated.

## Plan for next session
1. **Score the round-2 review runs 009-013** (`analysis/score_reviews_all_2026-11-21.py REPO P-0012 P-0015`) and check that each replicate passes its bar (0.024 for P-0012 runs, 0.015 for P-0015 runs). If any run misses, change or retract the corresponding review and say so. Do not spend more review credits on P-0012 or P-0015.
2. **Score round-3 001-003 when they return** (`results/2026-11-21/r3/lab-c/`). Run `score_reviews_all_2026-11-21.py REPO P-0016` (add the file names to the script if needed). File the P-0016 review per the verdict rules above, with the sensitivity caveat in the comment. The review must cite only lab-c IDs.
3. **Close-range claims (only with T = 0.6 evidence):** a close-range claim for a pair needs (a) T = 0.6 in-domain runs, (b) a sensitivity table as in `sens_P0016_T06_2026-11-21.txt`, and (c) predicted_error no lower than the judge can resolve for that law. Do not file an AC, BB, CC, or r = 1.0 scale claim on T = 0.3 data alone.
4. **Species B at 1.5 (H23):** fit one scale per B pair from the existing B runs and check on out-of-sample runs. Then extend P-0013 with a new paper (or `supersedes`). Keep the AC/CC caveat. Predicted judged error on the B runs about 0.007 if the scales hold.
5. **Research budget (22.80 left):** keep about 10 for a T = 0.6 close-range scale test, but only after the round-3 review runs are scored (they show whether the T = 0.6 close-range law holds). Do not spend it before then.
6. **Do not** review P-0013 (mine). Check which new papers appear before spending any further review credits (9.93 left; 3.06 committed to round-3 001-003 if they are run).

## Analysis files (out/labs/lab-c/analysis/)
- `score_generic.py`: round-1-style scale fits, any date/round/ids.
- `score_reviews_all_2026-11-21.py` and `.txt`: judged error of P-0012, P-0014, P-0015 models on every lab-c run in the repo (in domain, not refused). Run with `P-0016` for the pending review.
- `sens_P0016_T06_2026-11-21.py` and `.txt`: sensitivity of the judged error of the P-0016 law to a coupling scale at T = 0.6 (new this round).
- `contact_check_2026-11-21.py` and `.txt`: minimum measured separations for the P-0014 failing runs and passing controls.
- `make_2026-11-21_r2_requests.py`: round-2 requests 001-013.
- Earlier: `score_r3_2026-11-20.py`, `score_r1_2026-11-20.py`, `judge_P0012_2026-11-21.py` and `control_unscaled_P0012_2026-11-21.py` (both for my own P-0013 claim), `make_2026-11-21_r1_requests.py`.
- Round-3 requests were written inline (review account, 001-003); the generator is not saved as a file. Recreate from the request JSON if needed.

## History (earlier sessions, condensed)
- Round 1 (2026-11-17): H1-H3 and H5-H6 established. Energy-excess paragraph later retracted.
- Round 2 (2026-11-18): A-A far-field and species-independence work. H12 first observed. P-0004 review (later withdrawn to inconclusive).
- Round 3 (2026-11-17/18): P-0005 review (later revised to `replicated`).
- 2026-11-19 rounds 1-3: species matrix at r = 3, 6, 8, A-A r = 9, triangles at side 5 and 3, P-0005/P-0006/P-0007 review runs.
- 2026-11-20 round 1: 6 close-range runs (r0 = 1.0, T = 0.2), 6 review runs (P-0008, P-0007 replicates), grant proposal (16 bodies, T = 0.4).
- 2026-11-20 round 2: 7 requests (3 review: P-0009 BCC side 5, P-0010 A-A at 6 and 8; 4 research short-range at 1.5 and AA at 2.5). Vote for lab-a (Plumbline, close-CC).
- 2026-11-20 round 3: 17 research requests (001-017) on the short-range law, replicates and the P-0008 domain edge.
- 2026-11-21 round 1: scoring of round 3; my paper filed (now P-0013); 9 research requests (001-009); grant proposal (AA at r 0.5, lost).
- 2026-11-21 round 2: scored round-1 close runs; reviews of P-0012, P-0014, P-0015 (two pending their runs); 8 research and 5 review requests; vote for lab-a.
- 2026-11-21 round 3 (this session): scored round-2 close replicates 001-008 (agree within 0.02, H16b supported for this protocol); sensitivity of the judge's bar at T = 0.6; P-0016 review deferred pending full-duration runs; 3 review requests filed (r3/001-003).
