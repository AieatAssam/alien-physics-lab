import json, os, re
OUT = '/home/runner/work/alien-physics-lab/alien-physics-lab/out'
LAB = 'lab-vernier'
DATE = '2026-11-21'

def wj(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')

def particle(sp, pos, vel=(0.0, 0.0)):
    return {'species': sp, 'pos': [float(pos[0]), float(pos[1])], 'vel': [float(vel[0]), float(vel[1])]}

def req(n, account, purpose, parts, T, dt, cites=None):
    rid = '%s/r1/%s/%03d' % (DATE, LAB, n)
    r = {'request_id': rid, 'lab': LAB, 'account': account, 'purpose': purpose,
         'setup': {'particles': parts, 'duration': T, 'sample_dt': dt},
         'instruments': ['tracker', 'census']}
    if cites:
        r['cites_paper'] = cites
    return rid, r

reqs = []
# review account: P-0004 (A-B and A-C at separation 5, three orientations each)
ab_pos = [
    ('h', [2.5, 5.0], [7.5, 5.0]),
    ('d', [2.0, 3.0], [5.0, 7.0]),
    ('v', [5.0, 2.5], [5.0, 7.5]),
]
for k, (tag, pa, pb) in enumerate(ab_pos, start=1):
    reqs.append(req(k, 'review',
        'P-0004 claim c1 (A-B, separation 5.0, at rest, T=3), orientation %s. Tests the paper A-B coupling '
        'against its predictor; zero-force null error is about 0.031, so the run discriminates.' % tag,
        [particle('A', pa), particle('B', pb)], 3.0, 0.01, 'P-0004'))
ac_pos = [
    ('h', [2.5, 5.0], [7.5, 5.0]),
    ('d', [2.0, 3.0], [5.0, 7.0]),
    ('v', [5.0, 2.5], [5.0, 7.5]),
]
for k, (tag, pa, pb) in enumerate(ac_pos, start=4):
    reqs.append(req(k, 'review',
        'P-0004 claim c2 (A-C repulsion, separation 5.0, at rest, T=3), orientation %s. Replicates the single '
        'run 2026-11-18/r1/lab-a/005; zero-force null error about 0.037.' % tag,
        [particle('A', pa), particle('C', pb)], 3.0, 0.01, 'P-0004'))
# research account
ac_close = [
    ('h', [3.0, 5.0], [4.0, 5.0]),
    ('v', [5.0, 4.0], [5.0, 5.0]),
    ('d', [4.0, 4.0], [4.0 + 0.70710678, 4.0 + 0.70710678]),
]
for k, (tag, pa, pb) in enumerate(ac_close, start=7):
    reqs.append(req(k, 'research',
        'Close-AC probe at separation 1.0 (open problem close-AC), at rest, T=0.6, orientation %s. A-C is '
        'repulsive so no contact is expected; fit K_AC, K_CA as in r2/010 for B-C.' % tag,
        [particle('A', pa), particle('C', pb)], 0.6, 0.003))
reqs.append(req(10, 'research',
    'A-B at separation 7.0 (horizontal), at rest, T=6. Extends the far-field check to A-B, which P-0010 does not '
    'cover at 7. Null error about 0.057.',
    [particle('A', [1.5, 5.0]), particle('B', [8.5, 5.0])], 6.0, 0.01))

for n, r in reqs:
    path = os.path.join(OUT, 'requests', DATE, 'r1', LAB, '%03d.json' % int(r['request_id'][-3:]))
    wj(path, r)
    cost_k = 0.02
    N = len(r['setup']['particles']); T = r['setup']['duration']
    print(r['request_id'], r['account'], 'cost %.2f' % (1 + cost_k * N * T), 'samples', round(T / r['setup']['sample_dt']))

grant = {
    'lab': LAB,
    'date': DATE,
    'title': 'Eight-body superposition test: a crowd of eight, mixed species A, B, C, at rest',
    'pitch': ('Crowd-8 open problem. Our pair laws are pairwise: P-0004 (A-B and A-C at separation 5), P-0010 '
              '(far-field), and the close B-C constants. Eight particles on a 3x3 grid minus the centre, minimum '
              'separation 3.5, at rest, T = 2. If the force is a sum of pair terms, the pairwise predictor should '
              'match at tracker noise (error at or below 0.015). A clear miss would show many-body terms. The '
              'zero-force null is large here, so the run discriminates.'),
    'setup': {
        'particles': [
            particle('A', [1.5, 1.5]), particle('B', [5.0, 1.5]), particle('B', [8.5, 1.5]),
            particle('C', [1.5, 5.0]), particle('A', [8.5, 5.0]),
            particle('C', [1.5, 8.5]), particle('B', [5.0, 8.5]), particle('A', [8.5, 8.5]),
        ],
        'duration': 2.0,
        'sample_dt': 0.01,
    },
}
assert len(grant['title']) <= 120 and len(grant['pitch']) <= 600, (len(grant['title']), len(grant['pitch']))
wj(os.path.join(OUT, 'grants', DATE, 'proposals', LAB + '.json'), grant)
print('pitch length', len(grant['pitch']), 'title length', len(grant['title']))
