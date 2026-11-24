#!/usr/bin/env python3
"""Fine 2D grid check of P-0025's coupling on lab-c's round-3 map runs (judge-style RMSE, unbiased SSE).

For each run, scan a multiplicative scale s on P-0025's K_TAB and the species ratio RATIO.
Reports the best (s, RATIO) on the pre-approach window (samples with separation >= CUT, t <= 2)
and the SSE contour width, to check whether the grid-limited GN fits were artifacts.
Usage: python3 -I grid_P0025_map_2026-11-24.py REPO_ROOT
"""
import importlib.util, json, math, sys
from pathlib import Path
import numpy as np

REPO = Path(sys.argv[1])
CUT = 3.0
RUNS = [f"2026-11-23/r3/lab-c/{n:03d}" for n in range(3, 13)]


def load_model():
    spec = importlib.util.spec_from_file_location("m", REPO / "papers" / "P-0025" / "model.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_data(rid):
    d, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / d / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / d / rnd / lab / f"{nnn}.json").read_text())
    return req["setup"], res["samples"]


def window_end(samples):
    seps = [math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in samples]
    for i in range(2, len(samples) - 2):
        if samples[i]["t"] >= 0.5 and sum(seps[i - 2:i + 3]) / 5 < CUT:
            return samples[i]["t"]
    return samples[-1]["t"]


def sse(mod, setup, samples, tmax, scale, ratio):
    mod.K_TAB = BASE_K * scale
    mod.RATIO = ratio
    pred = mod.predict(setup)
    pm = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    se, n = 0.0, 0
    for s in samples:
        t = round(s["t"], 9)
        if t <= 0 or t > tmax + 1e-9 or t not in pm:
            continue
        for p in s["particles"]:
            for k in range(2):
                se += (p["pos"][k] - pm[t][p["id"]][k]) ** 2
                n += 1
    return se, n


mod = load_model()
BASE_K = np.array(mod.K_TAB, dtype=float)
scales = np.linspace(0.7, 1.3, 25)
ratios = np.linspace(1.0, 1.8, 17)
for rid in RUNS:
    setup, samples = run_data(rid)
    tmax = min(window_end(samples), 2.0)
    best = None
    grid = np.zeros((len(scales), len(ratios)))
    for i, s in enumerate(scales):
        for j, r in enumerate(ratios):
            v, n = sse(mod, setup, samples, tmax, s, r)
            grid[i, j] = v
            if best is None or v < best[0]:
                best = (v, s, r, n)
    v, s_b, r_b, n = best
    # noise sigma from the best fit's residual (per coordinate)
    sig = math.sqrt(v / n)
    # 1-sigma-ish region: SSE within chi2 threshold of 2 params (delta SSE = 2.3 sigma^2 -> ~68%)
    ok = grid <= v + 2.3 * sig * sig
    i_idx, j_idx = np.where(ok)
    ks = [BASE_K[0] * scales[i] for i in i_idx]
    print(f"{rid} r0={math.dist(setup['particles'][0]['pos'], setup['particles'][1]['pos']):.2f} "
          f"tmax={tmax:.2f} best_scale={s_b:.3f} (K_A(r0)~{np.interp(math.dist(setup['particles'][0]['pos'], setup['particles'][1]['pos']), mod.R_TAB, BASE_K)*s_b:.2f}) "
          f"best_ratio={r_b:.2f} rms_noise={sig:.4f} "
          f"scale_range=[{scales[i_idx].min():.3f},{scales[i_idx].max():.3f}] "
          f"ratio_range=[{ratios[j_idx].min():.2f},{ratios[j_idx].max():.2f}]")
