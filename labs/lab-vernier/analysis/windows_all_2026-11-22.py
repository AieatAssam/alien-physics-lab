"""Time-window free K_A(B), K_B(A) at fixed P for all A-B runs of 2026-11-22 rounds 1 and 2.
Each window is labelled by the mean observed separation inside it, not by the starting separation.
Purpose: test whether windows from different runs collapse onto one K(r) curve.
Run from repo root: python3 -I out/labs/lab-vernier/analysis/windows_all_2026-11-22.py [P]"""
import importlib.util, json, math, os, sys
ROOT = os.getcwd()
HERE = os.path.join(ROOT, "out/labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
P = float(sys.argv[1]) if len(sys.argv) > 1 else 2.5
keys = [("A", "B"), ("B", "A")]
bounds = {k: (-30.0, 30.0) for k in keys}
coup0 = {("A", "A"): 0.0, ("B", "B"): 0.0, ("A", "B"): 9.0, ("B", "A"): 9.0,
         ("A", "C"): 0.0, ("C", "A"): 0.0, ("B", "C"): 0.0, ("C", "B"): 0.0, ("C", "C"): 0.0}
RUNS = [f"2026-11-22/r1/lab-vernier/{i:03d}" for i in range(1, 9)] + \
       [f"2026-11-22/r2/lab-vernier/{i:03d}" for i in (1, 2, 3, 4)]
for rid in RUNS:
    d, n = rid.rsplit("/", 1)
    req = ft.load_json(os.path.join(ROOT, "requests", d, n + ".json"))
    res = ft.load_json(os.path.join(ROOT, "results", d, n + ".json"))
    T = req["setup"]["duration"]
    nw = 3 if T >= 5.5 else 2
    edges = [T * k / nw for k in range(nw + 1)]
    for t0, t1 in zip(edges[:-1], edges[1:]):
        seps = [math.hypot(s["particles"][0]["pos"][0]-s["particles"][1]["pos"][0],
                           s["particles"][0]["pos"][1]-s["particles"][1]["pos"][1])
                for s in res["samples"] if t0 - 1e-9 <= s["t"] <= t1 + 1e-9]
        coup, mse = ft.fit_couplings(req["setup"], res, coup0, keys, bounds, P=P, tmax=t1, tmin=t0, sweeps=2)
        print(json.dumps(dict(run=rid[-14:], T=T, window=[round(t0,2), round(t1,2)],
              r_mean=round(sum(seps)/len(seps),3), r_min=round(min(seps),3), r_max=round(max(seps),3),
              K_AB=round(coup[("A","B")],3), K_BA=round(coup[("B","A")],3),
              R=round(coup[("B","A")]/coup[("A","B")],4), fit_rmse_L=round(math.sqrt(mse)/ft.L,5))), flush=True)
