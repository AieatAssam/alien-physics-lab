"""lab-a scoring, round 1 of 2026-11-27 (Plumbline).

Modes (python3 -I score_2026-11-27.py <repo_root> <mode>):
  asym   : pre-registered R rule on requests 2026-11-26/r2/lab-a/001-004 (A-C, A-B, A-A control).
  calib  : judged RMSE/L of the P-0035 predictor against lab-c's own published run
           2026-11-25/r2/lab-c/001 (judge bar for the claim: published 0.00509).
  screen : judged RMSE/L of P-0035 on every lab-a run that lies inside P-0035's domain.

Judged RMSE/L (my reading, checked by calib): sqrt(mean over samples, particles, coords of
(pred - meas)^2) / L with L = 10. Pure stdlib; no numpy needed.
"""
import glob
import importlib.util
import json
import math
import os
import sys

ROOT = sys.argv[1]
MODE = sys.argv[2]
L = 10.0


def load_json(p):
    with open(p) as f:
        return json.load(f)


def load_model(path):
    spec = importlib.util.spec_from_file_location("p0035", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rmse_over_L(pred, samples):
    """pred: list of samples from predict(); samples: list from the result file."""
    pm = {round(s["t"], 9): s for s in pred}
    sq = 0.0
    n = 0
    for s in samples:
        key = round(s["t"], 9)
        if key not in pm:
            raise KeyError("time %r not in prediction" % key)
        for p_meas, p_pred in zip(s["particles"], pm[key]["particles"]):
            for k in range(2):
                d = p_pred["pos"][k] - p_meas["pos"][k]
                sq += d * d
                n += 1
    return math.sqrt(sq / n) / L, n


def in_p0035_domain(setup):
    parts = setup["particles"]
    if len(parts) != 2:
        return False, "N"
    if any(p["species"] != "A" for p in parts):
        return False, "species"
    if any(c != 0.0 for p in parts for c in p["vel"]):
        return False, "velocity"
    r0 = math.dist(parts[0]["pos"], parts[1]["pos"])
    if not (2.0 - 1e-9 <= r0 <= 2.75 + 1e-9):
        return False, "r0=%.4f" % r0
    if any(not (2.0 <= c <= L - 2.0) for p in parts for c in p["pos"]):
        return False, "wall"
    if float(setup["duration"]) > 0.6 + 1e-12:
        return False, "T"
    return True, "ok r0=%.4f" % r0


def mode_asym():
    reqs = {}
    for n in ["001", "002", "003", "004"]:
        req = load_json(os.path.join(ROOT, "requests/2026-11-26/r2/lab-a/%s.json" % n))
        res = load_json(os.path.join(ROOT, "results/2026-11-26/r2/lab-a/%s.json" % n))
        reqs[n] = (req, res)
    out = {}
    for n, (req, res) in reqs.items():
        setup = req["setup"]
        x0 = [p["pos"] for p in setup["particles"]]
        spp = [p["species"] for p in setup["particles"]]
        T = setup["duration"]
        # three windows for a time profile; the pre-registered window is [T-0.2, T]
        windows = {"early[0.2,0.4]": (0.2, 0.4), "mid[0.5,0.7]": (0.5, 0.7), "late[0.8,1.0]": (0.8, 1.0)}
        row = {"species": spp, "status": res.get("status"), "budget_remaining": res.get("budget_remaining")}
        for wname, (a, b) in windows.items():
            sel = [s for s in res["samples"] if a - 1e-9 <= s["t"] <= b + 1e-9]
            disp = []
            for i in range(2):
                mx = sum(s["particles"][i]["pos"][0] for s in sel) / len(sel)
                my = sum(s["particles"][i]["pos"][1] for s in sel) / len(sel)
                dx, dy = mx - x0[i][0], my - x0[i][1]
                disp.append(math.hypot(dx, dy))
            row[wname] = {"n": len(sel), "d_particle0": disp[0], "d_particle1": disp[1],
                          "R_0_over_1": disp[0] / disp[1] if disp[1] > 0 else float("nan")}
        out[n] = row
    return out


def mode_calib():
    req = load_json(os.path.join(ROOT, "requests/2026-11-25/r2/lab-c/001.json"))
    res = load_json(os.path.join(ROOT, "results/2026-11-25/r2/lab-c/001.json"))
    model = load_model(os.path.join(ROOT, "papers/P-0035/model.py"))
    pred = model.predict(req["setup"])
    score, n = rmse_over_L(pred, res["samples"])
    return {"request": req["request_id"], "judged_rmse_over_L": score, "n_values": n,
            "published_by_lab_c": 0.00509}


def mode_screen():
    model = load_model(os.path.join(ROOT, "papers/P-0035/model.py"))
    rows = []
    for rp in sorted(glob.glob(os.path.join(ROOT, "requests/*/r*/lab-a/*.json"))):
        req = load_json(rp)
        ok, why = in_p0035_domain(req["setup"])
        if not ok:
            continue
        date_round = rp.split("requests/")[1].rsplit("/lab-a/", 1)[0]
        resp = rp.replace("/requests/", "/results/")
        if not os.path.exists(resp):
            rows.append((req["request_id"], why, "no result", None, None))
            continue
        res = load_json(resp)
        pred = model.predict(req["setup"])
        score, n = rmse_over_L(pred, res["samples"])
        rows.append((req["request_id"], why, req["account"], req["setup"]["duration"], score))
    return rows


if __name__ == "__main__":
    if MODE == "asym":
        print(json.dumps(mode_asym(), indent=1))
    elif MODE == "calib":
        print(json.dumps(mode_calib(), indent=1))
    elif MODE == "screen":
        for r in mode_screen():
            print(r)
    else:
        raise SystemExit("unknown mode")
