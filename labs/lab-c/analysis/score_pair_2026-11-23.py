#!/usr/bin/env python3
"""Score lab-c runs against a paper's own model, judge-style.

Usage: python3 -I score_pair_2026-11-23.py REPO_ROOT PAPER RID [RID ...]
  RID like 2026-11-23/r1/lab-c/001 ; PAPER like P-0022

- Replays the paper's RK4 integrator (model._step) WITHOUT its strict domain raises,
  so out-of-domain runs still get a number. The judge's domain rule is checked
  separately with exact float comparisons (r within r_range, species, count).
- Error = RMSE over matched (t, particle, coord) / L, L = 10.
"""
import importlib.util, json, math, sys
from pathlib import Path

REPO = Path(sys.argv[1]); PAPER = sys.argv[2]; RIDS = sys.argv[3:]
L = 10.0
spec = importlib.util.spec_from_file_location("m", REPO / "papers" / PAPER / "model.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
dom = json.loads((REPO / "papers" / PAPER / "claim.json").read_text())["claims"][0]["domain"]


def replay(setup):
    parts = setup["particles"]
    species = [p["species"] for p in parts]
    pos = [list(map(float, p["pos"])) for p in parts]
    vel = [list(map(float, p["vel"])) for p in parts]
    dur = float(setup["duration"]); dt = float(setup["sample_dt"])
    n = int(round(dur / dt)); out = {0.0: [list(p) for p in pos]}
    t = 0.0
    for i in range(1, n + 1):
        target = round(i * dt, 9)
        while t < target - 1e-12:
            h = min(mod.H, target - t)
            pos, vel = mod._step(pos, vel, species, h)
            t += h
        t = target
        out[target] = [list(p) for p in pos]
    return out


def domain_problems(setup):
    parts = setup["particles"]; bad = []
    if not set(p["species"] for p in parts) <= set(dom["species"]): bad.append("species")
    if len(parts) > dom["max_particles"]: bad.append("count")
    lo, hi = dom["r_range"]
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            d = math.dist(parts[i]["pos"], parts[j]["pos"])
            if not (lo <= d <= hi): bad.append("r=%.7f" % d)
    return bad


for rid in RIDS:
    d, rnd, lab, nnn = rid.split("/")
    req = json.loads((REPO / "requests" / d / rnd / lab / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results" / d / rnd / lab / f"{nnn}.json").read_text())
    setup = req["setup"]
    pred = replay(setup)
    se = 0.0; n = 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t not in pred: continue
        for p_meas, p_pred in zip(s["particles"], pred[t]):
            for k in range(2):
                se += (p_meas["pos"][k] - p_pred[k]) ** 2; n += 1
    rmse_over_L = math.sqrt(se / n) / L if n else float("nan")
    bad = domain_problems(setup)
    print(f"{rid}  cites={req.get('cites_paper','-')}  acct={req['account']}  "
          f"sep0={math.dist(setup['particles'][0]['pos'], setup['particles'][1]['pos']):.6f}  "
          f"T={setup['duration']}  n={n}  RMSE/L={rmse_over_L:.5f}  "
          f"in_domain={'YES' if not bad else 'NO '+','.join(bad)}")
