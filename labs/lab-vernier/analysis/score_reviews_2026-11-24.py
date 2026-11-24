"""Score lab-vernier's own runs against another lab's paper model (review rules).

For each request id given on the command line:
  - loads the request and the result (status must be ok),
  - checks domain: species in claim list, particle count <= max_particles,
    exactly two particles (lone-particle runs are not pair evidence), every
    pairwise initial distance inside r_range,
  - predicts positions with the paper's own predict(setup) (run through its guard),
  - error = RMSE(predicted - measured positions, all particles, both coords) / L,
    computed over all samples and over samples with t <= tmax (claim window).

Usage (run with -I; paper models are other labs' code):
  PAPERS=<repo>/papers python3 -I score_reviews_2026-11-24.py P-0013 P-0013-c1 [--tmax 0.4] id1 id2 ...
Ids are like 2026-11-23/r3/lab-vernier/001.
"""
import importlib.util
import json
import math
import os
import sys

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
PAPERS = os.environ.get("PAPERS", REPO + "/papers")
L = 10.0


def load_model(pid):
    spec = importlib.util.spec_from_file_location("paper_model_" + pid.replace("-", "_"),
                                                  f"{PAPERS}/{pid}/model.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def in_domain(setup, dom):
    parts = setup["particles"]
    if len(parts) != 2:
        return False, "N=%d (need pair)" % len(parts)
    if not all(p["species"] in dom["species"] for p in parts):
        return False, "species"
    if len(parts) > dom["max_particles"]:
        return False, "N"
    lo, hi = dom["r_range"]
    d = math.dist(parts[0]["pos"], parts[1]["pos"])
    if not (lo - 1e-9 <= d <= hi + 1e-9):
        return False, "sep %.4f" % d
    return True, "ok sep %.4f" % d


def error(model, req, res, tmax=None):
    pred = {round(s["t"], 9): s for s in model.predict(req["setup"])}
    se, n = 0.0, 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if tmax is not None and t > tmax + 1e-9:
            continue
        if t not in pred:
            continue
        for p in s["particles"]:
            q = pred[t]["particles"][p["id"]]
            se += (p["pos"][0] - q["pos"][0]) ** 2 + (p["pos"][1] - q["pos"][1]) ** 2
            n += 2
    return math.sqrt(se / n) / L if n else float("nan")


def main(argv):
    args = list(argv)
    tmax = None
    if "--tmax" in args:
        i = args.index("--tmax")
        tmax = float(args[i + 1])
        del args[i:i + 2]
    pid, cid, ids = args[0], args[1], args[2:]
    claim = json.load(open(f"{PAPERS}/{pid}/claim.json"))
    c = [k for k in claim["claims"] if k["claim_id"] == cid][0]
    bar = 3 * c["predicted_error"]
    model = load_model(pid)
    print(f"{pid} {cid} domain={c['domain']} predicted_error={c['predicted_error']} bar={bar:.4f} tmax={tmax}")
    for rid in ids:
        req = json.load(open(f"{REPO}/requests/{rid}.json"))
        res = json.load(open(f"{REPO}/results/{rid}.json"))
        if res.get("status") != "ok":
            print(rid, "status", res.get("status"))
            continue
        ok, why = in_domain(req["setup"], c["domain"])
        try:
            e_full = error(model, req, res)
            e_win = error(model, req, res, tmax) if tmax is not None else float("nan")
            tag_full = "<=bar" if e_full <= bar else ">bar"
            tag_win = ("<=bar" if e_win <= bar else ">bar") if tmax is not None else ""
            print(f"{rid} {'IN' if ok else 'OUT'} ({why}) full={e_full:.5f}{tag_full} "
                  f"win={e_win:.5f}{tag_win}" if tmax is not None else
                  f"{rid} {'IN' if ok else 'OUT'} ({why}) full={e_full:.5f}{tag_full}")
        except ValueError as ex:
            print(rid, "predict refused:", ex)


if __name__ == "__main__":
    main(sys.argv[1:])
