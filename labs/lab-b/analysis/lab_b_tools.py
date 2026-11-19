"""Lab-b shared tools for the 2026-11-19 round-2 session (pure Python, no numpy).

Pairwise model: acceleration on i from j = K_i(j) * (x_j - x_i) / r^3.5 (P = 2.5),
K fixed per ordered species pair and initial separation. Positive K = attraction.
Run with `python3 -I`, from the repo root (paths relative to REPO = cwd).
"""
import json
import math
import os

REPO = os.getcwd()


def load(p):
    return json.load(open(os.path.join(REPO, p)))


def simulate(parts, coef, T, h, record_every=1):
    """RK4, fixed step h. coef(i, j, sp_i, sp_j, r0) -> K_i(j). Returns [(t, [pos])]."""
    n = len(parts)
    x = [list(p["pos"]) for p in parts]
    v = [list(p["vel"]) for p in parts]
    sp = [p["species"] for p in parts]
    K = {(i, j): coef(i, j, sp[i], sp[j], math.dist(parts[i]["pos"], parts[j]["pos"]))
         for i in range(n) for j in range(n) if i != j}

    def acc(xs):
        a = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dx = xs[j][0] - xs[i][0]
                dy = xs[j][1] - xs[i][1]
                f = K[(i, j)] / (math.hypot(dx, dy) ** 3.5)
                a[i][0] += f * dx
                a[i][1] += f * dy
        return a

    out = [(0.0, [list(p) for p in x])]
    for s in range(1, int(round(T / h)) + 1):
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
        if s % record_every == 0:
            out.append((s * h, [list(p) for p in x]))
    return out


def residuals(res, sim, tmax):
    """Per-particle rms/mean residual per coordinate over samples with 0 < t <= tmax."""
    simd = {round(t, 7): xs for t, xs in sim}
    n = len(res["samples"][0]["particles"])
    sq = [[0.0, 0.0] for _ in range(n)]
    sm = [[0.0, 0.0] for _ in range(n)]
    cnt = 0
    mx = 0.0
    for s in res["samples"]:
        t = round(float(s["t"]), 7)
        if t <= 0 or t > tmax + 1e-9 or t not in simd:
            continue
        cnt += 1
        for i in range(n):
            for k in range(2):
                d = s["particles"][i]["pos"][k] - simd[t][i][k]
                sq[i][k] += d * d
                sm[i][k] += d
                mx = max(mx, abs(d))
    rep = [([math.sqrt(sq[i][k] / cnt) for k in range(2)], [sm[i][k] / cnt for k in range(2)])
           for i in range(n)]
    return rep, mx


def fmt(rep, mx):
    lines = [f"    p{i}: rms=({r[0]:.4f},{r[1]:.4f}) mean=({m[0]:+.4f},{m[1]:+.4f})"
             for i, (r, m) in enumerate(rep)]
    lines.append(f"    max|res|={mx:.3f}")
    return "\n".join(lines)


def fit_single_K(req, res, tmax, h, lo, hi, step):
    """Fit one K shared by all ordered pairs (equal species pair, e.g. B-B or A-A)."""
    best = None
    k = lo
    while k <= hi + 1e-9:
        sim = simulate(req["setup"]["particles"], lambda i, j, a, b, r0, k=k: k, tmax, h, 1)
        rep, mx = residuals(res, sim, tmax)
        ssq = sum(r[0][0] ** 2 + r[0][1] ** 2 for r in rep)
        if best is None or ssq < best[0]:
            best = (ssq, k, rep, mx)
        k += step
    return best  # (ssq, K, rep, mx)
