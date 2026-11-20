#!/usr/bin/env python3
"""Round 3 (2026-11-20): finalisation checks for the round-2 review runs.

Run with: python3 -I review_runs_2026-11-20.py REPO_ROOT

002, 003: P-0010-c1 (A-A, r0 = 6 and 8, at rest, T = 6).
  - judged error and the time at which the model's position error first exceeds 0.2 (it blows up at contact)
  - one coupling-scale fit s for P-0010 (G0, G1 multiplied by s), chi2 at sigma 0.05 per coordinate,
    window = samples before the measured separation first drops below 1.5 (the approach).
    For 003 the whole run is used (its closest approach is 4.53).
001: P-0009-c1 (B, C, C triangle, side 5, at rest, T = 2).
  - judged error, per-coordinate rms residual, and the zero-force null, for the replicate bar (0.07).
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
SIGMA = 0.05
SIDE = 10.0


def load(pid):
    path = REPO / "papers" / pid / "model.py"
    spec = importlib.util.spec_from_file_location("m_" + pid.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(rid):
    date, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / date / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / date / rnd / lab / f"{nnn}.json").read_text())
    return req, res


def table(samples):
    return {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in samples}


def judged(pred, truth):
    tab = table(pred)
    sq = []
    for s in truth["samples"]:
        row = tab[round(s["t"], 9)]
        for p in s["particles"]:
            q = row[p["id"]]
            sq.append((q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2)
    return math.sqrt(sum(sq) / len(sq)) / SIDE


def chi2_window(pred, truth, tmax):
    tab = table(pred)
    tot = 0.0
    n = 0
    for s in truth["samples"]:
        if s["t"] > tmax + 1e-9:
            continue
        row = tab[round(s["t"], 9)]
        for p in s["particles"]:
            q = row[p["id"]]
            tot += (q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2
            n += 2
    return tot / SIGMA ** 2, n


def sep_of(p):
    d = {q["id"]: q["pos"] for q in p}
    return math.dist(d[0], d[1])


def parabola_min(xs, ys):
    m = len(xs)
    Sx = sum(xs); Sx2 = sum(x * x for x in xs); Sx3 = sum(x ** 3 for x in xs); Sx4 = sum(x ** 4 for x in xs)
    Sy = sum(ys); Sxy = sum(x * y for x, y in zip(xs, ys)); Sx2y = sum(x * x * y for x, y in zip(xs, ys))
    M = [[Sx4, Sx3, Sx2], [Sx3, Sx2, Sx], [Sx2, Sx, m]]
    v = [Sx2y, Sxy, Sy]

    def det(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
                - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    d = det(M)
    coef = []
    for col in range(3):
        mk = [row[:] for row in M]
        for i in range(3):
            mk[i][col] = v[i]
        coef.append(det(mk) / d)
    a, b, _ = coef
    return -b / (2 * a), a


def main():
    p10 = load("P-0010")
    base = (p10.G0, p10.G1)
    for rid, window_cut in [("2026-11-20/r2/lab-c/002", 1.5), ("2026-11-20/r2/lab-c/003", None)]:
        req, res = run(rid)
        pred = p10.predict(req["setup"])
        j = judged(pred, res)
        seps = [(s["t"], sep_of(s["particles"])) for s in res["samples"]]
        if window_cut is None:
            tmax = max(t for t, _ in seps)
        else:
            tmax = next((t for t, d in seps if d < window_cut), max(t for t, _ in seps))
        # first time the model's own positions are off by more than 0.2 in RMS
        tab = table(pred)
        first_bad = None
        for s in res["samples"]:
            row = tab[round(s["t"], 9)]
            e = math.sqrt(sum((row[p["id"]][0] - p["pos"][0]) ** 2 + (row[p["id"]][1] - p["pos"][1]) ** 2
                              for p in s["particles"]) / len(s["particles"]))
            if e > 0.2:
                first_bad = s["t"]
                break
        grid = [0.90, 0.93, 0.96, 0.98, 1.00, 1.02, 1.04, 1.06, 1.10]
        chis = []
        for sc in grid:
            p10.G0, p10.G1 = base[0] * sc, base[1] * sc
            c, n = chi2_window(p10.predict(req["setup"]), res, tmax)
            chis.append(c / n)
        p10.G0, p10.G1 = base
        s0, a = parabola_min(grid, chis)
        i_best = min(range(len(grid)), key=lambda i: chis[i])
        print(f"{rid}  min sep {min(d for _, d in seps):.3f}  judged {j:.5f} ({j / 0.01:.0f}x predicted_error 0.01)")
        print(f"    model error > 0.2 first at t={first_bad}  window t<= {tmax:.3f}")
        print(f"    best scale s = {s0:.4f}  (curvature a={a:.1f}); chi2/N by scale: " +
              "  ".join(f"{g:.2f}:{c:.2f}" for g, c in zip(grid, chis)))
    # 001: P-0009
    p9 = load("P-0009")
    req, res = run("2026-11-20/r2/lab-c/001")
    pred = p9.predict(req["setup"])
    j = judged(pred, res)
    tab = table(pred)
    sq = []
    for s in res["samples"]:
        row = tab[round(s["t"], 9)]
        for p in s["particles"]:
            q = row[p["id"]]
            sq.append((q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2)
    rms_coord = math.sqrt(sum(sq) / (2 * len(sq)))
    print(f"2026-11-20/r2/lab-c/001  P-0009 judged {j:.5f} (bar 0.03), per-coordinate rms {rms_coord:.4f} (bar 0.07)")
    # zero-force null: free drift from the request's initial state
    null_sq = []
    init = {i: pv["pos"] for i, pv in enumerate(req["setup"]["particles"])}
    init_vel = {i: pv["vel"] for i, pv in enumerate(req["setup"]["particles"])}
    for s in res["samples"]:
        t = s["t"]
        for p in s["particles"]:
            q = init[p["id"]]
            v = init_vel[p["id"]]
            null_sq.append((q[0] + v[0] * t - p["pos"][0]) ** 2 + (q[1] + v[1] * t - p["pos"][1]) ** 2)
    print(f"    zero-force null per-coordinate rms (drift from t=0 positions): "
          f"{math.sqrt(sum(null_sq) / (2 * len(null_sq))):.4f}  (samples at t=0 are part of the data)")
    # samples with census events
    print("    events:", len(res.get("events", [])))


if __name__ == "__main__":
    main()
