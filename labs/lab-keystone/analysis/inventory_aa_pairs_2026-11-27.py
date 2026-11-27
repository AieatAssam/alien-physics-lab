"""Inventory all filed requests with exactly two A particles at rest, with r0, T, sample_dt, account, and whether a result exists.
Read-only over requests/ and results/. Pure python."""
import json, glob, math, os
REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
rows = []
for path in sorted(glob.glob(f"{REPO}/requests/*/r*/*/*.json")):
    try:
        req = json.load(open(path))
    except Exception:
        continue
    parts = req.get("setup", {}).get("particles", [])
    if len(parts) != 2:
        continue
    if any(p["species"] != "A" for p in parts):
        continue
    if any(any(v != 0 for v in p["vel"]) for p in parts):
        continue
    r0 = math.dist(parts[0]["pos"], parts[1]["pos"])
    rid = req["request_id"]
    rp = f"{REPO}/results/" + rid.replace("/r", "/r", 1)
    # results path: results/<date>/r<round>/<lab>/<nnn>.json
    d, r, lab, n = rid.split("/")
    rp = f"{REPO}/results/{d}/{r}/{lab}/{n}.json"
    status = "result" if os.path.exists(rp) else "-"
    rows.append((round(r0, 3), req["setup"]["duration"], req["setup"]["sample_dt"], req["account"], rid, status))
rows.sort()
for row in rows:
    print(f"r0={row[0]:6.3f}  T={row[1]:6.2f}  dt={row[2]:<7} {row[3]:9s} {row[4]:32s} {row[5]}")
print("total A-A rest pairs:", len(rows))
