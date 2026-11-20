"""For in-domain runs: minimum measured pair separation, time of minimum, and model error by time window.
Also: does the P-0008 model stay within noise for T<=1 on each run? Run with python3 -I."""
import json, math, importlib.util, os
ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab"
spec = importlib.util.spec_from_file_location("p0008", os.path.join(ROOT, "papers/P-0008/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
IDS = ["2026-11-18/r2/lab-c/001", "2026-11-19/r1/lab-c/021", "2026-11-19/r1/lab-c/001",
       "2026-11-17/r2/lab-c/001", "2026-11-17/r2/lab-c/002", "2026-11-17/r2/lab-c/004",
       "2026-11-17/r2/lab-c/008", "2026-11-17/r2/lab-c/003", "2026-11-17/r2/lab-c/009"]
for rid in IDS:
    date, rnd, lab, num = rid.split("/")
    res = json.load(open(os.path.join(ROOT, "results", date, rnd, lab, num + ".json")))
    req = json.load(open(os.path.join(ROOT, "requests", date, rnd, lab, num + ".json")))
    pred = m.predict(req["setup"])
    n = len(req["setup"]["particles"])
    minsep, tmin = 1e9, None
    win = {}
    for ps, pm in zip(pred, res["samples"]):
        P = [q["pos"] for q in pm["particles"]]
        for a in range(n):
            for b in range(a + 1, n):
                d = math.hypot(P[b][0] - P[a][0], P[b][1] - P[a][1])
                if d < minsep: minsep, tmin = d, pm["t"]
        se = sum((ps["particles"][q["id"]]["pos"][k] - q["pos"][k]) ** 2 for q in pm["particles"] for k in range(2))
        w = min(int(pm["t"]), 9)
        win.setdefault(w, []).append(se)
    rms_by_w = {w: round(math.sqrt(sum(v) / (2 * n * len(v))), 3) for w, v in sorted(win.items())}
    print(rid, "min_meas_sep=%.2f at t=%.2f" % (minsep, tmin), "model rms by 1-unit window:", rms_by_w)
