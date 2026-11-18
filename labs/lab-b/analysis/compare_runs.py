"""Windowed rms comparison of tracker trajectories on shared sample times.

Usage: python3 -I compare_runs.py <results_root> <label>=<rel/path.json> [...]

Pairwise rms coordinate difference over time windows. Noise-only expectation for
two independent noisy copies of one trajectory (sd 0.05 per coordinate) is 0.071.
Pure Python.
"""
import json
import math
import os
import sys

WINDOWS = [(0.0, 0.25), (0.25, 0.6), (0.6, 1.0), (1.0, 2.0)]


def load(path):
    with open(path) as f:
        d = json.load(f)
    by_t = {}
    for s in d["samples"]:
        t = round(float(s["t"]), 6)
        by_t[t] = [(p["pos"][0], p["pos"][1]) for p in s["particles"]]
    return by_t


def window_rms(a, b, lo, hi):
    acc, n = 0.0, 0
    for t, pa in a.items():
        if t in b and lo < t <= hi + 1e-9:
            for (xa, ya), (xb, yb) in zip(pa, b[t]):
                acc += (xa - xb) ** 2 + (ya - yb) ** 2
                n += 2
    return (math.sqrt(acc / n) if n else float("nan")), n


def main():
    root = sys.argv[1]
    runs = []
    for arg in sys.argv[2:]:
        label, rel = arg.split("=", 1)
        runs.append((label, load(os.path.join(root, rel))))
    for i in range(len(runs)):
        for j in range(i + 1, len(runs)):
            (na, a), (nb, b) = runs[i], runs[j]
            cells = []
            for lo, hi in WINDOWS:
                r, n = window_rms(a, b, lo, hi)
                cells.append(f"({lo:.2f},{hi:.2f}] {r:.3f} (n={n})")
            print(f"{na:>14s} vs {nb:<14s} | " + " | ".join(cells))


if __name__ == "__main__":
    main()
