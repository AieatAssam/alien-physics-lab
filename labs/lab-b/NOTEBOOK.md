# LAB-B notebook

Persona: bold theorist. Rule I hold myself to: a striking law only after a discriminating run supports it, and stated with its domain.

Last updated: 2026-11-18, round 2 (requests written, results pending).

## Season facts (measured)

- Season 1, species in use: A, B, C (`protocol/season.json`). Chamber [0, 10]^2.
- **Cost constant k = 0.020.** Cost is `1 + k·N·T` and does **not** depend on `sample_dt`. Confirmed on every result so far.
- **Consequence 1:** sample_dt is free. The only limit is 2000 samples, so `sample_dt = duration/2000` gives the most data per credit. Check the ratio in Python before submitting; a float ratio of 2000.0000002 may be rejected.
- **Consequence 2:** the cost has a floor of 1.0 per run, and the term that scales with time is tiny for short runs. A run with T=0.3 costs 1.01. So many short, densely sampled runs are cheap. The binding limit is the number of runs, not the duration.
- Tracker noise: **sd about 0.05 per coordinate** (r1/001 0.053/0.052; r2/005 0.052/0.050; today's runs agree with this in the cross-run comparisons).
- Census: no decay or appear events in any run so far.
- Masses, relative to m_A = 1, from centre-of-mass conservation before wall contact (`analysis/r2_checks.py`). Rough:
  - A-A: 0.98, so equal masses.
  - A-B: 0.55, 0.74, 0.70. I take m_B ≈ 0.7 m_A, spread ±0.1.
  - A-C: 0.40. So m_C ≈ 0.4 m_A.

## Trajectory reproducibility (new, round 2 of 2026-11-18)

Four runs from the same state (A at (4.5, 5), B at (5.5, 5), at rest), all T=1, agree with each other at noise level in every time window, including through the first close pass at t≈0.25–0.3:

| Pair of runs | dt (A, B) | rms diff t≤0.25 | 0.25–0.6 | 0.6–1.0 |
|---|---|---|---|---|
| r1/001 vs r1/002 | 0.01, 0.05 | 0.085 | 0.054 | 0.072 |
| r1/001 vs r1/003 | 0.01, 0.02 | 0.061 | 0.067 | 0.064 |
| r1/002 vs r1/003 | 0.05, 0.02 | 0.060 | 0.077 | 0.065 |
| r3/006 vs r1/001 | 0.01, 0.01 | 0.062 | 0.068 | 0.113 |

Noise-only expectation for two noisy copies is 0.071. The r3/006 pairs are slightly high in the last window (0.11), which I do not yet explain. Everything else is at noise level.

**The outlier is r2/003, which is T=10, dt 0.05.** It agrees with the T=1 family for t≤0.25, then departs:

| Pair | rms diff t≤0.25 | 0.25–0.6 | 0.6–1.0 |
|---|---|---|---|
| r2/003 vs r1/001 | 0.066 | 0.162 | 0.292 |
| r2/003 vs r1/002 | 0.074 | 0.175 | 0.299 |
| r2/003 vs r1/003 | 0.072 | 0.180 | 0.325 |

What this says, and what it does not:
- **sample_dt-independence holds at T=1** (dt 0.01, 0.02, 0.05 agree). H9 is supported for dt.
- **Random per-run variation looks unlikely.** Four T=1 runs agree with each other through a close pass, so the dynamics are reproducible at T=1.
- **The new leading explanation is dependence on the requested duration** (or on something in the request beyond the initial state). The T=10 run splits from the T=1 family at the first close pass. Round-2 requests 001–003 (T=10, 5, 2 at the same state) test this directly.
- This matters beyond my own work. P-0003 (lab-a) uses durations 1–2, and its close-approach runs (003–004, reaching r≈0.14 at t=2) may depend on duration. Flagged for the review (see below).

Analysis: `out/labs/lab-b/analysis/determinism_windows_r1.py`.

## Pair sign pattern (main result so far)

All six unordered species pairs have been measured at rest with a requested separation of 1–2 (and A-B also at 4):

| Pair | Run(s) | Sign at short range | Evidence |
|---|---|---|---|
| A-A | r2/001 | attract | first r<0.5 at t=0.65 |
| A-B | r1/002, r2/002–004, r3/006 | attract | first r<0.5 at t=0.25–0.30 (sep 1); t=0.84 (sep 2, offset); t=2.55 (sep 4) |
| B-B | r3/001 | attract | first r<0.5 at t=1.08 (sep 2) |
| C-C | r3/002 | **attract** | first r<0.5 at t=0.72 (sep 2) |
| A-C | r2/006, r3/004, r3/005 | **repel** | separation grows monotonically; sep 1, 2, 4 |
| B-C | r3/003 | **repel** | separation grows monotonically to 7.95 at t=3 (sep 2) |

**Round 3 falsified my "C repels everything" rule (H7 as stated).** r3/002 (C-C) attracts.

The six signs fit a charge-product rule: F_ij ∝ q_i q_j, with q_A = q_B = +1 and q_C = −1. Like-charged pairs (AA, AB, BB) attract; unlike pairs with C (AC, BC) repel; CC attracts since q_C² > 0. **This fits every observed sign. It is not yet tested for magnitudes or for additivity.** Only the cross-species signs are informative.

Rough initial relative accelerations at the requested separation (`analysis/r3_summary.py`, noisy):

| Pair, sep | a (t≤0.3) | a (t≤0.6) | Sign |
|---|---|---|---|
| A-A, 2 (r2/001) | −5.5 | −7.1 | attract |
| B-B, 2 (r3/001) | −1.6 | −2.0 | attract |
| C-C, 2 (r3/002) | −4.6 | −5.1 | attract |
| B-C, 2 (r3/003) | +1.5 | +2.6 | repel |
| A-C, 4 (r3/005) | +1.1 | +0.8 | repel |
| A-C, 2 (r2/006) | +4.6 | +4.0 | repel |
| A-C, 1 (r3/004) | +16.8 | +12.7 | repel |
| A-B, 1 (r2/003) | −16.7 | −4.6 | attract |
| A-B, 1 (r3/006) | −16.7 | −6.6 | attract |

- **H6, A-C repulsion falls off steeply with separation (supported, rough).** +16.8, +4.6, +1.1 at sep 1, 2, 4: roughly r^-2, ±50%.
- **Cross-check with P-0003 (lab-a, see Papers).** Lab-a's per-particle law K/r^2.5 with K=17.7 predicts a relative A-A acceleration of 6.3 at sep 2. My r2/001 gives −5.5 (t≤0.3). Consistent at about 15%, but this is an extrapolation below P-0003's stated domain (3–6), and my estimate is noisy.
- BB attraction looks weaker than AA and CC at the same separation (−1.6 vs −5.5 and −4.6). Not claimed yet. Round 2 tests it with clean fits.

## Hypotheses (status after round 2 planning)

- **H1, free flight of a lone particle (A):** supported by r1/001. Published as **P-0001**.
- **H5, free flight of a lone particle (C), high speed, long run:** supported by r2/005. Published as **P-0002**.
- **H2, pair interaction is species-pair specific, with signs:** supported. Sign pattern fits a charge-product rule. Magnitudes not tested.
- **H7 (sign follows C alone):** **falsified** by r3/002.
- **H3, central pair force:** supported for A-B (r2/004). Not yet tested for other pairs.
- **H4, distance dependence of attraction (A-B):** qualitatively supported.
- **H6, A-C repulsion decays with separation:** supported (rough).
- **H8, short-range (r<1) pair dynamics follow a central power law:** not supported as measured; the close-approach fits are poor. See below.
- **H9, simulator is reproducible and sample_dt-independent:** **supported at T=1** for dt 0.01–0.05 (today's r1/001–003 plus r3/006). **Open for T:** the T=10 run r2/003 departs from the T=1 family after the first close pass. Round 2 tests whether duration sets the trajectory.
- **H10 (new), the charge-product rule is rank one in magnitude:** |F_ij|² = |F_ii||F_jj| for all pairs, with masses from Newton's third law. Untested. Round 2 tests it at sep 1.5 and sep 3.

## Close-approach problem (narrowed)

- Joint fit of the A-B and A-A runs with one power law F = k·r^(-n) gives rms 0.28–0.34 (noise 0.05). Not usable.
- The close-pass runs do not fit a single power law. Softening does not help.
- **Narrowed by today's data.** The disagreement is not random per-run noise (T=1 runs agree), and it is not sample_dt (dt-independent at T=1). Duration is the remaining candidate. If it is duration, every close-approach fit that mixes durations is suspect, including the T=10 run I used for the A-B power-law fit.
- Working rule: do not publish any pair law that depends on close-pass data until round 2 settles the duration question.

## Papers

- **P-0001** (lab-b, accepted). "Free flight of a lone species-A particle with specular wall reflection." Evidence r1/001. Domain: species A, one particle, r_range [0, 14.15]. Lab-a's review (`reviews/P-0001/lab-a.json`) verdict **replicated** for the x=10 and y=0 walls at speed 1.0. Not tested by lab-a: x=0 and y=10 walls, corners, durations above 12, speeds other than 1.0, other species. My domain says "species A, all walls" but the replication covers two walls. I will narrow it at the next revision if the other walls don't check out.
- **P-0002** (lab-b, submitted). "Free flight of a lone species-C particle over 40 time units with specular wall reflection." Evidence 2026-11-17/r2/lab-b/005. Domain: species C, one particle. Cites P-0001. Lab-a's review (`reviews/P-0002/lab-a.json`) verdict **replicated** on a narrow scope (speed 1.0, duration 12). Edge tests in lab-a's review requests 2026-11-18/r1/lab-a/014–016 pending.
- Pair claims: none yet. I will not publish a pair law until the duration question and the magnitude test are in.

## Review of P-0003 (lab-a, "A-A attraction, K/r^2.5, separation 3–6")

P-0003 is awaiting my review. Its claim: two A particles at rest, separation 3–6 along x, durations 1–2, no walls, per-particle accel 17.7/r^2.5, with the claim covering only that domain. Its evidence is eight runs, all horizontal at y=5, and its fit is to those same runs (a consistency check, not a prediction test). Lab-a states the power law and a screened form fit equally well, and it makes no statement below r≈0.14.

Points I can test inside its stated domain:
- **Orientation.** The claim says "along a line", but every run is horizontal. A diagonal pair tests isotropy.
- **Position.** The claim says "no other effects" and "no wall contact". A pair 1 unit from the bottom wall, at T=2, tests that.
- **Domain edges.** Separation 3 and 6, duration 2.
- **Duration dependence.** If trajectories depend on requested duration (see above), P-0003's T=2 runs reaching r≈0.14 may be off. I will flag this in the review once round-2 results arrive.

Review requests (account `review`, cites P-0003), written this round: 2026-11-18/r2/lab-b/018–021 (see round-2 table). Review credits used: 4.32 of 15 (pending).

Not yet done: the review file (`out/reviews/P-0003/lab-b.json`). I will write it after the results arrive, with a verdict only as strong as the data. I must not review P-0003 on the basis of the predictions alone.

## Results so far

### Round 1 of 2026-11-18 (r1), all status ok, all 0 census events

Cost 1.04 each, as predicted (`1 + 0.02·2·1`). Budget after round 1: 36.88.

- **001, A-B at (4.5,5)/(5.5,5), at rest, dt 0.01, T 1.** Replicate of r3/006. Agrees with r3/006 at about noise level, with a slight excess in the last window (0.11 vs 0.07). Basis for the determinism conclusion above.
- **002, same state, dt 0.05, T 1.** Agrees with 001 at noise level (0.075). **Disagrees with r2/003 (T=10, same dt and state) after t≈0.25.**
- **003, same state, dt 0.02, T 1.** Agrees with 001 and 002 at noise level.

### Round 3 of 2026-11-17 (r3), requested 2026-11-17, all status ok

- **001, B-B at rest, 2.0 apart, dt 0.02, T 3.** Attracts. First r<0.5 at t=1.08. Partly confirmed.
- **002, C-C at rest, 2.0 apart, dt 0.02, T 3.** **Attracts.** Falsified my H7.
- **003, B-C at rest, 2.0 apart, dt 0.02, T 3.** Repels. Confirmed.
- **004, A-C at rest, 1.0 apart, dt 0.02, T 3.** Repels at short range. Confirmed.
- **005, A-C at rest, 4.0 apart, dt 0.02, T 3.** Repels, slowly. Confirmed.
- **006, A-B at rest, 1.0 apart, dt 0.01, T 1.** Replicate of r2/003 initial state. Agrees with r2/003 before the first close pass but differs after. Today's analysis says this is consistent with the duration explanation (r2/003 is T=10).

### Earlier rounds

- Round 1 of 2026-11-17: r1/001 (lone A free flight, basis for P-0001), r1/002 (A-B pair, attract).
- Round 2 of 2026-11-17: r2/001 (A-A at rest 2.0 apart, T=10, dt 0.05, attracts), r2/002 (A-B at rest 4.0 apart, far-field approach), r2/003 (A-B at rest 1.0 apart, T=10, dt 0.05, close passes), r2/004 (A-B offset, central force supported), r2/005 (lone C, basis for P-0002), r2/006 (A-C at rest 2.0 apart, repel).

## Round 2 plan (2026-11-18 r2), submitted

Files: `out/requests/2026-11-18/r2/lab-b/001–021.json`. Research 18.24 credits (remaining 18.64 after the round). Review 4.32 credits (of 15).

| Request | Account | Setup | Cost | Question | Prediction if the hypothesis holds | Falsified if |
|---|---|---|---|---|---|---|
| 001 | research | A-B at (4.5,5)/(5.5,5), rest, T 10, dt 0.005 | 1.40 | Is T=10 reproducible, and is it the same as r2/003? | Matches r2/003 on t≤1 (rms ~0.07). Departs from the T=1 family after 0.25 | Matches the T=1 family: then r2/003 was a one-off and duration does not matter |
| 002 | research | same, T 5, dt 0.0025 | 1.20 | Where does the departure start as T changes? | Matches the T=10 branch if the trajectory depends on T | Matches T=1 family (duration not the cause) or an intermediate branch (continuous dependence) |
| 003 | research | same, T 2, dt 0.001 | 1.08 | Duration on the domain edge | Matches T=1 family on t≤1 if dependence is only at long T | Departs from T=1 family by t≈0.6 (short-T effect) |
| 004–009 | research | six pairs at sep 1.5 (AA, BB, CC, AB, AC, BC), rest, T 1, dt 0.0005 | 6.24 | Magnitude and sign at sep 1.5; fit t≤0.3 | AA per-particle accel ≈6.4 (P-0003 extrapolated). Rank-one: F_AB² = F_AA F_BB, etc. | Rank-one relation off by more than fit error (~10%) |
| 010–015 | research | six pairs at sep 3, rest, T 1, dt 0.0005 | 6.24 | Same at sep 3; fit t≤1.0 | AA per-particle ≈1.14 (P-0003, its domain). Rank-one as above | Rank-one off by more than fit error; AA differs from 1.14 by more than 10% |
| 016 | research | AA at sep 1.0, T 1 | 1.04 | Short-range AA; fit t≤0.2 | Per-particle ≈17.7 (P-0003 extrapolated) | Differs by more than 25% |
| 017 | research | AA at sep 2.0, T 1 | 1.04 | Short-range AA; fit t≤0.3 | Per-particle ≈3.13 | Differs by more than 25% |
| 018 | review | AA at (3,1)/(7,1), sep 4 along x at y=1, rest, T 2, dt 0.001 | 1.08 | P-0003 edge: near wall, off-centre, T=2 | Motion along x only; y stays 1.0; x matches the predictor | y drift > 0.15, or x departs from predictor by > 0.15 on average |
| 019 | review | AA at (3,3)/(5.83,5.83), sep 4 diagonal, T 2 | 1.08 | P-0003 orientation test (all its runs are horizontal) | Central, same law: diagonal relative curve matches the predictor | Departs from predictor by > 0.15 on average |
| 020 | review | AA at (8,3.5)/(8,6.5), sep 3 vertical, near right wall, T 2 | 1.08 | P-0003 short-end orientation and wall-proximity test | Motion along y only; x stays 8.0; matches predictor | x drift > 0.15, or separation departs > 0.15 |
| 021 | review | AA at (2,2)/(8,2), sep 6 along x at y=2, T 2 | 1.08 | P-0003 long-end edge | Attraction ~0.20 per particle; matches predictor | Departs from predictor by > 0.15 on average |

Predictions are written in the requests as well. For the magnitude runs I fit each particle's acceleration with a cubic (known initial state) and derive mass ratios from Newton's third law, m_i a_i = −m_j a_j. Then I check the rank-one relation.

## Ledger

- Research 2026-11-17: allowance 40. Used 17.70 (round 1: 2.60; round 2: 8.46; round 3: 6.64). The 22.30 left over does not roll over.
- Research 2026-11-18: allowance 40. Round 1 spend 3.12. Round 2 planned 18.24. Remaining after round 2: 18.64.
- Review 2026-11-18: allowance 15. Round 2 planned 4.32 (requests 018–021, cites P-0003). Remaining after: 10.68.

## Analysis files (`out/labs/lab-b/analysis/`)

- `determinism_windows_r1.py`: windowed rms comparison of runs sharing an initial state. Used for today's reproducibility table. Run with `python3 -I`.
- `make_round2_requests.py`: writes round-2 requests and checks sample counts (cap 2000) and review fields.
- `early_accel_fit.py <request.json> <result.json> <tmax> ...`: cubic early-window fit per particle (x0, v0 = 0 from the request), residual rms, and the mass ratio from Newton's third law. Checked on synthetic data with known acceleration and 0.05 noise: unbiased. **Precision:** with the jerk term free, sd about 10% per particle for a 0.3-wide window at a=6.4 (sep 1.5 AA), and about 2.6% for a 1.0-wide window at a≈1.1 (sep 3). The rank-one test needs to be read against those errors.
- Existing short-dt runs (r2/001, r3/001–003, r2/006) have only 6–30 samples in a 0.3–0.6 window. Their per-particle fits are not precise enough to test mass or the rank-one relation. Round 2 is designed to fix this with 2000 samples per run.

Existing tools in `labs/lab-b/analysis/` (repo, read-only for me): `r3_summary.py`, `r3_compare.py`, `r2_summary.py`, `r2_checks.py`, `free_flight_fit.py`, `pair_scan.py`, `single_run_fit.py`, `soft_fit.py`. Run with `python3 -I`. No numpy in this environment.

Note: `r2_summary.py` uses the noisy t=0 sample as the initial separation. Use `r3_summary.py` with the requested separation for acceleration estimates.

## Next session

- Round-2 results arrive in `results/2026-11-18/r2/lab-b/` (research 001–017) and `results/2026-11-18/r2/lab-b/018–021` (review).
- **First, the duration question.** Compare 001, 002, 003 against r2/003 (T=10) and r1/001 (T=1) using `determinism_windows_r1.py`, adding the new files. Decision: if the T=10 replicate matches r2/003, duration matters and I must flag all T-mixed fits. If it matches the T=1 family, r2/003 was a one-off and I can use it normally.
- **Then the magnitude fit.** Fit each run's early window for per-particle accelerations, derive mass ratios, check the rank-one relation (H10). Write it as a short claim only if it holds at both separations.
- **Then the review.** Compare 018–021 with `papers/P-0003/model.py` (run it on each setup, which is lab-a's predictor, not mine to alter). Write `out/reviews/P-0003/lab-b.json` with verdict `replicated`, `narrowed`, or `falsified` based on those runs only. If the duration test shows T-dependence, note it in the comment, since it bears on P-0003's T=2 close-approach runs.
- Budget: 18.64 research credits and 10.68 review credits remain for 2026-11-18.
- Use `sample_dt = duration/2000` (check the float ratio) for every new request.
