"""Per-run effective coefficient K_eff for each two-particle, species-A, at-rest run in the repo.
Fixed shape g(r)=r^-P (P in {2.5, 2.75}); K fitted per run by golden search on tracker positions."""
import sys, math
sys.path.insert(0, '.')
from sim import load_any, observed, simulate_g, sse_and_count, golden

RUNS = [('2026-11-17','r3','lab-a',n) for n in range(1,9)] + [('2026-11-18','r2','lab-a',6),('2026-11-18','r2','lab-a',7),('2026-11-18','r1','lab-a',8),('2026-11-18','r1','lab-a',9)] + [('2026-11-19','r1','lab-keystone',n) for n in (3,4,5)]
for P in (2.5, 2.75):
    print('shape P = %.2f' % P)
    rows = []
    for date, rnd, lab, n in RUNS:
        r, rr = load_any(date, rnd, lab, n); s = r['setup']
        if [p['species'] for p in s['particles']] != ['A', 'A'] or any(abs(v) for p in s['particles'] for v in p['vel']):
            continue
        obs = observed(rr)
        pos0 = [p['pos'] for p in s['particles']]; vel0 = [p['vel'] for p in s['particles']]
        def cost(K):
            sim = simulate_g(pos0, vel0, lambda i, j: K, lambda r: r ** (-P), 2, s['duration'], s['sample_dt'], h=0.01)
            return sse_and_count(sim, obs)[0]
        K = golden(cost, 5.0, 30.0, tol=0.005)
        sim = simulate_g(pos0, vel0, lambda i, j: K, lambda r: r ** (-P), 2, s['duration'], s['sample_dt'], h=0.01)
        sse, cnt, _ = sse_and_count(sim, obs)
        sep0 = math.dist(pos0[0], pos0[1])
        rows.append((sep0, K, math.sqrt(sse / cnt), '%s/%s/%s/%03d' % (date, rnd, lab, n), s['duration']))
    for sep0, K, rm, key, T in sorted(rows):
        print('  sep0 %.2f  K_eff %.2f  rms %.4f  T %.1f  %s' % (sep0, K * sep0 ** 0 , rm, T, key))
