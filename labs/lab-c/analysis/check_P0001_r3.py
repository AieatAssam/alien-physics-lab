"""Check P-0001 model.py against lab-c round-3 review requests 011 (speed 3.36, T=100, y-walls)
and 012 (exact diagonal, corners). Usage: python3 out/labs/lab-c/analysis/check_P0001_r3.py
Runs the paper's own predict(setup) and reports residuals per coordinate, per 10-unit segment."""
import json, importlib.util, os
import numpy as np

ROOT = "."
spec = importlib.util.spec_from_file_location("p1", os.path.join(ROOT, "papers/P-0001/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


def check(n):
    q = json.load(open(f"requests/2026-11-17/r3/lab-c/{n}.json"))
    r = json.load(open(f"results/2026-11-17/r3/lab-c/{n}.json"))
    pred = m.predict(q["setup"])
    pt = np.array([s["t"] for s in pred])
    rt = np.array([s["t"] for s in r["samples"]])
    assert np.allclose(pt, rt, atol=1e-9), "time grids differ"
    ids = [p["id"] for p in pred[0]["particles"]]
    print(f"== {n}: {q['purpose'][:80]}")
    for i in ids:
        P = np.array([[p["pos"] for p in s["particles"] if p["id"] == i][0] for s in pred])
        O = np.array([[p["pos"] for p in s["particles"] if p["id"] == i][0] for s in r["samples"]])
        res = O - P
        rms = np.sqrt((res ** 2).mean(axis=0))
        print(f"  particle {i}: rms residual x={rms[0]:.4f} y={rms[1]:.4f} overall={np.sqrt((res**2).mean()):.4f}")
        # residual in 10-unit segments (time)
        seg = np.floor(rt / 10.0).astype(int)
        for k in np.unique(seg):
            mk = seg == k
            mean = res[mk].mean(axis=0)
            print(f"    seg t[{10*k},{10*k+10}) mean residual x={mean[0]:+.4f} y={mean[1]:+.4f}")
        # wall-hit times from the model (x or y at 0 or 10 with velocity reversal)
        vx = q["setup"]["particles"][i]["vel"]
        print(f"    max |obs-pred| = {np.abs(res).max():.3f}")


for n in ["011", "012"]:
    check(n)
