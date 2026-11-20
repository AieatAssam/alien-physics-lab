"""Generate lab-keystone round-1 requests for 2026-11-20 (research 001-010, review 011-022)."""
import json, math, os
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
OUT = ROOT + '/out/requests/2026-11-20/r1/lab-keystone'
os.makedirs(OUT, exist_ok=True)
D = '2026-11-20'
def p(s, x, y, vx=0.0, vy=0.0): return {'species': s, 'pos': [round(x, 6), round(y, 6)], 'vel': [vx, vy]}
def req(n, account, purpose, parts, T, dt, cites=None):
    r = {'request_id': '%s/r1/lab-keystone/%03d' % (D, n), 'lab': 'lab-keystone', 'account': account,
         'purpose': purpose[:500], 'setup': {'particles': parts, 'duration': T, 'sample_dt': dt},
         'instruments': ['tracker', 'census']}
    if cites: r['cites_paper'] = cites
    json.dump(r, open('%s/%03d.json' % (OUT, n), 'w'), indent=2)
s3 = math.sqrt(3) / 2
R5 = 5 / (2 * math.sin(math.radians(36)))
pent = [p(sp, 5 + R5 * math.cos(math.radians(90 + 72 * k)), 5 + R5 * math.sin(math.radians(90 + 72 * k)))
        for k, sp in enumerate('ABCAB')]
H = 5 * s3  # triangle height for side 5
dd = 5 / math.sqrt(2)  # diagonal offset for separation 5
reqs = [
 (1, 'research', 'Radial factor at separation 7, B-B. Pre-registered: K_B(B) = 5.30 from the P-0009 candidate (shared factor 0.866 at r=7). Tests the far-field factor where no B-B data exist.', [p('B', 1.5, 5.0), p('B', 8.5, 5.0)], 6.0, 0.05),
 (2, 'research', 'Radial factor at separation 7, C-C. Pre-registered: K_C(C) = 10.14 (P-0009). Lab-a P-0006 c1 reports 10.44 at separation 7 (T=4); the two differ by 3%, so this run tests it.', [p('C', 1.5, 5.0), p('C', 8.5, 5.0)], 6.0, 0.05),
 (3, 'research', 'Radial factor at separation 7, A-A. Pre-registered: K_A(A) = 15.59 (P-0009, 18.0 x 0.866), T=4 (T=6 would bring the pair to 0.5 apart, near contact). Completes the separation-7 row for same-species A.', [p('A', 1.5, 5.0), p('A', 8.5, 5.0)], 4.0, 0.05),
 (4, 'research', 'Radial factor at separation 7, A-B. Pre-registered: K_A(B) = 7.78 and K_B(A) = 10.69 (P-0009, C-free so no C factor).', [p('A', 1.5, 5.0), p('B', 8.5, 5.0)], 6.0, 0.05),
 (5, 'research', 'Radial factor at separation 7, B-C (C factor 0.9475). Pre-registered: K_B(C) = -5.00 and K_C(B) = -8.69 (P-0009).', [p('B', 1.5, 5.0), p('C', 8.5, 5.0)], 6.0, 0.05),
 (6, 'research', 'Radial factor at separation 6, C-C, T=4. Pre-registered: K_C(C) = 11.21 (P-0009). Fills the separation-6 row for C-C; the factor set by BC at 6 implies a C effect.', [p('C', 2.0, 5.0), p('C', 8.0, 5.0)], 4.0, 0.05),
 (7, 'research', 'Radial factor at separation 6, A-A, T=3. Pre-registered: K_A(A) = 17.24 (P-0009, 18.0 x 0.958), T=3 (T=4 approaches within 1.2). Fills the separation-6 row for A-A.', [p('A', 2.0, 5.0), p('A', 8.0, 5.0)], 3.0, 0.05),
 (8, 'research', 'N=5 additivity: pentagon of side 5 (species A, B, C, A, B), at rest, T=2. Pairwise sum with P-0005 at side 5 and the P-0009 radial factor at the diagonal 8.09. Tests additivity beyond N=4; see predictions_round1_2026-11-20.json.', pent, 2.0, 0.02),
 (9, 'research', 'Close range, A-C repulsion at separation 1.5, T=1. Pure r^-2.5 law with P-0005 coefficients predicted; a deviation at short range tests whether the power law holds below 3.', [p('A', 4.25, 5.0), p('C', 5.75, 5.0)], 1.0, 0.01),
 (10, 'research', 'Close range, B-C repulsion at separation 1.5, T=1. Pure r^-2.5 law with P-0005 coefficients predicted.', [p('B', 4.25, 5.0), p('C', 5.75, 5.0)], 1.0, 0.01),
]
for n, acc, purpose, parts, T, dt in reqs: req(n, acc, purpose, parts, T, dt)
# review-account requests (cite paper), within each claim's stated domain
cx, cy = 5.0, 5.0
ab_h = [p('A', 2.5, 5.0), p('B', 7.5, 5.0)]
ab_v = [p('A', 5.0, 2.5), p('B', 5.0, 7.5)]
ab_d = [p('A', 2.5, 2.5), p('B', 2.5 + dd, 2.5 + dd)]
ac_h = [p('A', 2.5, 5.0), p('C', 7.5, 5.0)]
ac_v = [p('A', 5.0, 2.5), p('C', 5.0, 7.5)]
ac_d = [p('A', 2.5, 2.5), p('C', 2.5 + dd, 2.5 + dd)]
rv = [
 (11, 'P-0004 c1 test: A-B at separation 5, horizontal, at rest, T=2. Replicates the A-B pair coefficients (P-0004 c1) in a new orientation.', ab_h, 2.0, 0.02, 'P-0004'),
 (12, 'P-0004 c1 test: A-B at separation 5, vertical orientation, at rest, T=2.', ab_v, 2.0, 0.02, 'P-0004'),
 (13, 'P-0004 c1 test: A-B at separation 5, diagonal orientation, at rest, T=2.', ab_d, 2.0, 0.02, 'P-0004'),
 (14, 'P-0004 c2 test: A-C at separation 5, horizontal, at rest, T=2. P-0004 c2 is a single-run claim; this is the repeat it asked for.', ac_h, 2.0, 0.02, 'P-0004'),
 (15, 'P-0004 c2 test: A-C at separation 5, vertical orientation, at rest, T=2.', ac_v, 2.0, 0.02, 'P-0004'),
 (16, 'P-0004 c2 test: A-C at separation 5, diagonal orientation, at rest, T=2.', ac_d, 2.0, 0.02, 'P-0004'),
 (17, 'P-0007 c1 narrowing test: A, B, C equilateral triangle at side 5.0 (the only side P-0007 model.py accepts), at rest, T=1.5.', [p('A', 2.5, 3.0), p('B', 7.5, 3.0), p('C', 5.0, 3.0 + H)], 1.5, 0.03, 'P-0007'),
 (18, 'P-0007 c1 narrowing test: B, C, A ordering on an equilateral triangle of side 5.0, at rest, T=1.5.', [p('B', 2.5, 3.0), p('C', 7.5, 3.0), p('A', 5.0, 3.0 + H)], 1.5, 0.03, 'P-0007'),
 (19, 'P-0007 c1 narrowing test: C, A, B ordering on an equilateral triangle of side 5.0, at rest, T=1.5.', [p('C', 2.5, 3.0), p('A', 7.5, 3.0), p('B', 5.0, 3.0 + H)], 1.5, 0.03, 'P-0007'),
 (20, 'P-0007 c2 narrowing test: three species-A particles on an equilateral triangle of side 5.0, at rest, T=1.5 (the only side P-0007 model.py accepts for AAA).', [p('A', 2.5, 2.0), p('A', 7.5, 2.0), p('A', 5.0, 2.0 + H)], 1.5, 0.03, 'P-0007'),
 (21, 'P-0007 c2 narrowing test: AAA equilateral side 5.0, second placement, at rest, T=1.5.', [p('A', 5.0, 2.0), p('A', 2.5, 2.0 + H), p('A', 7.5, 2.0 + H)], 1.5, 0.03, 'P-0007'),
 (22, 'P-0007 c2 narrowing test: AAA equilateral side 5.0, third placement, at rest, T=1.5.', [p('A', 2.5, 6.0), p('A', 7.5, 6.0), p('A', 5.0, 6.0 + H)], 1.5, 0.03, 'P-0007'),
]
for n, purpose, parts, T, dt, paper in rv: req(n, 'review', purpose, parts, T, dt, cites=paper)
print('written', len(os.listdir(OUT)))
