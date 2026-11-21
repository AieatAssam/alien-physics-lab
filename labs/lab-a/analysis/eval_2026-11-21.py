"""lab-a, 2026-11-21 round 1 analysis.

(1) Reviews: evaluates the round-3 review runs of 2026-11-20 against P-0010 and P-0011 model.py, using the
    editor's metric (RMSE of predicted positions over matched (t, id), divided by L = 10) and the claim domain.
(2) Research: separation-profile fit of one pair coefficient K (P = 2.5 fixed) for the pre-registered runs
    2026-11-20/r2/lab-a/001, r3/002 (C-C at 3), r3/003, r3/004 (A-A at 1.0), r3/005 and r1/004 (B-B at 2),
    and r3/001 (grant, C-C at 2).

Usage: python3 -I eval_2026-11-21.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

root = sys.argv[1]
L = 10.0


def load_json(*parts):
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


def traj_error(pred, truth, side=L):
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


def claims_for(pid):
    return load_json("papers", pid, "claim.json")["claims"]


print("== (1) REVIEW RUNS")
review_ids = {
    "P-0010": ["2026-11-20/r3/lab-a/%03d" % i for i in range(6, 10)],
    "P-0011": ["2026-11-20/r3/lab-a/%03d" % i for i in range(10, 13)],
}
for pid, rids in review_ids.items():
    model = load_model(pid)
    for rid in rids:
        _, _, _, n = rid.split("/")
        req = load_json("requests", *rid.split("/")[:3], n + ".json")
        res = load_json("results", *rid.split("/")[:3], n + ".json")
        setup = req["setup"]
        doms = [c for c in claims_for(pid) if in_domain(c["domain"], setup)]
        pe = doms[0]["predicted_error"] if doms else None
        try:
            pred = model.predict(setup)
            err = traj_error(pred, res["samples"])
            err_s = "%.5f" % err if err is not None else "None"
        except ValueError as e:
            err, err_s = None, "ValueError: %s" % e
        sp = [p["species"] for p in setup["particles"]]
        ds = [round(math.dist(a["pos"], b["pos"]), 3) for i, a in enumerate(setup["particles"])
              for b in setup["particles"][i + 1:]]
        print("%s %s status=%s account=%s cites=%s species=%s r0=%s dur=%s dt=%s in_domain=%s pe=%s err/L=%s ok=%s"
              % (pid, rid, res["status"], req["account"], req.get("cites_paper"), sp, ds, setup["duration"],
                 setup["sample_dt"], bool(doms), pe, err_s,
                 (err is not None and pe is not None and err <= 3 * pe)))

print()
print("== (2) RESEARCH RUNS, separation-profile fit of K (P = 2.5 fixed)")


def sep_series(rid):
    _, r, lab, n = rid.split("/")
    res = load_json("results", "2026-11-20", r, lab, n + ".json")
    out = []
    for s in res["samples"]:
        b = {p["id"]: p["pos"] for p in s["particles"]}
        out.append((s["t"], math.hypot(b[0][0] - b[1][0], b[0][1] - b[1][1])))
    return out


def relpath(K, r0, times, P=2.5, h=1e-4):
    f = lambda x: -2.0 * K / max(x, 1e-4) ** P
    r, v, t = r0, 0.0, 0.0
    out = []
    for T in times:
        while t < T - 1e-12:
            s = min(h, T - t)
            k1r, k1v = v, f(r)
            r2, v2 = r + s / 2 * k1r, v + s / 2 * k1v
            k2r, k2v = v2, f(r2)
            r3, v3 = r + s / 2 * k2r, v + s / 2 * k2v
            k3r, k3v = v3, f(r3)
            r4, v4 = r + s * k3r, v + s * k3v
            k4r, k4v = v4, f(r4)
            r += s / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
            v += s / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            t += s
        out.append(r)
    return out


def true_r0(rid):
    _, r, lab, n = rid.split("/")
    req = load_json("requests", "2026-11-20", r, lab, n + ".json")
    a, b = req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"]
    return math.dist(a, b)


def fit_K(rid, Kguess):
    ser = sep_series(rid)
    times = [t for t, _ in ser]
    meas = [m for _, m in ser]
    r0 = true_r0(rid)  # the setup separation, not the noisy first sample

    def rms(K):
        m = relpath(K, r0, times, h=1e-4)
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(meas, m)) / len(meas))

    k_coarse = min((Kguess * (0.5 + 0.01 * i) for i in range(101)), key=rms)
    k_fit = min((k_coarse + 0.002 * Kguess * (j - 25) for j in range(51)), key=rms)
    return {"rid": rid, "r0": round(r0, 4), "T": times[-1], "n": len(meas), "K_fit": round(k_fit, 3),
            "rms_fit": round(rms(k_fit), 4), "sep_end": round(meas[-1], 4),
            "min_meas": round(min(meas), 4), "times": times, "meas": meas}


runs = {
    "CC_r0=3 (r2/001)": ("2026-11-20/r2/lab-a/001", 12.36),
    "CC_r0=3 replicate (r3/002)": ("2026-11-20/r3/lab-a/002", 12.36),
    "AA_r0=1 (r3/003)": ("2026-11-20/r3/lab-a/003", 18.0),
    "AA_r0=1 (r3/004)": ("2026-11-20/r3/lab-a/004", 18.0),
    "BB_r0=2 replicate (r3/005)": ("2026-11-20/r3/lab-a/005", 6.12),
    "BB_r0=2 earlier (r1/004)": ("2026-11-20/r1/lab-a/004", 6.12),
    "CC_r0=2 grant (r3/001)": ("2026-11-20/r3/lab-a/001", 12.36),
}
fits = {}
for name, (rid, Kg) in runs.items():
    try:
        f = fit_K(rid, Kg)
    except (OSError, KeyError) as e:
        print("%-30s skipped (%s)" % (name, e))
        continue
    fits[name] = f
    print("%-30s r0=%.3f T=%.3f n=%d K_fit=%.3f rms=%.4f sep_end=%.4f min=%.4f"
          % (name, f["r0"], f["T"], f["n"], f["K_fit"], f["rms_fit"], f["sep_end"], f["min_meas"]))
    print("   K_fit / Kflat - 1 = %+.3f" % (f["K_fit"] / Kg - 1))

with open(os.path.join(root, "out", "labs", "lab-a", "analysis", "fits_2026-11-21.json"), "w") as fh:
    json.dump({k: {kk: vv for kk, vv in v.items() if kk not in ("times", "meas")} for k, v in fits.items()},
              fh, indent=1)
