"""A-B runs with softened power-law force F = k * r / (r^2 + eps^2)^((n+1)/2)  (attractive for k>0).
eps = 0 gives F = k r^-n. Grid over eps, n, mb, k per run. Pure python.
Usage: python3 -I soft_fit.py"""
import math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pair_scan import setup, obs, DT

def run_soft(sp, x0, mass, k, n, eps, times):
    ms = [1.0 if s == "A" else mass[s] for s in sp]
    x = [list(p) for p in x0]; v = [[0.0, 0.0], [0.0, 0.0]]
    def acc(x):
        dx, dy = x[1][0]-x[0][0], x[1][1]-x[0][1]
        r = math.hypot(dx, dy)
        F = k * r / (r*r + eps*eps) ** ((n+1)/2) if r > 0 else 0.0
        if r == 0: return [[0.0, 0.0], [0.0, 0.0]]
        ux, uy = dx/r, dy/r
        return [[F*ux/ms[0], F*uy/ms[0]], [-F*ux/ms[1], -F*uy/ms[1]]]
    def step(x, v, h):
        a1 = acc(x)
        x2 = [[x[i][c]+0.5*h*v[i][c] for c in (0,1)] for i in range(2)]
        v2 = [[v[i][c]+0.5*h*a1[i][c] for c in (0,1)] for i in range(2)]
        a2 = acc(x2)
        x3 = [[x[i][c]+0.5*h*v2[i][c] for c in (0,1)] for i in range(2)]
        v3 = [[v[i][c]+0.5*h*a2[i][c] for c in (0,1)] for i in range(2)]
        a3 = acc(x3)
        x4 = [[x[i][c]+h*v3[i][c] for c in (0,1)] for i in range(2)]
        v4 = [[v[i][c]+h*a3[i][c] for c in (0,1)] for i in range(2)]
        a4 = acc(x4)
        xn = [[x[i][c]+h/6*(v[i][c]+2*v2[i][c]+2*v3[i][c]+v4[i][c]) for c in (0,1)] for i in range(2)]
        vn = [[v[i][c]+h/6*(a1[i][c]+2*a2[i][c]+2*a3[i][c]+a4[i][c]) for c in (0,1)] for i in range(2)]
        return xn, vn
    t = 0.0; out = []
    for T in times:
        while t < T - 1e-12:
            h = min(DT, T - t); x, v = step(x, v, h); t += h
        out.append(x)
    return out

def rms(data, mb, k, n, eps):
    tot = 0.0; cnt = 0
    for sp, x0, ob in data:
        pred = run_soft(sp, x0, {"B": mb, "C": 1.0}, k, n, eps, [o[0] for o in ob])
        for (t, pos), pr in zip(ob, pred):
            for i in range(2):
                for c in (0, 1):
                    tot += (pos[i][c]-pr[i][c])**2; cnt += 1
    return math.sqrt(tot/cnt)

if __name__ == "__main__":
    RUNS = [("r2/lab-b/003", 1.8), ("r1/lab-b/002", 1.4), ("r2/lab-b/002", 1.8), ("r2/lab-b/004", 0.85)]
    for rid, tmax in RUNS[:2]:
        sp, x0 = setup(rid)
        data = [(sp, x0, obs(rid, tmax))]
        best = None
        for n in [0.5, 1.0, 2.0]:
            for eps in [0.0, 0.2, 0.4, 0.7]:
                for mb in [0.6, 0.7]:
                    for k in [0.5, 1, 2, 4, 8]:
                        r = rms(data, mb, k, n, eps)
                        if best is None or r < best[0]:
                            best = (r, n, eps, mb, k)
        print(rid, "best rms %.3f n=%s eps=%s mb=%s k=%s" % best, flush=True)
