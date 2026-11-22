"""Free-exponent check for H14: for each far-field A-B run, scan P on a grid, fit K_A(B), K_B(A) at each P,
and report fit RMSE/L. Also print observed separation vs time for run 001 (sep 6) to check close approach.
Run from repo root: python3 -I out/labs/lab-vernier/analysis/pfree_h14_2026-11-22.py"""
import importlib.util, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
ROOT = os.getcwd()
def load(rid):
    d, n = rid.rsplit("/", 1)
    return ft.load_json(os.path.join(ROOT, "requests", d, n + ".json")), ft.load_json(os.path.join(ROOT, "results", d, n + ".json"))

mode = sys.argv[1] if len(sys.argv) > 1 else "scan"
if mode == "traj":
    req, res = load("2026-11-21/r3/lab-vernier/001")
    for s in res["samples"][::25]:
        a, b = s["particles"][0]["pos"], s["particles"][1]["pos"]
        print(f"t={s['t']:.2f} A=({a[0]:.3f},{a[1]:.3f}) B=({b[0]:.3f},{b[1]:.3f}) sep={math.hypot(a[0]-b[0],a[1]-b[1]):.3f}")
    sys.exit()

RUNS = ["2026-11-21/r3/lab-vernier/002", "2026-11-21/r3/lab-vernier/003", "2026-11-21/r1/lab-vernier/010"]
Ps = [round(2.0 + 0.1 * i, 2) for i in range(16)]  # 2.0 .. 3.5
for rid in RUNS:
    req, res = load(rid)
    setup = req["setup"]
    p = setup["particles"]
    sep = math.hypot(p[0]["pos"][0] - p[1]["pos"][0], p[0]["pos"][1] - p[1]["pos"][1])
    coup0 = {k: 0.0 for k in [("A","A"),("B","B"),("A","B"),("B","A"),("A","C"),("C","A"),("B","C"),("C","B"),("C","C")]}
    coup0[("A","B")] = 9.0; coup0[("B","A")] = 9.0
    keys = [("A","B"), ("B","A")]; bounds = {k: (-30.0, 30.0) for k in keys}
    print(f"{rid} sep={sep:.2f}")
    best = None
    for P in Ps:
        coup, mse = ft.fit_couplings(setup, res, coup0, keys, bounds, P=P, tmax=setup["duration"], sweeps=2)
        rm = mse ** 0.5 / ft.L
        print(f"   P={P:.2f} K_A(B)={coup[('A','B')]:7.3f} K_B(A)={coup[('B','A')]:7.3f} RMSE/L={rm:.5f}")
        if best is None or rm < best[0]:
            best = (rm, P, coup[('A','B')], coup[('B','A')])
    print(f"   BEST P={best[1]:.2f} K_A(B)={best[2]:.3f} K_B(A)={best[3]:.3f} RMSE/L={best[0]:.5f}")
