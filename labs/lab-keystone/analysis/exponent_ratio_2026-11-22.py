"""Local acceleration at each r0 from the P = 2.5 radial fit, with a 1-sigma interval from the rms-vs-g curve.
a(r0) = g / r0^2.5 (relative acceleration at r0 under the fitted shape). Ratios test the exponent:
P = 2.5 predicts 5.66 for a(0.5)/a(1.0) and a(1.0)/a(2.0); local exponent 1.9 predicts 3.7.
Run: python3 -I <this file>"""
import importlib.util, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ef', HERE + '/exponent_fit_2026-11-22.py')
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

groups = {0.5: [1, 2], 1.0: [3, 4], 2.0: [5, 6]}
out = {}
for r0, ns in groups.items():
    runs = [E.data(n) for n in ns]
    g_best, rms_best = E.best_g(runs, 2.5, 1.0, 400.0, ng=241)
    N = sum(len(r[3]) for r in runs)
    sigma2 = rms_best ** 2 / 1.0
    # 1-sigma: rms(g)^2 <= rms_best^2 * (1 + 1/N) approx (delta chi2 = 1 with sigma = rms_best)
    lo = hi = g_best
    step = g_best * 0.002
    g = g_best
    while True:
        g -= step
        e, _ = E.rss(runs, g, 2.5)
        if e * e > rms_best ** 2 * (1 + 1.0 / N):
            lo = g
            break
    g = g_best
    while True:
        g += step
        e, _ = E.rss(runs, g, 2.5)
        if e * e > rms_best ** 2 * (1 + 1.0 / N):
            hi = g
            break
    a = g_best / r0 ** 2.5
    out[r0] = (a, a * (hi - lo) / 2 / g_best, g_best, lo, hi, rms_best, N)
    print('r0=%.1f  g=%.2f [%.2f, %.2f]  a=%.2f +/- %.2f  rms=%.4f  N=%d' % (r0, g_best, lo, hi, a, out[r0][1], rms_best, N))

for lo_r, hi_r in [(0.5, 1.0), (1.0, 2.0)]:
    a1, s1 = out[lo_r][0], out[lo_r][1]
    a2, s2 = out[hi_r][0], out[hi_r][1]
    ratio = a1 / a2
    print('a(%.1f)/a(%.1f) = %.2f +/- %.2f   (P=2.5 predicts 5.66; local P 1.9 predicts 3.7)' % (lo_r, hi_r, ratio, ratio * math.hypot(s1 / a1, s2 / a2)))
