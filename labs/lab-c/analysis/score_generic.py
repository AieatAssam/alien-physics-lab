#!/usr/bin/env python3
"""Generic scorer (copy of score_r1_2026-11-20.py), date/round/ids as args.
Score 2026-11-20/r3/lab-c/001-017 with the P-0008 law times a scale s (two-body runs at rest).

Run: python3 -I score_generic.py REPO_ROOT DATE ROUND ID...
Same window rule as scale_fit_short_range.py: each scale's prediction is trusted only until its own
separation first drops below 0.6. Chi2 per separation sample, sigma 0.071. Parabola fit on grid.
Also reports the mean-residual over the first 60% of the run and the s=1 chi2/n.
"""
import importlib.util, json, math, sys
from pathlib import Path

REPO = Path(sys.argv[1])
SIGMA = 0.071
H = 0.0005
spec = importlib.util.spec_from_file_location("p0008", REPO / "papers" / "P-0008" / "model.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
COUP0 = dict(mod.COUP)
GRID = [round(0.50 + 0.01 * i, 2) for i in range(81)]  # 0.50 .. 1.30


def sep(p):
    d = {q["id"]: q["pos"] for q in p}
    return math.dist(d[0], d[1])


def integrate(species, pos0, vel0, times, s):
    """Predicted separation at each time in `times` (sorted ascending)."""
    mod.COUP = {k: s * v for k, v in COUP0.items()}
    pos = [list(p) for p in pos0]; vel = [list(v) for v in vel0]
    t = 0.0; out = []
    for target in times:
        while t < target - 1e-12:
            h = min(H, target - t)
            pos, vel = mod._step(pos, vel, species, h)
            t += h
        t = target
        out.append(math.dist(pos[0], pos[1]))
    return out


def chi_curve(meas, species, pos0, vel0, T, dt):
    times = [t for t, _ in meas]
    chis = []
    for s in GRID:
        pr = integrate(species, pos0, vel0, times, s)
        # trust the prediction only until its own separation first drops below 0.6
        tc = next((t for t, p in zip(times, pr) if p < 0.6), T)
        c = 0.0; n = 0
        for (t, m), p in zip(meas, pr):
            if t > tc + 1e-9: continue
            c += (m - p) ** 2; n += 1
        chis.append((c / SIGMA ** 2 / max(n, 1), n, tc))
    return chis


def parabola_vertex(xs, ys):
    m = len(xs)
    Sx = sum(xs); Sx2 = sum(x*x for x in xs); Sx3 = sum(x**3 for x in xs); Sx4 = sum(x**4 for x in xs)
    Sy = sum(ys); Sxy = sum(x*y for x, y in zip(xs, ys)); Sx2y = sum(x*x*y for x, y in zip(xs, ys))
    M = [[Sx4, Sx3, Sx2], [Sx3, Sx2, Sx], [Sx2, Sx, m]]; v = [Sx2y, Sxy, Sy]
    def det(a):
        return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1]) - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
                + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
    d = det(M); coef = []
    for col in range(3):
        mk = [r[:] for r in M]
        for i in range(3): mk[i][col] = v[i]
        coef.append(det(mk)/d)
    a, b, _ = coef
    return -b/(2*a)


def main():
    date, rnd = sys.argv[2], sys.argv[3]
    ids = sys.argv[4:]
    rows = []
    for rid in ids:
        req = json.loads((REPO / "requests" / date / rnd / "lab-c" / f"{rid}.json").read_text())
        res = json.loads((REPO / "results" / date / rnd / "lab-c" / f"{rid}.json").read_text())
        ps = req["setup"]["particles"]
        species = [p["species"] for p in ps]
        pos0 = [p["pos"] for p in ps]; vel0 = [p["vel"] for p in ps]
        T = req["setup"]["duration"]; dt = req["setup"]["sample_dt"]
        meas = [(s["t"], sep(s["particles"])) for s in res["samples"]]
        if res.get("status", "ok") != "ok":
            rows.append((rid, "".join(species), "status " + str(res.get("status"))))
            continue
        r0 = math.dist(pos0[0], pos0[1])
        chis = chi_curve(meas, species, pos0, vel0, T, dt)
        i0 = min(range(len(GRID)), key=lambda i: chis[i][0])
        lo, hi = max(0, i0-4), min(len(GRID), i0+5)
        sv = parabola_vertex(GRID[lo:hi], [chis[i][0] for i in range(lo, hi)])
        c1 = chis[GRID.index(1.0)]
        rows.append((rid, "".join(species), f"r0={r0:.2f} T={T} dt={dt} n={len(meas)} "
                     f"best_grid={GRID[i0]:.2f} vertex={sv:.3f} chi2/n_best={chis[i0][0]:.2f} "
                     f"chi2/n_s1={c1[0]:.2f} n_win={c1[1]} cut_s1={c1[2]:.3f}"))
    for r in rows:
        print(" ".join(str(x) for x in r))


if __name__ == "__main__":
    main()
