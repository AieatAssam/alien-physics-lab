"""Judge-style check of P-0023 (lab-vernier): RMSE/L of papers/P-0023/model.py predict(setup)
against measured tracker positions, L = 10. Domain check: A and B only, one each, at rest,
initial separation in [8.9, 9.1], duration <= 10, particles <= 2.

Usage: python3 -I judge_P0023_2026-11-23.py REPO REQ_ID [REQ_ID ...]   (REQ_ID like 2026-11-22/r2/lab-vernier/001)
"""
import json, math, os, sys, importlib.util

root = sys.argv[1]
spec = importlib.util.spec_from_file_location("p0023", os.path.join(root, "papers/P-0023/model.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
L, PE = 10.0, 0.006
BAR = 3 * PE


def run(rid):
    p = rid.split("/")  # date, round, lab, nnn
    req = json.load(open(os.path.join(root, "requests", p[0], p[1], p[2], p[3] + ".json")))
    res = json.load(open(os.path.join(root, "results", p[0], p[1], p[2], p[3] + ".json")))
    setup = req["setup"]
    species = [q["species"] for q in setup["particles"]]
    sep = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])
    vel0 = all(v == 0.0 for q in setup["particles"] for v in q["vel"])
    in_domain = (sorted(species) == ["A", "B"] and len(species) <= 2 and 8.9 <= sep <= 9.1
                 and setup["duration"] <= 10.0 + 1e-12 and vel0)
    pred = mod.predict(setup)
    se, n = 0.0, 0
    for ps, pm in zip(pred, res["samples"]):
        assert abs(ps["t"] - pm["t"]) < 1e-9
        for a, b in zip(ps["particles"], pm["particles"]):
            for k in range(2):
                se += (a["pos"][k] - b["pos"][k]) ** 2
                n += 1
    rmse = math.sqrt(se / n) / L
    return dict(id=req["request_id"], species="".join(species), sep=round(sep, 4), T=setup["duration"],
                in_domain=in_domain, rmse_L=round(rmse, 5), under_bar=rmse <= BAR, bar=round(BAR, 4))


if __name__ == "__main__":
    for rid in sys.argv[2:]:
        print(json.dumps(run(rid)))
