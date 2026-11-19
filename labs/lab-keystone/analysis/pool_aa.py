"""Pooled fit of the A-A radial law across all two-particle, species-A, at-rest runs in the repo:
separations 3 to 9. Compares power law K/r^P against screened K exp(-r/lam)/r^2 (both 2 params).
Each run: K is fitted by golden search, the shape by a grid. Residuals in tracker units."""
import sys, math, time
sys.path.insert(0, '.')
from sim import load_any, observed, simulate_g, sse_and_count, golden

RUNS = [('2026-11-17','r3','lab-a',n) for n in range(1,9)] + [('2026-11-18','r2','lab-a',6),('2026-11-18','r2','lab-a',7),('2026-11-18','r1','lab-a',8),('2026-11-18','r1','lab-a',9)] + [('2026-11-19','r1','lab-keystone',n) for n in (3,4,5)]
DATA = []
for date, rnd, lab, n in RUNS:
    r, rr = load_any(date, rnd, lab, n)
    s = r['setup']
    if [p['species'] for p in s['particles']] != ['A','A'] or any(abs(v) for p in s['particles'] for v in p['vel']):
        continue
    DATA.append(((date, rnd, lab, n), s, observed(rr)))

def pooled(gfun_factory, params):
    total_sse = 0.0; total_cnt = 0; per = []
    for key, s, obs in DATA:
        pos0 = [p['pos'] for p in s['particles']]; vel0 = [p['vel'] for p in s['particles']]
        sim = simulate_g(pos0, vel0, lambda i, j, K=params['K']: K, gfun_factory(params), 2, s['duration'], s['sample_dt'], h=0.02)
        sse, cnt, _ = sse_and_count(sim, obs)
        total_sse += sse; total_cnt += cnt; per.append((key, math.sqrt(sse / cnt)))
    return math.sqrt(total_sse / total_cnt), per

def fit_family(name, shape_grid, factory):
    best = None
    for sval in shape_grid:
        K = golden(lambda K: pooled(factory, {'K': K, 's': sval})[0] ** 2, 5.0, 30.0, tol=0.02)
        rmsv, per = pooled(factory, {'K': K, 's': sval})
        print('%s shape=%.3f K=%.3f pooled rms/coord %.4f' % (name, sval, K, rmsv), flush=True)
        if best is None or rmsv < best[0]:
            best = (rmsv, sval, K, per)
    return best

t0 = time.time()
pw = fit_family('power', [2.0, 2.25, 2.5, 2.75, 3.0], lambda p: (lambda r: r ** (-p['s'])))
sc = fit_family('screened', [4.0, 6.0, 8.0, 10.0, 14.0], lambda p: (lambda r: math.exp(-r / p['s']) / r ** 2))
for name, b in [('power', pw), ('screened', sc)]:
    print('BEST %s: shape %.3f K %.3f pooled rms %.4f' % (name, b[1], b[2], b[0]))
    for key, rm in b[3]:
        print('   %s %s run %03d  rms %.4f' % (name, key[2], key[3], rm))
print('elapsed %.0f s' % (time.time() - t0))
