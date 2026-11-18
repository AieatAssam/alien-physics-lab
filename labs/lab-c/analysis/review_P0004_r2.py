"""Review check of P-0004 (lab-a): species-dependent coupling at r=5.
In-domain runs (lab-a): r1/001, r1/002 (A-B, r=5), r1/005 (A-C, r=5), r2/005 (A-C repeat, r=5).
Edge runs (lab-c, outside the paper's r=5 domain): 2026-11-18/r1/lab-c/007 (A-B, r=4), r1/lab-c/008 (A-C, r=4).
Positions only, papers/P-0004/model.py unchanged, then a per-run best-K scan over the two coefficients
on A (K_A) and the partner (K_partner) is NOT done here: only the rms / mean residual check.
Usage: python3 -I out/labs/lab-c/analysis/review_P0004_r2.py  (from repo root)
"""
import json, importlib.util
import numpy as np

spec = importlib.util.spec_from_file_location("P0004", "papers/P-0004/model.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def check(tag, req, res):
    q = json.load(open(req)); r = json.load(open(res))
    pred = m.predict(q["setup"])
    S = r["samples"]
    n = len(S)
    O = np.array([[[p["pos"] for p in s["particles"] if p["id"] == i][0] for i in (0, 1)] for s in S])
    P = np.array([[[p["pos"] for p in s["particles"] if p["id"] == i][0] for i in (0, 1)] for s in pred[:n]])
    sp = [p["species"] for p in q["setup"]["particles"]]
    res_ = O - P
    rms = np.sqrt((res_ ** 2).mean(axis=0))
    mean = res_.mean(axis=0)
    t = np.array([s["t"] for s in S])
    last = res_[t > t[-1] / 2]
    print(f"== {tag}: species {sp} sep {np.linalg.norm(np.subtract(q['setup']['particles'][0]['pos'], q['setup']['particles'][1]['pos'])):.2f} T={q['setup']['duration']} events={len(r['events'])}")
    for i in (0, 1):
        print(f"   p{i}({sp[i]}): rms x={rms[i,0]:.4f} y={rms[i,1]:.4f} | mean x={mean[i,0]:+.4f} y={mean[i,1]:+.4f} | 2nd-half mean x={last[:,i,0].mean():+.4f} y={last[:,i,1].mean():+.4f}")

if __name__ == "__main__":
    base = "requests/2026-11-18/r1/lab-a"
    rb = "results/2026-11-18/r1/lab-a"
    check("lab-a r1/001 (A-B, r=5)", f"{base}/001.json", f"{rb}/001.json")
    check("lab-a r1/002 (A-B, r=5)", f"{base}/002.json", f"{rb}/002.json")
    check("lab-a r1/005 (A-C, r=5)", f"{base}/005.json", f"{rb}/005.json")
    check("lab-a r2/005 (A-C repeat, r=5)", "requests/2026-11-18/r2/lab-a/005.json", "results/2026-11-18/r2/lab-a/005.json")
    check("lab-c r1/007 (A-B, r=4, edge)", "requests/2026-11-18/r1/lab-c/007.json", "results/2026-11-18/r1/lab-c/007.json")
    check("lab-c r1/008 (A-C, r=4, edge)", "requests/2026-11-18/r1/lab-c/008.json", "results/2026-11-18/r1/lab-c/008.json")
