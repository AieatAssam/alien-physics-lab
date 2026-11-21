"""Diagnose P-0014 model error on my run 2026-11-19/r1/lab-vernier/007 (A-A, sep 3, T=2).
Reports measured min separation, and model error restricted to time windows.
Run: python3 -I diag_p0014_run007_2026-11-21.py
"""
import importlib.util, json, math

R = '/home/runner/work/alien-physics-lab/alien-physics-lab'
spec = importlib.util.spec_from_file_location('m', R + '/papers/P-0014/model.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
req = json.load(open(R + '/requests/2026-11-19/r1/lab-vernier/007.json'))
res = json.load(open(R + '/results/2026-11-19/r1/lab-vernier/007.json'))
pred = {round(s['t'], 9): s for s in m.predict(req['setup'])}

rows = []
for s in res['samples']:
    t = round(s['t'], 9)
    sep = math.dist(s['particles'][0]['pos'], s['particles'][1]['pos'])
    q = pred[t]['particles']
    se = sum((s['particles'][i]['pos'][k] - q[i]['pos'][k]) ** 2 for i in range(2) for k in range(2))
    pdist = math.dist(q[0]['pos'], q[1]['pos'])
    rows.append((t, sep, pdist, se))

tmin = min(rows, key=lambda r: r[1])
print('measured min sep %.3f at t=%.2f' % (tmin[1], tmin[0]))
for T in (0.5, 1.0, 1.5, 2.0):
    sub = [r for r in rows if r[0] <= T + 1e-9]
    rmse = math.sqrt(sum(r[3] for r in sub) / (4 * len(sub))) / 10
    print('model RMSE/L over t<=%.1f: %.5f' % (T, rmse))
for r in rows[::20]:
    print('t=%.2f meas_sep=%.3f model_sep=%.3f' % (r[0], r[1], r[2]))
