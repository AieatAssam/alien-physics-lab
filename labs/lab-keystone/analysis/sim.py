"""Shared pure-python helpers for lab-keystone round-2 analysis (no numpy available).

Two-body/N-body central pair model with specular walls on [0, L]^2:
  a_i = sum_j coef[(i, j)] * r_ij**(-P) * unit(x_j - x_i)
Integrated with RK4 at fixed internal step h. Samples at the request's sample_dt.
"""
import json, math

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
L = 10.0
DATE, RND, LAB = '2026-11-19', 'r1', 'lab-keystone'


def req(n):
    return json.load(open('%s/requests/%s/%s/%s/%03d.json' % (ROOT, DATE, RND, LAB, n)))


def res(n):
    return json.load(open('%s/results/%s/%s/%s/%03d.json' % (ROOT, DATE, RND, LAB, n)))


def observed(result):
    """Return {id: [(t, (x, y)), ...]} from tracker samples."""
    obs = {}
    for s in result['samples']:
        for p in s['particles']:
            if 'pos' in p:
                obs.setdefault(p['id'], []).append((s['t'], tuple(p['pos'])))
    return obs


def accel(pos, coef, P, n):
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            c = coef(i, j)
            if c == 0.0:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            if r < 1e-9:
                continue
            a = c / r ** P
            acc[i][0] += a * dx / r
            acc[i][1] += a * dy / r
    return acc


def simulate(init_pos, init_vel, coef, P, n, T, dt_out, h=0.005):
    """coef(i, j) -> coupling for particle i toward j (positive attracts). Returns {t: [pos...]}."""
    pos = [list(p) for p in init_pos]
    vel = [list(v) for v in init_vel]
    out = {0.0: [tuple(p) for p in pos]}
    nsteps_per_out = int(round(dt_out / h))
    nout = int(round(T / dt_out))
    t = 0.0
    for k in range(1, nout + 1):
        for _ in range(nsteps_per_out):
            pos, vel = _rk4(pos, vel, coef, P, n, h)
            t += h
        out[round(k * dt_out, 9)] = [tuple(p) for p in pos]
    return out


def _rk4(pos, vel, coef, P, n, h):
    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]
    k1p, k1v = vel, accel(pos, coef, P, n)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, accel(p2, coef, P, n)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, accel(p3, coef, P, n)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, accel(p4, coef, P, n)
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)] for i in range(n)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)] for i in range(n)]
    for i in range(n):
        for k in range(2):
            if newp[i][k] < 0.0:
                newp[i][k] = -newp[i][k]; newv[i][k] = -newv[i][k]
            elif newp[i][k] > L:
                newp[i][k] = 2 * L - newp[i][k]; newv[i][k] = -newv[i][k]
    return newp, newv


def sse_and_count(sim, obs):
    """Sum of squared residuals over all particles and sample times present in obs."""
    s, cnt, worst = 0.0, 0, 0.0
    for pid, series in obs.items():
        for t, (x, y) in series:
            m = sim.get(round(t, 9))
            if m is None:
                continue
            dx, dy = x - m[pid][0], y - m[pid][1]
            s += dx * dx + dy * dy
            cnt += 2
            worst = max(worst, abs(dx), abs(dy))
    return s, cnt, worst


def rms(sim, obs):
    s, c, _ = sse_and_count(sim, obs)
    return math.sqrt(s / c) if c else float('nan')


def golden(f, lo, hi, tol=1e-4):
    gr = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = f(c), f(d)
    while abs(b - a) > tol:
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a); fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a); fd = f(d)
    return (a + b) / 2


def load_any(date, rnd, lab, n):
    """Request and result for any lab's run (public repo files)."""
    r = json.load(open('%s/requests/%s/%s/%s/%03d.json' % (ROOT, date, rnd, lab, n)))
    rr = json.load(open('%s/results/%s/%s/%s/%03d.json' % (ROOT, date, rnd, lab, n)))
    return r, rr


def simulate_g(init_pos, init_vel, K, g, n, T, dt_out, h=0.01):
    """Like simulate, but magnitude = K(i,j) * g(r), with g an arbitrary radial function."""
    def acc(pos):
        out = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                c = K(i, j)
                dx = pos[j][0] - pos[i][0]; dy = pos[j][1] - pos[i][1]
                r = math.hypot(dx, dy)
                if r < 1e-9 or c == 0.0:
                    continue
                a = c * g(r)
                out[i][0] += a * dx / r; out[i][1] += a * dy / r
        return out
    pos = [list(p) for p in init_pos]; vel = [list(v) for v in init_vel]
    res_ = {0.0: [tuple(p) for p in pos]}
    nper = int(round(dt_out / h)); nout = int(round(T / dt_out))
    for k in range(1, nout + 1):
        for _ in range(nper):
            pos, vel = _rk4_g(pos, vel, acc, n, h)
        res_[round(k * dt_out, 9)] = [tuple(p) for p in pos]
    return res_


def _rk4_g(pos, vel, acc, n, h):
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
