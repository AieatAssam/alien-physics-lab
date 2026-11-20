"""lab-a, 2026-11-20 round 3: PRE-REGISTRATION for A-A at initial separation 1.0 (written before filing).

Two A particles at rest, centred at (5,5), r0 = 1.0, T = 0.15, sample_dt 0.0005 (300 samples). Two replicates.
Power law a = K / r^2.5 with P = 2.5 fixed; the separation is measured at each sample (tracker noise per coord 0.05,
so separation noise about 0.07).

Candidate values of K, both from our own fits at r0 = 1.5-2.0 (analysis/fit_close_KP_2026-11-20.py):
  flat      : K = 18.0 (separation-5 value, P-0003). Constant-K law as published.
  trend     : K in [14.0, 15.6] (fits at r0 = 1.5 and 2.0; the deficit at close range).
Rule (applied to the fitted K from the separation profile, sample level, P = 2.5 fixed):
  flat supported  if |K_fit/18.0 - 1| <= 0.05
  trend supported if K_fit in [13.3, 16.4]   (trend interval widened by 5%)
  otherwise inconclusive; if K_fit < 13.3 the deficit is larger than at r0 = 1.5-2 (report as a finding).
The check also requires no pair collision during the run (min predicted separation > 0.3).

Usage: python3 -I pred_AA_r1p0_2026-11-20.py <repo_root>
"""
import json
import os
import sys

root = sys.argv[1]
P = 2.5
R0 = 1.0
T = 0.15
DT = 0.0005


def rel_path(K, r0, T, dt, h=1e-5):
    n = int(round(T / dt))
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


doc = {"written_before_results": True, "tag": "AA_r1p0", "species": ["A", "A"], "P": P, "r0": R0,
       "T": T, "sample_dt": DT, "candidates": {}}
for name, K in [("flat", 18.0), ("trend_lo", 14.0), ("trend_hi", 15.6)]:
    rs = rel_path(K, R0, T, DT)
    doc["candidates"][name] = {"K": K, "sep_end": rs[-1], "sep_min": min(rs),
                               "sep_t": [round(i * DT, 9) for i in range(len(rs))], "sep_pred": rs}
    print("%-9s K=%5.2f  sep(T)=%.4f  min sep=%.4f" % (name, K, rs[-1], min(rs)))
doc["rule"] = ("flat supported if |K_fit/18-1|<=0.05; trend supported if K_fit in [13.3,16.4]; "
               "else inconclusive. No collision: min sep > 0.3.")
with open(os.path.join(root, "out", "labs", "lab-a", "analysis", "pred_2026-11-20_AA_r1p0.json"), "w") as fh:
    json.dump(doc, fh)
