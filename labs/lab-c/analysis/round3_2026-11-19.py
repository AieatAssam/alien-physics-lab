"""Round 3 (2026-11-19) analysis for lab-c (Nullius).

Parts:
 A. side-3 triangle (r2/002) against the pre-registered prediction (analysis/side3_prediction.json).
 B. window test at r=9 (r2/001): refit with data truncated to t <= TMAX, pre-registered rule
    (T<=6 vs T<=3 mean of 10.65).
 C. P-0006 review runs r2/003-011: two-body fits with the 1-D model (fit_pair_K_1d), plus
    the paper's predicted K values from P-0006 model.py (computed here by hand from the claim).
Usage: python3 -I round3_2026-11-19.py <repo_root> <analysis_dir>
"""
import json, math, os, sys

root, adir = sys.argv[1], sys.argv[2]
sys.path.insert(0, adir)
import fit_pair_K_1d as F

def load(rid):
    res = json.load(open(os.path.join(root, "results", rid + ".json")))
    req = json.load(open(os.path.join(root, "requests", rid + ".json")))
    return res, req

RUN = "2026-11-19/r2/lab-c/"

# ---- A. side-3 triangle ----
res, req = load(RUN + "002")
pred = json.load(open(os.path.join(adir, "side3_prediction.json")))["samples"]
pmap = {round(s["t"], 4): s["pos"] for s in pred}
devs = []
for s in res["samples"]:
    t = round(s["t"], 4)
    if t not in pmap or t == 0:
        continue
    for k in range(3):
        o = s["particles"][k]["pos"]
        p = pmap[t][k]
        devs.append((t, k, o[0] - p[0], o[1] - p[1]))
mx = max(max(abs(dx), abs(dy)) for _, _, dx, dy in devs)
rms = math.sqrt(sum(dx * dx + dy * dy for _, _, dx, dy in devs) / (2 * len(devs)))
worst = max(devs, key=lambda d: max(abs(d[2]), abs(d[3])))
print("A. r2/002 side-3 triangle: n=%d, max |dev|=%.4f (t=%.2f, particle %d), rms per coord=%.4f, falsifier 0.15"
      % (len(devs), mx, worst[0], worst[1], rms))
for tt in (0.5, 1.0, 1.5):
    sub = [d for d in devs if abs(d[0] - tt) < 1e-9]
    if sub:
        print("   t=%.1f: max |dev| = %.4f" % (tt, max(max(abs(dx), abs(dy)) for _, _, dx, dy in sub)))

# ---- B. window test at r=9 ----
res, req = load(RUN + "001")
print("B. r2/001 A-A r=9 T=6 window test")
for tmax in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0):
    r2 = dict(res)
    r2["samples"] = [s for s in res["samples"] if s["t"] <= tmax + 1e-9]
    K1, K2, rms, _, _, _, _ = F.fit_run(r2, req)
    print("   T<=%.1f: K_A(A)=%.3f, %.3f (mean %.3f), rms %.4f" % (tmax, K1, K2, (K1 + K2) / 2, rms))
K1, K2, rms, yr, *_ = F.fit_run(res, req)
print("   full T<=6: mean K=%.3f; y-spread %.4f" % ((K1 + K2) / 2, yr))

# ---- C. P-0006 review runs ----
print("C. P-0006 review runs (two-body, P=2.5 fixed, 1-D fit, whole window T<=4)")
for n in range(3, 12):
    rid = RUN + "%03d" % n
    res, req = load(rid)
    parts = req["setup"]["particles"]
    K1, K2, rms, yr, s1, s2, r0 = F.fit_run(res, req)
    print("   %s %s-%s r=%.1f  K1=%+.3f K2=%+.3f mean|K|=%.3f  rms=%.4f  ymean-spread=%.4f  events=%d"
          % (rid.split("/")[-1], s1, s2, r0, K1, K2, (abs(K1) + abs(K2)) / 2, rms, yr, len(res["events"])))
