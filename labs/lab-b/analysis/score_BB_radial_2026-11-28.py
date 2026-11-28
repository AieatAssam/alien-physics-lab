"""Score the 2026-11-27 round-3 radial runs (lab-b) against prereg_BB_radial_2026-11-27.json.
Pure Python. Run: python3 -I <this> <repo_root>
Model per run: relative separation r = |x1 - x0| along the axis of motion, released at rest at r0 = 9.
r'' = -S(r)/r^2.5, S = sum of the two particles' coefficients, piecewise constant in bands.
Window: samples with observed separation <= 2.0 are dropped before the residual sum.
Same-species pairs: S = 2 K_species. A-B: S = K_A (1 + 1.41) (H20 convention, not a free fit).
"""
import json, math, os, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
P = 2.5
BANDS = [(8.0, 9.5), (6.0, 8.0), (4.0, 6.0), (2.0, 4.0)]
WINDOW = 2.0
H = 0.002

def load(path_req, path_res):
    req = json.load(open(os.path.join(REPO, path_req)))
    res = json.load(open(os.path.join(REPO, path_res)))
    ps = req["setup"]["particles"]
    p0, p1 = ps[0]["pos"], ps[1]["pos"]
    axis = 0 if abs(p1[0] - p0[0]) > abs(p1[1] - p0[1]) else 1
    sp = "".join(p["species"] for p in ps)
    t, r_obs = [], []
    for s in res["samples"]:
        a, b = s["particles"][0]["pos"], s["particles"][1]["pos"]
        t.append(s["t"]); r_obs.append(b[axis] - a[axis])
    return dict(sp=sp, r0=abs(p1[axis] - p0[axis]), t=t, r=r_obs, status=res.get("status"), cost=res.get("cost"))

def band_of(r):
    for k, (lo, hi) in enumerate(BANDS):
        if lo <= r < hi:
            return k
    return 0 if r >= BANDS[0][1] else len(BANDS) - 1

def sim(svals, times, r0):
    def acc(r):
        return -svals[band_of(r)] / max(r, 0.05) ** P
    r, v, tt = r0, 0.0, 0.0
    out = {}
    for target in sorted(set(round(x, 9) for x in times)):
        while tt < target - 1e-12:
            h = min(H, target - tt)
            k1r, k1v = v, acc(r)
            k2r, k2v = v + h/2*k1v, acc(r + h/2*k1r)
            k3r, k3v = v + h/2*k2v, acc(r + h/2*k2r)
            k4r, k4v = v + h*k3v, acc(r + h*k3r)
            r += h/6*(k1r + 2*k2r + 2*k3r + k4r)
            v += h/6*(k1v + 2*k2v + 2*k3v + k4v)
            tt += h
            if r <= 0.05:
                r, v = 0.05, 0.0
        out[target] = r
    return out

def solve(M, b):
    n = len(b)
    A = [row[:] + [b[i]] for i, row in enumerate(M)]
    for c in range(n):
        piv = max(range(c, n), key=lambda q: abs(A[q][c]))
        A[c], A[piv] = A[piv], A[c]
        for q in range(n):
            if q != c:
                f = A[q][c] / A[c][c]
                for k in range(c, n + 1):
                    A[q][k] -= f * A[c][k]
    return [A[i][n] / A[i][i] for i in range(n)]

def fit_bands(d):
    keep = [i for i, rv in enumerate(d["r"]) if rv > WINDOW and d["t"][i] > 0]
    tk = [d["t"][i] for i in keep]; rk = [d["r"][i] for i in keep]
    pop = sorted(set(band_of(rv) for rv in rk))  # populated bands only; empty bands are not fitted
    def full(q):
        sv = [0.0]*len(BANDS)
        for k in range(len(BANDS)):
            near = min(pop, key=lambda j: abs(j-k))
            sv[k] = q[pop.index(near)]
        return sv
    def resid(q):
        m = sim(full(q), tk, d["r0"])
        return [ro - m[round(tt, 9)] for tt, ro in zip(tk, rk)]
    def chi(q):
        if any(x <= 0 for x in q):
            return float("inf")
        return sum(x*x for x in resid(q))
    n = len(pop)
    q = [10.0]*n
    lam = 1e-3
    for _ in range(25):
        r0v = resid(q); c0 = sum(x*x for x in r0v)
        J = []
        for k in range(n):
            qk = list(q); eps = 1e-4*max(1.0, abs(q[k])); qk[k] += eps
            J.append([(a-b)/eps for a, b in zip(resid(qk), r0v)])
        A = [[sum(J[i][m]*J[j][m] for m in range(len(r0v))) for j in range(n)] for i in range(n)]
        g = [sum(J[i][m]*r0v[m] for m in range(len(r0v))) for i in range(n)]
        imp = False
        for _t in range(8):
            M = [[A[i][j] + (lam*(1+A[i][i]) if i == j else 0.0) for j in range(n)] for i in range(n)]
            st = solve(M, g)
            qn = [q[i]-st[i] for i in range(n)]
            if chi(qn) < c0:
                q, lam, imp = qn, lam/3, True
                break
            lam *= 4
        if not imp:
            break
    rf = resid(q)
    s2 = sum(x*x for x in rf)/(len(rf)-n)
    J = []
    for k in range(n):
        qk = list(q); eps = 1e-4*max(1.0, abs(q[k])); qk[k] += eps
        J.append([(a-b)/eps for a, b in zip(resid(qk), rf)])
    A = [[sum(J[i][m]*J[j][m] for m in range(len(rf))) for j in range(n)] for i in range(n)]
    cols = [solve(A, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    # map to all four bands: empty bands report None
    S_out = [None]*len(BANDS); E_out = [None]*len(BANDS)
    for idx, k in enumerate(pop):
        S_out[k] = q[idx]; E_out[k] = math.sqrt(s2*cols[idx][idx])
    return S_out, E_out, math.sqrt(s2), len(keep)

RUNS = {
    "BB_horiz_001": ("requests/2026-11-27/r3/lab-b/001.json", "results/2026-11-27/r3/lab-b/001.json"),
    "AA_horiz_002": ("requests/2026-11-27/r3/lab-b/002.json", "results/2026-11-27/r3/lab-b/002.json"),
    "BB_vert_003":  ("requests/2026-11-27/r3/lab-b/003.json", "results/2026-11-27/r3/lab-b/003.json"),
    "AB_vert_004":  ("requests/2026-11-27/r3/lab-b/004.json", "results/2026-11-27/r3/lab-b/004.json"),
    "AB_horiz_H20": ("requests/2026-11-25/r3/lab-b/001.json", "results/2026-11-25/r3/lab-b/001.json"),
}
fits = {}
for name, (rq, rs) in RUNS.items():
    d = load(rq, rs)
    if d["status"] != "ok":
        print(name, "status", d["status"]); continue
    p, err, sd, n = fit_bands(d)
    fits[name] = (p, err)
    print(f"{name} [{d['sp']}] r0={d['r0']:.2f} n_kept={n} resid_sd={sd:.4f}")
    for k, (lo, hi) in enumerate(BANDS):
        if p[k] is None:
            print(f"    band [{lo},{hi}): no samples"); continue
        print(f"    band [{lo},{hi}): S = {p[k]:8.3f} +/- {err[k]:.3f}")

print("H23 shared-law test: S_BB/S_AA per band (001 vs 002, same geometry)")
if "BB_horiz_001" in fits and "AA_horiz_002" in fits:
    pb, eb = fits["BB_horiz_001"]; pa, ea = fits["AA_horiz_002"]
    rat = []
    for k, (lo, hi) in enumerate(BANDS):
        if pb[k] is None or pa[k] is None:
            rat.append((None, None)); print(f"    band [{lo},{hi}): not comparable (no samples in one run)"); continue
        R = pb[k]/pa[k]
        se = R*math.sqrt((eb[k]/pb[k])**2 + (ea[k]/pa[k])**2)
        rat.append((R, se))
        print(f"    band [{lo},{hi}): ratio = {R:.4f} +/- {se:.4f}")
    i, j = 2, 0  # band [4,6) vs [8,9.5) -- prereg names bands 3-4 and 8-9.5
    if rat[3][0] is None or rat[0][0] is None:
        print("    bands [2,4) vs [8,9.5): not comparable; band [2,4) has no B-B samples")
        diff = None
    else:
        diff = rat[3][0] - rat[0][0]
    if diff is not None:
        print(f"    bands [2,4) vs [8,9.5): diff = {diff:+.4f}, combined se {math.sqrt(rat[3][1]**2+rat[0][1]**2):.4f}, "
          f"z = {diff/math.sqrt(rat[3][1]**2+rat[0][1]**2):+.2f}")
if "BB_horiz_001" in fits and "BB_vert_003" in fits:
    print("H20-style orientation check (B-B): horizontal 001 vs vertical 003, S per band")
    for k, (lo, hi) in enumerate(BANDS):
        a, ea = fits["BB_horiz_001"][0][k], fits["BB_horiz_001"][1][k]
        b, eb = fits["BB_vert_003"][0][k], fits["BB_vert_003"][1][k]
        if a is None or b is None:
            print(f"    band [{lo},{hi}): no samples in one run"); continue
        if a is None or b is None:
            print(f"    band [{lo},{hi}): no samples in one run"); continue
        z = (a-b)/math.sqrt(ea*ea+eb*eb)
        print(f"    band [{lo},{hi}): z = {z:+.2f}")
if "AB_vert_004" in fits and "AB_horiz_H20" in fits:
    print("Orientation check (A-B): vertical 004 vs horizontal H20, S per band")
    for k, (lo, hi) in enumerate(BANDS):
        a, ea = fits["AB_vert_004"][0][k], fits["AB_vert_004"][1][k]
        b, eb = fits["AB_horiz_H20"][0][k], fits["AB_horiz_H20"][1][k]
        if a is None or b is None:
            print(f"    band [{lo},{hi}): no samples in one run"); continue
        z = (a-b)/math.sqrt(ea*ea+eb*eb)
        print(f"    band [{lo},{hi}): z = {z:+.2f}")
