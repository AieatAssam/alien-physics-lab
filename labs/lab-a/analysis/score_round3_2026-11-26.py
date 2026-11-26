"""Score r3/001-008 (A-A window profile, T=0.4) and r2/009-010 (S20) with whole-run scale s
on the P-0027 table (clamped below r=3). Reads results and requests from repo root given as argv[1].
Usage: python3 -I score_round3_2026-11-26.py <repo_root>
"""
import json, math, os, sys
import numpy as np

ROOT = sys.argv[1]
L = 10.0
P = 2.5
R_TAB = np.array([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
K_TAB = np.array([17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624])
SIGMA = 0.05  # tracker noise per coordinate (notebook)
H = 0.002

def accel(pos, s):
    d = pos[1] - pos[0]
    r = math.hypot(d[0], d[1])
    f = s * float(np.interp(r, R_TAB, K_TAB)) / r ** P
    return np.array([f * d / r, -f * d / r])

def sim(pos, vel, s, times):
    out = []
    t = 0.0
    for target in times:
        while t < target - 1e-12:
            h = min(H, target - t)
            k1p, k1v = vel, accel(pos, s)
            p2, v2 = pos + h/2*k1p, vel + h/2*k1v
            k2p, k2v = v2, accel(p2, s)
            p3, v3 = pos + h/2*k2p, vel + h/2*k2v
            k3p, k3v = v3, accel(p3, s)
            p4, v4 = pos + h*k3p, vel + h*k3v
            k4p, k4v = v4, accel(p4, s)
            pos = pos + h/6*(k1p+2*k2p+2*k3p+k4p)
            vel = vel + h/6*(k1v+2*k2v+2*k3v+k4v)
            for i in range(2):
                for k in range(2):
                    if pos[i,k] < 0: pos[i,k] = -pos[i,k]; vel[i,k] = -vel[i,k]
                    elif pos[i,k] > L: pos[i,k] = 2*L-pos[i,k]; vel[i,k] = -vel[i,k]
            t += h
        t = target
        out.append(pos.copy())
    return np.array(out)

def load(rnd, n, day="2026-11-25"):
    if day == "2026-11-25":
        pass
    q = json.load(open(os.path.join(ROOT, f"requests/{day}/{rnd}/lab-a/{n:03d}.json")))
    r = json.load(open(os.path.join(ROOT, f"results/{day}/{rnd}/lab-a/{n:03d}.json")))
    return q, r

def fit(day, rnd, n):
    q, r = load(rnd, n, day)
    parts = sorted(q["setup"]["particles"], key=lambda p: 0)
    pos0 = np.array([p["pos"] for p in q["setup"]["particles"]], float)
    vel0 = np.zeros((2,2))
    samples = r["samples"]
    times = [s["t"] for s in samples]
    X = np.array([[p["pos"] for p in sorted(s["particles"], key=lambda z: z["id"])] for s in samples], float)
    mask = [t > 1e-12 for t in times]
    tt = [t for t in times if t > 1e-12]
    XX = X[1:]
    grid = np.linspace(0.80, 1.20, 401)
    chis = []
    for s in grid:
        pr = sim(pos0.copy(), vel0.copy(), s, tt)
        chis.append(np.sum((pr - XX)**2) / SIGMA**2)
    chis = np.array(chis)
    i = int(np.argmin(chis))
    # 1-sigma: chi2 increase of 1 around min
    ok = grid[chis <= chis[i] + 1.0]
    dof = XX.size - 1
    r0 = math.dist(pos0[0], pos0[1])
    sep = np.linalg.norm(XX[:,0,:]-XX[:,1,:], axis=1)
    return dict(id=f"{day}/{rnd}/{n:03d}", r0=round(r0,3), T=q["setup"]["duration"], s=round(float(grid[i]),4),
                s_lo=round(float(ok.min()),4), s_hi=round(float(ok.max()),4), chi2_dof=round(float(chis[i]/dof),3),
                min_sep=round(float(sep.min()),3), orient=None)

if __name__ == "__main__":
    runs = [("2026-11-25","r3",n) for n in range(1,9)] + [("2026-11-25","r2",9),("2026-11-25","r2",10)]
    for day, rnd, n in runs:
        print(json.dumps(fit(day, rnd, n)))
