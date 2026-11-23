"""Constant-K claim check for at-rest A-B, initial separation 5.4 to 6.1, T <= 2 (round-3 runs 001, 002, 003, 006, 007).
(a) residual RMSE/L of a constant-K predictor (K_A(B) = 8.33, K_B(A) = 11.66 = 1.40 * 8.33) against each run's tracker data.
(b) discrimination: RMSE/L between that predictor and alternative constants at the same start (wrong-K detectability).
Run from repo root: python3 -I <this file>"""
import importlib.util, json, math, os
ROOT = os.getcwd()
HERE = os.path.join(ROOT, "out/labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
def coup(KAB, KBA):
    return {("A", "A"): 0, ("B", "B"): 0, ("A", "B"): KAB, ("B", "A"): KBA,
            ("A", "C"): 0, ("C", "A"): 0, ("B", "C"): 0, ("C", "B"): 0, ("C", "C"): 0}
KAB, KBA = 8.33, 1.40 * 8.33
errs = []
for i in (1, 2, 3, 6, 7):
    rid = f"2026-11-22/r3/lab-vernier/{i:03d}"
    req = ft.load_json(os.path.join(ROOT, "requests", rid + ".json"))
    res = ft.load_json(os.path.join(ROOT, "results", rid + ".json"))
    pred = ft.simulate(req["setup"], coup(KAB, KBA), P=2.5, h_max=0.001)
    obs = ft.observed_by_t(res)
    sq = []
    for t, o in obs.items():
        if round(t, 9) not in pred:
            continue
        for pid, (x, y) in o.items():
            px, py = pred[round(t, 9)][pid]
            sq += [(x - px) ** 2, (y - py) ** 2]
    e = math.sqrt(sum(sq) / len(sq)) / ft.L
    errs.append(e)
    print(f"run r3/{i:03d} start {req['setup']['particles'][1]['pos'][0]-req['setup']['particles'][0]['pos'][0]:.2f}"
          f" residual RMSE/L = {e:.5f}")
print("max residual RMSE/L over the 5 runs:", round(max(errs), 5), " mean:", round(sum(errs)/len(errs), 5))

setup = {"particles": [{"species": "A", "pos": [2.925, 5.0], "vel": [0, 0]},
                       {"species": "B", "pos": [8.075, 5.0], "vel": [0, 0]}], "duration": 2.0, "sample_dt": 0.005}
ref = ft.simulate(setup, coup(KAB, KBA), P=2.5, h_max=0.001)
for kab in (8.33 * 0.9, 8.33 * 0.8, 6.3 / 1.0):
    alt = ft.simulate(setup, coup(kab, 1.40 * kab), P=2.5, h_max=0.001)
    sq = []
    for t in ref:
        for (a, b), (c, d) in zip(ref[t], alt[t]):
            sq += [(a - c) ** 2, (b - d) ** 2]
    print(f"wrong-K detectability: K_A(B) = {kab:.2f} vs 8.33 at start 5.85 T=2: RMSE/L = {math.sqrt(sum(sq)/len(sq))/ft.L:.5f}"
          f" (claim bar at predicted_error 0.0055 is 0.0165)")
