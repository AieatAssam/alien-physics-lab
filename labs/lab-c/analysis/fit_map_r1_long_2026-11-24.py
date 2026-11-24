#!/usr/bin/env python3
"""Fit an A-B pair law a = K / r^P (separate K_A, K_B, free P) to the long-window research runs
2026-11-24/r1/lab-c/013-024 (lab-c's own runs, tracker only, noise sigma about 0.05 per coordinate).

Usage: python3 -I fit_map_r1_long_2026-11-24.py REPO_ROOT
Model (A at index 0, B at index 1, d = x_B - x_A, r = |d|):
    a_A = +K_A * d / r^(P+1)     (A pulled toward B)
    a_B = -K_B * d / r^(P+1)     (B pulled toward A)
Integrated with RK4 (step 0.002), no walls (the window is chosen so that no wall is reached).
The fit window is every sample with measured separation >= R_CUT (default 3.0), taken from the
start of the run until the first sample that falls below R_CUT. Per-coordinate noise assumed 0.05.
Reports: fit K_A, K_B, P (least squares), chi2/n with sigma 0.05, and a constant-K fixed-P=2.5 fit.
"""
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

REPO = Path(sys.argv[1])
RIDS = [f"2026-11-24/r1/lab-c/{n:03d}" for n in range(13, 25)]
SIGMA = 0.05
R_CUT = 3.0
DT = 0.002


def load(rid):
    d, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / d / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / d / rnd / lab / f"{nnn}.json").read_text())
    t = np.array([s["t"] for s in res["samples"]])
    xy = np.array([[p["pos"] for p in s["particles"]] for s in res["samples"]])  # (n, 2, 2)
    return req, t, xy


def simulate(params, x0, times, fixedP=None):
    if fixedP is None:
        KA, KB, P = params
    else:
        KA, KB = params
        P = fixedP
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


def window_end(t, xy):
    r = np.hypot(*(xy[:, 1, :] - xy[:, 0, :]).T)
    below = np.where(r < R_CUT)[0]
    n = below[0] if len(below) else len(t)
    return n  # samples [0, n) are inside the window


def main():
    rows = []
    for rid in RIDS:
        req, t, xy = load(rid)
        setup = req["setup"]
        x0 = [p["pos"] for p in setup["particles"]]
        r0 = math.dist(x0[0], x0[1])
        orient = "H" if abs(x0[0][1] - x0[1][1]) < 1e-9 else "V"
        n = window_end(t, xy)
        tw, xw = t[:n], xy[:n]
        res = {}

        def resid(p, fixedP=None):
            sim = simulate(p, x0, tw, fixedP)
            return (sim - xw).ravel() / SIGMA

        # free fit: KA, KB, P
        f = least_squares(resid, x0=[8.0, 11.0, 2.5],
                          bounds=([0.1, 0.1, 1.5], [30, 30, 4.0]))
        chi = np.sum(f.fun ** 2) / f.fun.size
        # constant-K fit with P fixed at 2.5 (the claim's exponent)
        g = least_squares(lambda p: resid(p, 2.5), x0=[8.0, 11.0],
                          bounds=([0.1, 0.1], [30, 30]))
        chi25 = np.sum(g.fun ** 2) / g.fun.size
        rows.append((rid, orient, r0, t[-1], n, f.x, chi, g.x, chi25))

    print("run                         or   r0    Twin  nwin   KA     KB     P      chi2/n  | KA(P2.5) KB(P2.5) chi2/n(P2.5)")
    for rid, orient, r0, tw_end, n, fx, chi, gx, chi25 in rows:
        print(f"{rid}  {orient}  {r0:4.1f}  {tw_end:5.2f}  {n:4d}  "
              f"{fx[0]:6.3f} {fx[1]:6.3f} {fx[2]:6.3f}  {chi:7.3f}  |  "
              f"{gx[0]:6.3f}   {gx[1]:6.3f}   {chi25:7.3f}")


if __name__ == "__main__":
    main()
