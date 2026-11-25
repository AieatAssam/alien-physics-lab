#!/usr/bin/env python3
"""Observed vs model pair separation over time for lab-c round-1 two-particle runs.
Usage: python3 -I sep_profile_2026-11-25.py REPO RID PAPER_MODULE_PATH
Prints t, observed sep (raw tracker), model sep at the same t, observed positions for particles 0 and 1.
"""
import importlib.util, json, math, sys
from pathlib import Path
REPO = Path(sys.argv[1]); RID = sys.argv[2]; MODEL = Path(sys.argv[3])
d, rnd, lab, nnn = RID.split("/")
req = json.loads((REPO/"requests"/d/rnd/lab/f"{nnn}.json").read_text())
res = json.loads((REPO/"results"/d/rnd/lab/f"{nnn}.json").read_text())
spec = importlib.util.spec_from_file_location("m", MODEL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
pred = mod.predict(req["setup"])
pm = {round(s["t"], 9): s["particles"] for s in pred}
step = max(1, len(res["samples"]) // 25)
print(RID, "n_samples", len(res["samples"]), "events", res.get("events"))
for k, s in enumerate(res["samples"]):
    if k % step and k != len(res["samples"]) - 1:
        continue
    t = round(s["t"], 9)
    o = s["particles"]
    so = math.dist(o[0]["pos"], o[1]["pos"])
    line = f"t={t:6.3f} obs_sep={so:7.4f} obs0={o[0]['pos']} obs1={o[1]['pos']}"
    if t in pm:
        p = pm[t]
        sm = math.dist(p[0]["pos"], p[1]["pos"])
        line += f" model_sep={sm:9.4f}"
    print(line)
