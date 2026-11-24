"""Diagnostics for research 2026-11-23/r3/lab-keystone/002-007: binned residual vs time, and best-fit G at P = 2.099.
Run: python3 -I <this file> <repo_root>
"""
import json, math, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
RUNS = ['002', '003', '004', '005', '006', '007']
P = 2.099


def traj(r0, T, dt, gg, h=1e-3):
    out = {0.0: r0}; q, v, t = r0, 0.0, 0.0
    def f(qq, vv):
        return (vv, 0.0) if qq <= 0 else (vv, -gg / qq ** P)
    for k in range(1, int(round(T / dt)) + 1):
        tgt = round(k * dt, 9)
        while t < tgt - 1e-12:
            s = min(h, tgt - t)
            a1 = f(q, v); a2 = f(q + s/2*a1[0], v + s/2*a1[1]); a3 = f(q + s/2*a2[0], v + s/2*a2[1]); a4 = f(q + s*a3[0], v + s*a3[1])
            q += s/6*(a1[0]+2*a2[0]+2*a3[0]+a4[0]); v += s/6*(a1[1]+2*a2[1]+2*a3[1]+a4[1]); t += s
        t = tgt; out[tgt] = q
    return out


def load(n):
    req = json.load(open('%s/requests/2026-11-23/r3/lab-keystone/%s.json' % (ROOT, n)))
    res = json.load(open('%s/results/2026-11-23/r3/lab-keystone/%s.json' % (ROOT, n)))
    ps = req['setup']['particles']
    d0 = [ps[1]['pos'][k] - ps[0]['pos'][k] for k in range(2)]
    r0 = math.hypot(*d0); u = [c / r0 for c in d0]
    pts = []
    for s in res['samples']:
        p = {q['id']: q['pos'] for q in s['particles']}
        d = [p[1][k] - p[0][k] for k in range(2)]
        pts.append((round(s['t'], 9), d[0] * u[0] + d[1] * u[1]))
    return r0, req['setup']['duration'], req['setup']['sample_dt'], pts


bins = [(0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0001)]
print('run   r0   ' + '  '.join('[%.1f,%.1f)' % b for b in bins) + '   (mean residual, measured minus P-0024 M1)')
for n in RUNS:
    r0, T, dt, pts = load(n)
    m = traj(r0, T, dt, 23.63)
    cells = []
    for lo, hi in bins:
        e = [s - m[t] for t, s in pts if lo <= t < hi and t in m]
        cells.append('%+.3f' % (sum(e) / len(e)))
    print(n, '%.1f' % r0, '  '.join(cells))
print('best-fit G (P = 2.099 fixed), t <= 1:')
for n in RUNS:
    r0, T, dt, pts = load(n)
    best = None
    for i in range(0, 41):
        gg = 20.0 + i * 0.1
        m = traj(r0, T, dt, gg)
        sse = sum((s - m[t]) ** 2 for t, s in pts if t in m and t <= 1.0)
        if best is None or sse < best[1]:
            best = (gg, sse)
    print(n, 'r0=%.1f  G_best=%.2f  G_best/G_M1=%.3f' % (r0, best[0], best[0] / 23.63))
