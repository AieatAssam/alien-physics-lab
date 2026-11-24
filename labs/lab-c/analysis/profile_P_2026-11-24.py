#!/usr/bin/env python3
"""Exponent profile on lab-c's long-window research runs 2026-11-24/r1/lab-c/013-024 (tracker only).

For each fixed exponent P on a grid, each run is fitted with its own K_A and K_B (P fixed), using the
window before the measured separation drops below R_CUT = 3.0. If one constant K with this exponent
describes the law, the per-run K_A should not depend on the initial separation r0. The script
prints per-run K_A, K_B, chi2/n (sigma 0.05) and, per P, the slope of K_A against r0 across the
T = 6 runs (H and V pooled) and the chi2/n spread.

Usage: python3 -I profile_P_2026-11-24.py REPO_ROOT
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
PGRID = [2.0, 2.25, 2.5, 2.75, 3.0]


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
        r0 = math.dist(x0[0], x0[1])
        orient = "H" if abs(x0[0][1] - x0[1][1]) < 1e-9 else "V"
        n = window_n(xy)
        data.append(dict(rid=rid, r0=r0, orient=orient, T=t[-1], x0=x0, t=t[:n], xy=xy[:n]))

    print("P grid: per-run K_A, K_B with P fixed; chi2/n at sigma 0.05")
    print("run                         or   r0    T     nwin   P      KA      KB     KB/KA  chi2/n")
    summary = {}
    for P in PGRID:
        KAs = []
        for d in data:
            def resid(p):
                sim = simulate(p[0], p[1], P, d["x0"], d["t"])
                return (sim - d["xy"]).ravel() / SIGMA
            f = least_squares(resid, x0=[8.0, 11.0], bounds=([0.1, 0.1], [40, 40]))
            chi = np.sum(f.fun ** 2) / f.fun.size
            d.setdefault("fit", {})[P] = (f.x[0], f.x[1], chi)
            print(f"{d['rid']}  {d['orient']}  {d['r0']:4.1f}  {d['T']:5.1f}  {len(d['t']):4d}  "
                  f"{P:5.2f}  {f.x[0]:7.3f} {f.x[1]:7.3f}  {f.x[1]/f.x[0]:6.3f}  {chi:7.3f}")
            if d["T"] == 6.0:
                KAs.append((d["r0"], f.x[0]))
        r0s = np.array([a for a, _ in KAs]); KA = np.array([b for _, b in KAs])
        slope = np.polyfit(r0s, KA, 1)[0]
        summary[P] = (slope, KA.max() - KA.min())
        print("-" * 110)
    print("\nP     slope dK_A/dr0 (T=6 runs)   K_A range (T=6 runs)   max chi2/n over all 12 runs")
    for P in PGRID:
        chis = [d["fit"][P][2] for d in data]
        print(f"{P:4.2f}  {summary[P][0]:+10.4f}                  {summary[P][1]:8.3f}              {max(chis):8.3f}")


if __name__ == "__main__":
    main()
