"""Round 2, 2026-11-22, lab-keystone.
Research 001-006: A-A replicate of the exponent test at r0 = 1.0 (T 0.1) and r0 = 2.0 (T 0.3), three orientations each.
  Pre-registered: P = 2.5 predicts a(1.0)/a(2.0) = 5.66 (fitted with exponent_ratio_2026-11-22.py);
  a local exponent of 1.9 predicts 3.7. Single pairs only (no cross-pair forces).
Review 007-012 (account review, cites): P-0019 (B-B, T <= 0.3, r 0.999-1.001) and P-0021 (A-B, sep 6.9-7.1, T <= 6).
Run: python3 -I <this file>"""
import json, math, os, sys
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
sys.path.insert(0, ROOT + '/tools')
import domain as dom

OUT = ROOT + '/out/requests/2026-11-22/r2/lab-keystone'
DAY_RND = '2026-11-22/r2/lab-keystone'
os.makedirs(OUT, exist_ok=True)
S2 = 1 / math.sqrt(2)


def P(sp, x, y):
    return {'species': sp, 'pos': [x, y], 'vel': [0.0, 0.0]}


def S(parts, T, dt):
    return {'particles': parts, 'duration': T, 'sample_dt': dt}


def req(n, account, purpose, s, cites=None):
    d = {'request_id': '%s/%03d' % (DAY_RND, n), 'lab': 'lab-keystone', 'account': account,
         'purpose': purpose, 'setup': s, 'instruments': ['tracker']}
    if cites:
        d['cites_paper'] = cites
    return d


reqs = []
PUR = 'A-A exponent replicate (pre-reg: P=2.5 gives a(1)/a(2)=5.66, local P 1.9 gives 3.7). %s, r0=%s, at rest, single pair.'
reqs.append(req(1, 'research', PUR % ('horizontal', '1.0'), S([P('A', 4.0, 3.0), P('A', 5.0, 3.0)], 0.1, 0.001)))
reqs.append(req(2, 'research', PUR % ('vertical', '1.0'), S([P('A', 7.0, 3.0), P('A', 7.0, 4.0)], 0.1, 0.001)))
reqs.append(req(3, 'research', PUR % ('diagonal', '1.0'), S([P('A', 2.0, 7.0), P('A', 2.0 + S2, 7.0 + S2)], 0.1, 0.001)))
reqs.append(req(4, 'research', PUR % ('horizontal', '2.0'), S([P('A', 2.0, 7.5), P('A', 4.0, 7.5)], 0.3, 0.005)))
reqs.append(req(5, 'research', PUR % ('vertical', '2.0'), S([P('A', 7.0, 6.5), P('A', 7.0, 8.5)], 0.3, 0.005)))
reqs.append(req(6, 'research', PUR % ('diagonal', '2.0'), S([P('A', 5.0, 2.0), P('A', 5.0 + 2 * S2, 2.0 + 2 * S2)], 0.3, 0.005)))

DOM_B = {'species': ['B'], 'r_range': [0.999, 1.001], 'max_particles': 2}
DOM_AB = {'species': ['A', 'B'], 'r_range': [6.9, 7.1], 'max_particles': 2}
rev = [
    (7, 'P-0019', DOM_B, 'B-B horizontal, r0 = 1.000 (centre), T = 0.3 (claim edge)',
     S([P('B', 4.0, 5.0), P('B', 5.0, 5.0)], 0.3, 0.001)),
    (8, 'P-0019', DOM_B, 'B-B vertical, r0 = 0.999 (lower edge), T = 0.3',
     S([P('B', 2.0, 2.0), P('B', 2.0, 2.999)], 0.3, 0.001)),
    (9, 'P-0019', DOM_B, 'B-B diagonal, r0 = 1.001 (upper edge), T = 0.3',
     S([P('B', 7.0, 7.0), P('B', 7.0 + 1.001 * S2, 7.0 + 1.001 * S2)], 0.3, 0.001)),
    (10, 'P-0021', DOM_AB, 'A-B horizontal, r0 = 6.901 (lower edge), T = 6 (claim edge)',
     S([P('A', 1.5, 5.0), P('B', 8.401, 5.0)], 6.0, 0.01)),
    (11, 'P-0021', DOM_AB, 'A-B vertical, r0 = 7.000 (centre), T = 6',
     S([P('A', 5.0, 1.5), P('B', 5.0, 8.5)], 6.0, 0.01)),
    (12, 'P-0021', DOM_AB, 'A-B diagonal, r0 = 7.099 (upper edge), T = 6',
     S([P('A', 2.0, 8.0), P('B', 2.0 + 7.099 * S2, 8.0 - 7.099 * S2)], 6.0, 0.01)),
]
for n, pid, d, desc, s in rev:
    assert dom.in_domain(d, s), (n, pid)
    reqs.append(req(n, 'review', 'Review of %s (%s). Edge-of-domain run; judged metric only.' % (pid, desc), s, cites=pid))

for r in reqs:
    with open('%s/%s.json' % (OUT, r['request_id'].split('/')[-1]), 'w') as f:
        json.dump(r, f, indent=2)
        f.write('\n')
    print(r['request_id'], r['account'], 'cost', round(1 + (1 / 60) * len(r['setup']['particles']) * r['setup']['duration'], 4))
