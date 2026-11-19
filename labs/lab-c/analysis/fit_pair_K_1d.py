"""Fit signed per-particle pair coefficients K1, K2 for two-particle runs on the x-axis at rest.

Model (P = 2.5 fixed, chamber L = 10, specular walls): particle 1 (left) accelerates +x by K1/r^2.5,
particle 2 (right) accelerates -x by K2/r^2.5 (K > 0 attracts, K < 0 repels). Positions are 1-D in x.
Fit: alternating golden-section scans on the sum of squared x-residuals (tracker) over all samples.
Also reports rms residual and the y-spread (should be noise only).
Usage: python3 -I fit_pair_K_1d.py <repo_root> <run ids like 2026-11-19/r1/lab-c/013 ...>
"""
import json, math, os, sys

P = 2.5
L = 10.0
H = 0.005
WALLS = True


def simulate(x1_0, x2_0, K1, K2, ts):
    # 1-D RK4 for x1, x2 with specular walls; returns list of (x1, x2) at times ts (sorted, starting at 0)
    x1, x2 = x1_0, x2_0
    v1 = v2 = 0.0
    t = 0.0
    out = []
    def acc(a, b):
        r = b - a
        m = abs(r) ** P
        return K1 / m * (1 if r > 0 else -1), K2 / m * (-1 if r > 0 else 1)
    for target in ts:
        while t < target - 1e-12:
            h = min(H, target - t)
            a1, a2 = acc(x1, x2)
            k1 = (v1, v2, a1, a2)
            def st(s):
                return (x1 + s * 0.5 * h * k1[0], x2 + s * 0.5 * h * k1[1]), (v1 + s * 0.5 * h * k1[2], v2 + s * 0.5 * h * k1[3])
            (p1, p2), (w1, w2) = st(1)
            b1, b2 = acc(p1, p2)
            k2 = (w1, w2, b1, b2)
            (p1, p2), (w1, w2) = (x1 + 0.5 * h * k2[0], x2 + 0.5 * h * k2[1]), (v1 + 0.5 * h * k2[2], v2 + 0.5 * h * k2[3])
            c1, c2 = acc(p1, p2)
            k3 = (w1, w2, c1, c2)
            (p1, p2), (w1, w2) = (x1 + h * k3[0], x2 + h * k3[1]), (v1 + h * k3[2], v2 + h * k3[3])
            d1, d2 = acc(p1, p2)
            k4 = (w1, w2, d1, d2)
            x1 += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            x2 += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            v1 += h / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
            v2 += h / 6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
            # specular walls
            for idx in ((1, 2) if WALLS else ()):
                if idx == 1:
                    if x1 < 0: x1, v1 = -x1, -v1
                    elif x1 > L: x1, v1 = 2 * L - x1, -v1
                else:
                    if x2 < 0: x2, v2 = -x2, -v2
                    elif x2 > L: x2, v2 = 2 * L - x2, -v2
            t += h
        out.append((x1, x2))
    return out


def cost(K1, K2, x1_0, x2_0, data):
    sim = simulate(x1_0, x2_0, K1, K2, [t for t, _, _ in data])
    s = 0.0
    for (p1, p2), (_, o1, o2) in zip(sim, data):
        s += (p1 - o1) ** 2 + (p2 - o2) ** 2
    return s


def golden(f, lo, hi, tol=1e-3):
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    while abs(b - a) > tol:
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a); fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a); fd = f(d)
    return (a + b) / 2


def fit_run(res, req):
    global WALLS
    parts = req["setup"]["particles"]
    p0, p1 = parts[0]["pos"], parts[1]["pos"]
    d = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    u = ((p1[0] - p0[0]) / d, (p1[1] - p0[1]) / d)
    axis_aligned = abs(u[1]) < 1e-9
    WALLS = axis_aligned  # diagonal runs: wall-free projection (checked separately)
    proj = lambda p: p[0] * u[0] + p[1] * u[1]
    x1_0, x2_0 = proj(p0), proj(p1)
    data = [(s["t"], proj(s["particles"][0]["pos"]), proj(s["particles"][1]["pos"])) for s in res["samples"] if s["t"] > 0]
    ts = [t for t, _, _ in data]
    # alternating scans, bracket wide
    K1, K2 = 0.0, 0.0
    for _ in range(3):
        K1 = golden(lambda k: cost(k, K2, x1_0, x2_0, data), -60, 60, tol=0.01)
        K2 = golden(lambda k: cost(K1, k, x1_0, x2_0, data), -60, 60, tol=0.01)
    sim = simulate(x1_0, x2_0, K1, K2, ts)
    rr1 = [p1 - o1 for (p1, _), (_, o1, _) in zip(sim, data)]
    rr2 = [p2 - o2 for (_, p2), (_, _, o2) in zip(sim, data)]
    rms = math.sqrt(sum(e * e for e in rr1 + rr2) / (2 * len(rr1)))
    ys = [s["particles"][k]["pos"][1] for s in res["samples"] for k in (0, 1)]
    if not axis_aligned:
        ys = [s["particles"][k]["pos"][0] for s in res["samples"] for k in (0, 1)]
    ymean = sum(ys) / len(ys)
    yrms = math.sqrt(sum((y - ymean) ** 2 for y in ys) / len(ys))
    return K1, K2, rms, yrms, parts[0]["species"], parts[1]["species"], d


if __name__ == "__main__":
    root = sys.argv[1]
    for rid in sys.argv[2:]:
        base = os.path.join(root, "results", rid.replace("/", os.sep)) + ".json"
        rqb = os.path.join(root, "requests", rid.replace("/", os.sep)) + ".json"
        res = json.load(open(base))
        req = json.load(open(rqb))
        if len(req["setup"]["particles"]) != 2:
            print(rid, "not two-particle; skipped")
            continue
        K1, K2, rms, yrms, s1, s2, r0 = fit_run(res, req)
        r0 = round(r0, 2)
        print("%s  %s-%s r=%.1f  K_%s=%+.3f  K_%s=%+.3f  x-rms=%.4f  y-spread=%.4f" % (
            rid, s1, s2, r0, s1, K1, s2, K2, rms, yrms))
