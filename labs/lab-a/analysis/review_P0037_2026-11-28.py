#!/usr/bin/env python3
"""Review of P-0037 (lab-keystone) from lab-a's review-account runs 2026-11-28/r1/lab-a/001-005.

Judge-style check: RMSE between predict(setup) positions and measured tracker positions, divided by L = 10.
Domain check: predict() raises ValueError outside the claim's domain or on contact; recorded per run.
Bar: 3 x predicted_error = 3 x 0.007 = 0.021.

Run: python3 -I review_P0037_2026-11-28.py <repo_root>
"""
import importlib.util
import json
import os
import sys

import numpy as np

ROOT = sys.argv[1]
L = 10.0
BAR = 3 * 0.007
spec = importlib.util.spec_from_file_location(
    "p0037", os.path.join(ROOT, "papers", "P-0037", "model.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for i in range(1, 6):
    rid = "%03d" % i
    req = json.load(open(os.path.join(ROOT, "requests", "2026-11-28", "r1", "lab-a", rid + ".json")))
    res = json.load(open(os.path.join(ROOT, "results", "2026-11-28", "r1", "lab-a", rid + ".json")))
    sep = float(np.linalg.norm(np.subtract(req["setup"]["particles"][1]["pos"], req["setup"]["particles"][0]["pos"])))
    T = req["setup"]["duration"]
    try:
        pred = mod.predict(req["setup"])
    except ValueError as e:
        print(rid, "sep0=%.4f T=%.2f OUT OF DOMAIN: %s" % (sep, T, e))
        continue
    P = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in pred])
    X = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in res["samples"]])
    m = min(len(P), len(X))
    err = float(np.sqrt(np.mean((P[:m] - X[:m]) ** 2)) / L)
    print("%s sep0=%.4f T=%.2f n=%d RMSE/L=%.5f  %s" % (
        rid, sep, T, m, err, "<= bar" if err <= BAR else "ABOVE bar"))
