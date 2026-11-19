"""Check out/papers/P-0008/model.py against the lab-b N=3,4 runs it claims (tracker, T=1).

Usage (repo root): python3 -I out/labs/lab-b/analysis/check_p0008_model.py
"""
import importlib.util
import json
import math
import os

REPO = os.getcwd()
spec = importlib.util.spec_from_file_location(
    "p0008", os.path.join(REPO, "out/papers/P-0008/model.py"))
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)

RUNS = [
    "2026-11-19/r2/lab-b/001",
    "2026-11-19/r1/lab-b/006",
    "2026-11-19/r1/lab-b/007",
    "2026-11-18/r3/lab-b/006",
]
for rid in RUNS:
    parts_ = rid.split("/")
    day, rnd, lab, nnn = parts_
    req = json.load(open(os.path.join(REPO, "requests", day, rnd, lab, nnn + ".json")))
    res = json.load(open(os.path.join(REPO, "results", day, rnd, lab, nnn + ".json")))
    pred = model.predict(req["setup"])
    by_t = {round(s["t"], 7): s for s in pred}
    n = len(req["setup"]["particles"])
    sq = 0.0
    cnt = 0
    mx = 0.0
    worst_mean = 0.0
    sm = [[0.0, 0.0] for _ in range(n)]
    nn = 0
    for s in res["samples"]:
        t = round(float(s["t"]), 7)
        if t <= 0 or t not in by_t:
            continue
        nn += 1
        for i in range(n):
            for k in range(2):
                d = s["particles"][i]["pos"][k] - by_t[t]["particles"][i]["pos"][k]
                sq += d * d
                cnt += 1
                sm[i][k] += d
                mx = max(mx, abs(d))
    rms = math.sqrt(sq / cnt)
    for i in range(n):
        for k in range(2):
            worst_mean = max(worst_mean, abs(sm[i][k] / nn))
    print("%s N=%d rms/coord %.4f max|res| %.3f max|mean res| %.4f samples %d events %d" %
          (rid, n, rms, mx, worst_mean, nn, len(res["events"])))
