#!/usr/bin/env python3
"""Refined exponent scan on lab-c's long-window runs 2026-11-24/r1/lab-c/013-022 (T = 6, tracker only).

Replaces the P grid in profile_P_2026-11-24.py, whose P = 2.0 and 2.25 fits hit optimiser failures
(start values never moved). Here the starting K scales with the fixed P so the optimiser begins near
the answer. Two tests per P:
  (a) per-run K_A, K_B (P fixed): slope of K_A against r0 (flat = one constant K describes all r0);
  (b) joint fit: one common K_A, K_B across all ten runs (P fixed): chi2/n per run and overall.
Window: samples until the measured separation first drops below 3.0 (R_CUT). sigma = 0.05.
Integrator RK4 with step 0.005 (coarser than profile_P_2026-11-24.py for speed; checked by the
agreement of P = 2.5 per-run values with that script to about 0.1 percent).

Usage: python3 -I profile_P_refine_2026-11-24.py REPO_ROOT
"""
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

REPO = Path(sys.argv[1])
RIDS = [f"2026-11-24/r1/lab-c/{n:03d}" for n in range(13, 23)]  # T = 6 runs
SIGMA = 0.05
R_CUT = 3.0
DT = 0.005
PGRID = [2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2]


def load(rid):
    d, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / d / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / d / rnd / lab / f"{nnn}.json").read_text())
    t = np.array([s["t"] for s in res["samples"]])
    xy = np.array([[p["pos"] for p in s["particles"]] for s in res["samples"]])
    return req, t, xy


def simulate(KA, KB, P, x0, times):
    pos = np.array(x0, float)
    vel = np.zeros((2, 2))

    def acc(p):
        d = p[1] - p[0]
        r = math.hypot(d[0], d[1])
        f = d / r ** (P + 1)
        return np.array([KA * f, -KB * f])

    out = np.zeros((len(times), 2, 2))
    out[0] = pos
    t = 0.0
    for i in range(1, len(times)):
        target = times[i]
        while t < target - 1e-12:
            h = min(DT, target - t)
            k1p, k1v = vel, acc(pos)
            p2, v2 = pos + h / 2 * k1p, vel + h / 2 * k1v
            k2p, k2v = v2, acc(p2)
            p3, v3 = pos + h / 2 * k2p, vel + h / 2 * k2v
            k3p, k3v = v3, acc(p3)
            p4, v4 = pos + h * k3p, vel + h * k3v
            k4p, k4v = v4, acc(p4)
            pos = pos + h / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
            vel = vel + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            t += h
        out[i] = pos
    return out


def window_n(xy):
    r = np.hypot(*(xy[:, 1, :] - xy[:, 0, :]).T)
    below = np.where(r < R_CUT)[0]
    return below[0] if len(below) else len(xy)


def main():
    data = []
    for rid in RIDS:
        req, t, xy = load(rid)
        x0 = [p["pos"] for p in req["setup"]["particles"]]
        n = window_n(xy)
        data.append(dict(rid=rid, r0=math.dist(x0[0], x0[1]),
                         orient="H" if abs(x0[0][1] - x0[1][1]) < 1e-9 else "V",
                         x0=x0, t=t[:n], xy=xy[:n]))

    print("P      slope dK_A/dr0   K_A(r0=4..8 pooled range)   joint K_A   joint K_B   joint chi2/n  max per-run chi2/n(joint)")
    for P in PGRID:
        scale = 6.0 ** (P - 2.5)
        KAs = []
        for d in data:
            def resid(p):
                return (simulate(p[0], p[1], P, d["x0"], d["t"]) - d["xy"]).ravel() / SIGMA
            f = least_squares(resid, x0=[8.0 * scale, 11.0 * scale], bounds=([0.1, 0.1], [200, 200]))
            d["fit"] = f.x
            KAs.append((d["r0"], f.x[0], np.sum(f.fun ** 2) / f.fun.size))
        r0s = np.array([a for a, _, _ in KAs]); KA = np.array([b for _, b, _ in KAs])
        slope = np.polyfit(r0s, KA, 1)[0]

        def joint(p):
            return np.concatenate([(simulate(p[0], p[1], P, d["x0"], d["t"]) - d["xy"]).ravel() / SIGMA
                                   for d in data])
        jf = least_squares(joint, x0=[8.0 * scale, 11.0 * scale], bounds=([0.1, 0.1], [200, 200]))
        jchi = np.sum(jf.fun ** 2) / jf.fun.size
        per = []
        for d in data:
            res = (simulate(jf.x[0], jf.x[1], P, d["x0"], d["t"]) - d["xy"]).ravel() / SIGMA
            per.append(np.sum(res ** 2) / res.size)
        print(f"{P:4.2f}  {slope:+9.4f}      {KA.min():6.3f} .. {KA.max():6.3f}           "
              f"{jf.x[0]:8.3f}  {jf.x[1]:8.3f}  {jchi:9.3f}     {max(per):9.3f}", flush=True)
        for d, (a, b, c) in zip(data, KAs):
            print(f"      {d['rid']} {d['orient']} r0={a:4.1f}  per-run K_A={b:7.3f}  chi2/n={c:6.3f}", flush=True)


if __name__ == "__main__":
    main()
