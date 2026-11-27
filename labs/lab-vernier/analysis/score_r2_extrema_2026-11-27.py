"""Post-contact extrema and gaps for r2 runs. Stdlib only.
Run: python3 -I score_r2_extrema_2026-11-27.py <repo_root>"""
import json, math, sys, os
ROOT = sys.argv[1]
def load(p):
    return json.load(open(os.path.join(ROOT, "results", "2026-11-27", p)))
def sep(res):
    return [(s["t"], math.hypot(s["particles"][0]["pos"][0]-s["particles"][1]["pos"][0],
                                s["particles"][0]["pos"][1]-s["particles"][1]["pos"][1]))
            for s in res["samples"]]
def binned(series, w=0.02):
    b = {}
    for t, d in series:
        b.setdefault(int(math.floor(t/w+1e-9)), []).append(d)
    return {round(k*w, 4): sum(v)/len(v) for k, v in b.items()}
r1 = binned(sep(load("r1/lab-vernier/001.json")))
r2a = binned(sep(load("r2/lab-vernier/001.json")))
r2b = binned(sep(load("r2/lab-vernier/002.json")))
s3 = sep(load("r2/lab-vernier/003.json"))

def maxdiff(a, b, lo, hi):
    ks = [k for k in a if k in b and lo <= k <= hi]
    k = max(ks, key=lambda k: abs(a[k]-b[k]))
    return abs(a[k]-b[k]), k, len(ks)

print("r2/001 vs r1/001, t<=0.24 (pre-contact):", maxdiff(r1, r2a, 0, 0.24))
print("r2/001 vs r1/001, t in [0.30,0.60]:    ", maxdiff(r1, r2a, 0.30, 0.60))
print("r2/002 vs r2/001, t in [0.30,0.60]:    ", maxdiff(r2a, r2b, 0.30, 0.60))
print("r2/002 vs r1/001, t in [0.30,0.60]:    ", maxdiff(r1, r2b, 0.30, 0.60))
# first t where r2/001 and r1/001 differ by > 0.05 (post contact)
first = next(k for k in sorted(r1) if k in r2a and k > 0.2 and abs(r1[k]-r2a[k]) > 0.05)
print("first post-contact divergence (>0.05) at t about", first)
# r2/003 post-contact (t >= 0.3) extrema on the raw per-sample trace
post = [(t, d) for t, d in s3 if t >= 0.3]
mx = max(post, key=lambda x: x[1]); print(f"r2/003 max sep for t>=0.3: {mx[1]:.3f} at t={mx[0]:.3f}")
mn = min(post, key=lambda x: x[1]); print(f"r2/003 min sep for t>=0.3: {mn[1]:.4f} at t={mn[0]:.3f}")
# count separate approaches below 0.3 (smoothed 0.02 bins, t>=0.3)
b3 = binned(s3)
ks = sorted(k for k in b3 if k >= 0.3)
dips = [k for i, k in enumerate(ks[1:-1], 1) if b3[k] < 0.3 and b3[k] <= b3[ks[i-1]] and b3[k] <= b3[ks[i+1]]]
print("r2/003 separate dips below 0.3 (t>=0.3):", [round(k, 2) for k in dips])
print("r2/003 smoothed max for t>=0.3:", round(max(b3[k] for k in ks), 3))
