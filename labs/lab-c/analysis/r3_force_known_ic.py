"""Initial accelerations for at-rest pairs using KNOWN initial conditions.

Model per particle and coordinate:  x(t) = x0 + 0.5*a*t^2 + j*t^3/6   (v0 = 0 from the request).
x0 is taken from the request (exact), so only a and j are fitted. Noise sd 0.05 (round 2).
Window: samples with t <= tmax. Output: force along the initial pair line, positive = attraction.
Usage: python3 out/labs/lab-c/analysis/r3_force_known_ic.py <results_dir> <requests_dir> <tmax> [n...]
"""
import json, sys, os
import numpy as np

RES, REQ, TMAX = sys.argv[1], sys.argv[2], float(sys.argv[3])
NAMES = sys.argv[4:] or [f"{k:03d}" for k in range(1, 11)]
SIGMA = 0.05


def fit(n, tmax=TMAX):
    r = json.load(open(os.path.join(RES, f"{n}.json")))
    q = json.load(open(os.path.join(REQ, f"{n}.json")))
    parts = q["setup"]["particles"]
    samples = [s for s in r["samples"] if s["t"] <= tmax + 1e-9]
    t = np.array([s["t"] for s in samples])
    rows = []
    # design: columns [a, j] ; target: x - x0
    A = np.column_stack([0.5 * t**2, t**3 / 6.0])
    res = {}
    for idx, p in enumerate(parts):
        pos0 = np.array(p["pos"], float)
        obs = np.array([[pp["pos"] for pp in s["particles"] if pp["id"] == idx][0] for s in samples])
        acc = []
        for c in range(2):
            y = obs[:, c] - pos0[c]
            b, *_ = np.linalg.lstsq(A, y, rcond=None)
            acc.append(b[0])
        # covariance of a (per coordinate): sigma^2 * [(A^T A)^-1]_{00}
        cov = np.linalg.inv(A.T @ A) * SIGMA**2
        res[idx] = dict(species=p["species"], pos0=pos0, acc=np.array(acc), se=np.sqrt(cov[0, 0]))
    return r, q, res, len(t)


if __name__ == "__main__":
    for n in NAMES:
        r, q, res, N = fit(n)
        T = q["setup"]["duration"]
        print(f"== {n} tmax={TMAX} N={N} | {q['purpose'][:60]}")
        if len(res) == 2:
            p0, p1 = res[0], res[1]
            d = p1["pos0"] - p0["pos0"]
            r0 = np.linalg.norm(d); u = d / r0
            F0 = p0["acc"] @ u          # on particle 0 along +u (toward 1): >0 attraction
            F1 = -(p1["acc"] @ u)       # on particle 1 along -u: >0 attraction
            print(f"  r0={r0:.3f} {p0['species']}-{p1['species']}  F_on0={F0:+.4f}  F_on1={F1:+.4f}  se~{p0['se']:.4f}")
            print(f"  transverse acc: a0_perp={p0['acc'] @ np.array([-u[1],u[0]]):+.4f}  a1_perp={p1['acc'] @ np.array([-u[1],u[0]]):+.4f}")
        else:
            for i, v in res.items():
                print(f"  id{i} {v['species']} acc={np.round(v['acc'],4)} se~{v['se']:.4f}")
