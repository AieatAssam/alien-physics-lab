"""Trajectory-level strength factor s for A-A pairs: model a = s * K / r^P with K=17.74, P=2.5 (P-0003).
Integrates the two-body problem from the request's exact initial state (no wall contact in these runs),
and finds the least-squares s over the full observed trajectory (both particles, both coordinates).
No cubic window, so the finite-window bias of the acceleration fit does not apply.
Usage: python3 -I traj_scale_r1.py  (repo root)
"""
import json
import numpy as np

K0, P = 17.74, 2.5
RES = "results/{d}/lab-c/{n}.json"; REQ = "requests/{d}/lab-c/{n}.json"
RUNS = [
    ("2026-11-18", "r1", "001", "approach r=2"),
    ("2026-11-18", "r1", "002", "recede   r=2"),
    ("2026-11-18", "r1", "003", "comove  r=2"),
    ("2026-11-18", "r1", "009", "rest y   r=2"),
    ("2026-11-17", "r3", "001", "rest x   r=2"),
    ("2026-11-18", "r1", "004", "approach r=4"),
    ("2026-11-18", "r1", "005", "recede   r=4"),
    ("2026-11-17", "r3", "003", "rest x   r=4"),
]

def integrate(x0, v0, s, times, h=0.0005):
    x = np.array(x0, float); v = np.array(v0, float)
    def acc(x):
        d = x[1] - x[0]; r = np.linalg.norm(d); f = s * K0 / r**P
        return np.array([f * d / r, -f * d / r])
    out = []; t = 0.0
    for T in times:
        while t < T - 1e-12:
            hh = min(h, T - t)
            a1 = acc(x); k1x, k1v = v, a1
            x2 = x + hh/2*k1x; v2 = v + hh/2*k1v; a2 = acc(x2)
            x3 = x + hh/2*v2; v3 = v + hh/2*a2; a3 = acc(x3)
            x4 = x + hh*v3; v4 = v + hh*a3; a4 = acc(x4)
            x = x + hh/6*(k1x + 2*v2 + 2*v3 + v4)
            v = v + hh/6*(a1 + 2*a2 + 2*a3 + a4)
            t += hh
        out.append(x.copy())
    return np.array(out)  # (ntimes, 2 particles, 2 coords)

def obs_array(r, nparts):
    S = r["samples"]
    O = np.zeros((len(S), nparts, 2)); 
    for k, s in enumerate(S):
        for p in s["particles"]:
            O[k, p["id"]] = p["pos"]
    return np.array([s["t"] for s in S]), O

def sse(s, x0, v0, times, O):
    M = integrate(x0, v0, s, times)
    return ((O - M) ** 2).sum()

def golden(f, a, b, tol=1e-5):
    g = (np.sqrt(5) - 1) / 2
    c, d = b - g*(b-a), a + g*(b-a)
    while abs(b - a) > tol:
        if f(c) < f(d): b = d
        else: a = c
        c, d = b - g*(b-a), a + g*(b-a)
    return (a + b) / 2

print(f"{'run':22s} {'T':>4s} {'s_hat':>7s} {'se':>6s} {'rms(s=1)':>9s} {'rms(s_hat)':>10s}   (prediction: s=1)")
for d, rd, n, label in RUNS:
    q = json.load(open(REQ.format(d=f"{d}/{rd}", n=n))); r = json.load(open(RES.format(d=f"{d}/{rd}", n=n)))
    parts = q["setup"]["particles"]
    x0 = [p["pos"] for p in parts]; v0 = [p["vel"] for p in parts]
    times, O = obs_array(r, len(parts))
    # the observed samples are at sample_dt; integrate on the same time points
    f = lambda s: sse(s, x0, v0, times, O)
    sh = golden(f, 0.5, 1.5)
    N = O.size
    # standard error from curvature of SSE (sigma = 0.05 per coordinate)
    h = 1e-3
    d2 = (f(sh+h) - 2*f(sh) + f(sh-h)) / h**2
    sig2 = 0.05**2
    se = np.sqrt(2*sig2 / d2) if d2 > 0 else np.nan
    rms1 = np.sqrt(f(1.0) / N); rmsh = np.sqrt(f(sh) / N)
    print(f"{label+' ('+d[5:]+'/'+rd+'/'+n+')':22s} {q['setup']['duration']:4.1f} {sh:7.3f} {se:6.3f} {rms1:9.4f} {rmsh:10.4f}")
