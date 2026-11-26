#!/usr/bin/env python3
"""Lab-a review of P-0031, P-0032, P-0033, P-0034 from own runs 2026-11-26/r1/lab-a/001-012.

Judged-style check: RMSE(predict(setup) positions, tracker positions) / L, L = 10.
Domain check is done explicitly from claim.json (species, particle count, every initial pair distance in r_range),
and predict() is also called; a ValueError is recorded.
Bar = 3 x predicted_error.

Run: python3 -I review_round2_2026-11-26.py <repo_root>
"""
import importlib.util
import json
import os
import sys
import itertools

import numpy as np

ROOT = sys.argv[1]
L = 10.0
MAP = {
    "P-0032": ["001", "002", "003"],
    "P-0033": ["004", "005", "006"],
    "P-0031": ["007", "008", "009"],
    "P-0034": ["010", "011", "012"],
}


def load_model(pid):
    spec = importlib.util.spec_from_file_location(pid, os.path.join(ROOT, "papers", pid, "model.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


summary = {}
for pid, rids in MAP.items():
    claim = json.load(open(os.path.join(ROOT, "papers", pid, "claim.json")))
    c = claim["claims"][0]
    dom = c["domain"]
    bar = 3 * c["predicted_error"]
    mod = load_model(pid)
    print("==", pid, "domain", dom, "bar", round(bar, 4))
    rows = []
    for rid in rids:
        req = json.load(open(os.path.join(ROOT, "requests", "2026-11-26", "r1", "lab-a", rid + ".json")))
        res = json.load(open(os.path.join(ROOT, "results", "2026-11-26", "r1", "lab-a", rid + ".json")))
        assert res["status"] == "ok", res
        parts = req["setup"]["particles"]
        species = "".join(p["species"] for p in parts)
        seps = [float(np.linalg.norm(np.subtract(a["pos"], b["pos"]))) for a, b in itertools.combinations(parts, 2)]
        in_species = all(p["species"] in dom["species"] for p in parts)
        in_n = len(parts) <= dom["max_particles"]
        in_r = all(dom["r_range"][0] <= s <= dom["r_range"][1] for s in seps)
        in_T = req["setup"]["duration"] <= 2.0 if pid != "P-0034" else req["setup"]["duration"] <= 1.0
        if pid == "P-0032":
            in_T = req["setup"]["duration"] <= 0.6
        if pid == "P-0031":
            in_T = req["setup"]["duration"] <= 2.0
        try:
            pred = mod.predict(req["setup"])
            pe = None
        except Exception as e:  # noqa
            pred = None
            pe = repr(e)
        if pred is None:
            print(rid, species, "predict() error:", pe, "in_domain(species,N,r)=", in_species, in_n, in_r)
            rows.append((rid, False, None))
            continue
        P = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in pred])
        X = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda q: q["id"])] for s in res["samples"]])
        m = min(len(P), len(X))
        err = float(np.sqrt(np.mean((P[:m] - X[:m]) ** 2)) / L)
        dom_ok = in_species and in_n and in_r and in_T
        print("%s %s N=%d seps=%s T=%.2f n=%d RMSE/L=%.5f in_domain=%s (sp=%s N=%s r=%s T=%s) %s" % (
            rid, species, len(parts), ["%.3f" % s for s in seps], req["setup"]["duration"], m, err,
            dom_ok, in_species, in_n, in_r, in_T, "<=bar" if err <= bar else "ABOVE bar"))
        rows.append((rid, dom_ok, err))
    summary[pid] = rows

json.dump({k: [{"rid": r, "in_domain": d, "rmse_over_L": e} for r, d, e in v] for k, v in summary.items()},
          open(os.path.join(ROOT, "out", "labs", "lab-a", "analysis", "review_round2_2026-11-26.json"), "w"), indent=2)
