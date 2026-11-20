"""Score runs against a paper's SHIPPED predict(setup), unmodified (round 3, 2026-11-20).

This mirrors the judge's rule: error = RMSE over particles, samples and coordinates of
(predicted - measured) divided by L = 10. A predict() that raises is reported, not worked around.

Usage: python3 -I score_shipped_2026-11-20.py <paper model.py> <request.json> <result.json> [...]
"""
import importlib.util
import json
import math
import sys

spec = importlib.util.spec_from_file_location("paper_model", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
args = sys.argv[2:]
for i in range(0, len(args), 2):
    req = json.load(open(args[i]))
    res = json.load(open(args[i + 1]))
    rid = res.get("request_id", req.get("request_id"))
    try:
        pred = m.predict(req["setup"])
    except Exception as e:  # report, do not work around
        print(rid, "predict() RAISED:", type(e).__name__, str(e)[:120])
        continue
    sq, n = 0.0, 0
    for ps, pm in zip(res["samples"], pred):
        for obs in ps["particles"]:
            for k in range(2):
                d = obs["pos"][k] - pm["particles"][obs["id"]]["pos"][k]
                sq += d * d
                n += 1
    rms = math.sqrt(sq / n)
    print("%s N=%d samples=%d/%d rms=%.4f error=%.5f" % (
        rid, len(req["setup"]["particles"]), len(res["samples"]), len(pred), rms, rms / 10.0))
