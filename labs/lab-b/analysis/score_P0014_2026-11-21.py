"""Judge-style score of P-0014 (lab-keystone) on lab-b in-domain runs. RMSE over all particles/coords/samples, error = RMSE/L (L=10).
Run: python3 -I out/labs/lab-b/analysis/score_P0014_2026-11-21.py"""
import importlib.util, os, json, math
ROOT = os.getcwd()
def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def score(mod, rid, domain):
    day, rnd, lab, n = rid.split("/")
    rq = json.load(open(os.path.join(ROOT, "requests", day, rnd, lab, n + ".json")))
    res = json.load(open(os.path.join(ROOT, "results", day, rnd, lab, n + ".json")))
    sp = rq["setup"]
    parts = sp["particles"]
    lo, hi = domain["r_range"]
    ok = (len(parts) <= domain["max_particles"] and all(p["species"] in domain["species"] for p in parts)
          and all(lo <= math.dist(parts[i]["pos"], parts[j]["pos"]) <= hi for i in range(len(parts)) for j in range(i+1, len(parts))))
    pred = mod.predict(sp)
    pm = {round(s["t"], 9): s["particles"] for s in pred}
    sq = 0.0; c = 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t not in pm: continue
        for i, p in enumerate(s["particles"]):
            for k in range(2):
                d = p["pos"][k] - pm[t][i]["pos"][k]; sq += d * d; c += 1
    rmse = math.sqrt(sq / c)
    return ok, rmse, rmse / 10.0
mod = load_mod(os.path.join(ROOT, "papers/P-0014/model.py"), "p14")
dom = {"species": ["A", "C"], "r_range": [2.5, 3.5], "max_particles": 2}
for rid in ["2026-11-18/r2/lab-b/010", "2026-11-18/r2/lab-b/012", "2026-11-18/r2/lab-b/014", "2026-11-18/r3/lab-b/016"]:
    ok, rmse, err = score(mod, rid, dom)
    print(rid, "in_domain=%s rmse=%.4f judge_err=%.5f (bar 0.039 at 3x0.013)" % (ok, rmse, err))
