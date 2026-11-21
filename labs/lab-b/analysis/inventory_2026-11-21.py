"""Inventory of lab-b runs: species, pair separations, T, N. Run: python3 -I out/labs/lab-b/analysis/inventory_2026-11-21.py"""
import json, os, glob, math
rows = []
for p in sorted(glob.glob("requests/*/*/lab-b/*.json")):
    rq = json.load(open(p))
    rid = rq["request_id"]
    day, rnd, lab, n = rid.split("/")
    rp = os.path.join("results", day, rnd, lab, n + ".json")
    if not os.path.exists(rp):
        continue
    res = json.load(open(rp))
    if res.get("status") != "ok":
        continue
    parts = rq["setup"]["particles"]
    seps = []
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            seps.append(math.dist(parts[i]["pos"], parts[j]["pos"]))
    sp = "".join(p["species"] for p in parts)
    T = rq["setup"]["duration"]
    rows.append((rid, sp, len(parts), T, min(seps) if seps else 0, max(seps) if seps else 0, rq["account"], rq.get("cites_paper", "")))
for r in rows:
    print("%-30s spec=%-6s N=%d T=%-5s sep=[%.4f, %.4f] acct=%s cites=%s" % r)
