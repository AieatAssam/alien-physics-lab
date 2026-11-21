"""Re-fit round-3 close-range runs (2026-11-20/r3/lab-keystone 001-004: A-A, B-B, C-C, A-B at r = 1.5, T = 0.4)
with the corrected fitter: integration step h = sample_dt (the repo simulate() uses a fixed H = 0.005, which
takes zero steps when sample_dt < 0.005). Search window f in [-0.2, 1.2] (old window was +-30% around the
pre-registered value and pinned the fits to its lower edge).
Run: python3 -B -I round3_refit_2026-11-21.py"""
import sys, math
REPO = '/home/runner/work/alien-physics-lab/alien-physics-lab'
sys.path.insert(0, REPO + '/labs/lab-keystone/analysis')
import round2_r1_check as m

m.DAY, m.RND, m.LAB = '2026-11-20', 'r3', 'lab-keystone'
T5 = m.TABLE5


def sim_rms(init, obs, T, dt, k0, k1):
    coef = lambda i, j: k0 if i == 0 else k1
    sim = m.simulate(init, [[0.0, 0.0], [0.0, 0.0]], coef, 2, T, dt, h=dt)
    return m.rmse(sim, obs)[0]


def fit(init, obs, T, dt, b0, b1):
    best = None
    lo, hi, n = -0.2, 1.2, 29
    for _ in range(3):
        g = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
        for f0 in g:
            for f1 in g:
                e = sim_rms(init, obs, T, dt, f0 * b0, f1 * b1)
                if best is None or e < best[2]:
                    best = (f0, f1, e)
        w = (hi - lo) / (n - 1) * 2
        lo, hi = best[0] - w, best[0] + w
    return best


SPEC = {1: ('A', 'A'), 2: ('B', 'B'), 3: ('C', 'C'), 4: ('A', 'B')}
for n, (s0, s1) in SPEC.items():
    req, res = m.load(n)
    s = req['setup']
    init = [p['pos'] for p in s['particles']]
    obs = m.observed(res)
    T, dt = s['duration'], s['sample_dt']
    b0, b1 = T5[(s0, s1)], T5[(s1, s0)]
    f0, f1, e = fit(init, obs, T, dt, b0, b1)
    print('r3-%03d %s%s r0=%.3f T=%.2f dt=%.4f fitted f=(%.3f, %.3f) rms=%.4f table rms=%.4f' % (
        n, s0, s1, math.dist(init[0], init[1]), T, dt, f0, f1, e, sim_rms(init, obs, T, dt, b0, b1)))
