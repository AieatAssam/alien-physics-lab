"""Score round-2 pre-registered runs (lab-keystone, 2026-11-28) against prereg_2026-11-28_r2.json.

Uses the chi2 scan in scale_fit_2026_11_28.fit on a wide grid (no quadratic across contact).
Run from any directory:  python3 -I score_r2_2026_11_28.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scale_fit_2026_11_28 as S  # noqa: E402

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
GRID = [0.94, 0.96, 0.98, 1.00, 1.02, 1.04, 1.06, 1.08, 1.10]
RUNS = [
    ('2026-11-28/r2/lab-keystone/001', 'A-A r0 3.5 horizontal, T 1 (offset replicate; decision band [1.02, 1.08])'),
    ('2026-11-28/r2/lab-keystone/002', 'A-A r0 4.5 horizontal, T 1 (flat-clamp vs P-0027 note; falsifier |s-1| > 0.05)'),
]

if __name__ == '__main__':
    for rid, label in RUNS:
        day, rnd, lab, nnn = rid.split('/')
        req_p = '%s/requests/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, nnn)
        res_p = '%s/results/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, nnn)
        out = S.fit(req_p, res_p, GRID)
        print(rid, label)
        print('  s = %.4f +/- %.4f  chi2/dof = %.2f' % (out['s_hat'], out['sigma_s'], out['chi2_per_dof']))
        print('  chi2/n:', ' '.join('%.2f:%.3f' % (g, v) for g, v in out['grid_chi2']))
