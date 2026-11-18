# Pair-run summary for round 3 (and cross-check r3/006 vs r2/003).
# Usage: python3 -I r3_summary.py <results_root> <run_id>:<requested_separation> ...
# The fit uses the REQUESTED separation (exact initial state), not the noisy t=0 sample.
# Pure python. Separation r(t); quadratic-start acceleration fit d(t)=0.5*a*t^2 over t<=tfit.
import json, math, sys

def load(root, rid):
    return json.load(open(f"{root}/{rid}.json"))

def series(d):
    out = []
    for s in d["samples"]:
        a, b = s["particles"][0]["pos"], s["particles"][1]["pos"]
        out.append((s["t"], math.hypot(b[0]-a[0], b[1]-a[1]), a, b))
    return out

def accel_fit(rows, r0, tfit):
    # least squares for a in r(t)-r0 = 0.5*a*t^2 (exact initial rest state assumed)
    num = den = 0.0
    for t, r, _, _ in rows:
        if 0 < t <= tfit + 1e-9:
            x = 0.5 * t * t
            num += x * (r - r0)
            den += x * x
    return num / den if den else float("nan")

root = sys.argv[1]
for spec in sys.argv[2:]:
    rid, d0s = spec.rsplit(':', 1)
    d0 = float(d0s)
    d = load(root, rid)
    rows = series(d)
    def at(T):
        best = min(rows, key=lambda x: abs(x[0]-T))
        return best[1]
    first_half = next((t for t, r, _, _ in rows if r < 0.5), None)
    mn = min(rows, key=lambda x: x[1])
    a03 = accel_fit(rows, d0, 0.3)
    a06 = accel_fit(rows, d0, 0.6)
    print(f"== {rid} cost={d['cost']} nsamp={len(rows)} requested_sep={d0}")
    print(f"   r(0.5)={at(0.5):.3f} r(1.0)={at(1.0):.3f} r(1.5)={at(1.5):.3f} r(2.0)={at(2.0):.3f} r(3.0)={at(3.0):.3f}")
    print(f"   first r<0.5 at t={first_half}  min r={mn[1]:.3f} at t={mn[0]:.2f}")
    print(f"   rel. accel from 0.5 a t^2 fit: a(t<=0.3)={a03:+.3f}  a(t<=0.6)={a06:+.3f}  (+ = separating)")
