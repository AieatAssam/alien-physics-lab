"""lab-a round-2 (and round-1 repeat) fits, 2026-11-18.

Model: two particles, zero initial velocity (as requested), acceleration of
particle i = K_i * r^(-P) * unit(toward other particle), P fixed at 2.5.
K_i > 0 attracts, K_i < 0 repels. Free parameters K0, K1 (per particle).
For same-species pairs by symmetry K0 and K1 should agree; both are reported.

Pure python (numpy not installed). RK4 integrator, step dt (default 0.005).
Usage: python3 -I round2_2026-11-18.py <repo_root>
"""
import sys, math, json, os

ROOT = sys.argv[1]
P = 2.5
DT = 0.005


def load(day, rnd, n):
    base = os.path.join(ROOT)
    req = json.load(open(os.path.join(base, f"requests/{day}/{rnd}/lab-a/{n:03d}.json")))
    res = json.load(open(os.path.join(base, f"results/{day}/{rnd}/lab-a/{n:03d}.json")))
    return req, res


def deriv(s, K0, K1):
    x0, y0, x1, y1, vx0, vy0, vx1, vy1 = s
    rx, ry = x1 - x0, y1 - y0
    r = math.hypot(rx, ry)
    f = r ** (-P)
    ux, uy = rx / r, ry / r
    return (vx0, vy0, vx1, vy1,
            K0 * f * ux, K0 * f * uy,
            -K1 * f * ux, -K1 * f * uy)


def simulate(req, K0, K1, dt=DT):
    """Return dict: sample index -> (x0,y0,x1,y1) at multiples of sample_dt."""
    p = req["setup"]["particles"]
    s = (p[0]["pos"][0], p[0]["pos"][1], p[1]["pos"][0], p[1]["pos"][1],
         p[0]["vel"][0], p[0]["vel"][1], p[1]["vel"][0], p[1]["vel"][1])
    T = req["setup"]["duration"]
    sdt = req["setup"]["sample_dt"]
    every = int(round(sdt / dt))
    nsteps = int(round(T / dt))
    out = {0: s[:4]}
    for k in range(1, nsteps + 1):
        k1 = deriv(s, K0, K1)
        s2 = tuple(a + 0.5 * dt * b for a, b in zip(s, k1))
        k2 = deriv(s2, K0, K1)
        s3 = tuple(a + 0.5 * dt * b for a, b in zip(s, k2))
        k3 = deriv(s3, K0, K1)
        s4 = tuple(a + dt * b for a, b in zip(s, k3))
        k4 = deriv(s4, K0, K1)
        s = tuple(a + dt / 6.0 * (b + 2 * c + 2 * d + e)
                  for a, b, c, d, e in zip(s, k1, k2, k3, k4))
        if k % every == 0:
            out[k // every] = s[:4]
    return out


def residual(req, res, K0, K1, dt=DT):
    sim = simulate(req, K0, K1, dt)
    sdt = req["setup"]["sample_dt"]
    ss, n = 0.0, 0
    for smp in res["samples"]:
        idx = int(round(smp["t"] / sdt))
        if idx not in sim:
            continue
        pred = sim[idx]
        for j, part in enumerate(smp["particles"]):
            # particles are listed in request order (id 0, 1)
            px, py = pred[2 * j], pred[2 * j + 1]
            ss += (part["pos"][0] - px) ** 2 + (part["pos"][1] - py) ** 2
            n += 2
    return ss, n


def fit_pair(req, res, lo=-30.0, hi=30.0, ngrid=24):
    """Coarse grid then pattern-search refinement over (K0, K1)."""
    best = None
    for i in range(ngrid + 1):
        a = lo + (hi - lo) * i / ngrid
        for j in range(ngrid + 1):
            b = lo + (hi - lo) * j / ngrid
            ss, n = residual(req, res, a, b)
            if best is None or ss < best[0]:
                best = (ss, a, b, n)
    ss, a, b, n = best
    step = (hi - lo) / ngrid
    while step > 1e-3:
        improved = False
        for da, db in ((step, 0), (-step, 0), (0, step), (0, -step),
                       (step, step), (-step, -step), (step, -step), (-step, step)):
            s2, _ = residual(req, res, a + da, b + db)
            if s2 < ss:
                ss, a, b = s2, a + da, b + db
                improved = True
        if not improved:
            step /= 2.0
    return a, b, math.sqrt(ss / n)


def fit_shared(req, res, lo=0.0, hi=40.0, n=160):
    """Single shared K (for same-species pair, equal magnitude by symmetry)."""
    best = None
    for i in range(n + 1):
        k = lo + (hi - lo) * i / n
        ss, cnt = residual(req, res, k, k)
        if best is None or ss < best[0]:
            best = (ss, k, cnt)
    ss, k, cnt = best
    step = (hi - lo) / n
    while step > 1e-4:
        improved = False
        for dk in (step, -step):
            s2, _ = residual(req, res, k + dk, k + dk)
            if s2 < ss:
                ss, k, improved = s2, k + dk, True
        if not improved:
            step /= 2.0
    return k, math.sqrt(ss / cnt)


def label(req):
    return "".join(p["species"] for p in req["setup"]["particles"])


def sep(req):
    p = req["setup"]["particles"]
    return math.hypot(p[1]["pos"][0] - p[0]["pos"][0], p[1]["pos"][1] - p[0]["pos"][1])


if __name__ == "__main__":
    print("# dt-convergence check, r2/001 (B-C) at dt 0.005 vs 0.0025")
    req, res = load("2026-11-18", "r2", 1)
    for d in (0.005, 0.0025):
        print(f"  dt={d}: rms at K=(-5.9,-10.7) = {math.sqrt(residual(req, res, -5.9, -10.7, d)[0] / residual(req, res, -5.9, -10.7, d)[1]):.4f}")

    print("\n# Pair fits, free per-particle K (K>0 attraction), P=2.5")
    runs = [
        ("2026-11-18", "r2", 1), ("2026-11-18", "r2", 2),
        ("2026-11-18", "r2", 3), ("2026-11-18", "r2", 4),
        ("2026-11-18", "r2", 5),
        ("2026-11-18", "r1", 1), ("2026-11-18", "r1", 2),
        ("2026-11-18", "r1", 3), ("2026-11-18", "r1", 4),
        ("2026-11-18", "r1", 5),
    ]
    for day, rnd, n in runs:
        req, res = load(day, rnd, n)
        K0, K1, rms = fit_pair(req, res)
        print(f"{rnd}/{n:03d} {label(req)} sep={sep(req):.2f} T={req['setup']['duration']} "
              f"K0={K0:+.2f} K1={K1:+.2f} rms={rms:.4f}")

    print("\n# A-A far field, shared K (P=2.5)")
    for rnd, n in (("r2", 6), ("r2", 7), ("r1", 6), ("r1", 7), ("r1", 8), ("r1", 9)):
        req, res = load("2026-11-18", rnd, n)
        k, rms = fit_shared(req, res)
        print(f"{rnd}/{n:03d} {label(req)} sep={sep(req):.2f} T={req['setup']['duration']} "
              f"K_shared={k:.2f} rms={rms:.4f}")
