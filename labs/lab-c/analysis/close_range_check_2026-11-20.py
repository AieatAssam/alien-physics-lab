#!/usr/bin/env python3
"""Round-2 check of the round-1 close-range pair runs (2026-11-20/r1/lab-c/001-006).

Run with: python3 -I close_range_check_2026-11-20.py REPO_ROOT ANALYSIS_DIR

Compares the measured tracker pair separation with the pre-registered prediction in
close_prediction.json (P-0008 coefficients, integrated past r = 2.95). The tracker noise on a
separation is about sqrt(2) * 0.05 = 0.071, so the round-1 falsifier of 0.1 on any single sample
is only about 1.4 sigma. This script therefore reports (a) the per-sample rms residual and
(b) the mean residual over windows of 10 samples, against that noise, before the separation
reaches 0.5 (the window where the pair is still well-separated).
"""
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
ANALYSIS = Path(sys.argv[2])
NOISE_SEP = math.sqrt(2) * 0.05
pred_all = json.loads((ANALYSIS / "close_prediction.json").read_text())

for n in range(1, 7):
    rid = f"2026-11-20/r1/lab-c/{n:03d}"
    res = json.loads((REPO / "results" / "2026-11-20" / "r1" / "lab-c" / f"{n:03d}.json").read_text())
    pred = pred_all[f"{n:03d}"]
    pair = pred["pair"]
    pmap = {round(float(k), 9): float(v) for k, v in pred["separation_at_t"].items()}
    rows = []
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t not in pmap or t == 0.0:
            continue
        meas = math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"])
        rows.append((t, meas, pmap[t]))
    # Use only samples before the predicted pair reaches 0.5 (well separated, away from contact).
    early = [(t, m, p) for t, m, p in rows if p >= 0.5]
    res_all = [m - p for _, m, p in early]
    rms = math.sqrt(sum(r * r for r in res_all) / len(res_all)) if res_all else float("nan")
    worst = max(early, key=lambda x: abs(x[1] - x[2])) if early else None
    # 10-sample window means
    wins = []
    for i in range(0, len(early) - 9, 10):
        chunk = early[i:i + 10]
        mr = sum(m - p for _, m, p in chunk) / 10
        wins.append(mr)
    print(f"{rid} pair={pair} early_samples={len(early)} rms_resid={rms:.3f} "
          f"(noise {NOISE_SEP:.3f}) worst={abs(worst[1]-worst[2]):.3f} at t={worst[0]:.3f} "
          if worst else f"{rid} no early samples")
    print("    window means (10 samples):", [round(w, 3) for w in wins])
    print("    measured min sep:", round(min(m for _, m, _ in rows), 3),
          " predicted min sep:", round(min(p for _, _, p in rows), 3))
