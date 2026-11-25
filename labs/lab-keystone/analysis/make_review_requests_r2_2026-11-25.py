"""Round 2 (2026-11-25) requests from lab-keystone. Writes out/requests/2026-11-25/r2/lab-keystone/NNN.json.

Review account (cites_paper), each run chosen to sit inside the target claim's domain AND window, so the paper's
predict() accepts it (checked below before writing):
  001-003  P-0029 (lab-a, A-A pair, r0 in [5,9]): edges and interior, T at the claim's window.
  004-006  P-0030 (lab-vernier, A-C pair, r0 in [2.5,3.5]): out-of-sample separations and orientation, T = 2.
  007-009  P-0028 (lab-a, A-A crowd, N <= 8, pairs in [3,9], T <= 1): N = 8 rings, tighter than P-0028's ring,
           so pairs fall below 3 during the run (the regime P-0028 says is untested).
Research account: 010-011, N = 4 square, side 5, T = 2 (synthesis gap between N = 2 and N = 8). Pre-registered
prediction: analysis/prereg_N4_square_2026-11-25.json.
"""
import json, math, os, sys
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/tools')
from domain import in_domain  # noqa: E402

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
DAY, RND, LAB = '2026-11-25', 'r2', 'lab-keystone'
OUT = os.path.join(ROOT, 'out/requests', DAY, RND, LAB)
L = 10.0


def load_model(pid):
    import importlib.util
    spec = importlib.util.spec_from_file_location('m_' + pid.replace('-', '_'), '%s/papers/%s/model.py' % (ROOT, pid))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def part(sp, x, y):
    return {'species': sp, 'pos': [round(x, 6), round(y, 6)], 'vel': [0.0, 0.0]}


def pair_h(sp1, sp2, r0, cx=5.0, cy=5.0):
    return [part(sp1, cx - r0 / 2, cy), part(sp2, cx + r0 / 2, cy)]


def pair_d(sp1, sp2, r0, cx=5.0, cy=5.0):
    c = r0 / (2 * math.sqrt(2))
    return [part(sp1, cx - c, cy - c), part(sp2, cx + c, cy + c)]


def pair_v(sp1, sp2, r0, cx=5.0, cy=5.0):
    return [part(sp1, cx, cy - r0 / 2), part(sp2, cx, cy + r0 / 2)]


def ring(n, R, phi, cx=5.0, cy=5.0):
    return [part('A', cx + R * math.cos(2 * math.pi * k / n + phi), cy + R * math.sin(2 * math.pi * k / n + phi))
            for k in range(n)]


def square(side, cx=5.0, cy=5.0, rot=0.0):
    h = side / 2
    pts = [(-h, -h), (h, -h), (h, h), (-h, h)]
    out = []
    for x, y in pts:
        xr = x * math.cos(rot) - y * math.sin(rot)
        yr = x * math.sin(rot) + y * math.cos(rot)
        out.append(part('A', cx + xr, cy + yr))
    return out


def req(n, purpose, particles, T, account, cites=None):
    r = {
        'request_id': '%s/%s/%s/%s' % (DAY, RND, LAB, n),
        'lab': LAB,
        'account': account,
        'purpose': purpose,
        'setup': {'particles': particles, 'duration': T, 'sample_dt': 0.01},
        'instruments': ['tracker'],
    }
    if cites:
        r['cites_paper'] = cites
    return r


# (id, claim paper, claim domain key, particles, T, account, purpose)
REVIEW = [
    ('001', 'P-0029', pair_h('A', 'A', 5.0), 2.0,
     'P-0029 lower edge: A-A r0 = 5.0 horizontal, T = 2.0 (window for r0 < 7).'),
    ('002', 'P-0029', pair_h('A', 'A', 9.0), 3.0,
     'P-0029 upper edge: A-A r0 = 9.0 horizontal (exact separation; diagonal rounding would fall outside [5,9]), T = 3.0 (window for r0 >= 7).'),
    ('003', 'P-0029', pair_v('A', 'A', 6.0), 2.0,
     'P-0029 interior: A-A r0 = 6.0 vertical, T = 2.0, orientation not used by the P-0029 evidence.'),
    ('004', 'P-0030', pair_h('A', 'C', 2.75), 2.0,
     'P-0030 out-of-sample separation: A-C r0 = 2.75 horizontal, T = 2.0 (nodes at 2.5, 3.0, 3.5 only).'),
    ('005', 'P-0030', pair_d('A', 'C', 3.25), 2.0,
     'P-0030 out-of-sample separation: A-C r0 = 3.25 diagonal, T = 2.0.'),
    ('006', 'P-0030', pair_d('A', 'C', 2.55), 2.0,
     'P-0030 lower edge, diagonal orientation: A-C r0 = 2.55 (just inside 2.5; exact diagonal 2.5 rounds outside the domain), T = 2.0.'),
    ('007', 'P-0028', ring(8, 4.2, 0.0), 1.0,
     'P-0028 crowd edge: 8 A on a ring of radius 4.2 (adjacent 3.2, diameter 8.4), at rest, T = 1.0; pairs fall below 3 during the run.'),
    ('008', 'P-0028', ring(8, 4.2, math.pi / 8), 1.0,
     'P-0028 crowd edge, orientation replicate: same ring rotated by 22.5 degrees, T = 1.0.'),
    ('009', 'P-0028', ring(8, 4.0, 0.0), 1.0,
     'P-0028 crowd edge: 8 A on a ring of radius 4.0 (adjacent 3.06, diameter 8.0), T = 1.0; tightest ring inside [3,9].'),
]
CLAIM_PAPER = {'P-0029': 'P-0029', 'P-0030': 'P-0030', 'P-0028': 'P-0028'}
SQUARE_RESEARCH = [
    ('010', 'N = 4 square, side 5.0, axis-aligned, T = 2.0 (pre-registered additivity check, research account).', square(5.0, rot=0.0), 2.0),
    ('011', 'N = 4 square, side 5.0, rotated 45 degrees, T = 2.0 (orientation replicate of 010, research account).', square(5.0, rot=math.pi / 4), 2.0),
]


def check_review(n, pid, particles, T):
    m = load_model(pid)
    claim = json.load(open('%s/papers/%s/claim.json' % (ROOT, pid)))
    setup = {'particles': particles, 'duration': T, 'sample_dt': 0.01}
    matched = [c for c in claim['claims'] if in_domain(c['domain'], setup)]
    try:
        m.predict(setup)
        ok = 'predict ok'
    except Exception as e:  # noqa: BLE001
        ok = 'predict REFUSES: %s' % str(e)[:80]
    dmin = min(math.dist(a['pos'], b['pos']) for i, a in enumerate(particles) for b in particles[i + 1:])
    dmax = max(math.dist(a['pos'], b['pos']) for i, a in enumerate(particles) for b in particles[i + 1:])
    return len(matched), ok, dmin, dmax


def main():
    os.makedirs(OUT, exist_ok=True)
    cost_total = 0.0
    for n, pid, particles, T, purpose in REVIEW:
        matched, ok, dmin, dmax = check_review(n, pid, particles, T)
        if matched == 0 or not ok.startswith('predict ok'):
            raise SystemExit('request %s not scoreable for %s: domain matches %d, %s' % (n, pid, matched, ok))
        cost = 1 + 0.02 * len(particles) * T
        cost_total += cost
        print('%s %s N=%d T=%.1f sep=[%.2f,%.2f] cost %.2f  %s' % (n, pid, len(particles), T, dmin, dmax, cost, ok))
        with open(os.path.join(OUT, n + '.json'), 'w') as f:
            json.dump(req(n, purpose, particles, T, 'review', cites=pid), f, indent=2)
            f.write('\n')
    print('review cost total %.2f (allowance 15)' % cost_total)
    for n, purpose, particles, T in SQUARE_RESEARCH:
        cost = 1 + 0.02 * len(particles) * T
        dmin = min(math.dist(a['pos'], b['pos']) for i, a in enumerate(particles) for b in particles[i + 1:])
        dmax = max(math.dist(a['pos'], b['pos']) for i, a in enumerate(particles) for b in particles[i + 1:])
        print('%s research N=%d T=%.1f sep=[%.2f,%.2f] cost %.2f' % (n, len(particles), T, dmin, dmax, cost))
        with open(os.path.join(OUT, n + '.json'), 'w') as f:
            json.dump(req(n, purpose, particles, T, 'research'), f, indent=2)
            f.write('\n')


if __name__ == '__main__':
    main()
