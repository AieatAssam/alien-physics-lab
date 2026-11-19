"""Round 3 analysis: fit the two-particle coupling of each round-2 run (r^-2.5 shape)
and compare with the pre-registered predictions in predictions_round2.json.
Self-contained (pure python). Reads only repo results for lab-keystone."""
import json, math, sys
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
L = 10.0
P = 2.5

def load(n):
    req = json.load(open('%s/requests/2026-11-19/r2/lab-keystone/%03d.json' % (ROOT, n)))
    res = json.load(open('%s/results/2026-11-19/r2/lab-keystone/%03d.json' % (ROOT, n)))
    return req, res

def observed(res):
    obs = {}
    for s in res['samples']:
        for p in s['particles']:
            obs.setdefault(p['id'], []).append((round(s['t'], 9), p['pos']))
    return obs

def sim(init_pos, K0, K1, T, dt_out, h=0.005):
    # two particles, 0 attracts toward 1 with K0, 1 toward 0 with K1; specular walls
    pos = [list(p) for p in init_pos]; vel = [[0.0, 0.0], [0.0, 0.0]]
    def acc(p):
        out = []
        for i, (c, j) in enumerate([(K0, 1), (K1, 0)]):
            dx = p[j][0] - p[i][0]; dy = p[j][1] - p[i][1]
            r = math.hypot(dx, dy)
            a = c / r ** P
            out.append([a * dx / r, a * dy / r])
        return out
    def step(p, v):
        def add(a, b, s): return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(2)]
        a1 = acc(p); k1p, k1v = v, a1
        p2, v2 = add(p, k1p, h/2), add(v, k1v, h/2); a2 = acc(p2); k2p, k2v = v2, a2
        p3, v3 = add(p, k2p, h/2), add(v, k2v, h/2); a3 = acc(p3); k3p, k3v = v3, a3
        p4, v4 = add(p, k3p, h), add(v, k3v, h); a4 = acc(p4); k4p, k4v = v4, a4
        np_ = [[p[i][k] + h/6*(k1p[i][k]+2*k2p[i][k]+2*k3p[i][k]+k4p[i][k]) for k in range(2)] for i in range(2)]
        nv = [[v[i][k] + h/6*(k1v[i][k]+2*k2v[i][k]+2*k3v[i][k]+k4v[i][k]) for k in range(2)] for i in range(2)]
        for i in range(2):
            for k in range(2):
                if np_[i][k] < 0: np_[i][k] = -np_[i][k]; nv[i][k] = -nv[i][k]
                elif np_[i][k] > L: np_[i][k] = 2*L - np_[i][k]; nv[i][k] = -nv[i][k]
        return np_, nv
    out = {0.0: [tuple(p) for p in pos]}
    nper = int(round(dt_out / h)); nout = int(round(T / dt_out))
    for kk in range(1, nout+1):
        for _ in range(nper):
            pos, vel = step(pos, vel)
        out[round(kk*dt_out, 9)] = [tuple(p) for p in pos]
    return out

def cost(K0, K1, init, obs, T, dt):
    s = sim(init, K0, K1, T, dt)
    sq = cnt = 0
    for pid, series in obs.items():
        for t, (x, y) in series:
            if t not in s: continue
            m = s[t][pid]
            sq += (x-m[0])**2 + (y-m[1])**2; cnt += 2
    return sq / cnt

def fit(init, obs, T, dt, c0, c1, span=0.25, n=9):
    best = None
    for it in range(3):
        grid0 = [c0*(1 + span*(2*i/(n-1)-1)) for i in range(n)]
        grid1 = [c1*(1 + span*(2*i/(n-1)-1)) for i in range(n)]
        for a in grid0:
            for b in grid1:
                e = cost(a, b, init, obs, T, dt)
                if best is None or e < best[0]: best = (e, a, b)
        _, c0, c1 = best
        span /= 4
    return c0, c1, math.sqrt(best[0])

if __name__ == '__main__':
    preds = json.load(open(ROOT + '/labs/lab-keystone/analysis/predictions_round2.json'))
    for pr in preds:
        n = int(pr['request_id'][-3:])
        req, res = load(n)
        if res.get('status') != 'ok':
            print(n, 'status', res.get('status')); continue
        init = [p['pos'] for p in req['setup']['particles']]
        sp = ''.join(p['species'] for p in req['setup']['particles'])
        T = req['setup']['duration']; dt = req['setup']['sample_dt']
        obs = observed(res)
        sep = math.dist(init[0], init[1])
        pred = pr.get('K_pred', None)
        # starting guess: pre-registered prediction for the pair, from the request purpose
        guess = {1: (9.55, 9.55), 2: (8.13, 8.13), 3: (5.92, 8.12), 4: (-5.59, -9.71), 5: (4.73, 4.73)}[n]
        K0, K1, rmsv = fit(init, obs, T, dt, guess[0], guess[1])
        print('%s %s r=%.1f T=%.1f  fitted K_on_0=%.3f K_on_1=%.3f  rms/coord=%.4f  | predicted %s' % (
            pr['request_id'], sp, sep, T, K0, K1, rmsv, guess))
