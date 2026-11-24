"""Single-parameter K fits at P = 2.5 on the pre-contact window, round-3 runs 2026-11-23 r3/011-022.

Companion to fit_KP_precontact_2026-11-24.py. The joint (K, P) fit is degenerate on these windows
(corr about 1.0, SE(P) from 0.15 to 3.7), so P is held at 2.5 and K alone is fitted.
Window: samples before the observed separation first drops below R_CUT = 1.0.
K is labelled by the mean observed separation over its window (the r at which it is measured).
A-B: K_A(B) = K, K_B(A) = 1.41 K (H17). A-A: K_A(A) = K.
SE from the curvature of the SSE with sigma^2 = SSE/(n-1).
Run from the repo root: python3 -I <this file>.
"""
import importlib.util
import json
import math
import os

ROOT = os.getcwd()
HERE = os.path.join(ROOT, "labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)

R_CUT = 1.0
P = 2.5
RATIO_BA = 1.41


def load(i):
    rid = f"2026-11-23/r3/lab-vernier/{i:03d}"
    req = ft.load_json(os.path.join(ROOT, "requests", rid + ".json"))
    res = ft.load_json(os.path.join(ROOT, "results", rid + ".json"))
    return req, res


def precontact_tmax(res):
    last = None
    for s in res["samples"]:
        p = s["particles"]
        if math.dist(p[0]["pos"], p[1]["pos"]) < R_CUT:
            break
        last = s["t"]
    return last


def sse(setup, res, pair, K, tmax):
    a, b = pair
    coup = {(a, a): 0.0, (b, b): 0.0, (a, b): 0.0, (b, a): 0.0}
    if a == b:
        coup[(a, a)] = K
        coup[(b, b)] = K
    else:
        coup[(a, b)] = K
        coup[(b, a)] = RATIO_BA * K
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


def fit_K(setup, res, pair, tmax):
    # coarse grid then golden-section refinement on K in [0, 30]
    grid = [0.5 * k for k in range(0, 61)]
    vals = [sse(setup, res, pair, K, tmax)[0] for K in grid]
    k = min(range(len(grid)), key=lambda j: vals[j])
    lo, hi = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = sse(setup, res, pair, c, tmax)[0], sse(setup, res, pair, d, tmax)[0]
    for _ in range(40):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = sse(setup, res, pair, c, tmax)[0]
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = sse(setup, res, pair, d, tmax)[0]
    K0 = (a + b) / 2
    s0, n = sse(setup, res, pair, K0, tmax)
    h = 0.05
    curv = (sse(setup, res, pair, K0 + h, tmax)[0] - 2 * s0 + sse(setup, res, pair, K0 - h, tmax)[0]) / h ** 2
    sigma2 = s0 / max(n - 1, 1)
    se = math.sqrt(2 * sigma2 / curv) if curv > 0 else float("nan")
    return K0, se, s0, n


RUNS = [(11, ("A", "B")), (12, ("A", "B")), (13, ("A", "B")), (14, ("A", "B")),
        (17, ("A", "B")), (18, ("A", "B")), (15, ("A", "B")), (16, ("A", "B")),
        (19, ("A", "A")), (20, ("A", "A")), (21, ("A", "A")), (22, ("A", "A"))]

if __name__ == "__main__":
    for i, pair in RUNS:
        req, res = load(i)
        setup = req["setup"]
        tmax = precontact_tmax(res)
        if tmax is None or tmax < 0.1:
            print(json.dumps(dict(run=f"r3/{i:03d}", note="no pre-contact window")), flush=True)
            continue
        K, se, s0, n = fit_K(setup, res, pair, tmax)
        seps = [math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"])
                for s in res["samples"] if s["t"] <= tmax + 1e-9]
        print(json.dumps(dict(
            run=f"r3/{i:03d}", pair="".join(pair),
            r0=round(math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"]), 2),
            duration=setup["duration"], tmax=round(tmax, 3),
            sep_mean=round(sum(seps) / len(seps), 3), sep_min=round(min(seps), 3),
            K=round(K, 3), seK=round(se, 3), rmse_L=round(math.sqrt(s0 / n) / ft.L, 5), n=n)), flush=True)
