#!/usr/bin/env python3
"""Pre-registered predictions for 2026-11-20/r2/lab-c/004-007 (written before any result).

Run with: python3 -I pred_2026-11-20_r2_shortrange.py REPO_ROOT OUT_JSON
Prediction = P-0008 power law (K/r^2.5, P-0008 coefficients), integrated at fine step 0.0005,
evaluated at the request sample times. Tracker separation noise is sqrt(2)*0.05 = 0.071.
Falsifier, per run: mean residual over the first 0.2 of the run (or the whole run for T=0.4)
more than 0.05 from zero AND the late-window mean (last 30% of samples) beyond 0.1 with the
sign predicted by the sub-power-law hypothesis (AA: measured > predicted; AC: measured < predicted).
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
OUT = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("p0008", REPO / "papers" / "P-0008" / "model.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

SETUPS = {
    "004": ("AA", 1.5, 0.4, 0.0002),
    "005": ("AC", 1.5, 0.4, 0.0002),
    "006": ("CC", 1.5, 0.4, 0.0002),
    "007": ("AA", 2.5, 1.0, 0.0005),
}
out = {}
for key, (pair, r0, T, dt) in SETUPS.items():
    species = list(pair)
    pos = [[5.0 - r0 / 2, 5.0], [5.0 + r0 / 2, 5.0]]
    vel = [[0.0, 0.0], [0.0, 0.0]]
    n = int(round(T / dt))
    H = 0.0005
    t = 0.0
    seps = {}
    for i in range(n + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = mod._step(pos, vel, species, h)
            t += h
        t = target
        seps[f"{target:.4f}"] = math.dist(pos[0], pos[1])
    out[key] = {"pair": pair, "r0": r0, "T": T, "dt": dt, "separation_at_t": seps}
OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
print("wrote", OUT, {k: round(v["separation_at_t"][f"{v['T']:.4f}"], 3) for k, v in out.items()})
