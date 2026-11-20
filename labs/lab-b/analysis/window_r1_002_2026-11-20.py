"""Score 2026-11-20/r1/lab-b/002 (A,B,C side 5, T=4) against P-0007's SHIPPED predict(), in windows.

Pairwise-sum prediction with P-0005 coefficients at side 5 (P-0007 accepts side 5.0 only).
Windows show whether a three-body residual builds up after T = 1.5. Round 3, 2026-11-20.
Usage: python3 -I window_r1_002_2026-11-20.py <P-0007 model.py> <request.json> <result.json>
"""
import importlib.util
import json
import math
import sys

spec = importlib.util.spec_from_file_location("p0007", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
req = json.load(open(sys.argv[2]))
res = json.load(open(sys.argv[3]))
pred = m.predict(req["setup"])
rows = []
for ps, pm in zip(res["samples"], pred):
    per = []
    for obs in ps["particles"]:
        for k in range(2):
            per.append(obs["pos"][k] - pm["particles"][obs["id"]]["pos"][k])
    rows.append((ps["t"], per))
# mean residual per coordinate in each window, and rms
for lo, hi in [(0.0, 1.5), (1.5, 2.5), (2.5, 4.01)]:
    sel = [d for t, d in rows if lo <= t < hi and t > 0]
    flat = [v for d in sel for v in d]
    rms = math.sqrt(sum(v * v for v in flat) / len(flat))
    mean = [sum(d[i] for d in sel) / len(sel) for i in range(6)]
    print("window [%.1f, %.1f): n=%d rms=%.4f error=%.5f max|mean| %.4f" % (
        lo, hi, len(sel), rms, rms / 10, max(abs(x) for x in mean)))
