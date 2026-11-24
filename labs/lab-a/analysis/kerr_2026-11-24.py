"""Statistical uncertainty on per-run K (two-body, P = 2.5, sigma 0.05): delta chi2 = 1 interval.
Usage: python3 -I kerr_2026-11-24.py <repo_root> <run numbers...>"""
import sys, importlib.util
ROOT = sys.argv[1]
nums = [int(x) for x in sys.argv[2:]]
sys.argv = [sys.argv[0], ROOT, "/dev/null"]
spec = importlib.util.spec_from_file_location("s2", "/home/runner/work/alien-physics-lab/alien-physics-lab/out/labs/lab-a/analysis/score_round2_2026-11-24.py")
s2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(s2)
import numpy as np
for n in nums:
    req, res, t, X, p0 = s2.load(n)
    K, c2 = s2.fit_K_pair(p0, t, X)
    c0 = s2.chi2_pair(K, p0, t, X)
    # local curvature of chi2 in K -> sigma_K = sqrt(2 / chi2''), chi2'' by finite difference
    h = 0.02 * K
    cp = s2.chi2_pair(K + h, p0, t, X); cm = s2.chi2_pair(K - h, p0, t, X)
    d2 = (cp - 2 * c0 + cm) / h ** 2
    sK = np.sqrt(2.0 / d2)
    print(f"{n:03d} sep {np.linalg.norm(p0[0]-p0[1]):.3f} T {req['setup']['duration']}: K {K:.3f} +/- {sK:.3f} ({100*sK/K:.2f}%)  chi2/dof {c2:.3f}")
