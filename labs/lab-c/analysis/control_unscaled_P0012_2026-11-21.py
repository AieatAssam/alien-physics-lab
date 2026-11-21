#!/usr/bin/env python3
"""Control: judged error of the unscaled P-0008 coefficients (all S = 1) on the six 1.5 runs used for P-0012.
Run: python3 -I control_unscaled_P0012_2026-11-21.py REPO_ROOT
"""
import importlib.util, json, math, sys
from pathlib import Path
REPO = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("p0012", REPO / "out" / "papers" / "P-0012" / "model.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mod.COUP = {k: v / mod.SCALE[k] for k, v in mod.COUP.items()}  # undo scaling -> P-0008 coefficients
RUNS = ["2026-11-20/r2/lab-c/004", "2026-11-20/r2/lab-c/005", "2026-11-20/r2/lab-c/006",
        "2026-11-20/r3/lab-c/006", "2026-11-20/r3/lab-c/008", "2026-11-20/r3/lab-c/014"]
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
for rid in RUNS:
    rq = json.loads((REPO/"requests"/(rid+".json")).read_text())
    res = json.loads((REPO/"results"/(rid+".json")).read_text())
    e = traj_error(mod.predict(rq["setup"]), res["samples"])
    print(f"{rid} unscaled judged_error={e:.5f}")
