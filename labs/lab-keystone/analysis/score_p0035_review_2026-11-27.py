"""Score lab-keystone review-account runs 004-007 against P-0035 model.py (judged RMSE/L)."""
import importlib.util, json, math, sys

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
L = 10.0
PRED_ERR = 0.006
BAR = 3 * PRED_ERR

spec = importlib.util.spec_from_file_location("p0035", REPO + "/papers/P-0035/model.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def rmse_over_L(setup, result):
    pred = m.predict(setup)
    pred_by_t = {round(s["t"], 9): s for s in pred}
    sq, n = 0.0, 0
    matched = 0
    for s in result["samples"]:
        t = round(s["t"], 9)
        if t not in pred_by_t:
            continue
        matched += 1
        for obs, p in zip(s["particles"], pred_by_t[t]["particles"]):
            for k in range(2):
                d = obs["pos"][k] - p["pos"][k]
                sq += d * d
                n += 1
    return math.sqrt(sq / n) / L, matched, n

rows = []
for rid in ["004", "005", "006", "007"]:
    req = json.load(open(f"{REPO}/requests/2026-11-27/r1/lab-keystone/{rid}.json"))
    res = json.load(open(f"{REPO}/results/2026-11-27/r1/lab-keystone/{rid}.json"))
    assert res["status"] == "ok", (rid, res.get("reason"))
    e, matched, n = rmse_over_L(req["setup"], res)
    parts = req["setup"]["particles"]
    r0 = math.dist(parts[0]["pos"], parts[1]["pos"])
    rows.append((rid, r0, e, matched, n, res["cost"]))
    print(f"{rid}  r0={r0:.4f}  RMSE/L={e:.5f}  samples_matched={matched}  coords={n}  cost={res['cost']}  "
          f"{'PASS' if e <= BAR else 'ABOVE BAR'} (bar {BAR:.3f})")

n_pass = sum(1 for r in rows if r[2] <= BAR)
print("runs at or below bar:", n_pass, "of", len(rows))
print("all in-domain runs above bar (falsified rule):", all(r[2] > BAR for r in rows))
