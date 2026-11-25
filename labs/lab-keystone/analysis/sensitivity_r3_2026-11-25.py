"""Round 3 (2026-11-25) sensitivity of the judge metric for the round-2 review runs.

For each run, RMSE/L of a paper's predict() against the tracker, with the paper's force table scaled by s,
and with the force switched off (null). Tells how far the judged bar (3 x predicted_error) can see a K error.
Run with: python3 -I sensitivity_r3_2026-11-25.py  (numpy must be importable; see /tmp/npdeps note in NOTEBOOK)
"""
import importlib.util, json, math, sys
sys.path.insert(0, '/tmp/npdeps')
import numpy as np

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
L = 10.0


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run_req(rid):
    day, rnd, lab, n = rid.split('/')
    req = json.load(open('%s/requests/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, n)))
    res = json.load(open('%s/results/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, n)))
    return req, res


def judged(pred_samples, res):
    pmap = {round(s['t'], 9): s for s in pred_samples}
    sq = cnt = 0
    for s in res['samples']:
        t = round(s['t'], 9)
        if t not in pmap:
            continue
        mp = {p['id']: p['pos'] for p in pmap[t]['particles']}
        for p in s['particles']:
            q = mp[p['id']]
            sq += (p['pos'][0] - q[0]) ** 2 + (p['pos'][1] - q[1]) ** 2
            cnt += 2
    return math.sqrt(sq / cnt) / L


def sweep(m, setfn, rids, scales):
    out = {}
    for rid in rids:
        req, res = run_req(rid)
        row = {}
        for s in scales:
            setfn(m, s)
            row[s] = judged(m.predict(req['setup']), res)
        row['null'] = None
        setfn(m, 0.0)
        row['null'] = judged(m.predict(req['setup']), res)
        setfn(m, 1.0)
        out[rid] = row
    return out


def show(title, out, scales, bar):
    print(title, '(bar = %.4f)' % bar)
    print('  run         ' + ' '.join('s=%-5s' % s for s in scales) + '  null')
    for rid, row in out.items():
        print('  %-40s ' % rid.split('/', 1)[1] + ' '.join('%.5f' % row[s] for s in scales) + '  %.5f' % row['null'])


SCALES = [0.90, 0.95, 1.00, 1.05, 1.10]

# P-0029: force table K_TAB scaled
p29 = load(ROOT + '/papers/P-0029/model.py', 'm29')
base29 = p29.K_TAB.copy()
def set29(m, s):
    m.K_TAB = base29 * s
show('P-0029 table, r0 5/6/9, scale on K', sweep(p29, set29,
     ['2026-11-25/r2/lab-keystone/001', '2026-11-25/r2/lab-keystone/003', '2026-11-25/r2/lab-keystone/002'], SCALES), SCALES, 0.021)

# P-0028: NODE_K scaled
p28 = load(ROOT + '/papers/P-0028/model.py', 'm28')
base28 = list(p28.NODE_K)
def set28(m, s):
    m.NODE_K = [k * s for k in base28]
show('P-0028 table, 8-ring, scale on K', sweep(p28, set28,
     ['2026-11-25/r2/lab-keystone/007', '2026-11-25/r2/lab-keystone/008', '2026-11-25/r2/lab-keystone/009'], SCALES), SCALES, 0.021)

# P-0030: K_AC and K_CA nodes scaled; plus P-0005 constant alternative
p30 = load(ROOT + '/papers/P-0030/model.py', 'm30')
base_ac, base_ca = list(p30.K_AC_NODES), list(p30.K_CA_NODES)
def set30(m, s):
    m.K_AC_NODES = [k * s for k in base_ac]
    m.K_CA_NODES = [k * s for k in base_ca]
show('P-0030 nodes, r0 2.55/2.75/3.25, scale on K', sweep(p30, set30,
     ['2026-11-25/r2/lab-keystone/004', '2026-11-25/r2/lab-keystone/005', '2026-11-25/r2/lab-keystone/006'], SCALES), SCALES, 0.024)

# P-0005 separation-5 constants (K_AC = -8.77, K_CA = -21.25) as a flat alternative, through P-0030's integrator
def set30_p5(m, s):
    m.K_AC_NODES = [-8.77 * s] * 3
    m.K_CA_NODES = [-21.25 * s] * 3
show('P-0030 integrator with P-0005 flat K (s scales it)', sweep(p30, set30_p5,
     ['2026-11-25/r2/lab-keystone/004', '2026-11-25/r2/lab-keystone/005', '2026-11-25/r2/lab-keystone/006'], SCALES), SCALES, 0.024)
