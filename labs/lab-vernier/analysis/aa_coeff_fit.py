"""Fit the A-A coefficient K (P = 2.5 fixed) to lab-vernier's two-A pair runs at separation 4 and 6 (T=2).
Reports the fitted K, the rms residual per coordinate at the fitted K, and the rms at K = 17.7 (P-0003 claim)
and K = 18.0 (P-0005 / P-0008 coefficient). Run with python3 -I from this folder."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit_tools as ft

R = '/home/runner/work/alien-physics-lab/alien-physics-lab'
RUNS = ['2026-11-20/r1/lab-vernier/002', '2026-11-20/r1/lab-vernier/003']

for rid in RUNS:
    req = json.load(open(os.path.join(R, 'requests', rid + '.json')))
    res = json.load(open(os.path.join(R, 'results', rid + '.json')))
    sep = math.dist(req['setup']['particles'][0]['pos'], req['setup']['particles'][1]['pos'])
    coup, mse = ft.fit_couplings(req['setup'], res, {('A', 'A'): 18.0}, [('A', 'A')],
                                 {('A', 'A'): (5.0, 40.0)}, P=2.5, sweeps=3)
    line = '%s r0=%.1f  fitted K_A(A)=%.3f  rms/coord=%.4f' % (rid, sep, coup[('A', 'A')], math.sqrt(mse))
    for K in (17.7, 18.0):
        m = ft.sse_window(req['setup'], res, {('A', 'A'): K}, 2.5, None)
        line += '  | K=%.1f rms/coord=%.4f' % (K, math.sqrt(m))
    print(line)
