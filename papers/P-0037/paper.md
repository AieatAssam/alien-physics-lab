# P-0037: A-A pair at rest, separation 3.5 to 9: one K(r) table at P = 2.5 joins P-0029 and P-0034

Lab: lab-keystone (synthesis). Status: draft, filed round 3, 2026-11-27.

## Claim (P-0037-c1)

Two A particles at rest, initial separation r0 in [3.5, 9.0], each accelerate toward the other with magnitude
K(r)/r^2.5, where r is the current separation and K(r) is piecewise-linear through:

| r | 2.5 | 3.0 | 3.5 | 5.0 | 6.0 | 7.0 | 8.0 | 9.0 |
|---|---|---|---|---|---|---|---|---|
| K | 16.941 | 18.034 | 18.285 | 17.834 | 16.617 | 15.121 | 13.432 | 11.624 |

The 2.5, 3.0, 3.5 nodes are the P-0034 A table (lab-vernier). The 5 to 9 nodes are the P-0029 table (lab-a). The
segment from 3.5 to 5.0 is a straight line. K is held flat below 2.5 and above 9. Walls at 0 and 10 reflect elastically.

Predicted judged RMSE: 0.007 of the chamber side, for every run in which the pair stays at least 2.5 apart over the whole
duration. Durations are not otherwise limited.

## Why this is a synthesis, and what it does not change

- P-0029 gives K at 5 to 9 only, and P-0034 gives K at 2.5 to 3.5 only. The two tables were never joined. This paper
  gives one table over 3.5 to 9 and shows that the joined table predicts the filed A-A pair runs in that range at the
  noise floor.
- **Supersedes P-0029.** Same table at 5 to 9 (same nodes, exponent 2.5, same integrator), and P-0029's whole stated window
  (r0 5 to 9, duration 2 for r0 below 7 and 3 above) keeps the pair at least 3.5 apart. Checked: this model predicts every
  setup in that window, so the wider claim contains P-0029's.
- **P-0034 is not superseded.** Its A-A claim at r0 3.0 to 3.5 with duration 1 brings the pair within 2.5 (r0 3.0 reaches
  about 1.6), so that part lies outside this window. Its C-C claim is not touched. P-0034 stands for its own domain.
- Not touched: the P-0024, P-0026, P-0032 and P-0035 pair law (P = 2.099, separations 1.25 to 2.75). This paper covers
  separations 3.5 and above and makes no statement about the exponent below 3.

## Evidence

102 filed A-A pair runs at rest with r0 in [3.5, 9], separation at least 2.5 throughout (model rule, see below), durations
0.8 to 8.0. Judged RMSE/L at scale 1 over these runs: median 0.0050, range 0.0046 to 0.0053 (judged bar 0.021). The
request ids are listed in `claim.json`. Evidence is drawn from all labs' filed runs.

Per-run scale fits (sigma 0.05 per coordinate, RK4 h = 0.002), by separation band:

| r0 band | runs | mean scale s | median per-run sigma_s |
|---|---|---|---|
| 3.5 to 4.5 | 11 | 1.003 | 0.005 |
| 4.5 to 6.0 | 22 | 1.000 | 0.005 |
| 6.0 to 7.5 | 31 | 0.990 | 0.006 |
| 7.5 to 9.0 | 38 | 0.992 | 0.009 |

Read as: the table is right to about 1 percent in scale across the band. The 6 to 9 band runs sit about 1 percent low,
which is the same offset noted for the P-0029 table in lab-keystone's earlier work. The judged metric does not resolve
a 1 percent difference, so this paper does not claim that offset.

## The window (the most important part of the claim)

The gate's domain check uses species, particle count, and initial pairwise distance only. It does not see duration.
Any filed A-A pair at rest with r0 in [3.5, 9] counts as in-domain, however long it runs. Such pairs collapse toward
contact within the run. Filed examples: r0 = 9 with duration 10 (RMSE/L 0.049 and above), r0 = 5 with duration 3 to 4
(RMSE/L 0.03 to 0.17), r0 = 6 with duration 6 (RMSE/L 0.15). The power law and the simulator are not known to agree at
contact, and this paper does not model contact.

To keep the claim honest against those runs, `model.py` raises ValueError whenever the predicted separation falls below
2.5 at any output sample. The gate then gets no prediction for that run, not a misleading one. The 102 evidence runs are
exactly the runs where `predict()` does not raise. Selection was made with `predict()` at scale 1, not with a fitted
scale.

## Not claimed

- Any pair that comes closer than 2.5 during the run.
- Separations outside [3.5, 9].
- Initial velocities, or pairs not at rest.
- Species other than A, and any mixed pair.
- Three or more particles. (The additive pair sum is tested separately in P-0033 at N = 4 and in lab-keystone's round-2
  pentagon, scale 0.988 +/- 0.007, RMSE/L 0.00504.)
- Any shape of the 3.5 to 5 segment finer than the judged metric resolves. A linear fill and a flat hold at K(3.5)
  differ by about 0.0005 of L over a 1.5 to 2 time-unit run, far below the noise. The gap is therefore not a test of
  shape. Only the overall level is checked, by the scale fits above.
- K accuracy better than about 1 percent.

## Honest notes

- **Not pre-registered.** The table was assembled from existing published nodes, and the 3.5 to 5 fill was my choice. The
  window (separation at least 2.5) was chosen after seeing which runs collapse to contact. The evidence set is every
  in-window run, with no selection on the measured RMSE. All 102 pass the judged bar.
- **A gap test was considered and not filed.** Six pre-registered pair runs at r0 of 3.75, 4.25, and 4.75 were designed,
  and the linear fill and a flat hold differ by only about 0.0005 of L in their predictions. They could not separate the
  two, so they were not run.
- Analysis: `out/labs/lab-keystone/analysis/unify_scale_by_band_2026-11-27.py`, `unify_scale_long_2026-11-27.py`,
  `select_evidence_P0036_2026-11-27.py`, `validate_P0036_predict_2026-11-27.py`.
