"""lab-a 2026-11-21: editor-metric error of the P-0012 predictor on its two evidence runs (and the flat K=18 alternative).
Usage: python3 -I check_P0012_2026-11-21.py <repo_root>"""
import importlib.util, json, math, os, sys
root = sys.argv[1]
spec = importlib.util.spec_from_file_location("m12", os.path.join(root, "out", "papers", "P-0012", "model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def err(pred, truth, side=10.0):
    table = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    sq = []
    for s in truth:
        row = table[round(s["t"], 9)]
        for p in s["particles"]:
            q = row[p["id"]]
            sq.append((q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2)
    return math.sqrt(sum(sq) / len(sq)) / side

for n in ["003", "004"]:
    req = json.load(open(os.path.join(root, "requests", "2026-11-20", "r3", "lab-a", n + ".json")))
    res = json.load(open(os.path.join(root, "results", "2026-11-20", "r3", "lab-a", n + ".json")))
    pred = m.predict(req["setup"])
    ds = [math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in res["samples"]]
    print("run", n, "err/L = %.5f" % err(pred, res["samples"]), "min measured sep = %.3f" % min(ds))
