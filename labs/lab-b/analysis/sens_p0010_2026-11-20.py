"""Sensitivity of the judge-style error to a common scale on P-0010's pair coefficients.

Shipped predict() is used; only COUP5 is scaled (in a copy of the module namespace), so the
output shows how much the error metric can see a K error at these run lengths. Round 3, 2026-11-20.
Usage: python3 -I sens_p0010_2026-11-20.py <P-0010 model.py> <repo_root>
"""
import importlib.util
import json
import math
import sys

spec = importlib.util.spec_from_file_location("p0010", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
root = sys.argv[2]
runs = ["2026-11-19/r2/lab-b/003", "2026-11-19/r2/lab-b/004", "2026-11-19/r3/lab-b/002",
        "2026-11-20/r1/lab-b/001", "2026-11-18/r2/lab-b/021"]
base = dict(m.COUP5)
for s in (0.85, 0.90, 1.00, 1.10):
    m.COUP5.clear()
    m.COUP5.update({k: v * s for k, v in base.items()})
    line = []
    for rid in runs:
        req = json.load(open("%s/requests/%s.json" % (root, rid)))
        res = json.load(open("%s/results/%s.json" % (root, rid)))
        pred = m.predict(req["setup"])
        sq = n = 0
        for ps, pm in zip(res["samples"], pred):
            for obs in ps["particles"]:
                for k in range(2):
                    d = obs["pos"][k] - pm["particles"][obs["id"]]["pos"][k]
                    sq += d * d
                    n += 1
        line.append("%s %.5f" % (rid.split("/")[-1], math.sqrt(sq / n) / 10))
    print("scale %.2f  " % s + "  ".join(line))
