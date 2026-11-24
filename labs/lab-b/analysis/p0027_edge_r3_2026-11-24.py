"""Edge of P-0027's domain: r0 = 3.0 and near it. Minimum separation along the table model, and judged
RMSE/L of the model with K scaled by small factors (noise-free comparison against the table model).
Usage: python3 -I p0027_edge_r3_2026-11-24.py <paper_dir>
"""
import sys, math, importlib.util, os
sys.path.insert(0, "/tmp/lab-b-pylib")
import numpy as np
paper_dir = sys.argv[1]
spec = importlib.util.spec_from_file_location("m", os.path.join(paper_dir, "model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
K0 = m.K_TAB.copy()
L = 10.0

def run(r0, T, f, h_dt=0.01):
    m.K_TAB = K0 * f
    c = 5.0
    p = [{"species": "A", "pos": [c - r0 / 2, c], "vel": [0, 0]}, {"species": "A", "pos": [c + r0 / 2, c], "vel": [0, 0]}]
    s = m.predict({"particles": p, "duration": T, "sample_dt": h_dt})
    return s

def min_sep(samples):
    return min(math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in samples)

for r0, T in [(3.0, 1.5), (3.0, 1.0), (3.0, 0.5), (3.5, 1.5), (4.0, 1.5), (4.5, 1.5)]:
    base = run(r0, T, 1.0)
    ms = min_sep(base)
    row = [f"r0={r0} T={T} min_sep(model)={ms:.4f}"]
    for f in (0.99, 0.995, 1.005, 1.01):
        alt = run(r0, T, f)
        sq = cnt = 0
        for a, b in zip(base, alt):
            if a["t"] <= 0 or a["t"] > T + 1e-9:
                continue
            for pa, pb in zip(a["particles"], b["particles"]):
                for k in range(2):
                    sq += (pa["pos"][k] - pb["pos"][k]) ** 2; cnt += 1
        row.append(f"x{f}:{math.sqrt(sq/cnt)/L:.4f}")
    print("  ".join(row))
m.K_TAB = K0.copy()
