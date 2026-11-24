"""Profile the exponent P with one shared coefficient K across runs, round-3 pre-contact windows.

Groups (2026-11-23 r3):
  AB: 011-018 (A-B, r0 1.5, 2.5, 3.0; one K_A(B) per group, K_B(A) = 1.41 K)   -- one shared K
  AA: 019-022 (A-A, r0 2.0 and 3.0; one shared K_AA)                          -- one shared K
For each P on a grid, K is scanned and the total SSE is minimised over K. Sigma^2 is estimated
from the best P=2.5 fit (SSE / (N - 1)). The 1-sigma band is where Delta SSE / sigma^2 < 1.
Windows: samples before the observed separation first drops below R_CUT = 1.0.
This is a shared-parameter fit, so it does not inherit the per-run (K, P) degeneracy.
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

spec2 = importlib.util.spec_from_file_location("kfit", os.path.join(ROOT, "out/labs/lab-vernier/analysis/fit_K_P25_precontact_2026-11-24.py"))
kfit = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(kfit)

RATIO_BA = 1.41


def sse_group(runs, K, P):
    """runs: list of (setup, res, pair, tmax). Returns (SSE, N points)."""
    total, N = 0.0, 0
    for setup, res, pair, tmax in runs:
        a, b = pair
        coup = {(a, a): 0.0, (b, b): 0.0, (a, b): 0.0, (b, a): 0.0}
        if a == b:
            coup[(a, a)] = K
            coup[(b, b)] = K
        else:
            coup[(a, b)] = K
            coup[(b, a)] = RATIO_BA * K
        sim = ft.simulate(setup, coup, P=P)
        for s in res["samples"]:
            if s["t"] > tmax + 1e-9:
                continue
            key = round(s["t"], 9)
            if key not in sim:
                continue
            for pt in s["particles"]:
                px, py = sim[key][pt["id"]]
                total += (pt["pos"][0] - px) ** 2 + (pt["pos"][1] - py) ** 2
                N += 2
    return total, N


def best_K(runs, P, Kgrid):
    vals = [(sse_group(runs, K, P)[0], K) for K in Kgrid]
    s, K = min(vals)
    # refine around best K
    step = Kgrid[1] - Kgrid[0]
    fine = [K + step * (j - 5) / 5 for j in range(0, 11)]
    s, K = min((sse_group(runs, Kf, P)[0], Kf) for Kf in fine)
    return s, K


def load_group(ids):
    out = []
    for i in ids:
        pair = ("A", "B") if i <= 18 else ("A", "A")
        req, res = kfit.load(i)
        tmax = kfit.precontact_tmax(res)
        out.append((req["setup"], res, pair, tmax))
    return out


def profile(name, runs, Pgrid, Kgrid):
    s25, K25 = best_K(runs, 2.5, Kgrid)
    N = sse_group(runs, K25, 2.5)[1]
    sigma2 = s25 / max(N - 1, 1)
    print(json.dumps(dict(group=name, note="P=2.5 shared-K best", K=round(K25, 3), SSE=round(s25, 5),
                          N=N, sigma_L=round(math.sqrt(sigma2) / ft.L, 5))), flush=True)
    rows = []
    for P in Pgrid:
        s, K = best_K(runs, P, Kgrid)
        rows.append((P, K, s))
        print(json.dumps(dict(group=name, P=round(P, 3), K=round(K, 3), dchi2=round((s - s25) / sigma2, 2))), flush=True)
    ok = [P for P, K, s in rows if (s - s25) / sigma2 < 1.0]
    if ok:
        print(json.dumps(dict(group=name, P_1sigma_band=[round(min(ok), 3), round(max(ok), 3)])), flush=True)


if __name__ == "__main__":
    Pgrid = [1.80 + 0.05 * k for k in range(0, 21)]   # 1.80 .. 2.80
    Kgrid = [0.25 * k for k in range(16, 81)]         # 4.0 .. 20.0
    profile("AB", load_group(list(range(11, 19))), Pgrid, Kgrid)
    profile("AA", load_group(list(range(19, 23))), Pgrid, Kgrid)
