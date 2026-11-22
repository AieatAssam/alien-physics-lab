"""Score research 001-006 (exponent test, model-free) and review 007-009 (P-0016 error).
Setups copied from labs/lab-keystone/analysis/make_requests_2026-11-22.py (requests not on disk in out/).
Run: python3 -I <this file>"""
import importlib.util, json, math

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
L = 10.0
RES = ROOT + '/results/2026-11-22/r1/lab-keystone/%03d.json'


def P(sp, x, y):
    return {'species': sp, 'pos': [x, y], 'vel': [0.0, 0.0]}


def S(parts, T, dt):
    return {'particles': parts, 'duration': T, 'sample_dt': dt}


SETUP = {
    1: S([P('A', 4.0, 4.0), P('A', 4.5, 4.0)], 0.03, 0.0005),
    2: S([P('A', 7.0, 2.0), P('A', 7.0, 2.5)], 0.03, 0.0005),
    3: S([P('A', 4.0, 6.0), P('A', 5.0, 6.0)], 0.1, 0.001),
    4: S([P('A', 7.0, 6.0), P('A', 7.0, 7.0)], 0.1, 0.001),
    5: S([P('A', 2.0, 2.0), P('A', 4.0, 2.0)], 0.3, 0.005),
    6: S([P('A', 8.0, 6.0), P('A', 8.0, 8.0)], 0.3, 0.005),
    7: S([P('A', 4.0, 5.0), P('C', 5.0, 5.0)], 0.6, 0.01),
    8: S([P('C', 2.0, 7.0), P('A', 2.0, 7.9995)], 0.6, 0.01),
    9: S([P('A', 7.0, 3.0), P('C', 7.0 + 1.0005 / math.sqrt(2), 3.0 + 1.0005 / math.sqrt(2))], 0.6, 0.01),
}


def load_model(pid):
    spec = importlib.util.spec_from_file_location('m', ROOT + '/papers/%s/model.py' % pid)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def rmse_error(model, setup, res):
    pred = model.predict(setup)
    pmap = {round(s['t'], 9): s for s in pred}
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
    return math.sqrt(sq / cnt) / L, cnt


def min_sep(setup):
    ps = setup['particles']
    return min(math.dist(ps[i]['pos'], ps[j]['pos']) for i in range(len(ps)) for j in range(i + 1, len(ps)))


def _solve(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [M[r][k] - f * M[c][k] for k in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def accel_at_zero(res, T):
    """Relative acceleration at t=0. Time scaled to u = t/T (conditioning). Model d(u) = sum_k c_k u^k, k=0..4,
    coordinates fitted separately by least squares. At rest, d = (1/2) a_rel t^2 + ..., so a_rel = 2 c2 / T^2.
    Returns (|a_rel(0)|, rms of fit in position units, initial velocity estimate in position/time units)."""
    rows = []
    for s in res['samples']:
        if s['t'] > T + 1e-12:
            continue
        p = {q['id']: q['pos'] for q in s['particles']}
        rows.append((s['t'] / T, [p[1][0] - p[0][0], p[1][1] - p[0][1]]))
    K = 5
    basis = lambda u: [u ** k for k in range(K)]
    G = [[0.0] * K for _ in range(K)]
    for u, _ in rows:
        b = basis(u)
        for i in range(K):
            for j in range(K):
                G[i][j] += b[i] * b[j]
    coefs = []
    for c in range(2):
        g = [0.0] * K
        for u, d in rows:
            b = basis(u)
            for i in range(K):
                g[i] += b[i] * d[c]
        coefs.append(_solve(G, g))
    c2 = [coefs[0][2], coefs[1][2]]
    rss = 0.0
    for u, d in rows:
        b = basis(u)
        for c in range(2):
            rss += (d[c] - sum(coefs[c][k] * b[k] for k in range(K))) ** 2
    rms = math.sqrt(rss / (2 * len(rows)))
    a_rel = 2.0 * math.hypot(*c2) / T ** 2
    v0 = [coefs[0][1] / T, coefs[1][1] / T]
    return a_rel, v0, rms


def main():
    print('== Review runs 007-009 vs P-0016 model (judge error = RMSE / L)')
    m16 = load_model('P-0016')
    for n in (7, 8, 9):
        res = json.load(open(RES % n))
        err, cnt = rmse_error(m16, SETUP[n], res)
        print('007-009: run %03d status=%s sep=%.5f T=%.2f error=%.5f (points %d)'
              % (n, res['status'], min_sep(SETUP[n]), SETUP[n]['duration'], err, cnt))

    print('== Exponent test runs 001-006 (model-free relative acceleration at t=0)')
    for n in range(1, 7):
        res = json.load(open(RES % n))
        s = SETUP[n]
        a0, v0, rms = accel_at_zero(res, s['duration'])
        print('%03d r0=%.2f T=%.2f  |a_rel(0)|=%.4f  fitted v0=(%.4f, %.4f)  fit rms=%.5f'
              % (n, min_sep(s), s['duration'], a0, v0[0], v0[1], rms))


if __name__ == '__main__':
    main()
