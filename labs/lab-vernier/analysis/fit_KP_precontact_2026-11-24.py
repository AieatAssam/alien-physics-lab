"""Joint (K, P) fits on the pre-contact window of round-3 runs (2026-11-23 r3/011-022), run 2026-11-24.

Why: the round-3 full-window fits (fit_r3_H24_H25_2026-11-24.py) include the approach to contact
(observed separation falls to 0.07 to 0.5 in several runs). The r^-P law is singular there and the
window K is then an average over a wide r range, so it cannot be labelled by r0.

Here: window = samples up to the last time before the observed separation first drops below R_CUT
(0.5 * r0 floor is not used; R_CUT = 1.0, the observed separation has noise about 0.07).
Model: fit_tools.simulate with constant K and exponent P. A-B runs: K_A(B) = K, K_B(A) = 1.41 K
(the H17 ratio), so one K per A-B run. A-A runs: K_A(A) = K.
Estimate: grid search on (K, P), then local 2D refinement; standard errors from the numerical
Hessian of the SSE with sigma^2 = SSE / (n - 2) (noise estimate from the fit).
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
        d = math.dist(p[0]["pos"], p[1]["pos"])
        if d < R_CUT:
            break
        last = s["t"]
    return last


def sse_KP(setup, res, species_pair, K, P, tmax):
    a, b = species_pair
    coup = {(a, a): 0.0, (b, b): 0.0, (a, b): 0.0, (b, a): 0.0}
    if a == b:
        coup[(a, a)] = K
        coup[(b, b)] = K
    else:
        coup[(a, b)] = K
        coup[(b, a)] = RATIO_BA * K
    sim = ft.simulate(setup, coup, P=P)
    sse, n = 0.0, 0
    for s in res["samples"]:
        t = s["t"]
        if t > tmax + 1e-9:
            continue
        key = round(t, 9)
        if key not in sim:
            continue
        for j, pt in enumerate(s["particles"]):
            px, py = sim[key][pt["id"]]
            sse += (pt["pos"][0] - px) ** 2 + (pt["pos"][1] - py) ** 2
            n += 2
    return sse, n


def fit(setup, res, species_pair, tmax):
    Ks = [x * 0.5 for x in range(10, 40)]          # 5.0 .. 19.5
    Ps = [1.8 + 0.05 * k for k in range(0, 31)]    # 1.8 .. 3.3
    best = None
    for K in Ks:
        for P in Ps:
            s, n = sse_KP(setup, res, species_pair, K, P, tmax)
            if best is None or s < best[0]:
                best = (s, K, P, n)
    # local refinement
    s0, K0, P0, n = best
    dK, dP = 0.25, 0.05
    for _ in range(3):
        cand = []
        for iK in range(-4, 5):
            for iP in range(-4, 5):
                K, P = K0 + iK * dK / 4, P0 + iP * dP / 4
                cand.append((sse_KP(setup, res, species_pair, K, P, tmax)[0], K, P))
        s0, K0, P0 = min(cand)
        dK /= 4
        dP /= 4
    # numerical Hessian of SSE in (K, P)
    hK, hP = 0.02, 0.005
    f = lambda K, P: sse_KP(setup, res, species_pair, K, P, tmax)[0]
    fpp = f(K0 + hK, P0 + hP); fpm = f(K0 + hK, P0 - hP)
    fmp = f(K0 - hK, P0 + hP); fmm = f(K0 - hK, P0 - hP)
    fKK = (f(K0 + hK, P0) - 2 * s0 + f(K0 - hK, P0)) / hK ** 2
    fPP = (f(K0, P0 + hP) - 2 * s0 + f(K0, P0 - hP)) / hP ** 2
    fKP = (fpp - fpm - fmp + fmm) / (4 * hK * hP)
    H = [[fKK, fKP], [fKP, fPP]]
    det = H[0][0] * H[1][1] - H[0][1] * H[1][0]
    inv = [[H[1][1] / det, -H[0][1] / det], [-H[1][0] / det, H[0][0] / det]]
    return s0, K0, P0, inv, n


def main():
    runs = [
        (11, ("A", "B"), 0.0), (12, ("A", "B"), 0.0), (13, ("A", "B"), 0.0), (14, ("A", "B"), 0.0),
        (17, ("A", "B"), 0.0), (18, ("A", "B"), 0.0),
        (15, ("A", "B"), 0.0), (16, ("A", "B"), 0.0),
        (19, ("A", "A"), 0.0), (20, ("A", "A"), 0.0),
        (21, ("A", "A"), 0.0), (22, ("A", "A"), 0.0),
    ]
    for i, pair, _ in runs:
        req, res = load(i)
        setup = req["setup"]
        tmax = precontact_tmax(res)
        if tmax is None or tmax < 0.1:
            print(json.dumps(dict(run=f"r3/{i:03d}", note="no pre-contact window")), flush=True)
            continue
        s0, K0, P0, inv, n = fit(setup, res, pair, tmax)
        sigma2 = s0 / max(n - 2, 1)
        seK = math.sqrt(max(2 * sigma2 * inv[0][0], 0.0))
        seP = math.sqrt(max(2 * sigma2 * inv[1][1], 0.0))
        cKP = 2 * sigma2 * inv[0][1]
        corr = cKP / (seK * seP) if seK > 0 and seP > 0 else float("nan")
        # mean observed separation in the window (label for the fitted K)
        seps = [math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"])
                for s in res["samples"] if s["t"] <= tmax + 1e-9]
        out = dict(run=f"r3/{i:03d}", pair="".join(pair), r0=round(math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"]), 3),
                   tmax=round(tmax, 3), sep_mean=round(sum(seps) / len(seps), 3),
                   sep_min=round(min(seps), 3), K=round(K0, 3), seK=round(seK, 3),
                   P=round(P0, 3), seP=round(seP, 3), corr_KP=round(corr, 3),
                   rmse_L=round(math.sqrt(s0 / n) / ft.L, 5), n=n)
        print(json.dumps(out), flush=True)


if __name__ == "__main__":
    main()
