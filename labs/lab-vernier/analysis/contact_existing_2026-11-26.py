"""Read-only look at the round-1 T=1 A-A runs at r0=2.5 (2026-11-25/r1/lab-vernier/006 horizontal,
007 vertical). Compares measured tracker separation with the pure-law prediction (signed 1D relative
coordinate, symmetric about the chamber centre). Pure math; no new credits.

Usage: PAPERS-free. Reads results/requests from the repo root; run with -I from this folder.
"""
import json, math, os

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
G, P = 23.63, 2.099
L = 10.0


def a_pure(r):
    return (G / 2.0) / r ** P


def integrate_signed(s0, T, dt_out, h=1e-5):
    """Signed relative separation s = x1 - x0 (both at rest). s'' = -2 a(|s|) sign(s) (attraction)."""
    s, v, t = s0, 0.0, 0.0
    out = [(0.0, s0)]
    n = int(round(T / dt_out))
    def acc(sv):
        ss = sv
        if abs(ss) < 1e-6:
            return 0.0
        return -2.0 * a_pure(abs(ss)) * (1 if ss > 0 else -1)
    for k in range(1, n + 1):
        target = round(k * dt_out, 9)
        while t < target - 1e-12:
            hh = min(h, target - t)
            k1v = acc(s); k1s = v
            k2s = v + hh / 2 * k1v; k2v = acc(s + hh / 2 * k1s)
            k3s = v + hh / 2 * k2v; k3v = acc(s + hh / 2 * k2s)
            k4s = v + hh * k3v; k4v = acc(s + hh * k3s)
            s = s + hh / 6 * (k1s + 2 * k2s + 2 * k3s + k4s)
            v = v + hh / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            t += hh
            if abs(s) < 0.02:
                return out
        out.append((target, s))
    return out


def measured_sep(res):
    ts, ss = [], []
    for smp in res["samples"]:
        p = smp["particles"]
        ts.append(smp["t"])
        ss.append(math.dist(p[0]["pos"], p[1]["pos"]))
    return ts, ss


if __name__ == "__main__":
    for rid in ["2026-11-25/r1/lab-vernier/006", "2026-11-25/r1/lab-vernier/007"]:
        res = json.load(open(f"{REPO}/results/{rid}.json"))
        ts, ms = measured_sep(res)
        pred = integrate_signed(2.5, 1.0, 0.0005)
        pmap = dict((round(a, 9), b) for a, b in pred)
        print(rid)
        print("  t      measured_sep  pure_law_|s|  (pure-law: 0 => pass-through / end of integration)")
        for tt in [0.5, 0.6, 0.7, 0.8, 0.85, 0.88, 0.9, 0.92, 0.93, 0.94, 0.95, 0.96, 0.98, 1.0]:
            i = min(range(len(ts)), key=lambda j: abs(ts[j] - tt))
            key = round(ts[i], 9)
            pv = pmap.get(key)
            print(f"  {ts[i]:.4f}   {ms[i]:.4f}        {('%.4f' % abs(pv)) if pv is not None else 'n/a (stopped)'}")
        last_pred = pred[-1]
        print("  pure law integrated until t =", round(last_pred[0], 4), "|s| =", round(abs(last_pred[1]), 4))
