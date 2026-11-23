"""Monte Carlo: sd of free K_A(B), K_B(A) fits (T<=2, tracker noise 0.05 per coord) for the H20 setups.
Truth: K_AB = 7.6, K_BA = 11.2 (near the at-rest r3 values). Run from repo root with python3 -I."""
import importlib.util, json, math, os, random, statistics
ROOT = os.getcwd()
spec = importlib.util.spec_from_file_location("ft", os.path.join(ROOT, "out/labs/lab-vernier/analysis/fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
P = 2.5
keys = [("A", "B"), ("B", "A")]
bounds = {k: (-30.0, 30.0) for k in keys}
base = {("A", "A"): 0.0, ("B", "B"): 0.0, ("A", "B"): 8.0, ("B", "A"): 10.0,
        ("A", "C"): 0.0, ("C", "A"): 0.0, ("B", "C"): 0.0, ("C", "B"): 0.0, ("C", "C"): 0.0}
truth = dict(base); truth[("A", "B")] = 7.6; truth[("B", "A")] = 11.2
random.seed(1)
for i in (7, 8, 9):
    rid = f"2026-11-23/r1/lab-vernier/{i:03d}"
    req = ft.load_json(os.path.join(ROOT, "requests", rid + ".json"))
    setup = req["setup"]
    sim = ft.simulate(setup, truth, P)
    ks_ab, ks_ba = [], []
    for rep in range(12):
        res = {"samples": []}
        for t in sorted(sim):
            if t > 2.0 + 1e-9: continue
            res["samples"].append({"t": t, "particles": [{"id": pid, "pos": [x + random.gauss(0, 0.05), y + random.gauss(0, 0.05)]}
                                                      for pid, (x, y) in enumerate(sim[t])]})
        c, _ = ft.fit_couplings(setup, res, base, keys, bounds, P=P, tmax=2.0, sweeps=2)
        ks_ab.append(c[("A", "B")]); ks_ba.append(c[("B", "A")])
    print(json.dumps(dict(run=f"r1/{i:03d}", K_AB_mean=round(statistics.mean(ks_ab), 3), K_AB_sd=round(statistics.stdev(ks_ab), 3),
          K_BA_mean=round(statistics.mean(ks_ba), 3), K_BA_sd=round(statistics.stdev(ks_ba), 3), reps=len(ks_ab))), flush=True)
