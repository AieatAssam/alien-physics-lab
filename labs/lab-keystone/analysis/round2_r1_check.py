"""Round 2 (2026-11-20): score round-1 pre-registered requests 001-010 (lab-keystone, own runs only).

Pairs 001-007: fit the two coefficients (K on particle 0, K on particle 1) of K/r^2.5 at fixed K,
compare with the pre-registered K_pred. Pentagon 008: pairwise sum with the P-0005 table at r^-2.5.
Close range 009-010: pure r^-2.5 law with the P-0005 table. Self-contained, pure python, reads repo results.
Run with: python3 -I round2_r1_check.py
"""
import json, math

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
DAY, RND, LAB = '2026-11-20', 'r1', 'lab-keystone'
P = 2.5
L = 10.0
H = 0.005
TABLE5 = {('A', 'A'): 18.0, ('A', 'B'): 8.99, ('B', 'A'): 12.34, ('A', 'C'): -8.77, ('C', 'A'): -21.25,
          ('B', 'B'): 6.12, ('C', 'C'): 12.36, ('B', 'C'): -6.10, ('C', 'B'): -10.59}


def load(n):
    req = json.load(open('%s/requests/%s/%s/%s/%03d.json' % (ROOT, DAY, RND, LAB, n)))
    res = json.load(open('%s/results/%s/%s/%s/%03d.json' % (ROOT, DAY, RND, LAB, n)))
    return req, res


def observed(res):
    obs = {}
    for s in res['samples']:
        for p in s['particles']:
            if 'pos' in p:
                obs.setdefault(p['id'], []).append((round(s['t'], 9), p['pos']))
    return obs


def acc_fn(coef, n):
    def acc(pos):
        out = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                c = coef(i, j)
                dx = pos[j][0] - pos[i][0]; dy = pos[j][1] - pos[i][1]
                r = math.hypot(dx, dy)
                if r < 1e-9 or c == 0.0:
                    continue
                a = c / r ** P
                out[i][0] += a * dx / r; out[i][1] += a * dy / r
        return out
    return acc


def rk4(pos, vel, acc, n, h):
    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]
    k1p, k1v = vel, acc(pos)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, acc(p2)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, acc(p3)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, acc(p4)
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)] for i in range(n)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)] for i in range(n)]
    for i in range(n):
        for k in range(2):
            if newp[i][k] < 0.0:
                newp[i][k] = -newp[i][k]; newv[i][k] = -newv[i][k]
            elif newp[i][k] > L:
                newp[i][k] = 2 * L - newp[i][k]; newv[i][k] = -newv[i][k]
    return newp, newv


def simulate(init_pos, init_vel, coef, n, T, dt_out, h=H):
    acc = acc_fn(coef, n)
    pos = [list(p) for p in init_pos]; vel = [list(v) for v in init_vel]
    out = {0.0: [tuple(p) for p in pos]}
    nper = int(round(dt_out / h)); nout = int(round(T / dt_out))
    for k in range(1, nout + 1):
        for _ in range(nper):
            pos, vel = rk4(pos, vel, acc, n, h)
        out[round(k * dt_out, 9)] = [tuple(p) for p in pos]
    return out


def rmse(sim, obs):
    s = cnt = 0
    worst = 0.0
    for pid, series in obs.items():
        for t, (x, y) in series:
            m = sim.get(round(t, 9))
            if m is None:
                continue
            dx, dy = x - m[pid][0], y - m[pid][1]
            s += dx * dx + dy * dy; cnt += 2
            worst = max(worst, abs(dx), abs(dy))
    return math.sqrt(s / cnt), worst


def sse(K0, K1, init, obs, T, dt):
    coef = lambda i, j: K0 if i == 0 else K1
    sim = simulate([p for p in init], [[0.0, 0.0], [0.0, 0.0]], coef, 2, T, dt)
    return rmse(sim, obs)[0]


def fit_pair(init, obs, T, dt, c0, c1):
    """Coarse grid around the prediction, then two refinement passes."""
    best = None
    span, n = 0.3, 13
    cx, cy = c0, c1
    for _ in range(3):
        grid0 = [cx * (1 + span * (2 * i / (n - 1) - 1)) for i in range(n)]
        grid1 = [cy * (1 + span * (2 * i / (n - 1) - 1)) for i in range(n)]
        for a in grid0:
            for b in grid1:
                e = sse(a, b, init, obs, T, dt)
                if best is None or e < best[2]:
                    best = (a, b, e)
        cx, cy = best[0], best[1]
        span /= 4
    return best


def pair_run(n, k_pred):
    req, res = load(n)
    s = req['setup']; parts = s['particles']
    init = [p['pos'] for p in parts]
    obs = observed(res)
    T, dt = s['duration'], s['sample_dt']
    K0, K1, rms = fit_pair(init, obs, T, dt, k_pred[0], k_pred[1])
    fit_rms = sse(K0, K1, init, obs, T, dt)
    pred_sim = simulate(init, [[0.0, 0.0], [0.0, 0.0]],
                        lambda i, j: k_pred[0] if i == 0 else k_pred[1], 2, T, dt)
    pr, pw = rmse(pred_sim, obs)
    print('%03d %s r0=%.2f T=%.1f  pred K=(%.3f,%.3f)  fitted K=(%.3f,%.3f)  dK=(%+.1f%%,%+.1f%%)  '
          'rms(fit)=%.4f  rms(pred)=%.4f  error(pred)=%.5f' % (
              n, ''.join(p['species'] for p in parts), math.dist(init[0], init[1]), T,
              k_pred[0], k_pred[1], K0, K1, 100 * (K0 / k_pred[0] - 1), 100 * (K1 / k_pred[1] - 1),
              fit_rms, pr, pr / 10.0))


def table_run(n, label):
    req, res = load(n)
    s = req['setup']; parts = s['particles']
    sp = [p['species'] for p in parts]
    init = [p['pos'] for p in parts]; vel = [p['vel'] for p in parts]
    obs = observed(res)
    T, dt = s['duration'], s['sample_dt']
    sim = simulate(init, vel, lambda i, j: TABLE5[(sp[i], sp[j])], len(parts), T, dt, h=0.002)
    r, w = rmse(sim, obs)
    d = [math.dist(init[i], init[j]) for i in range(len(init)) for j in range(i + 1, len(init))]
    print('%03d %s %s N=%d sep=[%.2f,%.2f] T=%.1f  rms=%.4f  max|res|=%.3f  error=%.5f  min-sep-in-model=%.3f' % (
        n, ''.join(sp), label, len(parts), min(d), max(d), T, r, w, r / 10.0, min(d)))


if __name__ == '__main__':
    preds = {1: (5.3, 5.3), 2: (10.142, 10.142), 3: (15.588, 15.588), 4: (7.785, 10.686),
             5: (-5.005, -8.689), 6: (11.219, 11.219), 7: (17.244, 17.244)}
    for n in range(1, 8):
        pair_run(n, preds[n])
    table_run(8, 'pentagon, pairwise sum, r^-2.5 (no radial factor)')
    for n in (9, 10):
        table_run(n, 'close range, pure r^-2.5 (P-0005 table)')
