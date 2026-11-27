"""Run P-0036 model.predict on every evidence request id; report failures and judged RMSE/L (s = 1) per run."""
import json, math, sys, statistics
REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
sys.path.insert(0, f"{REPO}/out/papers/P-0036")
import model
ev = json.load(open(f"{REPO}/out/labs/lab-keystone/analysis/evidence_P0036_2026-11-27.json"))["evidence"]
L = 10.0
errs = []; fails = []
for rid in ev:
    d, r, lab, n = rid.split("/")
    req = json.load(open(f"{REPO}/requests/{d}/{r}/{lab}/{n}.json"))
    res = json.load(open(f"{REPO}/results/{d}/{r}/{lab}/{n}.json"))
    try:
        pred = model.predict(req["setup"])
    except ValueError as e:
        fails.append((rid, str(e))); continue
    pm = {round(s["t"], 9): s for s in pred}
    sq = 0.0; cnt = 0
    for smp in res["samples"]:
        ps = pm[round(smp["t"], 9)]["particles"]
        for q, pp in zip(smp["particles"], ps):
            for c in range(2):
                sq += (q["pos"][c] - pp["pos"][c]) ** 2; cnt += 1
    errs.append(math.sqrt(sq / cnt) / L)
print("evidence ids:", len(ev), " predict failures:", len(fails))
for f in fails: print("  FAIL", f)
print("RMSE/L: min %.5f  median %.5f  max %.5f" % (min(errs), statistics.median(errs), max(errs)))
print("runs over 3x0.007 = 0.021:", sum(e > 0.021 for e in errs))
