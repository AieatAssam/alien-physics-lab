"""Tonight's grant (2026-11-24): 8 A particles in 4 horizontal pairs, r0 = 2.5, at rest, centres (2.25|7.75, 2.25|7.75).
T = 0.6, sample_dt 0.003. Pre-registered prediction: full pairwise-additive P-0024 law (per-particle (G/2)/r^P toward
each partner, G = 23.63, P = 2.099), RK4 h = 0.001, specular walls. Writes setup, prediction and geometry.
Run: python3 -I <this file> <repo_root> <out_dir_for_json>
"""
import json, math, sys
ROOT, OUT = sys.argv[1], sys.argv[2]
G, P, L = 23.63, 2.099, 10.0
R0, T, DT, H = 2.5, 0.6, 0.003, 0.001
centres = [(2.25, 2.25), (7.75, 2.25), (2.25, 7.75), (7.75, 7.75)]
parts = []
for cx, cy in centres:
    parts.append({'species': 'A', 'pos': [round(cx - R0 / 2, 6), cy], 'vel': [0.0, 0.0]})
    parts.append({'species': 'A', 'pos': [round(cx + R0 / 2, 6), cy], 'vel': [0.0, 0.0]})
n = len(parts)
pos0 = [p['pos'] for p in parts]
d = [math.dist(pos0[i], pos0[j]) for i in range(n) for j in range(i + 1, n)]
print('N=%d initial pairwise distance min %.4f max %.4f' % (n, min(d), max(d)))


def acc(pos):
    a = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = pos[j][0] - pos[i][0]; dy = pos[j][1] - pos[i][1]; r = math.hypot(dx, dy)
                f = 0.5 * G / r ** (P + 1)
                a[i][0] += f * dx; a[i][1] += f * dy
    return a


def step(pos, vel, h):
    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]
    k1p, k1v = vel, acc(pos)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2); k2p, k2v = v2, acc(p2)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2); k3p, k3v = v3, acc(p3)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h); k4p, k4v = v4, acc(p4)
    np_ = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)] for i in range(n)]
    nv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)] for i in range(n)]
    for i in range(n):
        for k in range(2):
            if np_[i][k] < 0: np_[i][k] = -np_[i][k]; nv[i][k] = -nv[i][k]
            elif np_[i][k] > L: np_[i][k] = 2 * L - np_[i][k]; nv[i][k] = -nv[i][k]
    return np_, nv


pos = [list(p) for p in pos0]; vel = [[0.0, 0.0] for _ in range(n)]
frames = {0.0: [list(p) for p in pos]}
t = 0.0; minsep = min(d)
for k in range(1, int(round(T / DT)) + 1):
    tgt = round(k * DT, 9)
    while t < tgt - 1e-12:
        h = min(H, tgt - t)
        pos, vel = step(pos, vel, h); t += h
    t = tgt
    frames[tgt] = [list(p) for p in pos]
    minsep = min(minsep, min(math.dist(pos[i], pos[j]) for i in range(n) for j in range(i + 1, n)))
print('min pairwise distance over run %.3f' % minsep)
setup = {'particles': parts, 'duration': T, 'sample_dt': DT}
json.dump(setup, open(OUT + '/grant_setup_2026-11-24.json', 'w'), indent=1)
json.dump({'t': sorted(frames), 'full': [frames[k] for k in sorted(frames)]}, open(OUT + '/grant_prereg_prediction_2026-11-24.json', 'w'))
print('setup written; frames', len(frames))
