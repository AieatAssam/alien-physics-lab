"""Validate P-0022 claim schema, run its model on the cited runs, judge-style RMSE/L, and min separation."""
import sys, json, math, importlib.util, os
sys.path.insert(0, "/tmp/lab-b-pylib")
import jsonschema
root = sys.argv[1]
claim = json.load(open(os.path.join(root, "out/papers/P-0022/claim.json")))
schema = json.load(open(os.path.join(root, "protocol/claim.schema.json")))
jsonschema.validate(claim, schema)
print("claim schema OK")
spec = importlib.util.spec_from_file_location("m", os.path.join(root, "out/papers/P-0022/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for rid in claim["claims"][0]["evidence"]:
    suffix = rid
    req = json.load(open(os.path.join(root, "requests", suffix + ".json")))
    res = json.load(open(os.path.join(root, "results", suffix + ".json")))
    print(rid, [(p["species"], p["pos"]) for p in req["setup"]["particles"]], req["setup"]["duration"], req["setup"]["sample_dt"], req["account"])
    pred = m.predict(req["setup"])
    se, n = 0.0, 0
    minsep = 9e9
    for ps, pm in zip(pred, res["samples"]):
        assert abs(ps["t"] - pm["t"]) < 1e-9
        d = math.dist(pm["particles"][0]["pos"], pm["particles"][1]["pos"]); minsep = min(minsep, d)
        for a, b in zip(ps["particles"], pm["particles"]):
            for k in range(2):
                se += (a["pos"][k] - b["pos"][k]) ** 2; n += 1
    print("  RMSE/L (all samples) = %.5f" % (math.sqrt(se / n) / 10.0), " min measured sep = %.3f" % minsep)
    pm_min = min(math.dist(p["pos"][0], p["pos"][1]) for p in [{"pos": [q["pos"] for q in s["particles"]]} for s in pred])
    print("  model min sep = %.3f" % pm_min)
