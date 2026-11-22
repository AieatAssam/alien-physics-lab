"""Judge-style check of P-0021 (lab-vernier) against lab-b review runs.

RMSE/L between model predict(setup) and measured tracker positions, L = 10.
Usage: python3 -I review_P0021_2026-11-22.py <repo_root>
"""
import json, math, sys, os, importlib.util

root = sys.argv[1]
spec = importlib.util.spec_from_file_location("p0021", os.path.join(root, "papers/P-0021/model.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
L = 10.0
PE = 0.007
BAR = 3 * PE

def check(req_path, res_path):
    req = json.load(open(req_path))
    res = json.load(open(res_path))
    setup = req["setup"]
    species = [p["species"] for p in setup["particles"]]
    sep = math.hypot(setup["particles"][1]["pos"][0] - setup["particles"][0]["pos"][0],
                     setup["particles"][1]["pos"][1] - setup["particles"][0]["pos"][1])
    in_domain = (sorted(species) == ["A", "B"] and len(species) <= 2 and 6.9 <= sep <= 7.1
                 and setup["duration"] <= 6.0 + 1e-12)
    pred = mod.predict(setup)
    se_all, n_all, se_post, n_post = 0.0, 0, 0.0, 0
    for ps, pm in zip(pred, res["samples"]):
        assert abs(ps["t"] - pm["t"]) < 1e-9, (ps["t"], pm["t"])
        for a, b in zip(ps["particles"], pm["particles"]):
            assert a["id"] == b["id"]
            for k in range(2):
                e = (a["pos"][k] - b["pos"][k]) ** 2
                se_all += e; n_all += 1
                if ps["t"] > 0:
                    se_post += e; n_post += 1
    rmse_all = math.sqrt(se_all / n_all) / L
    rmse_post = math.sqrt(se_post / n_post) / L
    return dict(id=req["request_id"], species=species, sep=round(sep, 4), T=setup["duration"],
                in_domain=in_domain, rmse_L_all=round(rmse_all, 5), rmse_L_post_t0=round(rmse_post, 5),
                ok_bar=rmse_all <= BAR, bar=BAR)

base = os.path.join(root, "requests/2026-11-22/r2/lab-b")
rbase = os.path.join(root, "results/2026-11-22/r2/lab-b")
for n in ["001", "002", "003", "004"]:
    print(json.dumps(check(os.path.join(base, n + ".json"), os.path.join(rbase, n + ".json"))))
