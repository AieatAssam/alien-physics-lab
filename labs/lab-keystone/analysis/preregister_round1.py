"""Pre-registration for lab-keystone round 1, 2026-11-20. Writes predictions_round1_2026-11-20.json.
Two-particle runs use the P-0009 candidate model (out/papers/P-0009/model.py), which is in-sample for r0 6-9.
Pentagon (N=5) and close-range (r0=1.5) runs use a pairwise sum with P-0005 coefficients at r0=5 (G=1) and
the P-0009 radial factor for r0 in 6-9 only; close-range runs use the pure r^-2.5 law with the P-0005 value at 5.
Pure python, RK4 step 0.002, specular walls at 0 and 10."""
import importlib.util, json, math
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
spec = importlib.util.spec_from_file_location('m_p0009', ROOT + '/out/papers/P-0009/model.py')
m9 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m9)
L = 10.0; P = 2.5; H = 0.002
COUP5 = m9.COUP5

def G(r0):
    if abs(r0 - 5.0) < 1e-9: return 1.0
    return m9.G0 + m9.G1 * r0

def pair_K(si, sj, r0):
    g = G(r0)
    if 'C' in (si, sj): g *= m9.S_C
    return COUP5[(si, sj)] * g

def simulate(pos, vel, species, Kfun, dur, dt):
    n = len(pos)
    K = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                r0 = math.dist(pos[i], pos[j])
                K[i][j] = Kfun(species[i], species[j], r0)
    def acc(p):
        out = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j: continue
                dx = p[j][0] - p[i][0]; dy = p[j][1] - p[i][1]
                r = math.hypot(dx, dy)
                a = K[i][j] / r ** P
                out[i][0] += a * dx / r; out[i][1] += a * dy / r
        return out
    def step(p, v, h):
        def add(a, b, s): return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]
        k1p, k1v = v, acc(p)
        p2, v2 = add(p, k1p, h/2), add(v, k1v, h/2); k2p, k2v = v2, acc(p2)
        p3, v3 = add(p, k2p, h/2), add(v, k2v, h/2); k3p, k3v = v3, acc(p3)
        p4, v4 = add(p, k3p, h), add(v, k3v, h); k4p, k4v = v4, acc(p4)
        np_ = [[p[i][k] + h/6*(k1p[i][k]+2*k2p[i][k]+2*k3p[i][k]+k4p[i][k]) for k in range(2)] for i in range(n)]
        nv = [[v[i][k] + h/6*(k1v[i][k]+2*k2v[i][k]+2*k3v[i][k]+k4v[i][k]) for k in range(2)] for i in range(n)]
        for i in range(n):
            for k in range(2):
                if np_[i][k] < 0: np_[i][k] = -np_[i][k]; nv[i][k] = -nv[i][k]
                elif np_[i][k] > L: np_[i][k] = 2*L - np_[i][k]; nv[i][k] = -nv[i][k]
        return np_, nv
    p = [list(x) for x in pos]; v = [list(x) for x in vel]
    out = {0.0: [tuple(x) for x in p]}; minsep = math.inf
    nout = int(round(dur / dt)); nper = int(round(dt / H))
    for kk in range(1, nout + 1):
        for _ in range(nper): p, v = step(p, v, H)
        for i in range(n):
            for j in range(i + 1, n): minsep = min(minsep, math.dist(p[i], p[j]))
        out[round(kk*dt, 9)] = [tuple(x) for x in p]
    return out, minsep

def req(n):
    return json.load(open('%s/out/requests/2026-11-20/r1/lab-keystone/%03d.json' % (ROOT, n)))

if __name__ == '__main__':
    preds = {}
    # two-particle runs (P-0009 model via predict)
    for n in range(1, 8):
        r = req(n); s = r['setup']
        samples = m9.predict(s)
        pos_end = [tuple(p['pos']) for p in samples[-1]['particles']]
        sp = [p['species'] for p in s['particles']]
        r0 = math.dist(s['particles'][0]['pos'], s['particles'][1]['pos'])
        K = [pair_K(sp[0], sp[1], r0), pair_K(sp[1], sp[0], r0)]
        minsep = min(math.dist(p['particles'][0]['pos'], p['particles'][1]['pos']) for p in samples)
        preds['%03d' % n] = {'species': ''.join(sp), 'r0': round(r0, 3), 'T': s['duration'], 'K_pred': [round(k, 3) for k in K],
                             'model_min_separation': round(minsep, 3), 'model_end_pos': [[round(a, 3), round(b, 3)] for a, b in pos_end]}
    # pentagon N=5 (008): pairwise sum, P-0005 at side 5 and P-0009 radial factor at diagonal 8.09
    r = req(8); ps = r['setup']['particles']
    pos = [p['pos'] for p in ps]; vel = [p['vel'] for p in ps]; sp = [p['species'] for p in ps]
    out, minsep = simulate(pos, vel, sp, pair_K, r['setup']['duration'], r['setup']['sample_dt'])
    preds['008'] = {'species': ''.join(sp), 'model': 'pairwise sum, P-0005 at side 5, P-0009 G at diagonal 8.09', 'min_separation': round(minsep, 3),
                    'end_pos': [[round(a, 3), round(b, 3)] for a, b in out[max(out)]]}
    # close-range repulsive runs (009, 010): pure r^-2.5 with P-0005 coefficient at r0=5 (no radial factor)
    for n in (9, 10):
        r = req(n); ps = r['setup']['particles']
        pos = [p['pos'] for p in ps]; vel = [p['vel'] for p in ps]; sp = [p['species'] for p in ps]
        def pure(si, sj, r0, _s=sp):
            c = COUP5[(si, sj)]
            return c
        out, minsep = simulate(pos, vel, sp, pure, r['setup']['duration'], r['setup']['sample_dt'])
        preds['%03d' % n] = {'species': ''.join(sp), 'model': 'pure r^-2.5, P-0005 coefficients (no radial factor)',
                             'K_pred': [round(pure(sp[0], sp[1], 0), 3), round(pure(sp[1], sp[0], 0), 3)],
                             'end_pos': [[round(a, 3), round(b, 3)] for a, b in out[max(out)]],
                             'min_separation': round(minsep, 3)}
    json.dump(preds, open(ROOT + '/out/labs/lab-keystone/analysis/predictions_round1_2026-11-20.json', 'w'), indent=1)
    print(json.dumps(preds, indent=1))
