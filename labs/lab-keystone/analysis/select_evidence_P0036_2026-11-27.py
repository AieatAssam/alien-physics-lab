"""Select evidence request ids for P-0036 (A-A pair at rest, r0 in [3.5, 9]).

Rule: a filed run is evidence if it is 2 A particles at rest with r0 in [3.5, 9] (the claim's domain), has a result on
file, and model.predict(setup) at scale 1 does not raise (i.e. the pair stays >= 2.5 apart over every output sample).
No selection on the measured outcome. Writes evidence_P0036_2026-11-27.json. Uses out/papers/P-0036/model.py only.
(An earlier version took the window from the fitted scale s; that was wrong and is fixed here.)
"""
import json, glob, math, os, sys
REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
sys.path.insert(0, f"{REPO}/out/papers/P-0036")
import model
HERE = os.path.dirname(os.path.abspath(__file__))
ok, refused, out_domain = [], [], 0
for path in sorted(glob.glob(f"{REPO}/requests/*/r*/*/*.json")):
    req = json.load(open(path))
    parts = req.get("setup", {}).get("particles", [])
    if len(parts) != 2 or any(p["species"] != "A" for p in parts):
        continue
    if any(any(v != 0 for v in p["vel"]) for p in parts):
        continue
    r0 = math.dist(parts[0]["pos"], parts[1]["pos"])
    if not 3.5 - 1e-9 <= r0 <= 9.0 + 1e-9:
        out_domain += 1
        continue
    d, r, lab, n = req["request_id"].split("/")
    if not os.path.exists(f"{REPO}/results/{d}/{r}/{lab}/{n}.json"):
        continue
    try:
        model.predict(req["setup"])
        ok.append(req["request_id"])
    except ValueError as e:
        refused.append((req["request_id"], str(e)[:60]))
print("in-domain runs with results: predict ok =", len(ok), " refused (window) =", len(refused), " r0 outside [3.5,9] =", out_domain)
json.dump({"evidence": ok, "refused_by_window": [r for r, _ in refused]},
          open(os.path.join(HERE, "evidence_P0036_2026-11-27.json"), "w"), indent=1)
