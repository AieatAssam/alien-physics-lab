"""Score research runs 2026-11-27/r1/lab-keystone 001-003.

001, 002: C-C pair at rest, r0 = 2.5. Model: P-0034 C-C node table (K linear in r, held at end values),
          P = 2.5, pairwise, specular walls. Note: P-0034 claims r0 in [3.0, 3.5] only; the 2.5 node is extrapolated.
003:      A equilateral triangle, side 7.0, T = 2. Model: P-0029 pair table (nodes 5..9, P = 2.5) summed pairwise
          (same table as P-0033 / N = 4 square). Table is interpolated at r in [7, 7.0].
Each run: RMSE/L at scale s = 1 (judged metric), and best-fit scale s with sigma = 0.05 per coordinate.
"""
import json, math

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
L = 10.0
SIG = 0.05

def make_K(nodes_r, nodes_k):
    def K(r):
        if r <= nodes_r[0]:
            return nodes_k[0]
        if r >= nodes_r[-1]:
            return nodes_k[-1]
        for i in range(len(nodes_r) - 1):
            if nodes_r[i] <= r <= nodes_r[i + 1]:
                f = (r - nodes_r[i]) / (nodes_r[i + 1] - nodes_r[i])
                return nodes_k[i] + f * (nodes_k[i + 1] - nodes_k[i])
    return K

def simulate(pos, K, P, s, T, dt, h=0.001):
    n = len(pos)
    pos = [list(p) for p in pos]
    vel = [[0.0, 0.0] for _ in range(n)]
    def acc(p):
        a = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dx = p[j][0] - p[i][0]; dy = p[j][1] - p[i][1]
                r = math.hypot(dx, dy)
                f = s * K(r) / r ** P / r
                a[i][0] += f * dx; a[i][1] += f * dy
        return a
    def step(p, v, hh):
        a1 = acc(p)
        p2 = [[p[i][k] + hh/2*v[i][k] for k in range(2)] for i in range(n)]
        v2 = [[v[i][k] + hh/2*a1[i][k] for k in range(2)] for i in range(n)]
        a2 = acc(p2)
        p3 = [[p[i][k] + hh/2*v2[i][k] for k in range(2)] for i in range(n)]
        v3 = [[v[i][k] + hh/2*a2[i][k] for k in range(2)] for i in range(n)]
        a3 = acc(p3)
        p4 = [[p[i][k] + hh*v3[i][k] for k in range(2)] for i in range(n)]
        v4 = [[v[i][k] + hh*a3[i][k] for k in range(2)] for i in range(n)]
        a4 = acc(p4)
        np_ = [[p[i][k] + hh/6*(v[i][k] + 2*v2[i][k] + 2*v3[i][k] + v4[i][k]) for k in range(2)] for i in range(n)]
        nv = [[v[i][k] + hh/6*(a1[i][k] + 2*a2[i][k] + 2*a3[i][k] + a4[i][k]) for k in range(2)] for i in range(n)]
        for i in range(n):
            for k in range(2):
                if np_[i][k] < 0.0:
                    np_[i][k] = -np_[i][k]; nv[i][k] = -nv[i][k]
                elif np_[i][k] > L:
                    np_[i][k] = 2*L - np_[i][k]; nv[i][k] = -nv[i][k]
        return np_, nv
    out = {}
    t = 0.0
    nsamp = int(round(T / dt))
    out[0] = [list(p) for p in pos]
    for m in range(1, nsamp + 1):
        target = round(m * dt, 9)
        while t < target - 1e-12:
            hh = min(h, target - t)
            pos, vel = step(pos, vel, hh)
            t += hh
        t = target
        out[m] = [list(p) for p in pos]
    return out

def residuals(meas, pred_by_idx):
    sq = 0.0; n = 0
    for s_ in meas:
        m = s_["_idx"]
        for k_obs, p in zip(s_["particles"], pred_by_idx[m]):
            for c in range(2):
                d = k_obs["pos"][c] - p[c]
                sq += d*d; n += 1
    return sq, n

def run(rid, K, P, T_expected, label):
    res = json.load(open(f"{REPO}/results/2026-11-27/r1/lab-keystone/{rid}.json"))
    req = json.load(open(f"{REPO}/requests/2026-11-27/r1/lab-keystone/{rid}.json"))
    setup = req["setup"]
    dt = setup["sample_dt"]; T = setup["duration"]
    pos0 = [p["pos"] for p in setup["particles"]]
    samples = res["samples"]
    for s_ in samples:
        s_["_idx"] = int(round(s_["t"] / dt))
    # Run simulation at s grid
    grid = [round(0.90 + 0.001*i, 3) for i in range(201)]  # 0.90..1.10
    best = None
    chi2_at = {}
    cache = {}
    for sc in grid:
        pred = simulate(pos0, K, P, sc, T, dt)
        sq, n = residuals(samples, pred)
        chi2 = sq / SIG**2
        chi2_at[sc] = chi2
        if best is None or chi2 < best[1]:
            best = (sc, chi2, n)
    s_best, chi2_min, n = best
    # one-sigma from chi2 + 1 (chi2 scale) with dof
    dof = n - 1
    # Delta chi2 = 1 interval
    inside = [sc for sc, c in chi2_at.items() if c <= chi2_min + 1.0]
    lo, hi = min(inside), max(inside)
    pred1 = simulate(pos0, K, P, 1.0, T, dt)
    sq1, n1 = residuals(samples, pred1)
    rmse_L = math.sqrt(sq1 / n1) / L
    print(f"{rid} [{label}] r0={math.dist(pos0[0], pos0[1]) if len(pos0)==2 else 'tri'} T={T}")
    print(f"   RMSE/L at s=1: {rmse_L:.5f}   (judged bar 3x0.007=0.021; noise floor ~0.005)")
    print(f"   best s = {s_best:.3f}  (1-sigma from dchi2=1: {lo:.3f} to {hi:.3f}; sigma ~ {(hi-lo)/2:.4f})")
    print(f"   chi2_min/dof = {chi2_min/dof:.3f}  (chi2 at s=1: {chi2_at[1.0]:.1f}, dof {dof})")
    return rmse_L, s_best, (hi-lo)/2

# C-C pair (P-0034 C-node table, exponent 2.5)
K_C = make_K([2.5, 3.0, 3.5], [12.730, 13.202, 13.184])
r_cc = []
for rid in ["001", "002"]:
    r_cc.append(run(rid, K_C, 2.5, 0.6, "C-C, P-0034 C table extrapolated to 2.5"))

# A equilateral side 7.0 (P-0029 table, exponent 2.5), pairwise sum
K_A = make_K([5.0, 6.0, 7.0, 8.0, 9.0], [17.834, 16.617, 15.121, 13.432, 11.624])
r_tri = run("003", K_A, 2.5, 2.0, "A triangle side 7.0, P-0029 table pairwise")

print("\nSummary:")
print("C-C 2.5 runs (001,002) RMSE/L:", [round(x[0],5) for x in r_cc], " s:", [round(x[1],3) for x in r_cc])
print("triangle 003 RMSE/L:", round(r_tri[0],5), " s:", round(r_tri[1],3), "+/-", round(r_tri[2],4))
