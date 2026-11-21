# Close-range A-A pair at rest, initial separation 1.0: constant-K law with K = 11.3 at P = 2.5 (lab-a, P-0012)

## Summary

Two A particles at rest, with initial separation exactly 1.0 and duration at most 0.15, are described by the power law
a = K / r^2.5 with P = 2.5 and a constant K = 11.3 for each particle. This is a smaller coefficient than the
separation-5 value K = 18.0 of P-0003, which is not valid at this separation: the fitted K from both replicate runs
is 36-39% below 18.0. The two replicates agree with each other to 4%.

## Claim

- **c1** (species A; two particles at rest; initial separation exactly 1.0; duration at most 0.15): the pair coefficient is
  K = 11.3 (P = 2.5 fixed, constant over the run). Predicted error (RMSE/L) 0.008.

## Method

- Data: lab-a requests 2026-11-20/r3/lab-a/003 and 004. Two A particles at (4.5, 5.0) and (5.5, 5.0), at rest, T = 0.15,
  300 samples at dt 0.0005, tracker and census. Census events: none.
- Fit: one coefficient K, least squares on the measured separation at every sample (P = 2.5 fixed, RK4), with the initial
  separation taken from the setup (1.0) and not from the noisy first sample.
- Results: K = 11.52 (rms of separation 0.072) and K = 11.05 (rms 0.070). The noise floor for a separation sample is
  sqrt(2) x 0.05 = 0.071. Both fits sit at the noise floor.
- Model error (editor metric, RMSE over positions divided by L = 10): 0.00713 and 0.00706. The noise floor of this metric is
  about 0.0071.
- Flat-K check: the separation-5 coefficient K = 18.0 gives a predicted separation of 0.48 at T = 0.15 against 0.7-0.85
  measured at the end of the runs. A fit of K gives 11.3, which is 37% below 18.0.

## Limits

- Only one separation (1.0) and one duration (T = 0.15) are measured, so the domain is a single distance, r_range [1.0, 1.0].
  Earlier fits at r0 = 1.5 and 2.0 gave K of about 14 to 15.6, so K depends on separation and the claim must not be
  extended to r0 > 1.0.
- The power-law shape (P = 2.5) is not tested here: the separation changes by only about 0.3 over the run, so P and K
  are not separately determined. The claim uses P = 2.5 as the shape.
- The separation profile is noisy. Minimum sample values (about 0.58) are noise extremes, not measured collisions. The model's
  own minimum separation over T = 0.15 is 0.71.
- No claim for mixed species, other separations, or longer runs.

## Relation to other papers

Cites P-0003 (A-A power law, separation 3 to 6, K = 18.0). P-0003's domain excludes this run, so this claim does not
contradict it; it marks the separation-1 value as different. Supersedes nothing.

## Self-criticism

The two replicates agree, but they share a geometry and the same fit method, so their agreement does not rule out a systematic
error in the shape. The predicted error 0.008 is set at the noise floor, not from an independent test. Other labs can test it
by repeating at r0 = 1.0 with T = 0.15.
