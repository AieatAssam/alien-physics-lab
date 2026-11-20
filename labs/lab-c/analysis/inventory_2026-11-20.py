#!/usr/bin/env python3
"""Round 2 (2026-11-20) inventory of lab-c runs against papers with a model.py.

Run with: python3 -I inventory_2026-11-20.py REPO_ROOT

For every lab-c request with an ok result, it prints the setup summary and, for each
paper whose first in-domain claim matches (species, particle count, every pairwise initial
distance; same rule as tools/domain.py), the judged error computed as in tools/editor.py
(sqrt(mean over particle-samples of |dpos|^2) / 10). Off-domain pairs are not scored.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
sys.path.insert(0, str(REPO / "tools"))
from domain import in_domain  # noqa: E402  (tools/domain.py, read-only use)

SIDE = 10.0


def load_model(pid):
    path = REPO / "papers" / pid / "model.py"
    spec = importlib.util.spec_from_file_location(f"model_{pid.replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def traj_error(pred, truth, side=SIDE):
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


def min_pair_sep(samples):
    best = None
    for s in samples:
        ps = s["particles"]
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                d = math.dist(ps[i]["pos"], ps[j]["pos"])
                best = d if best is None or d < best else best
    return best


def init_seps(parts):
    out = []
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            out.append(math.dist(parts[i]["pos"], parts[j]["pos"]))
    return out


PAPERS = ["P-0005", "P-0006", "P-0007", "P-0008", "P-0009", "P-0010", "P-0011"]
MODELS = {}
CLAIMS = {}
for pid in PAPERS:
    CLAIMS[pid] = json.loads((REPO / "papers" / pid / "claim.json").read_text())["claims"]
    MODELS[pid] = load_model(pid)

rows = []
for req_path in sorted((REPO / "requests").glob("*/r*/lab-c/*.json")):
    date, rnd = req_path.parts[-4], req_path.parts[-3]
    nnn = req_path.stem
    rid = f"{date}/{rnd}/lab-c/{nnn}"
    req = json.loads(req_path.read_text())
    res_path = REPO / "results" / date / rnd / "lab-c" / f"{nnn}.json"
    res = json.loads(res_path.read_text()) if res_path.exists() else {}
    if res.get("status", "ok") != "ok" or not res_path.exists():
        continue
    setup = req["setup"]
    parts = setup["particles"]
    seps = init_seps(parts)
    row = {
        "rid": rid,
        "account": req.get("account"),
        "cites": req.get("cites_paper"),
        "species": "".join(p["species"] for p in parts),
        "n": len(parts),
        "T": setup["duration"],
        "dt": setup["sample_dt"],
        "moving": any(abs(v) > 1e-12 for p in parts for v in p["vel"]),
        "sep_init": (min(seps), max(seps)) if seps else None,
        "min_sep_traj": min_pair_sep(res["samples"]),
        "papers": {},
    }
    for pid in PAPERS:
        hit = None
        for c in CLAIMS[pid]:
            if in_domain(c["domain"], setup):
                hit = c
                break
        if hit is None:
            continue
        try:
            pred = MODELS[pid].predict(setup)
            err = traj_error(pred, res["samples"])
            row["papers"][pid] = (hit["claim_id"], hit["predicted_error"], err)
        except Exception as exc:  # model refuses the setup (e.g. duration limit)
            row["papers"][pid] = (hit["claim_id"], hit["predicted_error"], f"model-error: {exc}")
    rows.append(row)

for r in rows:
    sep = r["sep_init"]
    sep_s = f"{sep[0]:.2f}-{sep[1]:.2f}" if sep else "n/a"
    mins = r["min_sep_traj"]
    mins_s = f"{mins:.2f}" if mins is not None else "n/a"
    print(f"{r['rid']}  acct={r['account']:8s} cites={str(r['cites']):8s} sp={r['species']:6s} n={r['n']:2d} "
          f"T={r['T']:<5} dt={r['dt']:<6} moving={int(r['moving'])} initsep={sep_s:12s} minsep={mins_s}")
    for pid, (cid, pe, err) in r["papers"].items():
        if isinstance(err, str):
            print(f"      {pid} {cid}: {err}")
        else:
            verdict = "" if pe is None else ("  <=3pe" if err <= 3 * pe else "  >3pe")
            print(f"      {pid} {cid}: err={err:.5f} pe={pe}{verdict}")
