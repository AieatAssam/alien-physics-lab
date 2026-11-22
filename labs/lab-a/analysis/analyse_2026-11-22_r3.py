"""Plumbline round 3 (2026-11-22) analysis.

(a) Per-particle K_AB / K_BA fits (P = 2.5 fixed) for close-AB round 2 runs 2026-11-22/r2/lab-a/001-012,
    using fit_AB_2026-11-22.py (copied unchanged alongside this file).
(b) Judged-metric check of P-0021 (lab-vernier) on my review runs 013-015: RMSE between the paper model's
    predicted positions and measured positions, divided by L = 10. Paper model imported from
    papers/P-0021/model.py via importlib (path given explicitly, no sys.path changes).

Usage: python3 -I analyse_2026-11-22_r3.py <repo_root>
"""
import importlib.util, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
root = sys.argv[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fitmod = load_module("fit_AB", os.path.join(HERE, "fit_AB_2026-11-22.py"))
# fit_AB reads sys.argv[1] at import time only for root; re-point its root explicitly via fit(rid) using repo root
fitmod.root = root

CLOSE_AB = ["2026-11-22/r2/lab-a/%03d" % i for i in range(1, 13)]
P0021 = ["2026-11-22/r2/lab-a/%03d" % i for i in range(13, 16)]
L = 10.0


def load(*p):
    with open(os.path.join(root, *p)) as f:
        return json.load(f)


def close_ab_fits():
    rows = []
    for rid in CLOSE_AB:
        sp, ka, kb, c = fitmod.fit(rid)
        rows.append((rid, ''.join(sp), ka, kb, c))
        print("%s  species=%s  K_AB(on A)=%.3f  K_BA(on B)=%.3f  rms_pos=%.5f" % (rid, ''.join(sp), ka, kb, c))
    return rows


def p0021_error(rid, paper_mod):
    d, r, lab, n = rid.split('/')
    q = load('requests', d, r, lab, n + '.json')
    res = load('results', d, r, lab, n + '.json')
    samples = paper_mod.predict(q['setup'])
    # match on t
    pred_by_t = {round(s['t'], 9): s for s in samples}
    sq, count = 0.0, 0
    for s in res['samples']:
        t = round(s['t'], 9)
        if t not in pred_by_t:
            raise SystemExit("time %s missing in prediction for %s" % (t, rid))
        mtab = {p['id']: p['pos'] for p in s['particles']}
        ptab = {p['id']: p['pos'] for p in pred_by_t[t]['particles']}
        for pid in (0, 1):
            for k in range(2):
                sq += (mtab[pid][k] - ptab[pid][k]) ** 2
                count += 1
    rmse = math.sqrt(sq / count)
    return rmse / L, len(res['samples']), t


if __name__ == '__main__':
    print("== close-AB round 2 per-particle fits")
    rows = close_ab_fits()
    hor = [r for r in rows if r[0][-3:] in ('001', '002', '003', '004', '005', '006')]
    dia = [r for r in rows if r[0][-3:] in ('007', '008', '009', '010', '011', '012')]
    import statistics as st
    for name, group in (("horizontal (3,3)", hor), ("diagonal (3,3)", dia), ("all 12", rows)):
        kab = [g[2] for g in group]; kba = [g[3] for g in group]
        print("%-18s K_AB mean %.3f sd %.3f se %.3f | K_BA mean %.3f sd %.3f se %.3f" % (
            name, st.mean(kab), st.stdev(kab), st.stdev(kab) / math.sqrt(len(kab)),
            st.mean(kba), st.stdev(kba), st.stdev(kba) / math.sqrt(len(kba))))

    print("\n== P-0021 judged-metric check on my runs 013-015")
    paper = load_module("p0021_model", os.path.join(root, "papers", "P-0021", "model.py"))
    for rid in P0021:
        e, n, _ = p0021_error(rid, paper)
        print("%s  error/L = %.5f  (bar 3 x 0.007 = 0.021)  samples=%d" % (rid, e, n))
