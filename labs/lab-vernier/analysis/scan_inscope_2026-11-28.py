"""Scan lab-vernier's own filed requests for in-domain two-particle at-rest runs (stdlib only).

Lists requests with exactly 2 particles, both at rest, and reports species, separation and
whether a result exists with status ok. Used to find own evidence for reviews of P-0036 / P-0037.
"""
import glob, json, math, os, sys

REPO = sys.argv[1]
rows = []
for path in sorted(glob.glob(os.path.join(REPO, "requests", "*", "*", "lab-vernier", "*.json"))):
    req = json.load(open(path))
    parts = req["setup"]["particles"]
    if len(parts) != 2:
        continue
    if any(any(v != 0 for v in p["vel"]) for p in parts):
        continue
    rid = req["request_id"]
    res_path = os.path.join(REPO, "results", rid.replace("/", os.sep) + ".json")
    status = "missing"
    if os.path.exists(res_path):
        status = json.load(open(res_path)).get("status")
    sp = "".join(sorted(p["species"] for p in parts))
    r = math.dist(parts[0]["pos"], parts[1]["pos"])
    rows.append((sp, round(r, 4), req["setup"]["duration"], req["setup"]["sample_dt"], status, rid,
                 [p["pos"] for p in parts]))
for row in rows:
    print(*row[:6])
