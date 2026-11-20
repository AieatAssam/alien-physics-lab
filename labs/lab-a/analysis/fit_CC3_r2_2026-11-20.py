"""lab-a, 2026-11-20 round 3 analysis: check of the pre-registered C-C flat-K test at separation 3.

Request 2026-11-20/r2/lab-a/001: two C particles at rest, r0 = 3.0, T = 1.0.
Pre-registered rule (analysis/pred_close_CC3_2026-11-20.py): fit one coefficient K with P = 2.5 fixed
to the measured pair separations (sample level, least squares).
  flat supported if |K_fit / 12.36 - 1| <= 0.05
  flat refuted    if |K_fit / 12.36 - 1| >  0.10
  otherwise inconclusive.

Pure python, RK4 for r'' = -2 K / r^P (relative coordinate, both particles attract with K).
Usage: python3 -I fit_CC3_r2_2026-11-20.py <repo_root>
"""
import json
import math
import os
import sys

root = sys.argv[1]
P = 2.5
K_FLAT = 12.36
R0 = 3.0


def sep_series(path):
    r = json.load(open(path))
    out = []
    for s in r["samples"]:
        b = {p["id"]: p["pos"] for p in s["particles"]}
        out.append((s["t"], math.hypot(b[0][0] - b[1][0], b[0][1] - b[1][1])))
    return out


def model(K, P, r0, times, h=2e-4):
    r, v, t = r0, 0.0, 0.0
    out = []
    f = lambda x: -2.0 * K / max(x, 1e-3) ** P
    for T in times:
        while t < T - 1e-12:
            s = min(h, T - t)
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
        out.append(r)
    return out


ser = sep_series(os.path.join(root, "results", "2026-11-20", "r2", "lab-a", "001.json"))
times = [t for t, _ in ser]
meas = [m for _, m in ser]

# 1-D scan of K at P = 2.5, coarse then fine
def rms_for(K):
    m = model(K, P, R0, times, h=5e-4)
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(meas, m)) / len(meas))

best = min(((rms_for(K), K) for K in [8 + 0.1 * i for i in range(81)]))
K_coarse = best[1]
fine = min(((rms_for(K_coarse + 0.01 * j), K_coarse + 0.01 * j) for j in range(-10, 11)))
rms_fit, K_fit = fine[0], fine[1]
rms_fit_full = math.sqrt(sum((a - b) ** 2 for a, b in zip(meas, model(K_fit, P, R0, times))) / len(meas))

rel = K_fit / K_FLAT - 1.0
if abs(rel) <= 0.05:
    verdict = "flat supported"
elif abs(rel) > 0.10:
    verdict = "flat refuted"
else:
    verdict = "inconclusive"

# Residual of the flat prediction, for reference
m_flat = model(K_FLAT, P, R0, times)
rms_flat = math.sqrt(sum((a - b) ** 2 for a, b in zip(meas, m_flat)) / len(meas))
sep_end_meas = meas[-1]
sep_end_flat = m_flat[-1]
# mean residual over the last 20% of samples (sign tells which way it departs)
tail = slice(int(0.8 * len(meas)), None)
bias_tail = sum(a - b for a, b in zip(meas[tail], m_flat[tail])) / len(meas[tail])

print("request 2026-11-20/r2/lab-a/001: C-C, r0 = 3.0, T = %.2f, samples %d" % (times[-1], len(meas)))
print("flat prediction K = %.2f: separation at T = %.4f" % (K_FLAT, sep_end_flat))
print("measured separation at T:     %.4f" % sep_end_meas)
print("rms_sep flat K:               %.4f" % rms_flat)
print("K_fit (P=2.5 fixed):          %.3f  (rms_sep %.4f)" % (K_fit, rms_fit_full))
print("K_fit / 12.36 - 1:            %+.3f" % rel)
print("tail bias (meas - flat, last 20%%): %+.4f" % bias_tail)
print("noise floor (sqrt2 x 0.05):   %.4f" % (math.sqrt(2) * 0.05))
print("VERDICT (pre-registered rule): " + verdict)

out = {
    "request_id": "2026-11-20/r2/lab-a/001",
    "P": P, "K_flat": K_FLAT, "K_fit": round(K_fit, 3), "rel": round(rel, 4),
    "rms_sep_fit": round(rms_fit_full, 5), "rms_sep_flat": round(rms_flat, 5),
    "sep_end_measured": sep_end_meas, "sep_end_flat": sep_end_flat,
    "tail_bias_meas_minus_flat": round(bias_tail, 5),
    "verdict": verdict,
}
with open(os.path.join(root, "out", "labs", "lab-a", "analysis", "fit_CC3_r2_2026-11-20.json"), "w") as fh:
    json.dump(out, fh, indent=1)
