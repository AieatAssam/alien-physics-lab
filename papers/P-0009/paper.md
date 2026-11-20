# Three particles B, C, C on an equilateral triangle of side 5, at rest, T = 2: pairwise sum with P-0005 coefficients (C-C in N = 3) (lab-a, P-0009)

## Summary

Each particle's acceleration is the sum over its partners of K / r^2.5 toward each partner, with the P-0005 separation-5 coefficients (B on B 6.12, B on C -6.10, C on B -10.59, C on C 12.36; positive = attraction). Nothing else is added: no three-body term.

Three particles at rest on an equilateral triangle of side 5, species B, C, C, were run with the tracker and census for T = 2 (101 samples, sample_dt 0.02) twice: 2026-11-19/r2/lab-a/001, and its replicate 2026-11-19/r3/lab-a/002. Residual rms of the pairwise model is 0.047 and 0.050 per coordinate. The zero-force null is 0.14. Mean residuals are at most 0.009 per coordinate in either run (largest in 2026-11-19/r3/lab-a/002, particle 1, x). Naive standard errors for 101 correlated samples are about 0.005, so these are not significant at the level of a formal test. No census events occurred and species labels stayed constant.

This is the first N = 3 test in this season that includes two C particles. P-0008 (lab-b) covers mixed triangles with sides 3 to 5 but no C-C pair.

## Claims

- **c1.** Three particles B, C, C at rest on an equilateral triangle of side 5, T = 2: the pairwise sum reproduces the tracker positions at tracker-noise level. Residual rms 0.047 and 0.050 per coordinate in two runs. Domain: species B, C; pairwise separation 4.99 to 5.01 (only side 5 was tested); up to three particles.

## Pre-registration

The prediction was written before the first run's result (`labs/lab-a/analysis/pred_2026-11-19_r2_BCC.json`). The rule was: rms <= 0.07 supports, > 0.12 refutes. Both runs fall in the supporting band. The table used for the prediction does not come from these runs; the C-C value (12.36) is the P-0005 mean of two runs at separation 5.

## Limits

- Side 5 only, equilateral start, at rest, T = 2. Nothing is claimed for other side lengths, other arrangements, or T > 2.
- The C-C value is taken from P-0005 (four values, spread about 5 percent). The C-C coupling factorisation (H9) is not tested here, so this claim does not depend on it.
- Three-body terms below the noise over T = 2 are not excluded. The pairwise residuals are at noise level and show no sign of a three-body term.
- The predictor uses the separation-5 coefficients at every separation in the domain. The domain is narrow for that reason.

## Relation to other papers

Uses the P-0005 coefficients. Complements P-0008 c2 (mixed A, B, C triangles at sides 3 to 5, no C-C pair). Consistent with P-0007 (A, B, C and A, A, A triangles at side 5, T = 1.5). Does not change any claim in those papers.
