"""Two more A-A-A runs (review account, cites P-0007) for the P-0007 c2 replication bar (needs 3 in-domain runs).
Interior sides 4.5 and 4.0 (P-0007 c2 domain is 3.75 to 5.0). Contact margin checked under the pair law first."""
import json, math, os, importlib.util
ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab"
OUT = os.path.join(ROOT, "out")
spec = importlib.util.spec_from_file_location("p0008", os.path.join(ROOT, "papers/P-0008/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def tri(side, cx=5.0, cy=5.0):
    R = side / math.sqrt(3)
    return [("A", cx, cy + R), ("A", cx - side/2, cy - R/2), ("A", cx + side/2, cy - R/2)]
def min_sep(parts, T, dt=0.002):
    sp = [p[0] for p in parts]; pos = [[p[1], p[2]] for p in parts]; vel = [[0.0, 0.0] for _ in parts]
    best = 1e9
    for _ in range(int(round(T/dt))):
        pos, vel = m._step(pos, vel, sp, dt)
        for a in range(3):
            for b in range(a+1, 3):
                best = min(best, math.hypot(pos[b][0]-pos[a][0], pos[b][1]-pos[a][1]))
    return best
reqs = [("011", 4.5, 1.5, "P-0007 c2 replicate, interior side 4.5: three A at rest, equilateral, centroid (5,5), T=1.5, dt 0.03 "
         "(same design as 2026-11-19/r3/lab-c/001, which is at the side-5 endpoint). Judged by P-0007 rule: every particle residual "
         "rms <= 0.07 and zero-force null > 0.09. Model min separation checked for contact (2.82 at T=1.5)."),
        ("012", 4.0, 1.0, "P-0007 c2 replicate, interior side 4.0: three A at rest, equilateral, centroid (5,5), T=1.0, dt 0.03. "
         "Same rule as 011. T=1.0 because the model reaches min separation 1.34 by T=1.5.")]
for num, side, T, purpose in reqs:
    parts = tri(side)
    ms = min_sep(parts, T)
    assert ms > 2.0, (num, ms)
    dists = [math.hypot(parts[b][1]-parts[a][1], parts[b][2]-parts[a][2]) for a in range(3) for b in range(a+1,3)]
    assert all(3.75 < d < 5.0 for d in dists), dists
    print(num, "side", side, "T", T, "model min separation: %.3f" % ms)
    req = {"request_id": f"2026-11-20/r1/lab-c/{num}", "lab": "lab-c", "account": "review", "cites_paper": "P-0007",
           "purpose": purpose + f" Model min separation {ms:.2f}.",
           "setup": {"particles": [{"species": s, "pos": [x, y], "vel": [0.0, 0.0]} for s, x, y in parts],
                     "duration": T, "sample_dt": 0.03},
           "instruments": ["tracker", "census"]}
    d = os.path.join(OUT, "requests", "2026-11-20", "r1", "lab-c"); os.makedirs(d, exist_ok=True)
    json.dump(req, open(os.path.join(d, num + ".json"), "w"), indent=2)
    print("wrote", num)
