import sys
sys.path.insert(0, '/tmp/npdeps')
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/labs/lab-keystone/analysis')
import review_error as R
m = R.load_model('P-0036')
ids = ['2026-11-28/r1/lab-keystone/%03d' % i for i in range(3, 11)]
for rid in ids:
    try:
        rmse, err, sp, n, dmin, dmax, T, ev = R.run_error(m, rid)
        print(rid, sp, 'N=%d' % n, 'sep=[%.3f,%.3f]' % (dmin, dmax), 'T=%.1f' % T, 'rmse=%.4f' % rmse, 'err=%.5f' % err, 'events=%d' % ev)
    except Exception as e:
        print(rid, 'ERROR', type(e).__name__, str(e)[:200])
