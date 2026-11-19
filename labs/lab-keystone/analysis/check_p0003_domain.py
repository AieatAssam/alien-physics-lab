"""Does P-0003's constant law (K=17.74, P=2.5) fit its own separation-6 runs? Compare rms at the
claimed K with the per-run best K, for lab-a 2026-11-17/r3 runs 007-008 (sep 6) and 005-006 (sep 5)."""
import sys, math
sys.path.insert(0, '.')
from sim import load_any, observed, simulate_g, sse_and_count, golden
for n in (5, 6, 7, 8):
    r, rr = load_any('2026-11-17', 'r3', 'lab-a', n)
    s = r['setup']; obs = observed(rr)
    pos0 = [p['pos'] for p in s['particles']]; vel0 = [p['vel'] for p in s['particles']]
    def cost(K):
        sim = simulate_g(pos0, vel0, lambda i, j: K, lambda q: q ** -2.5, 2, s['duration'], s['sample_dt'], h=0.01)
        return sse_and_count(sim, obs)[0]
    Kb = golden(cost, 5.0, 30.0, tol=0.005)
    sse17, cnt, _ = sse_and_count(simulate_g(pos0, vel0, lambda i, j: 17.74, lambda q: q ** -2.5, 2, s['duration'], s['sample_dt'], h=0.01), obs)
    print('lab-a 2026-11-17/r3/lab-a/%03d sep %.1f T %.1f: rms at K=17.74 %.4f ; best K %.2f rms %.4f' % (
        n, math.dist(pos0[0], pos0[1]), s['duration'], math.sqrt(sse17 / cnt), Kb, math.sqrt(cost(Kb) / cnt)))
