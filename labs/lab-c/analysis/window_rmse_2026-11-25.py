#!/usr/bin/env python3
"""Judge-style RMSE/L restricted to sample times t <= tmax, for a run vs a paper model.
Usage: python3 -I window_rmse_2026-11-25.py REPO MODEL_PATH RID [RID...]
Prints, per run: RMSE/L over t<=0.6, t<=1.0, t<=1.2, t<=full; min observed sep; first t where model sep > 1.0 blow-up.
"""
import importlib.util, json, math, sys
from pathlib import Path
REPO = Path(sys.argv[1]); MODEL = Path(sys.argv[2]); RIDS = sys.argv[3:]
L = 10.0
spec = importlib.util.spec_from_file_location("m", MODEL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
for rid in RIDS:
    d, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO/"requests"/d/rnd/lab/f"{nnn}.json").read_text())
    res = json.loads((REPO/"results"/d/rnd/lab/f"{nnn}.json").read_text())
    pred = mod.predict(req["setup"])
    pm = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    out = []
    minsep_obs = min(math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in res["samples"])
    blow = None
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t in pm:
            ms = math.dist(pm[t][0], pm[t][1])
            if ms > 10 and blow is None:
                blow = t
    for tmax in (0.6, 1.0, 1.2, 99):
        se = 0.0; n = 0
        for s in res["samples"]:
            t = round(s["t"], 9)
            if t > tmax or t not in pm: continue
            for p in s["particles"]:
                for k in range(2):
                    se += (p["pos"][k] - pm[t][p["id"]][k]) ** 2; n += 1
        out.append(f"t<={tmax if tmax<99 else 'end'}: {math.sqrt(se/n)/L:.5f}" if n else "n/a")
    print(f"{rid} minobs_sep={minsep_obs:.3f} model_blowup_t={blow} | " + " | ".join(out))
