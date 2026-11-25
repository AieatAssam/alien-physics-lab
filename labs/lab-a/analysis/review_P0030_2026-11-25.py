#!/usr/bin/env python3
"""Review of P-0030 (lab-vernier) from lab-a's own review-account runs 2026-11-25/r2/lab-a/001-004.

Judge-style check: RMSE between predict(setup) positions and measured tracker positions, divided by L = 10.
Domain check: predict() raises ValueError outside the claim's domain; that is recorded per run.
Bar: 3 x predicted_error = 3 x 0.008 = 0.024.

Run: python3 -I review_P0030_2026-11-25.py <repo_root>
"""
import importlib.util
import json
import os
import sys

import numpy as np

ROOT = sys.argv[1]
L = 10.0
BAR = 3 * 0.008
spec = importlib.util.spec_from_file_location(
    "p0030", os.path.join(ROOT, "papers", "P-0030", "model.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for i in range(1, 5):
    rid = "%03d" % i
    req = json.load(open(os.path.join(ROOT, "requests", "2026-11-25", "r2", "lab-a", rid + ".json")))
    res = json.load(open(os.path.join(ROOT, "results", "2026-11-25", "r2", "lab-a", rid + ".json")))
    assert res["status"] == "ok", res
    sep = float(np.linalg.norm(np.subtract(req["setup"]["particles"][1]["pos"], req["setup"]["particles"][0]["pos"])))
    species = "".join(p["species"] for p in req["setup"]["particles"])
    try:
        pred = mod.predict(req["setup"])
    except ValueError as e:
        print(rid, "OUT OF DOMAIN:", e)
        continue
    P = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in pred])
    X = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in res["samples"]])
    m = min(len(P), len(X))
    err = float(np.sqrt(np.mean((P[:m] - X[:m]) ** 2)) / L)
    print("%s species=%s sep0=%.4f T=%.2f n=%d RMSE/L=%.5f  %s" % (
        rid, species, sep, req["setup"]["duration"], m, err, "<= bar" if err <= BAR else "ABOVE bar"))
