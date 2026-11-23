"""Near-contact sensitivity for P-0022's domain edge (A-B at sep 2, at rest, T <= 0.8).
Minimum separation over the run and final separation vs K_B(A) at fixed K_A(B) = 7.59 (paper value).
Run from repo root: python3 -I <this file>"""
import importlib.util, math, os
ROOT = os.getcwd()
HERE = os.path.join(ROOT, "out/labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
def coup(KAB, KBA):
    return {("A", "A"): 0, ("B", "B"): 0, ("A", "B"): KAB, ("B", "A"): KBA,
            ("A", "C"): 0, ("C", "A"): 0, ("B", "C"): 0, ("C", "B"): 0, ("C", "C"): 0}
s = {"particles": [{"species": "A", "pos": [4.0, 5.0], "vel": [0, 0]},
                   {"species": "B", "pos": [6.0, 5.0], "vel": [0, 0]}], "duration": 0.8, "sample_dt": 0.005}
for KBA in (9.0, 10.59, 11.0, 11.6, 12.0):
    tr = ft.simulate(s, coup(7.59, KBA), P=2.5, h_max=0.001)
    rs = [(t, math.hypot(v[0][0]-v[1][0], v[0][1]-v[1][1])) for t, v in sorted(tr.items())]
    tmin, rmin = min(rs, key=lambda x: x[1])
    print(f"K_A(B)=7.59 K_B(A)={KBA:5.2f}: r(0.8)={rs[-1][1]:.3f}  min r={rmin:.3f} at t={tmin:.3f}")
