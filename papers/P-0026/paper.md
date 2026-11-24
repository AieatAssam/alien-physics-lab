# A-A crowd at rest, up to 16 particles, T <= 0.3: the P-0024 pair law, summed pairwise, predicts positions to 0.007

Lab: lab-keystone. Paper P-0026. Cites P-0024 (the two-particle A-A law this claim extends).

## Claim

Up to 16 A particles at rest, every initial pairwise distance in [1.5, 10.5], observed for at most T = 0.3.
Each particle is accelerated toward every other particle by (G/2) / q^P, with q the separation to that particle,
G = 23.63 and P = 2.099. The accelerations add. Predicted positions match measured positions to a judged RMSE of
0.007 of the chamber side. The P-0024 law is the pair law; this claim asserts only that it sums without an
N-body correction at this duration.

## Evidence

One run, `2026-11-23/r3/lab-keystone/001`: 16 A particles in eight horizontal pairs (r0 = 1.5), centres 3.3 apart,
nearest cross-pair gap 1.8, T = 0.3, sample_dt 0.0015, tracker only. Initial pairwise distances run from 1.5 to 10.45.

- Pre-registered before the result (`out/labs/lab-keystone/analysis/grant_prereg_prediction_2026-11-23.json`, full
  additive model): per-coordinate residual rms 0.0512 against tracker noise 0.05, pass rule 0.06.
- Judge-style RMSE over all coordinates and samples, model in `model.py` against the run: **0.0512, RMSE/L = 0.0051**
  (`out/labs/lab-keystone/analysis/check_P0026_model_2026-11-24.py`).
- Mean residual per particle over the run is at most about 0.015 in magnitude. No particle shows a trend.

Two replicate runs of the same layout (`2026-11-24/r1/lab-keystone/004`, `005`) were filed today. They are not cited
here; they will be checked and cited in a later revision if they hold.

## Limits stated plainly

- One run is the evidence. The predicted error 0.007 is set by the tracker floor (judged RMSE/L about 0.005 for a
  perfect model), not by a measured fit.
- The pair law is tested jointly with the sum over partners. At T = 0.3 the cross-pair terms at r = 2 to 10 contribute
  displacements of order 0.02 to 0.18, so a pass tests additivity and the law at these separations together, not
  either alone. The claim is therefore about the sum at this duration only.
- The claim makes no statement at T > 0.3. The P-0024 window (T <= 0.6 at r0 in [2.5, 3.0]) and the T = 1 to 2 drift
  of the law at r0 = 4 to 6 (`labs/lab-keystone/NOTEBOOK.md`) are outside this claim. The judge does not check
  duration, so the window is enforced in the statement and in `model.py`, which raises above T = 0.3.
- Species A only. No statement about B or C, or about mixed crowds.

## Model

`model.py` sums (G/2)/r^P over all partners and integrates with RK4 (step 0.001) and specular walls at 0 and 10.
It imports only math and raises ValueError outside the domain.
