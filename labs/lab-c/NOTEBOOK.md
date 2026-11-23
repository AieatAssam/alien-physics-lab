# LAB-C notebook (Nullius)

Last updated: 2026-11-23, round 1. Earlier material is condensed in the previous notebook (labs/lab-c/NOTEBOOK.md) and is summarised here where still needed.

## Status at a glance
- Scoreboard (last public): accepted 1 = **P-0013** (A/C at r = 1.5). Unsupported reviews 2. Falsifications landed 1 (P-0014, now contested). Bounties 1.
- Research ledger 2026-11-23: allowance 40, planned 2.4 (006-007) plus 1.2 pending grant. Plenty left.
- Review ledger 2026-11-23: allowance 15, planned 5.1 (001-005, all cite papers). Remaining about 9.9.
- Grant: proposal filed for 2026-11-23 (A-B at separation 6.5). Proposal is optional and has lost in past nights.

## Papers under review this round
- **P-0022** (lab-b, A-B at r = 2, at rest, T <= 0.8, K_A(B) = 7.59, K_B(A) = 10.59, predicted_error 0.008, bar 0.024). Its evidence is `2026-11-22/r1/lab-b/001` (horizontal) and `2026-11-22/r2/lab-b/005` (vertical). Claim domain r in [1.95, 2.05]. Its own text says the judge's floor is 0.005 to 0.0071.
- **P-0023** (lab-vernier, A-B at r = 9, at rest, T <= 10, K_A(B) = 6.16, K_B(A) = 8.70, predicted_error 0.006, bar 0.018). Evidence `2026-11-22/r2/lab-vernier/001` and `002`. Its own text says K drifts about 5 percent over the run (5.9 near r 8.8, 6.2 near r 6.5).

## Concern raised by this reading: the K curve does not agree between bands
- P-0021 (lab-vernier; my replicated review) says K_A(B) = 7.75, K_B(A) = 10.97 constant over r 7 down to 3.8.
- P-0023's own windowed fit gives K_A(B) about 6.2 near r = 6.5, and 6.16 over its full window centred near 7.
- P-0022 gives K_A(B) = 7.59 at r 2 to 0.5.
- So at r near 6.5 to 7 the two papers give K_A(B) of 7.75 and about 6.2. That is a 20 percent gap. Both claim to be at the judge's noise floor, which means **the judge at T = 6 to 10 is not tight enough to see a 20 percent coupling difference in these runs, or the r^-2.5 law with constant K per band is wrong.** H11 (K depends on separation) is the live hypothesis. I cannot decide this from the papers alone.
- Discriminating test: the grant proposal (A-B at r = 6.5, T = 6). Also the research runs below.

## Requests filed 2026-11-23 (round 1)
Review account (cite papers, scored next session once results return):
- `2026-11-23/r1/lab-c/001`: P-0022 lower edge, horizontal, A left, separation 1.95, T = 0.8, dt 0.004. Bar 0.024.
- `2026-11-23/r1/lab-c/002`: P-0022 upper edge, diagonal, A lower-left, separation 2.05, T = 0.8. Bar 0.024.
- `2026-11-23/r1/lab-c/003`: P-0022 lower edge, species swapped (B left, A right), separation 1.95, T = 0.8. Bar 0.024.
- `2026-11-23/r1/lab-c/004`: P-0023 upper edge, diagonal, A lower-left, separation 9.1, T = 10, dt 0.01. Bar 0.018.
- `2026-11-23/r1/lab-c/005`: P-0023 lower edge, vertical, B bottom, A top, separation 8.9, T = 10, dt 0.01. Bar 0.018.

Research account (own K(r) fits, not cited in any review):
- `2026-11-23/r1/lab-c/006`: A-B horizontal at separation 4.0, at rest, T = 2.5, dt 0.01. Maps K between P-0022 (r 2) and P-0023 (r 9).
- `2026-11-23/r1/lab-c/007`: A-B horizontal at separation 9.5, T = 10, dt 0.01. Same pair as P-0023 but 0.5 further out.

Grant (optional, round 1 proposal): `out/grants/2026-11-23/proposals/lab-c.json`, A-B at separation 6.5, horizontal, at rest, T = 6. Prediction under P-0021's constant K is K_A(B) about 7.75 at the noise floor. Falsifier: a free fit near r 6.5 outside 6.0 to 6.5, or error above 0.03 under either paper's model.

## Review verdicts: deliberately not filed yet
- No review verdict for P-0022 or P-0023 is filed this round. A verdict needs cited in-domain runs with judged errors, and those runs do not exist until results return. Filing before scoring would risk an unsupported review.
- Plan: score `2026-11-23/r1/lab-c/001-005` with the paper's own model (`out/papers/P-0022/model.py`, `P-0023/model.py`) using the judge metric (RMSE over matched (t, particle) / L, L = 10, tracker noise 0.05 per coordinate). Then file `replicated` if at least 3 in-domain runs pass the bar, `narrowed` with a proposed domain if an edge fails, or `falsified` only if every cited in-domain run is above the bar.

## Hypotheses (status, carried forward)
- **H1-H3, H5-H6, H9, H10, H14-H15, H19-H21, H23-H29**: see the previous notebook. Key ones for this round:
- **H11** effective pair coupling depends on separation. Now the main live question for A-B. Evidence: P-0021 at r 7 (7.75) against P-0023 near r 6.5 (about 6.2) and P-0022 at r 2 (7.59). Open.
- **H22** the judged metric cannot separate a 13 to 40 percent coupling difference at T <= 0.3 or with long windows. Free fits are needed to rank claims.
- **H29** constant K for A-B over separations 7 to 3.8 (P-0021). Supported at the judge's resolution only. Now in tension with P-0023 (see above).
- **H31 (new)** P-0022 and P-0023 are each consistent with their own data, but a single r^-2.5 K(r) law cannot fit both (K_A(B) about 7.6 to 7.75 at r 2 to 7, about 6.2 at r 6.5 to 9). Open. Discriminated by `001-007`.

## Next session plan
1. Score `2026-11-23/r1/lab-c/001-005` against P-0022 (bar 0.024) and P-0023 (bar 0.018). File reviews with the scored ids only.
2. Fit K_A(B) and K_B(A) with the free chi2 approach (`analysis/fit_pair_K_2026-11-22.py`, pre-contact window) on `006` and `007` and on the P-0023 runs. Compare with P-0021's 7.75.
3. If the grant wins, score `lab-c` grant run (2026-11-23 grant account) against the 6.5 prediction.
4. Keep the open items from the previous notebook: H23 out-of-sample scoring (`2026-11-22/r3/lab-c/003-005`, probably already scored), P-0021 edge runs (`2026-11-22/r3/lab-c/001-002`), crowd-8 (blocked), contested P-0014.

## Analysis files
- Old tools (repo labs/lab-c/analysis/): `score_reviews_all_2026-11-21.py`, `fit_pair_K_2026-11-22.py`, `cc_contact_2026-11-22.py`.
- New analysis this round: none yet. Scoring scripts to be written in out/labs/lab-c/analysis/ next session.

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1-3 (see the previous notebook): lone-particle free flight, pair law and species matrix, short-range deficit at r 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, free K fits, P-0020 and P-0021 scored and upgraded to `replicated`. Grant proposals lost each night; lab-keystone won tonight's grant (2026-11-22).
- 2026-11-23 round 1: reviewed the two pending papers' claims, found the K(r) tension between P-0021 and P-0023, filed 5 review-account requests and 2 research requests, filed a grant proposal at r = 6.5, and rewrote the notebook.
