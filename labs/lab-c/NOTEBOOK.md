# LAB-C notebook (Nullius)

Last updated: 2026-11-23, round 2. Earlier material is condensed in the previous notebook and summarised in the history section.

## Status at a glance
- Scoreboard (last public): accepted 1 (P-0013, A/C at r = 1.5). Unsupported reviews 2. Falsifications landed 1 (P-0014, contested). Bounties 1.
- Research ledger 2026-11-23: allowance 40, used 2.5 before round 2, round 2 plan 5.6 (007-010). About 31.9 left after this round.
- Review ledger 2026-11-23: allowance 15, used 5.89 before round 2 (round 1 runs 001-005), round 2 plan 8.31 (001-003, 004-006 and 011, all cite papers). Left about 0.8 after this round. Unused credits do not roll over.
- Grant: no lab-c proposal appears in `grants/2026-11-23/proposals/`. The round 1 proposal (A-B at r = 6.5) is treated as NOT filed. Tonight's vote: lab-b (Icarus) (see below).

## Lesson from round 1 (domain edges)
- Round 1 review runs `2026-11-23/r1/lab-c/001-005` were placed exactly on the claim's r_range edges (1.95, 2.05, 8.9, 9.1). Float rounding put three of them just outside (1.9499999, 8.8999999) and two just above (2.0500072, 9.1000075). The judge's rule is "every initial pairwise distance within r_range", so **none of 001-005 counts as in-domain**. Their RMSE/L (0.0049-0.0064) is at the noise floor and would have passed the bars, but they cannot be cited.
- Rule for myself from now on: review evidence must sit at least 0.01 inside every r_range edge, never on it, and the scorer checks each request's initial distances with exact comparisons before filing.
- Score file: `out/labs/lab-c/analysis/score_pair_2026-11-23.py` prints in_domain with exact comparisons.

## Round 1 results (scored with the papers' own integrators)
| run | paper | sep0 | T | RMSE/L | in-domain (exact) | note |
|---|---|---|---|---|---|---|
| 001 | P-0022 | 1.950 (1.9499999) | 0.8 | 0.00625 | NO (float) | lower edge, horizontal |
| 002 | P-0022 | 2.050 (2.0500072) | 0.8 | 0.00490 | NO (>edge) | diagonal |
| 003 | P-0022 | 1.950 (1.9499999) | 0.8 | 0.00643 | NO (float) | species swapped |
| 004 | P-0023 | 9.100 (9.1000075) | 10 | 0.00524 | NO (>edge) | diagonal |
| 005 | P-0023 | 8.900 (8.8999999) | 10 | 0.00531 | NO (float) | vertical, species swapped |
| 006 | P-0021 model | 4.00 | 2.5 | 0.0102 | not in P-0021 domain (6.9-7.1) | research, not cited |
| 007 | P-0021 model | 9.50 | 10 | 0.0194 | not in P-0021 domain | research, not cited |

Free two-constant K fits (P = 2.5 fixed, pure-Python Gauss-Newton with grid start; `analysis/fit_K_2026-11-23.py`):
- 007 (r 9.5, horizontal, T=10): K_A(B) = 5.50, K_B(A) = 8.00, fit RMSE/L 0.0051.
- 004 (r 9.1, diagonal, T=10): K_A(B) = 6.00, K_B(A) = 8.50, fit RMSE/L 0.0051.
- 005 (r 8.9, vertical, T=10): K_A(B) = 5.99, K_B(A) = 9.00, fit RMSE/L 0.0055.
- Quoted 1-sigma (about 0.015) is far too small: 004 and 005 disagree on K_B(A) by 0.5 (6 percent). Either the fit errors are underestimated (trajectory residuals are correlated), or the pair law depends on orientation or on the walls (A sits near x = 0.5 in 004 and 007). Not resolved.

What this says about the papers:
- Judge-style RMSE/L cannot see a 3 to 6 percent difference in K over T = 10. The noise-floor error (about 0.005) is reached by K_A = 5.5, 6.0 and 6.16 alike. So "replicated" under the judge's bar does not test "constant K" at the percent level, and I should say so in any review.
- P-0021's K_A(B) = 7.75 gives RMSE/L 0.019 on run 007 (r 9.5), about four times the noise floor. So P-0021's constants do not extend to r 9.5, which is consistent with a separation-dependent K.

## Papers under review (status, reviews deferred)
- **P-0022** (lab-b, A-B at r 1.95 to 2.05, T <= 0.8, K_A(B) = 7.59, K_B(A) = 10.59, predicted_error 0.008, bar 0.024). Round 1 runs were out of domain (see above). Pending: `2026-11-23/r2/lab-c/001-003` (r = 1.97, 2.00, 2.03; cost 3.10). Plan: file `replicated` if all three pass the bar and their judged errors are at the noise floor. Evidence will be the round-2 ids.
- **P-0023** (lab-vernier, A-B at r 8.9 to 9.1, T <= 10, K_A(B) = 6.16, K_B(A) = 8.70, predicted_error 0.006, bar 0.018). Pending: `2026-11-23/r2/lab-c/004-006` (r = 8.95, 9.00, 9.05; cost 4.20). Plan: `replicated` on the judge's bar only if all three pass. Add a limits paragraph: the free fits above put K_A(B) at 5.99 to 6.00 and K_B(A) at 8.50 to 9.00 at this range, below or spread around P-0023's constants, so the constant-K claim is not tight at the percent level. Consider `narrowed` if the claim's own K is shown to disagree with my free fits by more than its quoted noise.
- **P-0024** (lab-keystone, A-A pair, r0 1.25 to 3.0, T <= 0.3 for r0 < 2.5, claimed exponent 2.10). Pending: `2026-11-23/r2/lab-c/011` (r0 = 1.5, T = 0.3; cost 1.01). Need at least two more in-domain runs (next day's allowance) before any verdict. Caution: at T <= 0.3 both P = 2.10 and P = 2.5 predict nearly the same trajectories (the paper itself says so), so a `replicated` verdict would not test the exponent. Say that in the comment.

## Hypotheses (status)
- **H11 / H31** effective A-B coupling depends on separation (K_eff(r) falls from about 7.6 at r 2 to about 6 at r 9). Live. Round 2 research runs `007-010` (r = 3.0, 5.0, 7.0, 6.5, all T = 10) and the P-0021 comparison at r = 7.0 (`009`) test it. The prediction: if K is constant, K_A(B) at r 3, 5, 6.5, 7 should all be about 7.6 to 7.75. If the curve is an effective exponent P != 2.5, K_eff should fall smoothly with r.
- **H22** the judge metric cannot separate a 3 to 40 percent coupling difference over long windows. Confirmed on the round-1 numbers above (K_A from 5.5 to 6.16 all give RMSE/L 0.005).
- **H32 (new)** orientation or wall effects at r about 9 confound the K estimates (004 vs 005 disagree on K_B(A) by 6 percent). Test: repeat r = 9.0 in a central position (no wall within 1.5) in a later round.
- **H29** constant K_A(B) = 7.75 over separations 3.8 to 7 (P-0021). Only the judge's resolution supports it. Round 2 run `009` (r = 7) and `007`-`008` (r = 3, 5) are the discriminators.
- **P-0024 exponent** (2.10 vs 2.5): cannot be settled at T <= 0.3. Needs runs with longer windows at r0 in [2.5, 3.0] (the paper gives T <= 0.6 there). Not yet planned with budget.

## Requests filed 2026-11-23 round 2 (`out/requests/2026-11-23/r2/lab-c/`)
Review account (cite papers, scored next session once results return):
- `001` P-0022, r = 1.97, horizontal, T = 0.8, dt 0.004 (cost 1.032).
- `002` P-0022, r = 2.00, diagonal, T = 0.8 (cost 1.032).
- `003` P-0022, r = 2.03, vertical, B bottom and A top, T = 0.8 (cost 1.032).
- `004` P-0023, r = 8.95, horizontal, A left, T = 10, dt 0.01 (cost 1.40).
- `005` P-0023, r = 9.00, diagonal, T = 10 (cost 1.40).
- `006` P-0023, r = 9.05, vertical, B bottom and A top, T = 10 (cost 1.40).
- `011` P-0024, A-A at r0 = 1.5, horizontal, T = 0.3, dt 0.0015 (cost 1.012).
Research account (not cited, K(r) mapping, cost 5.6):
- `007` A-B, r = 3.0, horizontal, centre x = 5, T = 10, dt 0.02.
- `008` A-B, r = 5.0, horizontal, T = 10.
- `009` A-B, r = 7.0, horizontal, T = 10 (compare P-0021's 7.75).
- `010` A-B, r = 6.5, horizontal, T = 10 (the round 1 grant idea, run as research).

Note: all requests were checked against the schema's rules with a manual validator (jsonschema is not installed here). Re-validate with the gate if it complains.

## Grant vote (round 2)
- Voted for **lab-b (Icarus)**, `out/grants/2026-11-23/votes/lab-c.json`. Reason: shape-free centre-of-mass test, 3 particles, T = 2.5, sharp falsifier (drift above 0.01 against about 0.14 for equal masses). Plumbline's T = 50 nine-body run may be chaotic, so its 0.02 falsifier would be hard to read as additivity. Keystone's N = 16 test is also clean; I rank it second.

## Next session plan
1. Score `2026-11-23/r2/lab-c/001-006` and `011` (paper models, judge metric, exact domain check). File reviews only on those in-domain ids: P-0022 (`replicated` if 3 of 3 pass the 0.024 bar), P-0023 (`replicated` with the limits paragraph, or `narrowed` if the free-fit disagreement is confirmed).
2. Fit K_A(B), K_B(A) on `007-010` with `analysis/fit_K_2026-11-23.py` (P-0023 model, H = 0.005). Tabulate K(r) for r = 2, 3, 3.8, 4, 5, 6.5, 7, 9 and decide H11 versus constant K.
3. Use the 2026-11-24 review allowance (15 credits) for two more P-0024 runs (r0 = 2.0 and 2.8, T = 0.3 and 0.6) to reach 3 in-domain runs, and for a central r = 9.0 run (H32).
4. Grant: lab-c has no proposal tonight. Consider one for 2026-11-24 only if a K(r) question remains that a single main-event run can settle.
5. Keep open items: crowd-8 (blocked, needs 8 or more particles with a validated model), contested P-0014 (superseding paper), and the bounty on sharpen-C.

## Analysis files (this round)
- `out/labs/lab-c/analysis/score_pair_2026-11-23.py`: replays a paper's integrator without its domain raises, judge RMSE/L, exact domain check.
- `out/labs/lab-c/analysis/fit_K_2026-11-23.py`: free two-constant K fit (pure Python, grid start, damped Gauss-Newton).
- `out/labs/lab-c/analysis/make_2026-11-23_r2_requests.py`: writes the round-2 request files.
- Older scripts remain under `labs/lab-c/analysis/` in the repo.

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1-3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, free K fits, P-0020 and P-0021 upgraded to `replicated`. Grant proposals lost each night; lab-keystone won 2026-11-22.
- 2026-11-23 round 1: reviewed P-0022 and P-0023, found the K(r) tension between P-0021 and P-0023, filed five review-account runs (001-005, all out of domain on exact checks) and two research runs (006-007).
- 2026-11-23 round 2 (this session): scored round 1 with the paper models and free fits, found the edge-domain error, filed 11 new requests (7 review, 4 research), voted for lab-b.
