"""Score lab-c 2026-11-28/r2 research runs 001-008 with the pre-registered rules.

Rules (fixed in NOTEBOOK round 2, unchanged from round 1):
  Contact = first sample with pair separation < 0.2.
  Ejected = post-contact max separation >= 5. Bound = < 3. 3 to 5 = no verdict.
  Replicates at one dt that disagree = no verdict.
Usage: python3 -I score_r2_2026-11-28_research.py <repo_root>
"""
import json
import math
import os
import sys

REPO = sys.argv[1]
DATE, RND, LAB = "2026-11-28", "r2", "lab-c"
CONTACT = 0.2


def score(n):
    rid = f"{n:03d}"
    req = json.load(open(os.path.join(REPO, "requests", DATE, RND, LAB, rid + ".json")))
    res = json.load(open(os.path.join(REPO, "results", DATE, RND, LAB, rid + ".json")))
    s = req["setup"]
    p0, p1 = s["particles"]
    r0 = math.dist(p0["pos"], p1["pos"])
    seps = []
    for smp in res["samples"]:
        a, b = smp["particles"][0]["pos"], smp["particles"][1]["pos"]
        seps.append((smp["t"], math.dist(a, b)))
    contact = next(((t, d) for t, d in seps if d < CONTACT), None)
    row = {"run": f"{RND}/{LAB}/{rid}", "r0": round(r0, 3), "T": s["duration"],
           "sample_dt": s["sample_dt"], "cost": res.get("cost"), "n_samples": len(seps),
           "min_sep": round(min(d for _, d in seps), 3)}
    if contact is None:
        row.update(contact_t=None, post_max=None, verdict="no contact")
    else:
        tc = contact[0]
        post = [d for t, d in seps if t >= tc]
        pm = max(post)
        row.update(contact_t=round(tc, 4), post_max=round(pm, 2),
                   verdict="ejected" if pm >= 5 else ("bound" if pm < 3 else "no verdict"))
    return row


rows = [score(n) for n in range(1, 9)]
for r in rows:
    print(json.dumps(r))

# Replicate consistency: pair up (001,002) R13 dt 0.0025; (003,004) dt 0.0035; (005,006) dt 0.0045; (007,008) R30 dt 0.004
print()
for a, b in [(0, 1), (2, 3), (4, 5), (6, 7)]:
    ra, rb = rows[a], rows[b]
    agree = ra["verdict"] == rb["verdict"]
    print(f"{ra['run']} vs {rb['run']}: dt={ra['sample_dt']} r0={ra['r0']} "
          f"verdicts {ra['verdict']} / {rb['verdict']} agree={agree} "
          f"post_max {ra['post_max']} / {rb['post_max']}")
