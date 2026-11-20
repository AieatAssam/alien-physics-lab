"""lab-a, 2026-11-20 round 2: fit r'' = -2 K / r^P to measured pair separations (close range).
Pair at rest, both particles attract with the same K (relative motion). Grid search on (K, P),
least squares on measured separations (sample-level). Pure python RK4. Also reports the
same fit with P fixed at 2.5. Usage: python3 -I fit_close_KP_2026-11-20.py <repo_root>
"""
import json
import math
import os
import sys

root = sys.argv[1]


def sep_series(i):
    r = json.load(open(os.path.join(root, "results", "2026-11-20", "r1", "lab-a", i + ".json")))
    out = []
    for s in r["samples"]:
        b = {p["id"]: p["pos"] for p in s["particles"]}
        out.append((s["t"], math.hypot(b[0][0] - b[1][0], b[0][1] - b[1][1])))
    return out


def model(K, P, r0, times):
    """r(t) for r'' = -2K/r^P, r'(0)=0, returned at the given sorted times."""
    h = 2e-4
    r, v, t = r0, 0.0, 0.0
    out = []
    f = lambda x: -2.0 * K / max(x, 1e-3) ** P
    for T in times:
        while t < T - 1e-12:
            s = min(h, T - t)
            k1r, k1v = v, f(r)
            r2, v2 = r + s / 2 * k1r, v + s / 2 * k1v
            k2r, k2v = v2, f(r2)
            r3, v3 = r + s / 2 * k2r, v + s / 2 * k2v
            k3r, k3v = v3, f(r3)
            r4, v4 = r + s * k3r, v + s * k3v
            k4r, k4v = v4, f(r4)
            r += s / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
            v += s / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            t += s
        out.append(r)
    return out


def fit(runs, r0, Ps, Ks):
    best = None
    for P in Ps:
        for K in Ks:
            ss = 0.0
            n = 0
            for ser in runs:
                times = [t for t, _ in ser]
                m = model(K, P, r0, times)
                for (t, rm), rp in zip(ser, m):
                    ss += (rm - rp) ** 2
                    n += 1
            rms = math.sqrt(ss / n)
            if best is None or rms < best[0]:
                best = (rms, K, P)
    return best


r002 = sep_series("001"), sep_series("002")
print("A-A, r0=2.0 (runs 001+002, T=0.5)")
print("  best (K,P) grid:  rms_sep=%.4f K=%.2f P=%.2f" % fit(list(r002), 2.0,
      [2.0 + 0.1 * i for i in range(11)], [14 + 0.25 * i for i in range(33)]))
print("  P fixed 2.5:      rms_sep=%.4f K=%.2f P=%.2f" % fit(list(r002), 2.0, [2.5], [14 + 0.1 * i for i in range(61)]))
print("A-A, r0=1.5 (run 003, T=0.3)")
print("  best (K,P) grid:  rms_sep=%.4f K=%.2f P=%.2f" % fit([sep_series("003")], 1.5,
      [2.0 + 0.1 * i for i in range(11)], [14 + 0.25 * i for i in range(33)]))
print("  P fixed 2.5:      rms_sep=%.4f K=%.2f P=%.2f" % fit([sep_series("003")], 1.5, [2.5], [14 + 0.1 * i for i in range(61)]))
print("B-B, r0=2.0 (run 004, T=0.5)")
print("  P fixed 2.5:      rms_sep=%.4f K=%.2f P=%.2f" % fit([sep_series("004")], 2.0, [2.5], [4 + 0.05 * i for i in range(61)]))
