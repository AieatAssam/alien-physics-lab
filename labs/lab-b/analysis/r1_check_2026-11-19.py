"""Lab-b round-2 check of 2026-11-19 round-1 results (pure Python, no numpy).

Usage: python3 -I r1_check_2026-11-19.py

Model: pairwise sum. Acceleration on i from j is K_i(j) * (x_j - x_i) / r^3.5,
where r is the instantaneous separation and K_i(j) is the coefficient at the
pair's *initial* separation (table from lab-b notebook, sep 3/4/5 rows).
Positive K = attraction.
"""
import json
import math
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
REPO = os.environ.get("REPO", os.getcwd())


def load(p):
    return json.load(open(os.path.join(REPO, p)))


def simulate(parts, coef, T, h, record_every):
    """RK4 with fixed step h. coef(i, j, sp_i, sp_j) -> K. Returns list of (t, [pos...])."""
    n = len(parts)
    x = [list(p["pos"]) for p in parts]
    v = [list(p["vel"]) for p in parts]
    sp = [p["species"] for p in parts]
    # coefficients fixed at the initial separation of each pair
    K = {}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            r0 = math.dist(parts[i]["pos"], parts[j]["pos"])
            K[(i, j)] = coef(i, j, sp[i], sp[j], r0)

    def acc(xs):
        a = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dx = xs[j][0] - xs[i][0]
                dy = xs[j][1] - xs[i][1]
                r = math.hypot(dx, dy)
                f = K[(i, j)] / (r ** 3.5)
                a[i][0] += f * dx
                a[i][1] += f * dy
        return a

    out = [(0.0, [list(p) for p in x])]
    steps = int(round(T / h))
    t = 0.0
    for s in range(1, steps + 1):
        # state-derivative RK4 on (x, v)
        a1 = acc(x)
        k1x = v; k1v = a1
        x2 = [[x[i][k] + 0.5 * h * k1x[i][k] for k in range(2)] for i in range(n)]
        v2 = [[v[i][k] + 0.5 * h * k1v[i][k] for k in range(2)] for i in range(n)]
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
        t = s * h
        if s % record_every == 0:
            out.append((t, [list(p) for p in x]))
    return out


def residuals(res, sim, tmax, rmin=0.0):
    """Compare tracker samples to sim at matching times (within tmax)."""
    simd = {round(t, 7): xs for t, xs in sim}
    n = len(res["samples"][0]["particles"])
    stats = [dict(sq=[0.0, 0.0], sm=[0.0, 0.0], c=0) for _ in range(n)]
    mx = 0.0
    for s in res["samples"]:
        t = round(float(s["t"]), 7)
        if t <= 0 or t > tmax + 1e-9 or t not in simd:
            continue
        xs = simd[t]
        for i in range(n):
            for k in range(2):
                d = s["particles"][i]["pos"][k] - xs[i][k]
                stats[i]["sq"][k] += d * d
                stats[i]["sm"][k] += d
                mx = max(mx, abs(d))
            stats[i]["c"] += 1
    rep = []
    for i in range(n):
        c = max(stats[i]["c"], 1)
        rms = [math.sqrt(stats[i]["sq"][k] / c) for k in range(2)]
        mean = [stats[i]["sm"][k] / c for k in range(2)]
        rep.append((rms, mean))
    return rep, mx


def fmt(rep, mx):
    lines = []
    for i, (rms, mean) in enumerate(rep):
        lines.append(f"    p{i}: rms=({rms[0]:.4f},{rms[1]:.4f}) mean=({mean[0]:+.4f},{mean[1]:+.4f})")
    lines.append(f"    max|res|={mx:.3f}")
    return "\n".join(lines)


def table_coef(table):
    def coef(i, j, si, sj, r0):
        key = (si, sj)
        rr = round(r0)
        return table[key][rr]
    return coef


# Pre-registered table (lab-b notebook). Keyed by ordered species pair then by
# integer initial separation. Values are K_i(j) for particle i on j.
TABLE = {
    ("A", "B"): {3: 8.95, 4: 9.16, 5: 8.94},
    ("B", "A"): {3: 12.58, 4: 12.92, 5: 12.58},
    ("A", "C"): {3: -8.97, 4: -9.06, 5: -8.72},
    ("C", "A"): {3: -21.40, 4: -21.67, 5: -20.97},
    ("B", "C"): {3: -6.41, 4: -6.42, 5: -6.34},
    ("C", "B"): {3: -10.66, 4: -10.91, 5: -10.45},
}


def main():
    print("== Triangle additivity (pre-registered, falsify if >0.05 per coord, t<=1.0)")
    for rid in ["006", "007"]:
        req = load(f"requests/2026-11-19/r1/lab-b/{rid}.json")
        res = load(f"results/2026-11-19/r1/lab-b/{rid}.json")
        sim = simulate(req["setup"]["particles"], table_coef(TABLE), 1.0, 0.0005, 1)
        rep, mx = residuals(res, sim, 1.0)
        print(f"  {rid}:")
        print(fmt(rep, mx))
    print("== Pair replicates (B-B, C-C at sep 5, T=2): fit single K on both particles")
    for rid, sp in [("001", "B"), ("002", "C")]:
        req = load(f"requests/2026-11-19/r1/lab-b/{rid}.json")
        res = load(f"results/2026-11-19/r1/lab-b/{rid}.json")
        best = None
        for K10 in [x / 100 for x in range(400, 1500, 10)]:
            sim = simulate(req["setup"]["particles"], lambda i, j, a, b, r0: K10, 2.0, 0.001, 1)
            rep, mx = residuals(res, sim, 2.0)
            ssq = sum(r[0][0] ** 2 + r[0][1] ** 2 for r in rep)
            if best is None or ssq < best[0]:
                best = (ssq, K10, rep, mx)
        print(f"  {rid} ({sp}-{sp}): best K={best[1]:.2f}")
        print(fmt(best[2], best[3]))


if __name__ == "__main__":
    main()
