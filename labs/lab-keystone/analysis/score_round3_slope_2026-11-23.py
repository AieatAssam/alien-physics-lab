"""Pre-registered round-3 slope analysis (lab-keystone), written 2026-11-23 from the rule in NOTEBOOK 2026-11-22.
Per radius r (pooled over orientations): fit g with the P = 2.5 shape, a(r) = g / r^2.5 with 1-sigma (delta-rms rule).
Primary: weighted LS slope s of log a vs log r over the radii. Reject P=2.5 if |s+2.5| > 3 sigma_s.
Isotropy: per-orientation a vs pooled a, must be within 2 sigma. Shape: free-P fit at r = 2.5, 3.0 (T = 0.6).
Run: python3 -I <this file>
"""
import importlib.util, json, math

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


E = load(ROOT + '/labs/lab-keystone/analysis/exponent_fit_2026-11-22.py', 'ef')


def setup_of(rnd, n):
    return json.load(open('%s/requests/2026-11-22/r%d/lab-keystone/%03d.json' % (ROOT, rnd, n)))['setup']


def result_of(rnd, n):
    return json.load(open('%s/results/2026-11-22/r%d/lab-keystone/%03d.json' % (ROOT, rnd, n)))


def run_from(rnd, n):
    s = setup_of(rnd, n)
    rs = result_of(rnd, n)
    ps = s['particles']
    r0 = math.dist(ps[0]['pos'], ps[1]['pos'])
    u0 = [(ps[1]['pos'][k] - ps[0]['pos'][k]) / r0 for k in range(2)]
    pts = []
    for smp in rs['samples']:
        p = {q['id']: q['pos'] for q in smp['particles']}
        d = [p[1][k] - p[0][k] for k in range(2)]
        pts.append((round(smp['t'], 9), d[0] * u0[0] + d[1] * u0[1]))
    return (s['duration'], s['sample_dt'], r0, pts), orient(ps)


def orient(ps):
    dx = abs(ps[1]['pos'][0] - ps[0]['pos'][0])
    dy = abs(ps[1]['pos'][1] - ps[0]['pos'][1])
    r = math.hypot(dx, dy)
    if dy / r < 0.05:
        return 'H'
    if dx / r < 0.05:
        return 'V'
    return 'D'


def fit_g(runs, P=2.5):
    g_best, rms = E.best_g(runs, P, 1.0, 400.0, ng=241)
    N = sum(len(r[3]) for r in runs)
    thr = rms ** 2 * (1 + 1.0 / N)
    step = g_best * 0.002
    g = g_best
    while E.rss(runs, g, P)[0] ** 2 <= thr:
        g -= step
    lo = g
    g = g_best
    while E.rss(runs, g, P)[0] ** 2 <= thr:
        g += step
    hi = g
    return g_best, (hi - lo) / 2, rms, N


# radius -> list of (round, run). Round 1/2 runs are the earlier pooled A-A data.
GROUPS = {
    1.00: [(1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (3, 17)],
    1.25: [(3, 2), (3, 3), (3, 4)],
    1.50: [(3, 5), (3, 6), (3, 7)],
    1.75: [(3, 8), (3, 9), (3, 10)],
    2.00: [(1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 18)],
    2.50: [(3, 11), (3, 12), (3, 13)],
    3.00: [(3, 14), (3, 15), (3, 16), (3, 22), (3, 23), (3, 24)],
}


def main():
    rows = []
    print('radius  runs                                       g        +/-sig    a=g/r^2.5   sig_a    rms    N')
    for r in sorted(GROUPS):
        loaded = [(rnd, n) + run_from(rnd, n) for rnd, n in GROUPS[r]]
        runs = [x[2] for x in loaded]
        g, sg, rms, N = fit_g(runs)
        a = g / r ** 2.5
        sa = a * sg / g
        rows.append((r, a, sa))
        ids = ' '.join('r%d/%03d' % (x[0], x[1]) for x in loaded)
        print('%.2f  %-42s %7.2f  %6.2f  %10.3f  %7.3f  %.4f  %d' % (r, ids, g, sg, a, sa, rms, N))

    # Primary: weighted LS slope of log a vs log r
    xs = [math.log(r) for r, _, _ in rows]
    ys = [math.log(a) for _, a, _ in rows]
    ws = [(a / sa) ** 2 for _, a, sa in rows]
    Sw = sum(ws)
    Sx = sum(w * x for w, x in zip(ws, xs))
    Sy = sum(w * y for w, y in zip(ws, ys))
    Sxx = sum(w * x * x for w, x in zip(ws, xs))
    Sxy = sum(w * x * y for w, x, y in zip(ws, xs, ys))
    D = Sw * Sxx - Sx * Sx
    s = (Sw * Sxy - Sx * Sy) / D
    ss = math.sqrt(Sw / D)
    print('\nWLS slope s = %.3f +/- %.3f' % (s, ss))
    print('|s + 2.5| = %.3f  (3 sigma = %.3f)  -> P=2.5 rejected at 3 sigma: %s' % (abs(s + 2.5), 3 * ss, abs(s + 2.5) > 3 * ss))
    print('|s + 1.9| = %.3f  (1.9 band +/-0.15 check: %s)' % (abs(s + 1.9), abs(s + 1.9) <= 0.15))
    print('within 1 sigma of -2.5: %s' % (abs(s + 2.5) <= ss))

    # Isotropy: per orientation vs pooled, within each radius
    print('\nIsotropy (per-orientation a vs pooled a, z-score):')
    for r in sorted(GROUPS):
        loaded = [(rnd, n) + run_from(rnd, n) for rnd, n in GROUPS[r]]
        pooled = [x[2] for x in loaded]
        g0, _, _, _ = fit_g(pooled)
        a0 = g0 / r ** 2.5
        zs = []
        parts = []
        for o in 'HVD':
            sub = [x[2] for x in loaded if x[3] == o]
            if not sub:
                continue
            g, sg, _, _ = fit_g(sub)
            a = g / r ** 2.5
            sa = a * sg / g
            z = (a - a0) / sa
            zs.append(abs(z))
            parts.append('%s a=%.3f+/-%.3f z=%+.2f' % (o, a, sa, z))
        print('  r=%.2f  pooled a=%.3f  ' % (r, a0) + ' | '.join(parts) + '  max|z|=%.2f' % max(zs))

    # Shape check: free P at the long-T radii
    print('\nShape check (free P, coarse grid, r = 2.5 and 3.0):')
    for r in (2.5, 3.0):
        loaded = [(rnd, n) + run_from(rnd, n) for rnd, n in GROUPS[r]]
        runs = [x[2] for x in loaded]
        best = None
        for i in range(21):
            P = 1.5 + 0.1 * i
            # coarse log grid for g, scaled to the distance r
            a_guess = 5.47 * (2.0 / r) ** P * (r / 2.0) ** 0 if False else 5.47
            gs = [r ** P * a_guess * 10 ** (0.04 * j - 0.8) for j in range(61)]
            gbest = min(gs, key=lambda g: E.rss(runs, g, P)[0])
            e = E.rss(runs, gbest, P)[0]
            if best is None or e < best[2]:
                best = (P, gbest, e)
            print('  r=%.1f P=%.2f g=%.2f rms=%.5f' % (r, P, gbest, e))
        print('  r=%.1f best P=%.2f rms=%.5f' % (r, best[0], best[2]))


if __name__ == '__main__':
    main()
