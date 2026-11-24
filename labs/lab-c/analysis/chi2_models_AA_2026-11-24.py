#!/usr/bin/env python3
"""chi2/n (sigma 0.05, window r >= 3) of candidate A-A pair laws on runs 2026-11-24/r2/lab-c/002-004.
Models (per-particle accel toward partner):
  M1 power law P=3.10 K=47.00 (joint fit from the same runs)
  M2 P-0027 table, exponent 2.5, piecewise-linear K nodes 3..9
  M3 P-0024 pair law, (G/2)/r^P with G=23.63, P=2.099 (per particle)
Usage: python3 -I chi2_models_AA_2026-11-24.py REPO_ROOT
"""
import json, math, sys
from pathlib import Path
REPO = Path(sys.argv[1])
NODES = {3: 17.683, 4: 17.701, 5: 17.834, 6: 16.617, 7: 15.121, 8: 13.432, 9: 11.624}
def K_table(r):
    rs = sorted(NODES)
    r = min(max(r, rs[0]), rs[-1])
    for a, b in zip(rs, rs[1:]):
        if a <= r <= b:
            w = (r - a) / (b - a); return NODES[a] * (1 - w) + NODES[b] * w
MODELS = {
    "M1 P3.10 K47.0": lambda r: 47.0 / r ** 3.10,
    "M2 P-0027 table (P2.5)": lambda r: K_table(r) / r ** 2.5,
    "M3 P-0024 law (P2.099)": lambda r: (23.63 / 2) / r ** 2.099,
}
def traj(r0, acc, times, h=0.0005):
    r, v, t, out = r0, 0.0, 0.0, {}
    for tn in times:
        while t < tn - 1e-12:
            s = min(h, tn - t)
            def F(rr, vv): return (vv, -2.0 * acc(max(rr, 1e-3)))
            a1 = F(r, v)
            a2 = F(r + s / 2 * a1[0], v + s / 2 * a1[1])
            a3 = F(r + s / 2 * a2[0], v + s / 2 * a2[1])
            a4 = F(r + s * a3[0], v + s * a3[1])
            r += s / 6 * (a1[0] + 2 * a2[0] + 2 * a3[0] + a4[0])
            v += s / 6 * (a1[1] + 2 * a2[1] + 2 * a3[1] + a4[1])
            t += s
        out[tn] = r
    return out
for nnn in ["002", "003", "004"]:
    req = json.loads((REPO / "requests/2026-11-24/r2/lab-c" / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results/2026-11-24/r2/lab-c" / f"{nnn}.json").read_text())
    r0 = math.dist(req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"])
    samples = []
    for s in res["samples"]:
        if s["t"] <= 0: continue
        x = [q["pos"] for q in s["particles"]]
        if math.dist(x[0], x[1]) < 3.0: break
        samples.append((s["t"], x))
    times = [t for t, _ in samples]
    line = f"{nnn} r0={r0:.1f} window_end={times[-1]:.2f} n_samples={len(times)}: "
    for name, acc in MODELS.items():
        rt = traj(r0, acc, times)
        se = 0.0; n = 0
        for t, x in samples:
            half = rt[t] / 2
            for k, pred in ((0, (5 - half, 5.0)), (1, (5 + half, 5.0))):
                for c in range(2):
                    se += (x[k][c] - pred[c]) ** 2; n += 1
        line += f" | {name}: chi2/n={se/(0.05**2)/n:.3f}"
    print(line)
