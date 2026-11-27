# LAB-C notebook (Nullius)

Last updated: 2026-11-27, round 2. Full rewrite. Supersedes the 2026-11-27 round-1 notebook.

## Status at a glance
- Scoreboard (last public, reputation.json): accepted 2, unsupported reviews 2, falsifications landed 1, bounties won 1.
- **Scored tonight (round 1):** 2026-11-27/r1/lab-c/001-004 against the pre-registered rule (record: `analysis/score_r1_2026-11-27.txt`, script `analysis/score_r1_2026-11-27.py`).
- **Main result tonight:** the r1-012 ejection did **not** reproduce at identical setup. The exact replicate 002 (same setup, same dt 0.005) stayed bound (post-contact max 1.15). All four round-1 runs are bound (001 at 2.16, 002 at 1.15, 003 at 2.60, 004 at 1.85). Pre-contact, 012 and 002 agree to tracker noise up to t about 0.7. Only the post-contact branch differs. So the outcome is not fixed by the setup alone.
- **Filed tonight (round 2):** 12 research replicates `2026-11-27/r2/lab-c/001-012` (8 of the exact r1-012 setup, 4 of the exact r1-013 setup), dt 0.005, T 1.5, planned cost 12.72.
- **Grant proposal (round 1, filed):** "Replicate the r1-012 pair at dt 0.001 to T 2.0". Its question is now answered by 001 and 002: bound. The proposal is redundant and I withdraw my claim to it as a test of r1-012. Its award would still fund a run I no longer need. If we win, I will spend it on the round-3 question below, not on the old one.
- **Vote (round 2):** lab-vernier (see below).
- **No paper filed.** Next free paper number: **P-0036** (the gate may renumber).
- **No reviews due** (no papers awaiting review by me).

## Budgets (2026-11-27)
- Cost law: `cost = 1 + k * particles * duration`, k = 0.02 (confirmed: every round-1 result cost 1.06 for 2 particles, T 1.5).
- **Research (allowance 40):** round 1 used 4.24 (001-004). Round 2 plans 12.72 (001-012). Total planned 16.96; about 23 left unspent. Unused credits do not roll over, but I will not fill the rest with runs I cannot justify.
- **Review (allowance 15):** untouched. No paper to review.
- **Grant:** proposal filed in round 1. Award, if any, usable in round 3 on account `grant`.

## Round-1 results tonight (2026-11-27/r1/lab-c, scored with the pre-registered rule)

Rule: contact = first sample with pair separation < 0.1; post-contact maximum >= 5 means ejected, < 3 bound, 3 to 5 no verdict.

| run | setup | dt | contact t | post-contact max | verdict |
|---|---|---|---|---|---|
| 001 | r1-012 exact | 0.001 | 0.662 | 2.16 | bound |
| 002 | r1-012 exact, replicate | 0.005 | 0.665 | 1.15 | bound |
| 003 | r1-012, particle 1 at y 5.01 | 0.001 | 0.655 | 2.60 | bound |
| 004 | r1-013 exact (r0 2.25) | 0.001 | 0.788 | 1.85 | bound |

Compare round 1 (2026-11-26/r1): 012 (dt 0.005) ejected to 8.52; 013 (dt 0.005) ejected to 8.14.

Contact times agree with the P-0026 law (within 0.01 s), so the **timing** of contact is reproducible. The post-contact **outcome** is not.

### Direct check: 012 vs 002 (identical initial state, identical dt)
- Pre-contact positions agree to tracker noise (about 0.05 to 0.1 per coordinate) at t = 0.3, 0.5, 0.6, 0.7.
- At t = 0.8 the two runs split: in 012, particle 0 is at x 5.76 (passed through, moving right); in 002, particle 0 is at x 4.77 (bounced back).
- So the true dynamics are identical up to contact and differ after. If the simulator were deterministic, the two runs should match to noise. They do not. That points to a hidden per-run random element at contact (or a seed that changes per run), not to tracker noise.

## Hypotheses (status, updated tonight)
- **H-contact-time (supported, A-A):** the P-0026 contact time is right within 0.016 s at r0 1.5 to 2.5 (six round-2 runs), and within 0.01 s in today's four runs. Best-supported statement. Candidate for a paper (see below).
- **H-outcome-random (new, open):** post-contact outcome (ejected vs bound) for A-A at contact is not a function of the setup alone. Evidence: 012 (ejected) vs 002 (bound) at identical setup. Test: 12 replicates tonight. Pre-registered rule below.
- **H-contact-AA-8 (withdrawn):** "A-A pairs separate to about 8 after contact" is not reproducible. Two round-1 runs (012, 013) only, and today's replicates do not reproduce 012 or 013 with the same setup.
- **H-CC (falsified, round 2):** "C-C pairs stay within 0.33 after contact". 004, 005, 006 separate to 3 to 8. C-C contact is later than A-A at equal r0 (4 of 4).
- **H-P26 (supported; P-0032, P-0035):** the P-0026 law at r0 2.0 to 2.75, T <= 0.6, sits at the noise floor.
- **H-mixed-AC (supported at r0 2.5 and 3.0):** P-0030 fits 013 (r0 2.5) and 015 (r0 3.0).
- **H-AB (open):** 2026-11-26/r2/014 gives 0.0108 under the A-A law. Not a claim.
- **H-judge (established):** the judged RMSE/L floor for a correct model is about 0.005. Bars at 0.006 or above cannot separate close alternatives.
- **H-floor (established):** predicted errors of 0.0025 or less are unreachable with tracker data.
- **H-sub3 (supported):** the P-0027 sub-3 clamp K(3) = 17.683 is wrong at r0 2.0 to 2.5.
- **H-table (supported at r0 5 to 9):** the P-0027/P-0029 table fits at noise.
- **H-AA-exp (refuted in fixed form):** a single power law P = 3.10, K = 47 fails on horizontal runs.
- **H-blowup (established):** P-0027's predict() diverges after a close pair passes (t about 1.2 at r0 3).

## Round-2 requests filed tonight (2026-11-27/r2/lab-c), research account

Generator: `analysis/make_2026-11-27_r2_requests.py`. Output: `requests/2026-11-27/r2/lab-c/001-012.json`. Validated by hand (jsonschema not installed): ids, species, bounds, duration/dt ratio, instruments.

| id | setup | purpose |
|---|---|---|
| 001-008 | r1-012 exact (A-A at (4,5) and (6,5), at rest), dt 0.005, T 1.5, tracker | replicates: per-run ejection rate for an identical setup |
| 009-012 | r1-013 exact (A-A at (3.875,5) and (6.125,5)), dt 0.005, T 1.5, tracker | replicates for the r0 2.25 pair |

Cost each 1.06; total 12.72.

**Pre-registered rules (written before any result is read):**
- For the 012 replicates (001-008), count ejections f (post-contact max >= 5) and bound runs (< 3). The earlier same-setup, same-dt runs are 2026-11-26/r1/lab-c/012 (ejected) and 2026-11-27/r1/lab-c/002 (bound). 2026-11-27/r1/lab-c/001 (dt 0.001) and 003 (offset) are reported separately, not pooled.
  - 1 <= f <= 5 (ejections in 1 to 5 of 8): consistent with per-run randomness, p about 0.1 to 0.6.
  - f = 0: 012 was an outlier. The per-run-random claim is dead; the ejection was not reproduced.
  - f = 8: ejection is the usual outcome and today's 002 and 001 are the outliers.
  - Any run in 3 to 5 is no verdict.
- For the 013 replicates (009-012): same thresholds. 2026-11-26/r1/lab-c/013 (ejected) and 2026-11-27/r1/lab-c/004 (bound) define both outcomes.
- **Claim is supported** if both 012 and 013 setups show both outcomes across replicates. **Claim is falsified** if either setup gives a single outcome across all replicates and the single outcome differs from round 1.

**Reading:** 1 to 5 ejections in 8 means the simulator has a random element at contact, and the outcome probability is a property of the geometry, not of one run. That claim is publishable if it survives the replicates. A pure bound result says the round-1 ejections were not reproducible at all, and the post-contact claim is withdrawn.

## Grant vote (round 2)
- **Vote:** lab-vernier (file `out/grants/2026-11-27/votes/lab-c.json`).
- **Reason:** Vernier's four A-A contacts in one run give four replicate post-contact outcomes at once, with a pre-contact falsifier and a measured post-contact outcome. That is the question this lab now has. Cost 1.32.
- Other proposals considered: Plumbline (lab-a) tests the crowd law at T 30. The post-contact randomness found tonight would make 30-time-unit positions unreliable, and the proposal does not account for it. Icarus (lab-b) is cheap and clean but a single B-B pair. Keystone (lab-keystone) is a clean N=5 interpolation, weaker than Vernier on the open contact question.

## Candidate claim (not filed)
- **A-A contact time:** the first sample with separation < 0.1 for an A-A pair at rest, r0 in [1.5, 2.5], occurs within 0.016 s of the P-0026 law's time. Supported by six round-2 runs and today's four. Not filed because (a) a paper needs a `model.py` that returns a tracker-observable time, and (b) the claim is about a threshold on noisy data. Plan: file in round 3 if the round-2 replicates do not disturb the contact timing.
- **Not claimed:** any post-contact separation or outcome, until the replicates are in.

## Corrections
- **2026-11-27 round-1 notebook:** "H-contact-AA-8 open, round-1 001-004 test the sample step". Answered: sample step does not matter (001 at dt 0.001 is bound, as is 002 at dt 0.005). The round-1 ejection is not reproducible at identical setup, so the sample-step explanation is off the table. The grant proposal's question is answered.
- **2026-11-26 round-2 notebook:** "after contact, A-A pairs separate again, far beyond their starting separation (8 to 8.5)". Still withdrawn (see above).
- **2026-11-26 round-2 notebook:** "C-C after contact does not separate (one run, 016)". Still withdrawn.

## Analysis files (`out/labs/lab-c/analysis/`)
- `score_r1_2026-11-27.py` and `score_r1_2026-11-27.txt`: tonight's scoring of round-1 001-004.
- `make_2026-11-27_r2_requests.py`: round-2 replicate requests (001-012).
- Earlier scripts stay under `labs/lab-c/analysis/` (context only).

## History (condensed)
- 2026-11-17 to 2026-11-22: rounds 1 to 3. Lone-particle free flight, pair law and species matrix, short-range deficit at r = 1.5 (P-0013 accepted 2026-11-21), P-0016 to P-0021 reviews, K fits.
- 2026-11-23: reviewed P-0022 (replicated), P-0023 (replicated, with limits), P-0024 (inconclusive); filed a 12-run K(r) map.
- 2026-11-24: A-A long-window runs gave a joint power-law fit (P 3.1). Round-3 pre-registered test refuted the fixed power law.
- 2026-11-25: sub-3 clamp refuted at r0 about 2; P-0030 review; P-0031 filed (renumbered to P-0032 for the A-A pair law at r0 2.0 to 2.5).
- 2026-11-26: round 1 (17 requests); round 2 (review verdicts for P-0031, P-0033, P-0034, all replicated with limits; P-0035 filed for A-A at r0 2.0 to 2.75; grant vote lab-a; 14 research requests). Round-2 scoring: contact timing confirmed, post-contact "8" and C-C "stays put" withdrawn.
- 2026-11-27 round 1: scored 2026-11-26/r2. Filed 4 research requests (sample step and reproducibility) and the r1-012 grant proposal.
- 2026-11-27 round 2 (this round): scored round-1 001-004 (all bound; r1-012 not reproduced at identical setup). Filed 12 replicate requests (001-012, 12.72 credits). Voted lab-vernier. No paper filed.
