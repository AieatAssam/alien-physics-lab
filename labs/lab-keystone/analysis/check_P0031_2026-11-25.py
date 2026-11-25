"""Check the P-0031 predictor against its evidence runs 2026-11-25/r2/lab-keystone/010-011 and its domain edges."""
import importlib.util, json, math, sys
sys.path.insert(0, '/tmp/npdeps')
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
spec = importlib.util.spec_from_file_location('p31', ROOT + '/out/papers/P-0031/model.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
L = 10.0
for rid in ['010', '011']:
    req = json.load(open(ROOT + '/requests/2026-11-25/r2/lab-keystone/%s.json' % rid))
    res = json.load(open(ROOT + '/results/2026-11-25/r2/lab-keystone/%s.json' % rid))
    pred = m.predict(req['setup'])
    pm = {round(s['t'], 9): s for s in pred}
    sq = cnt = 0
    for s in res['samples']:
        t = round(s['t'], 9)
        if t not in pm: continue
        mp = {p['id']: p['pos'] for p in pm[t]['particles']}
        for p in s['particles']:
            q = mp[p['id']]; sq += (p['pos'][0]-q[0])**2 + (p['pos'][1]-q[1])**2; cnt += 2
    print(rid, 'judged RMSE/L = %.5f' % (math.sqrt(sq/cnt)/L))
# domain edges: should accept / refuse
def setup(pos, dur=2.0):
    return {'particles': [{'species': 'A', 'pos': p, 'vel': [0.0, 0.0]} for p in pos], 'duration': dur, 'sample_dt': 0.01}
sq5 = [[2.5, 2.5], [7.5, 2.5], [7.5, 7.5], [2.5, 7.5]]
for label, s in [('square side 5, T=2 (accept)', setup(sq5)),
                 ('square side 5, T=2.5 (refuse)', setup(sq5, 2.5)),
                 ('rectangle 5x6 pairs to 7.81 (refuse, outside r_range)', setup([[2.5, 2.0], [7.5, 2.0], [7.5, 8.0], [2.5, 8.0]])),
                 ('three particles (refuse)', setup(sq5[:3]))]:
    try:
        m.predict(s); print(label, '-> accepted')
    except ValueError as e:
        print(label, '-> ValueError:', str(e)[:80])
