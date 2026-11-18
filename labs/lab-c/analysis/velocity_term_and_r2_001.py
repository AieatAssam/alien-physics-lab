"""(1) Bound on a velocity term: a = K/r^P * (1 + g * vr), vr = relative radial velocity (positive = receding),
K,P fixed at the rest-fitted law. Fit g on approach/recede/comove runs (full trajectory, 2 coords).
(2) Round-2 energy case: 2026-11-17/r2/lab-c/001 (A-A at rest r=3, close approach, then separation to ~10),
compare the observed separation d(t) with the predictions of two conservative laws
(rest-fitted K=11.42,P=2.10; P-0003 K=17.74,P=2.50). Separation is id-free, so the tracker id swap does not matter.
Usage: python3 -I velocity_term_and_r2_001.py   (repo root)
"""
import json, numpy as np
H = 0.001
K_REST, P_REST = 11.423, 2.10

def load(d, n):
    q = json.load(open(f"requests/{d}/lab-c/{n}.json")); r = json.load(open(f"results/{d}/lab-c/{n}.json"))
    x0 = np.array([p["pos"] for p in q["setup"]["particles"]], float)
    v0 = np.array([p["vel"] for p in q["setup"]["particles"]], float)
    times = np.array([s["t"] for s in r["samples"]])
    O = np.zeros((len(times), 2, 2))
    for k, s in enumerate(r["samples"]):
        for p in s["particles"]:
            O[k, p["id"]] = p["pos"]
    return x0, v0, times, O, q, r

def integrate(x0, v0, times, law):
    x = x0.copy(); v = v0.copy(); out = np.zeros((len(times), 2, 2)); t = 0.0
    def acc(x, v):
        d = x[1] - x[0]; r = np.linalg.norm(d); u = d/r
        vr = np.dot(v[1]-v[0], u)           # relative radial velocity, positive = receding
        f = law(r, vr)
        return np.array([f*u, -f*u])
    for k, T in enumerate(times):
        while t < T - 1e-12:
            h = min(H, T - t)
            a1 = acc(x, v); x2 = x + h/2*v; v2 = v + h/2*a1; a2 = acc(x2, v2)
            x3 = x + h/2*v2; v3 = v + h/2*a2; a3 = acc(x3, v3)
            x4 = x + h*v3; v4 = v + h*a3; a4 = acc(x4, v4)
            x = x + h/6*(v + 2*v2 + 2*v3 + v4); v = v + h/6*(a1 + 2*a2 + 2*a3 + a4); t += h
        out[k] = x
    return out

# ---- (1) velocity-term bound
MOVE = [("2026-11-18/r1", "001"), ("2026-11-18/r1", "002"), ("2026-11-18/r1", "004"), ("2026-11-18/r1", "005")]
data = [load(d, n)[:4] for d, n in MOVE]
def sse_g(g):
    law = lambda r, vr: K_REST / r**P_REST * (1 + g*vr)
    return sum(((O - integrate(x0, v0, times, law))**2).sum() for x0, v0, times, O in data)
gs = np.linspace(-0.2, 0.2, 41)
S = np.array([sse_g(g) for g in gs])
gi = gs[np.argmin(S)]
N = sum(O.size for _, _, _, O in data)
sig2 = 0.05**2
# approximate 1-sigma / 95% range from Delta SSE = 4*sigma^2 (chi2 with 1 dof, 95%)
ok = gs[S <= S.min() + 3.84*sig2]
print(f"(1) velocity-term fit (K={K_REST}, P={P_REST} fixed): g_hat={gi:+.4f}, 95% range ~[{ok.min():+.4f},{ok.max():+.4f}]")
print(f"    relative radial speed for these runs: |vr| = 2.0 (r=2 approach/recede, speed 1 each) and 2.0 (r=4)")
print(f"    => acceleration change at |vr|=2 bounded to about +/-{100*max(abs(ok.min()),abs(ok.max()))*2:.0f}% (95%)")

# ---- (2) round-2 001 energy case
x0, v0, times, O, q, r = load("2026-11-17/r2", "001")
print(f"\n(2) 2026-11-17/r2/lab-c/001: duration={q['setup']['duration']} sample_dt={q['setup']['sample_dt']} particles={[(p['pos'],p['vel']) for p in q['setup']['particles']]}")
dobs = np.linalg.norm(O[:,1,:]-O[:,0,:], axis=1)
laws = {"rest-fit K=11.42,P=2.10": lambda rr,vr: K_REST/rr**P_REST,
        "P-0003 K=17.74,P=2.50": lambda rr,vr: 17.74/rr**2.5}
preds = {k: integrate(x0, v0, times, law) for k, law in laws.items()}
print(f"{'t':>5s} {'d_obs':>7s} " + " ".join(f"{k:>24s}" for k in laws))
for tt in [0.5, 0.9, 1.1, 1.2, 1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0, 10.0]:
    if tt > times[-1] + 1e-9: break
    k = int(np.argmin(np.abs(times-tt)))
    row = f"{times[k]:5.2f} {dobs[k]:7.3f} " + " ".join(f"{np.linalg.norm(preds[n][k,1]-preds[n][k,0]):24.3f}" for n in laws)
    print(row)
for name in laws:
    dp = np.linalg.norm(preds[name][:,1]-preds[name][:,0], axis=1)
    err = np.abs(dp - dobs)
    print(f"{name}: rms(d_pred - d_obs) over run = {np.sqrt(((dp-dobs)**2).mean()):.3f}; max |diff| = {err.max():.3f} at t={times[err.argmax()]:.2f}")
