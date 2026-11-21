"""lab-b, round 1 of 2026-11-21: fit pair coefficients for the far-range runs of 2026-11-20/r3.

Stdlib only. Run as:  python3 -I fit_far_2026-11-21.py <repo_root>

Model (same convention as the lab's earlier tools): acceleration on particle i from j is
    K_i(j) * (x_j - x_i) / r^3.5,   so the magnitude is K / r^2.5 (P = 2.5).
Positive K = attraction. Particles start at rest; no walls are reached in these windows
(checked below). Noise: tracker sd 0.05 per coordinate, so chi2 = SSQ / 0.05^2.

For each run we (a) evaluate chi2 at the pre-registered hypotheses and (b) fit K by
golden-section search (1-D for equal-species pairs, coordinate descent for two-species pairs).
"""
import json
import math
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
SIGMA = 0.05
GR = (math.sqrt(5) - 1) / 2


def load(p):
    return json.load(open(os.path.join(ROOT, p)))


def simulate(parts, K, nsteps, h):
    """RK4 with fixed step h. K[(i, j)] = K_i(j). Returns positions at steps 0..nsteps."""
    n = len(parts)
    x = [list(p["pos"]) for p in parts]
    v = [list(p["vel"]) for p in parts]

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

    out = [[list(p) for p in x]]
    for _ in range(nsteps):
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
        out.append([list(p) for p in x])
    return out


def chi2(req, res, Kfun, h):
    """chi2 over all samples t > 0 and all particles; Kfun() -> dict K[(i,j)]."""
    parts = req["setup"]["particles"]
    nsteps = int(round(req["setup"]["duration"] / h))
    sim = simulate(parts, Kfun(), nsteps, h)
    ssq = 0.0
    cnt = 0
    for s in res["samples"]:
        t = float(s["t"])
        if t <= 0:
            continue
        idx = int(round(t / h))
        if idx >= len(sim):
            continue
        for i, obs in enumerate(s["particles"]):
            for k in range(2):
                d = obs["pos"][k] - sim[idx][i][k]
                ssq += d * d
                cnt += 1
    return ssq / SIGMA ** 2, cnt


def golden(f, lo, hi, iters=60):
    a, b = lo, hi
    c = b - GR * (b - a)
    d = a + GR * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(iters):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - GR * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + GR * (b - a)
            fd = f(d)
    x = (a + b) / 2
    return x, f(x)


def pair_K(req, res, h, Kdict):
    """chi2 for an explicit assignment keyed by ordered pairs."""
    return chi2(req, res, lambda: Kdict, h)[0]


def fit_groups(req, res, h, groups, bounds, rounds=4):
    """groups: list of lists of ordered pairs; each group is one free K shared by its pairs."""
    def build(vals):
        K = {}
        for g, v in zip(groups, vals):
            for pair in g:
                K[pair] = v
        return K

    def objective(vals):
        return chi2(req, res, lambda: build(vals), h)[0]

    cur = [(lo + hi) / 2 for (lo, hi) in bounds]
    for _ in range(rounds):
        for gi in range(len(groups)):
            def f1(x, gi=gi):
                vv = list(cur)
                vv[gi] = x
                return objective(vv)
            cur[gi], _ = golden(f1, bounds[gi][0], bounds[gi][1])
    return cur, objective(cur)


def run_fit(label, pid, h, groups, bounds, hyps, names):
    """hyps: list of (name, values per group). names: labels for the groups."""
    req = load("requests/%s.json" % pid)
    res = load("results/%s.json" % pid)
    parts = req["setup"]["particles"]
    sp = [p["species"] for p in parts]
    print("== %s  %s  species=%s  N=%d  T=%.2f  dt=%.4f" % (
        label, pid, "".join(sp), len(parts), req["setup"]["duration"], h))
    lo = min(c for s in res["samples"] for p in s["particles"] for c in p["pos"])
    hi = max(c for s in res["samples"] for p in s["particles"] for c in p["pos"])
    print("   measured coordinate range [%.3f, %.3f] (chamber [0, 10])" % (lo, hi))
    out = {"request_id": pid, "label": label, "names": names}
    ndata = len(res["samples"]) * len(parts) * 2
    for name, vals in hyps:
        c2 = pair_K(req, res, h, {p: v for g, v in zip(groups, vals) for p in g})
        print("   hyp %-20s %s chi2=%9.1f  (chi2/ndata=%.4f)" % (
            name, ", ".join("%s=%.2f" % (n, v) for n, v in zip(names, vals)), c2, c2 / ndata))
        out.setdefault("hyps", {})[name] = {"values": vals, "chi2": c2}
    best, c2 = fit_groups(req, res, h, groups, bounds)
    print("   best fit " + ", ".join("%s=%.3f" % (n, v) for n, v in zip(names, best)) +
          "  chi2=%.1f  (chi2/ndata=%.4f)" % (c2, c2 / ndata))
    out["best"] = {"values": best, "chi2": c2}
    return out


if __name__ == "__main__":
    results = []
    AA = [(0, 1), (1, 0)]  # equal-species pair: one shared K
    results.append(run_fit("A-A far (sep 12)", "2026-11-20/r3/lab-b/007", 0.003,
                           [AA], [(0.0, 30.0)],
                           [("linear G (P-0010)", [7.3]), ("power-law cont.", [9.1])],
                           ["K_AA"]))
    results.append(run_fit("C-C far (sep 12)", "2026-11-20/r3/lab-b/010", 0.003,
                           [[(0, 1), (1, 0)]], [(0.0, 30.0)],
                           [("linear G (P-0010)", [4.75]), ("power-law cont.", [6.1])],
                           ["K_CC"]))
    print()
    results.append(run_fit("A-C far (sep 12)", "2026-11-20/r3/lab-b/009", 0.003,
                           [[(0, 1)], [(1, 0)]], [(-30.0, 0.0), (-30.0, 0.0)],
                           [("linear G (P-0010)", [-3.37, -8.17]), ("power-law cont.", [-4.4, -11.2])],
                           ["K_A(C)", "K_C(A)"]))
    print()
    results.append(run_fit("B-C H13 (sep 9)", "2026-11-20/r3/lab-b/008", 0.002,
                           [[(0, 1)], [(1, 0)]], [(-30.0, 0.0), (-30.0, 0.0)],
                           [("with C-factor", [-3.94, -6.85]), ("without C-factor", [-4.16, -7.22])],
                           ["K_B(C)", "K_C(B)"]))
    json.dump(results, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "fit_far_2026-11-21.json"), "w"), indent=1)
