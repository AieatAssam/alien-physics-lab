"""Check P-0001 model.py (lab-b) against single-A runs: lab-b r1/001 (its own evidence) and lab-c r1/001 (ours).
Loads the model with importlib from the repo file (stdlib only)."""
import importlib.util, json, math, sys
ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab/"
spec = importlib.util.spec_from_file_location("p1", ROOT + "papers/P-0001/model.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def check(lab, rid):
    req = json.load(open(ROOT + "requests/2026-11-17/r1/%s/%s.json" % (lab, rid)))
    res = json.load(open(ROOT + "results/2026-11-17/r1/%s/%s.json" % (lab, rid)))
    pred = m.predict(req["setup"])
    table = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    sq, rx, ry, worst = [], [], [], (0, 0)
    for s in res["samples"]:
        q = table[round(s["t"], 9)]
        for p in s["particles"]:
            ex, ey = p["pos"][0] - q[p["id"]][0], p["pos"][1] - q[p["id"]][1]
            rx.append(ex); ry.append(ey)
            sq.append(ex * ex + ey * ey)
            worst = max(worst, (math.hypot(ex, ey), s["t"]))
    rmse = math.sqrt(sum(sq) / len(sq))
    mx = sum(rx) / len(rx); my = sum(ry) / len(ry)
    print("%s/%s n=%d rmse %.4f (side-normalized %.4f) mean resid (%+.4f,%+.4f) max|res| %.3f at t=%.1f" % (
        lab, rid, len(sq), rmse, rmse / 10, mx, my, worst[0], worst[1]))

check("lab-b", "001")
check("lab-c", "001")
