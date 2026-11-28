"""Score lab-a review runs 2026-11-28/r1/lab-a/001-005 against P-0037 predict().

RMSE/L: sqrt(mean over samples, particles, coords of squared position error) / L, L = 10.
Usage: python3 -I score_P0037_review_2026-11-28.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

ROOT = sys.argv[1]
L = 10.0
BAR = 3 * 0.007  # 3 x predicted_error of P-0037-c1

spec = importlib.util.spec_from_file_location(
    "p0037", os.path.join(ROOT, "papers/P-0037/model.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

out = {}
for n in range(1, 6):
    rid = f"2026-11-28/r1/lab-a/{n:03d}"
    req = json.load(open(os.path.join(ROOT, f"requests/{rid}.json")))
    res = json.load(open(os.path.join(ROOT, f"results/{rid}.json")))
    setup = req["setup"]
    try:
        pred = mod.predict(setup)
    except ValueError as e:
        out[rid] = {"in_domain": False, "reason": str(e)}
        continue
    obs = res["samples"]
    assert len(pred) == len(obs), (rid, len(pred), len(obs))
    se, cnt = 0.0, 0
    for p, o in zip(pred, obs):
        assert abs(p["t"] - o["t"]) < 1e-9, (rid, p["t"], o["t"])
        byid = {q["id"]: q["pos"] for q in o["particles"]}
        for q in p["particles"]:
            ob = byid[q["id"]]
            for k in range(2):
                se += (q["pos"][k] - ob[k]) ** 2
                cnt += 1
    rmse_l = math.sqrt(se / cnt) / L
    r0 = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])
    out[rid] = {"in_domain": True, "r0": round(r0, 4), "duration": setup["duration"],
                "rmse_over_L": round(rmse_l, 5), "within_bar_0.021": rmse_l <= BAR}

n_ok = sum(1 for v in out.values() if v.get("in_domain") and v["within_bar_0.021"])
out["_summary"] = {"bar": BAR, "runs_in_domain_within_bar": n_ok,
                   "verdict": "replicated" if n_ok >= 3 else "not replicated"}
print(json.dumps(out, indent=2))
