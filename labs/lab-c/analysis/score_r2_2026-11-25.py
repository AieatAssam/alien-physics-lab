"""Score lab-c round-2 results (2026-11-25/r2/lab-c/001-008) for Nullius.

001-006: pre-registered sub-3 A-A runs. Observable: raw minimum tracker separation d_obs.
         Rule (fixed before runs): TAB-consistent if d_obs < 0.25; P26-consistent if d_obs > 0.45;
         otherwise no verdict.
007-008: review-account runs cited to P-0030. RMSE/L vs P-0030 predict(), L = 10.
Run with: python3 -I score_r2_2026-11-25.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
RES = os.path.join(ROOT, "results/2026-11-25/r2/lab-c")
REQ = os.path.join(ROOT, "requests/2026-11-25/r2/lab-c")
L = 10.0


def load(path):
    with open(path) as f:
        return json.load(f)


def dmin_obs(samples):
    best = (float("inf"), None)
    for s in samples:
        p = s["particles"]
        d = math.dist(p[0]["pos"], p[1]["pos"])
        if d < best[0]:
            best = (d, s["t"])
    return best


def rule(d):
    if d < 0.25:
        return "TAB-consistent"
    if d > 0.45:
        return "P26-consistent"
    return "no verdict"


PRED = {
    "001": (0.0706, 0.594, 0.6897, 0.600),
    "002": (0.0706, 0.594, 0.6897, 0.600),
    "003": (0.0731, 0.470, 0.5106, 0.500),
    "004": (0.0731, 0.470, 0.5106, 0.500),
    "005": (0.6324, 1.000, 0.8475, 1.000),
    "006": (0.0706, 0.594, 0.6897, 0.600),
}

print("== pre-registered sub-3 runs (tracker raw minimum separation)")
for k in sorted(PRED):
    d = load(os.path.join(RES, k + ".json"))
    dobs, tmin = dmin_obs(d["samples"])
    tab, tab_t, p26, p26_t = PRED[k]
    print(f"{k} d_obs={dobs:.4f} at t={tmin:.3f} | TAB {tab:.4f}@{tab_t:.3f} P26 {p26:.4f}@{p26_t:.3f} | rule: {rule(dobs)}")

# P-0030 model (lab-vernier). Loaded from the paper directory, imports only math.
spec = importlib.util.spec_from_file_location("p0030", os.path.join(ROOT, "papers/P-0030/model.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

print()
print("== P-0030 review runs (RMSE/L vs predict(), bar = 3 x 0.008 = 0.024)")
for k in ["007", "008"]:
    req = load(os.path.join(REQ, k + ".json"))
    res = load(os.path.join(RES, k + ".json"))
    pred = mod.predict(req["setup"])
    meas = res["samples"]
    if len(pred) != len(meas):
        raise SystemExit(f"length mismatch {k}: {len(pred)} vs {len(meas)}")
    se = 0.0
    n = 0
    max_err_t = (0.0, None)
    for p, m in zip(pred, meas):
        assert abs(p["t"] - m["t"]) < 1e-9, (p["t"], m["t"])
        sq = 0.0
        for i in range(2):
            for c in range(2):
                e = p["particles"][i]["pos"][c] - m["particles"][i]["pos"][c]
                se += e * e
                sq += e * e
                n += 1
        if math.sqrt(sq / 4) > max_err_t[0]:
            max_err_t = (math.sqrt(sq / 4), m["t"])
    rmse_L = math.sqrt(se / n) / L
    # windowed
    def window(tmax):
        s2 = 0.0
        nn = 0
        for p, m in zip(pred, meas):
            if m["t"] > tmax + 1e-12:
                break
            for i in range(2):
                for c in range(2):
                    e = p["particles"][i]["pos"][c] - m["particles"][i]["pos"][c]
                    s2 += e * e
                    nn += 1
        return math.sqrt(s2 / nn) / L
    dmin_model = min(math.dist(p["particles"][0]["pos"], p["particles"][1]["pos"]) for p in pred)
    dmin_meas = dmin_obs(meas)[0]
    print(f"{k}: RMSE/L full={rmse_L:.5f}  t<=0.5={window(0.5):.5f}  t<=1.0={window(1.0):.5f}  "
          f"t<=2.0={window(2.0):.5f}  | model min sep {dmin_model:.4f}, observed raw min sep {dmin_meas:.4f}  "
          f"| worst single-sample rms error {max_err_t[0]:.4f} at t={max_err_t[1]}")
