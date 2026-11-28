"""Score lab-vernier's round-3 contact runs (2026-11-27/r3) against the pre-registered table in NOTEBOOK.md.

stdlib only. Usage: python3 -I score_r3_contact_2026-11-28.py <repo_root>
Separation is the raw tracker separation; 0.02-wide bin means around the target time are also reported
(the pre-registration used 0.02-bin means at t = 0.60).
"""
import json, math, sys, os
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

print("== r3/002-006 (exact r1/001 setup), separation at t=0.60 (0.02-bin mean)")
vals = []
for n in ["002", "003", "004", "005", "006"]:
    rid = f"2026-11-27/r3/lab-vernier/{n}"
    req, res, seps = load(rid)
    m = binmean(seps, 0.60)
    vals.append(m)
    cls = "plateau" if 1.10 <= m <= 1.25 else ("rise" if 1.85 <= m <= 2.15 else "OUTSIDE BANDS")
    print(f"  {n} status={res['status']} dt={req['setup']['sample_dt']} T={req['setup']['duration']} "
          f"sep(0.60)={m:.3f} class={cls}")
print("== r3/007-010 (exact r2/003 setup): max sep in [0.5,2.0], min sep, count of dips below 0.3 (in [0.5,2.0])")
for n in ["007", "008", "009", "010"]:
    rid = f"2026-11-27/r3/lab-vernier/{n}"
    req, res, seps = load(rid)
    win = [(t, d) for t, d in seps if 0.5 <= t <= 2.0]
    mx = max(d for _, d in win)
    mn = min(d for _, d in win)
    # dips: entries into below-0.3 from above
    dips = 0; below = False
    for t, d in win:
        if d < 0.3 and not below:
            dips += 1; below = True
        elif d >= 0.3:
            below = False
    print(f"  {n} status={res['status']} dt={req['setup']['sample_dt']} max={mx:.3f} min={mn:.4f} dips<0.3={dips}"
          f" H_dt={'holds' if mx < 1.0 and dips >= 2 else 'FAILS'}")
print("== r3/001 grant: four pairs, per-pair separation traces (see pairs in request)")
req, res, _ = load("2026-11-27/r3/lab-vernier/001")
print("  status", res["status"], "n_particles", len(req["setup"]["particles"]), "dt", req["setup"]["sample_dt"])
