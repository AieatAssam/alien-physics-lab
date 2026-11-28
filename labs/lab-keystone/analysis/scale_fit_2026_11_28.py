"""Single-scale fit of the pair-sum K model to tracker runs (lab-keystone, 2026-11-28).

Model: additive pair sum with the P-0029 table (flat clamp below r = 5), P = 2.5, scaled by kscale = s.
Fit: chi2(s) over all particles, samples and coordinates with sigma = 0.05 (tracker noise per coordinate).
Quadratic fit to chi2 on a small grid gives s_hat and sigma_s = 1 / sqrt(a), where a is the quadratic coefficient.
Run with: python3 -I scale_fit_2026_11_28.py  (pairsum module from the same directory is numpy-free).
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pairsum as PS  # noqa: E402  (copy of pairsum_2026_11_28.py)

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
SIGMA = 0.05


def fit(req_path, res_path, grid):
    req = json.load(open(req_path))
    res = json.load(open(res_path))
    ps = req['setup']['particles']
    species = [p['species'] for p in ps]
    pos = [p['pos'] for p in ps]
    vel = [p['vel'] for p in ps]
    T = req['setup']['duration']
    dt = req['setup']['sample_dt']
    samples = [s for s in res['samples'] if s['t'] <= T + 1e-9]

    def chi2(sc):
        traj = PS.simulate(species, pos, vel, T, dt, kscale=sc)
        tmap = {round(i * dt, 9): frame for i, frame in enumerate(traj)}
        c = 0.0; n = 0
        for s in samples:
            t = round(s['t'], 9)
            if t not in tmap: continue
            for p in s['particles']:
                if 'pos' not in p: continue
                q = tmap[t][p['id']]
                c += ((p['pos'][0] - q[0]) ** 2 + (p['pos'][1] - q[1]) ** 2) / SIGMA ** 2
                n += 2
        return c, n

    vals = [chi2(g) for g in grid]
    n = vals[0][1]
    y = [v[0] for v in vals]
    # quadratic least squares y = a g^2 + b g + c on the grid
    xs = grid
    m = len(xs)
    S = [sum(x ** k for x in xs) for k in range(5)]
    # normal equations for [c, b, a]
    A = [[S[0], S[1], S[2]], [S[1], S[2], S[3]], [S[2], S[3], S[4]]]
    B = [sum(y), sum(x * v for x, v in zip(xs, y)), sum(x * x * v for x, v in zip(xs, y))]
    # solve 3x3 by Cramer's rule
    def det3(M):
        return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
                - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    D = det3(A)
    sol = []
    for col in range(3):
        Mc = [row[:] for row in A]
        for r in range(3):
            Mc[r][col] = B[r]
        sol.append(det3(Mc) / D)
    c, b, a = sol
    if a <= 0:
        return dict(s_hat=None, sigma_s=None, chi2_per_dof=None, grid_chi2=list(zip(grid, [v / n for v in y])))
    s_hat = -b / (2 * a)
    sig = 1 / math.sqrt(a)
    chi_min = c + b * s_hat + a * s_hat ** 2
    return dict(s_hat=s_hat, sigma_s=sig, chi2_per_dof=chi_min / (n - 1), grid_chi2=list(zip(grid, [v / n for v in y])))


if __name__ == '__main__':
    # Per-run scale grids. Runs with a close approach (contact) are scanned only where the model stays physical.
    runs = [
        ('2026-11-28/r1/lab-keystone/001', 'A-A r0 4.0 horizontal T 2 (contact by t about 1.6 in model)', [0.98, 0.99, 1.00, 1.005]),
        ('2026-11-28/r1/lab-keystone/002', 'A-A r0 3.5 diagonal T 1 (no contact)', [1.00, 1.02, 1.04, 1.06, 1.08]),
        ('2026-11-27/r2/lab-keystone/001', 'A pentagon side 5 (pair sum)', [0.96, 0.98, 1.00, 1.02, 1.04]),
    ]
    for rid, label, grid in runs:
        day, rnd, lab, nnn = rid.split('/')
        req_p = '%s/requests/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, nnn)
        res_p = '%s/results/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, nnn)
        out = fit(req_p, res_p, grid)
        if out['s_hat'] is None:
            print(rid, label, 'no convex minimum on grid')
        else:
            print(rid, label, 's = %.4f +/- %.4f  chi2/dof = %.2f' % (out['s_hat'], out['sigma_s'], out['chi2_per_dof']))
        print('   chi2/n per grid point:', ' '.join('%.3f:%.3g' % (g, v) for g, v in out['grid_chi2']))
