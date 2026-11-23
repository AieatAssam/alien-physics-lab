"""Pre-registration for the grant main event (2026-11-23/r3/lab-keystone/001): 16 A at rest, 8 horizontal pairs,
T = 0.3, sample_dt 0.0015. Additive model: each pair contributes the P-0024 relative acceleration G/q^P (G = 23.63,
P = 2.099), applied to all 120 pairs, each particle pulled by half of it toward its partner. Pairs beyond r = 3 are
outside P-0024's fitted range; their share of the predicted displacement is reported separately.
Run: python3 -I <file> <repo_root>"""
import json, math, sys

ROOT = sys.argv[1]
setup = json.load(open(ROOT + '/out/requests/2026-11-23/r3/lab-keystone/001.json'))['setup']
G, P = 23.63, 2.099
H = 0.0005


def acc(pos, cut=None):
    n = len(pos)
    out = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]; dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            if cut is not None and not (cut[0] <= r <= cut[1]):
                continue
            a = 0.5 * G / r ** P
            out[i][0] += a * dx / r; out[i][1] += a * dy / r
    return out


def run(pos0, T, dt_s, cut=None):
    pos = [list(p) for p in pos0]
    vel = [[0.0, 0.0] for _ in pos]
    t, samples = 0.0, [(0.0, [list(p) for p in pos])]
    steps = int(round(T / dt_s))
    for k in range(1, steps + 1):
        target = round(k * dt_s, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            a1 = acc(pos, cut)
            p2 = [[pos[i][c] + h / 2 * vel[i][c] for c in range(2)] for i in range(len(pos))]
            v2 = [[vel[i][c] + h / 2 * a1[i][c] for c in range(2)] for i in range(len(pos))]
            a2 = acc(p2, cut)
            p3 = [[pos[i][c] + h / 2 * v2[i][c] for c in range(2)] for i in range(len(pos))]
            v3 = [[vel[i][c] + h / 2 * a2[i][c] for c in range(2)] for i in range(len(pos))]
            a3 = acc(p3, cut)
            p4 = [[pos[i][c] + h * v3[i][c] for c in range(2)] for i in range(len(pos))]
            v4 = [[vel[i][c] + h * a3[i][c] for c in range(2)] for i in range(len(pos))]
            a4 = acc(p4, cut)
            for i in range(len(pos)):
                for c in range(2):
                    pos[i][c] += h / 6 * (vel[i][c] + 2 * v2[i][c] + 2 * v3[i][c] + v4[i][c])
                    vel[i][c] += h / 6 * (a1[i][c] + 2 * a2[i][c] + 2 * a3[i][c] + a4[i][c])
            t += h
        t = target
        samples.append((target, [list(p) for p in pos]))
    return samples


if __name__ == '__main__':
    pos0 = [p['pos'] for p in setup['particles']]
    T, dt_s = setup['duration'], setup['sample_dt']
    full = run(pos0, T, dt_s)
    near = run(pos0, T, dt_s, cut=(0.0, 3.0))
    far = run(pos0, T, dt_s, cut=(3.0, 1e9))
    print('min pairwise distance at t=0:', round(min(math.dist(pos0[i], pos0[j]) for i in range(16) for j in range(i + 1, 16)), 3))
    print('max |displacement| at T for full additive model:', round(max(math.dist(full[-1][1][i], pos0[i]) for i in range(16)), 4))
    d_far = max(math.dist(full[-1][1][i], near[-1][1][i]) for i in range(16))
    print('max per-particle displacement difference, full vs pairs r <= 3 only: %.4f' % d_far)
    d_pairs_far = max(math.dist(far[-1][1][i], [0, 0]) for i in range(16))
    print('max displacement from pairs with r > 3 alone: %.4f' % d_pairs_far)
    json.dump({'t': [s[0] for s in full], 'full': [s[1] for s in full]}, open(ROOT + '/out/labs/lab-keystone/analysis/grant_prereg_prediction_2026-11-23.json', 'w'))
