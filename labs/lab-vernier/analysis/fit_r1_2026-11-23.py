"""Round-1 2026-11-23 (r1 001-009) analysis. Run from repo root: python3 -I <this file>.
001-005: P-0022 edge (sep ~2, T 0.8): free fit K_A(B), K_B(A); also K_B(A) with K_A(B)=7.59 fixed.
006: P-0021 check (sep 7, T 6): residual RMSE/L of P-0021 model.py vs tracker.
007-009: H20 state/orientation (sep 6.5, T 2): free fits over t in [0,2]."""
import json, math, os
ROOT = os.getcwd()
ft = __import__("importlib.util").util
import importlib.util
HERE = os.path.join(ROOT, "out/labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
P = 2.5
keys = [("A", "B"), ("B", "A")]
bounds = {k: (-30.0, 30.0) for k in keys}
coup0 = {("A", "A"): 0.0, ("B", "B"): 0.0, ("A", "B"): 9.0, ("B", "A"): 9.0,
         ("A", "C"): 0.0, ("C", "A"): 0.0, ("B", "C"): 0.0, ("C", "B"): 0.0, ("C", "C"): 0.0}
zero = {k: 0.0 for k in coup0}

def load(i):
    rid = f"2026-11-23/r1/lab-vernier/{i:03d}"
    return ft.load_json(os.path.join(ROOT, "requests", rid + ".json")), ft.load_json(os.path.join(ROOT, "results", rid + ".json"))

def seps(res, tmax):
    out = []
    for s in res["samples"]:
        if s["t"] <= tmax + 1e-9:
            a, b = s["particles"][0]["pos"], s["particles"][1]["pos"]
            out.append(math.hypot(a[0]-b[0], a[1]-b[1]))
    return out

# 001-005 P-0022 edge, T <= 0.8
for i in range(1, 6):
    req, res = load(i)
    coup, mse = ft.fit_couplings(req["setup"], res, coup0, keys, bounds, P=P, tmax=0.8, sweeps=2)
    fixed = dict(coup0); fixed[("A", "B")] = 7.59
    c2, mse2 = ft.fit_couplings(req["setup"], res, fixed, [("B", "A")], bounds, P=P, tmax=0.8, sweeps=2)
    null = ft.sse_window(req["setup"], res, zero, P, 0.8)
    s = seps(res, 0.8)
    print(json.dumps(dict(run=f"r1/{i:03d}", sep_start=round(s[0], 3), sep_end=round(s[-1], 3),
        K_AB_free=round(coup[("A", "B")], 3), K_BA_free=round(coup[("B", "A")], 3),
        K_BA_given_KAB7p59=round(c2[("B", "A")], 3),
        fit_rmse_L=round(math.sqrt(mse)/ft.L, 5), null_rmse_L=round(math.sqrt(null)/ft.L, 5))), flush=True)

# 006 P-0021 model residual over T = 6
req, res = load(6)
model = ft.load_model(os.path.join(ROOT, "papers/P-0021/model.py"))
rows = ft.model_residuals(model, req, res)
rmse = ft.rms([dx for _, _, dx, _ in rows] + [dy for _, _, _, dy in rows])
# 007-009 free fit over t in [0, 2]
for i in (7, 8, 9):
    req, res = load(i)
    coup, mse = ft.fit_couplings(req["setup"], res, coup0, keys, bounds, P=P, tmax=2.0, sweeps=2)
    null = ft.sse_window(req["setup"], res, zero, P, 2.0)
    s = seps(res, 2.0)
    print(json.dumps(dict(run=f"r1/{i:03d}", sep_start=round(s[0], 3), sep_mean=round(sum(s)/len(s), 3),
        sep_min=round(min(s), 3), sep_end=round(s[-1], 3),
        K_AB=round(coup[("A", "B")], 3), K_BA=round(coup[("B", "A")], 3),
        fit_rmse_L=round(math.sqrt(mse)/ft.L, 5), null_rmse_L=round(math.sqrt(null)/ft.L, 5))), flush=True)
