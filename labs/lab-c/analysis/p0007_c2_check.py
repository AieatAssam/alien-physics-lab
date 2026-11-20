"""P-0007 c2 check on 2026-11-19/r3/lab-c/001 (three A at rest, side 5, T=1.5).
Residual = measured - pair-law prediction (P-0008 model.py, A-A coefficient 18.0), per particle rms per coordinate.
Zero-force null = measured - free flight (no forces). Rule (P-0007's, pre-registered in analysis/predict_round3.py):
supported if every particle's residual rms <= 0.07 and null rms > 0.09. Run with python3 -I."""
import json, math, importlib.util, os
ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab"
spec = importlib.util.spec_from_file_location("p0008", os.path.join(ROOT, "papers/P-0008/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rid = "2026-11-19/r3/lab-c/001"
res = json.load(open(os.path.join(ROOT, "results/2026-11-19/r3/lab-c/001.json")))
req = json.load(open(os.path.join(ROOT, "requests/2026-11-19/r3/lab-c/001.json")))
pred = m.predict(req["setup"])
parts = req["setup"]["particles"]; n = len(parts)
rs = [0.0]*n; rc = [0.0]*n; cnt = [0]*n
nulls = [0.0]*n; cnull = [0]*n
for ps, pm in zip(pred, res["samples"]):
    t = pm["t"]
    for q in pm["particles"]:
        i = q["id"]
        for k in range(2):
            dpred = ps["particles"][i]["pos"][k] - q["pos"][k]
            rs[i] += dpred*dpred; cnt[i] += 1
            free = parts[i]["pos"][k] + parts[i]["vel"][k]*t
            dn = free - q["pos"][k]
            nulls[i] += dn*dn; cnull[i] += 1
per = [math.sqrt(rs[i]/cnt[i]) for i in range(n)]
nul = [math.sqrt(nulls[i]/cnull[i]) for i in range(n)]
print(rid, "samples", len(res["samples"]), "residual rms per particle", [round(x,4) for x in per])
print("zero-force null rms per particle", [round(x,4) for x in nul], "overall null", round(math.sqrt(sum(nulls)/sum(cnull)),4))
print("residual overall", round(math.sqrt(sum(rs)/sum(cnt)),4))
print("rule supported:", max(per) <= 0.07 and math.sqrt(sum(nulls)/sum(cnull)) > 0.09)
