"""Score 2026-11-24/r3/lab-b/001-004 (A-B far range x3, three-body prereg).

A-B fit: K_A free, K_B = ratio * K_A, P = 2.5; also free ratio with K_A free.
Three-body: judged RMSE/L of the pre-registered pairwise-additive prediction (prereg json) vs measured,
over the times listed in the prereg, sigma 0.05 per coordinate for chi2.
Usage: python3 -I score_r3_2026-11-25.py <repo_root>
"""
import sys, json, math, os
sys.path.insert(0, "/tmp/lab-b-pylib")
import numpy as np
from scipy.optimize import least_squares

SIGMA, L = 0.05, 10.0


def acc_pair(x, Ks, P):
    # Ks[i]: coefficient for particle i acting toward the partner (attraction if > 0)
    d = x[1] - x[0]
    r = math.hypot(d[0], d[1])
    u = d / r
    a0 = Ks[0] / r ** P * u
    a1 = -Ks[1] / r ** P * u
    return np.array([a0, a1])


def integrate_ab(x0, Ks, P, T, dt, h=0.001):
    x = np.array(x0, float); v = np.zeros_like(x)
    out = [x.copy()]
    n = int(round(T / h)); per = int(round(dt / h))
    for s in range(1, n + 1):
        a1 = acc_pair(x, Ks, P); x2, v2 = x + .5*h*v, v + .5*h*a1
        a2 = acc_pair(x2, Ks, P); x3, v3 = x + .5*h*v2, v + .5*h*a2
        a3 = acc_pair(x3, Ks, P); x4, v4 = x + h*v3, v + h*a3
        a4 = acc_pair(x4, Ks, P)
        x = x + h/6*(v + 2*v2 + 2*v3 + v4); v = v + h/6*(a1 + 2*a2 + 2*a3 + a4)
        if s % per == 0:
            out.append(x.copy())
    return out


def load(root, suf):
    req = json.load(open(os.path.join(root, "requests", suf + ".json")))
    res = json.load(open(os.path.join(root, "results", suf + ".json")))
    return req, res


def measured(res, T):
    ts, pos = [], []
    for s in res["samples"]:
        if 0 < s["t"] <= T + 1e-9:
            ts.append(s["t"])
            pos.append([[q["pos"][0], q["pos"][1]] for q in sorted(s["particles"], key=lambda q: q["id"])])
    return np.array(ts), np.array(pos)


def ab_fit(root, suf):
    req, res = load(root, suf)
    parts = req["setup"]["particles"]
    x0 = [p["pos"] for p in parts]
    sp = [p["species"] for p in parts]
    T, dt = req["setup"]["duration"], req["setup"]["sample_dt"]
    ts, meas = measured(res, T)
    n = len(ts)
    # Ks[0] acts on particle 0 (species sp[0]); Ks[1] on particle 1
    def sim(K_A, ratio):
        Ks = [K_A, K_A * ratio] if sp[0] == "A" else [K_A * ratio, K_A]
        return np.array(integrate_ab(x0, Ks, 2.5, T, dt)[1:n + 1])
    def resid_fixed(p):
        return (sim(p[0], 1.41) - meas).ravel()
    def resid_free(p):
        return (sim(p[0], p[1]) - meas).ravel()
    fixed = least_squares(resid_fixed, x0=[10.0], xtol=1e-10, ftol=1e-10)
    free = least_squares(resid_free, x0=[10.0, 1.41], xtol=1e-10, ftol=1e-10)
    out = {"id": suf, "species": sp, "r0": round(math.dist(x0[0], x0[1]), 4), "T": T, "n": n,
           "chi2n_fixed_1.41": round(float(np.mean((fixed.fun / SIGMA) ** 2)), 3),
           "K_A_fixed_ratio": round(float(fixed.x[0]), 3)}
    J = free.jac; cov = np.linalg.pinv(J.T @ J) * SIGMA ** 2; err = np.sqrt(np.diag(cov))
    out.update({"K_A_free": round(float(free.x[0]), 3), "dK_A": round(float(err[0]), 3),
                "ratio_free": round(float(free.x[1]), 3), "d_ratio": round(float(err[1]), 3),
                "chi2n_free": round(float(np.mean((free.fun / SIGMA) ** 2)), 3)})
    return out


def threebody(root, suf):
    req, res = load(root, suf)
    T = req["setup"]["duration"]
    pre = json.load(open(os.path.join(root, "labs/lab-b/analysis/prereg_3body_2026-11-24.json")))
    pred = pre["pred_positions_by_t"]
    res_map = {round(s["t"], 4): s for s in res["samples"]}
    sq = 0.0; cnt = 0; rows = []
    for tk, pp in pred.items():
        t = round(float(tk), 4)
        if t not in res_map:
            continue
        for q in res_map[t]["particles"]:
            for k in range(2):
                sq += (pp[q["id"]][k] - q["pos"][k]) ** 2; cnt += 1
        rows.append(t)
    return {"id": suf, "times_scored": rows, "rmse_over_L_vs_prereg": round(math.sqrt(sq / cnt) / L, 5) if cnt else None}


if __name__ == "__main__":
    root = sys.argv[1]
    res = [ab_fit(root, "2026-11-24/r3/lab-b/%03d" % i) for i in (1, 2, 3)]
    res.append(threebody(root, "2026-11-24/r3/lab-b/004"))
    print(json.dumps(res, indent=1))
