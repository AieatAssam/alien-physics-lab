"""Judge-style RMSE/L of the P-0025 predictor against lab-b runs, truncated to t <= 2.0.
Usage: python3 -I check_P0025_model_2026-11-23.py <repo_root> [suffix ...]
Reads model from out/papers/P-0025/model.py (pure numpy/math).
"""
import sys, json, math, os, importlib.util
sys.path.insert(0, "/tmp/lab-b-pylib")
import numpy as np
root = sys.argv[1]
spec = importlib.util.spec_from_file_location("p0025", os.path.join(root, "out/papers/P-0025/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
L = 10.0
SUFFIXES = sys.argv[2:] or [
    "2026-11-23/r2/lab-b/006", "2026-11-23/r2/lab-b/007", "2026-11-23/r2/lab-b/008",
    "2026-11-23/r1/lab-b/006", "2026-11-23/r2/lab-b/009", "2026-11-22/r3/lab-b/002",
]
for sfx in SUFFIXES:
    req = json.load(open(os.path.join(root, "requests", sfx + ".json")))
    res = json.load(open(os.path.join(root, "results", sfx + ".json")))
    setup = dict(req["setup"]); setup["duration"] = min(setup["duration"], 2.0)
    pred = m.predict(setup)
    sq = n = 0
    for ps in pred:
        rs = next(s for s in res["samples"] if abs(s["t"] - ps["t"]) < 1e-9)
        if ps["t"] <= 0:
            continue
        for pp, mm in zip(ps["particles"], sorted(rs["particles"], key=lambda q: q["id"])):
            for k in range(2):
                sq += (pp["pos"][k] - mm["pos"][k]) ** 2; n += 1
    r0 = math.dist(req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"])
    print(json.dumps({"id": sfx, "r0": round(r0, 3), "T_used": setup["duration"],
                      "rmse_L": round(math.sqrt(sq / n) / L, 5)}))
