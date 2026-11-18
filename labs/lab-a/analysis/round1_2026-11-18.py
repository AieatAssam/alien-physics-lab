"""lab-a: analysis of round-1 (2026-11-18) results 001-016.
Pure python (numpy not installed). Pair runs are integrated with RK4 from the
requested initial conditions (both at rest unless stated); the tracker residual
sum of squares is minimised over the force constant K (and a screening length
where stated). Usage: python3 -I round1_2026-11-18.py <repo_root>"""
import json, math, sys, os, importlib.util

ROOT = sys.argv[1]
RES = os.path.join(ROOT, "results", "2026-11-18", "r1", "lab-a")
REQ = os.path.join(ROOT, "requests", "2026-11-18", "r1", "lab-a")
REQ_OLD = os.path.join(ROOT, "requests", "2026-11-17", "r3", "lab-a")
RES_OLD = os.path.join(ROOT, "results", "2026-11-17", "r3", "lab-a")


def jload(p):
    with open(p) as f:
        return json.load(f)


def sim(parts0, Kspec, form, times, dt):
    """parts0: list of (x,y) start positions, all at rest. Kspec: per-particle K.
    form ('pow', P) -> K/r^P ; ('scr', lam) -> K*exp(-r/lam)/r^2.
    Returns positions at each requested time (times must be multiples of dt)."""
    n = len(parts0)
    pos = [list(p) for p in parts0]
    vel = [[0.0, 0.0] for _ in range(n)]

    def mag(r):
        if form[0] == "pow":
            return r ** (-form[1])
        return math.exp(-r / form[1]) / (r * r)

    def acc(p):
        a = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dx, dy = p[j][0] - p[i][0], p[j][1] - p[i][1]
                r = math.hypot(dx, dy)
                g = Kspec[i] * mag(r) / r
                a[i][0] += g * dx
                a[i][1] += g * dy
        return a

    def f(p, v):
        return v, acc(p)

    out = []
    t = 0.0
    for tt in times:
        while t < tt - 1e-12:
            h = min(dt, tt - t)
            kp1, kv1 = f(pos, vel)
            P2 = [[pos[i][k] + 0.5 * h * kp1[i][k] for k in range(2)] for i in range(n)]
            V2 = [[vel[i][k] + 0.5 * h * kv1[i][k] for k in range(2)] for i in range(n)]
            kp2, kv2 = f(P2, V2)
            P3 = [[pos[i][k] + 0.5 * h * kp2[i][k] for k in range(2)] for i in range(n)]
            V3 = [[vel[i][k] + 0.5 * h * kv2[i][k] for k in range(2)] for i in range(n)]
            kp3, kv3 = f(P3, V3)
            P4 = [[pos[i][k] + h * kp3[i][k] for k in range(2)] for i in range(n)]
            V4 = [[vel[i][k] + h * kv3[i][k] for k in range(2)] for i in range(n)]
            kp4, kv4 = f(P4, V4)
            pos = [[pos[i][k] + h / 6 * (kp1[i][k] + 2 * kp2[i][k] + 2 * kp3[i][k] + kp4[i][k])
                    for k in range(2)] for i in range(n)]
            vel = [[vel[i][k] + h / 6 * (kv1[i][k] + 2 * kv2[i][k] + 2 * kv3[i][k] + kv4[i][k])
                    for k in range(2)] for i in range(n)]
            t += h
        out.append([list(p) for p in pos])
    return out


def get_run(res_path, req_path):
    res = jload(res_path)
    req = jload(req_path)
    s = res["samples"]
    times = [q["t"] for q in s]
    parts0 = [tuple(p["pos"]) for p in req["setup"]["particles"]]
    species = [p["species"] for p in req["setup"]["particles"]]
    obs = [[tuple(pp["pos"]) for pp in q["particles"]] for q in s]
    return dict(times=times, parts0=parts0, species=species, obs=obs,
                dt=req["setup"]["sample_dt"], T=req["setup"]["duration"],
                events=res.get("events", []), cost=res["cost"], N=len(parts0))


def residual(run, Kspec, form):
    sdt = run["dt"]
    h = sdt / 4.0
    # integrate on fine grid, sample at sample times
    times = [k * sdt for k in range(1, len(run["times"]))]
    fine = sim(run["parts0"], Kspec, form, [k * h for k in range(1, 4 * (len(run["times"]) - 1) + 1)], h)
    pred = [[run["parts0"][i] for i in range(run["N"])]] + [fine[4 * k - 1] for k in range(1, len(run["times"]))]
    sse, cnt = 0.0, 0
    for k in range(len(run["times"])):
        for i in range(run["N"]):
            for c in range(2):
                d = run["obs"][k][i][c] - pred[k][i][c]
                sse += d * d
                cnt += 1
    return sse, cnt


def fit_K(runs, form, grid=(0.5, 60.0), n=70):
    """Single shared K over runs (each particle acceleration = K * g(r))."""
    def tot(K):
        s = 0.0
        c = 0
        for r in runs:
            ss, cc = residual(r, [K] * r["N"], form)
            s += ss
            c += cc
        return s, c
    lo, hi = math.log(grid[0]), math.log(grid[1])
    best = None
    for i in range(n + 1):
        K = math.exp(lo + (hi - lo) * i / n)
        s, c = tot(K)
        if best is None or s < best[0]:
            best = (s, K, c)
    # golden refine around best
    a, b = best[1] / 1.1, best[1] * 1.1
    gr = (math.sqrt(5) - 1) / 2
    x1, x2 = b - gr * (b - a), a + gr * (b - a)
    f1, f2 = tot(x1)[0], tot(x2)[0]
    for _ in range(40):
        if f1 < f2:
            b, x2, f2 = x2, x1, f1
            x1 = b - gr * (b - a)
            f1 = tot(x1)[0]
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + gr * (b - a)
            f2 = tot(x2)[0]
    K = (a + b) / 2
    s, c = tot(K)
    return K, math.sqrt(s / c), c


def fit_K_single(run, form):
    return fit_K([run], form)


def jobs():
    def R(n):
        return get_run(os.path.join(RES, f"{n:03d}.json"), os.path.join(REQ, f"{n:03d}.json"))

    def Rold(n):
        return get_run(os.path.join(RES_OLD, f"{n:03d}.json"), os.path.join(REQ_OLD, f"{n:03d}.json"))
    return R, Rold


if __name__ == "__main__":
    R, Rold = jobs()
    P25 = ("pow", 2.5)
    print("== cost check (1 + 0.02 N T)")
    for n in range(1, 17):
        r = R(n) if n <= 13 else R(n)
        pred = 1 + 0.02 * r["N"] * r["T"]
        print(f"  {n:03d} N={r['N']:2d} T={r['T']:5.1f} cost={r['cost']:.2f} pred={pred:.2f} {'OK' if abs(r['cost']-pred)<1e-6 else 'MISMATCH'}")

    print("== reference A-A at sep 5 (r3 005-006) and sep 4 horizontal (r3 003-004)")
    for n in (3, 4, 5, 6):
        r = Rold(n)
        K, rms, c = fit_K_single(r, P25)
        print(f"  old {n:03d} sep={r['parts0'][1][0]-r['parts0'][0][0]:.1f} K={K:.2f} rms={rms:.4f}")

    print("== species (sep 5, T=2) shared-K fit at P=2.5")
    for n in (1, 2, 3, 4, 5):
        r = R(n)
        K, rms, c = fit_K_single(r, P25)
        print(f"  {n:03d} species={''.join(r['species'])} K={K:.2f} rms={rms:.4f}")

    print("== far field (P=2.5 vs screened lam=8), sep 8-9, T=4")
    for n in (6, 7, 8, 9):
        r = R(n)
        Kp, rp, _ = fit_K_single(r, P25)
        Ks, rs, _ = fit_K_single(r, ("scr", 8.0))
        print(f"  {n:03d} sep={r['parts0'][1][0]-r['parts0'][0][0]:.1f}  pow K={Kp:.2f} rms={rp:.4f} | scr K={Ks:.2f} rms={rs:.4f}")

    print("== isotropy (sep 4, T=2)")
    for n in (10, 11):
        r = R(n)
        K, rms, c = fit_K_single(r, P25)
        print(f"  {n:03d} K={K:.2f} rms={rms:.4f}")

    print("== near field (sep 2, T=0.5)")
    r = R(12)
    K, rms, c = fit_K_single(r, P25)
    print(f"  012 K={K:.2f} rms={rms:.4f}  (K=17.74 predicts per-particle accel {17.74/2**2.5:.3f})")

    print("== P-0003 predictor residuals on round-1 runs (K=17.74, P=2.5 shared)")
    for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
        r = R(n)
        ss, cc = residual(r, [17.74] * r["N"], P25)
        print(f"  {n:03d} rms={math.sqrt(ss/cc):.4f}")
