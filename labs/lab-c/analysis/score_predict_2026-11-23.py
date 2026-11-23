#!/usr/bin/env python3
"""Judge-style score of lab-c runs against a paper's predict(setup), via the paper's own domain checks.

Usage: python3 -I score_predict_2026-11-23.py REPO_ROOT PAPER RID [RID ...]
RID like 2026-11-23/r2/lab-c/011.
Error = RMSE over matched (t, particle id, x/y) / L, L = 10 (judge metric).
A run whose setup makes predict() raise is reported as OUT_OF_DOMAIN with the message.
"""
import importlib.util, json, math, sys
from pathlib import Path

REPO = Path(sys.argv[1]); PAPER = sys.argv[2]; RIDS = sys.argv[3:]
L = 10.0
spec = importlib.util.spec_from_file_location("m", REPO / "papers" / PAPER / "model.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
claim = json.loads((REPO / "papers" / PAPER / "claim.json").read_text())["claims"][0]

for rid in RIDS:
    d, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / d / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / d / rnd / lab / f"{nnn}.json").read_text())
    setup = req["setup"]
    try:
        pred = mod.predict(setup)
    except ValueError as e:
        print(f"{rid} {PAPER}: OUT_OF_DOMAIN ({e})")
        continue
    pm = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    se = 0.0; n = 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t not in pm:
            continue
        for p in s["particles"]:
            for k in range(2):
                se += (p["pos"][k] - pm[t][p["id"]][k]) ** 2; n += 1
    dist = [math.dist(setup["particles"][i]["pos"], setup["particles"][j]["pos"])
            for i in range(len(setup["particles"])) for j in range(i + 1, len(setup["particles"]))]
    lo, hi = claim["domain"]["r_range"]
    dom = all(lo <= x <= hi for x in dist) and len(setup["particles"]) <= claim["domain"]["max_particles"]
    rmse = math.sqrt(se / n) / L
    bar = 3 * claim["predicted_error"]
    print(f"{rid} {PAPER}: n={n} RMSE/L={rmse:.5f} bar={bar:.4f} "
          f"pass={rmse <= bar} predict_ok=YES r0={dist[0]:.7f} T={setup['duration']} "
          f"strict_domain={'YES' if dom else 'NO'} acct={req['account']} cites={req.get('cites_paper')}")
