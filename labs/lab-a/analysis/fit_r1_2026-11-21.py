"""lab-a, 2026-11-21 round-1 close-range fits (Plumbline).

Separation-profile fit of one pair coefficient K, P = 2.5 fixed, RK4 relative-motion model
(reduced mass 1/2 per particle: r'' = -2K/r^P for two equal-species particles at rest, as in the earlier fits).
Initial separation from the REQUEST setup, not a noisy sample. Pre-registered bands are from the notebook.

Usage: python3 -I fit_r1_2026-11-21.py <repo_root>
"""
import json
import math
import os
import sys

root = sys.argv[1]
DATE, RND = "2026-11-21", "r1"


def load(*parts):
    with open(os.path.join(root, *parts)) as fh:
        return json.load(fh)


def relpath(K, r0, times, P=2.5, h=1e-4):
    f = lambda x: -2.0 * K / max(x, 1e-4) ** P
    r, v, t = r0, 0.0, 0.0
    out = []
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


def fit(n, Kguess, band):
    rid = "%s/%s/lab-a/%03d" % (DATE, RND, n)
    req = load("requests", DATE, RND, "lab-a", "%03d.json" % n)
    res = load("results", DATE, RND, "lab-a", "%03d.json" % n)
    a, b = req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"]
    r0 = math.dist(a, b)
    ser = []
    for s in res["samples"]:
        q = {p["id"]: p["pos"] for p in s["particles"]}
        ser.append((s["t"], math.dist(q[0], q[1])))
    times = [t for t, _ in ser]
    meas = [m for _, m in ser]

    def rms(K):
        m = relpath(K, r0, times)
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(meas, m)) / len(meas))

    kc = min((Kguess * (0.5 + 0.01 * i) for i in range(101)), key=rms)
    kf = min((kc + 0.002 * Kguess * (j - 25) for j in range(51)), key=rms)
    # 1-sigma-like spread: K where rms rises by 1% of noise-floor-squared-sum (chi2 +1 with sigma 0.07)
    sig = 0.071
    chi = lambda K: sum(((x - y) / sig) ** 2 for x, y in zip(meas, relpath(K, r0, times))) / len(meas)
    c0 = chi(kf)
    lo = min(kf, kf)
    print("%s N=2 sp=%s r0=%.4f T=%.3f n=%d cost=%s  K_fit=%.3f  rms_sep=%.4f  min_meas=%.3f  band=%s  %s"
          % (rid, "".join(p["species"] for p in req["setup"]["particles"]), r0, times[-1], len(meas),
             res["cost"], kf, rms(kf), min(meas), band[0:2] if band else None,
             ("" if not band else
              ("inside" if band[0] <= kf <= band[1] else "OUTSIDE"))))


# pre-registered bands (notebook, round-1 table)
fit(1, 4.0, (3.6, 4.4))   # B-B r0 1.0, pre-reg 4.0 within 10%
fit(2, 4.0, (3.6, 4.4))
fit(3, 9.0, (8.0, 9.6))   # C-C r0 1.0, band [8.0, 9.6]
fit(4, 9.0, (8.0, 9.6))
fit(5, 12.5, (11.875, 13.125))  # A-A r0 1.25, 12.5 within 5%
fit(6, 12.5, (11.875, 13.125))
fit(7, 10.5, (9.5, 11.5))  # A-A r0 0.85, band [9.5, 11.5]
fit(8, 10.5, (9.5, 11.5))
fit(9, 11.3, (10.735, 11.865))  # A-A r0 1.0 diagonal centred (3,3), 11.3 within 5%
