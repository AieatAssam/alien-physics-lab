"""Run each reviewed paper's own model.py predict(setup) against the review runs.

Residuals are split into windows so that the encounter regime is shown separately.
Requires: papers/<P>/model.py (imports only math/numpy), results of 2026-11-19/r1/lab-vernier.
"""
import importlib.util
import json
import numpy as np
from load_results import load

BASE = "/home/runner/work/alien-physics-lab/alien-physics-lab/"
R = BASE + "results/2026-11-19/r1/lab-vernier/"
REQ = BASE + "requests/2026-11-19/r1/lab-vernier/"


def predictor(paper):
    spec = importlib.util.spec_from_file_location(paper, BASE + f"papers/{paper}/model.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.predict


def residuals(paper, run, windows):
    req = json.load(open(REQ + run + ".json"))
    d = load(R + run + ".json")
    pred = predictor(paper)(req["setup"])
    t_p = np.array([s["t"] for s in pred])
    out = {}
    for w0, w1 in windows:
        errs = []
        for k, s in enumerate(pred):
            t = s["t"]
            if not (w0 - 1e-9 <= t <= w1 + 1e-9):
                continue
            idx = int(np.argmin(np.abs(d["t"] - t)))
            for pid in range(len(s["particles"])):
                errs.append(np.array(s["particles"][pid]["pos"]) - np.array(d["pos"][pid][idx]))
        e = np.array(errs)
        out[(w0, w1)] = (float(np.sqrt(np.mean(e ** 2))), float(np.mean(e[:, 0])), float(np.mean(e[:, 1])), float(np.abs(e).max()), len(e))
    return out


if __name__ == "__main__":
    wins = [(0.0, 1.1), (1.1, 2.0), (0.0, 2.0)]
    for paper, run in [("P-0003", "007"), ("P-0005", "008"), ("P-0005", "009")]:
        r = residuals(paper, run, wins)
        print(f"{paper} on run {run}")
        for w, (rms, mx, my, mabs, n) in r.items():
            print(f"   window {w}: rms {rms:.4f}  mean res ({mx:+.4f},{my:+.4f})  max|res| {mabs:.3f}  n {n}")
