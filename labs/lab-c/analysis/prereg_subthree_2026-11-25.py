#!/usr/bin/env python3
"""Pre-registered predictions for the sub-3 A-A round (lab-c, 2026-11-25 round 2).
For each planned design: predicted min separation and predicted judged RMSE/L of TAB and P26 against
the run's (unknown) observations is not computable; we store each law's full predicted trajectory
(sampled at the run's sample_dt) and the min separation, with integrator step 1e-4 and 1e-5 for stability.
Decision rule (fixed here, before results):
  - A design is 'contact-sensitive' if |minsep(h=1e-4) - minsep(h=1e-5)| > 0.02 for either law: not used for a verdict.
  - For stable designs: the law whose judged RMSE/L against the observed run is lower wins; a law is 'refuted'
    for that run if its RMSE/L > 3 x 0.0050 (tracker-floor bar) = 0.015.
  - Sub-3 table (TAB) is refuted at r0 if it is refuted on >= 2 of the stable runs; P26 is supported if it is
    within 0.015 on all stable runs.
"""
import math, sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
src = (HERE / "subthree_compare_2026-11-25.py").read_text().split("for rid in")[0]
ns = {"__name__": "x"}; sys.argv = [sys.argv[0], "."]
exec(compile(src, "sc", "exec"), ns)
run, LAWS = ns["run"], ns["LAWS"]
DESIGNS = [
    # id, r0, orientation, T, sample_dt
    ("D1", 2.00, "vertical", 0.6, 0.001),
    ("D2", 2.00, "diagonal", 0.6, 0.001),
    ("D3", 1.75, "horizontal", 0.5, 0.001),
    ("D4", 1.75, "vertical", 0.5, 0.001),
    ("D5", 1.50, "horizontal", 0.6, 0.001),
    ("D6", 2.25, "horizontal", 0.8, 0.001),
    ("D7", 2.50, "horizontal", 1.0, 0.001),
    ("D8", 2.75, "horizontal", 1.0, 0.001),
]
def layout(r0, orient):
    c = 5.0
    if orient == "horizontal": d = (r0/2, 0.0)
    elif orient == "vertical": d = (0.0, r0/2)
    else: d = (r0/2/math.sqrt(2), r0/2/math.sqrt(2))
    return [[c-d[0], c-d[1]], [c+d[0], c+d[1]]], [[0.0, 0.0], [0.0, 0.0]]
out = []
for did, r0, orient, T, dt in DESIGNS:
    p0, v0 = layout(r0, orient)
    res = {"design": did, "r0": r0, "orient": orient, "T": T, "sample_dt": dt, "p0": p0, "laws": {}}
    for name in ["TAB", "P26"]:
        a = run(p0, v0, LAWS[name], T, dt, h=1e-4)
        b = run(p0, v0, LAWS[name], T, dt, h=1e-5)
        mina = min(math.dist(a[t][0], a[t][1]) for t in a)
        # minimum over the fine-step trajectory (min over all h=1e-5 integration is not stored; use samples)
        minb = min(math.dist(b[t][0], b[t][1]) for t in b)
        se = sum((a[t][i][k]-b[t][i][k])**2 for t in a for i in range(2) for k in range(2))
        n = len(a)*4
        res["laws"][name] = {"minsep_h1e-4": round(mina,4), "minsep_h1e-5": round(minb,4),
                             "integrator_RMSE_over_L": round(math.sqrt(se/n)/10.0, 6),
                             "stable": math.sqrt(se/n)/10.0 < 0.002}
    out.append(res)
    print(did, r0, orient, T, {k: (v["minsep_h1e-5"], v["stable"]) for k, v in res["laws"].items()})
(HERE / "prereg_subthree_2026-11-25.json").write_text(json.dumps(out, indent=1))
