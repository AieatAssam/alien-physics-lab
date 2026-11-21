"""Two-body coupling fits from tracker data (pure python; no numpy available).

Model: acc on particle i = COUP[(s_i, s_j)] / r**2.5 along the separation, RK4 step H = 0.002, specular walls.
Start state = the REQUEST setup (never the noisy sample at t = 0). Gaussian chi2 with sd 0.05 per coordinate.
Identical-species pairs: one K (both orders equal). Mixed pairs: two couplings (K_ij, K_ji), fitted by coordinate descent.

Usage: python3 -I pairfit_2026-11-21.py REPO RID [RID ...]
"""
import json
import math
import sys
from pathlib import Path

L = 10.0
P = 2.5
H = 0.002
SD = 0.05


def accel(pos, species, coup):
    acc = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(2):
        j = 1 - i
        dx = pos[j][0] - pos[i][0]
        dy = pos[j][1] - pos[i][1]
        r = math.hypot(dx, dy)
        a = coup[(species[i], species[j])] / r ** P
        acc[i][0] += a * dx / r
        acc[i][1] += a * dy / r
    return acc


def step(pos, vel, species, coup, h):
    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(2)]
    k1p, k1v = vel, accel(pos, species, coup)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, accel(p2, species, coup)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, accel(p3, species, coup)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, accel(p4, species, coup)
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)] for i in range(2)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)] for i in range(2)]
    for i in range(2):
        for k in range(2):
            if newp[i][k] < 0.0:
                newp[i][k] = -newp[i][k]; newv[i][k] = -newv[i][k]
            elif newp[i][k] > L:
                newp[i][k] = 2 * L - newp[i][k]; newv[i][k] = -newv[i][k]
    return newp, newv


def simulate(setup, coup):
    species = [p["species"] for p in setup["particles"]]
    pos = [list(map(float, p["pos"])) for p in setup["particles"]]
    vel = [list(map(float, p["vel"])) for p in setup["particles"]]
    dur, dt = float(setup["duration"]), float(setup["sample_dt"])
    n = int(round(dur / dt))
    out, t = [], 0.0
    for i in range(1, n + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = step(pos, vel, species, coup, h)
            t += h
        t = target
        out.append((t, [list(p) for p in pos]))
    return out


def chi2(setup, samples, coup):
    sim = simulate(setup, coup)
    table = {round(t, 9): p for t, p in sim}
    total, count = 0.0, 0
    for s in samples:
        t = round(s["t"], 9)
        if t == 0.0 or t not in table:
            continue
        for p in s["particles"]:
            q = table[t][p["id"]]
            total += ((q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2) / SD ** 2
            count += 2
    return total / count if count else float("inf")


def golden(f, a, b, tol=1e-4):
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol:
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a); fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a); fd = f(d)
    return (a + b) / 2


def fit(setup, samples, species):
    s0, s1 = species
    if s0 == s1:
        k = golden(lambda K: chi2(setup, samples, {(s0, s0): K}), -5.0, 40.0)
        return {"K": round(k, 3), "chi2n": round(chi2(setup, samples, {(s0, s0): k}), 3)}
    kf, kr = 0.0, 0.0
    for _ in range(4):
        kf = golden(lambda x: chi2(setup, samples, {(s0, s1): x, (s1, s0): kr}), -30.0, 30.0)
        kr = golden(lambda y: chi2(setup, samples, {(s0, s1): kf, (s1, s0): y}), -30.0, 30.0)
    return {"K_" + s0 + s1: round(kf, 3), "K_" + s1 + s0: round(kr, 3),
            "chi2n": round(chi2(setup, samples, {(s0, s1): kf, (s1, s0): kr}), 3)}


if __name__ == "__main__":
    repo = Path(sys.argv[1])
    for rid in sys.argv[2:]:
        res = json.loads((repo / "results" / f"{rid}.json").read_text())
        setup = json.loads((repo / "requests" / f"{rid}.json").read_text())["setup"]
        species = [p["species"] for p in setup["particles"]]
        seps = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])
        print(rid, "".join(species), "sep=%.4f" % seps, "T=%s" % setup["duration"], fit(setup, res["samples"], species))


def sigma_K(setup, samples, species, K):
    """1-sigma on a single K from delta chi2_total = 1 (same-species fits), by bisection on each side."""
    s0 = species[0]
    count = sum(2 * len(s["particles"]) for s in samples if round(s["t"], 9) != 0.0)
    base = chi2(setup, samples, {(s0, s0): K}) * count
    def dchi(x):
        return chi2(setup, samples, {(s0, s0): x}) * count - base - 1.0
    out = []
    for direction in (1, -1):
        lo, hi = K, K + direction * 0.5
        while dchi(hi) < 0:
            hi = K + 2 * (hi - K)
        for _ in range(40):
            mid = (lo + hi) / 2
            if dchi(mid) < 0:
                lo = mid
            else:
                hi = mid
        out.append(abs((lo + hi) / 2 - K))
    return round((out[0] + out[1]) / 2, 3)
