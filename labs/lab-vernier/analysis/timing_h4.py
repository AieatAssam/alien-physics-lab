"""H4 sample-timing check: lone A from (0.5,5.0) with v=(4,0), T=2, dt=0.01 (request 2026-11-20/r1/lab-vernier/004).
Free flight model x(t)=0.5+4t, y=5. If samples were taken at t+tau, the x residual mean is about -4*tau.
Reports mean residuals, naive and lag-corrected standard errors. Run with python3 -I."""
import json, math
R = '/home/runner/work/alien-physics-lab/alien-physics-lab'
rid = '2026-11-20/r1/lab-vernier/004'
req = json.load(open(R + '/requests/' + rid + '.json'))
res = json.load(open(R + '/results/' + rid + '.json'))
p = req['setup']['particles'][0]
x0, y0 = p['pos']; vx, vy = p['vel']
rx, ry = [], []
for s in res['samples']:
    t = s['t']
    q = s['particles'][0]['pos']
    rx.append(q[0] - (x0 + vx * t))
    ry.append(q[1] - (y0 + vy * t))
def stats(r, label):
    n = len(r); m = sum(r) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in r) / (n - 1))
    # lag-1 autocorrelation for an effective sample size
    d = [v - m for v in r]
    rho = sum(d[i] * d[i + 1] for i in range(n - 1)) / sum(v * v for v in d)
    neff = n * (1 - rho) / (1 + rho)
    se_naive = sd / math.sqrt(n); se_eff = sd / math.sqrt(neff)
    print('%s: n=%d mean=%+.5f sd=%.4f rho1=%+.3f se_naive=%.5f se_eff=%.5f' % (label, n, m, sd, rho, se_naive, se_eff))
stats(rx, 'x residual')
stats(ry, 'y residual')
# slope of x residual against t: a time offset tau would give residual -vx*tau (+ constant 0)
n = len(rx); ts = [s['t'] for s in res['samples']]
tb = sum(ts) / n; rb = sum(rx) / n
slope = sum((t - tb) * (r - rb) for t, r in zip(ts, rx)) / sum((t - tb) ** 2 for t in ts)
print('x residual slope vs t = %+.5f (time offset tau = -slope/vx = %+.5f)' % (slope, -slope / vx))
