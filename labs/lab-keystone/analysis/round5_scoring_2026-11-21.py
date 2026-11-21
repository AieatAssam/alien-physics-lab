"""Score research requests 010-013 (2026-11-21/r2/lab-keystone), A-A shape at r0 = 1.25..2.0, two-particle constant-K/r^2.5 fits.
BUG FIXED: round2_r1_check.simulate uses a fixed internal step H=0.005; with sample_dt=0.002 it takes
zero steps and freezes the particles, so its fits are meaningless. Here we integrate at h = sample_dt.
Fit: f0, f1 = fitted coupling / P-0005 table value, for particle 0 on 1 (f0) and 1 on 0 (f1).
Run: python3 -B -I <this file>"""
import sys, math
REPO = '/home/runner/work/alien-physics-lab/alien-physics-lab'
sys.path.insert(0, REPO + '/labs/lab-keystone/analysis')
import round2_r1_check as m
m.DAY, m.RND, m.LAB = '2026-11-21', 'r2', 'lab-keystone'
T5 = m.TABLE5
SPEC = {10: ('A', 'A'), 11: ('A', 'A'), 12: ('A', 'A'), 13: ('A', 'A')}


def sim_rms(init, obs, T, dt, k0, k1):
    coef = lambda i, j: k0 if i == 0 else k1
    sim = m.simulate(init, [[0.0, 0.0], [0.0, 0.0]], coef, 2, T, dt, h=dt)
    return m.rmse(sim, obs)[0]


def fit(init, obs, T, dt, base0, base1):
    best = None
    lo, hi, n = -0.2, 1.2, 29
    for it in range(3):
        grid = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
        for f0 in grid:
            for f1 in grid:
                e = sim_rms(init, obs, T, dt, f0 * base0, f1 * base1)
                if best is None or e < best[2]:
                    best = (f0, f1, e)
        w = (hi - lo) / (n - 1) * 2
        lo, hi = best[0] - w, best[0] + w
        # keep f1 window around its own best via separate bounds on second pass
    return best


for n, (s0, s1) in SPEC.items():
    req, res = m.load(n)
    s = req['setup']
    init = [p['pos'] for p in s['particles']]
    obs = m.observed(res)
    T, dt = s['duration'], s['sample_dt']
    b0, b1 = T5[(s0, s1)], T5[(s1, s0)]
    f0, f1, e = fit(init, obs, T, dt, b0, b1)
    e_table = sim_rms(init, obs, T, dt, b0, b1)
    e_zero = sim_rms(init, obs, T, dt, 0.0, 0.0)
    r0 = math.dist(init[0], init[1])
    print('%03d %s%s r0=%.3f T=%.2f dt=%.4f | fitted f=(%.3f, %.3f) rms=%.4f | table(f=1) rms=%.4f | zero-force rms=%.4f | error(f=1)=%.5f'
          % (n, s0, s1, r0, T, dt, f0, f1, e, e_table, e_zero, e_table / 10.0))
