"""Round-2 lab-c checks run this session.
001: A-A at rest r~3, T=2, dt 0.001 (replicate of 2026-11-17/r2/lab-c/001 energy case).
     Separation vs time from tracker positions (id-free), against papers/P-0003/model.py (K=17.74 and K=16.6).
002/003: A-A approach / recede at r=6, speed 2 each. Rest-law residuals with P-0003 model (K scanned).
Usage: python3 -I out/labs/lab-c/analysis/r2_001_003_check.py  (repo root)
"""
import json, importlib.util
import numpy as np

spec = importlib.util.spec_from_file_location("P0003", "papers/P-0003/model.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def pos_arrays(res):
    S = json.load(open(res))["samples"]
    t = np.array([s["t"] for s in S])
    O = np.array([[[p["pos"] for p in s["particles"] if p["id"] == i][0] for i in (0, 1)] for s in S])
    return t, O, S

def run_pred(req, K):
    q = json.load(open(req)); m.K = float(K)
    return m.predict(q["setup"])

def sep(A):  # A: (T,2,2)
    return np.linalg.norm(A[:, 0] - A[:, 1], axis=1)

print("== 001 replicate (A-A at rest, T=2)")
rq = "requests/2026-11-18/r2/lab-c/001.json"; rs = "results/2026-11-18/r2/lab-c/001.json"
t, O, S = pos_arrays(rs)
q = json.load(open(rq))
print("   setup sep:", np.linalg.norm(np.subtract(q['setup']['particles'][0]['pos'], q['setup']['particles'][1]['pos'])), " events:", len(json.load(open(rs))['events']))
sO = sep(O)
for K in (17.74,):
    pred = run_pred(rq, K)
    P = np.array([[[p["pos"] for p in s["particles"] if p["id"] == i][0] for i in (0, 1)] for s in pred[:len(O)]])
    sP = sep(P)
    print(f"   K={K}: sep obs vs pred at selected t (pred can be unreliable after close approach)")
    for tt in (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0):
        k = int(round(tt / 0.001)) if tt * 1000 < len(t) else None
        k = min(int(round(tt / 0.001)), len(t) - 1)
        print(f"     t={t[k]:.3f}  obs={sO[k]:6.3f}  pred={sP[k]:6.3f}")
    print(f"   min obs separation {sO.min():.3f} at t={t[sO.argmin()]:.3f}; min pred separation {sP.min():.3f} at t={t[sP.argmin()]:.3f}")
    print(f"   max obs separation {sO.max():.3f} at t={t[sO.argmax()]:.3f}")

print("== 002/003 A-A approach and recede at r=6, speed 2 each (rest-law residuals)")
for name, req, res in [("002 approach", "requests/2026-11-18/r2/lab-c/002.json", "results/2026-11-18/r2/lab-c/002.json"),
                        ("003 recede", "requests/2026-11-18/r2/lab-c/003.json", "results/2026-11-18/r2/lab-c/003.json")]:
    t, O, S = pos_arrays(res)
    best = None
    for K in np.arange(14.0, 20.01, 0.05):
        pred = run_pred(req, K)
        P = np.array([[[p["pos"] for p in s["particles"] if p["id"] == i][0] for i in (0, 1)] for s in pred[:len(O)]])
        sse = ((O - P) ** 2).sum()
        if best is None or sse < best[1]:
            best = (float(K), sse, P)
    K, sse, P = best
    res_ = O - P
    rms = np.sqrt((res_ ** 2).mean(axis=0))
    print(f"   {name}: best rest-law K={K:.2f} rms x/y p0=({rms[0,0]:.4f},{rms[0,1]:.4f}) p1=({rms[1,0]:.4f},{rms[1,1]:.4f}) | mean res p0 {res_[:,0].mean(axis=0).round(4)} p1 {res_[:,1].mean(axis=0).round(4)} | sep min {sep(O).min():.3f}")
    print(f"     events={len(json.load(open(res))['events'])}  T={t[-1]}")
