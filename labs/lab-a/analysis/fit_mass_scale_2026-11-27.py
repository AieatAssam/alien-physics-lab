"""Mass-aware pair-scale fit (Plumbline, 2026-11-27). numpy.

Model per run (two particles at rest, no walls reached):
  F(r) = g * K(r) / r^2.5 along the line of centres (equal and opposite, Newton III),
  K(r) = P-0029 table (piecewise linear, clamped at 5..9 by np.interp; same table for all runs),
  a_i = F / m_i toward the partner, masses m_A = 1, m_B = 0.72, m_C = 0.42 (from the momentum ratios).
g = 1 is the A-A law with the table. Fit g by chi2 over all samples with tracker sigma 0.05,
1-sigma from delta chi2 = 1. Runs use positions relative to the setup (t = 0 positions are the setup).
Factorisation prediction (g_ij = q_i q_j, from the BB and CC same-species scales with masses):
  g_AB = 0.504, g_AC = 0.542, g_BC = 0.273.
Run: python3 -I fit_mass_scale_2026-11-27.py <repo_root>
"""
import json, math, os, sys
import numpy as np

ROOT = sys.argv[1]
SIG = 0.05
MASS = {"A": 1.0, "B": 0.72, "C": 0.42}
R_TAB = np.array([5.0, 6.0, 7.0, 8.0, 9.0])
K_TAB = np.array([17.834, 16.617, 15.121, 13.432, 11.624])
H = 0.001


def K(r):
    return float(np.interp(r, R_TAB, K_TAB))


def simulate(x0, sp, g, T, dt_out):
    """x0: 2x2 array positions; sp: species pair. Returns positions at output times."""
    m0, m1 = MASS[sp[0]], MASS[sp[1]]
    x = np.array(x0, dtype=float)
    v = np.zeros((2, 2))

    def acc(x):
        d = x[1] - x[0]
        r = math.hypot(d[0], d[1])
        f = g * K(r) / r ** 2.5
        u = d / r
        return np.array([f * u / m0, -f * u / m1])

    n_out = int(round(T / dt_out))
    out = [x.copy()]
    t = 0.0
    for i in range(1, n_out + 1):
        target = i * dt_out
        while t < target - 1e-12:
            h = min(H, target - t)
            k1x, k1v = v, acc(x)
            x2, v2 = x + h / 2 * k1x, v + h / 2 * k1v
            k2x, k2v = v2, acc(x2)
            x3, v3 = x + h / 2 * k2x, v + h / 2 * k2v
            k3x, k3v = v3, acc(x3)
            x4, v4 = x + h * k3x, v + h * k3v
            k4x, k4v = v4, acc(x4)
            x = x + h / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
            v = v + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            t += h
        out.append(x.copy())
    return out


def load(rd, n):
    req = json.load(open(os.path.join(ROOT, "requests", rd, n + ".json")))
    res = json.load(open(os.path.join(ROOT, "results", rd, n + ".json")))
    return req, res


def chi2_for(req, res, sp, g):
    s = req["setup"]
    x0 = [p["pos"] for p in s["particles"]]
    T = s["duration"]
    dt = s["sample_dt"]
    pred = simulate(x0, sp, g, T, dt)
    c = 0.0
    for k, smp in enumerate(res["samples"]):
        if k == 0:
            continue
        meas = np.array([smp["particles"][i]["pos"] for i in range(2)])
        c += float(np.sum((meas - pred[k]) ** 2)) / SIG ** 2
    return c


def fit(rd, n, sp, grid=np.linspace(0.2, 1.4, 121)):
    req, res = load(rd, n)
    chis = np.array([chi2_for(req, res, sp, g) for g in grid])
    i = int(np.argmin(chis))
    best = grid[i]
    ok = grid[chis <= chis[i] + 1.0]
    nsamp = len(res["samples"]) - 1
    return best, ok.min(), ok.max(), chis[i] / (2 * nsamp), req["setup"]["duration"]


if __name__ == "__main__":
    runs = [
        ("2026-11-27/r1/lab-a", "009", "AC"), ("2026-11-27/r1/lab-a", "010", "AC"),
        ("2026-11-27/r1/lab-a", "011", "AB"), ("2026-11-27/r1/lab-a", "012", "AB"),
        ("2026-11-27/r1/lab-a", "013", "AA"),
        ("2026-11-26/r2/lab-a", "001", "AC"), ("2026-11-26/r2/lab-a", "002", "AC"),
        ("2026-11-26/r2/lab-a", "003", "AB"), ("2026-11-26/r2/lab-a", "004", "AA"),
        ("2026-11-27/r2/lab-a", "001", "BC"), ("2026-11-27/r2/lab-a", "002", "BC"),
        ("2026-11-27/r2/lab-a", "003", "BC"),
    ]
    for rd, n, sp in runs:
        spp = (sp[0], sp[1])
        b, lo, hi, rchi, T = fit(rd, n, spp)
        print("%s/%s %s T=%.1f  g = %.3f (%.3f..%.3f)  chi2/dof at best %.2f" % (rd, n, sp, T, b, lo, hi, rchi))
