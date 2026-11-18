"""Score paper predictors against lab-c result files (positions only, no fitting).
Usage: python3 -I check_papers_r1.py   (run from repo root)
Reports per-particle rms residual (x, y), mean residual per 10-unit time segment, and max |res|.
"""
import json, importlib.util, os, sys
import numpy as np

ROOT = "."

def load_model(pid):
    spec = importlib.util.spec_from_file_location(pid, os.path.join(ROOT, f"papers/{pid}/model.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def score(model, tag, req_path, res_path, seg_len=10.0, tmax=None):
    q = json.load(open(req_path)); r = json.load(open(res_path))
    pred = model.predict(q["setup"])
    S = r["samples"]
    if tmax is not None:
        S = [s for s in S if s["t"] <= tmax + 1e-9]
    pt = np.array([s["t"] for s in pred]); ot = np.array([s["t"] for s in S])
    pred = pred[:len(S)] if len(pred) >= len(S) else pred
    idx = np.arange(len(S))
    assert len(pred) == len(S) and np.allclose(pt[:len(S)], ot, atol=1e-6), ("time grids differ", len(pt), len(ot), pt[:3], ot[:3])
    ids = sorted({p["id"] for p in S[0]["particles"]})
    print(f"== {tag}: {q['purpose'][:90]}")
    print(f"   setup: {[(p['species'], p['pos'], p['vel']) for p in q['setup']['particles']]} T={q['setup']['duration']} dt={q['setup']['sample_dt']}")
    for i in ids:
        P = np.array([[p["pos"] for p in pred[k]["particles"] if p["id"] == i][0] for k in idx])
        O = np.array([[p["pos"] for p in s["particles"] if p["id"] == i][0] for s in S])
        res = O - P
        rms = np.sqrt((res ** 2).mean(axis=0))
        seg = np.floor(ot / seg_len).astype(int)
        segs = " ".join(f"[{10*k}:{res[seg==k].mean(axis=0)[0]:+.3f},{res[seg==k].mean(axis=0)[1]:+.3f}]" for k in np.unique(seg))
        print(f"   id{i}: rms x={rms[0]:.4f} y={rms[1]:.4f} | max|res|={np.abs(res).max():.3f} | seg mean res {segs}")

if __name__ == "__main__":
    p2 = load_model("P-0002")
    score(p2, "P-0002 on r1/006 (review edge)", "requests/2026-11-18/r1/lab-c/006.json", "results/2026-11-18/r1/lab-c/006.json")
    # sanity: P-0002's own evidence-scale run from our own lab, r2/007 (lone C, speed 1, T=100)
    score(p2, "P-0002 on r2/007 (lone C, sanity)", "requests/2026-11-17/r2/lab-c/007.json", "results/2026-11-17/r2/lab-c/007.json")
    p3 = load_model("P-0003")
    score(p3, "P-0003 on r3/003 (A-A rest, r=4, T=0.8; in domain)", "requests/2026-11-17/r3/lab-c/003.json", "results/2026-11-17/r3/lab-c/003.json")
    score(p3, "P-0003 on r3/001 (A-A rest, r=2; out of domain)", "requests/2026-11-17/r3/lab-c/001.json", "results/2026-11-17/r3/lab-c/001.json")
    score(p3, "P-0003 on r3/004 (A-A rest, r=8; out of domain, T=2)", "requests/2026-11-17/r3/lab-c/004.json", "results/2026-11-17/r3/lab-c/004.json", tmax=2.0)
