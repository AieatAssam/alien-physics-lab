"""lab-a 2026-11-21 review scoring (Plumbline). Own files only.

For each cited request: error/L of a paper model against OUR tracker positions (RMSE of 2D position over
matched (t, id), divided by L = 10, as in the review rule), in-domain check on the claim's machine domain,
and closest measured separation (for the T = 2 failures).

Also: P-0013 with its scale factors set to 1 (is the metric able to tell the scaled and unscaled tables apart?).

Usage: python3 -I score_reviews_2026-11-21.py <repo_root>
"""
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


def rid_parts(rid):
    d, r, lab, n = rid.split("/")
    req = load("requests", d, r, lab, n + ".json")
    res = load("results", d, r, lab, n + ".json")
    return req, res


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


def min_meas_sep(truth):
    best = None
    for s in truth:
        ps = s["particles"]
        if len(ps) == 2:
            d = math.dist(ps[0]["pos"], ps[1]["pos"])
            best = d if best is None or d < best else best
    return best


def report(pid, rids, mod=None, tag=""):
    mod = mod or load_model(pid)
    claim = load("papers", pid, "claim.json")
    for rid in rids:
        req, res = rid_parts(rid)
        for c in claim["claims"]:
            ok = in_domain(c["domain"], req["setup"])
            if not ok:
                print("%s %-18s %s OUT_OF_DOMAIN" % (pid + tag, rid, c["claim_id"]))
                continue
            e = traj_error(mod.predict(req["setup"]), res["samples"])
            bar = 3 * c["predicted_error"]
            print("%s %-18s %-10s err=%.4f bar(3*pe)=%.3f %s  min_meas_sep=%.3f"
                  % (pid + tag, rid, c["claim_id"], e, bar, "PASS" if e <= bar else "FAIL",
                     min_meas_sep(res["samples"])))


if __name__ == "__main__":
    # P-0014 (keystone): all in-domain cited-or-candidate lab-a runs
    report("P-0014", ["2026-11-17/r3/lab-a/001", "2026-11-17/r3/lab-a/002", "2026-11-20/r2/lab-a/001",
                      "2026-11-20/r3/lab-a/002", "2026-11-21/r2/lab-a/008", "2026-11-21/r2/lab-a/009",
                      "2026-11-21/r2/lab-a/010"])
    # P-0013 (lab-c): replicates at r0 1.5, T 0.4
    m13 = load_model("P-0013")
    report("P-0013", ["2026-11-20/r1/lab-a/003", "2026-11-21/r2/lab-a/005", "2026-11-21/r2/lab-a/006",
                      "2026-11-21/r2/lab-a/007"])
    # P-0013 with scales set to 1 (unscaled P-0005/P-0008 table)
    m13u = load_model("P-0013")
    m13u.COUP = dict(m13u.BASE)
    report("P-0013", ["2026-11-21/r2/lab-a/005", "2026-11-21/r2/lab-a/006", "2026-11-21/r2/lab-a/007"],
           mod=m13u, tag=" (unscaled)")
    # P-0015 (lab-vernier): B-C runs at r0 1.0, and its machine domain on B-B and C-C runs
    report("P-0015", ["2026-11-21/r2/lab-a/011", "2026-11-21/r2/lab-a/012", "2026-11-21/r2/lab-a/013",
                      "2026-11-21/r1/lab-a/001", "2026-11-21/r1/lab-a/002", "2026-11-21/r1/lab-a/003",
                      "2026-11-21/r1/lab-a/004"])
