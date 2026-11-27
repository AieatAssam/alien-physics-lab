"""H20 scoring (lab-b, 2026-11-27). Pure Python, no numpy.

Run: python3 -I <this> <repo_root>
Data: results/2026-11-25/r3/lab-b/001.json (A at x=0.5, B at x=9.5, y=5, at rest, T=12, tracker only).

Part 1: mass/coefficient ratio from momentum conservation along x.
  Equal and opposite central forces: m_A*(xA-xA0) + m_B*(xB-xB0) = 0, so
  q = m_B/m_A = -sum(dA*dB)/sum(dB^2).  Ratio K_B/K_A = m_A/m_B = 1/q.  H20 says 1.41.
Part 2: radial fit. Relative separation r(t) obeys r'' = -S(r)/r^2.5 with S = K_A + K_B = K_A*(1+1.41).
  S is piecewise constant in bands; fit by Gauss-Newton on the tracker separation (x_B - x_A).
  K_A(r) = S(r)/2.41.
"""
import json, math, os, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
RUN = os.path.join(REPO, "results/2026-11-25/r3/lab-b/001.json")
P = 2.5
SUM_FACTOR = 2.41  # 1 + K_B/K_A under H20 convention

d = json.load(open(RUN))
S = d["samples"]
t = [s["t"] for s in S]
xA = [s["particles"][0]["pos"][0] for s in S]
xB = [s["particles"][1]["pos"][0] for s in S]
x0A, x0B = 0.5, 9.5  # true start from setup (not the noisy t=0 sample)

# ---- Part 1: momentum-conservation ratio
dA = [a - x0A for a in xA[1:]]
dB = [b - x0B for b in xB[1:]]
num = -sum(a * b for a, b in zip(dA, dB))
den = sum(b * b for b in dB)
q = num / den
# residual scatter -> standard error of q (regression through origin)
res = [a + q * b for a, b in zip(dA, dB)]
s2 = sum(r * r for r in res) / (len(res) - 1)
se_q = math.sqrt(s2 / den)
print(f"Part 1: q = m_B/m_A = {q:.4f} +/- {se_q:.4f}  -> K_B/K_A = {1/q:.4f} +/- {se_q/q**2:.4f}")
print(f"        H20 prediction 1.41 (q = 0.7092). Deviation from 1.41: {1/q-1.41:+.4f} = {(1/q-1.41)/(se_q/q**2):+.2f} sigma")

# ---- Part 2: radial fit of S(r) in bands
r_obs = [b - a for a, b in zip(xA, xB)]
BANDS = [(8.0, 9.5), (6.0, 8.0), (4.0, 6.0), (2.0, 4.0)]  # band edges in r (upper-inclusive grid)
R0 = 9.0
H = 0.002

def band_index(r):
    for k, (lo, hi) in enumerate(BANDS):
        if lo <= r < hi:
            return k
    return None  # outside, treat as nearest

def sim(svals, times):
    """Integrate relative coord r from R0 at rest; svals per band (fallback to nearest band)."""
    def accel(r):
        k = band_index(r)
        if k is None:
            k = 0 if r >= BANDS[0][1] else len(BANDS) - 1
        return -svals[k] / max(r, 0.05) ** P
    r, v, tt = R0, 0.0, 0.0
    out = {}
    tset = sorted(set(round(x, 9) for x in times))
    idx = 0
    for target in tset:
        while tt < target - 1e-12:
            h = min(H, target - tt)
            k1r, k1v = v, accel(r)
            k2r, k2v = v + h/2*k1v, accel(r + h/2*k1r)
            k3r, k3v = v + h/2*k2v, accel(r + h/2*k2r)
            k4r, k4v = v + h*k3v, accel(r + h*k3r)
            r += h/6*(k1r + 2*k2r + 2*k3r + k4r)
            v += h/6*(k1v + 2*k2v + 2*k3v + k4v)
            tt += h
            if r <= 0.05:
                r = 0.05
                v = 0.0
        out[target] = r
    return out

def residuals(svals):
    model = sim(svals, t)
    return [ro - model[round(tt, 9)] for tt, ro in zip(t, r_obs)]

def chi2(svals):
    if any(v <= 0.0 for v in svals):
        return float('inf')  # S must be positive (attraction)
    return sum(x * x for x in residuals(svals))

def fit(p0, iters=25):
    p = list(p0)
    lam = 1e-3
    for _ in range(iters):
        r0v = residuals(p)
        c0 = sum(x*x for x in r0v)
        # numerical Jacobian of residuals
        J = []
        for k in range(len(p)):
            pk = list(p); eps = 1e-4 * max(1.0, abs(p[k]))
            pk[k] += eps
            rk = residuals(pk)
            J.append([(a - b) / eps for a, b in zip(rk, r0v)])
        n = len(p)
        A = [[sum(J[i][m]*J[j][m] for m in range(len(r0v))) for j in range(n)] for i in range(n)]
        g = [sum(J[i][m]*r0v[m] for m in range(len(r0v))) for i in range(n)]
        improved = False
        for _try in range(8):
            M = [[A[i][j] + (lam * (1 + A[i][i]) if i == j else 0.0) for j in range(n)] for i in range(n)]
            step = solve(M, g)
            pn = [p[i] - step[i] for i in range(n)]
            cn = chi2(pn)
            if cn < c0:
                p, lam, improved = pn, lam / 3, True
                break
            lam *= 4
        if not improved:
            break
    # covariance from final Jacobian
    rf = residuals(p)
    sig2 = sum(x*x for x in rf) / (len(rf) - len(p))
    J = []
    for k in range(len(p)):
        pk = list(p); eps = 1e-4 * max(1.0, abs(p[k])); pk[k] += eps
        rk = residuals(pk)
        J.append([(a - b) / eps for a, b in zip(rk, rf)])
    n = len(p)
    A = [[sum(J[i][m]*J[j][m] for m in range(len(rf))) for j in range(n)] for i in range(n)]
    cov = invert(A)
    err = [math.sqrt(sig2 * cov[i][i]) for i in range(n)]
    return p, err, sig2

def solve(M, b):
    n = len(b)
    A = [row[:] + [b[i]] for i, row in enumerate(M)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[piv] = A[piv], A[c]
        for r in range(n):
            if r != c:
                f = A[r][c] / A[c][c]
                for k in range(c, n + 1):
                    A[r][k] -= f * A[c][k]
    return [A[i][n] / A[i][i] for i in range(n)]

def invert(M):
    n = len(M)
    cols = []
    for j in range(n):
        e = [1.0 if i == j else 0.0 for i in range(n)]
        cols.append(solve(M, e))
    return [[cols[j][i] for j in range(n)] for i in range(n)]

# Single-constant fit first (S flat across bands)
# Use one parameter for flat: refit with all bands tied
def flat_chi2(sv):
    return chi2([sv, sv, sv, sv])  # sv is a scalar S
lo, hi = 5.0, 40.0
for _ in range(80):
    a = lo + (hi - lo) / 3; b = hi - (hi - lo) / 3
    if flat_chi2(a) < flat_chi2(b):
        hi = b
    else:
        lo = a
S_flat = 0.5 * (lo + hi)
print(f"Part 2a: single S (K flat across bands): S = {S_flat:.3f}, K_A = S/2.41 = {S_flat/SUM_FACTOR:.3f}, chi2 = {flat_chi2(S_flat):.4f}")

p, err, sig2 = fit([S_flat]*4)
print("Part 2b: band-wise S(r) (free per band), residual sd per sample = %.4f (tracker sd 0.05 x sqrt2 ~ 0.0707 expected)" % math.sqrt(sig2))
for k, (lo_b, hi_b) in enumerate(BANDS):
    print(f"   band r in [{lo_b:.1f},{hi_b:.1f}): S = {p[k]:7.3f} +/- {err[k]:.3f}   K_A = {p[k]/SUM_FACTOR:7.3f} +/- {err[k]/SUM_FACTOR:.3f}")
print(f"   chi2 free-bands = {chi2(p):.4f}  vs flat = {flat_chi2(S_flat):.4f}")

# P-0025 table for comparison (A-B, K_A nodes), converted to S
TAB = {4.0: 9.10, 5.0: 9.26, 6.0: 8.52, 7.0: 7.75, 8.0: 6.85}
print("P-0025 table K_A -> S (x2.41): " + ", ".join(f"r={k:.0f}: S={v*SUM_FACTOR:.2f}" for k, v in TAB.items()))

# ---- Part 3: band-wise ratio. Momentum conservation holds at every t, so within any
# sub-interval the slope of x_A against x_B is -q (= -m_B/m_A). Regress x_A on x_B per band
# (samples whose observed separation falls in the band), with intercept.
print("Part 3: band-wise ratio K_B/K_A = 1/q from slope of x_A on x_B within each band")
for lo_b, hi_b in BANDS:
    idx = [i for i in range(1, len(t)) if lo_b <= r_obs[i] < hi_b]
    if len(idx) < 10:
        print(f"   band [{lo_b:.1f},{hi_b:.1f}): too few samples ({len(idx)})")
        continue
    xs = [xB[i] for i in idx]; ys = [xA[i] for i in idx]
    mx = sum(xs)/len(xs); my = sum(ys)/len(ys)
    sxx = sum((a-mx)**2 for a in xs); sxy = sum((a-mx)*(b-my) for a, b in zip(xs, ys))
    slope_naive = sxy / sxx
    # errors-in-variables: x_B carries tracker noise sd 0.05; remove its variance from sxx
    SIG2 = 0.05 ** 2
    sxx_c = sxx - len(xs) * SIG2
    slope = sxy / sxx_c
    resid = [b - my - slope*(a-mx) for a, b in zip(xs, ys)]
    s2 = sum(e*e for e in resid)/(len(xs)-2)
    se = math.sqrt(s2/sxx_c)
    qb = -slope
    print(f"   band [{lo_b:.1f},{hi_b:.1f}): n={len(idx)}, x_B range {min(xs):.2f}-{max(xs):.2f}, "
          f"sd(x_B)={math.sqrt(sxx/len(xs)):.3f}, naive q={-slope_naive:.4f}, "
          f"EIV-corrected q = {qb:.4f} +/- {se:.4f} -> K_B/K_A = {1/qb:.3f} +/- {se/qb**2:.3f}")
