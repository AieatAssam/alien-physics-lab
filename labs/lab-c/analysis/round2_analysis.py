"""Round 2 analysis for lab-c (stdlib only). Reads results/2026-11-17/r2/lab-c/*.json.

Checks:
  007  single C particle vs unfolded free-flight model over duration 100
  001,005,006  A-A pairs at rest: symmetry of the pair (x0+x1 = 10) and quadratic
               fit to the relative separation over a short window (acceleration)
  002,003,004,008,009  moving pairs with the same ICs as round-1 003 (A-A):
               separation, closest approach, point symmetry, and speed.
"""
import json, math, os, sys

BASE = "/home/runner/work/alien-physics-lab/alien-physics-lab/results/2026-11-17/r2/lab-c/"
L = 10.0


def load(n):
    d = json.load(open(BASE + "%03d.json" % n))
    assert d["status"] == "ok", d
    traj = {}
    species = {}
    for s in d["samples"]:
        for p in s["particles"]:
            traj.setdefault(p["id"], []).append((s["t"], p["pos"][0], p["pos"][1]))
            if "species" in p:
                species[p["id"]] = p["species"]
    return d, traj, species


def unfold(x0, v, t):
    m = (x0 + v * t) % (2 * L)
    return m if m <= L else 2 * L - m


def polyfit(ts, ys, deg):
    """Least squares polynomial fit via normal equations. Returns coeffs c0..cdeg."""
    n = deg + 1
    A = [[0.0] * n for _ in range(n)]
    b = [0.0] * n
    for t, y in zip(ts, ys):
        pw = [t ** k for k in range(n)]
        for i in range(n):
            b[i] += pw[i] * y
            for j in range(n):
                A[i][j] += pw[i] * pw[j]
    # gaussian elimination
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[piv] = M[piv], M[i]
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                for c in range(i, n + 1):
                    M[r][c] -= f * M[i][c]
    return [M[i][n] / M[i][i] for i in range(n)]


def rms(v):
    return math.sqrt(sum(x * x for x in v) / len(v))


def mean(v):
    return sum(v) / len(v)


def report_single_free(n, x0, v0, duration, dt):
    _, traj, sp = load(n)
    rx, ry = [], []
    for t, x, y in traj[0]:
        rx.append(x - unfold(x0[0], v0[0], t))
        ry.append(y - unfold(x0[1], v0[1], t))
    print("== %03d single %s free-flight vs unfolded model, duration %g ==" % (n, sp[0], duration))
    print("  N=%d  x: mean %.4f sd %.4f rmse %.4f   y: mean %.4f sd %.4f rmse %.4f" % (
        len(rx), mean(rx), math.sqrt(sum((r - mean(rx)) ** 2 for r in rx) / len(rx)), rms(rx),
        mean(ry), math.sqrt(sum((r - mean(ry)) ** 2 for r in ry) / len(ry)), rms(ry)))
    seg = len(rx) // 8
    for k in range(8):
        a, b = k * seg, (k + 1) * seg
        print("  seg %d t[%5.1f,%5.1f]  mean resid x %+.4f  y %+.4f  max|res| %.3f" % (
            k, traj[0][a][0], traj[0][b - 1][0], mean(rx[a:b]), mean(ry[a:b]),
            max(max(abs(r) for r in rx[a:b]), max(abs(r) for r in ry[a:b]))))
    worst = max(range(len(rx)), key=lambda i: abs(rx[i]))
    print("  worst |x resid| %.3f at t=%.2f" % (abs(rx[worst]), traj[0][worst][0]))


def pair_at_rest(n):
    _, traj, sp = load(n)
    t = [s[0] for s in traj[0]]
    x0 = [s[1] for s in traj[0]]
    x1 = [s[1] for s in traj[1]]
    y0 = [s[2] for s in traj[0]]
    y1 = [s[2] for s in traj[1]]
    sym = [a + b - 10.0 for a, b in zip(x0, x1)]
    symy = [a + b - 10.0 for a, b in zip(y0, y1)]
    r = [b - a for a, b in zip(x0, x1)]
    print("== %03d A-A at rest (species %s,%s) ==" % (n, sp[0], sp[1]))
    print("  point symmetry x0+x1-10: mean %+.4f sd %.4f ; y0+y1-10: mean %+.4f sd %.4f" % (
        mean(sym), math.sqrt(sum((s - mean(sym)) ** 2 for s in sym) / len(sym)),
        mean(symy), math.sqrt(sum((s - mean(symy)) ** 2 for s in symy) / len(symy))))
    # relative separation r(t) = x1 - x0, fit r = r0 + b t + c t^2 on windows
    for W in (0.5, 1.0, 1.5, 2.0):
        idx = [i for i, tt in enumerate(t) if tt <= W]
        c = polyfit([t[i] for i in idx], [r[i] for i in idx], 2)
        print("  window [0,%.1f]: r0 %.4f  dr/dt %+.4f  d2r/dt2 (=2c) %+.4f  (N=%d)" % (
            W, c[0], c[1], 2 * c[2], len(idx)))
    # y motion check
    ysd = math.sqrt(sum((y - 5.0) ** 2 for y in y0) / len(y0))
    print("  y0 rms deviation from 5.0 over run: %.4f" % ysd)
    # closest approach and summary at selected times
    m = min(range(len(r)), key=lambda i: abs(r[i]))
    print("  first crossing / min |r| at t=%.3f:  sep %.3f" % (t[m], abs(r[m])))
    for tt in (0.5, 1.0, 2.0, 3.0, 5.0, 10.0):
        i = min(range(len(t)), key=lambda k: abs(t[k] - tt))
        print("    t=%5.2f  x0 %.3f  x1 %.3f  sep %.3f" % (t[i], x0[i], x1[i], abs(r[i])))


def smooth_speed(series, t, half=0.2, dt=0.005):
    """Local linear-fit speed at each time using +-half window (index based)."""
    k = int(round(half / dt))
    out = []
    for i in range(len(t)):
        a, b = max(0, i - k), min(len(t), i + k + 1)
        if b - a < 5:
            out.append(float("nan"))
            continue
        c = polyfit(t[a:b], series[a:b], 1)
        out.append(c[1])
    return out


def moving_pair(n, label):
    _, traj, sp = load(n)
    t = [s[0] for s in traj[0]]
    p0 = [(s[1], s[2]) for s in traj[0]]
    p1 = [(s[1], s[2]) for s in traj[1]]
    sep = [math.dist(a, b) for a, b in zip(p0, p1)]
    mi = min(range(len(sep)), key=lambda i: sep[i])
    sym = [math.hypot(a[0] + b[0] - 10, a[1] + b[1] - 10) for a, b in zip(p0, p1)]
    # speeds via local fit
    v0x = smooth_speed([p[0] for p in p0], t)
    v0y = smooth_speed([p[1] for p in p0], t)
    v1x = smooth_speed([p[0] for p in p1], t)
    v1y = smooth_speed([p[1] for p in p1], t)
    sp0 = [math.hypot(a, b) for a, b in zip(v0x, v0y)]
    sp1 = [math.hypot(a, b) for a, b in zip(v1x, v1y)]
    print("== %03d %s (species %s,%s) ==" % (n, label, sp[0], sp[1]))
    print("  min sep %.3f at t=%.3f ; sep at t=0 %.3f ; sep at t=10 %.3f" % (
        sep[mi], t[mi], sep[0], sep[-1]))
    print("  point symmetry |p0+p1-(10,10)|: mean %.4f max %.4f" % (mean(sym), max(sym)))
    for tt in (0.0, 0.5, 1.0, 1.4, 2.0, 3.0, 5.0, 8.0, 10.0):
        i = min(range(len(t)), key=lambda k: abs(t[k] - tt))
        s0 = sp0[i] if not math.isnan(sp0[i]) else float("nan")
        s1 = sp1[i] if not math.isnan(sp1[i]) else float("nan")
        print("    t=%5.2f  p0 (%.3f,%.3f) p1 (%.3f,%.3f) sep %.3f  |v0| %.2f |v1| %.2f" % (
            t[i], p0[i][0], p0[i][1], p1[i][0], p1[i][1], sep[i], s0, s1))
    return {"t": t, "p0": p0, "p1": p1, "sep": sep, "sp0": sp0, "sp1": sp1}


def compare(a, b, name):
    """RMSE of two runs' particle positions over the common time grid (same dt)."""
    d0 = [math.dist(x, y) for x, y in zip(a["p0"], b["p0"])]
    d1 = [math.dist(x, y) for x, y in zip(a["p1"], b["p1"])]
    print("  %-28s per-particle rms position diff: p0 %.4f  p1 %.4f  max p0 %.3f" % (
        name, rms(d0), rms(d1), max(d0)))


if __name__ == "__main__":
    report_single_free(7, (2.0, 5.0), (1.0, 0.0), 100.0, 0.05)
    print()
    for n in (1, 5, 6):
        pair_at_rest(n)
        print()
    runs = {}
    runs[4] = moving_pair(4, "A-A moving replicate of r1/003")
    print()
    runs[2] = moving_pair(2, "A-B moving")
    print()
    runs[3] = moving_pair(3, "B-B moving")
    print()
    runs[8] = moving_pair(8, "A-C moving")
    print()
    runs[9] = moving_pair(9, "C-C moving")
    print()
    print("== trajectory comparisons between moving runs (same ICs) ==")
    compare(runs[4], runs[2], "AA(004) vs AB(002)")
    compare(runs[4], runs[3], "AA(004) vs BB(003)")
    compare(runs[4], runs[8], "AA(004) vs AC(008)")
    compare(runs[4], runs[9], "AA(004) vs CC(009)")
    compare(runs[3], runs[9], "BB(003) vs CC(009)")
    compare(runs[2], runs[8], "AB(002) vs AC(008)")
