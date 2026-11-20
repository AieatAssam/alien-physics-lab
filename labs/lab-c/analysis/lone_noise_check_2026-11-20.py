#!/usr/bin/env python3
"""Round-2 check of P-0011 (noise of a lone tracker) against lab-c's own lone-particle runs.

Run with: python3 -I lone_noise_check_2026-11-20.py REPO_ROOT
Residual = measured position minus P-0011 model.py (reflected free flight, uses velocity).
Reports per-coordinate sd, mean, and kurtosis, pooled and per species.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("p0011", REPO / "papers" / "P-0011" / "model.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

RUNS = [
    "2026-11-17/r1/lab-c/001", "2026-11-17/r1/lab-c/002", "2026-11-17/r2/lab-c/007",
    "2026-11-18/r1/lab-c/006", "2026-11-17/r3/lab-c/011", "2026-11-17/r3/lab-c/012",
]
by_species = {}
for rid in RUNS:
    date, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / date / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / date / rnd / lab / f"{nnn}.json").read_text())
    pred = mod.predict(req["setup"])
    sp = req["setup"]["particles"][0]["species"]
    pm = {round(s["t"], 9): s["particles"][0]["pos"] for s in pred}
    rx, ry = [], []
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t == 0.0:
            continue  # the t=0 sample is the start; keep it out of the noise statistic
        q = pm[t]
        p = s["particles"][0]["pos"]
        rx.append(p[0] - q[0])
        ry.append(p[1] - q[1])
    n = len(rx)
    sd = lambda v: math.sqrt(sum((a - sum(v) / len(v)) ** 2 for a in v) / (len(v) - 1))
    mean_x, mean_y = sum(rx) / n, sum(ry) / n
    print(f"{rid} sp={sp} T={req['setup']['duration']} n={n} sd_x={sd(rx):.4f} sd_y={sd(ry):.4f} "
          f"mean_x={mean_x:+.4f} mean_y={mean_y:+.4f}")
    by_species.setdefault(sp, []).extend(rx + ry)
    by_species.setdefault("ALL", []).extend(rx + ry)

for sp, v in sorted(by_species.items()):
    n = len(v)
    m = sum(v) / n
    s2 = sum((a - m) ** 2 for a in v) / (n - 1)
    k = (sum((a - m) ** 4 for a in v) / n) / (s2 ** 2) if s2 > 0 else float("nan")
    print(f"pooled {sp}: values={n} sd_per_coord={math.sqrt(s2):.4f} mean={m:+.4f} kurtosis={k:.2f}")
