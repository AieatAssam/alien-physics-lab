"""Plumbline 2026-11-23 round 1: score pre-registered controls (prereg_2026-11-23.json).
Uses sim() from the lab's fit_AB_2026-11-22.py (shared integrator). Usage:
  python3 -I prereg_scoring_2026-11-23.py <repo_root> <lab_analysis_dir>
"""
import importlib.util, math, os, statistics as st, sys
root, ana = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("fit_AB", os.path.join(ana, "fit_AB_2026-11-22.py"))
fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
fm.root = root

def get(rid):
    d, r, lab, n = rid.split('/')
    q = fm.load('requests', d, r, lab, n + '.json'); res = fm.load('results', d, r, lab, n + '.json')
    ps = q['setup']['particles']; species = [p['species'] for p in ps]; p0 = [p['pos'] for p in ps]
    times = [s['t'] for s in res['samples']]
    meas = [[{p['id']: p['pos'] for p in s['particles']}[i] for i in range(2)] for s in res['samples']]
    return species, p0, times, meas

def rms(pred, meas, times):
    return math.sqrt(sum((meas[k][i][c]-pred[k][i][c])**2 for k in range(len(times)) for i in range(2) for c in range(2)) / (len(times)*4))

def fit_two(rid, la, lb):
    species, p0, times, meas = get(rid)
    def cost(k1, k2):
        return rms(fm.sim(p0, species, {(la, lb): k1, (lb, la): k2}, times, h=1e-3), meas, times)
    grid = [-30 + 1.5*i for i in range(41)]
    _, a0, b0 = min((cost(a, b), a, b) for a in grid for b in grid)
    _, a1, b1 = min((cost(a0+0.1*i, b0+0.1*j), a0+0.1*i, b0+0.1*j) for i in range(-15, 16) for j in range(-15, 16))
    return a1, b1

def fit_one(rid, s):
    species, p0, times, meas = get(rid)
    def cost(k):
        return rms(fm.sim(p0, species, {(s, s): k}, times, h=1e-3), meas, times)
    grid = [0.5*i for i in range(0, 81)]
    _, k0 = min((cost(k), k) for k in grid)
    _, k1 = min((cost(k0+0.02*i), k0+0.02*i) for i in range(-25, 26))
    return k1, cost(k1)

print("== close-AC: diagonal (2026-11-23/r1 009-014) vs horizontal (2026-11-22/r3 009-012)")
ac_d = [fit_two("2026-11-23/r1/lab-a/%03d" % i, 'A', 'C') for i in range(9, 15)]
ac_h = [fit_two("2026-11-22/r3/lab-a/%03d" % i, 'A', 'C') for i in range(9, 13)]
for lab, arr in [("diag", ac_d), ("horiz", ac_h)]:
    kac = [a for a, b in arr]; kca = [b for a, b in arr]
    print(lab, "K_AC", [round(x, 2) for x in kac], "K_CA", [round(x, 2) for x in kca])
    print(lab, "mean K_AC %.3f K_CA %.3f" % (st.mean(kac), st.mean(kca)))
mdA, mdC = st.mean(a for a, b in ac_d), st.mean(b for a, b in ac_d)
mhA, mhC = st.mean(a for a, b in ac_h), st.mean(b for a, b in ac_h)
print("gap K_AC diag-horiz %.2f%%  gap K_CA %.2f%%" % (100*(mdA-mhA)/mhA, 100*(mdC-mhC)/mhC))

print("== close-CC vertical (2026-11-23/r1 015-018) vs horizontal mean 9.50 (2026-11-21/r1 003,004)")
cc = [fit_one("2026-11-23/r1/lab-a/%03d" % i, 'C')[0] for i in range(15, 19)]
cc_h = [fit_one("2026-11-21/r1/lab-a/%03d" % i, 'C')[0] for i in (3, 4)]
print("vertical K_CC", [round(x, 2) for x in cc], "mean %.3f" % st.mean(cc))
print("horizontal K_CC (re-fit)", [round(x, 2) for x in cc_h], "mean %.3f" % st.mean(cc_h), "(pre-reg value 9.50)")
print("gap vs 9.50: %.2f%%" % (100*(st.mean(cc)-9.50)/9.50))

print("== A-A at separation 7 and 9 (2026-11-23/r1 021-024), K_AA vs 17.7")
for rid in ["2026-11-23/r1/lab-a/021", "2026-11-23/r1/lab-a/022", "2026-11-23/r1/lab-a/023", "2026-11-23/r1/lab-a/024"]:
    k, c = fit_one(rid, 'A')
    print(rid, "K_AA=%.3f  rms=%.5f  ratio to 17.7 = %.3f" % (k, c, k/17.7))
