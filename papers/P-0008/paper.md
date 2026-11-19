# Pairwise additivity to four particles at rest, separations 3 to 5, species A, B, C (T <= 1) (lab-b, P-0008)

## Summary

Each particle's acceleration is the sum over its partners of K / r^2.5 toward each partner, with the P-0005 pair coefficients (K_A(B) 8.99, K_B(A) 12.34, K_A(C) -8.77, K_C(A) -21.25, K_B(B) 6.12, K_C(C) 12.36, K_B(C) -6.10, K_C(B) -10.59, K_A(A) 18.0; positive = attraction). Nothing else is added: no three-body and no four-body term.

Four particles at rest on a 3 x 4 rectangle (A, B, C, A) and three particles at rest in triangles with sides 3, 4 and 5 or side 3 equilateral (A, B, C) were run with the tracker for T = 1. The pairwise sum reproduces every particle at tracker-noise level. The residual rms per coordinate is 0.049 to 0.051 in all four runs, which is the noise level measured elsewhere in this season (about 0.05). No census events occurred.

Tests in this paper are at initial separations 3 to 5 only, and T <= 1. Within that window they show no detectable three-body or four-body term.

## Claims

- **c1 (four particles, rectangle).** 2026-11-19/r2/lab-b/001: rectangle 3 x 4, species A, B, C, A, at rest. Residual rms 0.050 to 0.051 per coordinate for all four particles. Largest mean residual 0.004 (particle A, x), about 4 naive standard errors of the mean and under a tenth of the tracker sigma. Domain: species A, B, C; pairwise separations 3 to 5; up to four particles; T <= 1.
- **c2 (three particles, triangles).** 2026-11-19/r1/lab-b/006 (sides A-B 3, B-C 4, A-C 5), 2026-11-19/r1/lab-b/007 (sides A-B 4, B-C 3, A-C 5), and 2026-11-18/r3/lab-b/006 (equilateral side 3). Residual rms 0.049 to 0.051 per coordinate; largest mean residual 0.005. Domain: species A, B, C; separations 3 to 5; three particles; T <= 1.

## Method

- Fits and checks were made with pure-python RK4, step 0.002, specular walls (not reached in these runs).
- Predictor: `out/papers/P-0008/model.py`. It takes setups of 2 to 4 particles at separations 3 to 5 and raises ValueError otherwise. Its coefficients are the P-0005 run means. Its output for the four runs above was checked by `out/labs/lab-b/analysis/check_p0008_model.py`.
- Coefficients at separations 3 and 4 (A-B, B-C, A-C) were measured by lab-b in round 2 and agree with the separation-5 values within about 2 to 3 percent. The predictor uses the separation-5 values at every separation in 3 to 5. This is the claim that the coefficients are flat over that interval.

## Limits

- **T <= 1 only.** A three-body term that is small compared with the tracker noise over one time unit cannot be seen here. The pair acceleration at separations 3 to 5 is about 0.16 to 0.6 (K / r^2.5 with K about 9). A three-body term at 5 percent of that gives an acceleration of about 0.01 to 0.03 and a displacement of about 0.005 to 0.015 by t = 1. That is well below the 0.05 per-sample noise and is only weakly probed through the mean residual. This paper does not bound a three-body term more tightly than that.
- **Four particles: one run.** c1 is one experiment. Its pairs sit at separations 3, 4 and 5, and its only A-A pair is at separation 4, so the A-A coefficient is tested at one separation here. The C-C pair does not appear in the four-body run; C-C is covered only by P-0005 and by the N = 3 runs in P-0007.
- **Mean residual of 0.004 in c1.** One particle shows a mean x residual of -0.0043 over 2000 correlated samples. This is larger than the naive standard error (about 0.001), so there may be a small systematic error of order 0.004 in the predicted motion. I do not claim it is a real effect. It is inside the stated predicted error of 0.07 per coordinate.
- **Separations near 3.** The A-A and A-C coefficients are flat from 3 to 5 in our fits. Below 3 the lab-b fits show A-B and A-C falling and A-A rising (see the lab-b notebook). The domain stops at 2.95.

## Self-criticism

The pre-registered falsifier for c1 (round-2 request 001) was a deviation greater than 0.05 per coordinate. The measured residual rms is 0.050. That threshold sits exactly at the tracker noise, so a test with that threshold could not have failed on a real effect smaller than the noise. I report the rms and the mean residuals rather than a pass or fail verdict on that threshold.

## Relation to other papers

Uses the P-0005 coefficients. Its N = 3 result extends the N = 3 test in P-0007 (lab-a, equilateral A, B, C side 5, T = 1.5) to other side lengths and to four particles. It does not change any claim in P-0005 or P-0007.
