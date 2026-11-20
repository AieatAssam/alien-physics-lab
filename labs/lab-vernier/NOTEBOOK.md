# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost) before physics claims, then replicate and review other labs' claims at their edges with precise numbers. Reusable tools are in `out/labs/lab-vernier/analysis/`.

## Corrections to earlier notebooks

- **P-0009 is Plumbline's paper (B, C, C triangle), not mine.** My round-1 noise paper ("Tracker noise for a lone particle") was never placed in `papers/`, so it is not published. If I publish it, it needs a new number. Its evidence stands (pooled 28,014 residuals, sd 0.050 per coordinate, white, no clipping at x = 0.05).
- **Lone-particle runs pass the numeric domain test vacuously.** The domain rule checks species, N and pairwise separations. A single particle has no pairs, so it is "in domain" for any pair claim whose species list contains its species. For P-0003 (A-A pair attraction), my lone-A runs (2026-11-19/r1/001, 002, 005, 006; r2/002, 004; r3/003) pass the numeric test with error about 0.005, but they test free flight, not the pair force. I do not cite them for any pair claim. This is a reviewing trap for everyone; the review should say so.
- **Integrator sensitivity near close approach.** An A-A pair at r = 4 passes close to contact by T = 2. The paper's trajectory, and so the review error, depends on the integrator step: with the paper's step 0.002, K = 17.74 gives rms 0.053 per coordinate; with step 0.0005 the same K gives rms 0.74. A review that calls a pair run replicated or falsified near contact should check two steps before it counts the result. (Analysis: `aa_integrator_scan.py`.)
- Four reviews of mine were logged unsupported earlier (reputation: 4). The replicated bar is three cited in-domain runs of mine, and I will not write "replicated" with fewer.

## Round 2, 2026-11-20: results of round 1 and what they decide

Round-1 runs (all status ok, no census events):

| request | setup | error (paper's predict, /10) | decides |
|---|---|---|---|
| r1/001 | lone C, T=40, reflections | 0.00485 | P-0002 third run |
| r1/002 | A pair at r=4, T=2 | 0.00532 | P-0003 at r=4 (see integrator caveat) |
| r1/003 | A pair at r=6, T=2 | 0.00523 | P-0003 at r=6 (K barely constrained) |
| r1/004 | lone A moving, T=2 | 0.00504 | H4 timing |
| r1/005 | A-B at r=4, T=2 | 0.00521 | P-0008 mixed pair at 4 |
| r1/006 | B-C at r=3, T=2 | 0.00511 | P-0008 mixed pair at 3 |

- **P-0002 (lone C, walls): replicated.** Three in-domain runs at error 0.0049 or less (r1/003, r3/001, r1/001). Review updated (`out/reviews/P-0002/lab-vernier.json`).
- **P-0003 (A-A, r 3 to 6): "falsified" is too strong; the claim should be narrowed.** r = 3 fails (r1/007, error 0.181). r = 4 and r = 6 pass at noise level with the paper's integrator. Earlier "falsified" stood on one run; with r = 4 and 6 passing it is no longer the right verdict. The review will be rewritten to narrowed (proposed r 4 to 6) when r2/007 (r = 5) returns, so three in-domain runs support the narrowed domain. Caveat to state in that review: the r = 4 pass depends on the step (see above); r = 6 does not constrain K (K from 17.0 to 18.0 all fit at noise).
- **A-A coefficient (analysis `aa_integrator_scan.py`).** With the paper's integrator, K = 17.70 is the best fit at r = 4 (rms 0.0527) and K = 18.0 gives rms 0.25. With a 4x smaller step the best is K = 17.65 (rms 0.0530) and K = 18.0 gives rms 0.11. Both are above the 0.05 noise. So K_A(A) = 18.0 (used by P-0004 and P-0008) is not supported at r = 4. P-0003 uses 17.74. Lab-a's own numbers disagree (18.0 vs 17.74), which is worth flagging.
- **P-0008 (lab-b, pairwise additivity): narrowed to r = 5, N <= 3.** Mixed pairs at 3 and 4 pass (A-B at 4, B-C at 3). A-A fails at 3 (r1/007) and is off at 4 (above). The schema cannot exclude A-A only, so I keep the proposed domain at r = 5. Review updated (`out/reviews/P-0008/lab-vernier.json`). A-C at 3 and 4 is not tested by me.
- **H4 (sample timing): no offset detected.** r1/004: x mean residual -0.0009 (se 0.0038); slope of residual vs t gives time offset tau = -0.003 +- 0.002 (about 1.4 sigma); y mean -0.0036 (se 0.0036). Bounded claim: sample time offset below about 0.005 time units. The earlier round-1 y-excess (about 2 s.e.) is consistent with noise.

## Round 2 requests filed today (`out/requests/2026-11-20/r2/lab-vernier/`)

Budget check. Research: 40 allowed, 3.20 used in round 1, 3.07 filed now (remaining 33.73 after these). Review: 15 allowed, 3.96 used in round 1, 8.16 filed now (remaining 2.88 after these). Costs use cost = 1 + 0.02 N T, consistent with every result so far.

| request | account | cites | setup | cost | purpose |
|---|---|---|---|---|---|
| 001 | review | P-0010 | A-A at r0 = 9, T=6, dt=0.01 | 1.24 | far-field G(9), largest K |
| 002 | review | P-0010 | C-C at r0 = 7, T=6 | 1.24 | far-field G(7) with the S_C factor |
| 003 | review | P-0010 | B-C at r0 = 8 (repulsive), T=6 | 1.24 | far-field G(8) with the S_C factor |
| 004 | review | P-0009 | B, C, C triangle side 5, T=2 | 1.12 | replication, run 1 |
| 005 | review | P-0009 | C, B, C triangle side 5 (rotated), T=2 | 1.12 | replication, run 2 |
| 006 | review | P-0009 | C, C, B triangle side 5 (rotated 45 deg), T=2 | 1.12 | replication, run 3 |
| 007 | review | P-0003 | A-A at r = 5, T=2 | 1.08 | third in-domain pair run for narrowing P-0003 |
| 008 | research | - | B-B at r = 1.0, T=0.6, dt=0.003 | 1.02 | close-range probe (close-BB, exploratory) |
| 009 | research | - | A-B at r = 1.0, T=0.6 | 1.02 | close-range probe (close-AB, exploratory) |
| 010 | research | - | B-C at r = 1.0, T=0.6 | 1.02 | close-range probe (close-BC, exploratory) |

Pre-registered bars: review runs must give error at or below 0.03 (3 x predicted_error 0.01 for P-0010 and P-0003; 3 x 0.01 for P-0009). Not an exact model: a pass means the paper's predict() matches at noise level. Check each P-0009 and P-0010 run with the integrator scan before calling it falsified: the 3-body triangle at side 5 and the A-A at r0 = 9 are not near contact, so the integrator should not matter there.

Vote: `out/grants/2026-11-20/votes/lab-vernier.json` votes for **lab-a (Plumbline)** and its close-CC proposal. Reason: a pre-registered close-range C-C pair (r = 2, cost 1.02) with an explicit prediction and falsifier, filling an open bounty and testing the C-C coefficient that P-0005 and P-0009 use. I did not vote for my own proposal.

## Review status of papers in the ledger

- **P-0002 (lab-b, lone C): replicated.** Done.
- **P-0003 (lab-a, A-A): narrowing to r 4 to 6 pending r2/007.** Current file still says falsified (`reviews/P-0003/lab-vernier.json`, from round 1); it is superseded by the narrowing once 007 returns.
- **P-0008 (lab-b, pairwise sum): narrowed to r = 5, N <= 3.** Done (see above).
- **P-0009 (lab-a, B, C, C triangle N=3): pending r2/004 to 006.** No review written yet; no evidence yet. Verdict to follow the three runs with the bar at 0.03.
- **P-0010 (lab-keystone, far-field G(r), r0 6 to 9): pending r2/001 to 003.** Out-of-sample test of the in-sample fit. Verdict to follow the runs.
- **P-0004 (lab-a, A-B and A-C at r=5): not reviewed this round.** It is superseded by P-0005, which carries the same coefficients. Three A-B runs would cost 3.24, more than the 2.88 review credit left after the requests above. Note for next round.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported (P-0009 noise paper, not published).
- **H2 (species-independent noise, at N=1).** Supported at 2.4% spread (A, B, C).
- **H3 (no clipping near a wall).** Supported at x = 0.05 and in the corner.
- **H4 (no sample-timing offset).** Supported at about 0.005 time units (r1/004).
- **H5 (stationarity over T = 100).** Mean supported; the x-spread variation was not reproduced and is treated as chance.
- **H6 (P-0003 domain).** r = 3 fails (r1/007). r = 4 and 6 pass with the paper's integrator; K at r = 4 is 17.70, not 18.0, and K at r = 6 is not constrained. Narrowed domain r 4 to 6 pending r2/007.
- **H7 (P-0006 shared-law factor at separation 9 for A-C).** Supported within 3% in one fit; one run only.
- **H8 (P-0008 coefficients flat over separations 3 to 5).** Supported for A-B at 4 and B-C at 3 (r1/005, 006) and at 5 (four runs). Not supported for A-A at 3 and 4 (K = 18.0 excluded at 4). A-C at 3 and 4 untested.
- **H10 (new): the A-A coefficient is 17.70 at r = 4, not 18.0.** Supported by the scan (noise-level fit at 17.65 to 17.70 with either step; K = 18.0 excluded). Only r = 4 constrains it; r = 6 is flat.

## Plan for next round

1. When round-2 results return: run `review_check.py` on P-0009 (claim P-0009-c1), P-0010 (P-0010-c1), P-0003 (P-0003-c1), and the integrator scan on any run that closes below r = 1.5.
2. Write P-0010 review (replicated if 001, 002, 003 each at or below 0.03; otherwise say which runs fail and why). Note the duration limit T <= 6 is part of the claim.
3. Write P-0009 review from 004 to 006 (N = 3, B, C, C; side 5 only; state that the claim covers side 5 only).
4. Rewrite P-0003 review to narrowed (r 4 to 6), citing 002, 003 and 007, and keep r1/007 as the failing run. Include the integrator caveat for r = 4.
5. Use close-range probes (008 to 010) only if the runs are stable at both integrator steps. Then decide whether to file a close-range claim (need three runs in domain).
6. Do not publish a new physics claim until three in-domain runs support it.

## Notes for reproducibility

- Tools are in `out/labs/lab-vernier/analysis/`. Run with `python3 -I`.
- `review_check.py <paper> <claim>` applies the review rules to my own runs (note: lone particles pass the numeric domain test; see above).
- `aa_coeff_fit.py`, `aa_integrator_scan.py`: A-A coefficient at r = 4 and 6.
- `timing_h4.py`: sample-timing check on r1/004.
- `runtable.py`: table of all my runs with setups and status.
- `file_round2_requests.py`: writes the round-2 request files. `plan_check.py`: simulates planned setups with the paper models for wall and collision checks.
- I have not read `gate/`, `tools/`, `exam_papers.json`, or any predictor or score files. I will not.
