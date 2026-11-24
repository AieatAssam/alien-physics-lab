"""Power of the judged metric for P-0027 (lab-a K(r) table) on candidate lab-b review designs.
For a setup, compares the table model with K scaled by f in {0.95, 1.05} and with K = 0 (no force),
as RMSE/L against the table model (noise-free). Judge bar for P-0027 is 0.021 (3 x 0.007).
Usage: python3 -I p0027_power_2026-11-24.py <paper_dir>
"""
import sys, math, importlib.util, os
sys.path.insert(0, "/tmp/lab-b-pylib")
paper_dir = sys.argv[1]
spec = importlib.util.spec_from_file_location("m", os.path.join(paper_dir, "model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
K0 = m.K_TAB.copy()
L = 10.0

def traj(setup):
    return {round(s["t"], 9): [q["pos"] for q in s["particles"]] for s in m.predict(setup)}

def rmse_over_L(a, b, T, dt):
    sq = cnt = 0
    for t in sorted(a):
        if not (0 < t <= T + 1e-9):
            continue
        for pa, pb in zip(a[t], b[t]):
            for k in range(2):
                sq += (pa[k] - pb[k]) ** 2; cnt += 1
    return math.sqrt(sq / cnt) / L

designs = [
    ("r0=3.0 horiz T=1.5", 3.0, 1.5),
    ("r0=4.5 horiz T=1.5", 4.5, 1.5),
    ("r0=5.0 horiz T=2.0", 5.0, 2.0),
    ("r0=6.5 horiz T=2.0", 6.5, 2.0),
    ("r0=7.0 horiz T=3.0", 7.0, 3.0),
    ("r0=8.5 horiz T=3.0", 8.5, 3.0),
    ("r0=9.0 vert  T=3.0", 9.0, 3.0),
]
for name, r0, T in designs:
    c = 5.0
    if "vert" in name:
        p = [{"species": "A", "pos": [c, c - r0 / 2], "vel": [0, 0]}, {"species": "A", "pos": [c, c + r0 / 2], "vel": [0, 0]}]
    else:
        p = [{"species": "A", "pos": [c - r0 / 2, c], "vel": [0, 0]}, {"species": "A", "pos": [c + r0 / 2, c], "vel": [0, 0]}]
    setup = {"particles": p, "duration": T, "sample_dt": 0.01}
    base = traj(setup)
    res = []
    for f in (0.95, 1.05):
        m.K_TAB = K0 * f
        res.append(rmse_over_L(traj(setup), base, T, 0.01))
    m.K_TAB = K0 * 0.0
    res.append(rmse_over_L(traj(setup), base, T, 0.01))
    m.K_TAB = K0.copy()
    print(f"{name:22s} K x0.95: {res[0]:.5f}  K x1.05: {res[1]:.5f}  no-force: {res[2]:.5f}")
