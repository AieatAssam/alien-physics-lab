"""Edge-of-domain review designs for P-0028 (A-A crowd, N <= 8, pair distances in [3, 9], T <= 1).

Eight A particles on a ring of radius R about (5, 5). Adjacent pair distance 2R sin(22.5 deg),
opposite pair distance 2R. R = 4.2 gives 3.21 to 8.40; R = 4.4 gives 3.37 to 8.80. Both are inside [3, 9].
For each design: (a) check the paper's own predict() accepts it, (b) RMSE/L between the paper model
and a constant-K variant (K = 17.683, the r = 3 node) to see whether the run can discriminate the
K(r) table from constant K, (c) RMSE/L of the model against its own zero-force initial state
(the null scale). Bar for P-0028 is 3 x 0.007 = 0.021.

Usage: python3 -I design_P0028_ring_2026-11-25.py   (paper model is another lab's code; run it -I)
"""
import importlib.util
import json
import math
import os

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
PAPER = f"{REPO}/papers/P-0028/model.py"
L = 10.0


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ring_setup(R, phase_deg, T, n=8, cx=5.0, cy=5.0):
    parts = []
    for k in range(n):
        a = math.radians(phase_deg + 360.0 * k / n)
        parts.append({"species": "A",
                      "pos": [round(cx + R * math.cos(a), 6), round(cy + R * math.sin(a), 6)],
                      "vel": [0.0, 0.0]})
    return {"particles": parts, "duration": T, "sample_dt": T / 2000.0}


def rmse_over_L(a_samples, b_samples):
    se, n = 0.0, 0
    bmap = {round(s["t"], 9): s for s in b_samples}
    for s in a_samples:
        q = bmap[round(s["t"], 9)]
        for p, r in zip(s["particles"], q["particles"]):
            se += (p["pos"][0] - r["pos"][0]) ** 2 + (p["pos"][1] - r["pos"][1]) ** 2
            n += 2
    return math.sqrt(se / n) / L


if __name__ == "__main__":
    paper = load(PAPER, "p0028")
    designs = [(4.2, 0.0), (4.2, 22.5), (4.4, 0.0), (4.4, 22.5)]
    out = []
    for R, ph in designs:
        setup = ring_setup(R, ph, 1.0)
        pts = [p["pos"] for p in setup["particles"]]
        seps = [math.dist(pts[i], pts[j]) for i in range(8) for j in range(i + 1, 8)]
        try:
            table_samples = paper.predict(setup)
        except ValueError as ex:
            print("REFUSED", R, ph, ex)
            continue
        # constant-K variant of the same model
        const = load(PAPER, "p0028c")
        const.K = lambda r: 17.683
        const_samples = const.predict(setup)
        init = [{"t": s["t"], "particles": [{"id": p["id"], "pos": setup["particles"][p["id"]]["pos"]}
                                          for p in s["particles"]]} for s in table_samples]
        d_const = rmse_over_L(table_samples, const_samples)
        d_null = rmse_over_L(table_samples, init)
        print(f"R={R} phase={ph} min_sep={min(seps):.3f} max_sep={max(seps):.3f} "
              f"table-vs-constK={d_const:.4f} model-vs-null={d_null:.4f} n_samples={len(table_samples)}")
        out.append({"R": R, "phase": ph, "setup": setup})
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "p0028_designs_2026-11-25.json"), "w"), indent=1)
