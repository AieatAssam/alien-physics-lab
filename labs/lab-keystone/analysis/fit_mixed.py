"""Two-particle mixed-species runs at separations 3 (round-1 review requests 005-010) and 8
(research requests 013-015). Per run, fit the two signed coefficients (particle 0 on 1, and
1 on 0) with shape g(r)=r^-2.5 by coordinate golden search on tracker positions.
Then compare each coefficient with the P-0005 table value at r=5, and with the A-A factor
K_eff(r)/K_eff(5) measured in keff_aa.py (A-A: 17.6 at r=3, 18.0 at r=5, 13.9 at r=8)."""
import sys, math
sys.path.insert(0, '.')
from sim import req, res, observed, simulate_g, sse_and_count, golden

TABLE5 = {('A','A'): 18.0, ('A','B'): 8.99, ('B','A'): 12.34, ('A','C'): -8.77, ('C','A'): -21.25,
          ('B','B'): 6.12, ('C','C'): 12.36, ('B','C'): -6.10, ('C','B'): -10.59}
P = 2.5

def fit2(n, label):
    r = req(n); rr = res(n); obs = observed(rr)
    s = r['setup']; parts = s['particles']
    sp = [p['species'] for p in parts]; pos0 = [p['pos'] for p in parts]; vel0 = [p['vel'] for p in parts]
    T, dt = s['duration'], s['sample_dt']
    sep0 = math.dist(pos0[0], pos0[1])
    st = {'a': 0.0, 'b': 0.0}
    def cost(a, b):
        sim = simulate_g(pos0, vel0, lambda i, j: a if (i, j) == (0, 1) else (b if (i, j) == (1, 0) else 0.0),
                         lambda rr_: rr_ ** (-P), 2, T, dt, h=0.01)
        return sse_and_count(sim, obs)[0]
    a, b = 10.0, 10.0
    for _ in range(3):
        a = golden(lambda x: cost(x, b), -40.0, 40.0, tol=0.01)
        b = golden(lambda y: cost(a, y), -40.0, 40.0, tol=0.01)
    sim = simulate_g(pos0, vel0, lambda i, j: a if (i, j) == (0, 1) else (b if (i, j) == (1, 0) else 0.0),
                     lambda rr_: rr_ ** (-P), 2, T, dt, h=0.01)
    sse, cnt, worst = sse_and_count(sim, obs)
    ta = TABLE5[(sp[0], sp[1])]; tb = TABLE5[(sp[1], sp[0])]
    print('req %03d %s  %s-%s sep0 %.2f T %.1f  fit K0(%s on %s)=%.2f  K1(%s on %s)=%.2f  '
          'rms %.4f max %.3f' % (n, label, sp[0], sp[1], sep0, T, sp[0], sp[1], a, sp[1], sp[0], b,
                                 math.sqrt(sse / cnt), worst))
    print('     table@5: %s on %s %.2f (ratio %.3f) ; %s on %s %.2f (ratio %.3f)' % (
        sp[0], sp[1], ta, a / ta, sp[1], sp[0], tb, b / tb))

for n, lab in [(5, 'AA r3'), (6, 'AB r3'), (7, 'AC r3'), (8, 'BB r3'), (9, 'CC r3'), (10, 'BC r3')]:
    fit2(n, lab)
for n, lab in [(13, 'AB r8'), (14, 'AC r8'), (15, 'BC r8')]:
    fit2(n, lab)
