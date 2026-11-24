"""Score research 2026-11-23/r3/lab-keystone/002-007 against the pre-registered pass rule
(prereg_2026-11-23_r3.json): M1 = P-0024 law (G = 23.63, P = 2.099) on the projected
separation along the initial axis, t <= 1.0. Pass if pooled residual rms <= 0.09 and no run's
residual drifts past t = 0.5 by more than 0.1.
Run: python3 -I <this file> <repo_root>
"""
import json, math, sys
sys.path.insert(0, sys.path[0])
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
RUNS = ['002', '003', '004', '005', '006', '007']
G, P = 23.63, 2.099


def rk(r0, T, dt, h=1e-3):
    q, v, t = r0, 0.0, 0.0
    out = {0.0: q}
    n = int(round(T / dt))
    for i in range(1, n + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            s = min(h, target - t)
            def f(qq, vv):
                return (vv, 0.0) if qq <= 0 else (vv, -G / qq ** P)
            a1 = f(q, v); a2 = f(q + s / 2 * a1[0], v + s / 2 * a1[1])
            a3 = f(q + s / 2 * a2[0], v + s / 2 * a2[1]); a4 = f(q + s * a3[0], v + s * a3[1])
            q += s / 6 * (a1[0] + 2 * a2[0] + 2 * a3[0] + a4[0])
            v += s / 6 * (a1[1] + 2 * a2[1] + 2 * a3[1] + a4[1])
            t += s
        t = target
        out[target] = q
    return out


rows = []
for n in RUNS:
    req = json.load(open('%s/requests/2026-11-23/r3/lab-keystone/%s.json' % (ROOT, n)))
    res = json.load(open('%s/results/2026-11-23/r3/lab-keystone/%s.json' % (ROOT, n)))
    ps = req['setup']['particles']
    d0 = [ps[1]['pos'][k] - ps[0]['pos'][k] for k in range(2)]
    r0 = math.hypot(*d0)
    u = [c / r0 for c in d0]
    T, dt = req['setup']['duration'], req['setup']['sample_dt']
    model = rk(r0, T, dt)
    res_t = []
    for s in res['samples']:
        p = {q['id']: q['pos'] for q in s['particles']}
        d = [p[1][k] - p[0][k] for k in range(2)]
        sep = d[0] * u[0] + d[1] * u[1]
        t = round(s['t'], 9)
        if t in model:
            res_t.append((t, sep - model[t]))
    rms = math.sqrt(sum(e * e for _, e in res_t) / len(res_t))
    early = [e for t, e in res_t if t > 0.5]
    drift = max(abs(e) for e in early) if early else float('nan')
    mean_late = sum(early) / len(early)
    orient = 'H' if abs(u[0]) > 0.5 else 'V'
    rows.append((n, r0, orient, rms, drift, mean_late, len(res_t)))
    print('%s r0=%.1f %s n=%d rms=%.4f max|res|(t>0.5)=%.4f mean_res(t>0.5)=%+.4f' % (n, r0, orient, len(res_t), rms, drift, mean_late))

pooled = math.sqrt(sum(r[3] ** 2 * r[6] for r in rows) / sum(r[6] for r in rows))
max_drift = max(r[4] for r in rows)
print('pooled rms = %.4f (pass <= 0.09)' % pooled)
print('max |residual| after t = 0.5 across runs = %.4f (pass: no run drifts past 0.1 by more than 0.1)' % max_drift)
print('PASS' if (pooled <= 0.09 and max_drift <= 0.1) else 'FAIL')
