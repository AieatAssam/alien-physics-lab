"""Discrimination check on P-0013's A-A claim: scaled (S_AA = 0.753) vs unscaled (S_AA = 1) coefficient.

Uses lab-vernier's own in-domain runs 2026-11-23 r3/001-004 (A-A, separation 1.5, at rest, T = 0.4).
The paper model is loaded unchanged, then its A-A coefficient is replaced in memory for the unscaled variant.
Run from repo root: python3 -I <this file>.
"""
import importlib.util, json, math, os
ROOT = os.getcwd()
spec = importlib.util.spec_from_file_location("p0013", os.path.join(ROOT, "papers/P-0013/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
L = 10.0

def err(predicted_samples, res):
    pred = {round(s["t"], 9): s for s in predicted_samples}
    se, n = 0.0, 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t not in pred: continue
        for p in s["particles"]:
            q = pred[t]["particles"][p["id"]]
            se += (p["pos"][0] - q["pos"][0]) ** 2 + (p["pos"][1] - q["pos"][1]) ** 2; n += 2
    return math.sqrt(se / n) / L

base_coup = dict(m.COUP)
for i in range(1, 5):
    rid = f"2026-11-23/r3/lab-vernier/{i:03d}"
    req = json.load(open(os.path.join(ROOT, "requests", rid + ".json")))
    res = json.load(open(os.path.join(ROOT, "results", rid + ".json")))
    m.COUP = dict(base_coup)
    scaled = err(m.predict(req["setup"]), res)
    m.COUP = dict(base_coup); m.COUP[("A", "A")] = 18.0
    unscaled = err(m.predict(req["setup"]), res)
    m.COUP = dict(base_coup); m.COUP[("A", "A")] = 13.55 * 1.0  # same as scaled; control
    print(json.dumps(dict(run=f"r3/{i:03d}", scaled_AA_0753=round(scaled, 5), unscaled_AA_1=round(unscaled, 5),
                          bar=0.03, null_note="see notebook: null (K=0) near 0.028 at T 0.4")), flush=True)
