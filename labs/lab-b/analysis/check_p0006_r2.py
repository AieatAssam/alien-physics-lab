"""Out-of-sample check of P-0006 predictor on lab-b review requests 003 and 004.

Usage (from repo root): python3 -I out/labs/lab-b/analysis/check_p0006_r2.py

For each request: run papers/P-0006/model.py predict(setup), compare with tracker samples
at 0 < t <= 4, report per-particle rms and mean residual per coordinate, and the
maximum absolute residual. Also reports the paper's stated shared-law K values.
Pure python (math, json, importlib); reads only repo files.
"""
import importlib.util
import json
import math
import os

REPO = os.getcwd()
REQS = [
    "requests/2026-11-19/r2/lab-b/003.json",
    "requests/2026-11-19/r2/lab-b/004.json",
]
RESULTS = [
    "results/2026-11-19/r2/lab-b/003.json",
    "results/2026-11-19/r2/lab-b/004.json",
]

spec = importlib.util.spec_from_file_location(
    "p0006", os.path.join(REPO, "papers/P-0006/model.py"))
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


def load(p):
    with open(os.path.join(REPO, p)) as f:
        return json.load(f)


for rq, rs in zip(REQS, RESULTS):
    req = load(rq)
    res = load(rs)
    setup = req["setup"]
    pred = model.predict(setup)
    pred_by_t = {round(s["t"], 7): s for s in pred}
    n = len(setup["particles"])
    sq = [[0.0, 0.0] for _ in range(n)]
    sm = [[0.0, 0.0] for _ in range(n)]
    cnt = 0
    mx = 0.0
    for s in res["samples"]:
        t = round(float(s["t"]), 7)
        if t <= 0 or t > setup["duration"] + 1e-9 or t not in pred_by_t:
            continue
        cnt += 1
        for i in range(n):
            for k in range(2):
                d = s["particles"][i]["pos"][k] - pred_by_t[t]["particles"][i]["pos"][k]
                sq[i][k] += d * d
                sm[i][k] += d
                mx = max(mx, abs(d))
    print(req["request_id"], "cost", res["cost"], "events", len(res["events"]),
          "samples used", cnt)
    for i in range(n):
        sp = setup["particles"][i]["species"]
        rms = [math.sqrt(sq[i][k] / cnt) for k in range(2)]
        mean = [sm[i][k] / cnt for k in range(2)]
        print("  particle %d (%s): rms x %.4f y %.4f  mean x %+.4f y %+.4f" %
              (i, sp, rms[0], rms[1], mean[0], mean[1]))
    print("  max |residual| %.3f" % mx)
    r0 = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])
    print("  initial separation %.3f" % r0)
