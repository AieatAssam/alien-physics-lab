"""lab-a, 2026-11-20 round 2: score round-1 runs.

(a) close-range pair runs 001-004 against the pre-registered trajectories
    (labs/lab-a/analysis/pred_2026-11-20_<tag>.json, written before results).
(b) review runs 005-009 against P-0008's predictor (papers/P-0008/model.py),
    error = RMSE(predicted vs measured positions) / L, L = 10.

Usage: python3 -I check_r1_2026-11-20.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

root = sys.argv[1]
DATE = "2026-11-20"
RUNS_CLOSE = [("001", "AA_r2"), ("002", "AA_r2_rep"), ("003", "AA_r1p5"), ("004", "BB_r2")]
RUNS_REVIEW = ["005", "006", "007", "008", "009"]
L = 10.0


def load(path):
    with open(path) as fh:
        return json.load(fh)


def result(i):
    return load(os.path.join(root, "results", DATE, "r1", "lab-a", i + ".json"))


def request(i):
    return load(os.path.join(root, "requests", DATE, "r1", "lab-a", i + ".json"))


def measured(res, ids):
    """Return list over samples of [[x,y] per id in ids]."""
    out = []
    for s in res["samples"]:
        byid = {p["id"]: p["pos"] for p in s["particles"]}
        out.append([byid[k] for k in ids])
    return out


def min_sep(traj):
    best = float("inf")
    for frame in traj:
        d = math.hypot(frame[0][0] - frame[1][0], frame[0][1] - frame[1][1])
        best = min(best, d)
    return best


print("== (a) close-range pair runs vs pre-registered prediction")
for i, tag in RUNS_CLOSE:
    res = result(i)
    pred = load(os.path.join(root, "labs", "lab-a", "analysis", "pred_2026-11-20_%s.json" % tag))
    meas = measured(res, [0, 1])
    P = pred["samples_pos"]
    n = min(len(meas), len(P))
    sq = []
    for a in range(n):
        for k in range(2):
            for p in range(2):
                sq.append((meas[a][p][k] - P[a][p][k]) ** 2)
    rms = math.sqrt(sum(sq) / len(sq))
    # zero-force null: each particle stays at its start
    null = []
    for a in range(n):
        for k in range(2):
            for p in range(2):
                null.append((meas[a][p][k] - P[0][p][k]) ** 2)
    null_rms = math.sqrt(sum(null) / len(null))
    sp_meas_end = math.hypot(meas[-1][0][0] - meas[-1][1][0], meas[-1][0][1] - meas[-1][1][1])
    sp_pred_end = math.hypot(P[-1][0][0] - P[-1][1][0], P[-1][0][1] - P[-1][1][1])
    verdict = "supported" if rms <= 0.07 else ("refuted" if rms > 0.12 else "inconclusive")
    print("%s %-10s n=%d rms=%.4f null=%.4f min_sep_meas=%.4f sep_end_meas=%.4f sep_end_pred=%.4f events=%d -> %s"
          % (i, tag, n, rms, null_rms, min_sep(meas), sp_meas_end, sp_pred_end, len(res.get("events", [])), verdict))

print("== (b) review runs vs P-0008 predictor")
spec = importlib.util.spec_from_file_location("p0008", os.path.join(root, "papers", "P-0008", "model.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for i in RUNS_REVIEW:
    req = request(i)
    res = result(i)
    setup = req["setup"]
    ids = list(range(len(setup["particles"])))
    pred_samples = mod.predict(setup)
    meas = res["samples"]
    if len(meas) != len(pred_samples):
        print(i, "sample count mismatch", len(meas), len(pred_samples))
    sq = []
    per_part = {p: [] for p in ids}
    resid_mean = {p: [0.0, 0.0] for p in ids}
    n = 0
    for ms, ps in zip(meas, pred_samples):
        mb = {q["id"]: q["pos"] for q in ms["particles"]}
        pb = {q["id"]: q["pos"] for q in ps["particles"]}
        for p in ids:
            for k in range(2):
                d = mb[p][k] - pb[p][k]
                sq.append(d * d)
                per_part[p].append(d)
                resid_mean[p][k] += d
            n += 1
    rmse = math.sqrt(sum(sq) / len(sq))
    nsamp = len(meas)
    rms_per_coord = rmse
    mean_res = {p: [round(resid_mean[p][k] / nsamp, 4) for k in range(2)] for p in ids}
    ptc_max_mean = max(abs(v) for p in ids for v in mean_res[p])
    # pair separations at t=0 (domain check)
    pos0 = [q["pos"] for q in setup["particles"]]
    seps = [math.hypot(pos0[b][0] - pos0[a][0], pos0[b][1] - pos0[a][1])
            for a in range(len(pos0)) for b in range(a + 1, len(pos0))]
    species = sorted(set(q["species"] for q in setup["particles"]))
    indom = (all(2.95 <= s <= 5.05 for s in seps) and len(pos0) <= 4 and set(species) <= {"A", "B", "C"})
    print("%s N=%d species=%s seps=[%.2f..%.2f] in_domain=%s  RMSE=%.4f (per-coord rms) normalized=%.4f max|mean res|=%.4f events=%d"
          % (i, len(pos0), "".join(species), min(seps), max(seps), indom, rmse, rmse / L,
             ptc_max_mean, len(res.get("events", []))))
