"""Pre-registered prediction for 2026-11-19/r2/lab-c/002 (equilateral A-B-C, side 3, T=1.5, dt 0.01).

Pairwise-additive model with RK4 (dt 0.002). K from round-1 r=3 per-run fits (not from P-0005):
  K_A(B)=8.880 (2026-11-19/r1/lab-c/002), K_B(A)=12.615 (same run)
  K_A(C)=-8.803, K_C(A)=-21.404 (r1/lab-c/003)
  K_B(C)=-5.873, K_C(B)=-10.001 (r1/lab-c/005)
Writes predicted samples to analysis/side3_prediction.json. Run before results exist.
Usage: python3 -I predict_side3_triangle.py <repo_root>
"""
import json, math, os, sys
root = sys.argv[1]
req = json.load(open(os.path.join(root, "out/requests/2026-11-19/r2/lab-c/002.json")))
species = [p["species"] for p in req["setup"]["particles"]]
x0 = [list(p["pos"]) for p in req["setup"]["particles"]]
K = {("A", "B"): 8.880, ("B", "A"): 12.615, ("A", "C"): -8.803, ("C", "A"): -21.404,
     ("B", "C"): -5.873, ("C", "B"): -10.001}
P = 2.5


def acc(pos):
    n = len(pos)
    a = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            d = math.hypot(dx, dy)
            k = K[(species[i], species[j])] / d ** P
            a[i][0] += k * dx / d
            a[i][1] += k * dy / d
    return a


def rk4(pos, vel, h):
    def f(p, v):
        return v, acc(p)
    def lin(a, b, s):
        return [[a[i][c] + s * b[i][c] for c in range(2)] for i in range(len(a))]
    k1p, k1v = f(pos, vel)
    k2p, k2v = f(lin(pos, k1p, h / 2), lin(vel, k1v, h / 2))
    k3p, k3v = f(lin(pos, k2p, h / 2), lin(vel, k2v, h / 2))
    k4p, k4v = f(lin(pos, k3p, h), lin(vel, k3v, h))
    newp = [[pos[i][c] + h / 6 * (k1p[i][c] + 2 * k2p[i][c] + 2 * k3p[i][c] + k4p[i][c]) for c in range(2)] for i in range(len(pos))]
    newv = [[vel[i][c] + h / 6 * (k1v[i][c] + 2 * k2v[i][c] + 2 * k3v[i][c] + k4v[i][c]) for c in range(2)] for i in range(len(pos))]
    return newp, newv


T = req["setup"]["duration"]
dt = req["setup"]["sample_dt"]
n_samp = int(round(T / dt))
pos = [list(p) for p in x0]
vel = [[0.0, 0.0] for _ in x0]
samples = [{"t": 0.0, "pos": [list(p) for p in pos]}]
sub = 0.002
steps_per = int(round(dt / sub))
for s in range(n_samp):
    for _ in range(steps_per):
        pos, vel = rk4(pos, vel, sub)
    samples.append({"t": round((s + 1) * dt, 6), "pos": [list(p) for p in pos]})
a0 = acc(x0)
out = {
    "request_id": req["request_id"],
    "status": "pre-registered (written before results)",
    "species": species,
    "K": {"%s(%s)" % (a, b): v for (a, b), v in K.items()},
    "initial_accel": [[species[i], round(a0[i][0], 4), round(a0[i][1], 4)] for i in range(3)],
    "falsifier": "any tracker sample deviating from predicted position by > 0.15 per coordinate (t <= 1.5)",
    "samples": samples,
}
p = os.path.join(root, "out/labs/lab-c/analysis/side3_prediction.json")
json.dump(out, open(p, "w"))
print("wrote", p, "n_samples", len(samples))
print("initial accel:", out["initial_accel"])
print("end positions t=%.2f:" % samples[-1]["t"], [[round(c, 3) for c in q] for q in samples[-1]["pos"]])
