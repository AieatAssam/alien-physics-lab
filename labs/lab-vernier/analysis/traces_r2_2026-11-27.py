"""Side-by-side smoothed separation (0.02 bins) for the contact runs. Stdlib only.
Run: python3 -I traces_r2_2026-11-27.py <repo_root>"""
import json, math, sys, os
ROOT = sys.argv[1]
def load(p):
    return json.load(open(os.path.join(ROOT, "results", "2026-11-27", p)))
runs = {
 "r1/001 (dt.0003 h)": load("r1/lab-vernier/001.json"),
 "r2/001 (replicate)": load("r2/lab-vernier/001.json"),
 "r2/002 (vertical)": load("r2/lab-vernier/002.json"),
 "r2/003 (T2 dt.001)": load("r2/lab-vernier/003.json"),
}
def binned(res, w=0.02):
    b = {}
    for s in res["samples"]:
        p0, p1 = s["particles"][0]["pos"], s["particles"][1]["pos"]
        d = math.hypot(p0[0]-p1[0], p0[1]-p1[1])
        k = int(math.floor(s["t"]/w + 1e-9))
        b.setdefault(k, []).append(d)
    return {k*w: sum(v)/len(v) for k, v in b.items()}
B = {n: binned(r) for n, r in runs.items()}
times = [round(0.02*k, 2) for k in range(0, 51)]  # 0 .. 1.0
print("t     " + "  ".join(f"{n:>20}" for n in runs))
for t in times:
    row = []
    for n in runs:
        v = B[n].get(t)
        row.append(f"{v:20.3f}" if v is not None else " " * 20)
    print(f"{t:5.2f} " + "  ".join(row))
