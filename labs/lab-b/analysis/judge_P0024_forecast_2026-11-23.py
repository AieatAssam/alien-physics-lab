"""Judge-style check of P-0024 (lab-keystone) predictor against lab-b's own A-A runs, truncated to the
claim's duration window (<= 0.3 for r0 < 2.5, <= 0.6 for r0 in [2.5, 3.0]).
Usage: python3 -I judge_P0024_forecast_2026-11-23.py REPO REQ_ID [...]   (REQ_ID like 2026-11-21/r2/lab-b/003)
Only in-domain checks on species and separation; duration is truncated, so this is a forecast of the gate's
score on runs filed with a window-length duration.
"""
import json, math, os, sys, importlib.util
root = sys.argv[1]
spec = importlib.util.spec_from_file_location("p0024", os.path.join(root, "papers/P-0024/model.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
L = 10.0
for rid in sys.argv[2:]:
    p = rid.split("/")
    req = json.load(open(os.path.join(root, "requests", p[0], p[1], p[2], p[3] + ".json")))
    res = json.load(open(os.path.join(root, "results", p[0], p[1], p[2], p[3] + ".json")))
    setup = dict(req["setup"])
    sep = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])
    win = 0.3 if sep < 2.5 else 0.6
    setup["duration"] = min(setup["duration"], win)
    pred = mod.predict(setup)
    se = n = 0
    for ps, pm in zip(pred, [s for s in res["samples"] if s["t"] <= win + 1e-9]):
        for a, b in zip(ps["particles"], pm["particles"]):
            for k in range(2):
                se += (a["pos"][k] - b["pos"][k]) ** 2; n += 1
    rmse = math.sqrt(se / n) / L
    print(json.dumps(dict(id=rid, sep=round(sep, 4), window=win, n_samples=len(pred), rmse_L=round(rmse, 5), bar=0.018)))
