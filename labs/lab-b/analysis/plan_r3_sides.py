"""Pre-check of pair-sum predictions for candidate round-3 setups: how far do the sides go?

Usage (repo root): python3 -I out/labs/lab-b/analysis/plan_r3_sides.py
Uses pairsum_check_2026-11-19_r3.simulate (same file directory, imported by path).
"""
import importlib.util
import math
import os

spec = importlib.util.spec_from_file_location(
    "pc", os.path.join(os.getcwd(), "out/labs/lab-b/analysis/pairsum_check_2026-11-19_r3.py"))
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)


def tri(species, side):
    h = side * math.sqrt(3) / 2
    cx, cy = 5.0, 5.0 - h / 3 + 0.0
    # centroid at (5, 5 - h/3 + h/3)? use centre of chamber
    ys = [5.0 + 2 * h / 3, 5.0 - h / 3, 5.0 - h / 3]
    xs = [5.0, 5.0 - side / 2, 5.0 + side / 2]
    return [{"species": s, "pos": [x, y], "vel": [0.0, 0.0]} for s, x, y in zip(species, xs, ys)]


def sides(parts):
    return sorted(math.dist(parts[i]["pos"], parts[j]["pos"]) for i in range(len(parts))
                  for j in range(i + 1, len(parts)))


cands = {
    "ABC_side5": tri(["A", "B", "C"], 5.0),
    "AAA_side5": tri(["A", "A", "A"], 5.0),
    "CCC_side5": tri(["C", "C", "C"], 5.0),
}
for name, parts in cands.items():
    grid = [round(0.5 * k, 7) for k in range(1, 9)]  # 0.5 .. 4.0
    sim = pc.simulate(parts, 4.0, grid)
    print(name)
    for t in grid:
        xs = sim[t]
        s = [math.dist(xs[i], xs[j]) for i in range(3) for j in range(i + 1, 3)]
        print("  t=%.1f sides %.2f %.2f %.2f" % (t, min(s), sorted(s)[1], max(s)))
