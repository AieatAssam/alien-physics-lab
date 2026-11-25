# LAB-A notebook (Plumbline)

Season 1, chamber [0,10]^2, species in use A, B, C (`protocol/season.json`), difficulty 2.
Persona: cautious experimentalist. Every run is repeated before it is trusted. Narrow claims, tight domains.

## Judge notes that govern my claims

- The domain check covers species, particle count and initial pair separations. Duration is not in the domain, so a run at a different T can count as in-domain. I still cite runs inside the claim's own duration window, so reviews stay clean. A cited run is judged on its whole trajectory, so do not cite a run that reaches contact inside the claim's window.
- Edge runs: a run placed exactly on a domain edge can fail the paper's own check by float rounding. Place review-account edge runs 0.01 inside the edge. In my own models I accept a 1e-3 tolerance at the edge.
- **The judged metric is coarse.** Noise floor: tracker noise 0.05 per coordinate gives a correct model RMSE/L of about 0.005 (observed 0.0049 to 0.0051 on correct models). A 3% error in K at separation 3 to 5 is invisible to the judge. **My decisions on K rest on per-run K fits (chi2 at sigma 0.05, reduced chi2 about 1), not on the judged error.**
- **Do not state predicted_error below about 0.005.** The sharpen-A/B/C bounties ask for 0.0025 or less, below the floor a correct model reaches, so I will not claim them.
- Review evidence is judged on my own request ids only. Runs that test a paper use `account: review` with `cites_paper`.
- Cost is `1 + 0.02 * N * T`. Short runs are almost free: a pair at T = 0.3 costs 1.01 credits, a 16-particle run at T = 1 costs 1.32. The grant (120) is only needed for long or large runs.
- Scripts: numpy and jsonschema are installed in the sandbox (`python3 -m pip install numpy jsonschema` if missing). Run with `python3 -I`.
- **Per-run K is a trajectory average, not a local value, when the pair falls through a wide range.** Use short runs (T <= 1.5) for any local K(r) claim.
- **A constant-K fit cannot test a non-constant K(r) table.** Fitting a constant K over a time window that spans many separations gives chi2/dof in the thousands (the table varies by 35% over [5, 9]). Compare candidate laws over the whole trajectory instead.
- **A local acceleration fit cannot resolve a short run (new, 2026-11-25).** At tracker noise 0.05 and T = 0.3, a pair at separation 2 moves each particle about 0.14. A quadratic fit gives per-particle K with sigma 19 to 56 (against K about 18). Short runs only test the force through a whole-run scale fit against a full simulation. Longer runs (T 0.6 or more) are needed for local work.
- **Fall windows must end before contact.** The simulator has no contact model in my code, and the pair reaches separation 0.4 at t about 3 in a fall from r0 = 5. Judge windows end at the first measured separation below 2.5.

## Budget ledger

### Closed days
- 2026-11-17: research 23.30 of 40; review 6.00.
- 2026-11-18: research 30.38 of 40; review 6.20 (P-0002 review).
- 2026-11-19: research 13.12 of 40; grant 120 awarded, 33.00 spent on `2026-11-19/r3/lab-a/001` (16 particles, T = 100). Voted lab-keystone.
- 2026-11-20: research 9.19 of 40; review 13.90 of 15; grant 1.02 of 120. Voted lab-keystone.
- 2026-11-21: research 31.37 of 40; review 12.42 of 15; grant 1.09 of 120. Voted lab-vernier.
- 2026-11-22: research 32.32 of 40; review 6.75 of 15.
- 2026-11-23: research 37.78 of 40; review 13.80 of 15. Keystone won the grant; my proposal lost.
- 2026-11-24: research 27.44 of 40 (round 1 13.12, round 2 9.90, round 3 4.42, 12.56 left unspent at close); review 11.94 of 15 (P-0025, P-0026); grant 2.80 of 120 (`r3/001-002`, the radial fall main event). **Won the 2026-11-24 grant** (3 votes from other labs; record `grants/2026-11-24/award.json`). 117.20 of the award is unspent and expires with the award unless used in round 3 of 2026-11-24, which has closed.

### 2026-11-25 (today, rounds 1 to 3)
- Research: round 1 13.44 (`r1/001-013`, executed, scored below). Round 2 8.18 (`r2/005-012`, executed, scored below). Ledger at the start of round 3: 21.59 of 40 used, **18.41 left**. Round 3 files `r3/001-008` at an estimated 8.13 (planned, not yet run). Left after round 3 if all run: about 10.3.
- Review: round 2 4.32 of 15 (`r2/001-004`, P-0030 review). Round 3 filed the verdict (no further review runs needed; 10.68 of the review allowance is unspent and does not roll over). The review account has no other paper awaiting review.
- Grant: my proposal filed in round 1 (`out/grants/2026-11-25/proposals/lab-a.json`). Round 2 vote for **lab-c** (`out/grants/2026-11-25/votes/lab-a.json`, Nullius's close-approach proposal). Tonight's grant went to **lab-vernier** (16-body additivity test, 120 credits). I have no grant credits today.

## Results scored

Scored in round 2 with `out/labs/lab-a/analysis/score_round1_2026-11-25.py` (output `score_round1_2026-11-25.json`). Earlier scoring: `score_round3_2026-11-25.py` and `grant_check_2026-11-25.py` (round 3 and the fall check).

### Round 1 (2026-11-25, r1/001-013): close-range pairs and the falls

**Method departure from the pre-registration (stated up front).** The pre-registered rules used a local quadratic acceleration fit per run. At T = 0.3 that estimator is at the noise floor (per-particle K sigma 19 to 56). A first draft also doubled the acceleration (`a = 2*coef` with a 0.5 t^2 design column), caught and fixed before any number was used. The rules are therefore applied to a whole-run scale s: the pair is simulated with K(r) = s * K_table(r) (P-0027 nodes, clamped at 17.683 below r = 3) and s is fitted to the tracker positions (sigma 0.05). s = 1.00 is the stated law. 1-sigma from Delta chi2 = 1.

Pair runs (s relative to the clamped table; chi2/dof at s = 1 in brackets):

| run | species | r0 | T | s (1 sigma) | chi2/dof at s=1 |
|---|---|---|---|---|---|
| 001 | A-A horiz | 2.0 | 0.3 | 0.885 (0.825, 0.950) | 1.09 |
| 002 | A-A diag | 2.0 | 0.3 | 0.860 (0.795, 0.920) | 1.07 |
| 003 | A-A horiz | 2.5 | 0.3 | 0.840 (0.720, 0.955) | 1.08 |
| 004 | A-A diag | 2.5 | 0.3 | 0.965 (0.850, 1.085) | 0.97 |
| 005 | A-A horiz | 3.0 | 0.3 | 1.000 (0.815, 1.190) | 1.08 |
| 006 | A-A diag | 3.0 | 0.3 | 1.150 (0.960, 1.335) | 1.00 |
| 007 | A-A horiz | 1.5 | 0.15 | 1.040 (0.915, 1.170) | 0.90 |
| 008 | A-A diag | 1.5 | 0.15 | 0.895 (0.765, 1.025) | 0.93 |
| 009 | B-B horiz | 2.5 | 0.3 | 0.31 (grid floor 0.30, upper 0.43) | 1.14 |
| 010 | C-C horiz | 2.5 | 0.3 | 0.655 (0.535, 0.770) | 1.05 |
| 011 | A-B horiz | 2.5 | 0.3 | 0.465 (0.345, 0.585) | 1.12 |

Pooled by separation (pairs of replicates): s(2.0) = 0.87 +- 0.05; s(2.5) = 0.90 +- 0.09; s(3.0) = 1.08 +- 0.13; s(1.5, T 0.15) uninformative (+- 0.13 per run).

**Pre-registered rules applied:**
- Rule 1 (table consistent at close range, all replicates within 5% of 1.00): **not triggered**. s(2.0) sits about 2.5 to 3 sigma below 1.
- Rule 2 (ratio above 1.25 at 2.0 and 2.5): **not triggered**. Measured s is below 1, not above.
- Rule 3: **applies (inconclusive as a claim)**. No claim on the close range today.

**What the close-range data say, without the rule.** The clamp that P-0027 and P-0028 use below r = 3 (K held at 17.68) overpredicts the measured force near r = 2 by about 13%. This agrees with H15 (A-A K at r0 1.0 is 10.5 to 11.5, not 18). It also means the clamped-table predictions below 3 used in P-0028's crowd runs are biased where pairs come within 3. The P-0028 claim's stated domain (initial pairs in [3, 9]) is not affected by this on its face, but its octagon min pair of 2.5 is inside the biased region. Replicates agree (001 vs 002 within 0.025; 003 vs 004 within 0.125, both inside 1 sigma).

**Power law P = 3.2 (K = 55.4 r^-0.7).** Rescaled, the same short runs fit it equally well at r = 2 (the scale comes out 0.44). Both shapes agree at r = 2, so the short runs cannot separate them. They differ at 2.5 to 3.5.

**Falls (`r1/012-013`), no free parameter, windows before contact (measured separation above 2.5).** The fall from r0 = 5 reaches separation 2.4 to 2.5 at t about 2.45 and goes to contact by t about 2.8.

| run | window | table chi2/dof | power law chi2/dof |
|---|---|---|---|
| 012 horiz | t 0 to 1.5 (n 76) | 1.00 | 1.01 |
| 012 horiz | t 1.5 to 2.0 (n 25) | 1.00 | 1.05 |
| 012 horiz | t 2.0 to end (n 21) | 0.90 | 1.77 |
| 013 diag | t 0 to 1.5 (n 76) | 0.90 | 0.90 |
| 013 diag | t 1.5 to 2.0 (n 25) | 1.22 | 1.34 |
| 013 diag | t 2.0 to end (n 23) | 0.98 | 2.70 |

Read: the table with no free parameter fits both falls through 2.5 to 3.5 at noise level. The power law (no free parameter) is worse, and clearly so from 2.0 on. The falls do not reach the clamp region below 2.5, so they do not test the clamp. The fall with the table is the best evidence today that the table shape is right at 2.5 to 4.5 (consistent with H41 and H32). Separately, the pair falls about 2 to 4% faster than the clamped table just above 2.5 (measured 2.34 vs predicted 2.46 at t = 2.5). That is within the scatter of one fall and is not claimed.

**Factorisation (exploratory, rule 4).** Run 011 (A-B) and run 009 (B-B) are scored against A-A at 2.5 (run 003, s = 0.84). Ratios of s: B-B 0.37 (upper 0.51), C-C 0.78, A-B 0.55. Under factorisation K_AB/K_AA = q_B/q_A and K_BB/K_AA = (q_B/q_A)^2, so the A-B ratio should be the square root of the B-B ratio: sqrt(0.37) = 0.61 against 0.55 measured. Consistent within the errors (about 0.1). H9 stays partially supported. The species-pair claim is not filed.

Round-1 requests: nothing else scored. P-0030 review runs are in round 2.

### Round 1 (earlier, pre-round-2 results)

P-0025 (lab-b, A-B table at r0 4 to 8): replicated on the stated bound, RMSE/L 0.00497 to 0.00506 (`r1/001-008` in 2026-11-24). A-A K(r) at separations 4 to 9 agrees with the table (per-run K, reduced chi2 0.98 to 1.10). Crowd-8 ring at T = 0.5 (`r1/019-020`): at the floor, not discriminating.

### Round 3 (pre-registered 2026-11-24; scored 2026-11-25)

Full table used for all comparisons: piecewise-linear P-0027 nodes (17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624 at r = 3..9). Table value at 3.5 is 17.692, at 4.5 is 17.768.

**Rule 1, replicates at 3.5 and 4.5: triggered. P-0027 narrowed.**

| run | sep | T | orient | K_fit | chi2/dof | table | dev |
|---|---|---|---|---|---|---|---|
| `r2/001` | 3.5 | 1.0 | horiz | 18.252 | 1.005 | 17.692 | +3.17% |
| `r3/003` | 3.5 | 1.0 | diag | 18.178 | 0.989 | 17.692 | +2.75% |
| `r2/002` | 4.5 | 1.5 | diag | 18.203 | 1.025 | 17.768 | +2.45% |
| `r3/004` | 4.5 | 1.5 | horiz | 18.244 | 1.022 | 17.768 | +2.68% |

Both pairs replicate high (above 17.9 at 3.5 and above 18.0 at 4.5), in both orientations. The pre-registered rule says narrow P-0027 to [5, 9]. **Done: P-0029** (see Papers). The [3, 5) part of the table is withdrawn.

**Correction to round 2.** The round-2 scorer built the table with `np.interp` over nodes 3, 5, 7, 9 only, not all seven. Corrected round-2 deviations (full table): 3.5 horiz +3.17% (was +3.00%), 4.5 diag +2.45% (was +2.28%), 5.5 +0.5% (was +0.9%), 6.5 -0.1 to -0.4%, 7.5 0.0% (was +0.2%), 8.5 -1.8% (was -1.6%). Round-2 verdicts are unchanged. Rule 1 still triggered (3.5 and 4.5 miss the 2% bar).

**Rule 2, crowd-8 octagon (`r3/005-006`): PASSED.**
- Table pairwise chi2/dof 0.999 and 0.999 (threshold 1.5). Constant K=17.7 gives 1.052 and 1.052.
- Constant minus table: 1682 and 1678 per run (threshold 9).
- Judged-style RMSE/L: table 0.00500 both runs; constant 0.00513.
- Initial min pair 3.21 (inside [3, 9]). Measured min pair over the run 2.50 to 2.54, below the table's validated 3.0, clamped there.
- The crowd claim (P-0028) can add this geometry in a revision. **Not filed today.** The octagon and ring both use table values at 3 to 5, which are withdrawn above, and the round-1 close-range result (above) bears on the min-pair 2.5 segment. See Plan.

**Rule 3, radial fall (`r3/001-002`, the grant main event): reported, with a rule that could not be applied as written.** Pre-registered rule 3 asked for K(r) fits by windows with no exponent. A constant K fitted per window at P = 2.5 cannot test a non-constant table (see judge notes), so the windowed-constant fits are discarded. What the data do show:

| model | run | chi2/dof, t <= 9.2 | notes |
|---|---|---|---|
| free K/r^P (2 params) | 001 | 1.016 | P = 3.20, K = 55.4 |
| free K/r^P (2 params) | 002 | 1.051 | P = 3.18, K = 53.3 |
| P-0027 table, P = 2.5, no free parameter | 001 | per window: 1.01 (0-3), 1.01 (3-6), 1.06 (6-8), 1.11 (8-9.2) | |
| P-0027 table, P = 2.5, no free parameter | 002 | per window: 1.00 (0-3), 1.07 (3-6), 1.10 (6-8), 1.21 (8-9.2) | |

- Both models fit the pre-contact fall at noise level. **The fall does not separate a P = 2.5 table from a P = 3.2 power law over its full range.** It does show the table fits the fall from separation 9 down to about 5 with no free parameter (chi2/dof 1.00 to 1.10 through t = 8), and the residual grows only once the pair is below about 4.5, where the table is clamped at 3.
- Power-law over table force ratio at r = 3, 4, 5, 6, 7, 8, 9: 1.45, 1.19, 1.01, 0.95, 0.94, 0.96, 1.02. The two laws agree within about 5% over [5, 9]. They disagree at 3 to 4, where the table is an extrapolation from short runs (the 3.5 and 4.5 replicates above).
- Replicates agree: P 3.20 vs 3.18, K 55.4 vs 53.3 (4% apart, correlated with P).
- The free K/r^P fit is not my claim. It is a 2-parameter description, and a flexible shape could fit the fall equally well. P is not determined yet. Round-1 falls (above) add the 2.0-to-end window, which favours the table over the power law.

**Scaled-table fit: failed optimizer, discarded.** A one-parameter scale on the table returned s = 1.145 with chi2/dof 53. A direct grid on the same data gives s = 1.00 with chi2/dof 1.04 (s = 1.02 gives 1.64, s = 0.98 gives 1.17). The bracket search did not converge; I did not isolate why. The table at s = 1 is the right reading.

**Fixed-P=2.5 constant-K windows: discarded.** Those fits return K = 70.9 for three different cutoffs in both replicates, which is an optimizer failure, and the constant-K model is the wrong shape for this table anyway.

### Round 2 (rescored, see correction above)

Off-node A-A K: 3.5 and 4.5 miss by 2 to 3%. 5.5, 6.5, 7.5, 8.5 pass (within 2%). Crowd-8 ring (`r2/008-009`): table preferred over constant K (chi2/dof 1.00, difference 765 to 828 per run). P-0026 review (`r2/010-012`): replicated (see Reviews).

### 2026-11-25 round 2 scored (r2/005-012; scorer `out/labs/lab-a/analysis/score_round2_2026-11-25.py`, output `score_round2_2026-11-25.json`)

Same whole-run scale method as round 1 (imported unchanged from `score_round1_2026-11-25.py`), against the clamped P-0027 table. Sigma 0.05, 1-sigma from Delta chi2 = 1. Each set is a replicate pair (horizontal, diagonal).

| set | runs | r0 | T | s (run) | set mean s | Rule D |
|---|---|---|---|---|---|---|
| S25 | 005, 006 | 2.5 | 0.6 | 0.970 [0.960, 0.980], 0.960 [0.950, 0.970] | **0.965 +- 0.007** | passes (diff 0.010) |
| S28 | 007, 008 | 2.8 | 0.6 | 1.000 [0.985, 1.015], 0.995 [0.980, 1.005] | **0.998 +- 0.010** | passes (diff 0.005) |
| S20 | 009, 010 | 2.0 | 0.4 | 0.875 [0.860, 0.895], 0.895 [0.880, 0.910] | **0.885 +- 0.012** | passes (diff 0.020) |
| S30 | 011, 012 | 3.0 | 0.6 | 1.025 [1.005, 1.040], 0.980 [0.960, 0.995] | **1.003 +- 0.012** | passes (diff 0.045) |

Pre-registered rules, applied as written:
- **Rule A** (S28 near 1, S25 and S20 both below 0.95 with 1-sigma upper bounds below 1.00): **not triggered.** S20 meets it (0.885, upper bounds 0.895 and 0.910). S25 misses the 0.95 threshold by 0.015 (0.965), so the rule fails.
- **Rule B** (all of S25, S28, S20 within 0.05 of 1.00): **not triggered.** S20 is 0.115 below 1.
- **Rule C** (S28 and S30 both below 0.95): **not triggered.** Both are at 1.00.
- **Verdict: inconclusive. No claim** (as the pre-registration said for this outcome).

What the numbers show, without a rule:
- **The round-1 decline at r0 = 2.0 replicates.** s = 0.885 +- 0.012 in round 2, against round 1's 0.87 +- 0.05. The measured force is about 11.5% below the clamped table for a pair starting at 2.0 and run for 0.4 (the table is about 13% high relative to the measurement). Rule B (a systematic) is ruled out at this level. H43 is strengthened.
- **The deviation is smaller at 2.5 than round 1 suggested.** Round 1 gave s(2.5) = 0.90 +- 0.09 at T = 0.3. Round 2 gives 0.965 +- 0.007 at T = 0.6. Consistent within round 1's error, and the round-2 estimate is the tighter one. It sits about 5 sigma below 1 but above the 0.95 threshold.
- **At 2.8 and 3.0 the clamped table is correct to about 0.5%** (S28 0.998, S30 1.003). This does not contradict the withdrawn [3, 5) part of P-0027 in the way H35 was: H35 concerned K at 3.5 and 4.5 (18.2, about 2.5 to 3% above the table). Here the window is 2.8 to 3.4 at T = 0.6.
- **Caveat on every set above (new, from the scoring).** A T = 0.4 run from r0 = 2.0 is not local: the separation grows from 2.0 to about 2.5 over the run (relative acceleration about 6.3 at r0 = 2, so about 0.5 relative displacement by T = 0.4). S20 is therefore a window average over 2.0 to 2.5, not a value at 2.0. The S25 and S30 windows at T = 0.6 are wider (2.5 to about 3.0, 3.0 to about 3.6). These are **window** values. A local-K claim at any r0 needs a design that resolves windows, which is what round 3 does.
- **Precision and sensitivity (new).** Estimated by hand, a T = 0.2 run from r0 = 2.0 gives sigma(s) about 0.13 per run (not useful). T = 0.4 gives about 0.02 per run, T = 0.6 about 0.01. So T = 0.4 is the shortest duration that resolves s, and the window spans about 0.5 in separation. I drop the T = 0.2 idea.

### P-0030 review (filed 2026-11-25, round 3; `out/reviews/P-0030/lab-a.json`)

Runs `r2/001-004` (review account, cites P-0030). All four are in domain (A and C, N = 2, T = 2, separations 2.75, 3.25, 2.75 and 3.45 inside [2.5, 3.5]); `predict()` raises no ValueError. Judge-style RMSE/L against the paper's `model.py`: 0.00500 (001), 0.00496 (002), 0.00496 (003), 0.00495 (004). Bar 3 x 0.008 = 0.024. All four pass, so the verdict is **replicated** on the stated bound (rule: at least 3 of 4 pass). Script: `out/labs/lab-a/analysis/review_P0030_2026-11-25.py`.

Limits, as stated in the review: the judged metric sits at the noise floor (about 0.005 for a correct model), so these runs test the bound, not a few-percent K. The runs are out of sample for the nodes (2.75, 3.25, 3.45 are not nodes). The A-side at 3.45, the contested point, passes the bound, which does not settle P-0014's 4% statement on the A side. I make no claim about that.

## Round 3 requests and pre-registered rules (2026-11-25, written before the r3 results)

**Question.** Round 2 says the clamped table is 11 to 12% high at a pair starting at 2.0 and 3 to 3.5% high at 2.5 (window values), and correct at 2.8 and 3.0. The windows are not local (see the caveat above). Round 3 asks for a profile of window values with T = 0.4 and replicates, so that the decline can be placed. The runs are A-A, tracker, dt 0.002, research account. Generator: `out/labs/lab-a/analysis/make_2026-11-25_r3_requests.py` (validated; estimated cost 8.13 of 18.41).

| id | pair | r0 | T | window (approx.) | replicate of |
|---|---|---|---|---|---|
| r3/001 | A-A horiz | 2.25 | 0.4 | 2.25 to 2.75 | (first) |
| r3/002 | A-A diag | 2.25 | 0.4 | 2.25 to 2.75 | 001 |
| r3/003 | A-A horiz | 2.75 | 0.4 | 2.75 to 3.25 | (first) |
| r3/004 | A-A diag | 2.75 | 0.4 | 2.75 to 3.25 | 003 |
| r3/005 | A-A horiz | 2.5 | 0.4 | 2.5 to 3.0 | (first; same start as round-2 S25, T 0.4 instead of 0.6) |
| r3/006 | A-A diag | 2.5 | 0.4 | 2.5 to 3.0 | 005 |
| r3/007 | A-A horiz | 3.0 | 0.4 | 3.0 to 3.5 | (first) |
| r3/008 | A-A diag | 3.0 | 0.4 | 3.0 to 3.5 | 007 |

Sets: W225 = 001-002, W25 = 005-006, W275 = 003-004, W30 = 007-008. The S20 window (r2/009-010, T 0.4, from 2.0) is the lower end of the profile. Scoring uses the same whole-run scale s, Rule D as before.

**Predictions (stated before results).** If the decline is a ramp, s rises with r0: s(W225) about 0.90 to 0.95, s(W25) about 0.92 to 0.98, s(W275) about 0.96 to 1.02, s(W30) about 0.98 to 1.02. My best guess is a ramp that reaches 1.00 near 2.75. I am less sure of this than of the S20 result.

**Pre-registered rules (written before results):**
- **R1 (monotone ramp):** s(W20) <= s(W225) <= s(W25) <= s(W275) <= s(W30), each step within the replicate errors. A violated step means the profile is not a monotone ramp; no shape claim.
- **R2 (decline ends by 2.75):** s(W275) and s(W30) both within 0.02 of 1.00 (each with its 1-sigma interval reaching 1.00). Then the deviation is confined to windows starting below about 2.75.
- **R3 (decline reaches 2.75):** s(W275) below 0.95 with its 1-sigma upper bound below 1.00. Then the clamp is wrong at 2.75 as well, and the withdrawn [3, 5) region needs a second look (H35 is reopened). No claim this round either way.
- **R4 (T-dependence):** s(W25) at T = 0.4 differs from round-2 S25 at T = 0.6 (0.965) by more than 2 sigma. Then the window value depends on T, and only the shorter-T value is used.
- **R5 (replicate failure):** any set whose two runs differ by more than 2 sigma is not used, and I say so.
- **Claim rule for next round:** a profile claim is filed only if R1 and R2 both hold, with the window values, domain r0 2.0 to 3.0, T <= 0.4, and predicted_error at least 0.007 (not below 0.005). Not filed in this round, whatever the outcome.
- **Falsifier of my own round-2 reading:** if s(W225) is above 0.95, the round-2 S20 result (0.885) is not replicated at a neighbouring start and the decline is a feature of the start at exactly 2.0, not of the profile.

## Round 2 requests and pre-registered rules (2026-11-25, written before results)

Filed as `out/requests/2026-11-25/r2/lab-a/001-012`, all instruments `tracker`. Generator and validation: `out/labs/lab-a/analysis/make_2026-11-25_r2_requests.py` (validated against `protocol/request.schema.json`).

| id | account | purpose | N | T | dt | cost |
|---|---|---|---|---|---|---|
| r2/001 | review (P-0030) | A-C horiz, separation 2.75 | 2 | 2.0 | 0.002 | 1.08 |
| r2/002 | review (P-0030) | A-C diag, separation 3.25 | 2 | 2.0 | 0.002 | 1.08 |
| r2/003 | review (P-0030) | A-C vertical, separation 2.75 | 2 | 2.0 | 0.002 | 1.08 |
| r2/004 | review (P-0030) | A-C horiz, separation 3.45 | 2 | 2.0 | 0.002 | 1.08 |
| r2/005 | research | A-A horiz, separation 2.5 | 2 | 0.6 | 0.002 | 1.02 |
| r2/006 | research | A-A diag, separation 2.5 (replicate) | 2 | 0.6 | 0.002 | 1.02 |
| r2/007 | research | A-A horiz, separation 2.8 | 2 | 0.6 | 0.002 | 1.02 |
| r2/008 | research | A-A diag, separation 2.8 (replicate) | 2 | 0.6 | 0.002 | 1.02 |
| r2/009 | research | A-A horiz, separation 2.0 | 2 | 0.4 | 0.002 | 1.02 |
| r2/010 | research | A-A diag, separation 2.0 (replicate) | 2 | 0.4 | 0.002 | 1.02 |
| r2/011 | research | A-A diag, separation 3.0 | 2 | 0.6 | 0.002 | 1.02 |
| r2/012 | research | A-A horiz, separation 3.0 (replicate) | 2 | 0.6 | 0.002 | 1.02 |

Total research 8.18, review 4.32.

**Pre-registered rules for r2/005-012** (same whole-run scale-s method as round 1, against the clamped P-0027 table, 1 sigma from Delta chi2 = 1; each set is the pair of replicates):

Sets: S25 = 005, 006; S28 = 007, 008; S20 = 009, 010; S30 = 011, 012.

- **Rule A (decline begins above 2.5):** S28 within 0.05 of 1.00, and S25 and S20 both below 0.95 with each replicate's 1-sigma upper bound below 1.00.
- **Rule B (clamp holds at 2.0 to 2.8):** S25, S28 and S20 all within 0.05 of 1.00. This would contradict round 1's s(2.0) = 0.87, so if Rule B triggers I treat the round-1 result as a systematic and say so.
- **Rule C (decline across 2.0 to 3.0):** S28 and S30 both below 0.95 with 1-sigma upper bounds below 1.00.
- **Rule D (replicate failure):** any set whose two runs differ by more than 2 sigma. That set is not used, and I say so.
- Otherwise: inconclusive. No claim.

**Prediction from round 1 (stated before results):** s(S20) = 0.87 +- 0.05 and s(S25) about 0.90, so Rule A or Rule C is what I expect. S30 close to 1.00 (+- 0.13 from round 1), so Rule A over Rule C is my reading if S28 is near 1.

**Falsifier of my own round-1 reading:** S20 within 0.05 of 1.00 (Rule B) means the round-1 pair result is a systematic, not a K shape.

**Review of P-0030 (lab-vernier, A-C at 2.5 to 3.5, claim c1).** Pre-registered: the judge bar is 3 x 0.008 = 0.024. I expect RMSE/L about 0.005 on all four runs (in-sample floor), so verdict **replicated** if at least 3 of 4 runs are at or below 0.024. The four runs test the between-node region (2.75 and 3.25, out of sample) and the A-side at 3.45 that P-0014's bound and P-0030's own note call contested. Limits: the judged metric cannot see a few-percent K error (judge notes), so "replicated" will say only that the stated bound holds. I will file the review in round 3, once `out/results` for r2/001-004 exist. I will not file it before the results, because the verdict depends on them.

## Reviews

### Filed
- 2026-11-24: **P-0026 replicated** (lab-keystone, A crowd of 16 at T <= 0.3). Evidence `2026-11-24/r2/lab-a/010-012`. File: `out/reviews/P-0026/lab-a.json`.
- 2026-11-24: P-0025 replicated (`out/reviews/P-0025/lab-a.json`, evidence `2026-11-24/r1/lab-a/001-008`).
- 2026-11-23: P-0022 replicated; P-0023 replicated; P-0024 replicated, scoped (exponent not tested).
- 2026-11-22: P-0021, P-0017, P-0020, P-0016, P-0018 replicated.
- Standing: P-0013 replicated; P-0014 narrowed (T <= 1 for close approach); P-0015 replicated; P-0010 narrowed; P-0011 replicated; P-0002 replicated.

### Filed (round 3, 2026-11-25)
- **P-0030 replicated** (lab-vernier, A-C pair at rest, separation 2.5 to 3.5, stated bound 0.008). Evidence `2026-11-25/r2/lab-a/001-004`, RMSE/L 0.00495 to 0.00500 against bar 0.024. File: `out/reviews/P-0030/lab-a.json`. Scoped to the bound; the few-percent K is not tested.

### Pending
- None.

## Papers

### P-0029 (filed 2026-11-25, round 1, `out/papers/P-0029/`): A-A pair at rest, separation 5 to 9. Narrows and supersedes P-0027.
- Claim: K(r) piecewise linear through 17.834 (5), 16.617 (6), 15.121 (7), 13.432 (8), 11.624 (9). Judged error 0.007. Duration windows: T <= 2 for r0 < 7, T <= 3 for r0 >= 7.
- Evidence: 25 runs, all inside the window: `2026-11-23/r3/005-016`, `2026-11-24/r1/009-010, 013-018`, `2026-11-24/r2/003-007`. Judged RMSE/L 0.00492 to 0.00509 (check script `check_P0029_2026-11-25.py`).
- Withdrawn: the [3, 5) part of P-0027 (K 2 to 3% above table at 3.5 and 4.5).
- Not claimed: exponent, form, r < 5, r > 9, species B or C, three or more particles.
- The number P-0029 is the next free one at filing. The gate may renumber; refer to the paper by title until the final id is visible.

### P-0028 (filed 2026-11-24, round 3): A-A crowd at rest, up to 8 particles, T <= 1, the P-0027 table summed pairwise.
- Claim: N <= 8 A particles at rest, every initial pair in [3, 9], T <= 1.0: pairwise sum K(r)/r^2.5 with the P-0027 table, walls elastic. Judged error 0.007.
- Evidence: `r2/008-009` (ring, N = 8). Octagon `r3/005-006` passes the chi2 rule (see above) but is not yet cited.
- **Open issue (sharpened by round 1).** Its pairwise sum uses the P-0027 table at separations 3 to 5, which is withdrawn above (K about 2.7% high). The round-1 scale result also shows the clamp below 3 is about 13% high near r = 2. Both bear on the octagon's measured min pair (2.50 to 2.54). The judged error is unaffected (the bar is 0.021), but the claim relies on table values I now believe are off. A revision should restrict to separations at or above 5 (the ring has min pair 3.10 and would then fall outside the domain) or wait for a measured [3, 5) table and a measured close-range law.

## Requests filed 2026-11-25 (round 1; `out/labs/lab-a/analysis/make_2026-11-25_r1_requests.py`)

All account `research`, instruments `tracker`. Cost is `1 + 0.02 N T`. Total 13.44. **Executed; scored above.**

| id | purpose | N | T | dt | cost |
|---|---|---|---|---|---|
| r1/001 | A-A sep 2.0 horiz, local force at r = 2 | 2 | 0.3 | 0.005 | 1.01 |
| r1/002 | A-A sep 2.0 diag, replicate of 001 | 2 | 0.3 | 0.005 | 1.01 |
| r1/003 | A-A sep 2.5 horiz | 2 | 0.3 | 0.005 | 1.01 |
| r1/004 | A-A sep 2.5 diag, replicate of 003 | 2 | 0.3 | 0.005 | 1.01 |
| r1/005 | A-A sep 3.0 horiz, boundary against table at 3 | 2 | 0.3 | 0.005 | 1.01 |
| r1/006 | A-A sep 3.0 diag, replicate of 005 | 2 | 0.3 | 0.005 | 1.01 |
| r1/007 | A-A sep 1.5 horiz, T 0.15 | 2 | 0.15 | 0.0025 | 1.01 |
| r1/008 | A-A sep 1.5 diag, replicate of 007 | 2 | 0.15 | 0.0025 | 1.01 |
| r1/009 | B-B sep 2.5 horiz (factorisation) | 2 | 0.3 | 0.005 | 1.01 |
| r1/010 | C-C sep 2.5 horiz (factorisation) | 2 | 0.3 | 0.005 | 1.01 |
| r1/011 | A-B sep 2.5 horiz (factorisation) | 2 | 0.3 | 0.005 | 1.01 |
| r1/012 | A-A fall from r0 = 5 horiz, pre-contact trajectory | 2 | 4.0 | 0.02 | 1.16 |
| r1/013 | A-A fall from r0 = 5 diag, replicate of 012 | 2 | 4.0 | 0.02 | 1.16 |

### Pre-registered rules for `r1/001-013` (written before results; outcome above)
Local-force rules (1 to 3, below) were written with a local quadratic estimator that could not resolve T = 0.3 runs. They are applied above with the whole-run scale s. The outcome is recorded as rule 3 (inconclusive), with the scale numbers.

Predictions for the ratio F_meas / F_T (table clamped below 3; power law P = 3.2, K = 55.4):

| r | table (clamped) | power law, P = 3.2, K = 55.4 |
|---|---|---|
| 2.0 | 1.00 | 1.93 |
| 2.5 | 1.00 | 1.65 |
| 3.0 | 1.00 | 1.45 |

Rules:
1. **Table consistent at close range** if both replicates at each r agree with 1.00 to within 5%. Then the table is extended to [2, 3] with the clamped value, and I file a narrow claim at [2, 3] with the new runs. **Not triggered.**
2. **Steeper law at close range** if the ratio is above 1.25 at r = 2 and 2.5 and matches the power-law column within 10%. **Not triggered.**
3. **Inconclusive** if the ratio lies between 1.05 and 1.25, or replicates disagree by more than 5%. **Applies** (round-1 s(2.0) = 0.87, below the table).
4. **Species factorisation.** B-B, C-C and A-B at 2.5 are compared with A-A at 2.5 (ratio of F). Exploratory only, no claim this round. Done above.
5. **A-A falls (`r1/012-013`).** Fit pre-contact (measured separation above 2.5). Compare with the table (clamped below 3) and the power law over the same pre-contact samples. Chi2/dof reported per window. Not a claim until replicates agree. Done above; table preferred over the power law.

## Round 3 requests (2026-11-24, for reference)

| id | account | purpose | N | T | cost |
|---|---|---|---|---|---|
| r3/001 | grant | radial fall, r0 = 9 horizontal (proposal) | 2 | 10 | 1.40 |
| r3/002 | grant | replicate of 001 | 2 | 10 | 1.40 |
| r3/003 | research | A-A sep 3.5 diagonal, replicate of r2/001 | 2 | 1.0 | 1.04 |
| r3/004 | research | A-A sep 4.5 horizontal, replicate of r2/002 | 2 | 1.5 | 1.06 |
| r3/005 | research | crowd-8 octagon, R 4.2 rot 0.3 rad | 8 | 1.0 | 1.16 |
| r3/006 | research | replicate of 005 | 8 | 1.0 | 1.16 |

## Grant

- **Proposal (2026-11-25, round 1):** `out/grants/2026-11-25/proposals/lab-a.json`. Radial fall of an A-B pair from r0 = 9, same geometry as the A-A fall (`r3/001-002`), T = 10, 1990 samples. Test: K_AB(r)/K_AA(r) constant over separation 9 to contact (factorisation). A ratio that moves with r refutes factorisation. Pre-contact part only is fitted. Two particles, 1.40 credits. If it wins, the award is used in round 3 on this run and a replicate.
- **Vote (2026-11-25, round 2): lab-c (Nullius).** Its A-A close approach from r0 = 2.5 to contact tests the same open question as round 1 (the close-range law) on the trajectory, with two named rival laws that predict different paths. Two particles, cheap. I voted for it over Icarus (lab-b), whose A-B fall tests a ratio already in P-0025 (lab-b's own paper), and over Keystone and Vernier, whose N = 16 tests are for the pair sum (a different question). The vote is for discrimination, not for my own proposal.

## Hypotheses (status)
- H1 lone-particle free flight: supported (A, B, C).
- H2 species does not change free motion: supported for B, C at speed 1; C at speeds 0.2 to 8.6. B at high speed not tested.
- H3 cost = 1 + k N T, k = 0.02: supported at N = 1, 2, 3, 4, 8, 9, 16.
- H4 no decay: no census event in about 70 runs.
- H5 no pairwise interaction: refuted.
- H6 wall reflection elastic: supported.
- H7 pair attraction, central: supported. A-A: K(r) table on [5, 9] (P-0029). On [3, 5) the table is withdrawn (see H35). Below 3: see H43.
- H8 pair force identical for all species pairs: refuted at sep 5.
- H9 coupling factorises as g_ij = q_i q_j: partially supported. Round 1: A-B/A-A ratio 0.55 against sqrt(B-B/A-A) = 0.61, consistent within about 0.1 (exploratory). Grant test (A-B fall from 9) pending if it wins.
- H10 isotropy: supported at sep 4, 5, 8 (horiz vs diag within about 1.5%). A-B horizontal-diagonal -1.98% pooled, not significant. C-C horizontal-diagonal 5.4%: open.
- H11 shared distance law: C-based pairs at 7 and 9 within about 5% (P-0006). A-A at 7 and 9 refuted for constant K (H30).
- H12 pairwise additivity for 3 and 4 particles at separations 3 to 5 (T <= 1): supported. N = 9 at T = 10: not evaluable.
- H13 no census events in crowded long runs: supported (16 particles, T = 100).
- H14 constant-K power law at close range: refuted for A-A at r0 0.85 to 2.0.
- H15 A-A constant K at r0 = 1.0: refuted (K about 10.5 to 11.5, not 18). Consistent with H43.
- H16 B-B and C-C ratio to A-A at close range: B-B/A-A at r0 1.0 = 0.34; C-C/A-A = 0.84 (horizontal).
- H17 A-A K at r0 1.0 orientation-independent at (5,5): supported.
- H18 P-0014's T = 2 predictions fail for A-A at r0 2.5 (error 4.10) and C-C at r0 3.5. T <= 1 holds for pairs measured.
- H19 P-0013's S_AA = 0.753 supported. S_AC and S_CC not separated from 1.
- H20 close-range A-B: K_BA passes; K_AB fails clause (iii) on run 005. Open.
- H21 B-B at r0 1.0: K = 3.86 (lab-a), 3.98 (lab-b, P-0017). About 4 sigma apart; open pending lab-b refit.
- H22 C-C diagonal orientation 5.4% below horizontal at (5,5). Open.
- H23 A-B diagonal orientation: resolved as fluctuation.
- H24 P-0020 K_BA: my fit about 7.8 vs paper 7.33 (6%). Open.
- H25 P-0021 constant K over T = 6 (A-B at sep 7 falling to about 3.8): supported.
- H26 close-range A-B K_BA pooled 7.80: open as a claim only if K_AB is resolved.
- H27 A-C close range: K_AC -5.75, K_CA -13.6; diagonal control fails clause (iii). Held.
- H28 N = 9 same species, long time: not evaluable.
- H29 A-A K at sep 7 and 9 vs 17.7: confirmed (K 15.1 and 11.6).
- H30 A-A single P = 2.5 power law with K = 17.7 over sep 3 to 9: **refuted (2026-11-24).**
- H31 Exponent P of the A-A pair force: **open, not determined.** Round 1 narrows it: the falls fit the table with no free parameter before contact (chi2/dof 0.90 to 1.22 in every window), and the power law P = 3.2 without a free parameter is worse (1.77 to 2.70 from 2.0 to contact). The power law refit to the short runs at r = 2 (scale 0.44) matches the table at r = 2 by construction, so short runs cannot tell them apart. Close-range direct test: r2/005-012 and the grant (Nullius, if it wins).
- H32 A-A K(r) shape over sep 5 to 9: **supported (P-0029).** Per-run fits agree with the table within about 2%, and the pre-contact fall fits the table with no free parameter down to about separation 5.
- H33 crowd-8 pairwise law with table K at N = 8: supported on ring (`r2/008-009`) and octagon (`r3/005-006`): table preferred over constant K by about 1700 per run on the octagon. Table values at 3 to 5 are now suspect (see P-0028 open issue).
- H34 P-0025 (lab-b) A-B table at r0 4 to 8: replicated on the stated 0.007 bound (review 2026-11-24). K_B/K_A = 1.41 untested.
- H35 A-A K on [3.5, 4.5]: **refuted as P-0027 table (2026-11-25).** Replicates in both orientations (`r2/001-002`, `r3/003-004`) give K = 18.18 to 18.25, 2.5 to 3.2% above the table. K is about 18.2 across [3.5, 4.5] (flat within 0.4%). The P-0027 nodes at 3 and 4 (17.68, 17.70) are withdrawn.
- H36 P-0003's constant K = 17.7 is 6% high at separation 6 (measured 16.62): supported, per-run K fits.
- H37 judged metric cannot resolve K to better than several percent at T <= 2: supported.
- H38 A-A K at 6.5 is orientation-independent (horiz 15.81 vs diag 15.86, 0.37%): supported (`r2/004-005`).
- H39 A-A K at 5.5, 7.5, 8.5 agrees with the table within 0.5%, 0.0%, 1.8%: supported (`r2/003, 006, 007`).
- H40 Crowd-8 ring at T = 1: table pairwise sum preferred over constant K at chi2 difference 765 to 828 per run: supported.
- H41 Pre-contact radial fall from r0 = 9 (A-A) fits the P-0027 table with no free parameter, chi2/dof 1.00 to 1.10 through t = 8 (separation down to about 5): supported. Round 1 extends the falls from r0 = 5: table chi2/dof 0.90 to 1.22 in every window before contact (separations down to about 2.5).
- H42 Factorisation H9 via A-B fall vs A-A fall, same geometry: open, grant proposal filed.
- H43 (new, 2026-11-25) **A-A K falls below its r = 3 clamp value at r about 2.** Round 1: s = 0.87 +- 0.05 at r = 2, s = 0.90 +- 0.09 at 2.5. Round 2 (window values, T = 0.4 from 2.0): **s = 0.885 +- 0.012 at 2.0, replicated.** Round 2 at T = 0.6 from 2.5: s = 0.965 +- 0.007 (just above the 0.95 threshold). Round 2 at 2.8 and 3.0: about 1.00. Status: **strengthened (the decline at the 2.0 start is replicated); the profile shape is not yet resolved.** Round 3 (r3/001-008) places it. Not claimed.
- H44 (new, 2026-11-25) **The species coupling ratio: A-B against A-A at 2.5.** Round 1 (exploratory): A-B/A-A = 0.55, sqrt(B-B/A-A) = 0.61. Consistent. Not claimed. Grant test pending.
- H45 (new, 2026-11-25) **A-C K (P-0030) out of sample at 2.75, 3.25 and 3.45.** **Supported at the stated bound (review, round 3):** RMSE/L 0.00495 to 0.00500 on `r2/001-004`, bar 0.024. The few-percent K at these separations is not tested by the judged metric. Not claimed beyond P-0030's own claim.

## Plan for the next round

Done in round 3 (2026-11-25):
- Scored `r2/005-012` against Rules A to D: **inconclusive, no claim** (Rule A missed by S25 at 0.965 vs 0.95; Rules B and C not triggered).
- Filed the P-0030 review: **replicated** (`out/reviews/P-0030/lab-a.json`).
- Filed `r3/001-008` (A-A window profile at T = 0.4, research account, estimated 8.13 of 18.41). Pre-registered above.

Next (for the session that scores `r3/001-008`):
1. **Score r3/001-008** with the pre-registered rules R1 to R5 (window sets W225, W25, W275, W30, and the S20 window from r2/009-010). Write the scorer first: reuse `score_round1_2026-11-25.py` through the import pattern in `score_round2_2026-11-25.py`, with `RND = "r3"` and ids 1 to 8.
2. **If R1 and R2 hold:** file a narrow profile claim (A-A pair at rest, r0 2.0 to 3.0, T <= 0.4, window values, predicted_error at least 0.007). Evidence: `r2/009-010`, `r3/001-008`. Not filed before the scoring.
3. **If R3 holds (decline reaches 2.75):** no claim. Reopen H35 and look at the [3, 5) table again. The withdrawn region gets a dedicated test.
4. **If R4 holds (T-dependence):** use only the T = 0.4 values for any window claim and say so.
5. **P-0028 (crowd):** still open. Its pairwise table at 3 to 5 is in question, and the octagon's min pair (2.5) sits in the biased region. Prefer restricting its domain or waiting for the profile. Judge does not see the bias, so this is about honesty.
6. **Grant:** none today. Tonight's grant went to lab-vernier. My next grant proposal, if any, should target the close-range question only if the profile is still open.
7. Keep the sharpen bounties out of reach by design: no predicted_error below 0.005. A window profile claim would carry predicted_error 0.007 at the least, so none of the open bounties (`sharpen-A/B/C-*` need 0.0025) is in reach from it. `crowd-16` needs a 16-particle accepted claim, which is not what this profile is.
8. Research budget after round 3 (if all 8 run at about 1.02 each): about 10.3 credits left for this day, which does not roll over. Review allowance is unused (10.68), with no paper left to review.

## Errors caught

- **r0 from the first measured sample.** Fixed: r0 comes from the request setup.
- **Sample minimum read as collision.** Not used as a collision distance.
- **Grid bug in one B-B fit.** Refit on 3.0 to 4.5.
- **Edge runs fail the paper's own domain check.** Fixed by moving runs 0.01 inside.
- **Weak crowd test (T = 0.5 ring).** Insensitive to K. Replaced by T = 1.0 design (`r2/008-009`).
- **Uniform-K integrator divergence (N = 9, T = 10).** Recorded as not evaluable.
- **Exponent sensitivity overestimated (2026-11-23).** Recorded as null.
- **Circular secondary in the H30 scorer (2026-11-24).** Not reported.
- **Sharpen bounty trap.** Not pursued.
- **P-0003 bias at separation 6 went unnoticed until 2026-11-24.** Superseded by P-0027.
- **Random sequential 8-point layout infeasible at min pair 3.1 in the chamber.** Replaced by a regular octagon (`r3/005`).
- **Crowd-8 pair-separation preference misattributed in the first draft of P-0028.** Corrected.
- **Round-2 off-node predictions (2026-11-25 rescore).** Round-2 scorer used a sparse table (nodes 3, 5, 7, 9) for its deviations. Corrected to the full seven-node table; verdicts unchanged. Paper P-0029 uses the corrected numbers.
- **Round-3 rule 3 could not be applied as written (2026-11-25).** Constant-K windowed fits at P = 2.5 are invalid for a non-constant table, and the bracket search returned K = 70.9 for three cutoffs (optimizer failure). Replaced by whole-trajectory comparisons (free K/r^P and the table).
- **Scaled-table bracket search failed (2026-11-25).** Returned s = 1.145 with chi2/dof 53; direct grid gives s = 1.00 with chi2/dof 1.04. Used the grid. Did not isolate the cause in the search.
- **P-0027 narrowing was owed by the pre-registered rule and I had not filed it on 2026-11-24.** The replicates were in hand before I wrote P-0027's [3, 9] claim with the 3-to-4 nodes. Filed now as P-0029.
- **Round-2 and round-3 pre-registration used the sparse table value (17.72, 17.80) as the reference.** The pre-registered thresholds were relative to a wrong number. The verdict is the same with the full table, and I report both.
- **Round-1 local-force rules could not be run as written (2026-11-25, round 2).** The quadratic acceleration estimator at T = 0.3 has sigma 19 to 56 on K. A first draft also doubled the acceleration (a = 2*coef with a 0.5 t^2 column). Both caught before any number was reported. Rules applied to the whole-run scale s instead, stated above.
- **Round-1 fall windows reached contact (2026-11-25).** A first version compared post-contact samples (the sim has no contact model; RMSE/L 1e4 on the power law). Windows now end before the first measured separation below 2.5.
- **Window read as local (2026-11-25, round 3).** The round-2 pre-registration called S20 "the value at 2.0". A T = 0.4 run from r0 = 2.0 traverses about 2.0 to 2.5, so S20 is a window value. Caught while scoring the round-2 sets against their stated windows. The round-3 design and rules say "window" throughout.
- **Rule threshold without an error budget (2026-11-25, round 3).** The 0.95 threshold for Rule A was set without the replicate error. S25 came in at 0.965 (+- 0.007), so the rule fails by 0.015. Reported as inconclusive; the rule is not moved after the fact.
- **Round-2 review plan checked against the domain (2026-11-25).** Review runs 001 to 003 sit at least 0.25 inside [2.5, 3.5]. Run 004 (3.45) is 0.05 inside the 3.5 edge, well clear of the 1e-3 tolerance. Two particles, T = 2 inside the claim's window.

## Self-criticism

- **The judged metric hides K errors of several percent at these durations.** I have been reading "replicated" as "K confirmed". For K, the evidence is the per-run fit. The judge verdict only tests the error bound.
- **Replicate verdicts sit at the noise floor.** P-0022 through P-0026 are replicated only in the sense that the stated error bound holds.
- **P-0027 went out with a claim on [3, 9] that its own round-2 test had already questioned.** I should have fitted off-node nodes before filing it. P-0029 is the correction.
- **Per-run K at nodes 4 and 8 came from long falls.** They are trajectory averages, not local values. The table's node definitions are weaker than earlier notebooks claimed.
- **The fall analysis was written as a rule I could not run.** Rule 3 should have specified a whole-trajectory test before the data arrived.
- **Crowd-8 claim filed on one geometry.** The octagon now passes, but the claim's table is in question at 3 to 5. Not yet fixed.
- **The round-1 local-force rules were underpowered and I wrote them anyway.** I checked power at T = 0.3 only after the results came in. Next time: a noise-to-signal check (displacement over sigma) before the rule is written.
- **The clamp below 3 was carried in P-0027 and P-0028 without a test below 3.** Round 1 is the first measurement there; it contradicts the clamp by about 13% at r = 2.

- **Round-2 pre-registration named a value at 2.0 when its design gave a window.** The rule thresholds were fine; the words were not. Round 3 writes "window" everywhere and pre-registers the window profile instead of a single number.
- **The 0.95 threshold for Rule A had no error budget.** S25 landed 0.015 from it. A threshold should be set against the replicate error (about 0.01 here) before the data arrive.

## What would change my mind

- **Close range (`r2/005-012`):** Rule A (decline begins above 2.5) means the clamp is wrong from about 2.5 down, and a close-range claim follows. Rule B (clamp holds at 2.0 to 2.8) means round 1's 13% is a systematic I have not found. Rule C (decline across 2.0 to 3.0) means the table is high at 3 as well, which would also reopen H35.
- **A-B fall (grant, round 3):** if K_AB/K_AA is constant to 3% over separation 2 to 9, factorisation H9 is supported. If it moves more than 5%, factorisation is refuted and the species-pair claims are separate.
- **Exponent (H31):** the falls from r0 = 5 and the close-range runs decide P together. Until then P is not claimed. Round 1 already leans toward the table shape over the power law at 2.5 to 3.5.
- **P-0030 review:** if two or more of the four runs are above 0.024, the stated bound fails and I say so. **Resolved (round 3): all four pass (0.00495 to 0.00500).**
- **Close range, round 2 (`r2/005-012`, scored round 3):** inconclusive under the rules. The decline at 2.0 replicates (s = 0.885). S25 at 0.965 sits between the rules. S28 and S30 are at 1.00. What would change my mind now: **R3** (s(W275) below 0.95, decline reaching 2.75) reopens the clamp at 3, or **R1 failing** (a non-monotone profile), which would mean the windows are not a ramp at all.
