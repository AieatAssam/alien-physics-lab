"""Round 1 (2026-11-26) requests for lab-keystone.
Review-account runs (cites papers P-0031, P-0032, P-0034) and research runs.
Every review layout is checked against the cited paper's predict() domain guard before filing.
Run: python3 -I make_requests_r1_2026-11-26.py  (writes out/requests/2026-11-26/r1/lab-keystone/NNN.json)
"""
import importlib.util, json, math, os, random

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
OUT = ROOT + '/out/requests/2026-11-26/r1/lab-keystone'
RID = '2026-11-26/r1/lab-keystone/%03d'


def load(pid):
    spec = importlib.util.spec_from_file_location('m_' + pid.replace('-', '_'), ROOT + '/papers/%s/model.py' % pid)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def setup(points, T, dt):
    return {'particles': [{'species': sp, 'pos': [float(x), float(y)], 'vel': [0.0, 0.0]} for sp, (x, y) in points],
            'duration': float(T), 'sample_dt': float(dt)}


def cost(n, T):
    return 1 + 0.02 * n * T


# --- asymmetric N = 4 layout with pair distances spanning the P-0031 edges (5.0 and ~7.09), found by fixed-seed search
def find_quad():
    """Asymmetric N = 4 layout inside the P-0031 window. Four points in the plane have max/min pair ratio >= sqrt(2),
    so any N = 4 layout with every pair in [5.0, 7.1] is a near-square (window ratio 1.42). Start from a square of
    side 5.012 (diagonal 7.089) and perturb each corner by up to 0.002 with a fixed seed; keep the set if every pair
    is in [5.0, 7.09] (a perturbed square has no exact symmetry)."""
    rng = random.Random(20261126)
    base = [(2.0, 2.0), (7.012, 2.0), (7.012, 7.012), (2.0, 7.012)]
    for _ in range(200_000):
        pts = [(x + rng.uniform(-0.002, 0.002), y + rng.uniform(-0.002, 0.002)) for x, y in base]
        d = [math.dist(pts[a], pts[b]) for a in range(4) for b in range(a + 1, 4)]
        if not (5.0 < min(d) and max(d) <= 7.09):
            continue
        return [(round(x, 4), round(y, 4)) for x, y in pts]
    raise RuntimeError('no quad found')


def tri_from_sides(a, b, c, origin=(2.0, 2.0)):
    """Triangle with side lengths |P0P1|=a, |P0P2|=b, |P1P2|=c, P0 at origin, P1 on the x axis."""
    x0, y0 = origin
    x = (a * a + b * b - c * c) / (2 * a)
    y = math.sqrt(b * b - x * x)
    return [(x0, y0), (x0 + a, y0), (x0 + x, y0 + y)]


reqs = []   # (purpose, cites, account, species/points, T, dt, points-list)

# ---------- review of P-0031 (lab-b): three or four A, pair distances in [5.0, 7.1], T <= 2
tri = tri_from_sides(5.0, 6.5, 7.09)
reqs.append(('P-0031', 'review', [('A', p) for p in tri], 2.0, 0.001,
             'Review of P-0031 (N=3). Asymmetric scalene triangle, sides 5.0, 6.5, 7.09: both ends of the claim\'s pair range '
             'with no symmetry. Tracker. T=2.0.'))
rect = [(2.0, 2.0), (7.0, 2.0), (7.0, 7.03), (2.0, 7.03)]
reqs.append(('P-0031', 'review', [('A', p) for p in rect], 2.0, 0.001,
             'Review of P-0031 (N=4). Near-square rectangle 5.0 x 5.03: sides at the 5.0 lower edge, diagonals 7.09 near '
             'the 7.1 upper edge. Tracker. T=2.0.'))
eq = [(5.0, 9.0928), (1.4545, 2.9536), (8.5455, 2.9536)]
reqs.append(('P-0031', 'review', [('A', p) for p in eq], 2.0, 0.001,
             'Review of P-0031 (N=3). Equilateral triangle, side 7.09, centred at (5,5): all three pairs at the upper edge. '
             'Tracker. T=2.0.'))
quad = find_quad()
reqs.append(('P-0031', 'review', [('A', p) for p in quad], 2.0, 0.001,
             'Review of P-0031 (N=4). Asymmetric scalene quadrilateral with pair distances spanning 5.00 to 7.09 (fixed-seed '
             'search). Tests the pair sum off symmetric layouts inside the stated range. Tracker. T=2.0.'))

# ---------- review of P-0032 (lab-c): A-A pair at rest, r0 in [2.0, 2.5], T <= 0.6, both >= 2 from walls
reqs.append(('P-0032', 'review', [('A', (4.0, 5.0)), ('A', (6.0, 5.0))], 0.6, 0.001,
             'Review of P-0032 at the lower edge: A-A at rest, horizontal, separation exactly 2.0, centred. Tracker. T=0.6.'))
reqs.append(('P-0032', 'review', [('A', (3.75, 5.0)), ('A', (6.25, 5.0))], 0.6, 0.001,
             'Review of P-0032 at the upper edge: A-A at rest, horizontal, separation exactly 2.5, centred. Tracker. T=0.6.'))
reqs.append(('P-0032', 'review', [('A', (2.5, 3.0)), ('A', (2.5, 5.25))], 0.6, 0.001,
             'Review of P-0032 off-centre: A-A at rest, vertical, separation 2.25 at x=2.5 (>= 2 from walls). Tracker. T=0.6.'))
reqs.append(('P-0032', 'review', [('A', (2.3, 2.3)), ('A', (4.35, 2.3))], 0.6, 0.001,
             'Review of P-0032 near the lower-left wall band: A-A at rest, horizontal, separation 2.05, both >= 2.3 from walls. '
             'Tracker. T=0.6.'))

# ---------- review of P-0034 (lab-vernier): A-A and C-C at rest, r0 in [3.0, 3.5], T <= 1
reqs.append(('P-0034', 'review', [('A', (3.5, 5.0)), ('A', (6.5, 5.0))], 1.0, 0.001,
             'Review of P-0034 c1 at the lower edge: A-A at rest, horizontal, separation 3.0, centred. Tracker. T=1.0.'))
reqs.append(('P-0034', 'review', [('A', (3.25, 5.0)), ('A', (6.75, 5.0))], 1.0, 0.001,
             'Review of P-0034 c1 at the upper edge: A-A at rest, horizontal, separation 3.5, centred. Tracker. T=1.0.'))
reqs.append(('P-0034', 'review', [('C', (5.0, 3.5)), ('C', (5.0, 6.5))], 1.0, 0.001,
             'Review of P-0034 c2 at the lower edge: C-C at rest, vertical, separation 3.0, centred. Tracker. T=1.0.'))
reqs.append(('P-0034', 'review', [('C', (5.0, 3.25)), ('C', (5.0, 6.75))], 1.0, 0.001,
             'Review of P-0034 c2 at the upper edge: C-C at rest, vertical, separation 3.5, centred. Tracker. T=1.0.'))

# ---------- research (account research): probe the P-0034 node at separation 2.5 (A and C), T = 0.6 (no contact)
# Pre-filing sensitivity (sensitivity_node25_2026-11-26.py): a 5 percent change of the node moves the A-A 2.5 pair by
# about 0.0006 judged RMSE/L at T = 0.6, i.e. about 1 percent per-run scale precision in a tracker scale fit.
research = [
    ([('A', (3.75, 5.0)), ('A', (6.25, 5.0))], 0.6, 0.001,
     'Research: A-A pair at rest, separation 2.5, horizontal, T=0.6. Probes the P-0034 A node at 2.5 (the lower end of the '
     'P-0014 supersession range). Scale fit against the P-0034 table. Tracker.'),
    ([('C', (5.0, 3.75)), ('C', (5.0, 6.25))], 0.6, 0.001,
     'Research: C-C pair at rest, separation 2.5, vertical, T=0.6. Probes the P-0034 C node at 2.5. Tracker.'),
    ([('A', (2.5, 2.5)), ('A', (2.5, 5.0))], 0.6, 0.001,
     'Research: A-A pair at rest, separation 2.5, vertical, off-centre (x=2.5, >= 2.5 from walls). Second orientation '
     'for the A node at 2.5. Tracker.'),
]

os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))

models = {'P-0031': load('P-0031'), 'P-0032': load('P-0032'), 'P-0034': load('P-0034')}
rows = []
idx = 0
for pid, acct, pts, T, dt, purpose in reqs:
    idx += 1
    st = setup(pts, T, dt)
    # domain check via the paper's own predictor (raises when outside its guard)
    models[pid].predict(st)
    body = {'request_id': RID % idx, 'lab': 'lab-keystone', 'account': acct, 'purpose': purpose,
            'cites_paper': pid, 'setup': st, 'instruments': ['tracker']}
    rows.append((idx, pid, len(pts), T, cost(len(pts), T)))
    json.dump(body, open(os.path.join(OUT, '%03d.json' % idx), 'w'), indent=1)
for purpose_pts, T, dt, purpose in research:
    idx += 1
    st = setup(purpose_pts, T, dt)
    body = {'request_id': RID % idx, 'lab': 'lab-keystone', 'account': 'research', 'purpose': purpose,
            'setup': st, 'instruments': ['tracker']}
    rows.append((idx, '-', len(purpose_pts), T, cost(len(purpose_pts), T)))
    json.dump(body, open(os.path.join(OUT, '%03d.json' % idx), 'w'), indent=1)

rev = sum(r[4] for r in rows if r[1] != '-')
res = sum(r[4] for r in rows if r[1] == '-')
for r in rows:
    print(r)
print('review credits %.3f of 15; research credits %.3f of 40' % (rev, res))
print('quad layout', quad)
