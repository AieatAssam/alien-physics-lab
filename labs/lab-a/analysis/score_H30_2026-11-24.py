"""Score H30 (A-A distance law) under the pre-registered rule (prereg_H30_2026-11-23.json).

For each run: fit K (P fixed at 2.5) to the measured positions of both particles, using
the setup positions as exact initial conditions (at rest). Model: central force K/r^P,
equal masses, RK4 step 1e-3. Chi2 at sigma 0.05 per coordinate. K found by golden-section
search on sum of squared residuals.

Usage: python3 -I score_H30_2026-11-24.py <repo_root>
"""
import json, math, os, sys

import numpy as np

ROOT = sys.argv[1]
PREREG = os.path.join(ROOT, "labs/lab-a/analysis/prereg_H30_2026-11-23.json")
RES = os.path.join(ROOT, "results/2026-11-23/r3/lab-a")
REQ = os.path.join(ROOT, "requests/2026-11-23/r3/lab-a")
P = 2.5
H = 1e-3
L = 10.0
SIG = 0.05


def load(rid):
    n = rid.split("/")[-1]
    with open(os.path.join(RES, n + ".json")) as f:
        res = json.load(f)
    with open(os.path.join(REQ, n + ".json")) as f:
        req = json.load(f)
    t = np.array([s["t"] for s in res["samples"]])
    X = np.array([[p["pos"] for p in s["particles"]] for s in res["samples"]])  # (n,2,2)
    p0 = np.array([p["pos"] for p in req["setup"]["particles"]], float)
    return t, X, p0


def simulate(p0, K, times):
    """RK4 two-body with central force K/r^P at rest start; returns positions at times."""
    x = p0.copy()
    v = np.zeros((2, 2))

    def acc(xx):
        d = xx[1] - xx[0]
        r = math.hypot(d[0], d[1])
        f = K / r ** (P + 1)
        return np.array([f * d, -f * d])

    out = np.zeros((len(times), 2, 2))
    t = 0.0
    for i, tt in enumerate(times):
        while t < tt - 1e-12:
            h = min(H, tt - t)
            a1 = acc(x); x2 = x + h / 2 * v; v2 = v + h / 2 * a1
            a2 = acc(x2); x3 = x + h / 2 * v2; v3 = v + h / 2 * a2
            a3 = acc(x3); x4 = x + h * v3; v4 = v + h * a3
            a4 = acc(x4)
            x = x + h / 6 * (v + 2 * v2 + 2 * v3 + v4)
            v = v + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
            t += h
        out[i] = x
    return out


def chi2(K, p0, t, X):
    M = simulate(p0, K, t)
    return float(np.sum((M[1:] - X[1:]) ** 2) / SIG ** 2)


def fit_K(p0, t, X):
    lo, hi = 5.0, 40.0
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = chi2(c, p0, t, X), chi2(d, p0, t, X)
    for _ in range(40):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a); fc = chi2(c, p0, t, X)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a); fd = chi2(d, p0, t, X)
    K = (a + b) / 2
    return K, chi2(K, p0, t, X)


def main():
    pre = json.load(open(PREREG))
    rows = []
    for r in pre["runs"]:
        t, X, p0 = load(r["request_id"])
        K, c2 = fit_K(p0, t, X)
        n = len(t) - 1
        # Local acceleration implied by fitted K at the initial separation
        r0 = math.dist(p0[0], p0[1])
        rows.append(dict(rid=r["request_id"], sep=r["sep"], T=r["T"], orient=r["orient"],
                         K=K, chi2_per_dof=c2 / (4 * n), r0=r0))
        print(f'{r["request_id"]} sep {r["sep"]} {r["orient"]:10s} T {r["T"]} '
              f'K {K:.3f} chi2/dof {c2/(4*n):.3f} r0 {r0:.4f}', flush=True)

    print()
    seps = sorted({r["sep"] for r in rows})
    ok_all = True
    refuted_any = False
    summary = {}
    for s in seps:
        h = [r["K"] for r in rows if r["sep"] == s and r["orient"] == "horizontal"]
        dg = [r["K"] for r in rows if r["sep"] == s and r["orient"] == "diagonal"]
        allk = h + dg
        m = float(np.mean(allk))
        mh, md = float(np.mean(h)), float(np.mean(dg))
        orient_gap = abs(mh - md) / m * 100
        dev = (m - 17.7) / 17.7 * 100
        rep_spread = (max(allk) - min(allk)) / m * 100
        summary[s] = dict(mean=m, mh=mh, md=md, dev_pct=dev, orient_gap_pct=orient_gap, spread_pct=rep_spread)
        print(f"sep {s}: mean K {m:.3f} ({dev:+.2f}% vs 17.7), horiz {mh:.3f}, diag {md:.3f}, "
              f"orient gap {orient_gap:.2f}%, replicate spread {rep_spread:.2f}%")
        if abs(dev) > 4 or orient_gap > 3:
            ok_all = False
        if abs(dev) > 8 and rep_spread <= 3:
            refuted_any = True

    print()
    if refuted_any:
        verdict = "REFUTED (K depends on separation, replicates agree)"
    elif ok_all:
        verdict = "SUPPORTED (single K=17.7, P=2.5 over sep 3-9)"
    else:
        verdict = "INCONCLUSIVE"
    print("Pre-registered verdict:", verdict)

    # Secondary: free-P slope from local accelerations (mean K-free estimate of a(r0)).
    a = {}
    for s in seps:
        ks = [r["K"] for r in rows if r["sep"] == s]
        a[s] = float(np.mean(ks)) / s ** P  # local accel implied at P=2.5 (diagnostic)
    # Free-P slope: ln(a3/a9)/ln 3 using measured per-run local accel is not directly available;
    # report the slope of log(K_fit*) vs log r using a slope on the sep-3 and sep-9 means at P=2.5 model.
    print("secondary: log-slope of local accel between sep 3 and sep 9 (using the implied a at P=2.5):",
          round(math.log(a[3.0] / a[9.0]) / math.log(3.0), 4))
    json.dump(dict(rows=rows, summary=summary, verdict=verdict), open(os.path.join(os.path.dirname(__file__), "H30_scored_2026-11-24.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
