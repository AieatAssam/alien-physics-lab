"""Score lab-c 2026-11-28/r1 research runs 001-010 with the pre-registered rules.

Contact = first sample with pair separation < 0.2 (threshold declared 2026-11-28).
Post-contact max separation: >= 5 ejected, < 3 bound, 3 to 5 no verdict.
Usage: python3 -I score_r1_2026-11-28_research.py <repo_root>
"""
import json
import math
import os
import sys

REPO = sys.argv[1]
DATE, RND, LAB = "2026-11-28", "r1", "lab-c"
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
    row = {"run": f"{DATE}/{RND}/{LAB}/{rid}", "species": [p0["species"], p1["species"]],
           "r0": round(r0, 3), "x0": p0["pos"][0], "y0": p0["pos"][1],
           "x1": p1["pos"][0], "y1": p1["pos"][1], "T": s["duration"], "sample_dt": s["sample_dt"],
           "n_samples": len(seps), "min_sep": round(min(d for _, d in seps), 3)}
    if contact is None:
        row.update(contact_t=None, post_max=None, verdict="no contact")
    else:
        tc = contact[0]
        post = [d for t, d in seps if t >= tc]
        pm = max(post)
        row.update(contact_t=round(tc, 3), post_max=round(pm, 2),
                   verdict="ejected" if pm >= 5 else ("bound" if pm < 3 else "no verdict"))
    return row


rows = [score(n) for n in range(1, 11)]
for r in rows:
    print(json.dumps(r))
