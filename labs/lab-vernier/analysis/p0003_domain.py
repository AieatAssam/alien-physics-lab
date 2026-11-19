"""P-0003 domain check: residuals of its own model on lab-a's sep-3 and sep-4 runs, and min separations."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fit_tools import load_json, load_model, model_residuals, rms
R = "/home/runner/work/alien-physics-lab/alien-physics-lab"
m = load_model(os.path.join(R, "papers/P-0003/model.py"))
cases = [("2026-11-17/r3/lab-a/001"), ("2026-11-17/r3/lab-a/002"), ("2026-11-17/r3/lab-a/003"),
         ("2026-11-17/r3/lab-a/004"), ("2026-11-19/r1/lab-vernier/007")]
for c in cases:
    req = load_json(os.path.join(R, "requests", c + ".json"))
    res = load_json(os.path.join(R, "results", c + ".json"))
    rows = model_residuals(m, req, res)
    tmax = float(req["setup"]["duration"])
    mins = []
    for s in res["samples"]:
        p = s["particles"]
        r = math.hypot(p[1]["pos"][0] - p[0]["pos"][0], p[1]["pos"][1] - p[0]["pos"][1])
        mins.append((r, s["t"]))
    rmin, tmin = min(mins)
    seps0 = math.hypot(req["setup"]["particles"][1]["pos"][0]-req["setup"]["particles"][0]["pos"][0],
                       req["setup"]["particles"][1]["pos"][1]-req["setup"]["particles"][0]["pos"][1])
    early = [v for t, pid, dx, dy in rows if t <= 1.0 + 1e-9 for v in (dx, dy)]
    late = [v for t, pid, dx, dy in rows if t > 1.0 + 1e-9 for v in (dx, dy)]
    print(f"{c}: sep0 {seps0:.2f}, T {tmax}, min sep (obs) {rmin:.3f} at t={tmin}, "
          f"rms t<=1 {rms(early):.4f}, rms t>1 {rms(late) if late else float('nan'):.4f}, max|res| {max(abs(v) for v in early+late):.3f}")
