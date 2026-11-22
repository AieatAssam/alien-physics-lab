"""Per-particle K fit for two-particle runs of unequal species (Plumbline 2026-11-22).
Each particle i accelerates toward j with K(s_i,s_j) / r^P, P = 2.5 fixed, from rest.
Grid search (coarse then fine) on (K_AB on A, K_BA on B) minimising RMS 2D position residual.
Usage: python3 -I fit_AB_2026-11-22.py <repo_root>
"""
import json, math, os, sys
root = sys.argv[1]; P = 2.5
def load(*p):
    with open(os.path.join(root, *p)) as f: return json.load(f)
def sim(setup_pos, species, K, times, h=5e-4):
    # K: dict (si,sj)->K ; returns positions list per sample
    pos = [list(p) for p in setup_pos]; vel = [[0.0, 0.0], [0.0, 0.0]]
    def acc(pos):
        out = []
        for i in range(2):
            j = 1 - i
            dx, dy = pos[j][0]-pos[i][0], pos[j][1]-pos[i][1]
            r = math.hypot(dx, dy); a = K[(species[i], species[j])] / r**P
            out.append([a*dx/r, a*dy/r])
        return out
    t = 0.0; out = []
    for T in times:
        while t < T - 1e-12:
            s = min(h, T - t)
            a1 = acc(pos); v1 = vel
            p2 = [[pos[i][k]+s/2*v1[i][k] for k in range(2)] for i in range(2)]; v2 = [[vel[i][k]+s/2*a1[i][k] for k in range(2)] for i in range(2)]
            a2 = acc(p2)
            p3 = [[pos[i][k]+s/2*v2[i][k] for k in range(2)] for i in range(2)]; v3 = [[vel[i][k]+s/2*a2[i][k] for k in range(2)] for i in range(2)]
            a3 = acc(p3)
            p4 = [[pos[i][k]+s*v3[i][k] for k in range(2)] for i in range(2)]; v4 = [[vel[i][k]+s*a3[i][k] for k in range(2)] for i in range(2)]
            a4 = acc(p4)
            pos = [[pos[i][k]+s/6*(v1[i][k]+2*v2[i][k]+2*v3[i][k]+v4[i][k]) for k in range(2)] for i in range(2)]
            vel = [[vel[i][k]+s/6*(a1[i][k]+2*a2[i][k]+2*a3[i][k]+a4[i][k]) for k in range(2)] for i in range(2)]
            t += s
        out.append([list(p) for p in pos])
    return out
def fit(rid):
    d, r, lab, n = rid.split('/')
    q = load('requests', d, r, lab, n + '.json'); res = load('results', d, r, lab, n + '.json')
    ps = q['setup']['particles']; species = [p['species'] for p in ps]; p0 = [p['pos'] for p in ps]
    # map result ids to request order
    times, meas = [], []
    for s in res['samples']:
        tab = {p['id']: p['pos'] for p in s['particles']}; times.append(s['t']); meas.append([tab[0], tab[1]])
    def cost(ka, kb):
        K = {('A','B'): ka, ('B','A'): kb}
        pred = sim(p0, species, K, times)
        return math.sqrt(sum((meas[k][i][c]-pred[k][i][c])**2 for k in range(len(times)) for i in range(2) for c in range(2)) / (len(times)*4))
    # coarse
    best = min(((cost(a, b), a, b) for a in [x*0.5 for x in range(10, 25)] for b in [x*0.5 for x in range(14, 33)]))
    _, a0, b0 = best
    best = min(((cost(a0+0.02*i, b0+0.02*j), a0+0.02*i, b0+0.02*j) for i in range(-10, 11) for j in range(-10, 11)))
    c, ka, kb = best
    # keep species labels in order: species[0] first; K_AB is on A (A particle), K_BA on B
    return species, ka, kb, c
if __name__ == '__main__':
    runs = sys.argv[2:] or ['2026-11-21/r3/lab-a/012', '2026-11-21/r3/lab-a/013', '2026-11-21/r3/lab-a/014', '2026-11-21/r3/lab-a/015']
    for r in runs:
        sp, ka, kb, c = fit(r)
        print(r, ''.join(sp), 'K_AB(on A)=%.3f K_BA(on B)=%.3f rms_pos=%.4f' % (ka, kb, c))
