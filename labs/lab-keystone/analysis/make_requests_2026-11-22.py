"""Round 1, 2026-11-22, lab-keystone.
Research 001-006: A-A exponent scan. Model-free acceleration at r0 = 0.5, 1.0, 2.0 (two orientations each).
  Pre-registered: under a pure power law a(r) ~ r^-P with P = 2.5 the ratios a(0.5)/a(1.0) and a(1.0)/a(2.0)
  are both 2^2.5 = 5.66 (orientation-averaged). The shape notebook (f-knots) implies about 3.7 for a(1)/a(2) (local P about 1.9).
Review 007-009: P-0016 (A-C at r0 = 1.0, T <= 0.6). Account review, cites P-0016. Edge-of-domain placements.
Run: python3 -I <this file>"""
import json, math, sys
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/tools')
import domain as dom

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
OUT = ROOT + '/out/requests/2026-11-22/r1/lab-keystone'
DAY_RND = '2026-11-22/r1/lab-keystone'


def P(sp, x, y):
    return {'species': sp, 'pos': [x, y], 'vel': [0.0, 0.0]}


def setup(parts, T, dt):
    return {'particles': parts, 'duration': T, 'sample_dt': dt}


def req(n, account, purpose, s, instr, cites=None):
    d = {'request_id': '%s/%03d' % (DAY_RND, n), 'lab': 'lab-keystone', 'account': account,
         'purpose': purpose, 'setup': s, 'instruments': instr}
    if cites:
        d['cites_paper'] = cites
    return d


reqs = []
PUR = 'A-A exponent scan, at rest, %s, r0=%s. Model-free acceleration test of P=2.5 at close range (pre-reg in notebook 2026-11-22).'
reqs.append(req(1, 'research', PUR % ('horizontal', '0.5'), setup([P('A', 4.0, 4.0), P('A', 4.5, 4.0)], 0.03, 0.0005), ['tracker']))
reqs.append(req(2, 'research', PUR % ('vertical', '0.5'), setup([P('A', 7.0, 2.0), P('A', 7.0, 2.5)], 0.03, 0.0005), ['tracker']))
reqs.append(req(3, 'research', PUR % ('horizontal', '1.0'), setup([P('A', 4.0, 6.0), P('A', 5.0, 6.0)], 0.1, 0.001), ['tracker']))
reqs.append(req(4, 'research', PUR % ('vertical', '1.0'), setup([P('A', 7.0, 6.0), P('A', 7.0, 7.0)], 0.1, 0.001), ['tracker']))
reqs.append(req(5, 'research', PUR % ('horizontal', '2.0'), setup([P('A', 2.0, 2.0), P('A', 4.0, 2.0)], 0.3, 0.005), ['tracker']))
reqs.append(req(6, 'research', PUR % ('vertical', '2.0'), setup([P('A', 8.0, 6.0), P('A', 8.0, 8.0)], 0.3, 0.005), ['tracker']))

# P-0016 review: A-C, claim domain species A,C; r in [0.999, 1.001]; max_particles 2; T <= 0.6
DOM = {'species': ['A', 'C'], 'r_range': [0.999, 1.001], 'max_particles': 2}
rp = 0.9995 / math.sqrt(2)
rev_setups = [
    ('007', [P('A', 4.0, 5.0), P('C', 5.0, 5.0)], 'horizontal, A first, r0 = 1.000 (centre of domain)'),
    ('008', [P('C', 2.0, 7.0), P('A', 2.0, 7.9995)], 'vertical, C first, r0 = 0.9995 (lower edge of domain)'),
    ('009', [P('A', 7.0, 3.0), P('C', 7.0 + 1.0005 / math.sqrt(2), 3.0 + 1.0005 / math.sqrt(2))],
     'diagonal, A first, r0 = 1.0005 (upper edge of domain)'),
]
for tag, parts, desc in rev_setups:
    n = int(tag)
    s = setup(parts, 0.6, 0.01)
    assert dom.in_domain(DOM, s), tag
    reqs.append(req(n, 'review', 'Review of P-0016 (A-C at r0 = 1.0, T = 0.6, at rest, %s). Edge-of-domain test of the claim; K-insensitive metric, comment will say so.' % desc, s, ['tracker'], cites='P-0016'))

for r in reqs:
    with open('%s/%s.json' % (OUT, r['request_id'].split('/')[-1]), 'w') as f:
        json.dump(r, f, indent=2)
        f.write('\n')
    print(r['request_id'], r['account'], 'cost', round(1 + (1/60) * len(r['setup']['particles']) * r['setup']['duration'], 4))
