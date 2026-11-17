"""Scan power-law exponent n for A-B (or other) pair runs, starting from the EXACT requested
initial state (not the noisy t=0 sample). Force F = k * r^(-n), attractive if k>0.
Grid over mass ratio mb (m_A=1) and coupling k. Reports rms residual (noise expected ~0.05 per coord).
Usage: python3 -I pair_scan.py"""
import json, math, sys

REQ = "/home/runner/work/alien-physics-lab/alien-physics-lab/requests/2026-11-17/"
RES = "/home/runner/work/alien-physics-lab/alien-physics-lab/results/2026-11-17/"
RUNS = [
    ("r2/lab-b/002", "r2/lab-b/002", 1.8),  # A-B sep 4 (request r2/002)
    ("r2/lab-b/003", "r2/lab-b/003", 1.8),  # A-B sep 1
    ("r2/lab-b/004", "r2/lab-b/004", 0.85), # A-B offset, short window
    ("r1/lab-b/002", "r1/lab-b/002", 1.4),  # A-B sep 2, round 1 (dt 0.1)
]
DT = 0.002

def setup(rid):
    r = json.load(open(REQ + rid + ".json"))
    return [p["species"] for p in r["setup"]["particles"]], [p["pos"] for p in r["setup"]["particles"]]

def obs(rid, tmax):
    d = json.load(open(RES + rid + ".json"))
    return [(s["t"], [p["pos"] for p in s["particles"]]) for s in d["samples"] if s["t"] <= tmax + 1e-9 and s["t"] > 0]

def run(sp, x0, mass, k, n, times):
    ms = [1.0 if s == "A" else mass[s] for s in sp]
    x = [list(p) for p in x0]; v = [[0.0, 0.0], [0.0, 0.0]]
    def acc(x):
        dx, dy = x[1][0]-x[0][0], x[1][1]-x[0][1]
        r = max(math.hypot(dx, dy), 1e-4)
        F = k * r ** (-n)
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
            h = min(DT, T - t)
            x, v = step(x, v, h); t += h
        out.append(x)
    return out

def rms_for(mass, k, n, data):
    tot = 0.0; cnt = 0
    for sp, x0, ob in data:
        pred = run(sp, x0, mass, k, n, [o[0] for o in ob])
        for (t, pos), pr in zip(ob, pred):
            for i in range(2):
                for c in (0, 1):
                    tot += (pos[i][c]-pr[i][c])**2; cnt += 1
    return math.sqrt(tot/cnt)

if __name__ == "__main__":
    data = []
    for rid, rrid, tmax in RUNS:
        sp, x0 = setup(rid)
        data.append((sp, x0, obs(rid, tmax)))
    results = []
    for n in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        best = None
        for mb in [0.5, 0.6, 0.7, 0.8, 1.0]:
            for kk in [0.5, 1, 2, 4, 8, 16, 32]:
                k = kk * (1.0 if n == 0 else 1.0)
                r = rms_for({"B": mb, "C": 1.0}, k, n, data)
                if best is None or r < best[0]:
                    best = (r, mb, k)
        # refine k, mb near best
        r0, mb0, k0 = best
        for mb in [mb0*0.9, mb0, mb0*1.1]:
            for kf in [0.7, 0.85, 1.0, 1.15, 1.3]:
                r = rms_for({"B": mb, "C": 1.0}, k0*kf, n, data)
                if r < best[0]:
                    best = (r, mb, k0*kf)
        print(f"n={n}: best rms={best[0]:.4f} mb={best[1]:.3f} kAB={best[2]:.3f}", flush=True)
