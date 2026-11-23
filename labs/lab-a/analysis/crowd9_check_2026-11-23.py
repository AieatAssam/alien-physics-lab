"""Plumbline 2026-11-23: score a uniform pairwise-sum A-A law (K/r^2.5, central, at rest, specular walls) on the N=9 runs.
Usage: python3 -I crowd9_check_2026-11-23.py <repo_root> <K> <rid> [<rid> ...]
Prints RMSE/L per run (RMSE over all coordinates of all particles and samples, divided by L=10).
"""
import json, math, os, sys
root, K = sys.argv[1], float(sys.argv[2]); rids = sys.argv[3:]
P, L, H = 2.5, 10.0, 0.0005
def load(p):
    with open(os.path.join(root, p)) as f: return json.load(f)
def acc(pos):
    n = len(pos); out = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j: continue
            dx, dy = pos[j][0]-pos[i][0], pos[j][1]-pos[i][1]; r = math.hypot(dx, dy); a = K / r**P
            out[i][0] += a*dx/r; out[i][1] += a*dy/r
    return out
def walls(p, v):
    for i in range(len(p)):
        for k in range(2):
            if p[i][k] < 0: p[i][k] = -p[i][k]; v[i][k] = -v[i][k]
            elif p[i][k] > L: p[i][k] = 2*L - p[i][k]; v[i][k] = -v[i][k]
def run(pos, vel, times):
    t = 0.0; out = []
    for T in times:
        while t < T - 1e-12:
            h = min(H, T - t)
            a1 = acc(pos); v1 = vel
            p2 = [[pos[i][k]+h/2*v1[i][k] for k in range(2)] for i in range(len(pos))]; v2 = [[vel[i][k]+h/2*a1[i][k] for k in range(2)] for i in range(len(pos))]
            a2 = acc(p2)
            p3 = [[pos[i][k]+h/2*v2[i][k] for k in range(2)] for i in range(len(pos))]; v3 = [[vel[i][k]+h/2*a2[i][k] for k in range(2)] for i in range(len(pos))]
            a3 = acc(p3)
            p4 = [[pos[i][k]+h*v3[i][k] for k in range(2)] for i in range(len(pos))]; v4 = [[vel[i][k]+h*a3[i][k] for k in range(2)] for i in range(len(pos))]
            a4 = acc(p4)
            pos = [[pos[i][k]+h/6*(v1[i][k]+2*v2[i][k]+2*v3[i][k]+v4[i][k]) for k in range(2)] for i in range(len(pos))]
            vel = [[vel[i][k]+h/6*(a1[i][k]+2*a2[i][k]+2*a3[i][k]+a4[i][k]) for k in range(2)] for i in range(len(pos))]
            walls(pos, vel); t += h
        out.append([list(p) for p in pos])
    return out
for rid in rids:
    d, r, lab, n = rid.split('/')
    q = load('requests/%s/%s/%s/%s.json' % (d, r, lab, n)); res = load('results/%s/%s/%s/%s.json' % (d, r, lab, n))
    ps = q['setup']['particles']; pos0 = [p['pos'] for p in ps]; vel0 = [p['vel'] for p in ps]
    times = [s['t'] for s in res['samples']]
    meas = [[ {pp['id']: pp['pos'] for pp in s['particles']}[i] for i in range(len(ps))] for s in res['samples']]
    pred = run([list(p) for p in pos0], [list(v) for v in vel0], times)
    se = [(meas[k][i][c]-pred[k][i][c])**2 for k in range(len(times)) for i in range(len(ps)) for c in range(2)]
    print("%s N=%d T=%g  RMSE/L=%.5f" % (rid, len(ps), times[-1], math.sqrt(sum(se)/len(se))/L))
