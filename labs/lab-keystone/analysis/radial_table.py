"""Fit two-particle couplings (r^-2.5, K0 and K1 free) for every lab-keystone run at separation 6-9
(N=2, at rest), and report K / K_P0005(5) = G_pair(r). Reference K(5) = P-0005 run means (accepted claims).
Uses round2_check.sim/fit/observed (pure python). Usage: python3 -I radial_table.py"""
import json, math, sys
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/out/labs/lab-keystone/analysis')
from round2_check import sim, observed, fit, ROOT
REF = {'AA': (18.0, 18.0), 'AB': (8.99, 12.34), 'AC': (-8.77, -21.25), 'BB': (6.12, 6.12), 'CC': (12.36, 12.36), 'BC': (-6.10, -10.59)}
# (path, guess) — guess from the reference table times a rough shape factor
RUNS = [
 ('2026-11-19/r1/lab-keystone/003', 0.77), ('2026-11-19/r1/lab-keystone/004', 0.66),
 ('2026-11-19/r1/lab-keystone/013', 0.77), ('2026-11-19/r1/lab-keystone/014', 0.77), ('2026-11-19/r1/lab-keystone/015', 0.77),
 ('2026-11-19/r2/lab-keystone/001', 0.74), ('2026-11-19/r2/lab-keystone/002', 0.65), ('2026-11-19/r2/lab-keystone/003', 0.68),
 ('2026-11-19/r2/lab-keystone/004', 0.92), ('2026-11-19/r2/lab-keystone/005', 0.77),
 ('2026-11-19/r3/lab-keystone/001', 0.77), ('2026-11-19/r3/lab-keystone/004', 0.77), ('2026-11-19/r3/lab-keystone/005', 0.82),
 ('2026-11-19/r3/lab-keystone/007', 0.93), ('2026-11-19/r3/lab-keystone/008', 0.93), ('2026-11-19/r3/lab-keystone/003', 1.0),
]
if __name__ == '__main__':
    out = []
    for path, g0 in RUNS:
        day, rnd, lab, n = path.split('/')
        req = json.load(open('%s/requests/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, n)))
        res = json.load(open('%s/results/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, n)))
        ps = req['setup']['particles']
        sp = ''.join(p['species'] for p in ps)
        init = [p['pos'] for p in ps]
        r = math.dist(init[0], init[1])
        T = req['setup']['duration']; dt = req['setup']['sample_dt']
        key = ''.join(sorted(sp))
        ref = REF[key]
        if sp[0] == sp[1]:
            ref0 = ref[0]; ref1 = ref[0]
        else:
            ref0, ref1 = (ref if key == sp else (ref[1], ref[0]))  # ensure ref0 applies to particle 0's species
        # For mixed pairs reference orientation: REF key is sorted pair; K on particle sp[0] given by table
        K0, K1, rms = fit(init, observed(res), T, dt, ref0 * g0 / 1.0 if False else ref0 * g0, ref1 * g0)
        G0, G1 = K0 / ref0, K1 / ref1
        print('%s %s r=%.2f T=%.1f K0=%.3f K1=%.3f G0=%.4f G1=%.4f rms=%.4f' % (path, sp, r, T, K0, K1, G0, G1, rms), flush=True)
