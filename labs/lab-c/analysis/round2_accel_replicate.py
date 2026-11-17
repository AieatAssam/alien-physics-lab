"""Initial accelerations of at-rest pairs (quadratic fit over early window) and
replicate check of r2/004 against r1/003 at common times. stdlib only."""
import json, math, sys
sys.path.insert(0, "/home/runner/work/alien-physics-lab/alien-physics-lab/out/labs/lab-c/analysis")
from round2_analysis import load, polyfit, rms, mean

def accel(n, W):
    _, traj, sp = load(n)
    t = [s[0] for s in traj[0]]
    out = []
    for pid in (0, 1):
        xs = [s[1] for s in traj[pid]]
        ys = [s[2] for s in traj[pid]]
        idx = [i for i, tt in enumerate(t) if tt <= W]
        cx = polyfit([t[i] for i in idx], [xs[i] for i in idx], 2)
        cy = polyfit([t[i] for i in idx], [ys[i] for i in idx], 2)
        out.append((2 * cx[2], 2 * cy[2]))
    return out

for n, r0 in ((1, 3.0), (5, 1.5), (6, 6.0)):
    for W in (0.2, 0.3, 0.4):
        a0, a1 = accel(n, W)
        print("r2/%03d r0=%.1f W=%.1f  ax0 %+.3f ax1 %+.3f  (|a_rel| %.3f, ay0 %+.3f ay1 %+.3f)" % (
            n, r0, W, a0[0], a1[0], a1[0] - a0[0], a0[1], a1[1]))

# replicate check: r1/003 (dt 0.1) vs r2/004 (dt 0.005) at common times
R1 = "/home/runner/work/alien-physics-lab/alien-physics-lab/results/2026-11-17/r1/lab-c/003.json"
d1 = json.load(open(R1))
r1 = {round(s["t"], 6): {p["id"]: tuple(p["pos"]) for p in s["particles"]} for s in d1["samples"]}
_, traj, _ = load(4)
r2 = {round(s[0], 6): {0: (s[1], s[2])} for s in traj[0]}
for pid in (1,):
    pass
r2b = {round(s[0], 6): (s[1], s[2]) for s in traj[1]}
r2a = {round(s[0], 6): (s[1], s[2]) for s in traj[0]}
diffs0, diffs1, tt = [], [], []
for t in sorted(r1):
    k = round(t, 6)
    if k in r2a:
        diffs0.append(math.dist(r1[t][0], r2a[k]))
        diffs1.append(math.dist(r1[t][1], r2b[k]))
        tt.append(t)
print("replicate r1/003 vs r2/004 at %d common times (t up to %.1f)" % (len(tt), max(tt)))
print("  rms diff p0 %.4f  p1 %.4f  ; max p0 %.3f at t=%.2f ; max p1 %.3f at t=%.2f" % (
    rms(diffs0), rms(diffs1), max(diffs0), tt[diffs0.index(max(diffs0))], max(diffs1), tt[diffs1.index(max(diffs1))]))
for k in range(0, len(tt), 10):
    print("  t=%5.2f  d0 %.3f  d1 %.3f" % (tt[k], diffs0[k], diffs1[k]))
