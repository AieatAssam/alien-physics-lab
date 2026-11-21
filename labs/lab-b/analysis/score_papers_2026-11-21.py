"""Score lab-b runs against papers under review, mirroring tools/editor.py traj_error and tools/domain.py.

Usage: python3 -I score_papers_2026-11-21.py REPO P-0012 [P-0013 ...]
Prints, per paper, every lab-b ok run: in-domain flag, judge-style RMSE/L, and whether it is under 3 x predicted_error.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

repo = Path(sys.argv[1])
papers = sys.argv[2:]
L = 10.0


def in_domain(domain, setup):
    parts = setup["particles"]
    if len(parts) > domain["max_particles"]:
        return False
    if any(p["species"] not in domain["species"] for p in parts):
        return False
    lo, hi = domain["r_range"]
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            if not lo <= math.dist(a["pos"], b["pos"]) <= hi:
                return False
    return True


def traj_error(pred, truth, side):
    table = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    sq = []
    for s in truth:
        row = table.get(round(s["t"], 9), {})
        for p in s["particles"]:
            q = row.get(p["id"])
            if q is None or "pos" not in p:
                continue
            sq.append((q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2)
    return math.sqrt(sum(sq) / len(sq)) / side if sq else None


def load_model(path):
    spec = importlib.util.spec_from_file_location("model_" + path.parent.name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


runs = sorted(repo.glob("results/*/r*/lab-b/*.json"))
for pid in papers:
    pdir = repo / "papers" / pid
    claim = json.loads((pdir / "claim.json").read_text())
    mod = load_model(pdir / "model.py")
    print(f"=== {pid}: {claim['title']}")
    for c in claim["claims"]:
        print(f"  {c['claim_id']} pe={c['predicted_error']} domain={c['domain']} bar={3*c['predicted_error']:.4f}")
    for res_path in runs:
        res = json.loads(res_path.read_text())
        if res.get("status") != "ok":
            continue
        rid = res["request_id"]
        req = json.loads((repo / "requests" / f"{rid}.json").read_text())
        setup = req["setup"]
        acct = req.get("account")
        cites = req.get("cites_paper", "")
        seps = [round(math.dist(setup["particles"][i]["pos"], setup["particles"][j]["pos"]), 4)
                for i in range(len(setup["particles"])) for j in range(i + 1, len(setup["particles"]))]
        species = "".join(p["species"] for p in setup["particles"])
        for c in claim["claims"]:
            if not in_domain(c["domain"], setup):
                continue
            try:
                pred = mod.predict(setup)
            except Exception:
                pred = None
            err = traj_error(pred, res["samples"], L) if isinstance(pred, list) else None
            ok = err is not None and err <= 3 * c["predicted_error"]
            print(f"  {rid} {species} seps={seps} T={setup['duration']} acct={acct} cites={cites} "
                  f"err={'None' if err is None else format(err, '.5f')} under_bar={ok}")
