"""Round 3 (2026-11-23) checks. Run from repo root: python3 -I <this file>.
1. Verify the P-0022 review (r2/001-004): paper-model RMSE/L on each run (bar 0.024).
2. H20 pooled free fits over t in [0, 2] on the six at-rest, six moving (outward/inward) replicate runs
   plus the round-1 H20 runs (r1/007-009) and r3/004 (at rest, start 6.5, T=2) for reference."""
import importlib.util, json, math, os
ROOT = os.getcwd()
HERE = os.path.join(ROOT, "labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)

def load(day, rnd, i):
    rid = f"{day}/r{rnd}/lab-vernier/{i:03d}"
    return ft.load_json(os.path.join(ROOT, "requests", rid + ".json")), ft.load_json(os.path.join(ROOT, "results", rid + ".json"))

# 1. P-0022 review check
model = ft.load_model(os.path.join(ROOT, "papers/P-0022/model.py"))
for i in range(1, 5):
    req, res = load("2026-11-23", 2, i)
    rows = ft.model_residuals(model, req, res)
    rmse = ft.rms([dx for _, _, dx, _ in rows] + [dy for _, _, _, dy in rows])
    print(json.dumps(dict(run=f"r2/{i:03d}", n=len(rows), rmse_L=round(rmse / ft.L, 5), bar_L=0.024)), flush=True)

# 2. H20 pooled free fits, t in [0, 2]
P = 2.5
keys = [("A", "B"), ("B", "A")]
bounds = {k: (-30.0, 30.0) for k in keys}
coup0 = {k: 0.0 for k in [("A", "A"), ("B", "B"), ("A", "B"), ("B", "A"), ("A", "C"), ("C", "A"), ("B", "C"), ("C", "B"), ("C", "C")]}
coup0[("A", "B")] = 7.5; coup0[("B", "A")] = 11.0
arms = {"rest": [], "moving": []}
runs = [("2026-11-23", 2, i, "rest" if i <= 8 else ("outward" if i <= 12 else "inward")) for i in range(5, 17)]
runs += [("2026-11-23", 1, 7, "outward"), ("2026-11-23", 1, 8, "inward"), ("2026-11-23", 1, 9, "rest")]
runs += [("2026-11-22", 3, 4, "rest")]
for day, rnd, i, arm in runs:
    req, res = load(day, rnd, i)
    coup, mse = ft.fit_couplings(req["setup"], res, coup0, keys, bounds, P=P, tmax=2.0, sweeps=2)
    row = dict(run=f"{day}/r{rnd}/{i:03d}", arm=arm, K_AB=round(coup[("A", "B")], 3), K_BA=round(coup[("B", "A")], 3),
               fit_rmse_L=round(math.sqrt(mse) / ft.L, 5))
    print(json.dumps(row), flush=True)
