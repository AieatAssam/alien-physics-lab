"""Diagnostic for research 2026-11-23/r1/lab-keystone/001-006. Per-run best (G, P) on the 1D relative law
q'' = -G / q**P (symmetric pair at rest), plus time profile at r0 = 4 vs the P-0024 law. Run: python3 -I <file> <root>"""
import sys, math
sys.argv = sys.argv[:2]
import importlib.util
spec = importlib.util.spec_from_file_location('ext', sys.argv[0].replace('extension_diag_2026-11-23.py', 'extension_r0_4_6_2026-11-23.py'))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
ROOT = sys.argv[1]
E.ROOT = ROOT
data = {n: E.load(n) for n in E.RUNS}

def rms_for(n, G, P, tmax=None):
    r0, T, dt, pts, _ = data[n]
    if tmax is not None:
        pts = [p for p in pts if p[0] <= tmax + 1e-9]
    ms = E.resid(r0, pts, G, P, dt, T if tmax is None else tmax)
    return math.sqrt(sum(x * x for x in ms) / len(ms))

print('per-run best (G,P) grid, P in 1.8..3.2 step 0.2, G in 5..60 step 1 (cut at t <= 1.0 for r0=4 to avoid collapse)')
for n in E.RUNS:
    r0 = data[n][0]
    tmax = 1.0 if r0 < 4.5 else 1.0
    best = None
    for P in [1.8, 2.1, 2.5, 2.8, 3.2]:
        for G in range(5, 61, 2):
            r = rms_for(n, float(G), P, tmax)
            if best is None or r < best[0]:
                best = (r, G, P)
    print('%s r0=%.1f best rms=%.4f at G=%d P=%.1f | M1(23.63,2.099) rms(t<=1)=%.4f' % (n, r0, best[0], best[1], best[2], rms_for(n, 23.63, 2.099, tmax)))

print('r0=4 run 001 time profile: t, measured, M1(P=2.099,G=23.63), P=2.5 G=35')
r0, T, dt, pts, _ = data['001']
m1 = dict(E.rhs_series(r0, 23.63, 2.099, 2.0, dt))
m2 = dict(E.rhs_series(r0, 35.0, 2.5, 2.0, dt))
for t, d in pts[::10]:
    k = round(t, 9)
    print('%.2f %.3f %.3f %.3f' % (t, d, m1[k], m2[k]))
