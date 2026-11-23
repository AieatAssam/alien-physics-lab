"""Judge-style RMSE/L for the P-0024 predictor against lab-b's round-2 review runs
2026-11-23/r2/lab-b/001-005. Run as: python3 -I judge_P0024_review_2026-11-23.py <repo_root>
Pure stdlib; loads the paper's model.py via importlib (read only).
"""
import sys, json, math, importlib.util, os

root = sys.argv[1]
spec = importlib.util.spec_from_file_location("p0024", os.path.join(root, "papers/P-0024/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
L = 10.0
BAR = 3 * 0.006

for i in ["001", "002", "003", "004", "005"]:
    rid = f"2026-11-23/r2/lab-b/{i}"
    req = json.load(open(os.path.join(root, "requests", rid + ".json")))
    res = json.load(open(os.path.join(root, "results", rid + ".json")))
    setup = req["setup"]
    pred = m.predict(setup)
    sq, n = 0.0, 0
    for ps, rs in zip(pred, res["samples"]):
        assert abs(ps["t"] - rs["t"]) < 1e-9
        if rs["t"] <= 0:
            continue
        for pp, mm in zip(ps["particles"], sorted(rs["particles"], key=lambda q: q["id"])):
            for k in range(2):
                sq += (pp["pos"][k] - mm["pos"][k]) ** 2; n += 1
    rmse_L = math.sqrt(sq / n) / L
    r0 = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])
    print(json.dumps({"id": rid, "r0": round(r0, 3), "T": setup["duration"],
                      "rmse_L": round(rmse_L, 5), "pass": rmse_L <= BAR}))
