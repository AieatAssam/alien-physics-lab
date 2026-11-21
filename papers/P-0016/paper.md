# Close-range A-C pair at separation 1.0: repulsion with K_AC = -6.25 and K_CA = -14.78 (T <= 0.6)

Lab: lab-vernier. Companion to P-0015 (close-range B-C at the same separation). Fills the open problem close-AC if accepted.

## Claim

Two particles at rest, one species A and one species C, at initial separation 1.000, repel along the line joining them. Each particle accelerates away from the other with magnitude K / r^2.5, with K_AC = -6.25 on A due to C and K_CA = -14.78 on C due to A. Units are chamber and time units; negative means repulsion. The claim holds for durations T <= 0.6, before any wall contact.

## Evidence

- Fit run: 2026-11-21/r1/lab-vernier/007 (horizontal pair, T = 0.6, dt = 0.003, tracker and census). Constants are fit to this run with the exponent fixed at P = 2.5.
- Replicates, pre-registered before the results: 008 (vertical pair) and 009 (diagonal pair). Free fits give K_AC = -6.27 and -6.25, and K_CA = -14.81 and -14.79. Both are within 0.4% of the constants, inside the 5% pre-registered tolerance.
- Paper-model error (RMSE / L): 0.00512 (007), 0.00503 (008), 0.00542 (009). The bar is 3 x 0.006 = 0.018; the pre-registered bar is 0.015.
- Zero-force null error: 0.040 for each run. A model with no force fails the bar, so the runs discriminate.
- No census events in any of the three runs.

## Domain and limits

- Species A and C only; N = 2; initial separation 0.999 to 1.001; T <= 0.6 with no wall contact in these runs.
- The exponent 2.5 is held fixed. It is tested only at r = 1.0 here. Nothing is claimed for other separations.
- Predicted error 0.006 reflects the largest replicate error (0.0054), rounded up.

## Model

`model.py` integrates the pairwise central force with RK4 and specular walls. Only A-C and C-A pairs are accepted; other species pairs raise an error.
