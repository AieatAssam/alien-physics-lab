"""Score research 2026-11-23/r1/lab-keystone/001-006 (A-A at rest, r0 = 4, 5, 6, T = 2, sample_dt 0.01).
Projected separation along the initial axis d(t) (tracker noise ~0.05 per coordinate).
Models (1D relative motion of a symmetric pair, q'' = -G / q**P, q(0) = r0, q'(0) = 0):
  M1: P-0024 law, G = 23.63, P = 2.099 (fixed, extrapolated beyond its r0 <= 3 and T <= 0.6 window)
  M2: P = 2.5 law, G free (least squares on the 6 runs jointly)
Run: python3 -I <this file> <repo_root>
"""
import json, math, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
RUNS = ['001', '002', '003', '004', '005', '006']


def rhs_series(r0, G, P, T, dt, h=1e-3):
    q, v, t = r0, 0.0, 0.0
    out = [(0.0, q)]
    k = 0
    n = int(round(T / dt))
    for i in range(1, n + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            step = min(h, target - t)
            def f(qq, vv):
                if qq <= 0:
                    return vv, 0.0
                return vv, -G / qq ** P
            a1 = f(q, v)
            a2 = f(q + step / 2 * a1[0], v + step / 2 * a1[1])
            a3 = f(q + step / 2 * a2[0], v + step / 2 * a2[1])
            a4 = f(q + step * a3[0], v + step * a3[1])
            q += step / 6 * (a1[0] + 2 * a2[0] + 2 * a3[0] + a4[0])
            v += step / 6 * (a1[1] + 2 * a2[1] + 2 * a3[1] + a4[1])
            t += step
        t = target
        out.append((target, q))
    return out


def load(n):
    req = json.load(open('%s/requests/2026-11-23/r1/lab-keystone/%s.json' % (ROOT, n)))
    res = json.load(open('%s/results/2026-11-23/r1/lab-keystone/%s.json' % (ROOT, n)))
    ps = req['setup']['particles']
    p0 = ps[0]['pos']
    d0 = [ps[1]['pos'][k] - p0[k] for k in range(2)]
    r0 = math.hypot(*d0)
    u = [c / r0 for c in d0]
    pts = []
    for s in res['samples']:
        p = {q['id']: q['pos'] for q in s['particles']}
        d = [p[1][k] - p[0][k] for k in range(2)]
        pts.append((s['t'], d[0] * u[0] + d[1] * u[1]))
    return r0, req['setup']['duration'], req['setup']['sample_dt'], pts, d0


def resid(r0, pts, G, P, dt, T):
    model = dict(rhs_series(r0, G, P, T, dt))
    return [m - model[round(t, 9)] for t, m in pts if round(t, 9) in model]


if __name__ == '__main__':
    data = {n: load(n) for n in RUNS}
    print('run r0 T nsamp  min_measured_sep  M1 rms(sep)  ')
    for n in RUNS:
        r0, T, dt, pts, _ = data[n]
        m1 = resid(r0, pts, 23.63, 2.099, dt, T)
        rms1 = math.sqrt(sum(x * x for x in m1) / len(m1))
        print('%s %.1f %.1f %d  %.3f  M1 rms=%.4f  (RMSE/L=%.5f)' % (n, r0, T, len(pts), min(p[1] for p in pts), rms1, rms1 / 10))
    # M2: P = 2.5, G free: scan G, minimise total SSE over the six runs
    best = None
    for i in range(0, 61):
        G = 5.0 + i * 0.5
        sse = 0.0
        cnt = 0
        for n in RUNS:
            r0, T, dt, pts, _ = data[n]
            ms = resid(r0, pts, G, 2.5, dt, T)
            sse += sum(x * x for x in ms)
            cnt += len(ms)
        rms = math.sqrt(sse / cnt)
        if best is None or rms < best[1]:
            best = (G, rms)
    print('M2 (P=2.5) best G = %.2f, pooled rms = %.4f' % best)
    G2 = best[0]
    sse1 = 0.0; c1 = 0
    for n in RUNS:
        r0, T, dt, pts, _ = data[n]
        ms = resid(r0, pts, 23.63, 2.099, dt, T)
        sse1 += sum(x * x for x in ms); c1 += len(ms)
    print('M1 (P=2.099, G=23.63) pooled rms = %.4f' % math.sqrt(sse1 / c1))
    # Noise reference: per-coordinate tracker noise estimated from the early-time scatter of the unmoved pair
