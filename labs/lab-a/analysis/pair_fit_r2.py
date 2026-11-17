"""Global fit of a central pair force F = -K * rhat / r^p (attractive for K>0) to
round-2 pair runs 004+005 (repeats pooled), using only t <= T_FIT (before the close
encounter at separation < ~1.5). Integrates both particles with RK4.
Run from repo root: python3 -I out/labs/lab-a/analysis/pair_fit_r2.py
"""
import json
import numpy as np
from scipy.optimize import least_squares

T_FIT = float(__import__("sys").argv[1]) if len(__import__("sys").argv) > 1 else 1.0

def load(n):
    d = json.load(open(f"results/2026-11-17/r2/lab-a/{n}.json"))
    t = np.array([s["t"] for s in d["samples"]])
    P = np.array([[p["pos"] for p in s["particles"]] for s in d["samples"]])
    return t, P

def accel(X, K, p, eps):
    # X: (2,2) positions; returns accelerations for both particles
    d = X[1] - X[0]
    r2 = d @ d + eps**2
    f = K * d / r2 ** ((p + 1) / 2)   # attraction toward partner, magnitude K/r^p
    return np.array([f, -f])

def simulate(t, X0, V0, K, p, eps, dt=0.005):
    out = np.zeros((len(t), 2, 2))
    X = X0.copy(); V = V0.copy(); tc = 0.0
    out[0] = X
    for i in range(1, len(t)):
        while tc < t[i] - 1e-12:
            h = min(dt, t[i] - tc)
            def f(x, v):
                return v, accel(x, K, p, eps)
            k1x, k1v = f(X, V)
            k2x, k2v = f(X + 0.5*h*k1x, V + 0.5*h*k1v)
            k3x, k3v = f(X + 0.5*h*k2x, V + 0.5*h*k2v)
            k4x, k4v = f(X + h*k3x, V + h*k3v)
            X = X + h/6*(k1x + 2*k2x + 2*k3x + k4x)
            V = V + h/6*(k1v + 2*k2v + 2*k3v + k4v)
            tc += h
        out[i] = X
    return out

t4, P4 = load("004"); t5, P5 = load("005")
t = t4; P = (P4 + P5) / 2.0   # repeats agree; pooled mean reduces noise by sqrt2
m = t <= T_FIT + 1e-9
X0 = np.array([[2.0, 5.0], [6.0, 5.5]])
V0 = np.array([[1.0, 0.0], [0.0, 0.0]])

def resid(theta):
    K, p, eps = theta
    sim = simulate(t[m], X0, V0, K, p, abs(eps))
    return (sim - P[m]).ravel()

best = None
for p0 in [1.0, 2.0, 3.0]:
    r = least_squares(resid, x0=[1.0, p0, 0.1], bounds=([0, 0, 0], [100, 6, 2]))
    if best is None or r.cost < best.cost:
        best = r
K, p, eps = best.x
res = best.fun
print(f"T_FIT={T_FIT}: K={K:.3f} p={p:.3f} eps={abs(eps):.3f}  rms resid={np.sqrt(np.mean(res**2)):.4f} (n={len(res)})")
# Jacobian-based standard errors
J = best.jac
cov = np.linalg.pinv(J.T @ J) * (np.sum(res**2) / max(len(res) - 3, 1))
se = np.sqrt(np.diag(cov))
print(f"  SE: K={se[0]:.3f} p={se[1]:.3f} eps={se[2]:.3f}")
# Free-motion (K=0) residual for comparison
sim0 = simulate(t[m], X0, V0, 0.0, 2.0, 0.1)
print(f"  no-interaction rms resid={np.sqrt(np.mean((sim0-P[m])**2)):.4f}")
# Predict later data (before scatter) with fitted params
m2 = t <= 2.3
sim_all = simulate(t[m2], X0, V0, K, p, abs(eps))
print("  residual rms over t<=2.3:", np.round(np.sqrt(np.mean((sim_all-P[m2])**2)),4))
