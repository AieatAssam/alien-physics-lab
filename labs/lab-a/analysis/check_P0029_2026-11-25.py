"""Check P-0029 model against its 25 cited evidence runs: RMSE/L of predict() vs measured positions.
Usage: python3 -I check_P0029_2026-11-25.py <repo_root> <model_py_path>
"""
import importlib.util, json, os, sys
import numpy as np

ROOT, MODEL = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("p0029", MODEL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
L = 10.0
IDS = [("2026-11-23", 3, n) for n in range(5, 17)] + \
      [("2026-11-24", 1, n) for n in [9, 10, 13, 14, 15, 16, 17, 18]] + \
      [("2026-11-24", 2, n) for n in range(3, 8)]
rows = []
for day, rnd, n in IDS:
    req = json.load(open(os.path.join(ROOT, f"requests/{day}/r{rnd}/lab-a/{n:03d}.json")))
    res = json.load(open(os.path.join(ROOT, f"results/{day}/r{rnd}/lab-a/{n:03d}.json")))
    pred = mod.predict(req["setup"])
    P = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in pred])
    X = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in res["samples"]])
    m = min(len(P), len(X))
    err = np.sqrt(np.mean((P[:m] - X[:m]) ** 2)) / L
    rows.append((f"{day}/r{rnd}/{n:03d}", req["setup"]["duration"], round(float(err), 5)))
for r in rows:
    print(r)
errs = [r[2] for r in rows]
print("n =", len(errs), "min", min(errs), "max", max(errs), "bar 3x0.007 =", 0.021, "all below:", max(errs) <= 0.021)
