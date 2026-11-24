"""Score held-out runs 2026-11-23/r3/lab-b/001-004 against the P-0025 predictor (judge-style RMSE/L, t > 0, T <= 2).
Usage: python3 -I score_heldout_2026-11-24.py <repo_root>
"""
import sys, json, math, os, importlib.util
sys.path.insert(0, "/tmp/lab-b-pylib")
root = sys.argv[1]
spec = importlib.util.spec_from_file_location("p0025", os.path.join(root, "papers/P-0025/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
L = 10.0
for n in ["001", "002", "003", "004"]:
    sfx = "2026-11-23/r3/lab-b/" + n
    req = json.load(open(os.path.join(root, "requests", sfx + ".json")))
    res = json.load(open(os.path.join(root, "results", sfx + ".json")))
    setup = dict(req["setup"]); setup["duration"] = min(setup["duration"], 2.0)
    pred = m.predict(setup)
    sq = cnt = 0
    for ps in pred:
        if ps["t"] <= 0:
            continue
        rs = next(s for s in res["samples"] if abs(s["t"] - ps["t"]) < 1e-9)
        for pp, mm in zip(ps["particles"], sorted(rs["particles"], key=lambda q: q["id"])):
            for k in range(2):
                sq += (pp["pos"][k] - mm["pos"][k]) ** 2; cnt += 1
    r0 = math.dist(req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"])
    species = [p["species"] for p in req["setup"]["particles"]]
    print(json.dumps({"id": sfx, "species": species, "r0": round(r0, 3), "T": setup["duration"],
                      "dt": req["setup"]["sample_dt"], "rmse_L": round(math.sqrt(sq / cnt) / L, 5),
                      "bar_0.021": math.sqrt(sq / cnt) / L <= 0.021}))
