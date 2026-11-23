"""Check of the mixed-pair fits: 2-D chi2 grid around the coordinate-descent optimum, to see
whether the two couplings (K_ij, K_ji) are converged and how the ratio K_ji/K_ij is constrained.
Uses pairfit's chi2 (two bodies, RK4 H = 0.002, walls, tracker sd 0.05).
Usage: python3 -I mixed_grid_2026-11-23.py PAIRFIT REPO RID [RID ...]
"""
import importlib.util, json, math, sys
spec = importlib.util.spec_from_file_location("pf", sys.argv[1])
pf = importlib.util.module_from_spec(spec); spec.loader.exec_module(pf)
repo = sys.argv[2]
for rid in sys.argv[3:]:
    res = json.load(open(f"{repo}/results/{rid}.json"))
    setup = json.load(open(f"{repo}/requests/{rid}.json"))["setup"]
    sp = [p["species"] for p in setup["particles"]]
    s0, s1 = sp
    best = pf.fit(setup, res["samples"], sp)
    kf0, kr0 = best["K_" + s0 + s1], best["K_" + s1 + s0]
    count = sum(2 * len(s["particles"]) for s in res["samples"] if round(s["t"], 9) != 0.0)
    f = lambda a, b: pf.chi2(setup, res["samples"], {(s0, s1): a, (s1, s0): b}) * count
    base = f(kf0, kr0)
    # grid of +/- 4 sd-ish in steps; find min over grid, then ratio and 1-sigma (delta chi2 = 1) envelope
    span_f = max(0.3, 0.06 * abs(kf0)); span_r = max(0.3, 0.06 * abs(kr0))
    bestv, bx = None, None
    N = 21
    for i in range(N):
        a = kf0 + span_f * (i - N // 2) / (N // 2)
        for j in range(N):
            b = kr0 + span_r * (j - N // 2) / (N // 2)
            v = f(a, b)
            if bestv is None or v < bestv:
                bestv, bx = v, (a, b)
    ratio_best = bx[1] / bx[0]
    # profile of ratio: scan K_ji/K_ij = q, with K_ij free (min over K_ij at each q)
    pts = []
    for q10 in range(-40, 41):
        q = (kr0 / kf0) * (1 + q10 / 200.0)  # ratio scan +/-20 percent around the fit
        best_chi = None
        for i in range(41):
            a = kf0 * (1 + (i - 20) / 200.0)
            v = f(a, q * a)
            if best_chi is None or v < best_chi[0]:
                best_chi = (v, a)
        pts.append((best_chi[0], q))
    vmin = min(p[0] for p in pts)
    ok = [q for v, q in pts if v - vmin <= 1.0]
    print(json.dumps(dict(run=rid, pair=s0 + s1, sep=round(math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"]), 3),
                          T=setup["duration"], coord_fit=[round(kf0, 3), round(kr0, 3)],
                          coord_ratio=round(kr0 / kf0, 4), grid_best=[round(bx[0], 3), round(bx[1], 3)],
                          grid_ratio=round(ratio_best, 4), grid_dchi2_vs_fit=round(bestv - base, 3),
                          ratio_1sigma=[round(min(ok), 4), round(max(ok), 4)])))
