"""Sensitivity of P-0026's judged RMSE/L to its coefficient G, on lab-b review runs 006-009.
Loads P-0026 model.py, scales G by factors, reports RMSE/L against measured positions (0 < t <= 0.3).
Usage: python3 -I p0026_G_sensitivity_2026-11-24.py <repo_root> <paper_dir>
"""
import sys, json, math, os, importlib.util
L = 10.0
root, paper_dir = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("m", os.path.join(paper_dir, "model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
G0 = m.G
for n in ["006", "007", "008", "009"]:
    suf = f"2026-11-24/r2/lab-b/{n}"
    req = json.load(open(os.path.join(root, "requests", suf + ".json")))
    res = json.load(open(os.path.join(root, "results", suf + ".json")))
    pos0 = [p["pos"] for p in req["setup"]["particles"]]
    row = []
    for f in [0.0, 0.95, 1.0, 1.05]:
        m.G = G0 * f
        pred = {round(s["t"], 9): s for s in m.predict(req["setup"])}
        sq = cnt = 0
        for s in res["samples"]:
            t = round(s["t"], 9)
            if not (0 < t <= 0.3 + 1e-9):
                continue
            mp = {q["id"]: q["pos"] for q in pred[t]["particles"]}
            for q in s["particles"]:
                for k in range(2):
                    sq += (mp[q["id"]][k] - q["pos"][k]) ** 2; cnt += 1
        row.append(f"G x{f}: {math.sqrt(sq / cnt) / L:.5f}")
    print(suf, " | ".join(row))
