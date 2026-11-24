"""K fits at P = 2.5 for lab-vernier's round-2 dense runs (2026-11-24/r2, ids 001-027), plus the
round-3 windows of 2026-11-23 for A-A (r0 = 2.0, 3.0), for comparison with the pre-registered predictions.

Window: samples before the separation first drops below R_CUT = 1.0. Runs that start at r0 = 1.0 have
no such window, so their window is the full run (T as requested; the paper's claim covers that T).
A-B: K_A(B) and K_B(A) fitted separately (two free values, golden-section coordinate descent).
A-A and B-B: one K. K is labelled by the mean observed separation over its window.

Run from the repo root with: python3 -I out/labs/lab-vernier/analysis/fit_round2_K_2026-11-24.py
Writes one JSON line per run to stdout.
"""
import importlib.util
import json
import math
import os

ROOT = os.getcwd()
spec = importlib.util.spec_from_file_location(
    "fit_tools", os.path.join(ROOT, "labs/lab-vernier/analysis/fit_tools.py"))
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)

P = 2.5
R_CUT = 1.0
L = 10.0


def load(rid):
    req = ft.load_json(os.path.join(ROOT, "requests", rid + ".json"))
    res = ft.load_json(os.path.join(ROOT, "results", rid + ".json"))
    return req, res


def window_tmax(res, r0):
    if abs(r0 - 1.0) < 1e-9:
        return res["samples"][-1]["t"]
    last = None
    for s in res["samples"]:
        if math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) < R_CUT:
            break
        last = s["t"]
    return last


def coup_for(pair, KA, KB):
    a, b = pair
    if a == b:
        return {(a, a): KA}
    return {(a, b): KA, (b, a): KB}


def sse_and_n(setup, res, coup, tmax):
    sim = ft.simulate(setup, coup, P=P)
    s2, n = 0.0, 0
    for s in res["samples"]:
        if s["t"] > tmax + 1e-9:
            continue
        key = round(s["t"], 9)
        if key not in sim:
            continue
        for pt in s["particles"]:
            px, py = sim[key][pt["id"]]
            s2 += (pt["pos"][0] - px) ** 2 + (pt["pos"][1] - py) ** 2
            n += 2
    return s2, n


def _golden(fun, lo, hi, iters=30):
    gr = (math.sqrt(5) - 1) / 2
    c1, c2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
    f1, f2 = fun(c1), fun(c2)
    for _ in range(iters):
        if f1 < f2:
            hi, c2, f2 = c2, c1, f1
            c1 = hi - gr * (hi - lo)
            f1 = fun(c1)
        else:
            lo, c1, f1 = c1, c2, f2
            c2 = lo + gr * (hi - lo)
            f2 = fun(c2)
    return (lo + hi) / 2


def _grid_then_golden(fun, grid_lo=0.0, grid_hi=30.0, step=1.0):
    """Global coarse grid, then golden section in the bracket around the best grid point."""
    xs = [grid_lo + k * step for k in range(int(round((grid_hi - grid_lo) / step)) + 1)]
    vals = [fun(x) for x in xs]
    k = min(range(len(xs)), key=lambda j: vals[j])
    lo, hi = xs[max(k - 1, 0)], xs[min(k + 1, len(xs) - 1)]
    return _golden(fun, lo, hi)


def fit(setup, res, pair, tmax):
    """Return dict with K values, their SEs (curvature), rmse/L of the fit, and n.

    Same species: one K by grid + golden search. A-B: K_A(B) and K_B(A) free, by two sweeps of
    grid + golden coordinate search (each sweep starts from the other's current value)."""
    a, b = pair
    same = a == b

    def f(KA, KB):
        s2, _ = sse_and_n(setup, res, coup_for(pair, KA, KB), tmax)
        return s2

    if same:
        KA = _grid_then_golden(lambda v: f(v, v))
        KB = KA
    else:
        KA, KB = 7.0, 10.0
        for _ in range(2):
            KA = _grid_then_golden(lambda v: f(v, KB))
            KB = _grid_then_golden(lambda v: f(KA, v))
    s0, n = sse_and_n(setup, res, coup_for(pair, KA, KB), tmax)
    h = 0.02

    def curv_of(which):
        def ff(dv):
            y = [KA, KB]
            y[which] += dv
            s, _ = sse_and_n(setup, res, coup_for(pair, y[0], y[1]), tmax)
            return s
        return (ff(h) - 2 * s0 + ff(-h)) / h ** 2

    sigma2 = s0 / max(n - 1, 1)
    se_a = math.sqrt(2 * sigma2 / curv_of(0)) if curv_of(0) > 0 else float("nan")
    se_b = float("nan") if same else (math.sqrt(2 * sigma2 / curv_of(1)) if curv_of(1) > 0 else float("nan"))
    return dict(KA=KA, seA=se_a, KB=KB if not same else KA, seB=se_b,
                rmse_L=math.sqrt(s0 / n) / L, n=n)


RUNS = [
    # (request id, pair, label)
    ("2026-11-24/r2/lab-vernier/001", ("B", "B"), "BB r1 H T0.3"),
    ("2026-11-24/r2/lab-vernier/002", ("B", "B"), "BB r1 V T0.3"),
    ("2026-11-24/r2/lab-vernier/027", ("B", "B"), "BB r1 D T0.3"),
    ("2026-11-24/r2/lab-vernier/019", ("A", "A"), "AA r1 H T0.15"),
    ("2026-11-24/r2/lab-vernier/020", ("A", "A"), "AA r1 V T0.15"),
    ("2026-11-24/r2/lab-vernier/005", ("A", "B"), "AB r1.5 H T0.5"),
    ("2026-11-24/r2/lab-vernier/006", ("A", "B"), "AB r1.5 V T0.5"),
    ("2026-11-24/r2/lab-vernier/007", ("A", "B"), "AB r1.5 D T0.5"),
    ("2026-11-24/r2/lab-vernier/008", ("A", "B"), "AB r2.5 H T1"),
    ("2026-11-24/r2/lab-vernier/009", ("A", "B"), "AB r2.5 V T1"),
    ("2026-11-24/r2/lab-vernier/010", ("A", "B"), "AB r2.5 D T1"),
    ("2026-11-24/r2/lab-vernier/011", ("A", "B"), "AB r3 H T1.5"),
    ("2026-11-24/r2/lab-vernier/012", ("A", "B"), "AB r3 V T1.5"),
    ("2026-11-24/r2/lab-vernier/013", ("A", "B"), "AB r4 H T1.5"),
    ("2026-11-24/r2/lab-vernier/014", ("A", "B"), "AB r4 V T1.5"),
    ("2026-11-24/r2/lab-vernier/015", ("A", "B"), "AB r6 H T2"),
    ("2026-11-24/r2/lab-vernier/016", ("A", "B"), "AB r6 V T2"),
    ("2026-11-24/r2/lab-vernier/017", ("A", "B"), "AB r9 H T10"),
    ("2026-11-24/r2/lab-vernier/018", ("A", "B"), "AB r9 V T5"),
    ("2026-11-24/r2/lab-vernier/021", ("A", "A"), "AA r2 H T0.5"),
    ("2026-11-24/r2/lab-vernier/022", ("A", "A"), "AA r2 V T0.5"),
    ("2026-11-24/r2/lab-vernier/023", ("A", "A"), "AA r2.5 H T0.6"),
    ("2026-11-24/r2/lab-vernier/026", ("A", "A"), "AA r2.5 V T0.6"),
    ("2026-11-24/r2/lab-vernier/024", ("A", "A"), "AA r3 H T1.1"),
    ("2026-11-24/r2/lab-vernier/025", ("A", "A"), "AA r3 V T1.1"),
]

if __name__ == "__main__":
    import sys
    want = sys.argv[1:]
    for rid, pair, label in RUNS:
        if want and not any(w in rid for w in want):
            continue
        req, res = load(rid)
        setup = req["setup"]
        r0 = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])
        tmax = window_tmax(res, r0)
        seps = [math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"])
                for s in res["samples"] if tmax is not None and s["t"] <= tmax + 1e-9]
        out = fit(setup, res, pair, tmax)
        print(json.dumps(dict(
            run=rid.split("/", 2)[2], label=label, pair="".join(pair), r0=round(r0, 3),
            T=setup["duration"], tmax=round(tmax, 3), sep_mean=round(sum(seps) / len(seps), 3),
            sep_min=round(min(seps), 3),
            KA=round(out["KA"], 3), seA=round(out["seA"], 3),
            KB=round(out["KB"], 3), seB=round(out["seB"], 3),
            rmse_L=round(out["rmse_L"], 5), n=out["n"])), flush=True)
