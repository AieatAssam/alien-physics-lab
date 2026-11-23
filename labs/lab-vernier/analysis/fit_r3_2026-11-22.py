"""Round-3 (2026-11-22 r3 001-008) free K_A(B), K_B(A) at P = 2.5 over t in [0, 2], all A-B at rest.
Reports sensitivity: null RMSE/L (all K = 0) vs fit RMSE/L. Run from repo root: python3 -I <this file>"""
import importlib.util, json, math, os
ROOT = os.getcwd()
HERE = os.path.join(ROOT, "out/labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
P = 2.5
keys = [("A", "B"), ("B", "A")]
bounds = {k: (-30.0, 30.0) for k in keys}
coup0 = {("A", "A"): 0.0, ("B", "B"): 0.0, ("A", "B"): 9.0, ("B", "A"): 9.0,
         ("A", "C"): 0.0, ("C", "A"): 0.0, ("B", "C"): 0.0, ("C", "B"): 0.0, ("C", "C"): 0.0}
zero = {k: 0.0 for k in coup0}
for i in range(1, 9):
    rid = f"2026-11-22/r3/lab-vernier/{i:03d}"
    req = ft.load_json(os.path.join(ROOT, "requests", rid + ".json"))
    res = ft.load_json(os.path.join(ROOT, "results", rid + ".json"))
    setup = req["setup"]
    seps = [math.hypot(s["particles"][0]["pos"][0]-s["particles"][1]["pos"][0],
                       s["particles"][0]["pos"][1]-s["particles"][1]["pos"][1])
            for s in res["samples"] if s["t"] <= 2.0 + 1e-9]
    coup, mse = ft.fit_couplings(setup, res, coup0, keys, bounds, P=P, tmax=2.0, tmin=0.0, sweeps=2)
    null = ft.sse_window(setup, res, zero, P, 2.0, 0.0)
    K_AB, K_BA = coup[("A", "B")], coup[("B", "A")]
    print(json.dumps(dict(
        run=f"r3/{i:03d}", r0_designed=round(math.hypot(setup["particles"][1]["pos"][0]-setup["particles"][0]["pos"][0],
                                                       setup["particles"][1]["pos"][1]-setup["particles"][0]["pos"][1]), 3),
        r_obs_mean=round(sum(seps)/len(seps), 3), r_obs_min=round(min(seps), 3), r_obs_max=round(max(seps), 3),
        K_AB=round(K_AB, 3), K_BA=round(K_BA, 3), R=round(K_BA/K_AB, 4),
        fit_rmse_L=round(math.sqrt(mse)/ft.L, 5), null_rmse_L=round(math.sqrt(null)/ft.L, 5))), flush=True)
