"""Early-window acceleration fit for a run started from rest at a known state.

Usage:
  python3 -I early_accel_fit.py <request.json> <result.json> <window_tmax> [<window_tmax> ...]

The initial state (x0, v0 = 0) comes from the request file, not from the result,
because the result's t=0 sample carries tracker noise.

For each particle and coordinate, fits  x(t) - x0 = (1/2) a t^2 + (1/6) j t^3
on samples with 0 < t <= window_tmax. Prints per-particle acceleration, jerk and
residual rms. For a two-particle run, prints the mass ratio from Newton's third law,
m_i a_i = -m_j a_j, along the line joining them (the x-axis for the runs used here).

Pure Python (no numpy). Tracker noise is about 0.05 per coordinate.
"""
import json
import math
import sys


def fit_a_j(ts, ys, x0):
    """Least squares for y = (1/2) a t^2 + (1/6) j t^3, y = x - x0. Returns (a, j, rms)."""
    s22 = s23 = s33 = b2 = b3 = 0.0
    rows = []
    for t, x in zip(ts, ys):
        y = x - x0
        u = 0.5 * t * t
        v = t ** 3 / 6.0
        s22 += u * u
        s23 += u * v
        s33 += v * v
        b2 += u * y
        b3 += v * y
        rows.append((u, v, y))
    det = s22 * s33 - s23 * s23
    a = (b2 * s33 - b3 * s23) / det
    j = (s22 * b3 - s23 * b2) / det
    sq = sum((y - (a * u + j * v)) ** 2 for u, v, y in rows)
    return a, j, math.sqrt(sq / len(rows))


def main():
    req_path, res_path = sys.argv[1], sys.argv[2]
    windows = [float(w) for w in sys.argv[3:]]
    with open(req_path) as f:
        req = json.load(f)
    with open(res_path) as f:
        res = json.load(f)

    req_parts = req["setup"]["particles"]
    species = [p["species"] for p in req_parts]
    x0 = [p["pos"] for p in req_parts]
    samples = res["samples"]
    times = [float(s["t"]) for s in samples]
    n = len(req_parts)
    pos = [[[s["particles"][i]["pos"][0], s["particles"][i]["pos"][1]] for s in samples]
           for i in range(n)]

    print(f"{req['request_id']} ({res.get('status', '?')}): species {species}, "
          f"T={req['setup']['duration']:g}, dt={req['setup']['sample_dt']:g}, samples={len(times)}")
    for w in windows:
        idx = [k for k, t in enumerate(times) if 0.0 < t <= w + 1e-12]
        ts = [times[k] for k in idx]
        print(f"  window t <= {w:g}: n={len(idx)}")
        acc = []
        for i in range(n):
            fits = []
            for c in range(2):
                ys = [pos[i][k][c] for k in idx]
                fits.append(fit_a_j(ts, ys, x0[i][c]))
            acc.append(fits)
            ax, ay = fits[0][0], fits[1][0]
            print(f"    particle {i} ({species[i]}): a=({ax:+.4f}, {ay:+.4f}) "
                  f"|a|={math.hypot(ax, ay):.4f} jerk=({fits[0][1]:+.3f}, {fits[1][1]:+.3f}) "
                  f"rms=({fits[0][2]:.4f}, {fits[1][2]:.4f})")
        if n == 2 and abs(acc[1][0][0]) > 1e-12:
            # m_i a_i = -m_j a_j along x (sep axis) -> m_j / m_i = -a_i,x / a_j,x
            ratio = -acc[0][0][0] / acc[1][0][0]
            print(f"    m_{species[1]}/m_{species[0]} from Newton's third law (x-axis): {ratio:.3f}")


if __name__ == "__main__":
    main()
