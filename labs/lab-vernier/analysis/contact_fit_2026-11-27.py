"""Smoothed contact-probe trajectories and softened-core fits for 2026-11-27/r1/lab-vernier/001 (r0 1.0) and 002 (r0 1.5).

Model family: relative separation r'' = -G / max(r, rc)^P (G = 23.63, P = 2.099 fixed; rc = 0 is the bare law).
rc is the softening radius. Fit rc on the window where the measured trajectory is above the tracker-noise
floor (separation >= 0.25 and t before the first separation below 0.25), then look at the post-window data.
Run: python3 -I contact_fit_2026-11-27.py <repo-root>
"""
import json
import math
import sys

G, P = 23.63, 2.099
REPO = sys.argv[1] if len(sys.argv) > 1 else "/home/runner/work/alien-physics-lab/alien-physics-lab"


def load(rid):
    res = json.load(open(f"{REPO}/results/{rid}.json"))
    return [(s["t"], math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"])) for s in res["samples"]]


def smooth(seps, dt=0.01):
    """Average separation in bins of width dt (centre times)."""
    out = {}
    for t, d in seps:
        k = round(t / dt)
        out.setdefault(k, []).append(d)
    return [(k * dt, sum(v) / len(v), len(v)) for k, v in sorted(out.items())]


def sim(r0, rc, t_end, h=2e-5):
    """Return list of (t, r) for the softened law, stopping at r = 0.005 or t_end."""
    r, v, t = r0, 0.0, 0.0
    out = [(0.0, r0)]
    while t < t_end:
        def f(rr, vv):
            return vv, -G / max(rr, rc) ** P if rc > 0 else -G / rr ** P
        k1r, k1v = f(r, v)
        k2r, k2v = f(r + h / 2 * k1r, v + h / 2 * k1v)
        k3r, k3v = f(r + h / 2 * k2r, v + h / 2 * k2v)
        k4r, k4v = f(r + h * k3r, v + h * k3v)
        r = r + h / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
        v = v + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        t += h
        if r < 0.005:
            break
        out.append((t, r))
    return out


def val_at(track, t):
    for (t0, r0_), (t1, r1_) in zip(track, track[1:]):
        if t0 <= t <= t1:
            return r0_ + (r1_ - r0_) * (t - t0) / (t1 - t0)
    return None


def window_rmse(seps, track, lo, hi):
    errs = []
    for t, d in seps:
        if lo <= t <= hi:
            p = val_at(track, t)
            if p is not None:
                errs.append(d - p)
    return math.sqrt(sum(e * e for e in errs) / len(errs)), len(errs)


def main():
    for rid, r0 in (("2026-11-27/r1/lab-vernier/001", 1.0), ("2026-11-27/r1/lab-vernier/002", 1.5)):
        seps = load(rid)
        sm = smooth(seps)
        print(f"== {rid} r0={r0}  smoothed (dt 0.01, n per bin ~33)")
        print("  t      smooth_sep  ")
        for t, d, n in sm:
            if t <= 0.61 and t >= 0.0:
                print(f"  {t:.2f}  {d:.3f}")
        # first time the smoothed trace drops below 0.25
        t_lo = next((t for t, d, n in sm if d < 0.25), None)
        print(f"  smoothed first < 0.25 at t={t_lo}")
        # fit rc on the window t in [0, t_lo - 0.02] (above the noise floor)
        hi = (t_lo or 0.3) - 0.02
        best = None
        for rc in [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]:
            track = sim(r0, rc, 0.62)
            rm, n = window_rmse(seps, track, 0.0, hi)
            print(f"  rc={rc:.2f}: RMSE(sep - model) on t in [0,{hi:.3f}] = {rm:.4f} (n={n})")
            if best is None or rm < best[1]:
                best = (rc, rm)
        print(f"  best rc on pre-contact window: {best[0]} (RMSE {best[1]:.4f})")


if __name__ == "__main__":
    main()
