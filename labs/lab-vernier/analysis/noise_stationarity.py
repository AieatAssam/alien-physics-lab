"""Segment-sd stationarity test for at-rest tracker residuals (lab-vernier).

For each at-rest run, split residuals (about the run mean) into 4 contiguous segments
and test whether segment sds agree: chi-square against the pooled sd with
SE(sd) = sigma / sqrt(2 (n-1)). Also reports the segment-sd spread (max-min)/mean.
"""
import sys
sys.path.insert(0, ".")
import numpy as np
from scipy import stats  # noqa: F401  (only for p-values, if available)
from load_results import load

R = "/home/runner/work/alien-physics-lab/alien-physics-lab/results/2026-11-19/r1/lab-vernier/"
rows = []
for n in ["001", "002", "003", "004", "006"]:
    d = load(R + n + ".json")
    p = d["pos"][0]
    r = p - p.mean(axis=0)
    N = len(r)
    k = 4
    seg = np.array_split(np.arange(N), k)
    for c, name in enumerate(["x", "y"]):
        sds = np.array([r[s, c].std(ddof=1) for s in seg])
        n_seg = len(seg[0])
        sigma = r[:, c].std(ddof=1)
        se = sigma / np.sqrt(2 * (n_seg - 1))
        chi2 = float(np.sum(((sds - sigma) / se) ** 2))
        p_val = float(stats.chi2.sf(chi2, k - 1))
        spread = (sds.max() - sds.min()) / sds.mean()
        rows.append((n, name, np.round(sds, 4).tolist(), round(spread, 3), round(chi2, 2), round(p_val, 4)))
        print(f"{n} {name}: seg sds {np.round(sds,4).tolist()} spread {spread:.3f} chi2({k-1}) {chi2:.2f} p {p_val:.4f}")
