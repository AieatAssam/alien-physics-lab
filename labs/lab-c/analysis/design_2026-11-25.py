#!/usr/bin/env python3
"""Design check for 2026-11-25 review and research runs (lab-c).

For each candidate layout: (a) check the paper's own domain rules (predict() must not raise),
(b) report the minimum predicted separation during the run, and (c) judged RMSE/L between the
paper's model and a rival model that differs only where the layout probes (a discrimination check).

Usage: python3 -I design_2026-11-25.py REPO_ROOT
"""
import importlib.util, math, sys
from pathlib import Path

REPO = Path(sys.argv[1])


def load(paper):
    spec = importlib.util.spec_from_file_location(paper.replace("-", "_"), REPO / "papers" / paper / "model.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def setup(parts, dur, dt):
    return {"particles": [{"species": s, "pos": list(p), "vel": [0.0, 0.0]} for s, p in parts],
            "duration": dur, "sample_dt": dt}


def judged(pred_a, pred_b, L=10.0):
    """RMSE/L between two predict() outputs on common sample times."""
    a = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred_a}
    se = n = 0
    for s in pred_b:
        t = round(s["t"], 9)
        if t not in a:
            continue
        for p in s["particles"]:
            for k in range(2):
                se += (p["pos"][k] - a[t][p["id"]][k]) ** 2
                n += 1
    return math.sqrt(se / n) / L


def min_sep(pred):
    m = 1e9
    for s in pred:
        ps = [p["pos"] for p in s["particles"]]
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                m = min(m, math.dist(ps[i], ps[j]))
    return m


def pair_line(r0, cx=5.0, cy=5.0):
    return [("A", (cx - r0 / 2, cy)), ("A", (cx + r0 / 2, cy))]


def report(tag, paper, parts, dur, dt, rival=None):
    m = load(paper)
    s = setup(parts, dur, dt)
    try:
        pred = m.predict(s)
    except ValueError as e:
        print(f"{tag}: {paper} OUT_OF_DOMAIN ({e})")
        return
    line = f"{tag}: {paper} in-domain, min predicted sep={min_sep(pred):.3f}"
    if rival is not None:
        rv = rival(s)
        line += f", judged RMSE/L model vs rival={judged(pred, rv):.5f}"
    print(line)


def grid_ring(spacing, cx=5.0, cy=5.0):
    """3x3 grid minus centre, given spacing."""
    pts = []
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            pts.append(("A", (cx + i * spacing, cy + j * spacing)))
    return pts


def circle(n, chord, cx=5.0, cy=5.0):
    R = chord / (2 * math.sin(math.pi / n))
    return [("A", (cx + R * math.cos(2 * math.pi * k / n), cy + R * math.sin(2 * math.pi * k / n))) for k in range(n)]


def main():
    # P-0027 windows: r0<5 -> T<=1.5; 5<=r0<7 -> T<=2; r0>=7 -> T<=3
    report("P27 r0=3.0 T=1.5", "P-0027", pair_line(3.0), 1.5, 0.003)
    report("P27 r0=3.02 T=1.5", "P-0027", pair_line(3.02), 1.5, 0.003)
    report("P27 r0=5.0 T=2.0", "P-0027", pair_line(5.0), 2.0, 0.005)
    report("P27 r0=9.0 T=3.0", "P-0027", pair_line(9.0), 3.0, 0.005)
    # P-0028 ring at the domain floor (initial pair distance 3.02, just above 3)
    report("P28 grid3.02 T=1", "P-0028", grid_ring(3.02), 1.0, 0.002)
    report("P28 circle8 chord3.02 T=1", "P-0028", circle(8, 3.02), 1.0, 0.002)
    report("P28 grid3.1 T=1 (paper's own)", "P-0028", grid_ring(3.1), 1.0, 0.002)


if __name__ == "__main__":
    main()
