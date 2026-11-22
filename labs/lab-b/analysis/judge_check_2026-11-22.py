"""Judge-style RMSE/L of a predictor against stored runs. Usage: python3 -I judge_check_2026-11-22.py REPO MODEL_PY RID [RID ...]"""
import importlib.util, json, math, sys
from pathlib import Path
REPO, MODEL = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("m", MODEL)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
def traj_error(pred, truth, side=10.0):
    table = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    sq = []
    for s in truth:
        row = table.get(round(s["t"], 9), {})
        for p in s["particles"]:
            q = row.get(p["id"])
            if q is None or "pos" not in p:
                continue
            sq.append((q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2)
    return math.sqrt(sum(sq) / len(sq)) / side
for rid in sys.argv[3:]:
    res = json.loads((REPO / "results" / f"{rid}.json").read_text())
    setup = json.loads((REPO / "requests" / f"{rid}.json").read_text())["setup"]
    try:
        err = "%.5f" % traj_error(mod.predict(setup), res["samples"])
    except Exception as e:
        err = "raises: %s" % e
    print(rid, "".join(p["species"] for p in setup["particles"]), "T=%s" % setup["duration"], err)
