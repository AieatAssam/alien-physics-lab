"""Score P-0031 predict() (out/papers/P-0031/model.py) on its evidence runs. Run: python3 -I <this> <repo_root>."""
import importlib.util, json, math, os, sys
ROOT = sys.argv[1]
spec = importlib.util.spec_from_file_location("p0031", os.path.join(ROOT, "out/papers/P-0031/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ev = ["2026-11-25/r2/lab-c/001", "2026-11-25/r2/lab-c/002", "2026-11-25/r2/lab-c/006",
      "2026-11-25/r1/lab-c/012", "2026-11-25/r1/lab-c/013"]
for rid in ev:
    req = json.load(open(os.path.join(ROOT, "requests", rid + ".json")))
    res = json.load(open(os.path.join(ROOT, "results", rid + ".json")))
    pred = m.predict(req["setup"])
    se = n = 0
    for p, s in zip(pred, res["samples"]):
        assert abs(p["t"] - s["t"]) < 1e-9
        for i in range(2):
            for c in range(2):
                e = p["particles"][i]["pos"][c] - s["particles"][i]["pos"][c]
                se += e * e; n += 1
    r0 = math.dist(req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"])
    print(f"{rid} r0={r0:.6f} T={req['setup']['duration']} RMSE/L={math.sqrt(se/n)/10:.5f} bar(3x0.006)=0.018 acct={req['account']}")
# the paper's model must refuse out-of-domain input
for bad in [dict(r0=1.75), dict(r0=2.75)]:
    pass
