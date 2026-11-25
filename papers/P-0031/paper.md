# Three and four A particles at rest, symmetric layouts: the P-0027 pair table summed pairwise predicts positions to 0.007 (T <= 2)

Lab: lab-b (Icarus). Paper P-0031. Cites P-0027 (the A-A K(r) table) and P-0028 (the N = 8 ring check of the same table).

## Claim

Three or four A particles at rest, every initial pairwise distance in [5.0, 7.1], observed for at most T = 2.0. Each
particle is accelerated toward every other particle by K(r)/r^2.5, with K(r) the P-0027 piecewise-linear table. The
accelerations add. Walls at 0 and 10 reflect elastically. Measured positions are predicted to a judged RMSE of 0.007 of
the chamber side.

## Evidence

Two tracker-only runs, both symmetric, both at rest:

| request | layout | N | pair range | T | judged RMSE/L | zero-force null |
|---|---|---|---|---|---|---|
| 2026-11-25/r2/lab-b/007 | equilateral triangle, side 6.0, centre (5, 5) | 3 | 6.0 | 2.0 | 0.00492 | 0.0226 |
| 2026-11-25/r2/lab-b/008 | square, side 5.0, centre (5, 5) | 4 | 5.0 to 7.07 | 1.5 | 0.00477 | 0.0222 |

- The bar for a replication is 3 x 0.007 = 0.021. Both runs are under it by a factor of about four.
- Noise floor: a correct model gives about 0.005 at tracker sd 0.05. Both runs sit on that floor.
- Scoring was pre-registered (`out/labs/lab-b/analysis/PREREG_additivity_N34_2026-11-25.md`) before the runs were scored. The
  scoring script is `out/labs/lab-b/analysis/additivity_N34_2026-11-25.py`.
- Global-factor test: one factor f on K over both runs gives f = 0.996 +/- 0.004 (|f - 1| / sigma = 0.98). chi2/dof = 0.94
  at sd 0.05. In these layouts a uniform change of K larger than about 1 percent is excluded at 2 sigma. A three-body term
  that does not look like a uniform scale of K is not constrained by this factor test.
- Power: the zero-force null is above the bar for both runs, so each run discriminates the model from no force.

## Limits stated plainly

- Two runs, both in highly symmetric layouts. A symmetric layout can hide a three-body term that projects onto the
  global factor, so "additive" here means "additive in these geometries". Asymmetric N = 3 and N = 4 layouts are not tested.
- Pair separations in both runs lie in [5.0, 7.1]. Pairs near 3 (where P-0027 is less certain, see its limits) are not tested.
- Duration is at most 2.0. Nothing is claimed beyond that. P-0028 gives the N = 8 ring at T <= 1.
- Tracker only. No species B or C, no initial velocity, no census events.
- The judged metric cannot resolve K to better than a few percent at these durations, so the claim is about positions, not
  about the coefficient at any one separation.

## Model

`model.py` implements the pairwise sum with RK4 (step 0.001) and specular walls. It imports only math. `predict()` raises
ValueError for N outside {3, 4}, species other than A, nonzero initial velocity, any initial pair outside [5.0, 7.1], and
duration above 2.0. Its output on runs 007 and 008 reproduces the pre-registered scores above to the printed digits.
