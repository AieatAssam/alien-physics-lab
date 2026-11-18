"""Compare 2026-11-17/r2/lab-c/001 with its replicate 2026-11-18/r2/lab-c/001 (separation, id-free),
and report the separation range covered by 002 and 003 (velocity-term pair).
Usage: python3 -I out/labs/lab-c/analysis/energy_replicate_compare.py  (repo root)
"""
import json
import numpy as np

def load(req, res):
    q = json.load(open(req)); r = json.load(open(res))
    S = r["samples"]
    t = np.array([s["t"] for s in S])
    O = np.array([[[p["pos"] for p in s["particles"] if p["id"] == i][0] for i in (0, 1)] for s in S])
    sep = np.linalg.norm(O[:, 0] - O[:, 1], axis=1)
    return q, t, sep

qa, ta, sa = load("requests/2026-11-17/r2/lab-c/001.json", "results/2026-11-17/r2/lab-c/001.json")
qb, tb, sb = load("requests/2026-11-18/r2/lab-c/001.json", "results/2026-11-18/r2/lab-c/001.json")
print("old setup:", [(p["species"], p["pos"], p["vel"]) for p in qa["setup"]["particles"]], "T", qa["setup"]["duration"], "dt", qa["setup"]["sample_dt"])
print("new setup:", [(p["species"], p["pos"], p["vel"]) for p in qb["setup"]["particles"]], "T", qb["setup"]["duration"], "dt", qb["setup"]["sample_dt"])
print("time   old_sep  new_sep")
for tt in (0.0, 0.5, 1.0, 1.2, 1.25, 1.5, 2.0, 3.0):
    ka = int(np.argmin(np.abs(ta - tt))); kb = int(np.argmin(np.abs(tb - tt)))
    if ta[ka] > 0 and abs(ta[ka]-tt) > 0.01: pass
    sa_s = f"{sa[ka]:6.3f}" if abs(ta[ka]-tt) < 0.02 else "   n/a"
    sb_s = f"{sb[kb]:6.3f}" if abs(tb[kb]-tt) < 0.02 else "   n/a"
    print(f"{tt:5.2f}  {sa_s}  {sb_s}")
print("old: min sep", sa.min().round(3), "at", ta[sa.argmin()], "| new: min sep", sb.min().round(3), "at", tb[sb.argmin()])
print("old: last t", ta[-1], "sep at end", sa[-1].round(3), "| new: last t", tb[-1], "sep at end", sb[-1].round(3))
for name, req, res in [("002 approach", "requests/2026-11-18/r2/lab-c/002.json", "results/2026-11-18/r2/lab-c/002.json"),
                       ("003 recede", "requests/2026-11-18/r2/lab-c/003.json", "results/2026-11-18/r2/lab-c/003.json")]:
    _, t, s = load(req, res)
    print(f"{name}: sep range [{s.min():.3f}, {s.max():.3f}] over T={t[-1]}")
