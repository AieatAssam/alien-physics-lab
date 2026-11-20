"""Inventory of lab-b runs for review domain checks (round 3, 2026-11-20).

For every lab-b request in the repo: species, N, initial pairwise separations, whether at rest,
duration, sample_dt, cost, and result status. Usage: python3 -I inventory_2026-11-20.py <repo_root>
"""
import glob
import json
import math
import os
import sys

root = sys.argv[1]
rows = []
for rp in sorted(glob.glob(os.path.join(root, "requests", "*", "r*", "lab-b", "*.json"))):
    req = json.load(open(rp))
    rid = req["request_id"]
    parts = req["setup"]["particles"]
    seps = [math.dist(parts[a]["pos"], parts[b]["pos"])
            for a in range(len(parts)) for b in range(a + 1, len(parts))]
    at_rest = all(abs(v) < 1e-12 for p in parts for v in p["vel"])
    rp_res = rp.replace(os.sep + "requests" + os.sep, os.sep + "results" + os.sep)
    status, cost = "missing", None
    if os.path.exists(rp_res):
        res = json.load(open(rp_res))
        status, cost = res.get("status"), res.get("cost")
    rows.append((rid, req["account"], req.get("cites_paper", "-"),
                 "".join(p["species"] for p in parts), len(parts),
                 "[%s]" % ", ".join("%.3f" % s for s in seps) if seps else "-",
                 "rest" if at_rest else "MOVING",
                 req["setup"]["duration"], req["setup"]["sample_dt"], status, cost))
for r in rows:
    print("%-28s %-8s %-7s %-6s N=%d seps=%-22s %-6s T=%-5s dt=%-5s %s cost=%s" % r)
