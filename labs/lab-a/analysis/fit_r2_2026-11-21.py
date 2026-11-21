"""lab-a 2026-11-21 round-2 fits (Plumbline): orientation/position control for A-A at r0 1.0 and the r0 1.25 replicate.

Same method as fit_r1_2026-11-21.py: separation-profile fit of one pair coefficient K, P = 2.5 fixed,
relative RK4 model r'' = -2K/r^P (two equal particles at rest). Initial separation from the REQUEST setup.
Also reports closest measured separation and the measured-vs-model separation RMSE.

Usage: python3 -I fit_r2_2026-11-21.py <repo_root>
"""
import json
import math
import os
import sys

root = sys.argv[1]
DATE, RND = "2026-11-21", "r2"


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


def fit(rnd, n, Kguess):
    req = load("requests", DATE, rnd, "lab-a", "%03d.json" % n)
    res = load("results", DATE, rnd, "lab-a", "%03d.json" % n)
    a, b = req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"]
    r0 = math.dist(a, b)
    times, meas = [], []
    for s in res["samples"]:
        q = {p["id"]: p["pos"] for p in s["particles"]}
        times.append(s["t"])
        meas.append(math.dist(q[0], q[1]))

    def rms(K):
        m = relpath(K, r0, times)
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(meas, m)) / len(meas))

    kc = min((Kguess * (0.5 + 0.01 * i) for i in range(101)), key=rms)
    kf = min((kc + 0.002 * Kguess * (j - 25) for j in range(51)), key=rms)
    sig = 0.071
    chi = lambda K: sum(((x - y) / sig) ** 2 for x, y in zip(meas, relpath(K, r0, times))) / len(meas)
    # 1-sigma: K where chi2 rises by 1 (chi2 scaled per sample, so use Delta(sum chi2) = 1 on the mean-normalised scale)
    c0 = sum(((x - y) / sig) ** 2 for x, y in zip(meas, relpath(kf, r0, times)))
    grid = [kf + 0.002 * Kguess * (j - 250) for j in range(501)]
    inside = [K for K in grid if sum(((x - y) / sig) ** 2 for x, y in zip(meas, relpath(K, r0, times))) - c0 <= 1.0]
    err = (min(inside), max(inside)) if inside else (kf, kf)
    print("%s/%s/lab-a/%03d r0=%.4f T=%.3f n=%d K_fit=%.3f  +-%.3f  rms_sep=%.4f  min_meas_sep=%.3f  min_model_sep=%.3f"
          % (DATE, rnd, n, r0, times[-1], len(meas), kf, (err[1] - err[0]) / 2, rms(kf), min(meas), min(relpath(kf, r0, times))))
    return kf


if __name__ == "__main__":
    fit("r2", 1, 11.0)  # A-A r0 1.0 horizontal, centred (3,3)
    fit("r2", 2, 11.0)  # A-A r0 1.0 diagonal, centred (5,5)
    fit("r2", 3, 10.0)  # A-A r0 1.0 diagonal, centred (3,3)  (repeat of r1/009)
    fit("r2", 4, 12.5)  # A-A r0 1.25 horizontal, centred (5,5), third run
