"""Windowed judged RMSE/L for lab-c research runs vs ungated P-0026 law (lab-c analysis only)."""
import json, math, sys
sys.path.insert(0, sys.argv[1] + "/labs/lab-c/analysis")
import law_ungated as law
REPO = sys.argv[1]
L = 10.0
def windowed(rid, tmax):
    req = json.load(open(f"{REPO}/requests/{rid}.json"))
    res = json.load(open(f"{REPO}/results/{rid}.json"))
    setup = req["setup"]
    pred = law.predict(setup)
    se = n = 0
    for p, m in zip(pred, res["samples"]):
        if m["t"] > tmax + 1e-9: break
        for i in range(2):
            for c in range(2):
                e = p["particles"][i]["pos"][c] - m["particles"][i]["pos"][c]
                se += e * e; n += 1
    return math.sqrt(se / n) / L if n else float("nan")
for rid in sys.argv[2:]:
    print(rid, " ".join(f"t<={t}: {windowed(rid, t):.5f}" for t in (0.3, 0.5, 0.6, 0.8, 1.0, 1.5)))
