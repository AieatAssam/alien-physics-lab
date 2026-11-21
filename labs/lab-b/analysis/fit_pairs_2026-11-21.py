"""Lab-b pair fits, round 2 (2026-11-21). Pure python, run with python3 -I from repo root.

Model: two-or-more particles, pairwise acceleration on i from j = K[sp_i,sp_j] * (x_j - x_i) / r^2.5
(P = 2.5 fixed; r = current separation). Constant K per ordered species pair (no r-dependence).
Positive K = attraction. Fit by coordinate scan on tracker positions; report rms per coordinate,
RMSE/L (L = 10) as the judge computes it, and chi2/ndata with sd 0.05.
"""
import json, math, sys, os

L = 10.0
NOISE = 0.05


def load(rid):
    day, rnd, lab, n = rid.split("/")
    p = os.path.join("results", day, rnd, lab, n + ".json")
    return json.load(open(p))


def req(rid):
    day, rnd, lab, n = rid.split("/")
    return json.load(open(os.path.join("requests", day, rnd, lab, n + ".json")))


def simulate(species, x0, v0, Kmat, T, dt):
    n = len(species)
    x = [list(p) for p in x0]
    v = [list(p) for p in v0]

    def acc(xs):
        a = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dx = xs[j][0] - xs[i][0]
                dy = xs[j][1] - xs[i][1]
                r = math.hypot(dx, dy)
                f = Kmat[(species[i], species[j])] / (r ** 3.5)
                a[i][0] += f * dx
                a[i][1] += f * dy
        return a

    out = {0.0: [list(p) for p in x]}
    steps = int(round(T / dt))
    h = dt
    for s in range(1, steps + 1):
        a1 = acc(x)
        x2 = [[x[i][k] + 0.5 * h * v[i][k] for k in range(2)] for i in range(n)]
        v2 = [[v[i][k] + 0.5 * h * a1[i][k] for k in range(2)] for i in range(n)]
        a2 = acc(x2)
        x3 = [[x[i][k] + 0.5 * h * v2[i][k] for k in range(2)] for i in range(n)]
        v3 = [[v[i][k] + 0.5 * h * a2[i][k] for k in range(2)] for i in range(n)]
        a3 = acc(x3)
        x4 = [[x[i][k] + h * v3[i][k] for k in range(2)] for i in range(n)]
        v4 = [[v[i][k] + h * a3[i][k] for k in range(2)] for i in range(n)]
        a4 = acc(x4)
        for i in range(n):
            for k in range(2):
                x[i][k] += h / 6 * (v[i][k] + 2 * v2[i][k] + 2 * v3[i][k] + v4[i][k])
                v[i][k] += h / 6 * (a1[i][k] + 2 * a2[i][k] + 2 * a3[i][k] + a4[i][k])
        out[round(s * h, 9)] = [list(p) for p in x]
    return out


def score(res, Kmat, T_use=None):
    """Return (rmse_per_coord, judge_error = rmse_all/L, chi2/ndata, mean residual per particle)."""
    rq = req(res["request_id"])["setup"]["particles"]
    sp = [p["species"] for p in rq]
    x0 = [p["pos"] for p in rq]
    v0 = [p["vel"] for p in rq]
    T = res["samples"][-1]["t"]
    dt = res["samples"][1]["t"] - res["samples"][0]["t"]
    sim = simulate(sp, x0, v0, Kmat, T, dt if T_use is None else T_use)
    sq = 0.0
    cnt = 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t <= 0:
            continue
        key = t
        if key not in sim:
            continue
        for i, p in enumerate(s["particles"]):
            for k in range(2):
                d = p["pos"][k] - sim[key][i][k]
                sq += d * d
                cnt += 1
    rmse = math.sqrt(sq / cnt)
    return rmse, rmse / L, sq / (NOISE ** 2 * cnt)


def fit(res, pairs, grid):
    """Coordinate-descent fit of K for each ordered species pair in `pairs` (list of keys)."""
    K = {k: grid[0] for k in pairs}
    base = {}
    for k in pairs:
        base[k] = 0.0
    best = None
    for k in pairs:
        pass
    # initial: coarse scan per key
    cur = {k: 0.0 for k in pairs}
    for _ in range(3):
        for k in pairs:
            cands = [cur[k] + d for d in [x * 0.5 for x in range(-12, 13)]]
            bestc = None
            for c in cands:
                trial = dict(cur)
                trial[k] = c
                Kmat = mat(trial)
                r, e, chi = score(res, Kmat)
                if bestc is None or chi < bestc[0]:
                    bestc = (chi, c, r, e)
            cur[k] = bestc[1]
        # refine
        for k in pairs:
            cands = [cur[k] + d for d in [x * 0.05 for x in range(-10, 11)]]
            bestc = None
            for c in cands:
                trial = dict(cur)
                trial[k] = c
                r, e, chi = score(res, mat(trial))
                if bestc is None or chi < bestc[0]:
                    bestc = (chi, c, r, e)
            cur[k] = bestc[1]
    return cur


def mat(d):
    """d maps (sp_i, sp_j) -> K; symmetric fill for missing keys."""
    m = {}
    for (a, b), v in d.items():
        m[(a, b)] = v
    return m


if __name__ == "__main__":
    pass
