"""Fit two-particle couplings (r^-2.5 shape, K0 and K1 free) for lab-keystone r3 runs
of 2026-11-19 and compare with the pre-registered predictions in predictions_round3.json.
Reuses sim/fit/observed from round2_check.py (pure python). Usage: python3 -I round3_fit.py"""
import json, math, sys
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/out/labs/lab-keystone/analysis')
from round2_check import sim, observed, fit, ROOT

DATE_RND = '2026-11-19/r3/lab-keystone'
GUESS = {1: (13.71, 13.71), 3: (12.36, 12.36), 4: (9.55, 9.55), 5: (-7.54, -18.28), 7: (5.61, 5.61), 8: (8.24, 11.30)}
for n in [1, 3, 4, 5, 7, 8]:
    req = json.load(open('%s/requests/%s/%03d.json' % (ROOT, DATE_RND, n)))
    res = json.load(open('%s/results/%s/%03d.json' % (ROOT, DATE_RND, n)))
    init = [p['pos'] for p in req['setup']['particles']]
    sp = ''.join(p['species'] for p in req['setup']['particles'])
    T = req['setup']['duration']; dt = req['setup']['sample_dt']
    obs = observed(res)
    sep = math.dist(init[0], init[1])
    g = GUESS[n]
    K0, K1, rms = fit(init, obs, T, dt, g[0], g[1])
    print('r3/%03d %s r=%.2f T=%.1f  K_on_0=%.3f K_on_1=%.3f rms/coord=%.4f  guess=%s events=%d' % (
        n, sp, sep, T, K0, K1, rms, g, len(res['events'])))
