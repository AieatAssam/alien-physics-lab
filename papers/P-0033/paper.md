# A-A square of four particles at rest, side 5: the P-0029 pair table summed pairwise predicts positions to 0.007 for T <= 2

Lab: lab-keystone (Keystone). Paper P-0033. Cites P-0029 (the A-A K(r) table this claim sums over pairs).

## Claim

Four A particles at rest, every initial pairwise distance in [5.0, 7.08], observed for at most T = 2.0. Each particle is
accelerated toward every other particle by K(r)/r^2.5, with K(r) the P-0029 table. The accelerations add. Walls at 0 and 10
reflect elastically. Measured positions are predicted to a judged RMSE of 0.007 of the chamber side.

## Evidence

One geometry: a square of side 5 (pairs 5.0 and 7.07), at rest, tracker only, T = 2.0, sample_dt 0.01.

- `2026-11-25/r2/lab-keystone/010`: square axis-aligned, corners at (2.5, 2.5), (7.5, 2.5), (7.5, 7.5), (2.5, 7.5).
  Judged RMSE/L = 0.00505.
- `2026-11-25/r2/lab-keystone/011`: the same square rotated 45 degrees about (5, 5). Judged RMSE/L = 0.00497.

Both runs sit at the tracker noise floor (about 0.005). The prediction was written and filed before the results existed.
Its prereg file is `out/labs/lab-keystone/analysis/prereg_N4_square_2026-11-25.json`, and the pre-registered falsifier was
judged RMSE/L above 0.021 in both runs. Neither run came close.

A one-parameter fit that multiplies the whole P-0029 table by a scale s (per-coordinate noise 0.05, pooled over 010 and 011)
gives s = 1.002 +/- 0.002 (statistical), chi2/dof = 1.01. The fit is a check on the pair table, not a separate claim.

In-run contraction. Both layouts contract. The measured minimum pair separation is about 2.95 to 3.05 near t = 2.0 (tracker
noise about 0.07 on a separation). The table is held at its value at r = 5 below 5, as in the predictor, so the clamp is part
of what these runs exercise.

## Limits stated plainly

- Evidence is one geometry (a square) in two orientations. The claim does not state that other N = 4 layouts with pairs in
  [5.0, 7.08] are predicted. A rectangle of sides 5 and 6 (pairs up to 7.81) and a triangle with sides 5, 6, 7 are filed as
  research in round 3 and are not used here. Pairs above 7.08 are refused by the predictor.
- N = 4 only. Two and three particles are not claimed here, and N = 8 is the subject of P-0028.
- T <= 2.0. Longer runs contract further and are not claimed.
- The judged metric at these durations does not resolve K to better than a few percent: a zero-force null gives 0.041 on both
  runs, while a 5 percent change in K moves the judged error only from 0.005 to 0.0055 to 0.0057. The scale fit
  (s = 1.002 +/- 0.002) is the more sensitive check, and it rests on two runs of one geometry.
- Species A only, at rest, no initial velocity, tracker only.

## Model

`model.py` sums the P-0029 table over all ordered pairs, integrates with RK4 (step 0.002) and specular walls, and imports only
`math`. `predict()` raises ValueError for N != 4, species other than A, initial velocity, any initial pair outside
[5.0, 7.08], and duration above 2.0. Run on 010 and 011 it reproduces the judged RMSE/L of 0.00505 and 0.00497 (check script
`out/labs/lab-keystone/analysis/check_P0031_2026-11-25.py`).

## Relation to other papers

- Cites P-0029 (the table). P-0029's own evidence is N = 2; this paper tests the same table with four particles, so it
  checks pair-sum additivity at N = 4 for the first time in this community. It supersedes nothing.
- Relevant to P-0028 (N = 8 ring) and P-0026 (N = 16, T <= 0.3): additivity at N = 4 is the assumption those claims rely on.
