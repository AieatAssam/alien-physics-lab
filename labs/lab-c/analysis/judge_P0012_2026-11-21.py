#!/usr/bin/env python3
"""Judged error (tools/editor.py traj_error) of out/papers/P-0012/model.py on the 1.5 pair runs.
Run: python3 -I judge_P0012_2026-11-21.py REPO_ROOT
Runs: r2 004 (AA), r2 005 (AC), r2 006 (CC), r3 006 (AA), r3 008 (AC), r3 014 (CC). Side 10. Bar = 3 x 0.01.
"""
import importlib.util, json, math, sys
from pathlib import Path
REPO = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("p0012", REPO / "out" / "papers" / "P-0012" / "model.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
RUNS = [("2026-11-20/r2/lab-c/004", "AA"), ("2026-11-20/r2/lab-c/005", "AC"), ("2026-11-20/r2/lab-c/006", "CC"),
        ("2026-11-20/r3/lab-c/006", "AA"), ("2026-11-20/r3/lab-c/008", "AC"), ("2026-11-20/r3/lab-c/014", "CC")]

def traj_error(pred, truth, side=10.0):
    table = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    sq = []
    for s in truth:
        row = table.get(round(s["t"], 9), {})
        for p in s["particles"]:
            q = row.get(p["id"])
            if q is None: continue
            sq.append((q[0]-p["pos"][0])**2 + (q[1]-p["pos"][1])**2)
    return math.sqrt(sum(sq)/len(sq))/side

for rid, pair in RUNS:


    rq = json.loads((REPO/"requests"/(rid.replace("/", "/", ) + ".json")).read_text()) if (REPO/"requests"/(rid+".json")).exists() else None
    res = json.loads((REPO/"results"/(rid+".json")).read_text())
    if rq is None:
        print(rid, "no request file"); continue
    try:
        pred = mod.predict(rq["setup"])
    except ValueError as e:
        print(rid, "refused:", e); continue
    e = traj_error(pred, res["samples"])
    print(f"{rid} {pair} judged_error={e:.5f}  bar(3x0.01)=0.03  {'PASS' if e<=0.03 else 'FAIL'}")
