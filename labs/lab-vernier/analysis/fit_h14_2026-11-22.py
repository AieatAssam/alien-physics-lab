"""H14 far-field A-B fit: free K_A(B) and K_B(A) at P=2.5 for round-3 runs 001-003 and round-1 run 010.
Run with: python3 -I out/labs/lab-vernier/analysis/fit_h14_2026-11-22.py  (from repo root)."""
import importlib.util, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)

ROOT = os.getcwd()
RUNS = [
    ("2026-11-21/r3/lab-vernier/001", "A-B sep 6 horiz"),
    ("2026-11-21/r3/lab-vernier/002", "A-B sep 8 diag"),
    ("2026-11-21/r3/lab-vernier/003", "A-B sep 7 vert"),
    ("2026-11-21/r1/lab-vernier/010", "A-B sep 7 horiz (r1)"),
]
P = 2.5
for rid, label in RUNS:
    req = ft.load_json(os.path.join(ROOT, "requests", rid.rsplit("/", 1)[0], rid.rsplit("/", 1)[1] + ".json"))
    res = ft.load_json(os.path.join(ROOT, "results", rid.rsplit("/", 1)[0], rid.rsplit("/", 1)[1] + ".json"))
    setup = req["setup"]
    p = setup["particles"]
    sep = math.hypot(p[0]["pos"][0] - p[1]["pos"][0], p[0]["pos"][1] - p[1]["pos"][1])
    keys = [("A", "B"), ("B", "A")]
    bounds = {k: (-30.0, 30.0) for k in keys}
    coup0 = {("A", "A"): 0.0, ("B", "B"): 0.0, ("A", "B"): 9.0, ("B", "A"): 9.0,
             ("A", "C"): 0.0, ("C", "A"): 0.0, ("B", "C"): 0.0, ("C", "B"): 0.0, ("C", "C"): 0.0}
    coup, mse = ft.fit_couplings(setup, res, coup0, keys, bounds, P=P, tmax=setup["duration"], sweeps=2)
    null = ft.sse_window(setup, res, {k: 0.0 for k in coup0}, P, setup["duration"]) ** 0.5
    fit_rmse = mse ** 0.5
    print(f"{rid} [{label}] sep={sep:.3f} dt={setup['sample_dt']} T={setup['duration']}")
    print(f"   K_A(B)={coup[('A','B')]:.3f}  K_B(A)={coup[('B','A')]:.3f}  fit RMSE/L={fit_rmse/ft.L:.5f}  null RMSE/L={null/ft.L:.5f}")
