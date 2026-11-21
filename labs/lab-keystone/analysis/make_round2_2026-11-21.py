"""Round 2 (2026-11-21) requests for lab-keystone.
Review account (cites the paper, must be in domain): P-0015 (001-003), P-0012 (004-006), P-0013 (007-009).
Research account: AA close-range shape at r = 1.25, 1.5, 1.75, 2.0 (010-013).
Pre-registered predictions printed from each paper's model (reviews) and from the interpolation rule (research).
Run: python3 -B -I make_round2_2026-11-21.py"""
import json, math, os, sys, importlib.util
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
sys.path.insert(0, ROOT + '/tools')
from domain import in_domain
OUT = ROOT + '/out/requests/2026-11-21/r2/lab-keystone'
DAY_RND = '2026-11-21/r2/lab-keystone'


def load_model(pid):
    spec = importlib.util.spec_from_file_location('m_' + pid.replace('-', '_'), '%s/papers/%s/model.py' % (ROOT, pid))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


def P(sp, x, y, vx=0.0, vy=0.0):
    return {"species": sp, "pos": [x, y], "vel": [vx, vy]}


def pair(sp0, sp1, x, y, r, ang_deg=0.0):
    a = math.radians(ang_deg)
    return [P(sp0, x, y), P(sp1, x + r * math.cos(a), y + r * math.sin(a))]


# (n, account, cites, purpose, particles, T, dt, domain (for review runs))
DOM = {
    'P-0015': {"species": ["B", "C"], "r_range": [0.999, 1.001], "max_particles": 2},
    'P-0012': {"species": ["A"], "r_range": [1.0, 1.0], "max_particles": 2},
    'P-0013': {"species": ["A", "C"], "r_range": [1.45, 1.55], "max_particles": 2},
}
BAR = {'P-0015': 0.015, 'P-0012': 0.024, 'P-0013': 0.03}
RUNS = [
    (1, 'review', 'P-0015', 'B-C at r=1.0, T=0.6 (edge of T<=0.6), at rest, horizontal', pair('B', 'C', 3.0, 3.0, 1.0, 0.0), 0.6, 0.02),
    (2, 'review', 'P-0015', 'B-C at r=1.0, T=0.6 (edge), at rest, 135 deg, C first', pair('C', 'B', 6.0, 7.0, 1.0, 135.0), 0.6, 0.02),
    (3, 'review', 'P-0015', 'B-C at r=1.0, T=0.6, at rest, 30 deg', pair('B', 'C', 6.0, 3.0, 1.0, 30.0), 0.6, 0.02),
    (4, 'review', 'P-0012', 'A-A at r=1.0 horizontal at (4,2), T=0.15 (claim limit), at rest', pair('A', 'A', 4.0, 2.0, 1.0, 0.0), 0.15, 0.005),
    (5, 'review', 'P-0012', 'A-A at r=1.0 horizontal at (7,6), T=0.15, at rest', pair('A', 'A', 7.0, 6.0, 1.0, 0.0), 0.15, 0.005),
    (6, 'review', 'P-0012', 'A-A at r=1.0 vertical at (3,8), T=0.15, at rest', pair('A', 'A', 3.0, 7.5, 1.0, 90.0), 0.15, 0.005),
    (7, 'review', 'P-0013', 'A-A at r=1.45 (lower edge of [1.45,1.55]), T=0.4, at rest', pair('A', 'A', 4.0, 4.0, 1.45, 0.0), 0.4, 0.002),
    (8, 'review', 'P-0013', 'A-C at r=1.55 (upper edge), T=0.4, at rest', pair('A', 'C', 6.0, 6.0, 1.55, 45.0), 0.4, 0.002),
    (9, 'review', 'P-0013', 'C-C at r=1.5, T=0.4, at rest, vertical', pair('C', 'C', 5.0, 3.0, 1.5, 90.0), 0.4, 0.002),
    (10, 'research', None, 'A-A at r=1.25, T=0.3, at rest: close-range shape (interpolation test; pre-reg f=0.66, linear between f~0.59 at r=1.0 and f~0.72 at 1.5)', pair('A', 'A', 4.5, 5.0, 1.25, 0.0), 0.3, 0.002),
    (11, 'research', None, 'A-A at r=1.5, T=0.4, at rest: clean replicate of the round-3 refit point (pre-reg f=0.72, +-0.05)', pair('A', 'A', 4.5, 5.0, 1.5, 0.0), 0.4, 0.002),
    (12, 'research', None, 'A-A at r=1.75, T=0.4, at rest: shape (pre-reg f=0.79, linear 1.5 to 2.5; 0.72 if plateau)', pair('A', 'A', 4.5, 5.0, 1.75, 0.0), 0.4, 0.002),
    (13, 'research', None, 'A-A at r=2.0, T=0.4, at rest: shape (pre-reg f=0.85, linear; 0.72 if plateau)', pair('A', 'A', 4.5, 5.0, 2.0, 0.0), 0.4, 0.002),
]
os.makedirs(OUT, exist_ok=True)
total = {'review': 0.0, 'research': 0.0}
for n, acct, pid, note, parts, T, dt in RUNS:
    rid = '2026-11-21/r2/lab-keystone/%03d' % n
    req = {"request_id": rid, "lab": "lab-keystone", "account": acct,
           "purpose": note[:500],
           "setup": {"particles": parts, "duration": T, "sample_dt": dt},
           "instruments": ["tracker"]}
    if acct == 'review':
        req["cites_paper"] = pid
        req["purpose"] = ("Review of %s (%s). Pre-registered: error <= %.3f in-domain counts as replicate." % (pid, note, BAR[pid]))[:500]
        ok = in_domain(DOM[pid], {"particles": parts})
        model = load_model(pid)
        pred = model.predict({"particles": parts, "duration": T, "sample_dt": dt})
        print(rid, pid, 'in_domain=%s' % ok, 'pred end', [p['pos'] for p in pred[-1]['particles']])
        assert ok, rid
    else:
        req["purpose"] = note[:500]
    cost = 1 + 0.02 * len(parts) * T
    total[acct] += cost
    with open(os.path.join(OUT, '%03d.json' % n), 'w') as f:
        json.dump(req, f, indent=2); f.write('\n')
    print(rid, acct, 'cost %.3f' % cost)
print('totals', {k: round(v, 3) for k, v in total.items()})
