"""Pre-registered predictions for two-particle runs at rest on the power-law pair form
a = K / r^2.5 (P = 2.5, the P-0003 / P-0005 form). Written before any close-range result.

Relative separation: r'' = -2K / r^2.5 (both particles attract with the same K), r(0)=r0, r'(0)=0.
Each particle moves by half the change in separation, along x, pair centred at (5, 5).

Rule (same as earlier pre-registrations): residual rms per coordinate <= 0.07 supports the
power-law extension to this separation; > 0.12 refutes it.

Usage: python3 -I pred_close_2026-11-20.py <repo_root>
Writes <repo_root>/out/labs/lab-a/analysis/pred_2026-11-20_<tag>.json
"""
import json
import sys

root = sys.argv[1]
CASES = [
    # tag, request_id (or 'grant-proposal'), K, r0, T, sample_dt, species
    ("AA_r2", "2026-11-20/r1/lab-a/001", 18.0, 2.0, 0.5, 0.0005, ("A", "A")),
    ("AA_r2_rep", "2026-11-20/r1/lab-a/002", 18.0, 2.0, 0.5, 0.0005, ("A", "A")),
    ("AA_r1p5", "2026-11-20/r1/lab-a/003", 18.0, 1.5, 0.3, 0.0003, ("A", "A")),
    ("BB_r2", "2026-11-20/r1/lab-a/004", 6.12, 2.0, 0.5, 0.0005, ("B", "B")),
    ("CC_r2_grant", "grant-proposal (round 3 main event)", 12.36, 2.0, 0.5, 0.0005, ("C", "C")),
]
CX, CY = 5.0, 5.0


def rel_path(K, r0, T, dt):
    """RK4 for r(t) with r'' = -2K/r^2.5; returns r at t_i = i*dt, i = 0..n."""
    n = int(round(T / dt))
    h = 1e-5
    f = lambda r: -2.0 * K / r ** 2.5
    r, v, t = r0, 0.0, 0.0
    out = [r0]
    for i in range(1, n + 1):
        target = i * dt
        while t < target - 1e-12:
            s = min(h, target - t)
            k1r, k1v = v, f(r)
            r2, v2 = r + s / 2 * k1r, v + s / 2 * k1v
            k2r, k2v = v2, f(r2)
            r3, v3 = r + s / 2 * k2r, v + s / 2 * k2v
            k3r, k3v = v3, f(r3)
            r4, v4 = r + s * k3r, v + s * k3v
            k4r, k4v = v4, f(r4)
            r += s / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
            v += s / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            t += s
        t = target
        out.append(r)
    return out


for tag, rid, K, r0, T, dt, sp in CASES:
    rs = rel_path(K, r0, T, dt)
    pos = []
    for r in rs:
        shift = (r0 - r) / 2
        pos.append([[CX - r0 / 2 + shift, CY], [CX + r0 / 2 - shift, CY]])
    doc = {
        "written_before_results": True,
        "tag": tag,
        "request_id": rid,
        "species": list(sp),
        "K": K,
        "r0": r0,
        "T": T,
        "sample_dt": dt,
        "rule": "supported if residual rms per coordinate <= 0.07; refuted if > 0.12",
        "samples_t": [round(i * dt, 9) for i in range(len(rs))],
        "samples_pos": pos,
    }
    with open(f"{root}/out/labs/lab-a/analysis/pred_2026-11-20_{tag}.json", "w") as fh:
        json.dump(doc, fh)
    print(tag, "r(T)=%.4f" % rs[-1], "samples", len(rs))
