"""lab-a, 2026-11-20 round 2: PRE-REGISTRATION (written before the run is filed or results exist).

Two C particles at rest, separation r0 = 3.0, centred at (5,5), T = 1.0, sample_dt 0.002 (500 samples).
Flat-K prediction: a = K/r^2.5 with K = 12.36 (the P-0005 C-C value at separation 5, as used by P-0008).
Rule: fit the single coefficient K (P fixed at 2.5) to the measured separations.
  flat supported if |K_fit / 12.36 - 1| <= 0.05
  flat refuted    if |K_fit / 12.36 - 1| >  0.10
  otherwise inconclusive.
Predicted separation at T for flat K is written to the JSON so the check can compare directly.

Usage: python3 -I pred_close_CC3_2026-11-20.py <repo_root>
"""
import json
import sys

root = sys.argv[1]
K, r0, T, dt = 12.36, 3.0, 1.0, 0.002
P = 2.5


def rel_path(K, r0, T, dt):
    n = int(round(T / dt))
    h = 1e-5
    f = lambda r: -2.0 * K / r ** P
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


rs = rel_path(K, r0, T, dt)
doc = {
    "written_before_results": True,
    "tag": "CC_r3_flatK",
    "request_id": "2026-11-20/r2/lab-a/001",
    "species": ["C", "C"],
    "K": K, "P": P, "r0": r0, "T": T, "sample_dt": dt,
    "rule": "flat supported if |K_fit/12.36-1|<=0.05; refuted if >0.10; else inconclusive",
    "predicted_sep_at_T": rs[-1],
    "sep_t": [round(i * dt, 9) for i in range(len(rs))],
    "sep_pred": rs,
}
with open(root + "/out/labs/lab-a/analysis/pred_2026-11-20_CC_r3_flatK.json", "w") as fh:
    json.dump(doc, fh)
print("predicted separation at T=%.1f: %.4f (samples %d)" % (T, rs[-1], len(rs)))
