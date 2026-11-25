import json, math, sys
sys.path.insert(0, '/tmp/npdeps')
import numpy as np
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
sys.path.insert(0, ROOT + '/labs/lab-keystone/analysis')
import importlib.util
spec = importlib.util.spec_from_file_location('pre', ROOT + '/labs/lab-keystone/analysis/prereg_N4_square_2026-11-25.py')
pre = importlib.util.module_from_spec(spec); spec.loader.exec_module(pre)
L = 10.0
for rid in ['010', '011']:
    req = json.load(open(ROOT + '/requests/2026-11-25/r2/lab-keystone/%s.json' % rid))
    res = json.load(open(ROOT + '/results/2026-11-25/r2/lab-keystone/%s.json' % rid))
    pos0 = [p['pos'] for p in req['setup']['particles']]
    traj, minsep = pre.run(pos0)
    sq = cnt = 0
    for s in res['samples']:
        t = round(s['t'], 9)
        if t not in traj: continue
        for pt in s['particles']:
            q = traj[t][pt['id']]
            sq += (pt['pos'][0]-q[0])**2 + (pt['pos'][1]-q[1])**2; cnt += 2
    print(rid, 'RMSE/L (filed setup, same ids):', round(math.sqrt(sq/cnt)/L, 5), 'min sep T=1:', round(minsep[499],3), 'T=2:', round(minsep[-1],3))
