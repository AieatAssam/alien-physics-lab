"""Inventory lab-c runs that fall inside P-0008's judged domain and score P-0008's model on them.

Domain (judging rule): species in {A,B,C}; particle count <= 4 (claim c1) ; every initial pairwise
distance within [3.0, 5.0]. Error = RMSE over (sample, particle, coordinate) between predicted and
measured positions, divided by chamber side L = 10.
Run with: python3 -I this_file  (the paper model is loaded by path with importlib).
"""
import glob, json, math, importlib.util, os, sys

ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab"
MODEL = os.path.join(ROOT, "papers/P-0008/model.py")
spec = importlib.util.spec_from_file_location("p0008", MODEL)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

L = 10.0
rows = []
for rp in sorted(glob.glob(os.path.join(ROOT, "results/*/r*/lab-c/*.json"))):
    res = json.load(open(rp))
    if res.get("status") != "ok":
        continue
    rid = res["request_id"]
    date, rnd, lab, num = rid.split("/")
    reqp = os.path.join(ROOT, "requests", date, rnd, lab, num + ".json")
    if not os.path.exists(reqp):
        continue
    req = json.load(open(reqp))
    parts = req["setup"]["particles"]
    sp = [p["species"] for p in parts]
    n = len(parts)
    dists = []
    for a in range(n):
        for b in range(a + 1, n):
            dists.append(math.hypot(parts[b]["pos"][0] - parts[a]["pos"][0],
                                    parts[b]["pos"][1] - parts[a]["pos"][1]))
    in_dom = (all(s in "ABC" for s in sp) and n <= 4 and n >= 2 and
              all(3.0 <= d <= 5.0 for d in dists))
    if not in_dom:
        continue
    at_rest = all(p["vel"] == [0.0, 0.0] for p in parts)
    pred = m.predict(req["setup"])
    se, cnt = 0.0, 0
    per_part = [0.0] * n
    for ps, pm in zip(pred, res["samples"]):
        assert abs(ps["t"] - pm["t"]) < 1e-6, (rid, ps["t"], pm["t"])
        for q in pm["particles"]:
            pid = q["id"]
            p_pred = ps["particles"][pid]["pos"]
            dx = p_pred[0] - q["pos"][0]
            dy = p_pred[1] - q["pos"][1]
            se += dx * dx + dy * dy
            per_part[pid] += dx * dx + dy * dy
            cnt += 2
    rmse = math.sqrt(se / cnt)
    rows.append({
        "request_id": rid, "account": req["account"], "species": "".join(sp), "n": n,
        "pair_dists": [round(d, 3) for d in dists], "T": req["setup"]["duration"],
        "at_rest": at_rest, "rmse_abs": round(rmse, 4), "error_norm": round(rmse / L, 5),
        "pass_3x_0.07": rmse / L <= 3 * 0.07, "n_samples": len(res["samples"]),
        "events": len(res.get("events", [])),
        "mean_resid_abs": None,
    })

for r in rows:
    print(json.dumps(r))
print("in-domain runs:", len(rows))
