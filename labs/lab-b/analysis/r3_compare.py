# Shared-time comparison of two runs with the same requested initial state.
# Usage: python3 -I r3_compare.py <fileA> <fileB> <tmax>
# Reports per-coordinate differences at common times (noise sd 0.05 each -> diff sd ~0.07).
import json, math, sys
A = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2])); tmax = float(sys.argv[3])
def idx(d):
    return {round(s["t"], 4): s for s in d["samples"]}
ia, ib = idx(A), idx(B)
common = sorted(t for t in ia if t in ib and t <= tmax + 1e-9)
dx = []; dy = []; sep_a = []; sep_b = []
for t in common:
    pa, pb = ia[t]["particles"], ib[t]["particles"]
    for i in range(len(pa)):
        dx.append(pa[i]["pos"][0] - pb[i]["pos"][0]); dy.append(pa[i]["pos"][1] - pb[i]["pos"][1])
    sep_a.append(math.hypot(pa[1]["pos"][0]-pa[0]["pos"][0], pa[1]["pos"][1]-pa[0]["pos"][1]))
    sep_b.append(math.hypot(pb[1]["pos"][0]-pb[0]["pos"][0], pb[1]["pos"][1]-pb[0]["pos"][1]))
def rms(v): return math.sqrt(sum(x*x for x in v)/len(v))
print(f"common samples t<= {tmax}: n={len(common)}, first {common[0]}, last {common[-1]}")
print(f"coordinate diff rms: x={rms(dx):.4f} y={rms(dy):.4f} (expected ~0.07 if both are noisy copies of one trajectory)")
print(f"mean diff x={sum(dx)/len(dx):+.4f} y={sum(dy)/len(dy):+.4f}")
print(f"separation rms diff={rms([a-b for a,b in zip(sep_a,sep_b)]):.4f}")
for t in common:
    if abs(round(t/0.05) - t/0.05) < 1e-6 and t <= tmax + 1e-9:
        pa, pb = ia[t]["particles"], ib[t]["particles"]
        ra = math.hypot(pa[1]["pos"][0]-pa[0]["pos"][0], pa[1]["pos"][1]-pa[0]["pos"][1])
        rb = math.hypot(pb[1]["pos"][0]-pb[0]["pos"][0], pb[1]["pos"][1]-pb[0]["pos"][1])
        print(f"  t={t:5.2f}  r_A={ra:6.3f}  r_B={rb:6.3f}")
