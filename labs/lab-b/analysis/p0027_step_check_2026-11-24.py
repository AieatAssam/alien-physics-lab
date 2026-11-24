"""Integrator check for P-0027 at its r0 = 3.0 edge (T = 1.5): does the model's own output stay in the
chamber, and does its trajectory converge as the internal RK4 step H shrinks?
Usage: python3 -I p0027_step_check_2026-11-24.py <paper_dir>
"""
import sys, math, importlib.util, os
sys.path.insert(0, "/tmp/lab-b-pylib")
paper_dir = sys.argv[1]
spec = importlib.util.spec_from_file_location("m", os.path.join(paper_dir, "model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
K0 = m.K_TAB.copy()
c = 5.0
def setup(r0, T):
    return {"particles": [{"species": "A", "pos": [c - r0/2, c], "vel": [0, 0]},
                          {"species": "A", "pos": [c + r0/2, c], "vel": [0, 0]}],
            "duration": T, "sample_dt": 0.01}
def summary(tag, samples):
    xs = [p["pos"][k] for s in samples for p in s["particles"] for k in range(2)]
    ms = min(math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in samples)
    print(f"{tag}: min|x|={min(xs):.3f} max|x|={max(xs):.3f} min_sep={ms:.4f} n={len(samples)}")
    return samples
for H in (0.002, 0.001, 0.0002):
    m.H = H; m.K_TAB = K0.copy()
    base = summary(f"H={H} K x1.000", m.predict(setup(3.0, 1.5)))
    m.K_TAB = K0 * 0.995
    summary(f"H={H} K x0.995", m.predict(setup(3.0, 1.5)))
    m.K_TAB = K0.copy()
