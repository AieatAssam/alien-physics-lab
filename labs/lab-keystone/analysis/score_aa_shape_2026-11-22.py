"""Score out-of-sample A-A requests 2026-11-21/r3/lab-keystone 001-003 (pre-registered in NOTEBOOK).
Fit: per-particle coupling factors f0, f1 times the P-0005 table value (K/r^2.5 at separation 5), integrated at h = dt.
Run: python3 -I <this file>"""
import sys, math
REPO = '/home/runner/work/alien-physics-lab/alien-physics-lab'
sys.path.insert(0, REPO + '/labs/lab-keystone/analysis')
import round2_r1_check as m
m.DAY, m.RND, m.LAB = '2026-11-21', 'r3', 'lab-keystone'
T5 = m.TABLE5


def sim_obs(init, T, dt, k0, k1):
    coef = lambda i, j: k0 if i == 0 else k1
    return m.simulate(init, [[0.0, 0.0], [0.0, 0.0]], coef, 2, T, dt, h=dt)


def fit(init, obs, T, dt, b0, b1):
    best = None
    lo, hi, n = -0.2, 1.4, 33
    grid = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
    for f0 in grid:
        for f1 in grid:
            sim = sim_obs(init, T, dt, f0 * b0, f1 * b1)
            e = m.rmse(sim, obs)[0]
            if best is None or e < best[2]:
                best = (f0, f1, e)
    return best


def run(n, Tcut=None):
    req, res = m.load(n)
    s = req['setup']
    init = [p['pos'] for p in s['particles']]
    obs = m.observed(res)
    T, dt = s['duration'], s['sample_dt']
    if Tcut is not None:
        obs = {pid: [(t, x) for t, x in ser if t <= Tcut + 1e-9] for pid, ser in obs.items()}
        T = Tcut
    r0 = math.dist(init[0], init[1])
    b = T5[('A', 'A')]
    f0, f1, e = fit(init, obs, T, dt, b, b)
    e1 = m.rmse(sim_obs(init, T, dt, b, b), obs)[0]
    e0 = m.rmse(sim_obs(init, T, dt, 0.0, 0.0), obs)[0]
    print('   f=1 rms=%.4f  zero-force rms=%.4f' % (e1, e0))
    return r0, f0, f1, e


for n, label, pre in [(1, 'A-A diagonal', 0.705), (2, 'A-A vertical', 0.865)]:
    r0, f0, f1, e = run(n)
    ok = abs(f0 - pre) <= 0.05 and abs(f1 - pre) <= 0.05
    print('req %03d %s r0=%.3f fitted f=(%.3f, %.3f) rms=%.4f pre=%.3f within_bar=%s' % (n, label, r0, f0, f1, e, pre, ok))

r0, f0, f1, e = run(3, Tcut=0.2)
print('req 003 A-A horizontal r0=%.3f t<=0.2 f=(%.3f, %.3f) rms=%.4f' % (r0, f0, f1, e))
r0, f0, f1, e = run(3)
print('req 003 A-A horizontal r0=%.3f full t<=0.4 f=(%.3f, %.3f) rms=%.4f' % (r0, f0, f1, e))
