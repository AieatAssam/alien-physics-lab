"""Constant-K pair fits, a = K / r^2.5 toward partner, two particles, at rest, walls specular.
Fits K_i (acceleration of particle i due to j) by least squares on tracker positions, t > 0.
Usage: python3 -I pairfit_2026-11-22.py <repo_root> <request_path_suffix> [...]
"""
import sys, json, math, os
sys.path.insert(0, "/tmp/lab-b-pylib")
import numpy as np
from scipy.optimize import least_squares

P = 2.5
L = 10.0
H = 0.002

def integrate(pos0, species, Kmap, duration, dt):
    pos = np.array(pos0, float); vel = np.zeros((2, 2))
    def acc(p):
        d = p[1] - p[0]; r = math.hypot(*d)
        a = np.zeros((2, 2))
        a[0] = Kmap[species[0]] / r**P * d / r
        a[1] = -Kmap[species[1]] / r**P * d / r
        return a
    n = int(round(duration / dt)); out = [pos.copy()]; t = 0.0
    for i in range(1, n + 1):
        target = i * dt
        while t < target - 1e-12:
            h = min(H, target - t)
            k1p, k1v = vel, acc(pos)
            p2, v2 = pos + h/2*k1p, vel + h/2*k1v; k2p, k2v = v2, acc(p2)
            p3, v3 = pos + h/2*k2p, vel + h/2*k2v; k3p, k3v = v3, acc(p3)
            p4, v4 = pos + h*k3p, vel + h*k3v; k4p, k4v = v4, acc(p4)
            pos = pos + h/6*(k1p + 2*k2p + 2*k3p + k4p)
            vel = vel + h/6*(k1v + 2*k2v + 2*k3v + k4v)
            t += h
        out.append(pos.copy())
    return out

def run(root, suffix):
    req = json.load(open(os.path.join(root, "requests", suffix + ".json")))
    res = json.load(open(os.path.join(root, "results", suffix + ".json")))
    parts = req["setup"]["particles"]
    species = [p["species"] for p in parts]
    pos0 = [p["pos"] for p in parts]
    sep = math.dist(pos0[0], pos0[1])
    dur = req["setup"]["duration"]; dt = req["setup"]["sample_dt"]
    meas = []
    for s in res["samples"]:
        if s["t"] <= 0: continue
        meas.append(np.array([[q["pos"][0], q["pos"][1]] for q in sorted(s["particles"], key=lambda q: q["id"])]))
    names = sorted(set(species))
    def resid(k):
        Km = {}
        # K for particle i's species from j; if same species both, shared K
        Km = {}
        Km[species[0]] = k[0]
        Km[species[1]] = k[1]
        traj = integrate(pos0, species, Km, dur, dt)
        r = []
        for idx, m in enumerate(meas):
            pr = traj[idx + 1]
            r.append((pr - m).ravel())
        return np.concatenate(r)
    if species[0] == species[1]:
        raise SystemExit("same species not handled here")
    fit = least_squares(resid, x0=[-8.0, -8.0], xtol=1e-10, ftol=1e-10)
    rr = fit.fun
    chi2n = float(np.mean((rr / 0.05) ** 2))
    J = fit.jac
    cov = np.linalg.pinv(J.T @ J) * (0.05**2)
    err = np.sqrt(np.diag(cov))
    return dict(id=req["request_id"], sp=("".join(species)), sep=round(sep, 3), T=dur,
                K_first=(species[0], round(fit.x[0], 3), round(err[0], 3)),
                K_second=(species[1], round(fit.x[1], 3), round(err[1], 3)),
                rms_L=round(float(np.sqrt(np.mean(rr**2)) / L), 5), chi2n=round(chi2n, 3))

if __name__ == "__main__":
    root = sys.argv[1]
    for s in sys.argv[2:]:
        print(json.dumps(run(root, s)))
