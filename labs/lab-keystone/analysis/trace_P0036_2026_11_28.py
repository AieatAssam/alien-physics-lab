import sys, json, math
sys.path.insert(0, '/tmp/npdeps')
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/labs/lab-keystone/analysis')
import review_error as R
import numpy as np
m = R.load_model('P-0036')
for n in ['006', '007']:
    rid = '2026-11-28/r1/lab-keystone/' + n
    req = json.load(open('requests/2026-11-28/r1/lab-keystone/%s.json' % n))
    res = json.load(open('results/2026-11-28/r1/lab-keystone/%s.json' % n))
    print(n, json.dumps(req['setup']))
    pred = {round(s['t'], 9): s for s in m.predict(req['setup'])}
    print(' t   obs_sep  model_sep  obs_A(x,y)        model_A        obs_B(x,y)  model_B   |dpos|')
    for s in res['samples']:
        t = round(s['t'], 9)
        if round(t * 100) % 10 != 0: continue
        o = s['particles']; p = pred[t]['particles']
        od = math.dist(o[0]['pos'], o[1]['pos']); md = math.dist(p[0]['pos'], p[1]['pos'])
        err = math.hypot(*[o[i]['pos'][k] - p[i]['pos'][k] for i in range(2) for k in range(2)][:0] or [0]) 
        dd = max(math.dist(o[i]['pos'], p[i]['pos']) for i in range(2))
        print('%.2f  %6.3f  %8.3f   (%5.2f,%5.2f)  (%6.2f,%6.2f)  (%5.2f,%5.2f) (%6.2f,%6.2f)  %7.3f' % (t, od, md, o[0]['pos'][0], o[0]['pos'][1], p[0]['pos'][0], p[0]['pos'][1], o[1]['pos'][0], o[1]['pos'][1], p[1]['pos'][0], p[1]['pos'][1], dd))
