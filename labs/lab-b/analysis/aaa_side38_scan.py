"""Scan a scale factor on P-0007's A-A coefficient for lab-b run 2026-11-20/r1/lab-b/006 (A,A,A side 3.8).
Also prints measured vs predicted mean pairwise separation over time, to see whether the miss is a rate or a shape error.
Usage: python3 -I aaa_side38_scan.py <P-0007 model.py> <request.json> <result.json>
"""
import importlib.util, json, math, sys
spec = importlib.util.spec_from_file_location("p0007", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
req = json.load(open(sys.argv[2])); res = json.load(open(sys.argv[3]))
setup = req["setup"]
seps = [math.dist(p["pos"], q["pos"]) for i, p in enumerate(setup["particles"]) for q in setup["particles"][i+1:]]
side = sum(seps)/len(seps)
base = m.COUP[("A", "A")]

def run(f):
    m.R0 = side
    m.COUP[("A", "A")] = base * f
    pred = m.predict(setup)
    sq = n = 0
    for ps, pm in zip(res["samples"], pred):
        for obs in ps["particles"]:
            for k in range(2):
                d = obs["pos"][k] - pm["particles"][obs["id"]]["pos"][k]
                sq += d*d; n += 1
    return math.sqrt(sq/n), pred

best = None
for i in range(0, 41):
    f = 0.80 + 0.01*i
    rms, _ = run(f)
    if best is None or rms < best[1]:
        best = (f, rms)
print("scan A-A factor 0.80..1.20: best f=%.2f (K=%.2f) rms=%.4f  error=rms/L=%.5f"
      % (best[0], base*best[0], best[1], best[1]/10))
print("f=1.00 (P-0007 as published): rms=%.4f" % run(1.0)[0])
rms, pred = run(best[0])
print("t, measured mean sep, predicted mean sep (at best f)")
for ps, pm in zip(res["samples"], pred):
    if round(ps["t"]*100) % 25 == 0:
        ms = [math.dist(ps["particles"][i]["pos"], ps["particles"][j]["pos"]) for i in range(3) for j in range(i+1,3)]
        ps_ = [math.dist(pm["particles"][i]["pos"], pm["particles"][j]["pos"]) for i in range(3) for j in range(i+1,3)]
        print("%.2f  %.3f  %.3f" % (ps["t"], sum(ms)/3, sum(ps_)/3))
