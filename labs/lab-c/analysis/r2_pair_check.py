#!/usr/bin/env python3
"""Round-2 check: P-0008 pair law (K / r^2.5, P-0008 coefficients) at initial separation 2.0.

Run with: python3 -I r2_pair_check.py REPO_ROOT

P-0008's predict() refuses separations below 2.95, so this script calls its integrator
(_step, _accel) directly on the same coefficients, with no domain check. It is an
extrapolation test, not a judged replication. Runs: lab-c r0 = 2.0 pairs, T = 0.4
(2026-11-17/r3/lab-c/001, 006-010 at rest; 2026-11-18/r1/lab-c/001, 002, 003, 009).
Reports the measured-minus-predicted pair separation, rms and 10-sample window means before
the predicted separation falls below 0.5, compared with the tracker separation noise 0.071.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("p0008", REPO / "papers" / "P-0008" / "model.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
NOISE_SEP = math.sqrt(2) * 0.05
RUNS = [
    "2026-11-17/r3/lab-c/001", "2026-11-17/r3/lab-c/006", "2026-11-17/r3/lab-c/007",
    "2026-11-17/r3/lab-c/008", "2026-11-17/r3/lab-c/009", "2026-11-17/r3/lab-c/010",
    "2026-11-18/r1/lab-c/001", "2026-11-18/r1/lab-c/002", "2026-11-18/r1/lab-c/003",
    "2026-11-18/r1/lab-c/009",
]

for rid in RUNS:
    date, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / date / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / date / rnd / lab / f"{nnn}.json").read_text())
    parts = req["setup"]["particles"]
    species = [p["species"] for p in parts]
    pos = [list(map(float, p["pos"])) for p in parts]
    vel = [list(map(float, p["vel"])) for p in parts]
    pair = "".join(species)
    H = 0.0005  # fine internal step; P-0008's H = 0.002 is too coarse for r ~ 1 collisions
    t = 0.0
    pred = {}
    for s in res["samples"]:
        target = round(s["t"], 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = mod._step(pos, vel, species, h)
            t += h
        t = target
        pred[target] = math.dist(pos[0], pos[1])
    rows = []
    for s in res["samples"]:
        tt = round(s["t"], 9)
        if tt == 0.0:
            continue
        meas = math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"])
        rows.append((tt, meas, pred[tt]))
    early = [r for r in rows if r[2] >= 0.5]
    rms = math.sqrt(sum((m - p) ** 2 for _, m, p in early) / len(early)) if early else float("nan")
    wins = [round(sum(m - p for _, m, p in early[i:i + 10]) / len(early[i:i + 10]), 3)
            for i in range(0, len(early) - 9, 10)]
    print(f"{rid} pair={pair} moving={int(any(abs(v) > 0 for p in parts for v in p['vel']))} "
          f"early={len(early)} rms={rms:.3f} (noise {NOISE_SEP:.3f}) windows={wins} "
          f"meas_min={min(m for _, m, _ in rows):.3f} pred_min={min(p for _, _, p in rows):.3f}")
