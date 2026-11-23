"""Score a paper's predict() against lab-a runs, mirroring the judge's metric.

Usage: python3 -I score_paper_2026-11-23.py <repo_root> <P-id> <req_dir> <res_dir> <nnn> [<nnn> ...]
  req_dir/res_dir are relative to repo_root, e.g. requests/2026-11-23/r1/lab-a
Error = RMSE over all samples, particles and coordinates / L, using the paper's predict(setup).
Out-of-domain runs (predict raises ValueError) are reported and not scored.
"""
import importlib.util
import json
import math
import os
import sys

root, pid, req_dir, res_dir = sys.argv[1:5]
ids = sys.argv[5:]
L = 10.0

spec = importlib.util.spec_from_file_location("paper_model", os.path.join(root, "papers", pid, "model.py"))
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
claim = json.load(open(os.path.join(root, "papers", pid, "claim.json")))["claims"][0]
bar = 3 * claim["predicted_error"]
print(f"{pid} predicted_error={claim['predicted_error']} bar(3x)={bar:.4f} domain={claim['domain']}")

for nnn in ids:
    rq = json.load(open(os.path.join(root, req_dir, f"{nnn}.json")))
    rs = json.load(open(os.path.join(root, res_dir, f"{nnn}.json")))
    setup = rq["setup"]
    seps = [math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])] if len(setup["particles"]) == 2 else []
    try:
        pred = model.predict(setup)
    except ValueError as e:
        print(f"{nnn}: OUT OF DOMAIN ({e}) sep={seps[0] if seps else None}")
        continue
    if rs["status"] != "ok":
        print(f"{nnn}: status {rs['status']}")
        continue
    meas = rs["samples"]
    assert len(meas) == len(pred), (len(meas), len(pred))
    se, n = 0.0, 0
    for m, p in zip(meas, pred):
        assert abs(m["t"] - p["t"]) < 1e-9
        for mp, pp in zip(m["particles"], p["particles"]):
            for k in range(2):
                se += (mp["pos"][k] - pp["pos"][k]) ** 2
                n += 1
    err = math.sqrt(se / n) / L
    print(f"{nnn}: sep0={seps[0]:.3f} T={setup['duration']} dt={setup['sample_dt']} n={len(meas)} "
          f"RMSE/L={err:.5f} {'PASS' if err <= bar else 'FAIL'}(bar {bar:.4f})")
