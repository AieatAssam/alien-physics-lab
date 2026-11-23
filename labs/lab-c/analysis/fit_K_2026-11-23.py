#!/usr/bin/env python3
"""Free two-constant fit K_A(B), K_B(A) for a 2-body at-rest run (power P fixed), pure Python.

Usage: python3 -I fit_K_2026-11-23.py REPO_ROOT PAPER_MODEL P RID [RID...]
Gauss-Newton on residuals (measured - replayed) over all sample times t>0, both particles, x and y,
using the paper model's _step integrator with K overridden. Numerical Jacobian. Reports K +/- 1 sigma
(from J^T J with sigma^2 = chi2/dof) and the fit RMSE/L.
"""
import importlib.util, json, math, sys
from pathlib import Path

REPO = Path(sys.argv[1]); MODEL = sys.argv[2]; P = float(sys.argv[3]); RIDS = sys.argv[4:]
spec = importlib.util.spec_from_file_location("m", REPO / "papers" / MODEL / "model.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mod.P = P


def load(rid):
    d, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / d / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / d / rnd / lab / f"{nnn}.json").read_text())
    return req["setup"], res["samples"]


def replay(setup, KA, KB, tmax_needed):
    mod.K = {"A": KA, "B": KB}
    parts = setup["particles"]
    species = [p["species"] for p in parts]
    pos = [list(map(float, p["pos"])) for p in parts]
    vel = [list(map(float, p["vel"])) for p in parts]
    dt = float(setup["sample_dt"]); n = int(round(float(setup["duration"]) / dt))
    out = {}; t = 0.0
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
    meas = [(round(s["t"], 9), pm["id"], pm["pos"]) for s in samples if s["t"] > 0 for pm in s["particles"]]

    def resid(th):
        pred = replay(setup, th[0], th[1], None)
        return [c - pred[t][pid][k] for t, pid, p in meas for k, c in enumerate(p)]

    def ssq(th):
        return sum(x * x for x in resid(th))
    # coarse grid start (avoids divergence of plain Gauss-Newton)
    best = None
    for KA in [4 + 0.5 * i for i in range(17)]:
        for KB in [6 + 0.5 * j for j in range(17)]:
            v = ssq([KA, KB])
            if best is None or v < best[0]: best = (v, [KA, KB])
    th = best[1]
    for it in range(12):
        r0 = resid(th)
        eps = 1e-4
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
    cov_diag = [s2 * inv[0][0], s2 * inv[1][1]]
    rmse = math.sqrt(sum(x * x for x in r) / len(r)) / 10.0
    print(f"{rid} P={P}: K_A(B)={th[0]:.3f}+/-{math.sqrt(cov_diag[0]):.3f}  "
          f"K_B(A)={th[1]:.3f}+/-{math.sqrt(cov_diag[1]):.3f}  fit RMSE/L={rmse:.5f}  n={len(r)}")
