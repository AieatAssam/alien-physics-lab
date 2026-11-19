"""N=3 (req 011) and N=4 (req 012) additivity: integrate with the P-0005 pair table and the
r^-2.5 shape (pairwise sum), and with the shared factor G(r) (A-A K_eff curve, see keff_aa.py).
Compare with tracker positions per particle; report displacement error and sample-wise residual."""
import sys, math
sys.path.insert(0, '.')
from sim import req, res, observed, simulate_g, sse_and_count

TABLE5 = {('A','A'): 18.0, ('A','B'): 8.99, ('B','A'): 12.34, ('A','C'): -8.77, ('C','A'): -21.25,
          ('B','B'): 6.12, ('C','C'): 12.36, ('B','C'): -6.10, ('C','B'): -10.59}
# A-A effective factor relative to r=5 (P=2.5 fixed), from keff_aa.py: K_eff/18.0, interpolated
G_PTS = [(3, 17.6/18), (4, 17.7/18), (5, 1.0), (6, 16.5/18), (7, 15.5/18), (8, 13.94/18), (9, 11.9/18)]
def G(r):
    if r <= G_PTS[0][0]: return G_PTS[0][1]
    if r >= G_PTS[-1][0]: return G_PTS[-1][1]
    for (r0, g0), (r1, g1) in zip(G_PTS, G_PTS[1:]):
        if r0 <= r <= r1: return g0 + (g1 - g0) * (r - r0) / (r1 - r0)

for n, lab in [(11, 'N=3 A,A,C'), (12, 'N=4 A,B,C,A')]:
    r = req(n); rr = res(n); obs = observed(rr); s = r['setup']; parts = s['particles']
    sp = [p['species'] for p in parts]; pos0 = [p['pos'] for p in parts]; vel0 = [p['vel'] for p in parts]
    N = len(parts); T, dt = s['duration'], s['sample_dt']
    coefT = lambda i, j: TABLE5[(sp[i], sp[j])]
    simT = simulate_g(pos0, vel0, coefT, lambda r_: r_ ** -2.5, N, T, dt, h=0.005)
    # shared-factor version: g(r) = G(r) * r^-2.5 applied to the pair table, pair by pair
    simG = simulate_g(pos0, vel0, coefT, lambda r_: G(r_) * r_ ** -2.5, N, T, dt, h=0.005)
    print(lab, 'T', T, 'N', N)
    for name, sim in [('table r^-2.5 (pre-registered H1)', simT), ('table x shared factor G(r)', simG)]:
        sse, cnt, worst = sse_and_count(sim, obs)
        print('  %-34s rms/coord %.4f  max|res| %.3f' % (name, math.sqrt(sse / cnt), worst))
        for pid in range(N):
            tf = obs[pid][-1][1]; sf = sim[round(T, 9)][pid]
            print('     particle %d (%s): measured end (%.3f, %.3f) predicted (%.3f, %.3f) miss %.3f' % (
                pid, sp[pid], tf[0], tf[1], sf[0], sf[1], math.dist(tf, sf)))
    # no-interaction baseline
    simN = simulate_g(pos0, vel0, lambda i, j: 0.0, lambda r_: 1.0, N, T, dt, h=0.005)
    print('  no-interaction baseline rms/coord %.4f' % math.sqrt(sse_and_count(simN, obs)[0] / sse_and_count(simN, obs)[1]))
