"""Plumbline 2026-11-22 round 3: how sensitive is the judged metric to K for P-0021 at T = 6?

Uses my review runs 2026-11-22/r2/lab-a/013-015 (A-B at separation 7, at rest, T = 6, sample_dt 0.01).
(1) Judged error/L of the paper's model with K scaled by s, for s in a small grid.
(2) Best global scale s* (least RMSE over all three runs) with its spread between runs.
Paper model is imported from papers/P-0021/model.py. Usage: python3 -I p0021_sensitivity_2026-11-22.py <repo_root>
"""
import importlib.util, json, math, os, sys

root = sys.argv[1]
L = 10.0
RIDS = ["2026-11-22/r2/lab-a/%03d" % i for i in (13, 14, 15)]


def load(*p):
    with open(os.path.join(root, *p)) as f:
        return json.load(f)


spec = importlib.util.spec_from_file_location("p0021", os.path.join(root, "papers", "P-0021", "model.py"))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
K0 = dict(M.K)


def run_err(rid, scale):
    d, r, lab, n = rid.split('/')
    q = load('requests', d, r, lab, n + '.json')
    res = load('results', d, r, lab, n + '.json')
    M.K = {k: v * scale for k, v in K0.items()}
    pred = {round(s['t'], 9): s for s in M.predict(q['setup'])}
    sq, cnt = 0.0, 0
    for s in res['samples']:
        mt = {p['id']: p['pos'] for p in s['particles']}
        pt = {p['id']: p['pos'] for p in pred[round(s['t'], 9)]['particles']}
        for pid in (0, 1):
            for k in range(2):
                sq += (mt[pid][k] - pt[pid][k]) ** 2; cnt += 1
    M.K = K0
    return math.sqrt(sq / cnt) / L


scales = [0.95, 0.97, 0.99, 1.00, 1.01, 1.03, 1.05]
print("scale  " + "  ".join(rid[-3:] for rid in RIDS) + "   mean")
for s in scales:
    errs = [run_err(rid, s) for rid in RIDS]
    print("%.2f   " % s + "  ".join("%.5f" % e for e in errs) + "   %.5f" % (sum(errs) / len(errs)))

# finer scan for best scale on pooled squared error
best = None
for i in range(-10, 11):
    s = 1.0 + 0.005 * i
    errs = [run_err(rid, s) for rid in RIDS]
    m = sum(e * e for e in errs) / len(errs)
    if best is None or m < best[0]:
        best = (m, s, errs)
print("best global scale (grid 0.005) = %.3f, per-run error/L at best: %s" % (best[1], ["%.5f" % e for e in best[2]]))
