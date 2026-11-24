"""Judge-rule scorer for lab-vernier's own runs against another lab's paper (round 3, 2026-11-24).

Domain rule (as in the review rules): species of every particle in the claim's species list,
particle count <= max_particles, and EVERY pairwise initial distance inside r_range (exact
boundary values are accepted only if the distance is exact to 1e-12).

Error: RMSE over all samples and all particles, both coordinates, of (paper predict - measured),
divided by the chamber side L = 10. Null: the same RMSE with predicted = initial positions
(zero force, particles at rest). A run whose predict() raises is reported as refused.

Usage (run with -I; paper models are other labs' code, so run them only in this sandboxed way):
  PAPERS=<repo>/papers REQS=<repo>/requests RES=<repo>/results \
    python3 -I judge_score.py P-0012 P-0012-c1 2026-11-24/r2/lab-vernier/019 ...
"""
import importlib.util
import json
import math
import os
import sys

# -I hides the user site-packages where numpy was installed; add it back (appended, so stdlib wins).
sys.path.append(os.path.expanduser("~/.local/lib/python3.12/site-packages"))

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
PAPERS = os.environ.get("PAPERS", REPO + "/papers")
REQS = os.environ.get("REQS", REPO + "/requests")
RES = os.environ.get("RES", REPO + "/results")
L = 10.0


def load_model(pid):
    spec = importlib.util.spec_from_file_location("pm_" + pid.replace("-", "_"),
                                                  f"{PAPERS}/{pid}/model.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def domain_check(setup, dom):
    parts = setup["particles"]
    if len(parts) > dom["max_particles"]:
        return False, f"N={len(parts)} > {dom['max_particles']}"
    if not all(p["species"] in dom["species"] for p in parts):
        return False, "species"
    lo, hi = dom["r_range"]
    seps = []
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            d = math.dist(parts[i]["pos"], parts[j]["pos"])
            seps.append(d)
            if lo - 1e-12 <= d <= hi + 1e-12:
                continue
            return False, f"pair sep {d:.6f} outside [{lo},{hi}]"
    if len(parts) < 2:
        return False, "N<2"
    return True, f"ok N={len(parts)} seps [{min(seps):.4f},{max(seps):.4f}]"


def rmse_over_L(pred_by_t, res):
    se, n = 0.0, 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t not in pred_by_t:
            raise ValueError(f"no prediction at t={t}")
        for p in s["particles"]:
            q = pred_by_t[t][p["id"]]["pos"]
            se += (p["pos"][0] - q[0]) ** 2 + (p["pos"][1] - q[1]) ** 2
            n += 2
    return math.sqrt(se / n) / L


def score(model, req, res):
    pred = {round(s["t"], 9): {q["id"]: q for q in s["particles"]} for s in model.predict(req["setup"])}
    e = rmse_over_L(pred, res)
    # zero-force null: each particle stays at its initial position
    init = {p["id"]: p["pos"] for p in res["samples"][0]["particles"]}
    null_pred = {}
    for s in res["samples"]:
        null_pred[round(s["t"], 9)] = {pid: {"pos": init[pid]} for pid in init}
    null = rmse_over_L(null_pred, res)
    return e, null


def main(argv):
    pid, cid, ids = argv[0], argv[1], argv[2:]
    claim = json.load(open(f"{PAPERS}/{pid}/claim.json"))
    c = [k for k in claim["claims"] if k["claim_id"] == cid][0]
    bar = 3 * c["predicted_error"]
    model = load_model(pid)
    print(f"{pid} {cid} domain={c['domain']} predicted_error={c['predicted_error']} bar={bar:.4f}")
    for rid in ids:
        req = json.load(open(f"{REQS}/{rid}.json"))
        res = json.load(open(f"{RES}/{rid}.json"))
        if res.get("status") != "ok":
            print(rid, "status", res.get("status"))
            continue
        ok, why = domain_check(req["setup"], c["domain"])
        tag = "IN " if ok else "OUT"
        try:
            e, null = score(model, req, res)
            print(f"{rid} {tag} ({why}) err={e:.5f} {'<=bar' if e <= bar else '>bar'} null={null:.5f}"
                  f" {'null>bar' if null > bar else 'null<=bar'}")
        except ValueError as ex:
            print(f"{rid} {tag} ({why}) predict refused: {ex}")


if __name__ == "__main__":
    main(sys.argv[1:])
