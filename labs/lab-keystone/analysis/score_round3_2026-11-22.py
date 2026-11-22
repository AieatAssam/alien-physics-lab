"""Round 3 scoring (lab-keystone, 2026-11-22).
(a) Review runs: judged error (RMSE/L of paper model vs measured positions) for P-0019 (007-009) and P-0021 (010-012),
    plus exact in-domain check against each claim's domain (tools/domain.py logic, lo <= d <= hi).
(b) Exponent test: pooled radial fits (q'' = -g/q^P, P = 2.5 shape) per r0 group across round 1 and round 2 A-A runs,
    with a(r0) = g/r0^2.5 and the ratios a(1)/a(2) and a(0.5)/a(1). Pooling is within r0 group only.
Run: python3 -I <this file>
"""
import importlib.util, json, math, os

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
L = 10.0


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


DOM = load(ROOT + '/tools/domain.py', 'dom')


def req(rnd, n):
    return json.load(open(ROOT + '/requests/2026-11-22/r%d/lab-keystone/%03d.json' % (rnd, n)))


def res(rnd, n):
    return json.load(open(ROOT + '/results/2026-11-22/r%d/lab-keystone/%03d.json' % (rnd, n)))


def rmse_error(model, setup, result):
    pred = model.predict(setup)
    pmap = {round(s['t'], 9): s for s in pred}
    sq = cnt = 0
    for s in result['samples']:
        t = round(s['t'], 9)
        if t not in pmap:
            continue
        mp = {p['id']: p['pos'] for p in pmap[t]['particles']}
        for p in s['particles']:
            q = mp[p['id']]
            sq += (p['pos'][0] - q[0]) ** 2 + (p['pos'][1] - q[1]) ** 2
            cnt += 2
    return math.sqrt(sq / cnt) / L, cnt


def review_part():
    for pid, runs in (('P-0019', (7, 8, 9)), ('P-0021', (10, 11, 12))):
        claim = json.load(open(ROOT + '/papers/%s/claim.json' % pid))
        dom = claim['claims'][0]['domain']
        pe = claim['claims'][0]['predicted_error']
        model = load(ROOT + '/papers/%s/model.py' % pid, 'm' + pid.replace('-', ''))
        print('== %s predicted_error=%.4f bar(3x)=%.4f domain=%s' % (pid, pe, 3 * pe, dom))
        for n in runs:
            rq = req(2, n)
            rs = res(2, n)
            inside = DOM.in_domain(dom, rq['setup'])
            seps = [math.dist(rq['setup']['particles'][0]['pos'], rq['setup']['particles'][1]['pos'])]
            err, cnt = rmse_error(model, rq['setup'], rs)
            try:
                err_s = '%.5f' % err
            except Exception:
                err_s = str(err)
            print('  r2/%03d status=%s account=%s in_domain=%s sep0=%.6f T=%.2f dt=%.4f error=%.5f pass=%s points=%d'
                  % (n, rs['status'], rq['account'], inside, seps[0], rq['setup']['duration'],
                     rq['setup']['sample_dt'], err, (inside and err <= 3 * pe), cnt))


def exp_part():
    E = load(ROOT + '/labs/lab-keystone/analysis/exponent_fit_2026-11-22.py', 'ef')
    # reuse sim/rss/best_g from the round-1 fitter (radial model, RK4 with dt/5)
    def run_from(rnd, n):
        rq = req(rnd, n)
        rs = res(rnd, n)
        ps = rq['setup']['particles']
        r0 = math.dist(ps[0]['pos'], ps[1]['pos'])
        T, dt = rq['setup']['duration'], rq['setup']['sample_dt']
        # Project the noisy relative vector onto the initial axis (linear in noise, unbiased), not the norm
        # (the norm of a noisy vector is biased upward by about s^2/(2r) at small r).
        u0 = [(ps[1]['pos'][k] - ps[0]['pos'][k]) / r0 for k in range(2)]
        pts = []
        for s in rs['samples']:
            p = {q['id']: q['pos'] for q in s['particles']}
            d = [p[1][k] - p[0][k] for k in range(2)]
            pts.append((round(s['t'], 9), d[0] * u0[0] + d[1] * u0[1]))
        return (T, dt, r0, pts)
    groups = {}
    for rnd, ns in ((1, range(1, 7)), (2, range(1, 7))):
        for n in ns:
            r = run_from(rnd, n)
            groups.setdefault(round(r[2], 3), []).append((rnd, n, r))
    out = {}
    for r0 in sorted(groups):
        runs = [g[2] for g in groups[r0]]
        ids = ['r%d/%03d' % (g[0], g[1]) for g in groups[r0]]
        g_best, rms = E.best_g(runs, 2.5, 1.0, 400.0, ng=241)
        N = sum(len(r[3]) for r in runs)
        lo = hi = g_best
        step = g_best * 0.002
        g = g_best
        while True:
            g -= step
            if E.rss(runs, g, 2.5)[0] ** 2 > rms ** 2 * (1 + 1.0 / N):
                lo = g
                break
        g = g_best
        while True:
            g += step
            if E.rss(runs, g, 2.5)[0] ** 2 > rms ** 2 * (1 + 1.0 / N):
                hi = g
                break
        a = g_best / r0 ** 2.5
        sa = a * (hi - lo) / 2 / g_best
        out[r0] = (a, sa)
        print('r0=%.3f runs=%s g=%.2f [%.2f, %.2f] a=%.2f +/- %.2f rms=%.4f N=%d'
              % (r0, ids, g_best, lo, hi, a, sa, rms, N))
    for a_r, b_r in ((0.5, 1.0), (1.0, 2.0)):
        ka = [k for k in out if abs(k - a_r) < 1e-6]
        kb = [k for k in out if abs(k - b_r) < 1e-6]
        if ka and kb:
            a1, s1 = out[ka[0]]
            a2, s2 = out[kb[0]]
            rat = a1 / a2
            print('a(%.1f)/a(%.1f) = %.2f +/- %.2f  (P=2.5 -> %.2f; local 1.9 -> %.2f)'
                  % (a_r, b_r, rat, rat * math.hypot(s1 / a1, s2 / a2), 2 ** 2.5 if b_r == 2 * a_r else (b_r / a_r) ** 2.5,
                     (b_r / a_r) ** 1.9))


if __name__ == '__main__':
    review_part()
    exp_part()
