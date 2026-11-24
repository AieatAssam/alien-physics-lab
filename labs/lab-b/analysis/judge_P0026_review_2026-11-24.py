"""Judge-style check of P-0026 (lab-keystone) against lab-b review runs 2026-11-24/r2/lab-b/006-009.

For each run: (1) domain check against the claim's stated domain (species A, 2..16 particles,
every initial pairwise distance in [1.5, 10.5]); (2) RMSE/L between predict(setup) and the measured
positions over 0 < t <= T, all particles and coordinates, L = 10; (3) reference null: the particles
held at their initial positions (zero-force model) to show the power of the test.

Usage: python3 -I judge_P0026_review_2026-11-24.py <repo_root> <paper_dir>
"""
import sys, json, math, os, importlib.util

L = 10.0
root, paper_dir = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("p0026", os.path.join(paper_dir, "model.py"))
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)

ids = ["006", "007", "008", "009"]
out = []
for n in ids:
    base = os.path.join(root, "requests", "2026-11-24", "r2", "lab-b", n + ".json")
    req = json.load(open(base))
    res = json.load(open(os.path.join(root, "results", "2026-11-24", "r2", "lab-b", n + ".json")))
    parts = req["setup"]["particles"]
    T = req["setup"]["duration"]
    pos0 = [p["pos"] for p in parts]
    # domain check (judge rules: species, count, initial pairwise distances)
    species_ok = all(p["species"] == "A" for p in parts)
    count_ok = 2 <= len(parts) <= 16
    d = [math.dist(pos0[i], pos0[j]) for i in range(len(parts)) for j in range(i + 1, len(parts))]
    rmin, rmax = min(d), max(d)
    in_dom = species_ok and count_ok and 1.5 <= rmin and rmax <= 10.5
    # model prediction
    pred = model.predict(req["setup"])
    pmap = {round(s["t"], 9): s for s in pred}
    sq, cnt, sq0 = 0.0, 0, 0.0
    worst = 0.0
    for s in res["samples"]:
        t = round(float(s["t"]), 9)
        if not (0 < t <= T + 1e-9) or t not in pmap:
            continue
        mp = {q["id"]: q["pos"] for q in pmap[t]["particles"]}
        for q in s["particles"]:
            for k in range(2):
                e = mp[q["id"]][k] - q["pos"][k]
                sq += e * e
                e0 = pos0[q["id"]][k] - q["pos"][k]
                sq0 += e0 * e0
                worst = max(worst, abs(e))
                cnt += 1
    rmse = math.sqrt(sq / cnt)
    null = math.sqrt(sq0 / cnt)
    out.append({"id": "2026-11-24/r2/lab-b/" + n, "n": len(parts), "T": T, "in_domain": in_dom,
                "pair_min": round(rmin, 3), "pair_max": round(rmax, 3), "samples": cnt // (2 * len(parts)),
                "rmse_over_L": round(rmse / L, 5), "null_rmse_over_L": round(null / L, 5),
                "max_abs_resid": round(worst, 4)})
print(json.dumps(out, indent=1))
