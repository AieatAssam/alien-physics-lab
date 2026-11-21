import json, math, sys, importlib.util
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/labs/lab-keystone/analysis')
import review_error as re_
ROOT = re_.ROOT
def load(pid):
    spec = importlib.util.spec_from_file_location('mm_' + pid.replace('-', '_') + str(id(object())), '%s/papers/%s/model.py' % (ROOT, pid))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
# P-0012: scale K
for f in [0.9, 0.95, 1.0, 1.05, 1.1]:
    m = load('P-0012'); m.K = 11.3 * f
    errs = [re_.run_error(m, '2026-11-21/r2/lab-keystone/%03d' % n)[1] for n in (4, 5, 6)]
    print('P-0012 K x%.2f (K=%.2f): errs %s' % (f, m.K, ' '.join('%.5f' % e for e in errs)))
# P-0015: scale both constants
for f in [0.9, 0.95, 1.0, 1.05, 1.1]:
    m = load('P-0015')
    for k in list(m.COUP): m.COUP[k] = m.COUP[k] * f
    errs = [re_.run_error(m, '2026-11-21/r2/lab-keystone/%03d' % n)[1] for n in (1, 2, 3)]
    print('P-0015 K x%.2f: errs %s' % (f, ' '.join('%.5f' % e for e in errs)))
# P-0013 run 007 truncated windows
m = load('P-0013')
req = json.load(open(ROOT + '/requests/2026-11-21/r2/lab-keystone/007.json'))
res = json.load(open(ROOT + '/results/2026-11-21/r2/lab-keystone/007.json'))
pred = m.predict(req['setup'])
for tmax in [0.2, 0.25, 0.3, 0.35, 0.4]:
    sq = cnt = 0
    for s, p in zip(res['samples'], pred):
        if s['t'] > tmax + 1e-9: break
        for a, b in zip(s['particles'], p['particles']):
            sq += (a['pos'][0]-b['pos'][0])**2 + (a['pos'][1]-b['pos'][1])**2; cnt += 2
    print('P-0013 run 007 window t<=%.2f: err=%.5f  bar=0.03' % (tmax, math.sqrt(sq/cnt)/10))
