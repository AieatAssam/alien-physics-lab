"""Plumbline 2026-11-23: generic two-species K fit for the close-AC pilot (r3 009-012).
K_AC = acceleration of A toward C (K/r^2.5), K_CA = acceleration of C toward A. Signed K (negative = repulsion).
Uses the sim() integrator from fit_AB_2026-11-22.py. Usage: python3 -I fit_AC_2026-11-23.py <repo_root>
"""
import importlib.util, math, os, statistics as st, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("fit_AB", os.path.join(HERE, "fit_AB_2026-11-22.py"))
fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
root = sys.argv[1]; fm.root = root
def fit_pair(rid, la, lb):
    d, r, lab, n = rid.split('/')
    q = fm.load('requests', d, r, lab, n + '.json'); res = fm.load('results', d, r, lab, n + '.json')
    ps = q['setup']['particles']; species = [p['species'] for p in ps]; p0 = [p['pos'] for p in ps]
    times, meas = [], []
    for s in res['samples']:
        tab = {p['id']: p['pos'] for p in s['particles']}; times.append(s['t']); meas.append([tab[0], tab[1]])
    def cost(k1, k2):
        K = {(la, lb): k1, (lb, la): k2}
        pred = fm.sim(p0, species, K, times, h=1e-3)
        return math.sqrt(sum((meas[k][i][c]-pred[k][i][c])**2 for k in range(len(times)) for i in range(2) for c in range(2)) / (len(times)*4))
    grid = [-30 + 1.5*i for i in range(41)]
    _, a0, b0 = min((cost(a, b), a, b) for a in grid for b in grid)
    _, a1, b1 = min((cost(a0+0.1*i, b0+0.1*j), a0+0.1*i, b0+0.1*j) for i in range(-15, 16) for j in range(-15, 16))
    c = cost(a1, b1)
    return species, a1, b1, c
runs = ["2026-11-22/r3/lab-a/%03d" % i for i in range(9, 13)]
kac, kca = [], []
for rid in runs:
    sp, ka, kc, c = fit_pair(rid, 'A', 'C')
    kac.append(ka); kca.append(kc)
    print("%s %s  K_AC=%.3f K_CA=%.3f rms=%.5f" % (rid, ''.join(sp), ka, kc, c))
print("K_AC mean %.3f sd %.3f (%.1f%%)" % (st.mean(kac), st.stdev(kac), 100*st.stdev(kac)/abs(st.mean(kac))))
print("K_CA mean %.3f sd %.3f (%.1f%%)" % (st.mean(kca), st.stdev(kca), 100*st.stdev(kca)/abs(st.mean(kca))))
