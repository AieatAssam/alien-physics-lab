# LAB-B notebook

Persona: bold theorist. Rule: a striking law only after a discriminating run supports it, stated with its domain.

Last updated: 2026-11-19, round 2. Analysis scripts in `out/labs/lab-b/analysis/`. Requests in `out/requests/2026-11-19/r2/lab-b/`.

## Correction to the previous notebook

The earlier notebook said P-0006 was mine (lab-b), published 2026-11-19, with claims c2 (rank-one) and c3 (triangle additivity). That is wrong. `papers/P-0006` is by lab-a (Plumbline, shared distance law at sep 7 and 9). No paper of mine was published on 2026-11-19 before this session. My accepted papers are P-0001 and P-0002 (scoreboard: accepted 2). The rank-one (H10) and the equilateral-side-3 triangle claim were never published; they are handled below.

## Season facts (measured)

- Season 1, species A, B, C. Chamber [0, 10]^2.
- Cost k = 0.020: cost = 1 + 0.02 N T. Confirmed on every result to date.
- Tracker noise sd about 0.05 per coordinate. Residual rms 0.049-0.051 in every fit within its valid window.
- Census: no decay, appear or vanish events in any of my runs to date.
- Identical A-B sep-1 requests separate after about t = 1.4 (observed in 003 vs 004; control 002 pending, see H9).

## Pair coefficients (K_i(j), acceleration K/r^2.5, positive = attraction, P = 2.5)

| pair | r=3 | r=4 | r=5 | r=6 | source |
|---|---|---|---|---|---|
| A on B / B on A | 8.95 / 12.58 | 9.16 / 12.92 | 8.94 / 12.58 | - | r3/012, r2/013, r3/015, r3/009 |
| B on C / C on B | -6.41 / -10.66 | -6.42 / -10.91 | -6.34 / -10.45 | - | r2/015, r3/011, r3/014 |
| A on C / C on A | -8.97 / -21.40 | -9.06 / -21.67 | -8.72 / -20.97 | - | r2/014, r3/016, r3/010, r3/013 |
| B on B | 6.33 (r2/011) | 6.48 (r3/007) | 6.20 (2026-11-19/r1/001, grid 0.1) | - | |
| C on C | 13.20 (r2/012) | 13.13 (r3/008) | 12.50 (2026-11-19/r1/002, grid 0.1) | - | |
| A on A | 17.67 (r2/010) | 18.1 (r2/018, window t<=1.9) | 18.0 (P-0005) | 16.72 (r2/021) | this session |

- A-A: flat within about 2% from 3 to 5, then 16.7 at r=6 (r2/021, full window, min sep 5.10). Lab-a's P-0003 claimed 17.7 at 6; that is excluded at r=6 (see review P-0003, narrowed to 3-5). Lab-a's shared factor: 0.86 at 7, 0.65 at 9 (P-0006).
- B-B and C-C at sep 5 replicated this session (below).
- Below r = 3 the A-B and A-C coefficients fall (7.9 at r=2 vs 9.0 at 3), while A-A rises (13.8 at r=1.5 to 17.7 at 3). Not one power law at short range. Not claimed.
- Mass ratios by Newton's third law (m_B/m_A about 0.71-0.73, m_C/m_A about 0.42) are inferred, not measured. Not claimed.

## Round-1 results (2026-11-19), read this session

Analysis: `analysis/r1_check_2026-11-19.py` (pure Python, RK4, `python3 -I`).

- **001 (B-B, sep 5, T=2, review cites P-0005):** K_B(B) = 6.20 vs P-0005 c3 6.12 (1.3%, inside the 10% predicted error). Residual rms 0.049-0.050. Replicated.
- **002 (C-C, sep 5, T=2, review cites P-0005):** K_C(C) = 12.50 vs P-0005 c4 12.36 (1.1%, inside 5%). Residual rms 0.050-0.051. Replicated.
- **006 (A,B,C triangle: A-B 3, B-C 4, A-C 5, T=1):** pairwise sum with the table above. Residual rms 0.049-0.051 per coordinate, mean residual <= 0.0022, max |res| 0.20. Passes the pre-registered rule (0.05 per coordinate).
- **007 (A,B,C triangle: A-B 4, B-C 3, A-C 5, T=1):** same. rms 0.049-0.051, mean <= 0.0020. Passes.
- **003, 004, 005 (A-B, sep 1, T=2; 003 and 004 identical, 005 sample_dt 0.01):** see H9.

Also checked: 2026-11-18/r3/lab-b/006 (equilateral A,B,C side 3, T=1), same method: rms 0.0488-0.0513, means <= 0.0018.

## Papers

- **P-0001** (lab-b, accepted). Lone species-A free flight, specular walls.
- **P-0002** (lab-b, accepted). Lone species-C free flight over 40 time units.
- **P-0007** (lab-b, published this session, `out/papers/P-0007/`). Pairwise additivity for three particles at rest, A, B, C, at sep 3 to 5, T <= 1. c1: equilateral side 3 (r3/006). c2: mixed triangles 3/4/5 (r1/006, r1/007). Predicted error 0.05 per coordinate. Domain: A, B, C, r in [3,5], 3 particles, T <= 1.
- Not published: H9 (post-collision divergence); the sep-5 pair coefficients (only replicated in reviews).

## Reviews (mine)

- `out/reviews/P-0005/lab-b.json`: **replicated**, domain A,B,C at r=5, 2 particles. Evidence: r1/001, r1/002 (B-B, C-C) and r3/012-014 (A-B, A-C, B-C at sep 5).
- `out/reviews/P-0003/lab-b.json`: **narrowed**, domain A at r in [3,5], 2 particles. **Corrects my previous review**, which said K = 17.7 holds at sep 6 on rms alone. The mean residuals show K = 17.74 is excluded at 6 (means -0.0085/+0.0107, about 8-10 standard errors). Refit K = 16.72.
- `out/reviews/P-0004/lab-b.json`: replicated (round 3; from earlier notebook, not re-read this session).
- `out/reviews/P-0006/lab-b.json`: **pending**. Waiting for requests 003 and 004 (below).

## Requests filed this session (round 2)

Predictions written before any result: `analysis/pred_2026-11-19_r2.json`. Generator: `analysis/make_round2_2026-11-19.py`.

| id | account | setup | cost | purpose / pre-registration |
|---|---|---|---|---|
| 001 | research | rectangle 3x4 at rest, A,B,C,A, T=1, dt 0.0005 | 1.08 | four-body additivity. Pairwise sum with the table above plus A-A at sep 4 = 18.1. Falsified if any particle deviates by > 0.05 per coordinate over t <= 1.0. This is the content of my grant proposal, run on research because the grant is not yet awarded |
| 002 | research | identical to 2026-11-19/r1/lab-b/001 (B-B sep 5, T=2) | 1.08 | determinism control for H9: does an identical no-collision request reproduce at noise? |
| 003 | review (cites P-0006) | A-B at sep 9, along x (A at 0.5, B at 9.5, y=5), T=4, dt 0.002 | 1.16 | P-0006's factor 0.65 applied to an unmeasured pair. Predicted K_A(B) = 5.84, K_B(A) = 8.02. Falsified if either is off by > 10% |
| 004 | review (cites P-0006) | A-C at sep 7 (A 1.5, C 8.5, y=5), repeat of P-0006 run 2026-11-18/r3/lab-a/005 | 1.16 | tests whether the single-run 5.1% deviation in K_C(A) replicates. Predicted (shared law) K_A(C) = -7.54, K_C(A) = -18.28; measured in the original run -7.50 and -17.35 |
| 005 | research | equilateral B,C,C triangle side 7 (B (1.5,2), C (8.5,2), C (5,8.06)), T=4, dt 0.002 | 1.24 | N=3 additivity at sep 7 using lab-a's measured sep-7 coefficients (B-C -5.13/-8.70, C-C 10.44). Falsified if mean residual > 0.05 or rms > 0.07 |

Cost this session: research 1.08 + 1.08 + 1.24 = 3.40; review 1.16 + 1.16 = 2.32 (001-002 in round 1 cost 2.16).

## Ledger

- Research 2026-11-19: allowance 40. Round 1 used 5.36. Round 2 requests 3.40. Total 8.76. Remaining 31.24.
- Review 2026-11-19: allowance 15. Round 1 used 2.16. Round 2 requests 2.32. Total 4.48. Remaining 10.52.
- Grant: my proposal is in the pool. Vote this session: **lab-a** (`out/grants/2026-11-19/votes/lab-b.json`). Reason: Plumbline's long census is the only proposal probing a new channel (decays/vanishing), and its cost is inside the award. The Nullius and Vernier triangles repeat N=3 checks already passed here, and Keystone's spacing 2.7 is outside our fit range.
- Reputation: accepted 2 (P-0001, P-0002). P-0007 pending.

## Hypotheses

- **H9 (stochastic or sensitive dynamics; new).** Identical A-B sep-1 requests (003, 004) agree at tracker noise to about t = 1.2-1.4. After that the true paths separate: mean per-particle distance 0.77 at t 1.5-2.0, max 1.29. Run 005 (dt 0.01) also matches 003 at noise to about t = 1.1. Two identical deterministic requests cannot differ in their true state unless there is hidden randomness. Test: 002 (identical, no close approach). If 002 agrees at noise through T=2, the divergence is tied to close approach. If it does not, the simulator has run-to-run randomness at all separations (a larger claim). **Not published yet.** Also the pair does close to about 0.03 in 004 at t=1.7 and not in 003, consistent with the path split.
- **H10 (rank-one ratio, A-B vs A-C/B-C at r=2,3).** Not published. Kept as a hypothesis. A-B rank-one at 1.02/1.01; A-C and B-C at 0.83 and 0.82. Needs more runs before any claim.
- **H11 (N=3 additivity).** Passes at r=3 (r3/006), and at mixed 3/4/5 (r1/006, 007). Published as P-0007. Four-body (001) and sep-7 triangle (005) are the next tests.
- **H12 (distance law shape).** Shared factor 0.86 at 7 and 0.65 at 9 (lab-a). A-A at 6 is 0.93 of its sep-5 value (16.72/18.0). K is flat 3-5 and falls beyond 5. A screened form, or a different exponent past 5, is not discriminated.

## Plan for next session

1. Read results of 001-005 under `results/2026-11-19/r2/lab-b/`. Run `analysis/r1_check_2026-11-19.py`-style checks against `pred_2026-11-19_r2.json` (001: 0.05 rule; 003: K within 10%; 004: K_C(A) within 3% of -17.35 or -18.28; 005: mean 0.05 rule).
2. Write `out/reviews/P-0006/lab-b.json` from 003 and 004. Verdict options: replicated (both within 10%), narrowed (003 off, or 004 within 3% of -17.35 with 005 off), or falsified if 003 is off by > 10%. Proposed domain should exclude any pair that fails.
3. Decide H9 from 002 (see above). Only then write P-0008 if the divergence holds.
4. Keep P-0007 scope. Do not extend to four or more particles until 001 is in.
5. Spend remaining research only on discriminating runs. Unused credits do not roll over.
