"""Independent check of P-0007 (lab-a triangle runs 2026-11-19/r1/lab-a/001-004).
Pairwise sum, P-0005 table at r=5 (A-A from P-0003 K), r^-2.5, no three-body term."""
import sys, json
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/labs/lab-keystone/analysis')
from sim import simulate, observed, rms, sse_and_count, ROOT
import math

def table(aa):
    # coef[(si,sj)] = coupling for a particle of species si pulled toward species sj
    return {('A','A'): aa, ('A','B'): 8.99, ('B','A'): 12.34, ('A','C'): -8.77, ('C','A'): -21.25,
            ('B','B'): 6.12, ('B','C'): -6.10, ('C','B'): -10.59, ('C','C'): 12.36}

for aa in [17.7, 18.0]:
    T = table(aa)
    print('A-A coefficient', aa)
    for n in [1, 2, 3, 4]:
        req = json.load(open('%s/requests/2026-11-19/r1/lab-a/%03d.json' % (ROOT, n)))
        res = json.load(open('%s/results/2026-11-19/r1/lab-a/%03d.json' % (ROOT, n)))
        parts = req['setup']['particles']
        sp = [p['species'] for p in parts]
        init = [p['pos'] for p in parts]; vel = [p['vel'] for p in parts]
        Tt, dt = req['setup']['duration'], req['setup']['sample_dt']
        coef = lambda i, j, sp=sp: T[(sp[i], sp[j])]
        sim = simulate(init, vel, coef, 2.5, len(parts), Tt, dt, h=0.005)
        obs = observed(res)
        print('  run %03d %s rms/coord %.4f  (status %s, cost %s)' % (n, ''.join(sp), rms(sim, obs), res.get('status'), res.get('cost')))
