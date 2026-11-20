"""Score the P-0009 candidate model on lab-keystone far-field runs with the editor's metric
(RMSE of predicted vs tracker positions / 10). Usage: python3 -I eval_p0009.py"""
import importlib.util, sys
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/out/labs/lab-keystone/analysis')
from review_error import run_error, ROOT
spec = importlib.util.spec_from_file_location('m_p0009', ROOT + '/out/papers/P-0009/model.py')
model = importlib.util.module_from_spec(spec); spec.loader.exec_module(model)
RUNS = ['2026-11-19/r1/lab-keystone/%03d' % n for n in (3, 4, 13, 15)] + \
       ['2026-11-19/r2/lab-keystone/%03d' % n for n in (1, 2, 3, 4, 5)] + \
       ['2026-11-19/r3/lab-keystone/%03d' % n for n in (1, 4, 5, 7, 8)]
worst = 0
for rid in RUNS:
    rmse, err, sp, n, dmin, dmax, T, ev = run_error(model, rid)
    worst = max(worst, err)
    print('%s %s sep=%.1f T=%.0f rmse=%.4f error=%.5f' % (rid[11:], sp, dmin, T, rmse, err))
print('worst error %.5f' % worst)
