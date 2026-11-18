"""Law scan on AT-REST A-A trajectories (r = 1, 2, 4, 8), trajectory-level, full run.
Forms: power K/r^P (P scanned) and screened K*exp(-r/lam)/r^2 (lam scanned). K fitted by golden search.
Then predict the MOVING runs (approach/recede, r=2,4) with the best screened law and fit a velocity term g
(a = F(r)*(1 + g*vr)), with a fine grid, to bound g.
Usage: python3 -I law_scan_r1.py   (repo root)
"""
import numpy as np, json
H = 0.002

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

def integrate(x0, v0, times, law):
    x = x0.copy(); v = v0.copy(); out = np.zeros((len(times), 2, 2)); t = 0.0
    def acc(x, v):
        d = x[1] - x[0]; r = np.linalg.norm(d); u = d / r
        vr = np.dot(v[1] - v[0], u)
        f = law(r, vr)
        return np.array([f * u, -f * u])
    for k, T in enumerate(times):
        while t < T - 1e-12:
            h = min(H, T - t)
            a1 = acc(x, v); x2 = x + h/2*v; v2 = v + h/2*a1; a2 = acc(x2, v2)
            x3 = x + h/2*v2; v3 = v + h/2*a2; a3 = acc(x3, v3)
            x4 = x + h*v3; v4 = v + h*a3; a4 = acc(x4, v4)
            x = x + h/6*(v + 2*v2 + 2*v3 + v4); v = v + h/6*(a1 + 2*a2 + 2*a3 + a4); t += h
        out[k] = x
    return out

REST = [load(d, n) for d, n in [("2026-11-17/r3", "001"), ("2026-11-17/r3", "002"), ("2026-11-17/r3", "003"),
                                ("2026-11-18/r1", "009"), ("2026-11-17/r3", "004")]]
MOVE = [("2026-11-18/r1", n) for n in ["001", "002", "004", "005"]]
MOVE = [load(d, n) for d, n in MOVE]

def golden(f, a, b, tol=1e-4):
    g = (np.sqrt(5)-1)/2; c, d = b-g*(b-a), a+g*(b-a); fc, fd = f(c), f(d)
    while abs(b-a) > tol:
        if fc < fd: b, d, fd = d, c, fc; c = b-g*(b-a); fc = f(c)
        else: a, c, fc = c, d, fd; d = a+g*(b-a); fd = f(d)
    return (a+b)/2

def sse(runs, law):
    return sum(((O - integrate(x0, v0, t, law))**2).sum() for x0, v0, t, O in runs)

def fitK(form, shape):
    f = lambda K: sse(REST, lambda r, vr: form(K, r, shape, vr))
    K = golden(f, 8.0, 16.0, tol=2e-3); return K, f(K)

power = lambda K, r, P, vr: K / r**P
screen = lambda K, r, lam, vr: K * np.exp(-r/lam) / r**2
print("Rest-only fits (r=1,2,2,4,8): SSE, rms/coord (noise floor 0.050)")
N = sum(O.size for _,_,_,O in REST)
best = {}
for lab, form, grid in [("power", power, [2.0, 2.1, 2.2, 2.5]), ("screen", screen, [6.0, 8.0, 10.0, 14.0])]:
    for s in grid:
        K, S = fitK(form, s)
        print(f"  {lab:6s} shape={s:5.2f} K={K:8.3f} SSE={S:9.3f} rms={np.sqrt(S/N):.5f}")
        best.setdefault(lab, []).append((S, K, s))
bp = min(best["power"]); bs = min(best["screen"])
print(f"best power: P={bp[2]} K={bp[1]:.3f} rms={np.sqrt(bp[0]/N):.5f}; best screened: lam={bs[2]} K={bs[1]:.3f} rms={np.sqrt(bs[0]/N):.5f}")

# refine screened lambda
lam_grid = np.linspace(bs[2]-1, bs[2]+1, 5)
ref = []
for lam in lam_grid:
    K, S = fitK(screen, lam); ref.append((S, K, lam))
S_best, K_best, LAM = min(ref)
print(f"refined screened: lam={LAM:.2f} K={K_best:.3f} rms={np.sqrt(S_best/N):.5f}")
# per-run check at best screened
law = lambda r, vr: screen(K_best, r, LAM, vr)
for (x0, v0, t, O), nm in zip(REST, ["r3/001 r=2", "r3/002 r=1", "r3/003 r=4", "r1/009 r=2 y", "r3/004 r=8"]):
    res = O - integrate(x0, v0, t, law)
    print(f"  at rest {nm:12s} rms={np.sqrt((res**2).mean()):.4f} mean={res.mean(axis=(0,2)).round(4)}")

# velocity-term bound with the screened law fixed at the rest fit
gs = np.linspace(-0.03, 0.03, 31)
Ss = np.array([sse(MOVE, lambda r, vr: screen(K_best, r, LAM, vr) * (1 + g*vr)) for g in gs])
gi = gs[np.argmin(Ss)]
ok = gs[Ss <= Ss.min() + 3.84*0.05**2]
Nm = sum(O.size for _,_,_,O in MOVE)
print(f"velocity term on moving runs (r=2,4 approach/recede, |vr|=2): g_hat={gi:+.4f}, 95% range [{ok.min():+.4f},{ok.max():+.4f}]; rms(g=0)={np.sqrt(sse(MOVE, law)/Nm):.5f}")
