"""Round 3 part 2 (2026-11-19, lab-c):
 D. side-3 triangle (r2/002): residual structure by time window, exceedance count vs Gaussian expectation,
    pair separations along the run.
 E. P-0006 predictor (papers/P-0006/model.py, lab-a's own code, run as-is, imports math only) run out of sample
    on my review runs r2/003-011: residual rms, mean residual, max |residual| per run.
Usage: python3 -I round3_part2.py <repo_root> <analysis_dir>
"""
import importlib.util, json, math, os, sys
root, adir = sys.argv[1], sys.argv[2]
sys.path.insert(0, adir)
RUN = "2026-11-19/r2/lab-c/"
pred = {round(s["t"], 4): s["pos"] for s in json.load(open(os.path.join(adir, "side3_prediction.json")))["samples"]}
res = json.load(open(os.path.join(root, "results", RUN + "002.json")))

# ---- D ----
rows = []
for s in res["samples"]:
    t = round(s["t"], 4)
    if t == 0 or t not in pred:
        continue
    for k in range(3):
        o = s["particles"][k]["pos"]; p = pred[t][k]
        rows.append((t, k, o[0] - p[0], o[1] - p[1]))
def sd(xs):
    m = sum(xs) / len(xs); return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))
print("D. side-3 (r2/002): N=%d residuals (x,y for 3 particles, t in (0,1.5])" % len(rows))
for lo, hi in ((0, 0.5), (0.5, 1.0), (1.0, 1.5)):
    sub = [r for r in rows if lo < r[0] <= hi + 1e-9]
    rx = [r[2] for r in sub]; ry = [r[3] for r in sub]
    print("   t in (%.1f,%.1f]: n=%d  rms x=%.4f y=%.4f  mean x=%+.4f y=%+.4f  max|res|=%.4f"
          % (lo, hi, len(sub), math.sqrt(sum(x*x for x in rx)/len(rx)), math.sqrt(sum(y*y for y in ry)/len(ry)),
             sum(rx)/len(rx), sum(ry)/len(ry), max(max(abs(x), abs(y)) for x, y in zip(rx, ry))))
allc = [c for r in rows for c in (r[2], r[3])]
sig = math.sqrt(sum(c*c for c in allc) / len(allc))
n_exc = sum(1 for c in allc if abs(c) > 0.15)
# Gaussian expectation for exceedance count at sigma=estimate
p_exc = math.erfc(0.15 / (sig * math.sqrt(2)))
print("   overall sigma=%.4f; |res|>0.15 observed %d of %d (Gaussian expectation %.2f)" % (sig, n_exc, len(allc), p_exc * len(allc)))
print("   exceedances:", [(r[0], r[1], round(r[2], 3), round(r[3], 3)) for r in rows if max(abs(r[2]), abs(r[3])) > 0.15])
# ---- E ----
spec = importlib.util.spec_from_file_location("p0006", os.path.join(root, "papers", "P-0006", "model.py"))
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
print("E. P-0006 predictor out of sample on r2/003-011 (model.py, unmodified)")
for n in range(3, 12):
    rid = RUN + "%03d" % n
    rq = json.load(open(os.path.join(root, "requests", rid + ".json")))
    rs = json.load(open(os.path.join(root, "results", rid + ".json")))
    try:
        ps = M.predict(rq["setup"])
    except ValueError as e:
        print("   %03d: predictor refused: %s" % (n, e)); continue
    pmap = {round(s["t"], 4): s["particles"] for s in ps}
    rx, ry = [], []
    for s in rs["samples"]:
        t = round(s["t"], 4)
        if t == 0 or t not in pmap: continue
        for k in range(2):
            o = s["particles"][k]["pos"]; p = pmap[t][k]["pos"]
            rx.append(o[0] - p[0]); ry.append(o[1] - p[1])
    mx = max(max(abs(a), abs(b)) for a, b in zip(rx, ry))
    print("   %03d %s-%s: n=%d rms x=%.4f y=%.4f  mean x=%+.4f y=%+.4f  max|res|=%.3f"
          % (n, rq["setup"]["particles"][0]["species"], rq["setup"]["particles"][1]["species"], len(rx),
             math.sqrt(sum(a*a for a in rx)/len(rx)), math.sqrt(sum(b*b for b in ry)/len(ry)),
             sum(rx)/len(rx), sum(ry)/len(ry), mx))
