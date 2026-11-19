"""Pre-registered predictions for round 3 (2026-11-19, lab-c), written BEFORE the runs.

Model: pure pairwise central acceleration K / r^2.5 toward each partner (P = 2.5 fixed), constant K per
species pair, RK4 step 0.001, no walls (no particle approaches a wall in these runs; checked below).
 - r3/001 (review, cites P-0007): three A at rest, equilateral side 5, centroid (5,5), T=1.5, dt 0.03.
   K_AA = 18.0 (P-0005 / P-0003 value that P-0007 itself uses).
   (A same-species side-3 triangle was considered and dropped: it collapses through itself by t~0.9.)
 - r3/002 (research): replicate of r2/002 (A-B-C side 3). Prediction = analysis/side3_prediction.json (unchanged).
Usage: python3 -I predict_round3.py <analysis_dir>
"""
import json, math, os, sys
adir = sys.argv[1]
P = 2.5

def acc(pos, sp, K):
    out = []
    for i in range(len(pos)):
        ax = ay = 0.0
        for j in range(len(pos)):
            if i == j: continue
            dx = pos[j][0] - pos[i][0]; dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            a = K[(sp[i], sp[j])] / r ** P
            ax += a * dx / r; ay += a * dy / r
        out.append((ax, ay))
    return out

def run(pos0, sp, K, T, dt, h=0.001):
    pos = [list(p) for p in pos0]; vel = [[0.0, 0.0] for _ in pos0]
    res = [{"t": 0.0, "pos": [list(p) for p in pos]}]
    n = int(round(T / dt)); t = 0.0; minwall = 10.0
    for k in range(1, n + 1):
        target = k * dt
        while t < target - 1e-12:
            hh = min(h, target - t)
            def st(p, v, a):
                return p, v
            a1 = acc(pos, sp, K)
            k1p = [v for v in vel]; k1v = a1
            p2 = [[pos[i][c] + hh/2*k1p[i][c] for c in range(2)] for i in range(len(pos))]
            v2 = [[vel[i][c] + hh/2*k1v[i][c] for c in range(2)] for i in range(len(pos))]
            a2 = acc(p2, sp, K)
            p3 = [[pos[i][c] + hh/2*v2[i][c] for c in range(2)] for i in range(len(pos))]
            v3 = [[vel[i][c] + hh/2*a2[i][c] for c in range(2)] for i in range(len(pos))]
            a3 = acc(p3, sp, K)
            p4 = [[pos[i][c] + hh*v3[i][c] for c in range(2)] for i in range(len(pos))]
            v4 = [[vel[i][c] + hh*a3[i][c] for c in range(2)] for i in range(len(pos))]
            a4 = acc(p4, sp, K)
            pos = [[pos[i][c] + hh/6*(k1p[i][c] + 2*v2[i][c] + 2*v3[i][c] + v4[i][c]) for c in range(2)] for i in range(len(pos))]
            vel = [[vel[i][c] + hh/6*(k1v[i][c] + 2*a2[i][c] + 2*a3[i][c] + a4[i][c]) for c in range(2)] for i in range(len(pos))]
            t += hh
        for p in pos:
            for c in range(2):
                minwall = min(minwall, p[c], 10 - p[c])
        res.append({"t": round(target, 6), "pos": [list(p) for p in pos]})
    return res, minwall

def tri(cx, cy, s):
    R = s / math.sqrt(3)
    return [[cx, cy + R], [cx - s/2, cy - R/2], [cx + s/2, cy - R/2]]

out = {}
p5 = tri(5.0, 5.0, 5.0)
r1, w1 = run(p5, ["A", "A", "A"], {("A", "A"): 18.0}, 1.5, 0.03)
out["2026-11-19/r3/lab-c/001"] = {"K": {"A(A)": 18.0}, "T": 1.5, "dt": 0.03, "min_wall_clearance": round(w1, 3), "samples": r1,
    "rule": "P-0007 rule for comparability: supported if every particle's residual rms per coordinate <= 0.07 and the zero-force null rms > 0.09; refuted if any run's residual rms > 0.12."}
out["2026-11-19/r3/lab-c/002"] = {"note": "replicate of r2/002 (A-B-C side 3, identical setup); prediction is analysis/side3_prediction.json (pre-registered in round 2)."
    , "rule": "refuted if residual rms per coordinate > 0.065, or any particle's mean residual over (0,0.5] or (0.5,1.0] exceeds 0.03 in any coordinate. Replaces the 0.15 per-sample rule, which sits at 3 sigma and fires by chance (see NOTEBOOK).",
    "samples_file": "side3_prediction.json"}
json.dump(out, open(os.path.join(adir, "round3_predictions.json"), "w"))
print("wall clearance 001: min %.3f (must be > 0 for the no-wall model)" % w1)
print("final positions 001:", [[round(c, 3) for c in p] for p in r1[-1]["pos"]])
