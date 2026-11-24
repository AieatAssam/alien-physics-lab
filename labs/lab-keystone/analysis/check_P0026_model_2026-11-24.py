"""Judge-style RMSE/L of out/papers/P-0026/model.py against the N=16 run 2026-11-23/r3/lab-keystone/001 (tracker).
Also the in-domain check: min and max initial pairwise distance of that setup.
Run: python3 -I <this file> <repo_root>
"""
import json, math, sys, importlib.util
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
spec = importlib.util.spec_from_file_location('m', ROOT + '/out/papers/P-0026/model.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
req = json.load(open(ROOT + '/requests/2026-11-23/r3/lab-keystone/001.json'))
res = json.load(open(ROOT + '/results/2026-11-23/r3/lab-keystone/001.json'))
ps = req['setup']['particles']
d = [math.dist(ps[i]['pos'], ps[j]['pos']) for i in range(len(ps)) for j in range(i + 1, len(ps))]
print('N=%d initial pairwise distance min %.3f max %.3f' % (len(ps), min(d), max(d)))
pred = {round(s['t'], 9): s for s in m.predict(req['setup'])}
se, cnt = 0.0, 0
for s in res['samples']:
    p = pred[round(s['t'], 9)]
    for a, b in zip(s['particles'], p['particles']):
        se += (a['pos'][0] - b['pos'][0]) ** 2 + (a['pos'][1] - b['pos'][1]) ** 2
        cnt += 2
rmse = math.sqrt(se / cnt)
print('RMSE over all coords = %.4f ; RMSE/L = %.5f (claim predicted_error 0.007; replicate bar 0.021)' % (rmse, rmse / 10.0))
