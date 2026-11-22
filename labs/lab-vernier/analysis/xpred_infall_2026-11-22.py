"""Out-of-sample check for a constant-K A-B law from initial separation 9 (requests r2/001 horizontal, r2/002 vertical).
Fit K on one run, predict the other run's full trajectory (T = 10). Run from repo root:
  python3 -I out/labs/lab-vernier/analysis/xpred_infall_2026-11-22.py"""
import importlib.util, json, math, os
ROOT = os.getcwd()
HERE = os.path.join(ROOT, "out/labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
keys = [("A", "B"), ("B", "A")]
bounds = {k: (-30.0, 30.0) for k in keys}
coup0 = {("A", "A"): 0.0, ("B", "B"): 0.0, ("A", "B"): 9.0, ("B", "A"): 9.0,
         ("A", "C"): 0.0, ("C", "A"): 0.0, ("B", "C"): 0.0, ("C", "B"): 0.0, ("C", "C"): 0.0}
R = {i: (ft.load_json(f"{ROOT}/requests/2026-11-22/r2/lab-vernier/{i:03d}.json"),
         ft.load_json(f"{ROOT}/results/2026-11-22/r2/lab-vernier/{i:03d}.json")) for i in (1, 2)}
K = {}
for i in (1, 2):
    req, res = R[i]
    c, mse = ft.fit_couplings(req["setup"], res, coup0, keys, bounds, P=2.5, sweeps=2)
    K[i] = {"AB": c[("A","B")], "BA": c[("B","A")]}
    print(json.dumps(dict(run=i, fit_K_AB=round(K[i]["AB"],4), fit_K_BA=round(K[i]["BA"],4), in_sample_rmse_L=round(math.sqrt(mse)/ft.L,5))))
for i, j in ((1, 2), (2, 1)):
    req, res = R[j]
    c = dict(coup0); c[("A","B")] = K[i]["AB"]; c[("B","A")] = K[i]["BA"]
    rm = math.sqrt(ft.sse_window(req["setup"], res, c, 2.5, req["setup"]["duration"])) / ft.L
    print(json.dumps(dict(fit_on=i, predict=j, K_AB=round(K[i]["AB"],4), K_BA=round(K[i]["BA"],4), rmse_L_full_T10=round(rm,5))))
# averaged constants applied to both runs
avgAB = (K[1]["AB"] + K[2]["AB"]) / 2; avgBA = (K[1]["BA"] + K[2]["BA"]) / 2
for j in (1, 2):
    req, res = R[j]
    c = dict(coup0); c[("A","B")] = avgAB; c[("B","A")] = avgBA
    rm = math.sqrt(ft.sse_window(req["setup"], res, c, 2.5, req["setup"]["duration"])) / ft.L
    print(json.dumps(dict(avg_K_AB=round(avgAB,4), avg_K_BA=round(avgBA,4), run=j, rmse_L_full_T10=round(rm,5), ratio=round(avgBA/avgAB,4))))
