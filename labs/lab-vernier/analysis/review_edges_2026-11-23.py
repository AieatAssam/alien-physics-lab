"""Pre-filing checks for round 1 (2026-11-23).
(a) P-0022 (lab-b, A-B sep 2, T <= 0.8, bar = 3 * 0.008 = 0.024): zero-force null and paper-model error, RMSE/L,
    for the candidate review designs, against a 'true' K that differs from the paper's (7.7 / 11.6, the r2/004 values).
(b) P-0021 (own, sep 7, T <= 6): minimum separation of the paper-model trajectory over T = 6 (close-pass check).
Run from repo root: python3 -I <this file>"""
import importlib.util, math, os
ROOT = os.getcwd()
HERE = os.path.join(ROOT, "out/labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
L = ft.L

def setup_for(p0, p1, T, dt, va=(0, 0), vb=(0, 0)):
    return {"particles": [{"species": "A", "pos": list(p0), "vel": list(va)},
                          {"species": "B", "pos": list(p1), "vel": list(vb)}],
            "duration": T, "sample_dt": dt}

def coup(KAB, KBA):
    return {("A", "A"): 0, ("B", "B"): 0, ("A", "B"): KAB, ("B", "A"): KBA,
            ("A", "C"): 0, ("C", "A"): 0, ("B", "C"): 0, ("C", "B"): 0, ("C", "C"): 0}

def rms_vs(pred, truth):
    sq = []
    for t in truth:
        for (a, b) in zip(pred[t], truth[t]):
            sq += [(a[0]-b[0])**2, (a[1]-b[1])**2]
    return math.sqrt(sum(sq) / len(sq)) / L

designs = {
    "vert_2.0": ((5.0, 4.0), (5.0, 6.0)),
    "horiz_2.0": ((4.0, 5.0), (6.0, 5.0)),
    "diag_2.0": ((5 - 0.7071, 5 - 0.7071), (5 + 0.7071, 5 + 0.7071)),
}
for name, (p0, p1) in designs.items():
    s = setup_for(p0, p1, 0.8, 0.005)
    truth = ft.simulate(s, coup(7.7, 11.6), P=2.5, h_max=0.001)
    null = ft.simulate(s, coup(0, 0), P=2.5, h_max=0.001)
    paper = ft.simulate(s, coup(7.59, 10.59), P=2.5, h_max=0.001)
    print(f"P-0022 {name}: null RMSE/L vs truth(7.7/11.6) = {rms_vs(null, truth):.4f}; "
          f"paper-model RMSE/L vs truth = {rms_vs(paper, truth):.4f}; paper bar = 0.024")
    print(f"   null vs paper-model (noise-free) = {rms_vs(null, paper):.4f}; min r (truth) = "
          f"{min(math.hypot(v[0][0]-v[1][0], v[0][1]-v[1][1]) for v in truth.values()):.3f}")

s = setup_for((3.5, 5.0), (10.5 - 3.5 - 3.0 + 0.0, 5.0), 6.0, 0.01)  # placeholder, replaced below
s = setup_for((5 - 3.5, 5.0), (5 + 3.5, 5.0), 6.0, 0.01)
tr = ft.simulate(s, coup(7.75, 10.97), P=2.5, h_max=0.001)
rs = [math.hypot(v[0][0]-v[1][0], v[0][1]-v[1][1]) for v in tr.values()]
print(f"P-0021 check: start 7.0 at rest, T=6, model K 7.75/10.97: min r = {min(rs):.3f}, final r = {rs[-1]:.3f}")
