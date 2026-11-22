"""Round-2 2026-11-22 A-B runs (requests 001-004): free K_A(B), K_B(A) at fixed P, full window
and, for the infall runs 001/002, time windows that map to separation bins.
Uses fit_tools.py copied into this folder. Run from repo root:
  python3 -I out/labs/lab-vernier/analysis/fit_r2_2026-11-22.py [P]"""
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

def load(rid):
    d, n = rid.rsplit("/", 1)
    return (ft.load_json(os.path.join(ROOT, "requests", d, n + ".json")),
            ft.load_json(os.path.join(ROOT, "results", d, n + ".json")))

def fit(req, res, tmin=0.0, tmax=None):
    setup = req["setup"]
    tmax = setup["duration"] if tmax is None else tmax
    coup, mse = ft.fit_couplings(setup, res, coup0, keys, bounds, P=P, tmax=tmax, tmin=tmin, sweeps=2)
    null = ft.sse_window(setup, res, {k: 0.0 for k in coup0}, P, tmax, tmin) ** 0.5
    return coup[("A", "B")], coup[("B", "A")], math.sqrt(mse) / ft.L, null / ft.L

def sep(res, t):
    s = min(res["samples"], key=lambda s: abs(s["t"] - t))
    p = s["particles"]
    return math.hypot(p[0]["pos"][0] - p[1]["pos"][0], p[0]["pos"][1] - p[1]["pos"][1])

# Full-window fits for all four runs
for i in range(1, 5):
    rid = f"2026-11-22/r2/lab-vernier/{i:03d}"
    req, res = load(rid)
    kab, kba, rmse, null = fit(req, res)
    rmin = min(math.hypot(s["particles"][0]["pos"][0]-s["particles"][1]["pos"][0],
                          s["particles"][0]["pos"][1]-s["particles"][1]["pos"][1]) for s in res["samples"])
    print(json.dumps(dict(run=rid, T=req["setup"]["duration"], K_AB=round(kab,3), K_BA=round(kba,3),
          R=round(kba/kab,4), fit_rmse_L=round(rmse,5), null_rmse_L=round(null,4), rmin_obs=round(rmin,3))))

# Infall time windows for 001 and 002 (separation mapped from observed mean over window)
WINDOWS = [(0.0, 4.0), (4.0, 6.0), (6.0, 8.0), (8.0, 10.0)]
for i in (1, 2):
    rid = f"2026-11-22/r2/lab-vernier/{i:03d}"
    req, res = load(rid)
    for t0, t1 in WINDOWS:
        kab, kba, rmse, null = fit(req, res, tmin=t0, tmax=t1)
        rs = [sep(res, t) for t in [t0 + k * (t1 - t0) / 8 for k in range(9)]]
        print(json.dumps(dict(run=rid, window=[t0, t1], r_mean=round(sum(rs)/len(rs),3),
              r_span=[round(min(rs),3), round(max(rs),3)], K_AB=round(kab,3), K_BA=round(kba,3),
              R=round(kba/kab,4), fit_rmse_L=round(rmse,5), null_rmse_L=round(null,4))))
