#!/usr/bin/env python3
"""Sensitivity of the judge metric (RMSE/L) to perturbations of P-0025's constants.

Loads papers/P-0025/model.py (paper's own predictor, read-only), perturbs K_TAB by a scale
factor and RATIO, and scores lab-c's round-3 map runs that are strictly inside P-0025's domain.
Usage: python3 -I sens_P0025_2026-11-24.py REPO_ROOT
"""
import importlib.util, json, math, sys
from pathlib import Path

REPO = Path(sys.argv[1])
L = 10.0
RUNS = [f"2026-11-23/r3/lab-c/{n:03d}" for n in range(3, 13)]


def load_model():
    spec = importlib.util.spec_from_file_location("m", REPO / "papers" / "P-0025" / "model.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rmse_for(mod, rid):
    d, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / d / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / d / rnd / lab / f"{nnn}.json").read_text())
    pred = mod.predict(req["setup"])
    pm = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    se, n = 0.0, 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t not in pm:
            continue
        for p in s["particles"]:
            for k in range(2):
                se += (p["pos"][k] - pm[t][p["id"]][k]) ** 2
                n += 1
    r0 = math.dist(req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"])
    return math.sqrt(se / n) / L, r0


def main():
    base = load_model()
    configs = [("paper", 1.0, base.RATIO)]
    for scale in (0.8, 0.9, 1.1, 1.2):
        configs.append((f"K x{scale}", scale, base.RATIO))
    for ratio in (1.2, 1.6):
        configs.append((f"ratio {ratio}", 1.0, ratio))
    print(f"{'config':14s} " + " ".join(f"{r.split('/')[-1]:>7s}" for r in RUNS))
    for name, scale, ratio in configs:
        mod = load_model()
        mod.K_TAB = base.K_TAB * scale
        mod.RATIO = ratio
        vals = []
        for rid in RUNS:
            e, r0 = rmse_for(mod, rid)
            vals.append(e)
        print(f"{name:14s} " + " ".join(f"{v:7.5f}" for v in vals))
    print("bar (3 x 0.007) = 0.0210; noise floor expected ~0.005")


if __name__ == "__main__":
    main()
