#!/usr/bin/env python3
"""Sensitivity of the judged error (side 10) of P-0016's model to a coupling scale s, at the claim's full T = 0.6.
Truth = P-0016 model with COUP scaled by s (noise-free); prediction = unscaled P-0016 model.
Judged error = RMSE over matched (t, particle) positions / 10. Noise floor for tracker sigma 0.05: 0.0071.
Run: python3 -I sens_P0016_T06_2026-11-21.py REPO_ROOT
"""
import importlib.util, math, sys
from pathlib import Path
REPO = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("p0016", REPO / "papers/P-0016/model.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
COUP0 = dict(m.COUP)
setup = {"particles": [{"species": "A", "pos": [4.5, 5.0], "vel": [0.0, 0.0]},
                       {"species": "C", "pos": [5.5, 5.0], "vel": [0.0, 0.0]}],
         "duration": 0.6, "sample_dt": 0.0005}
pred = m.predict(setup)
def err(a, b):
    tb = {round(s["t"], 9): s for s in b}
    sq = []
    for s in a:
        t = round(s["t"], 9)
        for p, q in zip(s["particles"], tb[t]["particles"]):
            sq.append((p["pos"][0]-q["pos"][0])**2 + (p["pos"][1]-q["pos"][1])**2)
    return math.sqrt(sum(sq)/len(sq))/10.0
for s in [0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.05, 1.1, 1.15, 1.2, 1.3, 1.5]:
    m.COUP = {k: s*v for k, v in COUP0.items()}
    truth = m.predict(setup)
    m.COUP = dict(COUP0)
    e = err(pred, truth)
    print(f"s={s:.2f}  judged error vs P-0016 model = {e:.4f}  (bar 0.018)  {'would PASS' if e <= 0.018 else 'FAIL'}")
