import json, sys, math
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/tools')
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/labs/lab-keystone/analysis')
from domain import in_domain
import review_error as re_
ROOT = re_.ROOT
PAPERS = {'P-0012': [4,5,6,7,8,9], 'P-0013': [7,8,9,4,5,6], 'P-0015': [1,2,3,4,5,6,7,8,9]}
def claim(pid):
    return json.load(open('%s/papers/%s/claim.json' % (ROOT, pid)))
for pid in ['P-0012', 'P-0013', 'P-0015']:
    c = claim(pid)['claims'][0]
    dom = c['domain']; pe = c['predicted_error']; bar = 3 * pe
    print('==', pid, 'domain', dom, 'pe', pe, 'bar', round(bar, 4))
    model = re_.load_model(pid)
    for n in range(1, 10):
        rid = '2026-11-21/r2/lab-keystone/%03d' % n
        req = json.load(open('%s/requests/2026-11-21/r2/lab-keystone/%03d.json' % (ROOT, n)))
        indom = in_domain(dom, req['setup'])
        try:
            rmse, err, sp, N, dmin, dmax, T, ev = re_.run_error(model, rid)
            print(' ', rid, 'indom=%s' % indom, 'sp=%s N=%d sep=[%.5f,%.5f] T=%.2f rmse=%.5f err=%.5f ev=%d' % (sp, N, dmin, dmax, T, rmse, err, ev), 'OK' if err <= bar else 'FAIL')
        except Exception as e:
            print(' ', rid, 'indom=%s' % indom, 'ERR', type(e).__name__, str(e)[:100])
