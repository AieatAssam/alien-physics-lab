"""Judged-metric sensitivity of P-0031 on runs 010, 011: K scale s in {0.95, 1, 1.05} and zero-force null."""
import importlib.util, json, math, sys
sys.path.insert(0, '/tmp/npdeps')
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
spec = importlib.util.spec_from_file_location('p31', ROOT + '/out/papers/P-0031/model.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base = list(m.K_NODES)
def judged(pred, res):
    pm = {round(s['t'], 9): s for s in pred}
    sq = cnt = 0
    for s in res['samples']:
        t = round(s['t'], 9)
        if t not in pm: continue
        mp = {p['id']: p['pos'] for p in pm[t]['particles']}
        for p in s['particles']:
            q = mp[p['id']]; sq += (p['pos'][0]-q[0])**2 + (p['pos'][1]-q[1])**2; cnt += 2
    return math.sqrt(sq/cnt)/10.0
for rid in ['010', '011']:
    req = json.load(open(ROOT + '/requests/2026-11-25/r2/lab-keystone/%s.json' % rid))
    res = json.load(open(ROOT + '/results/2026-11-25/r2/lab-keystone/%s.json' % rid))
    out = []
    for s in [0.95, 1.0, 1.05, 0.0]:
        m.K_NODES = [k * s for k in base]
        out.append('s=%.2f %.5f' % (s, judged(m.predict(req['setup']), res)))
    m.K_NODES = base
    print(rid, '  '.join(out))
