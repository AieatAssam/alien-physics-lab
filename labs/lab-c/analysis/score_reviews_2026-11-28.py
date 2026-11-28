"""Score lab-c 2026-11-28/r1 review runs (011-020) against the papers' own predict().

Judged-style metric: RMSE over all samples, particles and coordinates, divided by L = 10.
Usage: python3 -I score_reviews_2026-11-28.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

REPO = sys.argv[1]
L = 10.0
DATE, ROUND, LAB = "2026-11-28", "r1", "lab-c"
PAPERS = {"P-0037": range(11, 16), "P-0036": range(16, 21)}


def load_model(pid):
    path = os.path.join(REPO, "papers", pid, "model.py")
    spec = importlib.util.spec_from_file_location("m_" + pid.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(pid, n):
    rid = f"{n:03d}"
    req = json.load(open(os.path.join(REPO, "requests", DATE, ROUND, LAB, rid + ".json")))
    res = json.load(open(os.path.join(REPO, "results", DATE, ROUND, LAB, rid + ".json")))
    setup = req["setup"]
    species = [p["species"] for p in setup["particles"]]
    out = {"run": f"{DATE}/{ROUND}/{LAB}/{rid}", "paper": pid, "species": species,
           "r0": round(math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"]), 4),
           "T": setup["duration"], "sample_dt": setup["sample_dt"],
           "cost": res.get("cost"), "budget_remaining": res.get("budget_remaining")}
    try:
        pred = load_model(pid).predict(setup)
    except ValueError as e:
        out["predict"] = f"refused: {e}"
        return out
    out["predict"] = "ok"
    meas = res["samples"]
    if len(meas) != len(pred):
        out["note"] = f"sample count mismatch meas {len(meas)} pred {len(pred)}"
    k = min(len(meas), len(pred))
    P = np.array([[p["pos"] for p in s["particles"]] for s in pred[:k]])
    M = np.array([[p["pos"] for p in s["particles"]] for s in meas[:k]])
    err = (P - M)
    rmse_all = math.sqrt(np.mean(err ** 2)) / L
    rmse_pos = math.sqrt(np.mean(err[1:] ** 2)) / L if k > 1 else float("nan")
    out["rmse_over_L"] = round(rmse_all, 5)
    out["rmse_over_L_excl_t0"] = round(rmse_pos, 5)
    out["min_sep_model"] = round(float(np.min(np.linalg.norm(P[:, 0] - P[:, 1], axis=1))), 3)
    out["min_sep_meas"] = round(float(np.min(np.linalg.norm(M[:, 0] - M[:, 1], axis=1))), 3)
    out["max_abs_resid"] = round(float(np.max(np.abs(err))), 4)
    return out


rows = []
for pid, ns in PAPERS.items():
    for n in ns:
        rows.append(run(pid, n))
for r in rows:
    print(json.dumps(r))
