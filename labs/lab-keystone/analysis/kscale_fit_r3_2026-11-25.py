"""Round 3 (2026-11-25): per-run force-scale fits against tracker data, to test the force tables at ~1 percent.

chi2 = sum over samples, particles, coords of (measured - predicted)^2 / 0.05^2 (tracker noise 0.05 per coord,
as stated by the paper claims). The paper's table is multiplied by a scale s (P-0029 and P-0028: one s;
P-0030: separate s_AC, s_CA). The minimum and covariance come from a quadratic fit to a grid of chi2 values.
Run with: python3 -I kscale_fit_r3_2026-11-25.py
"""
import importlib.util, json, math, sys
sys.path.insert(0, '/tmp/npdeps')
import numpy as np

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
SIG = 0.05


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


def chi2(pred, res):
    pmap = {round(s['t'], 9): s for s in pred}
    tot = 0.0; n = 0
    for s in res['samples']:
        t = round(s['t'], 9)
        if t not in pmap:
            continue
        mp = {p['id']: p['pos'] for p in pmap[t]['particles']}
        for p in s['particles']:
            q = mp[p['id']]
            tot += ((p['pos'][0] - q[0]) ** 2 + (p['pos'][1] - q[1]) ** 2) / SIG ** 2
            n += 2
    return tot, n


def fit1(predict_scaled, rids, grid=np.linspace(0.90, 1.10, 21)):
    """One scale parameter, shared by the listed runs."""
    cs = []
    for s in grid:
        c = 0.0
        for rid in rids:
            req, res = run_req(rid)
            c += chi2(predict_scaled(s, req), res)[0]
        cs.append(c)
    cs = np.array(cs)
    x = grid - 1.0
    A = np.vstack([x**2, x, np.ones_like(x)]).T
    a, b, c0 = np.linalg.lstsq(A, cs, rcond=None)[0]
    s0 = 1.0 - b / (2 * a)
    sig = 1.0 / math.sqrt(a)          # delta chi2 = 1
    ndof = 0
    for r in rids:
        req, res = run_req(r)
        ndof += chi2(predict_scaled(1.0, req), res)[1]
    ndof -= 1
    cmin = c0 - b * b / (4 * a)
    return s0, sig, cmin, ndof


def main():
    # P-0029 table, scale on K_TAB (pairs at r0 = 5, 6, 9)
    p29 = load(ROOT + '/papers/P-0029/model.py', 'm29')
    base29 = p29.K_TAB.copy()
    def pred29(s, req):
        p29.K_TAB = base29 * s
        return p29.predict(req['setup'])
    rids29 = ['2026-11-25/r2/lab-keystone/001', '2026-11-25/r2/lab-keystone/003', '2026-11-25/r2/lab-keystone/002']
    print('P-0029 table, scale s (runs 001 r0=5, 003 r0=6, 002 r0=9), per-run and pooled')
    for rid in rids29:
        s0, sig, cmin, ndof = fit1(pred29, [rid])
        print('  %s  s = %.4f +/- %.4f  chi2/dof = %.2f' % (rid.split('/', 1)[1], s0, sig, cmin / ndof))
    s0, sig, cmin, ndof = fit1(pred29, rids29)
    print('  pooled s = %.4f +/- %.4f  chi2/dof = %.2f' % (s0, sig, cmin / ndof))

    # P-0028 table, scale on NODE_K (8-ring, three runs)
    p28 = load(ROOT + '/papers/P-0028/model.py', 'm28')
    base28 = list(p28.NODE_K)
    def pred28(s, req):
        p28.NODE_K = [k * s for k in base28]
        return p28.predict(req['setup'])
    rids28 = ['2026-11-25/r2/lab-keystone/007', '2026-11-25/r2/lab-keystone/008', '2026-11-25/r2/lab-keystone/009']
    print('P-0028 table, scale s (8-ring, runs 007-009 pooled; T = 1)')
    s0, sig, cmin, ndof = fit1(pred28, rids28, grid=np.linspace(0.85, 1.15, 31))
    print('  pooled s = %.4f +/- %.4f  chi2/dof = %.2f' % (s0, sig, cmin / ndof))

    # N=4 square (010 axis, 011 diagonal) with the P-0029 table through the pre-registration integrator
    pre = load(ROOT + '/labs/lab-keystone/analysis/prereg_N4_square_2026-11-25.py', 'pre')
    base_k = pre.K_TAB.copy()
    def pred_n4(s, req):
        pre.K_TAB = base_k * s
        pos0 = [p['pos'] for p in req['setup']['particles']]
        traj, _ = pre.run(pos0)
        return [{'t': t, 'particles': [{'id': i, 'pos': traj[t][i].tolist()} for i in range(len(pos0))]}
                for t in sorted(traj)]
    rids_n4 = ['2026-11-25/r2/lab-keystone/010', '2026-11-25/r2/lab-keystone/011']
    print('N=4 square side 5, pair table scale s (runs 010 axis, 011 diagonal, pooled; T = 2)')
    s0, sig, cmin, ndof = fit1(pred_n4, rids_n4)
    print('  pooled s = %.4f +/- %.4f  chi2/dof = %.2f' % (s0, sig, cmin / ndof))

    # P-0030: separate scales on K_AC and K_CA, runs 004-006 (out-of-sample r0 = 2.75, 3.25, 2.55)
    p30 = load(ROOT + '/papers/P-0030/model.py', 'm30')
    base_ac, base_ca = list(p30.K_AC_NODES), list(p30.K_CA_NODES)
    def pred30(sa, sc, req):
        p30.K_AC_NODES = [k * sa for k in base_ac]
        p30.K_CA_NODES = [k * sc for k in base_ca]
        return p30.predict(req['setup'])
    rids30 = ['2026-11-25/r2/lab-keystone/004', '2026-11-25/r2/lab-keystone/005', '2026-11-25/r2/lab-keystone/006']
    grid = np.linspace(0.92, 1.08, 9)
    rows = []
    for sa in grid:
        for sc in grid:
            c = 0.0
            for rid in rids30:
                req, res = run_req(rid)
                c += chi2(pred30(sa, sc, req), res)[0]
            rows.append((sa, sc, c))
    R = np.array(rows)
    X = R[:, 0] - 1.0; Y = R[:, 1] - 1.0; Cc = R[:, 2]
    M = np.vstack([X**2, Y**2, X*Y, X, Y, np.ones_like(X)]).T
    a11, a22, a12, b1, b2, c0 = np.linalg.lstsq(M, Cc, rcond=None)[0]
    H = np.array([[a11, a12], [a12, a22]])
    d = -np.linalg.solve(2 * H, np.array([b1, b2]))
    cov = np.linalg.inv(H)
    cmin = c0 + 0.5 * np.array([b1, b2]) @ d
    ndof = 3 * 201 * 2 * 2 - 2  # 3 runs x 201 samples x 2 particles x 2 coords
    print('P-0030 nodes (runs 004-006, out of sample): s_AC = %.4f +/- %.4f, s_CA = %.4f +/- %.4f, chi2/dof = %.2f'
          % (1 + d[0], math.sqrt(cov[0, 0]), 1 + d[1], math.sqrt(cov[1, 1]), cmin / ndof))


if __name__ == '__main__':
    main()
