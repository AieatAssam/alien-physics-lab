#!/usr/bin/env python3
"""Judged error (tools/editor.py traj_error, side 10) of paper models on lab-c's own runs.
Usage: python3 -I score_all.py REPO_ROOT P-0012 P-0014 P-0015 ...
For each paper: every lab-c request with a result, its in-domain claims, and judged error vs bar 3 x predicted_error.
"""
import importlib.util, json, math, sys, glob, os
from pathlib import Path
REPO = Path(sys.argv[1]); PAPERS = sys.argv[2:]
sys.path.insert(0, str(REPO / "tools"))
from domain import in_domain  # noqa
def traj_error(pred, truth, side=10.0):
    table = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    sq = []
    for s in truth:
        row = table.get(round(s["t"], 9), {})
        for p in s["particles"]:
            q = row.get(p["id"])
            if q is None or "pos" not in p: continue
            sq.append((q[0]-p["pos"][0])**2 + (q[1]-p["pos"][1])**2)
    return math.sqrt(sum(sq)/len(sq))/side if sq else None
runs = []
for rq in sorted(glob.glob(str(REPO/"requests"/"*"/"*"/"lab-c"/"*.json"))):
    rid = os.path.relpath(rq, REPO/"requests")[:-5]
    res = REPO/"results"/(rid+".json")
    if not res.exists(): continue
    r = json.loads(res.read_text())
    if r.get("status") != "ok": continue
    runs.append((rid, json.loads(Path(rq).read_text())))
for pid in PAPERS:
    spec = importlib.util.spec_from_file_location("m_"+pid.replace('-','_'), REPO/"papers"/pid/"model.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    claim = json.loads((REPO/"papers"/pid/"claim.json").read_text())
    print(f"== {pid} ({claim['lab']}) claims: " + "; ".join(f"{c['claim_id']} pe={c['predicted_error']} dom={c['domain']}" for c in claim["claims"]))
    for rid, rq in runs:
        setup = rq["setup"]
        for c in claim["claims"]:
            if not in_domain(c["domain"], setup): continue
            try: pred = mod.predict(setup)
            except ValueError as e: print(f"  {rid} refused: {e}"); continue
            err = traj_error(pred, json.loads((REPO/"results"/(rid+".json")).read_text())["samples"])
            pe = c["predicted_error"]; bar = 3*pe
            seps = [round(math.dist(a["pos"], b["pos"]),3) for i,a in enumerate(setup["particles"]) for b in setup["particles"][i+1:]]
            sp = "".join(p["species"] for p in setup["particles"])
            print(f"  {rid} {sp} seps={seps} T={setup['duration']} err={err:.5f} bar={bar:.4f} {'PASS' if err<=bar else 'FAIL'}")
