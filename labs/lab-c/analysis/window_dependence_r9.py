"""Window-dependence of fitted A-A coefficient at separation 9 (P-0006 factor 0.65 edge).

Refits the same runs with the data truncated to t <= TMAX. Tests whether K_AA(9) is window-independent
under the fixed-P=2.5 law. Runs: my 2026-11-19/r1/lab-c/019 (T=3) and lab-a 2026-11-18/r1/lab-a/008-009 (T=4).
Usage: python3 -I window_dependence_r9.py <repo_root>
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit_pair_K_1d as F

root = sys.argv[1]
runs = ["2026-11-19/r1/lab-c/019", "2026-11-18/r1/lab-a/008", "2026-11-18/r1/lab-a/009"]
for tmax in (1.0, 2.0, 3.0, 4.0):
    row = []
    for rid in runs:
        res = json.load(open(os.path.join(root, "results", rid + ".json")))
        req = json.load(open(os.path.join(root, "requests", rid + ".json")))
        res = dict(res)
        res["samples"] = [s for s in res["samples"] if s["t"] <= tmax + 1e-9]
        K1, K2, rms, _, _, _, _ = F.fit_run(res, req)
        row.append("%s: K=%.2f,%.2f (mean %.2f, rms %.3f)" % (rid.split("/")[-2] + "/" + rid.split("/")[-1], K1, K2, (K1 + K2) / 2, rms))
    print("T<=%.1f | " % tmax + " | ".join(row))
