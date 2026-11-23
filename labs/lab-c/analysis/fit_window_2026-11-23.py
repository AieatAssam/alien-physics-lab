#!/usr/bin/env python3
"""Two-constant K fit (K_A(B), K_B(A)) on the PRE-APPROACH window of A-B at-rest runs.

Usage: python3 -I fit_window_2026-11-23.py REPO_ROOT MODEL P CUT RID [RID ...]
- Window: samples up to the first measured separation < CUT (tracker noise ~0.05 per coord).
- Model: MODEL's _accel/_step with K overridden (P fixed). Constants grid + damped Gauss-Newton.
- Reports K +/- 1 sigma (chi2/dof scaled), window end time, RMSE/L over the window.
"""
import importlib.util, json, math, sys
from pathlib import Path

REPO = Path(sys.argv[1]); MODEL = sys.argv[2]; P = float(sys.argv[3]); CUT = float(sys.argv[4]); RIDS = sys.argv[5:]
spec = importlib.util.spec_from_file_location("m", REPO / "papers" / MODEL / "model.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mod.P = P


def load(rid):
    d, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / d / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / d / rnd / lab / f"{nnn}.json").read_text())
    return req["setup"], res["samples"]


def replay(setup, KA, KB, tmax):
    mod.K = {"A": KA, "B": KB}
    parts = setup["particles"]
    species = [p["species"] for p in parts]
    pos = [list(map(float, p["pos"])) for p in parts]
    vel = [list(map(float, p["vel"])) for p in parts]
    dt = float(setup["sample_dt"]); out = {}; t = 0.0
    n = int(round(tmax / dt))
    for i in range(1, n + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(mod.H, target - t)
            pos, vel = mod._step(pos, vel, species, h)
            t += h
        t = target
        out[target] = [list(p) for p in pos]
    return out


def solve2(A, b):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [(A[1][1] * b[0] - A[0][1] * b[1]) / det, (-A[1][0] * b[0] + A[0][0] * b[1]) / det], \
           [[A[1][1] / det, -A[0][1] / det], [-A[1][0] / det, A[0][0] / det]]


for rid in RIDS:
    setup, samples = load(rid)
    # cut at the first time (t >= 0.5) where the 5-sample running mean of the measured separation < CUT
    seps = [math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in samples]
    tcut = None
    for i in range(2, len(samples) - 2):
        if samples[i]["t"] >= 0.5 and sum(seps[i-2:i+3]) / 5 < CUT:
            tcut = samples[i]["t"]; break
    tmax = tcut if tcut is not None else samples[-1]["t"]
    if tmax < 1.0:
        print(f"{rid}: window too short ({tmax:.2f}), skipped"); continue
    meas = [(round(s["t"], 9), pm["id"], pm["pos"]) for s in samples if 0 < s["t"] < tmax for pm in s["particles"]]

    def resid(th):
        pred = replay(setup, th[0], th[1], tmax)
        return [c - pred[t][pid][k] for t, pid, p in meas for k, c in enumerate(p)]

    def ssq(th):
        return sum(x * x for x in resid(th))
    best = None
    for KA in [2 + 0.5 * i for i in range(21)]:
        for KB in [2 + 0.5 * j for j in range(21)]:
            v = ssq([KA, KB])
            if best is None or v < best[0]: best = (v, [KA, KB])
    th = best[1]
    for it in range(10):
        r0 = resid(th); eps = 1e-4
        r1 = resid([th[0] + eps, th[1]]); r2 = resid([th[0], th[1] + eps])
        Jc = [[(a - b) / eps for a, b in zip(r1, r0)], [(a - b) / eps for a, b in zip(r2, r0)]]
        JTJ = [[sum(x * y for x, y in zip(Jc[i], Jc[j])) for j in range(2)] for i in range(2)]
        JTr = [sum(x * y for x, y in zip(Jc[i], r0)) for i in range(2)]
        step, inv = solve2(JTJ, JTr)
        lam = 1.0; base = ssq(th)
        while lam > 1e-3:
            cand = [th[0] + lam * step[0], th[1] + lam * step[1]]
            if ssq(cand) < base: break
            lam /= 2
        th = cand
        if lam * max(abs(step[0]), abs(step[1])) < 1e-6: break
    r = resid(th); dof = max(len(r) - 2, 1)
    s2 = sum(x * x for x in r) / dof
    rmse = math.sqrt(sum(x * x for x in r) / len(r)) / 10.0
    r_start = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])
    print(f"{rid} P={P} r0={r_start:.2f} window_end={tmax:.2f} n={len(r)}: "
          f"K_A(B)={th[0]:.3f}+/-{math.sqrt(s2*inv[0][0]):.3f}  K_B(A)={th[1]:.3f}+/-{math.sqrt(s2*inv[1][1]):.3f}  "
          f"RMSE/L={rmse:.5f}")
