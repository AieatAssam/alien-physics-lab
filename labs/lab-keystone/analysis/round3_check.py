"""Round 3 (2026-11-20): score round-2 pre-registered requests 001-007 (lab-keystone, own runs)
and check my P-0011 review runs 008-010 (review account) against the P-0011 model.

Pairs: constant K per particle with the r^-2.5 law, two free coefficients (grid + refinement),
from round2_r1_check.pair_run in the repo analysis dir (imported read-only, -B so no bytecode is written).
Run with: python3 -B -I round3_check.py
"""
import sys, math, json
REPO = '/home/runner/work/alien-physics-lab/alien-physics-lab'
sys.path.insert(0, REPO + '/labs/lab-keystone/analysis')
import round2_r1_check as m

m.DAY, m.RND, m.LAB = '2026-11-20', 'r2', 'lab-keystone'

# Pre-registered (see NOTEBOOK round-2 table). K ordering: (K on particle 0, K on particle 1).
K5 = {'AC': (-8.77, -21.25), 'BB': (6.12, 6.12), 'CC': (12.36, 12.36), 'AA': (18.0, 18.0)}
PRED = {
    1: tuple(0.87 * k for k in K5['AC']),   # A-C r=2.0, ratio 0.87
    2: tuple(0.90 * k for k in K5['AC']),   # A-C r=2.5, ratio 0.90
    3: tuple(0.95 * k for k in K5['AC']),   # A-C r=3.5, ratio 0.95
    4: tuple(0.90 * k for k in K5['BB']),   # B-B r=2.5, ratio 0.90
    5: tuple(0.90 * k for k in K5['CC']),   # C-C r=2.5, ratio 0.90
    6: tuple(0.93 * k for k in K5['AA']),   # A-A r=3.0, ratio 0.93
    7: (8.43, 8.43),                         # C-C r=9, T=6, S_CC=1 (alt 7.99 for S_C=0.9475)
}

if __name__ == '__main__':
    for n in range(1, 8):
        req = json.load(open('%s/requests/%s/%s/%s/%03d.json' % (REPO, m.DAY, m.RND, m.LAB, n)))
        print('-- %03d: %s' % (n, req['purpose'][:110]))
        m.pair_run(n, PRED[n])
    print('-- 007 alt (S_C=0.9475 prediction): 7.99 each')
    print('-- P-0011 review runs (review account), lone particle, noise-free position = initial (at rest, no wall reached)')
    for n in (8, 9, 10):
        req, res = m.load(n)
        p = req['setup']['particles'][0]
        x0, y0 = p['pos']
        obs = m.observed(res)[0]
        dx = [q[0] - x0 for _, q in obs]; dy = [q[1] - y0 for _, q in obs]
        rms = math.sqrt(sum(v * v for v in dx + dy) / (2 * len(dx)))
        mx, my = sum(dx) / len(dx), sum(dy) / len(dy)
        print('%03d %s at (%.2f,%.2f) N=%d  rms/coord=%.4f  mean=(%+.4f,%+.4f)  error=%.5f  bar=0.015  %s' % (
            n, p['species'], x0, y0, len(dx), rms, mx, my, rms / 10.0,
            'PASS' if rms / 10.0 <= 0.015 else 'MISS'))
