"""Residual check of out/papers/P-0006/model.py on round-3 runs (2026-11-18/r3/lab-a/001-007).

Usage: python3 -I check_p0006.py <repo_root>
The predictor has no fitted constants for these runs (SCALE from A-A reference runs and
P-0005 run means), so this is an out-of-sample check.
"""
import json, math, os, sys
ROOT = sys.argv[1]
sys.path.insert(0, os.path.join(ROOT, "out", "papers", "P-0006"))
import model  # noqa: E402

for rid in ["001", "002", "003", "004", "005", "006", "007"]:
    req = json.load(open(os.path.join(ROOT, "requests", "2026-11-18", "r3", "lab-a", rid + ".json")))
    res = json.load(open(os.path.join(ROOT, "results", "2026-11-18", "r3", "lab-a", rid + ".json")))
    pred = model.predict(req["setup"])
    ss = 0.0; n = 0; worst = 0.0
    for ps, ob in zip(pred, res["samples"]):
        assert abs(ps["t"] - ob["t"]) < 1e-9
        obs = {q["id"]: q["pos"] for q in ob["particles"]}
        for q in ps["particles"]:
            for k in range(2):
                e = q["pos"][k] - obs[q["id"]][k]
                ss += e * e; n += 1; worst = max(worst, abs(e))
    sp = [p["species"] for p in req["setup"]["particles"]]
    print(rid, "".join(sp), "rms/coord %.4f" % math.sqrt(ss / n), "max|res| %.3f" % worst)
