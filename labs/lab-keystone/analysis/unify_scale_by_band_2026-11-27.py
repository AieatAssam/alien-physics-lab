"""Test a single candidate piecewise K(r) at P = 2.5 over r in [2.5, 9] against every filed A-A pair at rest with
r0 in [3, 9], T <= 2, and a result on file (any lab, any account).

Candidate table (held flat outside the nodes):
  r = 2.5 -> 16.941, 3.0 -> 18.034, 3.5 -> 18.285  (P-0034 A node table, lab-vernier)
  3.5 .. 5.0 -> linear fill (UNMEASURED GAP, an assumption: K(5) = 17.834 end of this stretch)
  r = 5 -> 17.834, 6 -> 16.617, 7 -> 15.121, 8 -> 13.432, 9 -> 11.624  (P-0029 A table, lab-a)
Per run: best-fit single scale s (sigma 0.05 per coordinate, chi2 search), and sigma_s from curvature.
Reports per r0 band: median s, mean s, and the RMS residual at s = 1 in judged units (RMSE/L).
Pure python. Reads requests/ and results/ only.
"""
import json, glob, math, os, statistics, sys

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
L = 10.0
SIG = 0.05
P = 2.5
H = 0.002

NODES_R = [2.5, 3.0, 3.5, 5.0, 6.0, 7.0, 8.0, 9.0]
NODES_K = [16.941, 18.034, 18.285, 17.834, 16.617, 15.121, 13.432, 11.624]

def K(r):
    if r <= NODES_R[0]:
        return NODES_K[0]
    if r >= NODES_R[-1]:
        return NODES_K[-1]
    for i in range(len(NODES_R) - 1):
        if NODES_R[i] <= r <= NODES_R[i + 1]:
            f = (r - NODES_R[i]) / (NODES_R[i + 1] - NODES_R[i])
            return NODES_K[i] + f * (NODES_K[i + 1] - NODES_K[i])

def simulate_pair(p0a, p0b, s, T, dt):
    # two particles at rest; returns list of (xa, ya, xb, yb) at sample times
    xa, ya = p0a; xb, yb = p0b
    va = [0.0, 0.0]; vb = [0.0, 0.0]
    pa = [xa, ya]; pb = [xb, yb]
    def acc(pa, pb):
        dx = pb[0] - pa[0]; dy = pb[1] - pa[1]
        r = math.hypot(dx, dy)
        f = s * K(r) / r ** P / r
        return [f * dx, f * dy], [-f * dx, -f * dy]
    def step(pa, va, pb, vb, h):
        a1, b1 = acc(pa, pb)
        pa2 = [pa[k] + h/2*va[k] for k in range(2)]; pb2 = [pb[k] + h/2*vb[k] for k in range(2)]
        va2 = [va[k] + h/2*a1[k] for k in range(2)]; vb2 = [vb[k] + h/2*b1[k] for k in range(2)]
        a2, b2 = acc(pa2, pb2)
        pa3 = [pa[k] + h/2*va2[k] for k in range(2)]; pb3 = [pb[k] + h/2*vb2[k] for k in range(2)]
        va3 = [va[k] + h/2*a2[k] for k in range(2)]; vb3 = [vb[k] + h/2*b2[k] for k in range(2)]
        a3, b3 = acc(pa3, pb3)
        pa4 = [pa[k] + h*va3[k] for k in range(2)]; pb4 = [pb[k] + h*vb3[k] for k in range(2)]
        va4 = [va[k] + h*a3[k] for k in range(2)]; vb4 = [vb[k] + h*b3[k] for k in range(2)]
        a4, b4 = acc(pa4, pb4)
        npa = [pa[k] + h/6*(va[k] + 2*va2[k] + 2*va3[k] + va4[k]) for k in range(2)]
        npb = [pb[k] + h/6*(vb[k] + 2*vb2[k] + 2*vb3[k] + vb4[k]) for k in range(2)]
        nva = [va[k] + h/6*(a1[k] + 2*a2[k] + 2*a3[k] + a4[k]) for k in range(2)]
        nvb = [vb[k] + h/6*(b1[k] + 2*b2[k] + 2*b3[k] + b4[k]) for k in range(2)]
        for p, v in ((npa, nva), (npb, nvb)):
            for k in range(2):
                if p[k] < 0.0:
                    p[k] = -p[k]; v[k] = -v[k]
                elif p[k] > L:
                    p[k] = 2*L - p[k]; v[k] = -v[k]
        return npa, nva, npb, nvb
    out = {0: (pa[0], pa[1], pb[0], pb[1])}
    t = 0.0
    nsamp = int(round(T / dt))
    for m in range(1, nsamp + 1):
        target = round(m * dt, 9)
        while t < target - 1e-12:
            hh = min(H, target - t)
            pa, va, pb, vb = step(pa, va, pb, vb, hh)
            t += hh
        t = target
        out[m] = (pa[0], pa[1], pb[0], pb[1])
    return out

def chi2(samples, p0a, p0b, s, T, dt):
    pred = simulate_pair(p0a, p0b, s, T, dt)
    tot = 0.0; n = 0; min_r = 1e9
    for smp in samples:
        m = smp["_idx"]
        xa, ya, xb, yb = pred[m]
        min_r = min(min_r, math.hypot(xb - xa, yb - ya))
        pts = smp["particles"]
        meas = [(pts[0]["pos"][0], pts[0]["pos"][1]), (pts[1]["pos"][0], pts[1]["pos"][1])]
        model = [(xa, ya), (xb, yb)]
        for (mx, my), (px, py) in zip(meas, model):
            tot += ((mx - px)**2 + (my - py)**2) / SIG**2
            n += 2
    return tot, n, pred, min_r

def fit_scale(samples, p0a, p0b, T, dt):
    # coarse grid then golden refinement on chi2 (unimodal in s over this range)
    grid = [0.85 + 0.01 * i for i in range(31)]
    vals = [chi2(samples, p0a, p0b, s, T, dt)[0] for s in grid]
    i = min(range(len(grid)), key=lambda k: vals[k])
    a, b = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    g = (math.sqrt(5) - 1) / 2
    c = b - g * (b - a); d = a + g * (b - a)
    fc = chi2(samples, p0a, p0b, c, T, dt)[0]; fd = chi2(samples, p0a, p0b, d, T, dt)[0]
    for _ in range(14):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a); fc = chi2(samples, p0a, p0b, c, T, dt)[0]
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a); fd = chi2(samples, p0a, p0b, d, T, dt)[0]
    s0 = (a + b) / 2
    h = 0.01
    c0, n, _, min_r = chi2(samples, p0a, p0b, s0, T, dt)
    cp = chi2(samples, p0a, p0b, s0 + h, T, dt)[0]
    cm = chi2(samples, p0a, p0b, s0 - h, T, dt)[0]
    curv = (cp + cm - 2 * c0) / (2 * h * h)
    sig_s = 1 / math.sqrt(curv) if curv > 0 else float("nan")
    c1, _, _, _ = chi2(samples, p0a, p0b, 1.0, T, dt)
    rmse1 = math.sqrt(c1 * SIG**2 / n) / L
    return s0, sig_s, c0 / (n - 1), rmse1, min_r

rows = []
for path in sorted(glob.glob(f"{REPO}/requests/*/r*/*/*.json")):
    try:
        req = json.load(open(path))
    except Exception:
        continue
    parts = req.get("setup", {}).get("particles", [])
    if len(parts) != 2 or any(p["species"] != "A" for p in parts):
        continue
    if any(any(v != 0 for v in p["vel"]) for p in parts):
        continue
    r0 = math.dist(parts[0]["pos"], parts[1]["pos"])
    T = req["setup"]["duration"]; dt = req["setup"]["sample_dt"]
    if not (3.0 <= r0 <= 9.0) or T > 2.0 + 1e-9:
        continue
    d, r, lab, n = req["request_id"].split("/")
    rp = f"{REPO}/results/{d}/{r}/{lab}/{n}.json"
    if not os.path.exists(rp):
        continue
    res = json.load(open(rp))
    samples = res.get("samples", [])
    for smp in samples:
        smp["_idx"] = int(round(smp["t"] / dt))
    rows.append((req["request_id"], r0, T, dt, parts, samples))

print(f"runs in scope: {len(rows)}", flush=True)
out = []
for rid, r0, T, dt, parts, samples in rows:
    p0a, p0b = parts[0]["pos"], parts[1]["pos"]
    s0, sig_s, chi_dof, rmse1, min_r = fit_scale(samples, p0a, p0b, T, dt)
    out.append((r0, rid, T, s0, sig_s, chi_dof, rmse1, min_r))
    print(f"{rid:34s} r0={r0:5.2f} T={T:4.1f} s={s0:.4f}+/-{sig_s:.4f} chi2/dof={chi_dof:6.3f} RMSE/L(s=1)={rmse1:.5f} minr_model={min_r:.2f}", flush=True)

json.dump([dict(r0=o[0], rid=o[1], T=o[2], s=o[3], sig_s=o[4], chi2_dof=o[5], rmse_L_s1=o[6], min_r_model=o[7]) for o in out],
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "unify_scale_by_band_2026-11-27.json"), "w"), indent=1)
bands = [(3.0, 3.5), (3.5, 4.5), (4.5, 5.5), (5.5, 7.0), (7.0, 8.0), (8.0, 9.01)]
print("\nBand summary (per-run scale s; weighted mean with sigma_s; median; RMSE/L at s=1 median):")
for lo, hi in bands:
    sel = [o for o in out if lo <= o[0] < hi and o[4] == o[4]]
    if not sel:
        print(f"  [{lo},{hi}) no runs"); continue
    w = [1 / o[4]**2 for o in sel]
    wm = sum(wi * o[3] for wi, o in zip(w, sel)) / sum(w)
    wse = 1 / math.sqrt(sum(w))
    med = statistics.median([o[3] for o in sel])
    rm = statistics.median([o[6] for o in sel])
    print(f"  [{lo},{hi}) n={len(sel):3d}  wmean s={wm:.4f} +/- {wse:.4f}  median s={med:.4f}  median RMSE/L(s=1)={rm:.5f}")
