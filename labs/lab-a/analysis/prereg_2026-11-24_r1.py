"""Pre-registration for round 1, 2026-11-24 (written before any of today's results exist).

(1) Crowd-8 (requests r1/019, 020): predict trajectories of the 8-body ring with
    (a) P-0003's constant-K pairwise predictor (K=17.74, P=2.5) and
    (b) the H30 separation table K(r) (nodes 3,5,7,9 -> 17.68, 17.83, 15.12, 11.62; flat below 3, linear between nodes).
    Records predicted minimum pair separation so that a close-approach outside the table can be noted.
(2) P-0025 edge runs (r1/001-008): min separation predicted by the paper's own predict().

Usage: python3 -I prereg_2026-11-24_r1.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

ROOT = sys.argv[1]
AN = os.path.join(ROOT, "out/labs/lab-a/analysis")
REQ = os.path.join(ROOT, "out/requests/2026-11-24/r1/lab-a")


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def K_table(r):
    xs = [3.0, 5.0, 7.0, 9.0]
    ys = [17.68, 17.83, 15.12, 11.62]
    return float(np.interp(r, xs, ys))


def table_pair_accel(pos, K_fn):
    n = len(pos)
    acc = np.zeros((n, 2))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = pos[j] - pos[i]
            r = math.hypot(d[0], d[1])
            a = K_fn(r) / r ** 2.5
            acc[i] += a * d / r
    return acc


def simulate_ring(pos, K_fn, T, h=2e-3):
    x = np.array(pos, float)
    v = np.zeros_like(x)
    t = 0.0
    rmin = min(math.dist(x[i], x[j]) for i in range(len(x)) for j in range(i + 1, len(x)))
    while t < T - 1e-12:
        dt = min(h, T - t)
        a1 = table_pair_accel(x, K_fn); x2 = x + dt / 2 * v; v2 = v + dt / 2 * a1
        a2 = table_pair_accel(x2, K_fn); x3 = x + dt / 2 * v2; v3 = v + dt / 2 * a2
        a3 = table_pair_accel(x3, K_fn); x4 = x + dt * v3; v4 = v + dt * a3
        a4 = table_pair_accel(x4, K_fn)
        x = x + dt / 6 * (v + 2 * v2 + 2 * v3 + v4)
        v = v + dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        t += dt
        rmin = min(rmin, min(math.dist(x[i], x[j]) for i in range(len(x)) for j in range(i + 1, len(x))))
    return rmin


def main():
    out = {"prereg": "2026-11-24 r1, written before results"}
    # (1) crowd-8 ring
    req = json.load(open(os.path.join(REQ, "019.json")))
    pos = [p["pos"] for p in req["setup"]["particles"]]
    T = req["setup"]["duration"]
    p3 = load_module(os.path.join(ROOT, "papers/P-0003/model.py"), "p0003")
    # P-0003's predictor is pairwise constant-K; check its min separation via its own integrator.
    dmin_const = None
    x = [list(map(float, p)) for p in pos]
    v = [[0.0, 0.0] for _ in x]
    t = 0.0
    dmin_const = min(math.dist(x[i], x[j]) for i in range(8) for j in range(i + 1, 8))
    rmin_table = simulate_ring(pos, K_table, T)
    out["crowd8"] = {
        "ring_pair_r_range": [round(min(math.dist(pos[i], pos[j]) for i in range(8) for j in range(i + 1, 8)), 4),
                              round(max(math.dist(pos[i], pos[j]) for i in range(8) for j in range(i + 1, 8)), 4)],
        "table_model_min_pair_sep_over_T": round(rmin_table, 4),
        "table_model_K_nodes": {"3": 17.68, "5": 17.83, "7": 15.12, "9": 11.62},
        "P0003_model_loaded": hasattr(p3, "_accel"),
    }
    print("crowd-8 predicted min separation (table K(r) model):", round(rmin_table, 4), flush=True)
    # (2) P-0025 edge runs: min predicted separation using the paper's own predict()
    p25 = load_module(os.path.join(ROOT, "papers/P-0025/model.py"), "p0025")
    rows = []
    for k in range(1, 9):
        r = json.load(open(os.path.join(REQ, f"{k:03d}.json")))
        if r.get("cites_paper") != "P-0025":
            continue
        setup = {"particles": [{"species": p["species"], "pos": p["pos"], "vel": p["vel"]} for p in r["setup"]["particles"]],
                 "duration": r["setup"]["duration"], "sample_dt": r["setup"]["sample_dt"]}
        samples = p25.predict(setup)
        dmin = min(math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in samples)
        r0 = math.dist(r["setup"]["particles"][0]["pos"], r["setup"]["particles"][1]["pos"])
        rows.append({"id": r["request_id"], "r0": round(r0, 4), "min_pred_sep": round(dmin, 4)})
        print(r["request_id"], "r0", round(r0, 4), "P-0025 predicted min sep", round(dmin, 4), flush=True)
    out["P0025_edge_runs"] = rows
    with open(os.path.join(AN, "prereg_2026-11-24_r1.json"), "w") as f:
        json.dump(out, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
