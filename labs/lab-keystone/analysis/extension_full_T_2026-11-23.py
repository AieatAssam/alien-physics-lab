"""Full-T fits (t <= 2 for r0 = 5, 6; t <= 1.8 for r0 = 4 to stay clear of the collision near t = 1.95).
Per-run best (G, P) on the 1D law q'' = -G/q^P, and the M1 residual profile for run 005. Run: python3 -I <file> <root>"""
import sys, math, importlib.util
ROOT = sys.argv[1]
spec = importlib.util.spec_from_file_location('ext', ROOT + '/out/labs/lab-keystone/analysis/extension_r0_4_6_2026-11-23.py')
E = importlib.util.module_from_spec(spec); sys.argv = ['x', ROOT]; spec.loader.exec_module(E)
data = {n: E.load(n) for n in E.RUNS}

def rms(n, G, P, tmax):
    r0, T, dt, pts, _ = data[n]
    pts = [p for p in pts if p[0] <= tmax + 1e-9]
    ms = E.resid(r0, pts, G, P, dt, tmax)
    return math.sqrt(sum(x * x for x in ms) / len(ms))

for n in E.RUNS:
    r0 = data[n][0]
    tmax = 1.8 if r0 < 4.5 else 2.0
    best = None
    for P in [1.8, 2.0, 2.1, 2.3, 2.5, 2.8]:
        for G in range(5, 61, 1):
            r = rms(n, float(G), P, tmax)
            if best is None or r < best[0]:
                best = (r, G, P)
    print('%s r0=%.1f tmax=%.1f best rms=%.4f G=%d P=%.1f | M1 rms=%.4f' % (n, r0, tmax, best[0], best[1], best[2], rms(n, 23.63, 2.099, tmax)))

r0, T, dt, pts, _ = data['005']
m1 = dict(E.rhs_series(r0, 23.63, 2.099, 2.0, dt))
print('run 005 (r0=6) t, measured sep, M1 sep, residual')
for t, d in pts[::20]:
    print('%.2f %.3f %.3f %+.3f' % (t, d, m1[round(t, 9)], d - m1[round(t, 9)]))
