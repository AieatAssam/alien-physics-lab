"""Round-2 scoring (lab-keystone, 2026-11-26): per-run scale fits and node-2.5 fit.

Chi-square uses tracker sigma 0.05 per coordinate. Each paper's own model.py is used, with its domain guard
bypassed only for the fit (the judged metric is computed separately by review_error.py, with the guard on).

  P-0031 (N = 3, 4 A): global scale s on NODE_K, runs 2026-11-26/r1/lab-keystone/001-004.
  P-0034 (A-A, C-C):   global scale s on the node table, runs 009-012 (review account).
  P-0034 node 2.5:     fit of the A node at 2.5 alone (others fixed), research runs 013-015 at r0 = 2.5.
"""
import importlib.util, json, math
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'


def load(pid):
    spec = importlib.util.spec_from_file_location('m_' + pid.replace('-', '_'), ROOT + '/papers/%s/model.py' % pid)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def samples_of(rid):
    day, rnd, lab, n = rid.split('/')
    req = json.load(open('%s/requests/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, n)))
    res = json.load(open('%s/results/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, n)))
    return req, res


def chi2(pred, res):
    pm = {round(p['t'], 9): p for p in pred}
    c = 0.0
    n = 0
    for s in res['samples']:
        t = round(s['t'], 9)
        if t not in pm:
            continue
        for i, p in enumerate(s['particles']):
            if 'pos' not in p:
                continue
            q = pm[t]['particles'][i]['pos']
            c += ((p['pos'][0] - q[0]) ** 2 + (p['pos'][1] - q[1]) ** 2) / 0.05 ** 2
            n += 2
    return c, n


def parabola_min(grid, cs):
    k = min(range(len(cs)), key=lambda i: cs[i])
    k = min(max(k, 1), len(cs) - 2)
    x0, x1, x2 = grid[k - 1], grid[k], grid[k + 1]
    y0, y1, y2 = cs[k - 1], cs[k], cs[k + 1]
    a = ((y2 - y1) / (x2 - x1) - (y1 - y0) / (x1 - x0)) / (x2 - x0)
    b = (y1 - y0) / (x1 - x0) - a * (x0 + x1)
    s0 = -b / (2 * a)
    sig = 1 / math.sqrt(a)
    cmin = y1 - a * (x1 - s0) ** 2
    return s0, sig, cmin


def scan(rid, pred_fn, grid):
    req, res = samples_of(rid)
    cs = []
    n = 0
    for s in grid:
        pred = pred_fn(req['setup'], s)
        c, n = chi2(pred, res)
        cs.append(c)
    s0, sig, cmin = parabola_min(grid, cs)
    return s0, sig, cmin / max(n - 1, 1), n


# --- P-0031: global scale on the P-0027 table (N = 3, 4)
m31 = load('P-0031')
base31 = list(m31.NODE_K)


def pred31(setup, s):
    m31.NODE_K = [k * s for k in base31]
    m31.R_LO, m31.R_HI, m31.N_MAX, m31.T_MAX = 0, 100, 16, 100
    return m31.predict(setup)


grid = [0.97 + 0.01 * k for k in range(7)]
for rid in ['2026-11-26/r1/lab-keystone/%03d' % i for i in range(1, 5)]:
    s0, sig, rchi, n = scan(rid, pred31, grid)
    print('P-0031 %s  s = %.4f +/- %.4f  chi2/dof = %.2f  (n = %d)' % (rid, s0, sig, rchi, n))

# --- P-0034: global scale on both node tables (A-A and C-C), review runs 009-012
m34 = load('P-0034')
base34 = {k: list(v) for k, v in m34.NODE_K.items()}


def pred34(setup, s, species_scale=None):
    m34.NODE_K = {k: [x * s for x in v] for k, v in base34.items()}
    m34.R_LO, m34.R_HI, m34.T_MAX = 0, 100, 100
    return m34.predict(setup)


for rid in ['2026-11-26/r1/lab-keystone/%03d' % i for i in range(9, 13)]:
    s0, sig, rchi, n = scan(rid, pred34, grid)
    print('P-0034 %s  s = %.4f +/- %.4f  chi2/dof = %.2f  (n = %d)' % (rid, s0, sig, rchi, n))


# --- P-0034 node at 2.5: fit the A (or C) node value at r = 2.5, other nodes fixed, research runs 013-015
def pred_node(species, setup, k25):
    m34.NODE_K = {k: list(v) for k, v in base34.items()}
    m34.NODE_K[species][0] = k25
    m34.R_LO, m34.R_HI, m34.T_MAX = 0, 100, 100
    return m34.predict(setup)


for rid, sp in [('2026-11-26/r1/lab-keystone/013', 'A'), ('2026-11-26/r1/lab-keystone/015', 'A'),
                ('2026-11-26/r1/lab-keystone/014', 'C')]:
    base = base34[sp][0]
    grid25 = [base * (0.94 + 0.01 * k) for k in range(13)]
    req, res = samples_of(rid)
    cs = [chi2(pred_node(sp, req['setup'], g), res)[0] for g in grid25]
    n = chi2(pred_node(sp, req['setup'], base), res)[1]
    k25, sig, cmin = parabola_min(grid25, cs)
    print('node2.5 %s %s  K(2.5) fit = %.3f +/- %.3f  table node = %.3f  ratio = %.4f +/- %.4f  chi2/dof = %.2f (n = %d)'
          % (rid, sp, k25, sig, base, k25 / base, sig / base, cmin / max(n - 1, 1), n))
