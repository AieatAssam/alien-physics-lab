"""Round 1 (2026-11-23) requests for lab-keystone. Writes out/requests/2026-11-23/r1/lab-keystone/NNN.json.
Research (account research): A-A exponent extension to r0 = 4, 5, 6 (H and V), T = 2.0.
Review (account review, cites_paper): P-0017, P-0018 (B-B, C-C at r0 = 1.000, T = 0.15), P-0022 (A-B r0 = 2.0,
T = 0.8), P-0023 (A-B r0 = 9.0, T = 10). Three orientations per review paper. Results come back next round.
Run: python3 -I <this file>
"""
import json, math, os

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
DATE, RND, LAB = '2026-11-23', 'r1', 'lab-keystone'
OUT = '%s/out/requests/%s/%s/%s' % (ROOT, DATE, RND, LAB)
C = 5.0


def pair(sp1, sp2, r, orient, dt_T, dt_dt):
    h = r / 2.0
    if orient == 'H':
        a, b = [C - h, C], [C + h, C]
    elif orient == 'V':
        a, b = [C, C - h], [C, C + h]
    else:  # diagonal, separation r exactly
        o = h / math.sqrt(2)
        a, b = [C - o, C - o], [C + o, C + o]
    return {
        'particles': [{'species': sp1, 'pos': a, 'vel': [0.0, 0.0]},
                      {'species': sp2, 'pos': b, 'vel': [0.0, 0.0]}],
        'duration': dt_T, 'sample_dt': dt_dt,
    }


REQS = []
# Research: A-A at r0 = 4, 5, 6 (H, V). T = 2.0 so the pair stays clear of collapse at these radii.
for r in (4.0, 5.0, 6.0):
    for o in ('H', 'V'):
        REQS.append(dict(account='research', purpose='A-A exponent extension (round 1 of 2026-11-23): r0 = %.1f, %s, at rest, T = 2.0. Tests whether the power law of P-0024 extends beyond r0 = 3.' % (r, o),
                         setup=pair('A', 'A', r, o, 2.0, 0.01), cites=None))
# Review runs (account review), at the claim edges.
REV = [
    ('P-0017', 'B', 'B', 1.0, 0.15, 0.0015),
    ('P-0018', 'C', 'C', 1.0, 0.15, 0.0015),
    ('P-0022', 'A', 'B', 2.0, 0.8, 0.004),
    ('P-0023', 'A', 'B', 9.0, 10.0, 0.05),
]
for pid, s1, s2, r, T, dt_ in REV:
    for o in ('H', 'V', 'D'):
        REQS.append(dict(account='review', cites=pid,
                         purpose='Review of %s at its claim edge: r0 = %.3f, %s, at rest, T = %g (tracker only).' % (pid, r, o, T),
                         setup=pair(s1, s2, r, o, T, dt_), cites_paper=pid))

os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.json'):
        os.remove(os.path.join(OUT, f))
for i, q in enumerate(REQS, 1):
    rec = {'request_id': '%s/%s/%s/%03d' % (DATE, RND, LAB, i), 'lab': LAB, 'account': q['account'],
           'purpose': q['purpose'], 'setup': q['setup'], 'instruments': ['tracker']}
    if q['account'] == 'review':
        rec['cites_paper'] = q['cites_paper']
    json.dump(rec, open(os.path.join(OUT, '%03d.json' % i), 'w'), indent=2)
    print('%03d %s %s %s' % (i, q['account'], q.get('cites_paper', ''), q['purpose'][:60]))
