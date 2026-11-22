"""Trajectory fit of the A-A relative radial law for research 001-006 (exponent test, round 1 of 2026-11-22).
Model: separation q(t) with q'' = -g / q**P (attractive), g = 2K (two identical particles, each K/r^P).
Data: |p1 - p0| from tracker samples. RK4 with step = sample_dt / 5. Grid search over (g, P) and over g at P = 2.5.
Pooled over the two orientations at each r0 (orientation does not enter the radial model).
Run: python3 -I <this file>"""
import json, math

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
RES = ROOT + '/results/2026-11-22/r1/lab-keystone/%03d.json'
SETUP_T = {1: (0.03, 0.0005, 0.5), 2: (0.03, 0.0005, 0.5), 3: (0.1, 0.001, 1.0), 4: (0.1, 0.001, 1.0),
           5: (0.3, 0.005, 2.0), 6: (0.3, 0.005, 2.0)}


def sim(q0, g, P, T, dt):
    n = 5
    h = dt / n
    out = {}
    q, v = q0, 0.0
    t = 0.0
    def acc(x):
        x = max(abs(x), 0.02)
        return -g / x ** P
    # integrate on a fine grid, record at sample times
    steps = int(round(T / h))
    rec_every = n
    out[0.0] = q
    for i in range(1, steps + 1):
        k1q, k1v = v, acc(q)
        q2, v2 = q + h / 2 * k1q, v + h / 2 * k1v
        k2q, k2v = v2, acc(q2)
        q3, v3 = q + h / 2 * k2q, v + h / 2 * k2v
        k3q, k3v = v3, acc(q3)
        q4, v4 = q + h * k3q, v + h * k3v
        k4q, k4v = v4, acc(q4)
        q += h / 6 * (k1q + 2 * k2q + 2 * k3q + k4q)
        v += h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        if i % rec_every == 0:
            out[round(i * h, 9)] = q
    return out


def data(n):
    T, dt, r0 = SETUP_T[n]
    res = json.load(open(RES % n))
    pts = []
    for s in res['samples']:
        p = {q['id']: q['pos'] for q in s['particles']}
        d = math.dist(p[0], p[1])
        pts.append((round(s['t'], 9), d))
    return T, dt, r0, pts


def rss(runs, g, P):
    tot = 0.0
    cnt = 0
    for T, dt, r0, pts in runs:
        m = sim(r0, g, P, T, dt)
        for t, d in pts:
            if t in m:
                tot += (d - m[t]) ** 2
                cnt += 1
    return math.sqrt(tot / cnt), cnt


def best_g(runs, P, glo, ghi, ng=121):
    best = None
    for i in range(ng):
        g = glo + (ghi - glo) * i / (ng - 1)
        e, _ = rss(runs, g, P)
        if best is None or e < best[1]:
            best = (g, e)
    return best


def best_gp(runs):
    best = None
    for P in [1.0 + 0.1 * j for j in range(26)]:
        # coarse g scan around the P=2.5 scale, then refine
        g0 = 0.0
        scan = best_g(runs, P, 1.0, 400.0, ng=60)
        g1, e1 = scan
        fine = best_g(runs, P, max(0.1, g1 * 0.8), g1 * 1.2, ng=41)
        if best is None or fine[1] < best[2]:
            best = (fine[0], P, fine[1])
    return best


if __name__ == '__main__':
    groups = {0.5: [1, 2], 1.0: [3, 4], 2.0: [5, 6]}
    for r0, ns in groups.items():
        runs = [data(n) for n in ns]
        # noise floor: rms of the samples about the raw distance is noise; report fits
        g25, e25 = best_g(runs, 2.5, 1.0, 400.0, ng=241)
        gb, Pb, eb = best_gp(runs)
        print('r0=%.1f runs=%s  P=2.5 fit: g=%.2f (2K=%.2f, K=%.2f) rms=%.4f | free fit: g=%.2f P=%.2f rms=%.4f'
              % (r0, ns, g25, g25, g25 / 2, e25, gb, Pb, eb))
