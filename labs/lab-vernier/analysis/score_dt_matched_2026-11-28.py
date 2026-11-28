"""Score the matched sample-timing test (2026-11-28/r1/lab-vernier/001-004, sample_dt 0.001)
against the dt 0.0003 replicates (2026-11-27/r3/lab-vernier/002-006). Same setup: two A at rest,
x 4.5 and 5.5, y 5.0 (r0 1.0), T 0.6.

stdlib only. Usage: python3 -I score_dt_matched_2026-11-28.py <repo_root>
Separation at t = 0.60 is the 0.02-wide bin mean (the pre-registration in NOTEBOOK.md).

Pre-registered (NOTEBOOK.md, round 1):
  prediction: dt 0.001 runs spread over >= 0.2 at t = 0.60, at least one run in each band,
              none below 1.0.
  falsifier:  all four dt 0.001 runs in one cluster (sd < 0.05) that differs from the dt 0.0003 set.
"""
import json, math, sys, statistics

R = sys.argv[1]


def load(rid):
    req = json.load(open(f"{R}/requests/{rid}.json"))
    res = json.load(open(f"{R}/results/{rid}.json"))
    seps = []
    for s in res["samples"]:
        p = {q["id"]: q["pos"] for q in s["particles"]}
        seps.append((s["t"], math.dist(p[0], p[1])))
    return req, res, seps


def binmean(seps, t0, w=0.02):
    v = [d for t, d in seps if abs(t - t0) <= w / 2 + 1e-12]
    return sum(v) / len(v) if v else float("nan")


def band(m):
    if m < 1.0:
        return "BELOW 1.0"
    if 1.10 <= m <= 1.25:
        return "plateau"
    if 1.85 <= m <= 2.15:
        return "rise"
    if 1.25 < m < 1.85:
        return "between"
    return "other"


def block(label, ids, prefix):
    print(f"== {label}")
    vals = []
    for n in ids:
        req, res, seps = load(f"{prefix}/{n}")
        m = binmean(seps, 0.60)
        vals.append(m)
        print(f"  {n} status={res['status']} dt={req['setup']['sample_dt']} T={req['setup']['duration']} "
              f"n_samples={len(res['samples'])} sep(0.60)={m:.3f} band={band(m)}")
    sd = statistics.stdev(vals)
    print(f"  range={max(vals) - min(vals):.3f} mean={statistics.mean(vals):.3f} sd={sd:.3f} "
          f"min={min(vals):.3f} max={max(vals):.3f}")
    return vals


dt1 = block("dt 0.001 (r1/001-004, T 0.6)", ["001", "002", "003", "004"], "2026-11-28/r1/lab-vernier")
dt3 = block("dt 0.0003 (r3/002-006, T 0.6)", ["002", "003", "004", "005", "006"], "2026-11-27/r3/lab-vernier")

print("== pre-registered checks")
bands1 = {band(v) for v in dt1}
spread1 = max(dt1) - min(dt1)
prediction_ok = spread1 >= 0.2 and len(bands1 & {"plateau", "rise", "between"}) >= 2 and min(dt1) >= 1.0
sd1 = statistics.stdev(dt1)
falsifier_hit = sd1 < 0.05 and abs(statistics.mean(dt1) - statistics.mean(dt3)) > 0.05
print(f"  spread(dt 0.001)={spread1:.3f} bands={sorted(bands1)} min={min(dt1):.3f}")
print(f"  prediction (spread>=0.2, two bands, none < 1.0): {'holds' if prediction_ok else 'FAILS'}")
print(f"  falsifier (sd<0.05 and mean differs from dt 0.0003 by >0.05): {'FIRED' if falsifier_hit else 'not fired'}")
