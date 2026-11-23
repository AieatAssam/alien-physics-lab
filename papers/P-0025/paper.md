# A-B pair at rest, separation 4 to 8, T <= 2: K_B/K_A = 1.41 with an interpolated K_A(r) table

Lab: lab-b. Paper P-0025. Cites P-0022 (A-B at separation 2, own paper).

## Claim

One A and one B particle, both at rest, initial separation r0 in [4.0, 8.0], observed for at most T = 2.0.
Each particle accelerates toward the other with magnitude K / r^2.5, where r is the current separation.

- K_A(r) (acceleration of A due to B) is linear in r between nodes:
  9.10 (r = 4), 9.26 (r = 5), 8.52 (r = 6), 7.75 (r = 7), 6.85 (r = 8).
- K_B(r) (acceleration of B due to A) = 1.41 K_A(r) at every r. The ratio is the mass ratio m_A / m_B.
- Predicted error: judge RMSE / L of 0.007 against tracker data (tracker noise 0.05 per coordinate gives a floor of 0.005).

Scope: species pair A-B only, two particles, specular walls at 0 and 10. No statement about other separations,
times beyond 2.0, other species, three or more particles, or close approach below r = 4 (a run at r0 = 4 passes
r = 2.2 by T = 2 and the constant-K fits stop describing it near T = 2.2).

## Evidence

Three runs, all T = 2.0, cited for their initial setups inside the domain:

- `2026-11-23/r2/lab-b/006`: horizontal, r0 = 6.0. Free constant-K fit K_A = 8.45 +/- 0.24, K_B = 11.94 +/- 0.24 (ratio 1.413), chi2/n 0.96.
- `2026-11-23/r2/lab-b/007`: vertical, r0 = 6.0. Free fit K_A = 8.28 +/- 0.24, K_B = 11.75 +/- 0.24 (ratio 1.418), chi2/n 1.05.
- `2026-11-22/r3/lab-b/002`: horizontal, r0 = 6.0. Free fit K_A = 8.95 +/- 0.24, K_B = 11.36 +/- 0.24 (ratio 1.27), chi2/n 1.00.
  This run is the outlier. It is kept in the evidence. The other two runs and the T <= 2 windows of
  `2026-11-23/r1/lab-b/006` and `2026-11-23/r2/lab-b/008` give ratios 1.35 to 1.45.

Predictor check: judge-style RMSE / L of this model against each run, truncated to t <= 2 (`out/labs/lab-b/analysis/check_P0025_model_2026-11-23.py`):
006 0.00490, 007 0.00513, 2026-11-22/r3/002 0.00502, r2/008 (T truncated to 2) 0.00502, r1/006 (T truncated to 2) 0.00493,
and r2/009 at r0 = 4.0 (T truncated to 2) 0.00478. All are at the tracker noise floor.

## Limits stated plainly

- At T <= 2 and r >= 6, a 0.6 change in K_B moves a particle by about 0.01, which is below tracker noise per run.
  This claim therefore does not resolve the mass ratio to better than about 0.03 on its own. The ratio is a
  consistency statement across runs, not a sharp prediction.
- Only the r = 6 nodes have more than one replicate. The nodes at 4, 5, 7 and 8 come from single runs or from runs
  outside the claim window (T up to 5). Held-out runs at r = 4.5, 5.5, 7.5 and 7.8 (2026-11-23/r3/lab-b/001-004) are
  filed to test the interpolation. Their results are not used in this paper.
- The exponent 2.5 is assumed. It is not tested here.

## Model

`model.py` (out/papers/P-0025/model.py) implements the interpolated constant-K approach with RK4 (step 0.002) and specular walls.
It imports only numpy and math.
