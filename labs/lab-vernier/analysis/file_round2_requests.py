"""Write round-2 request files for lab-vernier (2026-11-20). Run with python3 -I. Writes only under out/requests."""
import json, math, os
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab/out/requests/2026-11-20/r2/lab-vernier'
os.makedirs(ROOT, exist_ok=True)
R5 = 5 / math.sqrt(3)

def cen(cx, cy, deg):
    return [[round(cx + R5 * math.cos(math.radians(a)), 4), round(cy + R5 * math.sin(math.radians(a)), 4)] for a in deg]

def parts(spec):
    return [{'species': s, 'pos': p, 'vel': [0.0, 0.0]} for s, p in spec]

tri1 = [(['B', 'C', 'C'][0], [2.5, 2.5]), ('C', [7.5, 2.5]), ('C', [5.0, 6.8301])]
u2 = cen(5.0, 4.5, [90, 210, 330])
u3 = cen(5.0, 5.0, [45, 165, 285])
reqs = [
 ('001', 'review', 'P-0010', 'Out-of-sample test of P-0010 far-field G(r): two A at rest, initial separation 9.0 (the top of its range), T=6, tracker. Pre-registered: error at or below 0.03 is replication; above 0.03 is falsification.',
  parts([('A', [0.5, 5.0]), ('A', [9.5, 5.0])]), 6.0, 0.01),
 ('002', 'review', 'P-0010', 'Out-of-sample test of P-0010 with a C pair (S_C factor): two C at rest, initial separation 7.0, T=6, tracker. Pre-registered bar: error at or below 0.03.',
  parts([('C', [1.5, 5.0]), ('C', [8.5, 5.0])]), 6.0, 0.01),
 ('003', 'review', 'P-0010', 'Out-of-sample test of P-0010 with a repulsive B-C pair at initial separation 8.0, T=6, tracker. Pre-registered bar: error at or below 0.03.',
  parts([('B', [1.5, 5.0]), ('C', [9.5, 5.0])]), 6.0, 0.01),
 ('004', 'review', 'P-0009', 'Replication of P-0009 (B, C, C equilateral triangle, side 5, at rest, T=2), run 1 of 3, with B at (2.5,2.5), C at (7.5,2.5), C at (5,6.8301). Bar: error at or below 0.03.',
  parts([('B', [2.5, 2.5]), ('C', [7.5, 2.5]), ('C', [5.0, 6.8301])]), 2.0, 0.01),
 ('005', 'review', 'P-0009', 'Replication of P-0009 (B, C, C triangle, side 5), run 2 of 3: rotated centre (5, 4.5), B at the lower-left vertex, C at the apex and lower-right. Bar: error at or below 0.03.',
  parts([('C', u2[0]), ('B', u2[1]), ('C', u2[2])]), 2.0, 0.01),
 ('006', 'review', 'P-0009', 'Replication of P-0009 (B, C, C triangle, side 5), run 3 of 3: centre (5, 5), rotated by 45 degrees, B at the lower-right vertex. Bar: error at or below 0.03.',
  parts([('C', u3[0]), ('C', u3[1]), ('B', u3[2])]), 2.0, 0.01),
 ('007', 'review', 'P-0003', 'Replication of P-0003 (two A at rest) at separation 5.0, the middle of its range 3 to 6, to complete three in-domain pair runs at r = 4, 5, 6. Bar: error at or below 0.03.',
  parts([('A', [2.5, 5.0]), ('A', [7.5, 5.0])]), 2.0, 0.01),
 ('008', 'research', None, 'Close-range probe (open bounty close-BB): two B at rest, separation 1.0, T=0.6, tracker. Exploratory: first data at separation 1.',
  parts([('B', [4.5, 5.0]), ('B', [5.5, 5.0])]), 0.6, 0.003),
 ('009', 'research', None, 'Close-range probe (open bounty close-AB): A at rest at (4.5,5.0), B at rest at (5.5,5.0), separation 1.0, T=0.6, tracker. Exploratory.',
  parts([('A', [4.5, 5.0]), ('B', [5.5, 5.0])]), 0.6, 0.003),
 ('010', 'research', None, 'Close-range probe (open bounty close-BC): B at rest at (4.5,5.0), C at rest at (5.5,5.0), separation 1.0, T=0.6, tracker. Exploratory.',
  parts([('B', [4.5, 5.0]), ('C', [5.5, 5.0])]), 0.6, 0.003),
]
for num, acct, cites, purpose, p, dur, dt in reqs:
    req = {'request_id': '2026-11-20/r2/lab-vernier/' + num, 'lab': 'lab-vernier', 'account': acct,
           'purpose': purpose, 'setup': {'particles': p, 'duration': dur, 'sample_dt': dt}, 'instruments': ['tracker']}
    if cites:
        req['cites_paper'] = cites
    with open(os.path.join(ROOT, num + '.json'), 'w') as f:
        json.dump(req, f, indent=2)
        f.write('\n')
    N = len(p)
    cost = 1 + 0.02 * N * dur
    print(num, acct, cites, N, dur, round(cost, 3), 'samples', round(dur / dt) + 1)
