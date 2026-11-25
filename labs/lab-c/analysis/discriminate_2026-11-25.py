#!/usr/bin/env python3
"""Judged RMSE/L between each paper's own model and a rival that continues the power law
K = 47 r^-0.6 (per-particle accel 47/r^3.1, the refuted round-2 M1 form) at all separations.
Usage: python3 -I discriminate_2026-11-25.py REPO_ROOT
"""
import importlib.util, math, sys
from pathlib import Path

REPO = Path(sys.argv[1])
HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("design", HERE / "design_2026-11-25.py")
D = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0], str(REPO)]
spec.loader.exec_module(D)


def rival_predict(paper, parts, dur, dt):
    m = D.load(paper)
    if paper == "P-0027":
        m._k = lambda r: 47.0 * r ** (-0.6)
    elif paper == "P-0028":
        m.K = lambda r: 47.0 * r ** (-0.6)
    return m.predict(D.setup(parts, dur, dt))


def main():
    cases = [
        ("P-0027 r0=3.0 T=1.5", "P-0027", D.pair_line(3.0), 1.5, 0.003),
        ("P-0027 r0=3.02 T=1.5", "P-0027", D.pair_line(3.02), 1.5, 0.003),
        ("P-0027 r0=5.0 T=2.0", "P-0027", D.pair_line(5.0), 2.0, 0.005),
        ("P-0027 r0=9.0 T=3.0", "P-0027", D.pair_line(9.0), 3.0, 0.005),
        ("P-0028 grid3.02 T=1", "P-0028", D.grid_ring(3.02), 1.0, 0.002),
        ("P-0028 circle8 chord3.02 T=1", "P-0028", D.circle(8, 3.02), 1.0, 0.002),
    ]
    for tag, paper, parts, dur, dt in cases:
        m = D.load(paper)
        own = m.predict(D.setup(parts, dur, dt))
        riv = rival_predict(paper, parts, dur, dt)
        print(f"{tag}: min sep own={D.min_sep(own):.3f} rival={D.min_sep(riv):.3f} "
              f"judged RMSE/L(own vs rival)={D.judged(own, riv):.5f}  (bar 3x predicted=0.021)")


if __name__ == "__main__":
    main()
