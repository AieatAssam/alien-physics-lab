"""Time-windowed comparison of runs that share the same A-B initial state.

Usage: python3 -I determinism_windows_r1.py <results_root>

Compares each pair of runs on shared sample times, reporting per-coordinate rms
difference in time windows. Tracker noise is about 0.05 per coordinate, so a pair
of independent noisy copies of one trajectory has rms difference about 0.071.
"""
import json
import math
import os
import sys

ROOT = sys.argv[1]

RUNS = {
    "r3/006 (T1 dt.01)": "2026-11-17/r3/lab-b/006.json",
    "r2/003 (T10 dt.05)": "2026-11-17/r2/lab-b/003.json",
    "r1/001 (T1 dt.01)": "2026-11-18/r1/lab-b/001.json",
    "r1/002 (T1 dt.05)": "2026-11-18/r1/lab-b/002.json",
    "r1/003 (T1 dt.02)": "2026-11-18/r1/lab-b/003.json",
}

WINDOWS = [(0.0, 0.25), (0.25, 0.6), (0.6, 1.0)]


def load(rel):
    with open(os.path.join(ROOT, rel)) as f:
        d = json.load(f)
    by_t = {}
    for s in d["samples"]:
        t = round(float(s["t"]), 6)
        by_t[t] = [(p["id"], p["pos"][0], p["pos"][1]) for p in s["particles"]]
    return by_t


def window_rms(a, b, lo, hi):
    """rms of coordinate differences over shared times in (lo, hi]; returns (rms, n)."""
    acc, n = 0.0, 0
    for t, pa in a.items():
        if t in b and lo < t <= hi + 1e-9:
            pb = b[t]
            for (ia, xa, ya), (ib, xb, yb) in zip(pa, pb):
                acc += (xa - xb) ** 2 + (ya - yb) ** 2
                n += 2
    if n == 0:
        return float("nan"), 0
    return math.sqrt(acc / n), n


def main():
    data = {k: load(v) for k, v in RUNS.items()}
    names = list(RUNS)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = data[names[i]], data[names[j]]
            parts = []
            for lo, hi in WINDOWS:
                r, n = window_rms(a, b, lo, hi)
                parts.append(f"({lo:.2f},{hi:.2f}] rms={r:.3f} n={n}")
            print(f"{names[i]:>20s} vs {names[j]:<20s} | " + " | ".join(parts))
    print("noise-only expectation for a pair of noisy copies: 0.071")


if __name__ == "__main__":
    main()
