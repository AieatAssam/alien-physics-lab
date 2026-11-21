"""lab-a, 2026-11-21 round 2 analysis (Plumbline).

(1) For every lab-a result on disk, list setup and in-domain status for P-0013, P-0014, P-0015
    and the error/L of each paper model (RMSE of predicted vs tracker positions over matched (t, id), / L = 10).
(2) Separation-profile fit of one pair coefficient K (P = 2.5 fixed) for the round-1 close-range runs
    2026-11-21/r1/lab-a/001-009, using the separation from the REQUEST setup (not a noisy sample).

Usage: python3 -I review_check_2026-11-21.py <repo_root>
"""
import glob
import importlib.util
import json
import math
import os
import sys

root = sys.argv[1]
L = 10.0


def load(*parts):
    with open(os.path.join(root, *parts)) as fh:
        return json.load(fh)


def load_model(pid):
    spec = importlib.util.spec_from_file_location("m_" + pid.replace("-", "_"),
                                                  os.path.join(root, "papers", pid, "model.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def traj_error(pred, truth):
    table = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    sq = []
    for s in truth:
        row = table.get(round(s["t"], 9), {})
        for p in s["particles"]:
            q = row.get(p["id"])
            if q is None or "pos" not in p:
                continue
            sq.append((q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2)
    return math.sqrt(sum(sq) / len(sq)) / L if sq else None


def rid_paths(rid):
    _, r, lab, n = rid.split("/")
    d = rid.split("/")[0]
    return d, r, lab, n


PAPERS = ["P-0013", "P-0014", "P-0015"]
models = {p: load_model(p) for p in PAPERS}
claims = {p: load(os.path.join("papers", p, "claim.json"))["claims"] for p in PAPERS}

print("== (1) ALL LAB-A RESULTS vs P-0013 / P-0014 / P-0015")
rows = []
for path in sorted(glob.glob(os.path.join(root, "results", "*", "*", "lab-a", "*.json"))):
    rel = os.path.relpath(path, os.path.join(root, "results"))
    d, r, lab, fn = rel.split(os.sep)[0], rel.split(os.sep)[1], rel.split(os.sep)[2], rel.split(os.sep)[3][:-5]
    rid = "%s/%s/%s/%s" % (d, r, lab, fn)
    req = load("requests", d, r, lab, fn + ".json")
    res = load("results", d, r, lab, fn + ".json")
    if res.get("status") not in (None, "ok") or not res.get("samples"):
        continue
    setup = req["setup"]
    sp = "".join(p["species"] for p in setup["particles"])
    ds = [round(math.dist(a["pos"], b["pos"]), 3) for i, a in enumerate(setup["particles"])
          for b in setup["particles"][i + 1:]]
    line = "%s N=%d sp=%s r0=%s T=%s dt=%s" % (rid, len(setup["particles"]), sp, ds,
                                             setup["duration"], setup["sample_dt"])
    hits = []
    for pid in PAPERS:
        for c in claims[pid]:
            if in_domain(c["domain"], setup):
                try:
                    err = traj_error(models[pid].predict(setup), res["samples"])
                except ValueError as e:
                    err = None
                hits.append("%s(%s) pe=%s err=%s" % (pid, c["claim_id"], c["predicted_error"],
                                                     None if err is None else "%.4f" % err))
    if hits:
        rows.append(line)
        print(line)
        for h in hits:
            print("    " + h)
