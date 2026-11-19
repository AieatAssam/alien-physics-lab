"""Pooled tracker-noise statistics for lone particles at rest (lab-vernier round 1-2 runs)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fit_tools import load_json
R = "/home/runner/work/alien-physics-lab/alien-physics-lab"
RUNS = {  # request id -> (species, rest position)
    "2026-11-19/r1/lab-vernier/001": ("A", (5.0, 5.0)),
    "2026-11-19/r1/lab-vernier/002": ("A", (0.3, 9.7)),
    "2026-11-19/r1/lab-vernier/003": ("C", (5.0, 5.0)),
    "2026-11-19/r1/lab-vernier/004": ("B", (5.0, 5.0)),
    "2026-11-19/r1/lab-vernier/006": ("A", (5.0, 5.0)),
    "2026-11-19/r2/lab-vernier/002": ("A", (5.0, 5.0)),
}
def stats(xs):
    n = len(xs); m = sum(xs) / n
    v = sum((x - m) ** 2 for x in xs) / (n - 1)
    s2 = sum((x - m) ** 2 for x in xs) / n
    k = (sum((x - m) ** 4 for x in xs) / n) / (s2 * s2)
    return m, math.sqrt(v), k
def lag1(xs):
    m = sum(xs) / len(xs)
    num = sum((xs[i] - m) * (xs[i + 1] - m) for i in range(len(xs) - 1))
    den = sum((x - m) ** 2 for x in xs)
    return num / den
allx, ally = [], []
by_species = {}
for rid, (sp, (x0, y0)) in RUNS.items():
    path = os.path.join(R, "results", rid.replace("2026-11-19/", "2026-11-19/") + ".json")
    res = load_json(path)
    dx = [s["particles"][0]["pos"][0] - x0 for s in res["samples"]]
    dy = [s["particles"][0]["pos"][1] - y0 for s in res["samples"]]
    mx, sx, kx = stats(dx); my, sy, ky = stats(dy)
    print(f"{rid} {sp} T={res['samples'][-1]['t']} n={len(dx)}: mean x {mx:+.4f} y {my:+.4f}; sd x {sx:.4f} y {sy:.4f}; kurt x {kx:.2f} y {ky:.2f}; lag1 x {lag1(dx):+.3f} y {lag1(dy):+.3f}")
    allx += dx; ally += dy
    by_species.setdefault(sp, []).extend(dx + dy)
mx, sx, kx = stats(allx); my, sy, ky = stats(ally)
print(f"POOLED all {len(allx)} per coord: mean x {mx:+.4f} y {my:+.4f}; sd x {sx:.4f} y {sy:.4f}; kurt x {kx:.2f} y {ky:.2f}")
for sp, v in sorted(by_species.items()):
    m, s, k = stats(v)
    print(f"  species {sp}: n {len(v)} sd {s:.4f} mean {m:+.4f} kurt {k:.2f}")
