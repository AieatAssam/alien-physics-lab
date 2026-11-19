"""A-A pair (two species-A particles at rest on x). Fit K and P (power law K/r^P) per run
to round-1 runs 003 (r~8), 004 (r~9), 005 (r~3, T=1). Also evaluate P-0003 (K=17.74, P=2.5)
and the pre-registered H1/H2 forms."""
import sys, math
sys.path.insert(0, '.')
from sim import req, res, observed, simulate, sse_and_count, rms, golden

def fit_run(n, dt_fit=0.01):
    r = req(n); rr = res(n); obs = observed(rr)
    parts = r['setup']['particles']
    pos0 = [p['pos'] for p in parts]; vel0 = [p['vel'] for p in parts]
    T = r['setup']['duration']; dt = r['setup']['sample_dt']
    sep0 = math.dist(pos0[0], pos0[1])
    def run(K, P):
        sim = simulate(pos0, vel0, lambda i, j: K, P, 2, T, dt, h=dt_fit)
        return sse_and_count(sim, obs)[0]
    def best_K(P):
        return golden(lambda K: run(K, P), 3.0, 40.0, tol=1e-3)
    best = None
    for P in [2.0, 2.25, 2.5, 2.75, 3.0]:
        K = best_K(P); s = run(K, P)
        cnt = sse_and_count(simulate(pos0, vel0, lambda i, j: K, P, 2, T, dt, h=dt_fit), obs)[1]
        line = 'run %03d sep0 %.3f T %.1f  P=%.2f K=%.3f rms/coord %.4f' % (n, sep0, T, P, K, math.sqrt(s / cnt))
        print(line)
        if best is None or s < best[0]:
            best = (s, P, K, cnt)
    # also: P=2.5, K=17.74 (P-0003) and K=18.0 (P-0005) predicted forms
    for K, P, name in [(17.74, 2.5, 'P-0003 K=17.74 P=2.5')]:
        sim = simulate(pos0, vel0, lambda i, j: K, P, 2, T, dt, h=dt_fit)
        s, c, w = sse_and_count(sim, obs)
        end_obs = obs[0][-1][1]; end_obs2 = obs[1][-1][1]
        end_sim = sim[round(T, 9)]
        print('  %s: rms/coord %.4f  final sep obs %.3f sim %.3f' % (name, math.sqrt(s/c), math.dist(end_obs, end_obs2), math.dist(end_sim[0], end_sim[1])))
    print('  best-fit overall: P=%.2f K=%.3f rms %.4f' % (best[1], best[2], math.sqrt(best[0] / best[3])))
    return best

for n in [5, 3, 4]:
    fit_run(n)
    print()
