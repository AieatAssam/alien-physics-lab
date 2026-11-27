"""Score 2026-11-27/r2/lab-c/001-012 (replicates of r1-012 and r1-013 setups) against the
pre-registered rule in labs/lab-c/NOTEBOOK.md (round 2 section).

Contact = first sample with pair separation < 0.1. Post-contact max >= 5 -> ejected,
< 3 -> bound, 3-5 -> no verdict. Usage: python3 -I score_r2_replicates_2026-11-27.py <repo_root>
"""
import json
import math
import sys

ROOT = sys.argv[1]


def score(path):
    d = json.load(open(path))
    seps = [(s["t"], math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]))
            for s in d["samples"]]
    contact = next((t for t, x in seps if x < 0.1), None)
    post = [x for t, x in seps if contact is not None and t >= contact]
    pmax = max(post) if post else float("nan")
    if contact is None:
        verdict = "no contact"
    elif pmax >= 5:
        verdict = "ejected"
    elif pmax < 3:
        verdict = "bound"
    else:
        verdict = "no verdict"
    return contact, pmax, verdict, len(seps), d["cost"], d["budget_remaining"]


def show(label, path):
    c, p, v, n, cost, rem = score(path)
    print(f"{label:<42} contact={c} post_max={p:.2f} -> {v} (n={n}, cost={cost}, remaining={rem})")
    return v


print("== r1-012 setup (dt 0.005) ==")
anchor_012 = show("2026-11-26/r1/012 (anchor, ejected)", f"{ROOT}/results/2026-11-26/r1/lab-c/012.json")
rep_012 = []
for n in range(1, 9):
    rep_012.append(show(f"2026-11-27/r2/{n:03d} (replicate)",
                        f"{ROOT}/results/2026-11-27/r2/lab-c/{n:03d}.json"))
f012 = rep_012.count("ejected")
b012 = rep_012.count("bound")
print(f"r1-012 replicates: ejected={f012}, bound={b012}, other={8 - f012 - b012}")

print("\n== r1-013 setup (dt 0.005) ==")
anchor_013 = show("2026-11-26/r1/013 (anchor, ejected)", f"{ROOT}/results/2026-11-26/r1/lab-c/013.json")
rep_013 = []
for n in range(9, 13):
    rep_013.append(show(f"2026-11-27/r2/{n:03d} (replicate)",
                        f"{ROOT}/results/2026-11-27/r2/lab-c/{n:03d}.json"))
f013 = rep_013.count("ejected")
b013 = rep_013.count("bound")
print(f"r1-013 replicates: ejected={f013}, bound={b013}, other={4 - f013 - b013}")
