"""Round 3 requests for lab-keystone (2026-11-22).
001: grant, the voted main-event design (proposals/lab-keystone.json), unchanged.
002-016: research, A-A pairs at rest, five new radii (1.25, 1.5, 1.75, 2.5, 3.0) x {horizontal, vertical, diagonal},
     centred on (5,5); duration chosen so the relative displacement is ~0.2 to 0.4 (the signal scale), 101 samples each.
017: research, A-A diagonal r0 = 1.0 replicate at centre (3,7), T = 0.1 (second centre, same radius as round 1/2 anchor).
018: research, A-A vertical r0 = 2.0 replicate at centre (7,3), T = 0.3 (second centre, same radius as anchor).
022-024: research, r0 = 3.0 replicates at second centres (lever arm)
019-021: review (cites P-0020), A-B pair at r0 = 1.000, at rest, T = 0.15: horizontal (A left), vertical (B on top), diagonal.
Run: python3 -I <this file>
"""
import json, math, os

OUT = '/home/runner/work/alien-physics-lab/alien-physics-lab/out/requests/2026-11-22/r3/lab-keystone'
os.makedirs(OUT, exist_ok=True)
RID = '2026-11-22/r3/lab-keystone/%03d'
C = 0.7071067811865476  # 1/sqrt(2)


def pair(sp1, sp2, centre, r, orient):
    cx, cy = centre
    if orient == 'H':
        d = (r / 2, 0.0)
    elif orient == 'V':
        d = (0.0, r / 2)
    else:
        d = (r / 2 * C, r / 2 * C)
    p1 = [cx - d[0], cy - d[1]]
    p2 = [cx + d[0], cy + d[1]]
    return [
        {'species': sp1, 'pos': p1, 'vel': [0.0, 0.0]},
        {'species': sp2, 'pos': p2, 'vel': [0.0, 0.0]},
    ]


def setup(parts, T, dt):
    return {'particles': parts, 'duration': T, 'sample_dt': dt}


def write(n, obj):
    with open(os.path.join(OUT, '%03d.json' % n), 'w') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')


def research(n, purpose, parts, T, dt):
    write(n, {
        'request_id': RID % n, 'lab': 'lab-keystone', 'account': 'research', 'purpose': purpose,
        'setup': setup(parts, T, dt), 'instruments': ['tracker'],
    })


# 001: grant, voted design (16 particles, 8 A-A pairs), unchanged from the proposal
gp = json.load(open('/home/runner/work/alien-physics-lab/alien-physics-lab/grants/2026-11-22/proposals/lab-keystone.json'))
write(1, {
    'request_id': RID % 1, 'lab': 'lab-keystone', 'account': 'grant',
    'purpose': 'Grant main event (voted design, unchanged): eight A-A pairs at rest, r0 = 0.5 to 2.25 in steps of 0.25, one run. '
               'Pre-registered analysis masks samples where any pair separation is below 0.3 (the r0 = 0.5 pair reaches 0.25 r0 by t = 0.065 in a one-body model).',
    'setup': gp['setup'], 'instruments': ['tracker'],
})

# 002-016: five new radii x three orientations
radii = [(1.25, 0.20, 0.002), (1.5, 0.25, 0.0025), (1.75, 0.30, 0.003), (2.5, 0.60, 0.006), (3.0, 0.60, 0.006)]
n = 2
for r, T, dt in radii:
    for o, name in (('H', 'horizontal'), ('V', 'vertical'), ('D', 'diagonal')):
        research(n, 'A-A exponent curve (round 3): r0 = %.2f, %s, at rest, centre (5,5), T = %.2f. Pre-registered: '
                    'log-slope of a(r) vs log r; P = 2.5 gives -2.5, local P near 1.9 gives -1.9.' % (r, name, T),
                 pair('A', 'A', (5.0, 5.0), r, o), T, dt)
        n += 1
# 017, 018: anchor replicates at second centres
research(17, 'A-A diagonal anchor replicate: r0 = 1.00 at centre (3,7), T = 0.1. Second centre, same radius as round 1-2 anchors.',
         pair('A', 'A', (3.0, 7.0), 1.0, 'D'), 0.1, 0.001)
research(18, 'A-A vertical anchor replicate: r0 = 2.00 at centre (7,3), T = 0.3. Second centre, same radius as round 1-2 anchors.',
         pair('A', 'A', (7.0, 3.0), 2.0, 'V'), 0.3, 0.003)

# 022-024: r0 = 3.0 replicates at second centres (weakest-signal point at the end of the log-slope lever arm)
research(22, 'A-A horizontal r0 = 3.00 replicate at centre (6,4), T = 0.6. Second centre for the log-slope lever arm.',
         pair('A', 'A', (6.0, 4.0), 3.0, 'H'), 0.6, 0.006)
research(23, 'A-A vertical r0 = 3.00 replicate at centre (5,4), T = 0.6. Second centre for the log-slope lever arm.',
         pair('A', 'A', (5.0, 4.0), 3.0, 'V'), 0.6, 0.006)
research(24, 'A-A diagonal r0 = 3.00 replicate at centre (4,6), T = 0.6. Second centre for the log-slope lever arm.',
         pair('A', 'A', (4.0, 6.0), 3.0, 'D'), 0.6, 0.006)

# 019-021: review runs for P-0020 (A-B, close range, at rest, T = 0.15 = claim edge)
rv = [
    (19, 'Review of P-0020 (A-B horizontal, A left, r0 = 1.000 centre (5,5), T = 0.15 = claim edge). Judged error against the P-0020 model.',
     [{'species': 'A', 'pos': [4.5, 5.0], 'vel': [0.0, 0.0]}, {'species': 'B', 'pos': [5.5, 5.0], 'vel': [0.0, 0.0]}]),
    (20, 'Review of P-0020 (A-B vertical, B on top, r0 = 1.000 centre (5,5), T = 0.15). Judged error against the P-0020 model.',
     [{'species': 'A', 'pos': [5.0, 4.5], 'vel': [0.0, 0.0]}, {'species': 'B', 'pos': [5.0, 5.5], 'vel': [0.0, 0.0]}]),
    (21, 'Review of P-0020 (A-B diagonal, A lower-left, r0 = 1.000 centre (5,5), T = 0.15). Judged error against the P-0020 model.',
     [{'species': 'A', 'pos': [5.0 - 0.5 * C, 5.0 - 0.5 * C], 'vel': [0.0, 0.0]},
      {'species': 'B', 'pos': [5.0 + 0.5 * C, 5.0 + 0.5 * C], 'vel': [0.0, 0.0]}]),
]
for k, purpose, parts in rv:
    write(k, {
        'request_id': RID % k, 'lab': 'lab-keystone', 'account': 'review', 'cites_paper': 'P-0020',
        'purpose': purpose, 'setup': setup(parts, 0.15, 0.0015), 'instruments': ['tracker'],
    })
print('wrote requests 001-024')
