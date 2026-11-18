"""Fit a central law a = K / r^P to AT-REST A-A runs only (trajectory level, full run), then predict
the moving runs (approach / recede / co-moving) with NO velocity term. If approach and recede residuals are
at noise level under the rest-fitted law, the data show no velocity dependence at this sensitivity.
Shape-vs-velocity check: the moving runs explore different r ranges than the rest runs, so a shape
mismatch in P could mimic a velocity effect. Scanning P (outer) and K (golden, inner) addresses this.
Usage: python3 -I traj_KP_r1.py   (repo root)
"""
import json, numpy as np

H = 0.002
REST = [("2026-11-17/r3", "001"), ("2026-11-17/r3", "002"), ("2026-11-17/r3", "003"),
        ("2026-11-18/r1", "009")]                     # at rest, A-A (009 is the y-direction pair)
MOVE = [("2026-11-18/r1", "001", "approach r=2"), ("2026-11-18/r1", "002", "recede r=2"),
        ("2026-11-18/r1", "003", "co-moving r=2"), ("2026-11-18/r1", "004", "approach r=4"),
        ("2026-11-18/r1", "005", "recede r=4")]

def load(d, n):
    q = json.load(open(f"requests/{d}/lab-c/{n}.json")); r = json.load(open(f"results/{d}/lab-c/{n}.json"))
    x0 = np.array([p["pos"] for p in q["setup"]["particles"]], float)
    v0 = np.array([p["vel"] for p in q["setup"]["particles"]], float)
    times = np.array([s["t"] for s in r["samples"]])
    O = np.zeros((len(times), 2, 2))
    for k, s in enumerate(r["samples"]):
        for p in s["particles"]:
            O[k, p["id"]] = p["pos"]
    return x0, v0, times, O

def integrate(x0, v0, K, P, times):
    x = x0.copy(); v = v0.copy(); out = np.zeros((len(times), 2, 2)); t = 0.0; k = 0
    def acc(x):
        d = x[1] - x[0]; r = np.linalg.norm(d); f = K / r**P
        return np.array([f*d/r, -f*d/r])
    while k < len(times):
        T = times[k]
        while t < T - 1e-12:
            h = min(H, T - t)
            a1 = acc(x); x2 = x + h/2*v; v2 = v + h/2*a1; a2 = acc(x2)
            x3 = x + h/2*v2; v3 = v + h/2*a2; a3 = acc(x3)
            x4 = x + h*v3; v4 = v + h*a3; a4 = acc(x4)
            x = x + h/6*(v + 2*v2 + 2*v3 + v4); v = v + h/6*(a1 + 2*a2 + 2*a3 + a4); t += h
        out[k] = x; k += 1
    return out

RUNS_REST = [load(d, n) for d, n in REST]
RUNS_MOVE = [(lbl, load(d, n)) for d, n, lbl in MOVE]

def sse_rest(K, P):
    tot = 0.0
    for x0, v0, times, O in RUNS_REST:
        tot += ((O - integrate(x0, v0, K, P, times))**2).sum()
    return tot

def fitK(P):
    lo, hi = 2.0, 40.0; g = (np.sqrt(5)-1)/2
    a, b = lo, hi; c, d = b-g*(b-a), a+g*(b-a); fc, fd = sse_rest(c, P), sse_rest(d, P)
    while abs(b-a) > 1e-3:
        if fc < fd: b, d, fd = d, c, fc; c = b-g*(b-a); fc = sse_rest(c, P)
        else: a, c, fc = c, d, fd; d = a+g*(b-a); fd = sse_rest(d, P)
    K = (a+b)/2; return K, sse_rest(K, P)

best = None
print("P-scan (rest runs only): P, K_best, SSE")
for P in [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6]:
    K, s = fitK(P)
    print(f"  P={P:.2f}  K={K:7.3f}  SSE={s:9.4f}")
    if best is None or s < best[2]: best = (K, P, s)
K, P, S = best
N_rest = sum(O.size for _, _, _, O in RUNS_REST)
print(f"best rest-only law: K={K:.3f} P={P:.2f}; rms per coord on rest runs={np.sqrt(S/N_rest):.4f}")
print("\nMoving runs predicted with the rest-fitted law, no velocity term:")
for lbl, (x0, v0, times, O) in RUNS_MOVE:
    M = integrate(x0, v0, K, P, times); res = O - M
    rms = np.sqrt((res**2).mean())
    m = res.mean(axis=(0, 2))
    print(f"  {lbl:14s} T={times[-1]:.1f}  rms/coord={rms:.4f}  mean res per particle={m.round(4)}")
