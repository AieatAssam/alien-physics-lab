"""Independent check of the separation-5 pair runs cited for P-0004 (lab-b runs
2026-11-18/r3/lab-b/012-014). Same two-particle r^-2.5 fit as round2_check.py."""
import json, math, sys
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/out/labs/lab-keystone/analysis')
from round2_check import observed, fit, ROOT

GUESS = {'AB': (9.0, 12.3), 'AC': (-8.6, -21.4), 'BC': (-6.1, -10.6)}
for n in [12, 13, 14]:
    req = json.load(open('%s/requests/2026-11-18/r3/lab-b/%03d.json' % (ROOT, n)))
    res = json.load(open('%s/results/2026-11-18/r3/lab-b/%03d.json' % (ROOT, n)))
    parts = req['setup']['particles']
    sp = ''.join(p['species'] for p in parts)
    init = [p['pos'] for p in parts]
    T, dt = req['setup']['duration'], req['setup']['sample_dt']
    if res.get('status') != 'ok':
        print(n, res.get('status')); continue
    obs = observed(res)
    g = GUESS[sp] if sp in GUESS else GUESS[sp[::-1]]
    if sp not in GUESS: g = (g[1], g[0])
    K0, K1, rms = fit(init, obs, T, 0.01, g[0], g[1])  # sample_dt 0.001 is finer than integrator step; use 0.01 grid
    print('lab-b %03d %s r=%.2f T=%.1f  K_on_0=%.3f K_on_1=%.3f rms/coord=%.4f' % (n, sp, math.dist(init[0], init[1]), T, K0, K1, rms))
