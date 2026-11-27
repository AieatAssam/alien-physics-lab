"""Score 2026-11-27/r2/lab-keystone/001: five A at rest, regular pentagon, side 5.5, T = 1.0, tracker.

Model (pre-registered in labs/lab-keystone/analysis/prereg_pentagon_2026-11-27.json): additive pairwise sum of the
P-0029 K table (nodes 5..9, held flat outside), P = 2.5, RK4 h = 0.001, specular walls at 0 and 10.
Falsifier: |s - 1| > 0.05 or judged RMSE/L > 0.021.
Noise sigma taken as 0.05 per coordinate (tracker floor ~0.005 of L), as in the earlier scoring scripts.
Reads the filed setup and result only. Pure python (numpy not installed).
"""
import json, math, sys

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
L = 10.0
SIG = 0.05
RID = "2026-11-27/r2/lab-keystone/001"

R_NODES = [5.0, 6.0, 7.0, 8.0, 9.0]
K_NODES = [17.834, 16.617, 15.121, 13.432, 11.624]

def K(r):
    if r <= R_NODES[0]:
        return K_NODES[0]
    if r >= R_NODES[-1]:
        return K_NODES[-1]
    for i in range(len(R_NODES) - 1):
        if R_NODES[i] <= r <= R_NODES[i + 1]:
            f = (r - R_NODES[i]) / (R_NODES[i + 1] - R_NODES[i])
            return K_NODES[i] + f * (K_NODES[i + 1] - K_NODES[i])

P = 2.5

def simulate(pos0, s, T, dt, h=0.001):
    n = len(pos0)
    pos = [list(p) for p in pos0]
    vel = [[0.0, 0.0] for _ in range(n)]

    def acc(p):
        a = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                dx = p[j][0] - p[i][0]; dy = p[j][1] - p[i][1]
                r = math.hypot(dx, dy)
                f = s * K(r) / r ** P / r
                a[i][0] += f * dx; a[i][1] += f * dy
                a[j][0] -= f * dx; a[j][1] -= f * dy
        return a

    def step(p, v, hh):
        a1 = acc(p)
        p2 = [[p[i][k] + hh / 2 * v[i][k] for k in range(2)] for i in range(n)]
        v2 = [[v[i][k] + hh / 2 * a1[i][k] for k in range(2)] for i in range(n)]
        a2 = acc(p2)
        p3 = [[p[i][k] + hh / 2 * v2[i][k] for k in range(2)] for i in range(n)]
        v3 = [[v[i][k] + hh / 2 * a2[i][k] for k in range(2)] for i in range(n)]
        a3 = acc(p3)
        p4 = [[p[i][k] + hh * v3[i][k] for k in range(2)] for i in range(n)]
        v4 = [[v[i][k] + hh * a3[i][k] for k in range(2)] for i in range(n)]
        a4 = acc(p4)
        np_ = [[p[i][k] + hh / 6 * (v[i][k] + 2 * v2[i][k] + 2 * v3[i][k] + v4[i][k]) for k in range(2)] for i in range(n)]
        nv = [[v[i][k] + hh / 6 * (a1[i][k] + 2 * a2[i][k] + 2 * a3[i][k] + a4[i][k]) for k in range(2)] for i in range(n)]
        for i in range(n):
            for k in range(2):
                if np_[i][k] < 0.0:
                    np_[i][k] = -np_[i][k]; nv[i][k] = -nv[i][k]
                elif np_[i][k] > L:
                    np_[i][k] = 2 * L - np_[i][k]; nv[i][k] = -nv[i][k]
        return np_, nv

    out = {0: [list(p) for p in pos]}
    t = 0.0
    nsamp = int(round(T / dt))
    for m in range(1, nsamp + 1):
        target = round(m * dt, 9)
        while t < target - 1e-12:
            hh = min(h, target - t)
            pos, vel = step(pos, vel, hh)
            t += hh
        t = target
        out[m] = [list(p) for p in pos]
    return out

req = json.load(open(f"{REPO}/requests/{RID[:-0] if False else RID.replace('2026-11-27/', '2026-11-27/')}.json")) if False else None
req = json.load(open(f"{REPO}/requests/2026-11-27/r2/lab-keystone/001.json"))
res = json.load(open(f"{REPO}/results/2026-11-27/r2/lab-keystone/001.json"))
setup = req["setup"]
dt = setup["sample_dt"]; T = setup["duration"]
pos0 = [p["pos"] for p in setup["particles"]]
n = len(pos0)

# Index samples by step; check the result's time grid and particle ids.
samples = res["samples"]
for s_ in samples:
    s_["_idx"] = int(round(s_["t"] / dt))
    ids = [q["id"] for q in s_["particles"]]
    assert ids == list(range(n)), ids

# Min/max pair distances at the filed initial layout (domain check: table covers 5..9).
pd = [math.dist(pos0[i], pos0[j]) for i in range(n) for j in range(i + 1, n)]
print(f"initial pair distances: min {min(pd):.4f} max {max(pd):.4f}")

def chi_and_rmse(s):
    pred = simulate(pos0, s, T, dt)
    sq = 0.0; cnt = 0
    for smp in samples:
        m = smp["_idx"]
        for q, p in zip(smp["particles"], pred[m]):
            for c in range(2):
                d = q["pos"][c] - p[c]
                sq += d * d; cnt += 1
    return sq / SIG**2, math.sqrt(sq / cnt) / L, pred

# Sanity: the pre-registered prediction at s = 1.0 must reproduce.
prereg = json.load(open(f"{REPO}/labs/lab-keystone/analysis/prereg_pentagon_2026-11-27.json"))
chk_idx = 1000
chk = simulate(pos0, 1.0, T, dt)[chk_idx]
ref = prereg["predicted_positions"]["1.0"][0] if False else prereg["predicted_positions"]["1.0"]
err = max(abs(chk[i][c] - ref[i][c]) for i in range(n) for c in range(2))
print(f"sanity: max |sim - prereg(s=1, t=1.0)| = {err:.2e}")
assert err < 1e-3, "simulator does not reproduce the pre-registered prediction"

# Scale grid 0.90..1.10 in steps of 0.002
grid = [round(0.90 + 0.002 * i, 3) for i in range(101)]
chi = {}
for sc in grid:
    c, _, _ = chi_and_rmse(sc)
    chi[sc] = c
s_best = min(chi, key=chi.get)
chi_min = chi[s_best]
inside = [sc for sc, c in chi.items() if c <= chi_min + 1.0]
lo, hi = min(inside), max(inside)
dof = sum(len(s_["particles"]) * 2 for s_ in samples) - 1

_, rmse_L, _ = chi_and_rmse(1.0)
print(f"RMSE/L at s = 1: {rmse_L:.5f}   (falsifier 0.021)")
print(f"best s = {s_best:.3f}  (dchi2=1 interval {lo:.3f} to {hi:.3f}; sigma ~ {(hi - lo) / 2:.4f})")
print(f"chi2_min/dof = {chi_min / dof:.3f}  (dof {dof})")
print(f"|s - 1| = {abs(s_best - 1):.3f}  (falsifier 0.05)")
fail = abs(s_best - 1) > 0.05 or rmse_L > 0.021
print("VERDICT:", "FALSIFIED by pre-registered rule" if fail else "passes pre-registered rule")
