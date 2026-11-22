"""Round-1 2026-11-22 A-B far-field runs (requests 001-008): free K_A(B), K_B(A) at fixed P.
Reads fit_tools from the lab's checked-in analysis folder (read-only use).
Run from repo root: python3 -I out/labs/lab-vernier/analysis/fit_r1_2026-11-22.py [P]"""
import importlib.util, json, math, os, sys

ROOT = os.getcwd()
spec = importlib.util.spec_from_file_location(
    "fit_tools", os.path.join(ROOT, "out/labs/lab-vernier/analysis/fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)

P = float(sys.argv[1]) if len(sys.argv) > 1 else 2.5
RUNS = [f"2026-11-22/r1/lab-vernier/{i:03d}" for i in range(1, 9)]
keys = [("A", "B"), ("B", "A")]
bounds = {k: (-30.0, 30.0) for k in keys}
coup0 = {("A", "A"): 0.0, ("B", "B"): 0.0, ("A", "B"): 9.0, ("B", "A"): 9.0,
         ("A", "C"): 0.0, ("C", "A"): 0.0, ("B", "C"): 0.0, ("C", "B"): 0.0, ("C", "C"): 0.0}
out = []
for rid in RUNS:
    d, n = rid.rsplit("/", 1)
    req = ft.load_json(os.path.join(ROOT, "requests", d, n + ".json"))
    res = ft.load_json(os.path.join(ROOT, "results", d, n + ".json"))
    setup = req["setup"]
    p = setup["particles"]
    sep0 = math.hypot(p[0]["pos"][0] - p[1]["pos"][0], p[0]["pos"][1] - p[1]["pos"][1])
    tmax = setup["duration"]
    coup, mse = ft.fit_couplings(setup, res, coup0, keys, bounds, P=P, tmax=tmax, sweeps=2)
    null = ft.sse_window(setup, res, {k: 0.0 for k in coup0}, P, tmax) ** 0.5
    # minimum separation along the observed trajectory
    rmin = min(math.hypot(s["particles"][0]["pos"][0] - s["particles"][1]["pos"][0],
                          s["particles"][0]["pos"][1] - s["particles"][1]["pos"][1])
               for s in res["samples"])
    kab, kba = coup[("A", "B")], coup[("B", "A")]
    row = dict(run=rid, sep0=round(sep0, 3), T=tmax, dt=setup["sample_dt"],
               K_AB=round(kab, 3), K_BA=round(kba, 3), ratio=round(kba / kab, 4),
               fit_rmse_L=round(math.sqrt(mse) / ft.L, 5), null_rmse_L=round(null / ft.L, 4),
               rmin_obs=round(rmin, 3), cost=res.get("cost"))
    out.append(row)
    print(json.dumps(row))
