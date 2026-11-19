"""Run out/papers/P-0007/model.py against every two-particle and N-body at-rest run in the repo that
falls in its domain, plus the round-1 runs of lab-keystone. Reports rms per coordinate per run.
In-sample: A-A runs (G nodes were fitted to them). Out-of-sample for mixed species at r=8 and N=3,4."""
import sys, math, importlib.util
sys.path.insert(0, '.')
from sim import load_any, observed, ROOT
spec = importlib.util.spec_from_file_location('p0007', ROOT + '/out/papers/P-0007/model.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

RUNS = [('2026-11-17','r3','lab-a',n) for n in range(1,9)] + [('2026-11-18','r2','lab-a',6),('2026-11-18','r2','lab-a',7),('2026-11-18','r1','lab-a',8),('2026-11-18','r1','lab-a',9)]
RUNS += [('2026-11-19','r1','lab-keystone',n) for n in range(5, 16)]
for date, rnd, lab, n in RUNS:
    r, rr = load_any(date, rnd, lab, n)
    s = r['setup']
    if rr.get('status') != 'ok':
        continue
    try:
        pred = M.predict(s)
    except ValueError as e:
        print('%s/%s/%s/%03d  outside domain: %s' % (date, rnd, lab, n, e))
        continue
    obs = observed(rr)
    pm = {round(x['t'], 9): x for x in pred}
    sq = cnt = 0; worst = 0.0
    for pid, series in obs.items():
        for t, (x, y) in series:
            p = pm[round(t, 9)]['particles'][pid]['pos']
            dx, dy = x - p[0], y - p[1]
            sq += dx * dx + dy * dy; cnt += 2; worst = max(worst, abs(dx), abs(dy))
    sp = ''.join(p['species'] for p in s['particles'])
    print('%s/%s/%s/%03d  %-5s T=%.1f  rms/coord %.4f  max|res| %.3f' % (date, rnd, lab, n, sp, s['duration'], math.sqrt(sq / cnt), worst))
