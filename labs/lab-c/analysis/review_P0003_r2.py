"""Review check of P-0003 (lab-a) on lab-c's domain-edge runs.
Runs: 2026-11-18/r2/lab-c/004 (A-A at rest, r=6, T=2) and 005 (A-A at rest, r=3, T=1).
Positions only. Uses papers/P-0003/model.py unchanged for the rms check, and
re-runs it with K varied (P fixed at 2.5) for a best-K estimate.
Usage: python3 -I out/labs/lab-c/analysis/review_P0003_r2.py   (from repo root)
"""
import json, importlib.util, math
import numpy as np

def load(path):
    spec = importlib.util.spec_from_file_location("P0003", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def arrays(res_path, pred):
    S = json.load(open(res_path))["samples"]
    ot = np.array([s["t"] for s in S])
    O = np.array([[ [p["pos"] for p in s["particles"] if p["id"] == i][0] for i in (0, 1)] for s in S])  # (T,2,2)
    P = np.array([[ [p["pos"] for p in s["particles"] if p["id"] == i][0] for i in (0, 1)] for s in pred])
    return ot, O, P[:len(O)]

def report(tag, req_path, res_path, pid_path):
    q = json.load(open(req_path))
    m = load(pid_path)
    ot = None
    pred = m.predict(q["setup"])
    ot, O, P = arrays(res_path, pred)
    res = O - P                                 # (T,2,2)
    rms = np.sqrt((res ** 2).mean(axis=(0)))    # (2 particles, 2 coords)
    print(f"== {tag}  T={q['setup']['duration']} dt={q['setup']['sample_dt']} n={len(ot)} events={len(json.load(open(res_path))['events'])}")
    for i in (0, 1):
        print(f"   particle {i}: rms x={rms[i,0]:.4f} y={rms[i,1]:.4f} | mean res x={res[:,i,0].mean():+.4f} y={res[:,i,1].mean():+.4f} | max|res|={np.abs(res[:,i]).max():.3f}")
    # segment means over quarters of the run
    edges = np.linspace(0, ot[-1] + 1e-9, 5)
    for k in range(4):
        sel = (ot >= edges[k]) & (ot < edges[k+1])
        if sel.sum():
            print(f"   t in [{edges[k]:.2f},{edges[k+1]:.2f}): mean res p0 x={res[sel,0,0].mean():+.4f} y={res[sel,0,1].mean():+.4f}  p1 x={res[sel,1,0].mean():+.4f} y={res[sel,1,1].mean():+.4f}")
    # best K at P=2.5 (positions only, joint over both particles)
    best = None
    for K in np.arange(12.0, 24.01, 0.05):
        m.K = float(K)
        pr = m.predict(q["setup"])
        _, _, Pk = arrays(res_path, pr)
        sse = ((O - Pk) ** 2).sum()
        if best is None or sse < best[1]:
            best = (float(K), sse)
    n = O.size
    rms_best = math.sqrt(best[1] / n)
    print(f"   best K at P=2.5: {best[0]:.2f}  (rms {rms_best:.4f} per coord; paper K=17.74)")
    m.K = 17.74

if __name__ == "__main__":
    P3 = "papers/P-0003/model.py"
    report("r2/004 (A-A rest r=6, T=2)", "requests/2026-11-18/r2/lab-c/004.json", "results/2026-11-18/r2/lab-c/004.json", P3)
    report("r2/005 (A-A rest r=3, T=1)", "requests/2026-11-18/r2/lab-c/005.json", "results/2026-11-18/r2/lab-c/005.json", P3)
