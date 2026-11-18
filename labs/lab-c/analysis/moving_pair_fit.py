"""Initial along-line force for pairs with KNOWN initial velocity (round-1 velocity tests).
Model per particle/coordinate:  x(t) = x0 + v0*t + a*t^2/2 + j*t^3/6, with x0, v0 from the request.
Only a and j are fitted. Noise sd 0.05. Force along the initial line, positive = attraction.
Usage: python3 out/labs/lab-c/analysis/moving_pair_fit.py <results_dir> <requests_dir> <tmax> <n> [n ...]
Check: run on 2026-11-17/r3/lab-c with v0=0 reproduces r3_force_known_ic.py (F about 2.6 at r=2).
"""
import json, os, sys
import numpy as np

SIGMA = 0.05
RES, REQ, TMAX = sys.argv[1], sys.argv[2], float(sys.argv[3])
NAMES = sys.argv[4:]


def run(n):
    r = json.load(open(os.path.join(RES, f"{n}.json")))
    q = json.load(open(os.path.join(REQ, f"{n}.json")))
    parts = q["setup"]["particles"]
    S = [s for s in r["samples"] if s["t"] <= TMAX + 1e-9]
    t = np.array([s["t"] for s in S])
    A = np.column_stack([0.5 * t**2, t**3 / 6.0])
    cov_a = np.linalg.inv(A.T @ A)[0, 0] * SIGMA**2
    acc, pos0 = [], []
    for idx, p in enumerate(parts):
        x0 = np.array(p["pos"], float); v0 = np.array(p["vel"], float)
        obs = np.array([[pp["pos"] for pp in s["particles"] if pp["id"] == idx][0] for s in S])
        a = np.zeros(2)
        for c in range(2):
            y = obs[:, c] - x0[c] - v0[c] * t
            b, *_ = np.linalg.lstsq(A, y, rcond=None)
            a[c] = b[0]
        acc.append(a); pos0.append(x0)
    d = pos0[1] - pos0[0]; r0 = np.linalg.norm(d); u = d / r0
    F0 = acc[0] @ u
    F1 = -(acc[1] @ u)
    print(f"{n}: r0={r0:.3f} tmax={TMAX} N={len(t)} | F_on0={F0:+.3f} F_on1={F1:+.3f} "
          f"mean={0.5*(F0+F1):+.3f} se(one particle)~{np.sqrt(cov_a):.3f} | "
          f"perp a0={acc[0] @ np.array([-u[1], u[0]]):+.3f} a1={acc[1] @ np.array([-u[1], u[0]]):+.3f}")


for n in NAMES:
    run(n)
