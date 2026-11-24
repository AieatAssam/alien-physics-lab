"""Score round-1 runs 2026-11-24/r1/lab-b/001-004 (T = 2, dt = 0.01, tracker).

Model: equal-species pair, acceleration on each particle toward the other of magnitude K / r^P
(same K for both orderings, A-A or B-B). Fit K (and P when free) by least squares on the measured
positions over 0 < t <= T, starting from the request setup (never the noisy t = 0 sample).
Sigma = 0.05 per coordinate. Walls are not modelled: the pairs stay well inside the chamber over T = 2.

Usage: python3 -I score_r1_2026-11-24.py <repo_root>
"""
import sys, json, math, os
sys.path.insert(0, "/tmp/lab-b-pylib")
import numpy as np
from scipy.optimize import least_squares

SIGMA = 0.05
L = 10.0


def integrate(x0, K, P, T, dt, h=0.001):
    """RK4 of two equal-species particles at rest; returns positions at multiples of dt."""
    x = np.array(x0, float)
    v = np.zeros_like(x)

    def acc(x):
        d = x[1] - x[0]
        r = math.hypot(d[0], d[1])
        f = K / r ** (P + 1)
        return np.array([f * d, -f * d])

    out = [x.copy()]
    n_steps = int(round(T / h))
    per = int(round(dt / h))
    for s in range(1, n_steps + 1):
        a1 = acc(x)
        x2, v2 = x + 0.5 * h * v, v + 0.5 * h * a1
        a2 = acc(x2)
        x3, v3 = x + 0.5 * h * v2, v + 0.5 * h * a2
        a3 = acc(x3)
        x4, v4 = x + h * v3, v + h * a3
        a4 = acc(x4)
        x = x + h / 6 * (v + 2 * v2 + 2 * v3 + v4)
        v = v + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        if s % per == 0:
            out.append(x.copy())
    return out


def score(root, suffix):
    req = json.load(open(os.path.join(root, "requests", suffix + ".json")))
    res = json.load(open(os.path.join(root, "results", suffix + ".json")))
    parts = req["setup"]["particles"]
    x0 = [p["pos"] for p in parts]
    sp = parts[0]["species"]
    T = req["setup"]["duration"]
    dt = req["setup"]["sample_dt"]
    meas = []
    for s in res["samples"]:
        if 0 < s["t"] <= T + 1e-9:
            meas.append(np.array([[q["pos"][0], q["pos"][1]]
                                  for q in sorted(s["particles"], key=lambda q: q["id"])]))
    meas = np.array(meas)
    n = len(meas)

    def resid(p, free_P):
        K = p[0]
        P = p[1] if free_P else 2.5
        traj = integrate(x0, K, P, T, dt)
        sim = np.array(traj[1:n + 1])
        return (sim - meas).ravel()

    out = {"id": suffix, "species": sp, "r0": round(math.dist(x0[0], x0[1]), 4), "T": T, "samples": n}
    for free_P in (False, True):
        p0 = [10.0, 2.5] if free_P else [10.0]
        fit = least_squares(lambda p: resid(p, free_P), x0=p0, xtol=1e-10, ftol=1e-10)
        chi2n = float(np.mean((fit.fun / SIGMA) ** 2))
        J = fit.jac
        cov = np.linalg.pinv(J.T @ J) * SIGMA ** 2
        err = np.sqrt(np.diag(cov))
        key = "free" if free_P else "P2.5"
        out[key] = {"K": round(float(fit.x[0]), 3), "dK": round(float(err[0]), 3),
                    "P": round(float(fit.x[1]), 4) if free_P else 2.5,
                    "dP": round(float(err[1]), 4) if free_P else None,
                    "chi2n": round(chi2n, 3),
                    "rmse_over_L": round(float(np.sqrt(np.mean(fit.fun ** 2))) / L, 5)}
    return out


if __name__ == "__main__":
    root = sys.argv[1]
    rows = [score(root, s) for s in sys.argv[2:]]
    print(json.dumps(rows, indent=1))
