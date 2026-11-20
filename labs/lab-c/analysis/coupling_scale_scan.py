#!/usr/bin/env python3
"""Per-run coupling-scale fit for two-body runs against a paper's model.py.

Run with: python3 -I coupling_scale_scan.py REPO_ROOT PAPER

For each lab-c run in a fixed list, the paper's predictor is evaluated with its coupling
multiplied by s, for s in {0.94, 0.97, 1.00, 1.03, 1.06}. chi2(s) = sum over particle-samples
of |measured - predicted|^2 / sigma^2 with sigma = 0.05 per coordinate (the tracker noise).
A parabola through the five points gives the best scale s0 and its 1-sigma width
(delta chi2 = 1). This is a sceptic's check of the coefficients, not the editor's metric:
the judged metric (RMSE / 10) cannot resolve a few-percent coupling error at this noise.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
PAPER = sys.argv[2]
SIGMA = 0.05
SCALES = [0.94, 0.97, 1.00, 1.03, 1.06]

RUNS = {
    "P-0010": [
        "2026-11-18/r2/lab-c/004", "2026-11-17/r3/lab-c/004",
        "2026-11-19/r1/lab-c/007", "2026-11-19/r1/lab-c/008", "2026-11-19/r1/lab-c/009",
        "2026-11-19/r1/lab-c/010", "2026-11-19/r1/lab-c/011", "2026-11-19/r1/lab-c/012",
        "2026-11-19/r1/lab-c/013", "2026-11-19/r1/lab-c/014", "2026-11-19/r1/lab-c/015",
        "2026-11-19/r1/lab-c/016", "2026-11-19/r1/lab-c/017", "2026-11-19/r1/lab-c/018",
        "2026-11-19/r1/lab-c/019",
        "2026-11-19/r2/lab-c/001", "2026-11-19/r2/lab-c/003", "2026-11-19/r2/lab-c/004",
        "2026-11-19/r2/lab-c/005", "2026-11-19/r2/lab-c/006", "2026-11-19/r2/lab-c/007",
        "2026-11-19/r2/lab-c/008", "2026-11-19/r2/lab-c/009", "2026-11-19/r2/lab-c/010",
        "2026-11-19/r2/lab-c/011",
    ],
    "P-0009": ["2026-11-19/r1/lab-c/023", "2026-11-19/r1/lab-c/024", "2026-11-19/r1/lab-c/025"],
}


def load_model(pid):
    path = REPO / "papers" / pid / "model.py"
    spec = importlib.util.spec_from_file_location("m_" + pid.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scale_model(mod, pid, s):
    """Scale the pair coupling of the paper model by s, without touching its code."""
    if pid == "P-0010":
        mod.G0 = 1.5100 * s
        mod.G1 = -0.0920 * s
    elif pid == "P-0009":
        mod.COUP = {k: v * s for k, v in MODEL_COUP0.items()}


def chi2(pred, truth):
    table = {round(x["t"], 9): {p["id"]: p["pos"] for p in x["particles"]} for x in pred}
    tot = 0.0
    for x in truth:
        row = table[round(x["t"], 9)]
        for p in x["particles"]:
            q = row[p["id"]]
            tot += (q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2
    return tot / SIGMA ** 2


def parabola(xs, ys):
    """Least-squares quadratic y = a x^2 + b x + c; returns (x0, curvature a)."""
    n = len(xs)
    sx = sum(xs); sx2 = sum(x * x for x in xs); sx3 = sum(x ** 3 for x in xs); sx4 = sum(x ** 4 for x in xs)
    sy = sum(ys); sxy = sum(x * y for x, y in zip(xs, ys)); sx2y = sum(x * x * y for x, y in zip(xs, ys))
    M = [[sx4, sx3, sx2], [sx3, sx2, sx], [sx2, sx, n]]
    v = [sx2y, sxy, sy]
    # Cramer's rule for 3x3
    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    d = det(M)
    cols = []
    for k in range(3):
        mk = [row[:] for row in M]
        for i in range(3):
            mk[i][k] = v[i]
        cols.append(det(mk) / d)
    a, b, _c = cols
    return -b / (2 * a), a


def main():
    results = {}
    for pid, rids in RUNS.items():
        mod0 = load_model(pid)
        if pid == "P-0009":
            global MODEL_COUP0
            MODEL_COUP0 = dict(mod0.COUP)
        for rid in rids:
            date, rnd, lab, nnn = rid.split("/")
            req = json.loads((REPO / "requests" / date / rnd / lab / f"{nnn}.json").read_text())
            res = json.loads((REPO / "results" / date / rnd / lab / f"{nnn}.json").read_text())
            setup = req["setup"]
            vals = []
            for s in SCALES:
                mod = load_model(pid)
                if pid == "P-0009":
                    mod.COUP = dict(MODEL_COUP0)
                scale_model(mod, pid, s)
                vals.append(chi2(mod.predict(setup), res["samples"]))
            s0, a = parabola(SCALES, vals)
            sig = math.sqrt(1.0 / a) if a > 0 else float("nan")
            npts = sum(len(x["particles"]) for x in res["samples"]) * 2
            species = "".join(p["species"] for p in setup["particles"])
            results[rid] = (species, setup["duration"], s0, sig, vals[2] / npts * 1.0, npts)
            print(f"{rid}  {pid} sp={species} T={setup['duration']}  s0={s0:.4f} +/- {sig:.4f}  "
                  f"chi2(s=1)/N={vals[2] / (npts):.3f}  dchi2(s=1 vs s0)={vals[2] - min(vals):.2f}")
    # pooled over all runs of a paper
    for pid in RUNS:
        s0s = [v[2] for k, v in results.items() if k in RUNS[pid] and v[3] == v[3]]
        sigs = [v[3] for k, v in results.items() if k in RUNS[pid] and v[3] == v[3]]
        if not s0s:
            continue
        w = [1 / s ** 2 for s in sigs]
        mean = sum(x * wi for x, wi in zip(s0s, w)) / sum(w)
        print(f"{pid} inverse-variance mean s = {mean:.4f} +/- {1 / math.sqrt(sum(w)):.4f} over {len(s0s)} runs")


MODEL_COUP0 = {}
if __name__ == "__main__":
    main()
