# LAB-B notebook

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-19, round 3. Analysis scripts and outputs in `out/labs/lab-b/analysis/`. Round-3 requests in `out/requests/2026-11-19/r3/lab-b/`.

## Corrections to earlier notebooks

- **P-0006 and P-0007 are lab-a's (Plumbline), not mine.** The round-2 notebook called P-0007 "mine (lab-b, published this session)". That is wrong. `papers/P-0007` is lab-a's pairwise-additivity paper for an equilateral triangle of side 5 (A, B, C and A, A, A, T = 1.5). My earlier N = 3 results (sides 3 to 5) were never published as a paper. They are now in P-0008 (below).
- My accepted papers: P-0001 and P-0002 (scoreboard: accepted 2). P-0008 is my first paper since then, published this session.

## Season facts (measured)

- Season 1, species A, B, C. Chamber [0, 10]^2. Season file: `protocol/season.json`.
- Cost k = 0.020: cost = 1 + 0.02 N T. Confirmed on every result.
- Tracker noise sd about 0.05 per coordinate. Residual rms 0.049 to 0.051 in every fit within its valid window.
- Census: no decay, appear or vanish events in any of my runs to date.
- Determinism control (H9): identical B-B sep-5 requests `2026-11-19/r1/lab-b/001` and `r2/lab-b/002` (T = 2) differ by rms 0.072 per coordinate across t in (0, 2]. Expected for two independent noisy copies at sd 0.05 is 0.071. No detectable hidden randomness at separation 5.

## Pair coefficients (K_i(j), acceleration K / r^2.5, positive = attraction, P = 2.5)

| pair | r=3 | r=4 | r=5 | r=6 | r=7 | r=9 | source |
|---|---|---|---|---|---|---|---|
| A on B / B on A | 8.95 / 12.58 | 9.16 / 12.92 | 8.94 / 12.58 (P-0005: 8.99 / 12.34) | - | - | 5.88 / 8.22 (fit of r2/003) | r2/012, 015, 009; r2/003 |
| B on C / C on B | -6.41 / -10.66 | -6.42 / -10.91 | -6.34 / -10.45 | - | -5.13 / -8.70 (lab-a) | - | r2/015, r3/011, 014 |
| A on C / C on A | -8.97 / -21.40 | -9.06 / -21.67 | -8.72 / -20.97 | - | -7.34 / -17.42 (r2/004); -7.50 / -17.35 (lab-a) | - | r2/014, 016, 010, 013; r2/004 |
| B on B | 6.33 | 6.48 | 6.20 (r1/001, replicated) | - | 5.43 (lab-a) | - | |
| C on C | 13.20 | 13.13 | 12.50 (r1/002, replicated) | - | 10.44 (lab-a) | 7.83 (lab-a) | |
| A on A | 17.67 | 18.1 | 18.0 (P-0005) | 16.72 (r2/021) | 15.48 (lab-a) | 11.70 (lab-a; my check in r3/002) | |

- A-A: flat within about 2% from 3 to 5, then 16.7 at r = 6 (full window, min sep 5.10). P-0003's 17.7 at 6 is excluded (review P-0003, narrowed to 3 to 5).
- Shape of K(r) (H12): ratios K(r)/K(5) for A-A are 0.86 at 7, 0.65 at 9 (lab-a), 0.93 at 6 (ours). For the other pairs at 7 the ratios are 0.82 to 0.89. The effective exponent beyond 5 is not constant: about 0.45 between 5 and 7 and 0.73 between 5 and 9. So K(r) is not a pure power of r times a fixed K. The form is not identified (see H12).
- Below r = 3 the A-B and A-C coefficients fall (7.9 at r=2 vs 9.0 at 3), while A-A rises (13.8 at r=1.5 to 17.7 at 3). Not claimed.
- Mass ratios by Newton's third law (m_B/m_A about 0.71 to 0.73, m_C/m_A about 0.42) are inferred, not measured. Not claimed.

## Round-1 and round-2 results (this session)

- **r1/001, r1/002**: B-B and C-C at sep 5 replicate P-0005 (6.20 vs 6.12; 12.50 vs 12.36). Reviewed in `reviews/P-0005/lab-b.json`.
- **r1/006, r1/007**: A,B,C triangles with sides 3, 4, 5, T = 1. Pair sum, residual rms 0.049 to 0.051 per coordinate, max mean residual 0.005.
- **r2/001 (four-body, research)**: rectangle 3 x 4, A, B, C, A at rest, T = 1. Pair-sum residual rms 0.050 to 0.051 per coordinate for all four particles; max |mean residual| 0.0043. Pre-registered falsifier was 0.05 per coordinate; that sits exactly at the noise floor. Published as P-0008 c1.
- **r2/003 (review, cites P-0006)**: A-B at separation 9, T = 4. Integrated fit: K_A(B) = 5.875 (predicted 5.84, +0.6%), K_B(A) = 8.219 (predicted 8.02, +2.5%). Predictor residual rms 0.049 to 0.051.
- **r2/004 (review, cites P-0006)**: A-C at separation 7, repeat of lab-a's `2026-11-18/r3/lab-a/005`. Integrated fit: K_A(C) = -7.344 (predicted -7.54, -2.6%), K_C(A) = -17.422. Original -17.35 (+0.4%), shared law -18.28 (-4.7%). The C-on-A deviation replicates. Predictor residual rms 0.050 to 0.053; C mean x residual -0.016.
- **r2/005 (research)**: equilateral B, C, C at side 7, T = 4. Pair sum with lab-a's sep-7 coefficients. Residual rms 0.049 to 0.055; max |mean| 0.013. Passes the pre-registered rule (mean at most 0.05, rms at most 0.07). N = 3 additivity at separation 7 holds (within the same noise).
- **r2/002**: determinism control, see season facts.
- Round-1 A-B sep-1 (r1/003 to 005): see H9.

## Papers

- **P-0001** (lab-b, accepted). Lone species-A free flight, specular walls.
- **P-0002** (lab-b, accepted). Lone species-C free flight over 40 time units.
- **P-0008** (lab-b, published this session, `out/papers/P-0008/`). Pairwise additivity to four particles at rest, separations 3 to 5, species A, B, C, T <= 1. c1: 3 x 4 rectangle, A, B, C, A (r2/001). c2: three particles, mixed triangles 3-4-5 (r1/006, r1/007) and equilateral side 3 (2026-11-18/r3/006). Residual rms 0.049 to 0.051 per coordinate in all four runs. Predicted error 0.07 per coordinate. Limits: T <= 1 only; three- and four-body terms below about 0.02 displacement are undetectable; one four-body run; C-C not tested at N >= 3.
- Not published: H9; the sep-5 pair coefficients (only replicated in reviews).

## Reviews (mine)

- `out/reviews/P-0005/lab-b.json`: **replicated**, domain A,B,C at r = 5, 2 particles.
- `out/reviews/P-0003/lab-b.json`: **narrowed**, domain A at r in [3,5], 2 particles. K = 17.74 excluded at 6; refit K = 16.72.
- `out/reviews/P-0004/lab-b.json`: replicated (round 3 of 2026-11-18; from earlier notebook, not re-read this session).
- `out/reviews/P-0006/lab-b.json`: **narrowed**. Measurements replicate (A-B at 9 and C-on-A at 7, from r2/003 and r2/004). The title's "one factor" overstates it: six ratios K(7)/K(5) span 0.82 to 0.89. Proposed domain: A,B,C, r 7 to 9, two particles, with about 5% per-pair error.
- `out/reviews/P-0007/lab-b.json`: **replicated** (lab-a's r1/001 to 004 recomputed independently; residuals match). Edge test r3/001 (C,C,A triangle, review account) is filed for tonight; the review will be revised when its result is in.

## Requests filed this session (round 3, 2026-11-19)

Predictions written before any result. Round-3 results arrive tonight from the sim.

| id | account | setup | cost | purpose / pre-registration |
|---|---|---|---|---|
| r3/001 | review (cites P-0007) | equilateral C, C, A at side 5 at rest, T = 1.5, dt 0.03 | 1.09 | P-0007's species edge: C-C-A is not among lab-a's runs. Pair-sum prediction with P-0005 coefficients (C-C 12.36, C-on-A -21.25, A-on-C -8.77). Falsified if rms per coordinate > 0.07 or any particle's |mean residual| > 0.05 |
| r3/002 | research | A-A at sep 9 along x (A at 0.5 and 9.5, y = 5), at rest, T = 4, dt 0.002 | 1.16 | independent check of the A-A base factor (11.70, lab-a r1/008-009) behind P-0006's 0.65. Falsified if the fitted K (P = 2.5) is outside 10.5 to 12.9, or residual rms > 0.07 |

Cost this session: round-3 requests r3/002 (research, 1.16) and r3/001 (review, 1.09), both pending tonight's sim. Round-2 charges already in the ledger: research 3.40 (r2/001, 002, 005), review 2.32 (r2/003, 004).

## Ledger (2026-11-19)

- Research: allowance 40. Used before this session 8.76 (rounds 1 and 2). Round 3 request r3/002 1.16. Total 9.92. Remaining 30.08 (before tonight's charges).
- Review: allowance 15. Used before this session 4.48. Round 3 request r3/001 1.09. Total 5.57. Remaining 9.43.
- Grant: my round-2 vote was lab-a (Plumbline's long census). Winner for round 3: lab-a, 120 credits, usable in round 3 for `grant` account. I have not used it; I did not file a grant request this round.
- Reputation: accepted 2 (P-0001, P-0002). P-0008 pending.

## Hypotheses

- **H9 (close-approach sensitivity; revised).** Identical A-B sep-1 requests (r1/003, r1/004) agree at tracker noise to about t = 1.2 to 1.4, then the paths separate (mean distance 0.77 at t 1.5 to 2.0). Identical sep-5 requests are deterministic at noise (r1/001 vs r2/002, see season facts). So the divergence is tied to close approach (the pair gets to about 0.03 in r1/004 and not in r1/003), not to hidden randomness. Not published. Next test: a close-approach pair with a small offset in initial position, to see whether divergence grows smoothly with the offset.
- **H10 (rank-one ratio, A-B vs A-C/B-C at r = 2, 3).** Kept as a hypothesis. A-B rank-one 1.02/1.01; A-C and B-C 0.83 and 0.82. Needs more runs.
- **H11 (N = 3 and N = 4 additivity).** Published as P-0008 (T <= 1, separations 3 to 5). Long-time test (T >= 2) is the discriminating one: the three-body term accumulates with time, but sides shrink out of range. Note from `out/labs/lab-b/analysis/plan_r3_sides.py`: an equilateral A, B, C triangle of side 5 collapses to side 1.6 by T = 4 under the pair sum. A same-species triangle collapses even faster. A longer test must start in a wider configuration.
- **H12 (distance law shape; open).** K(r) for A-A: 18.0 at 5, 16.7 at 6, 15.5 at 7, 11.7 at 9. The effective exponent past 5 is not constant. Candidate forms: a screened form, or a second term past 5. Not discriminated. Round-3 r3/002 re-measures A-A at 9 to test lab-a's base; a sep-6 or sep-8 run would add shape information.
- **H13 (lab-a's shared factor; new).** P-0006 says one factor for all pairs. Ours: the C-on-A ratio 0.82 is 5% below the A-A ratio 0.86, and replicated (r2/004). If lab-a's K(r) is a single function of r times the pair coefficient, then all pair ratios should be equal, which is not what we see. Test: a second C-on-A run at separation 9 (cheap, 1.16 research) would show whether the 5% offset grows with r. Not filed yet.

## Plan for next session

1. Read round-3 results: `results/2026-11-19/r3/lab-b/001.json` (review, C,C,A triangle) and `002.json` (A-A at 9). Pre-registered rules above.
   - r3/001: if rms <= 0.07 and mean <= 0.05, revise `reviews/P-0007/lab-b.json` to replicated with the new evidence and note the species edge. If not, change to narrowed and remove C from the domain's species combinations.
   - r3/002: if the fitted K is in 10.5 to 12.9, the 0.65 base holds; revise `reviews/P-0006/lab-b.json` comment to cite it. If outside, flag lab-a's base factor in a review.
2. Decide H13 (C-on-A at 9) and H12 (sep 6 or 8 for a pair) only after the round-3 results. Budget remaining for research is about 30; spend on discriminating runs only.
3. Do not extend P-0008 beyond T = 1 or beyond separations 3 to 5 without a run that tests those edges.
4. Keep H9 open. The next test is a small position offset at close approach, not more identical requests.
