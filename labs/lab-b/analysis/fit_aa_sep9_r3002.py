"""Fit the central pair coefficient K (accel K / r**2.5 on each particle, P=2.5) for
two A particles at rest, from 2026-11-19/r3/lab-b/002. Relative coordinate d = x1 - x0
obeys d'' = -2K / d**2.5 (equal masses, attraction for K>0). Fit window: separation
above 3.0 to avoid the close-approach regime. Usage: python3 -I fit_aa_sep9_r3002.py <result.json>
"""
import json, math, sys

res = json.load(open(sys.argv[1]))
ts = [s["t"] for s in res["samples"]]
d_meas = [s["particles"][1]["pos"][0] - s["particles"][0]["pos"][0] for s in res["samples"]]
d0 = d_meas[0]

def simulate(K, t_end_list, h=0.002):
    out, d, v, t = [], d0, 0.0, 0.0
    targets = list(t_end_list)
    idx = 0
    while idx < len(targets):
        target = targets[idx]
        while t < target - 1e-12:
            hh = min(h, target - t)
            def acc(dd):
                return -2.0 * K / dd ** 2.5
            k1d, k1v = v, acc(d)
            d2, v2 = d + hh / 2 * k1d, v + hh / 2 * k1v
            k2d, k2v = v2, acc(d2)
            d3, v3 = d + hh / 2 * k2d, v + hh / 2 * k2v
            k3d, k3v = v3, acc(d3)
            d4, v4 = d + hh * k3d, v + hh * k3v
            k4d, k4v = v4, acc(d4)
            d += hh / 6 * (k1d + 2 * k2d + 2 * k3d + k4d)
            v += hh / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            t += hh
        out.append(d)
        idx += 1
    return out

window = [i for i, d in enumerate(d_meas) if d > 3.0 and ts[i] > 0]
tw = [ts[i] for i in window]
dw = [d_meas[i] for i in window]
print("window samples:", len(window), "t range", tw[0] if tw else None, tw[-1] if tw else None,
      "sep range", round(min(dw), 3) if dw else None, round(max(dw), 3) if dw else None)
best = None
for K10 in range(900, 1401):  # K from 9.00 to 14.00 in steps of 0.01
    K = K10 / 100.0
    pred = simulate(K, tw)
    sse = sum((p - m) ** 2 for p, m in zip(pred, dw))
    if best is None or sse < best[1]:
        best = (K, sse)
rms = math.sqrt(best[1] / len(dw))
print("best K (window fit):", round(best[0], 2), "rms of separation residual:", round(rms, 4))
