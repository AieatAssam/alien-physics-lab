"""Generic judge-style check: a paper's predict(setup) against measured runs (tracker, 0 < t <= T).

For each request id given: domain check (species list, particle count, all initial pairwise distances
in r_range), then RMSE/L over all particles, coordinates and samples with 0 < t <= T (L = 10), and the
zero-force null (particles held at their initial positions) for reference. Duration is not part of the
judged domain; a model that raises (e.g. duration beyond its window) is reported as ERROR.

Usage: python3 -I judge_generic_2026-11-24.py <repo_root> <paper_dir> <domain_json> <suffix> [<suffix> ...]
  suffix like 2026-11-24/r2/lab-b/002 (reads requests/<suffix>.json and results/<suffix>.json)
  domain_json e.g. '{"species":["A"],"r_range":[3,9],"max_particles":2}'
"""
import sys, json, math, os, importlib.util
sys.path.insert(0, "/tmp/lab-b-pylib")

L = 10.0
root, paper_dir, dom = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
spec = importlib.util.spec_from_file_location("paper_model", os.path.join(paper_dir, "model.py"))
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)

rows = []
for suf in sys.argv[4:]:
    req = json.load(open(os.path.join(root, "requests", suf + ".json")))
    res = json.load(open(os.path.join(root, "results", suf + ".json")))
    parts = req["setup"]["particles"]
    T = req["setup"]["duration"]
    pos0 = [p["pos"] for p in parts]
    d = [math.dist(pos0[i], pos0[j]) for i in range(len(parts)) for j in range(i + 1, len(parts))]
    in_dom = (all(p["species"] in dom["species"] for p in parts) and len(parts) <= dom["max_particles"]
              and dom["r_range"][0] <= min(d) and max(d) <= dom["r_range"][1])
    row = {"id": suf, "n": len(parts), "species": parts[0]["species"], "r0": round(min(d), 4),
           "r_max": round(max(d), 4), "T": T, "in_domain": in_dom}
    try:
        pred = model.predict(req["setup"])
    except ValueError as e:
        row["rmse_over_L"] = "ERROR: " + str(e)
        rows.append(row)
        continue
    pmap = {round(s["t"], 9): s for s in pred}
    sq = sq0 = 0.0
    cnt = 0
    for s in res["samples"]:
        t = round(float(s["t"]), 9)
        if not (0 < t <= T + 1e-9) or t not in pmap:
            continue
        mp = {q["id"]: q["pos"] for q in pmap[t]["particles"]}
        for q in s["particles"]:
            for k in range(2):
                sq += (mp[q["id"]][k] - q["pos"][k]) ** 2
                sq0 += (pos0[q["id"]][k] - q["pos"][k]) ** 2
                cnt += 1
    row["rmse_over_L"] = round(math.sqrt(sq / cnt) / L, 5)
    row["null_over_L"] = round(math.sqrt(sq0 / cnt) / L, 5)
    rows.append(row)
print(json.dumps(rows, indent=1))
